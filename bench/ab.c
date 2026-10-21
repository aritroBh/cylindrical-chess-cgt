/* ab.c - whole-board alpha-beta for pawn-only games (ChessSums baseline).
 *
 * Same rules, same move order and same node counting as bench/baseline.py
 * (Solver): pawns in (file, rank) order; per pawn: single push, double push,
 * capture towards file-1, capture towards file+1 (en passant included).
 * Values are +1 / -1 for the side to move; the window is always (-1, +1), so
 * every node result is exact and can be stored in the transposition table.
 *
 * Build:  cc -O2 -o bench/ab bench/ab.c
 * Input (stdin), one job per line:
 *   files wrap side tt node_cap time_cap nW f r f r ... nB f r f r ...
 *   (side 1 = White to move; files 0-based; ranks 1..8)
 * Output, one line per job:  result nodes cpu_seconds ep_events (time_cap is also CPU seconds)
 *   result 1 = side to move wins, -1 = loses, 0 = cap reached (unsolved)
 *   ep_events = double steps made during the search after which the moved pawn
 *   is passed (textbook test) and an enemy pawn stands beside it, so that the
 *   opponent could take a passed pawn en passant. This search uses the
 *   textbook passed test. The e.p.-aware test (a pawn that can still be taken
 *   e.p. is not passed) judges a position differently only right after such a
 *   double step, so ep_events == 0 certifies that the e.p.-aware search would
 *   visit the same nodes and return the same result.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXF 26
#define R 8

static int W, WRAP;
static signed char sq[MAXF][R + 2]; /* 0 empty, 1 white, 2 black */
static long long nodes, node_cap, ep_events;
static double t_end;
static int use_tt, capped;
static uint64_t Z[MAXF][R + 2][3], ZSIDE, ZEP[MAXF][R + 2];

#define TTBITS 24
static uint64_t *tt_key;
static signed char *tt_val;

static double now(void) {
    struct timespec ts;
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts); /* CPU time: robust to a loaded machine */
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

static uint64_t rng_state = 0x9E3779B97F4A7C15ULL;
static uint64_t rnd(void) {
    uint64_t z = (rng_state += 0x9E3779B97F4A7C15ULL);
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}

static int nb(int f, int df) {
    int g = f + df;
    if (WRAP) return (g % W + W) % W;
    return (g >= 0 && g < W) ? g : -1;
}

/* does `color` (1 white, 2 black) have a passed pawn? */
static int has_passer(int color) {
    int maxB[MAXF], minW[MAXF];
    for (int f = 0; f < W; f++) {
        maxB[f] = 0; minW[f] = 9;
        for (int r = 1; r <= R; r++) {
            if (sq[f][r] == 2 && r > maxB[f]) maxB[f] = r;
            if (sq[f][r] == 1 && r < minW[f]) minW[f] = r;
        }
    }
    for (int f = 0; f < W; f++) {
        int fs[3] = {f, nb(f, -1), nb(f, 1)};
        for (int r = 1; r <= R; r++) {
            if (sq[f][r] != color) continue;
            int blocked = 0;
            for (int i = 0; i < 3; i++) {
                int g = fs[i];
                if (g < 0) continue;
                if (color == 1 && maxB[g] > r) blocked = 1;
                if (color == 2 && minW[g] < r) blocked = 1;
            }
            if (!blocked) return 1;
        }
    }
    return 0;
}

/* Per-file extreme ranks, kept up to date on make/unmake. Because every
 * searched node has no passed pawn (a passer ends the game), a move can only
 * create a passer on the files next to its from- and to-squares, so the check
 * after a move looks at those files only (full_mode falls back to a whole-board
 * scan when the root already has a passer). Results are identical. */
static int maxW[MAXF], minW[MAXF], maxB[MAXF], minB[MAXF], full_mode;

static void refresh(int f) {
    maxW[f] = 0; maxB[f] = 0; minW[f] = 9; minB[f] = 9;
    for (int r = 1; r <= R; r++) {
        if (sq[f][r] == 1) { if (r > maxW[f]) maxW[f] = r; if (r < minW[f]) minW[f] = r; }
        else if (sq[f][r] == 2) { if (r > maxB[f]) maxB[f] = r; if (r < minB[f]) minB[f] = r; }
    }
}

/* textbook test for one pawn: no enemy pawn ahead on its own or an adjacent file */
static int pawn_passed(int color, int f, int r) {
    int fs[3] = {f, nb(f, -1), nb(f, 1)};
    for (int i = 0; i < 3; i++) {
        int g = fs[i];
        if (g < 0) continue;
        if (color == 1 && maxB[g] > r) return 0;
        if (color == 2 && minW[g] < r) return 0;
    }
    return 1;
}

static int passer_on_file(int color, int g) {
    int a = nb(g, -1), b = nb(g, 1);
    if (color == 1) {
        if (!maxW[g]) return 0;
        int m = maxB[g];
        if (a >= 0 && maxB[a] > m) m = maxB[a];
        if (b >= 0 && maxB[b] > m) m = maxB[b];
        return m <= maxW[g];
    }
    if (minB[g] == 9) return 0;
    int m = minW[g];
    if (a >= 0 && minW[a] < m) m = minW[a];
    if (b >= 0 && minW[b] < m) m = minW[b];
    return m >= minB[g];
}

static int passer_near(int color, int f1, int f2) {
    int fs[6] = {f1, nb(f1, -1), nb(f1, 1), f2, nb(f2, -1), nb(f2, 1)};
    for (int i = 0; i < 6; i++)
        if (fs[i] >= 0 && passer_on_file(color, fs[i])) return 1;
    return 0;
}

/* moves to promote for the best passed front pawn (cylcgt "count" rule) */
static int dist(int color) {
    int best = 1000000;
    for (int f = 0; f < W; f++) {
        int fs[3] = {f, nb(f, -1), nb(f, 1)};
        for (int r = 1; r <= R; r++) {
            if (sq[f][r] != color) continue;
            int blocked = 0, ahead = 0;
            for (int i = 0; i < 3; i++) {
                int g = fs[i];
                if (g < 0) continue;
                for (int s = 1; s <= R; s++) {
                    if (color == 1 && s > r && sq[g][s] == 2) blocked = 1;
                    if (color == 2 && s < r && sq[g][s] == 1) blocked = 1;
                }
            }
            for (int s = 1; s <= R; s++)
                if (sq[f][s] && ((color == 1 && s > r) || (color == 2 && s < r))) ahead = 1;
            if (blocked || ahead) continue;
            int d = color == 1 ? R - r - (r == 2) : r - 1 - (r == R - 1);
            if (d < best) best = d;
        }
    }
    return best;
}

static uint64_t hash_pos(int side_white, int epf, int epr) {
    uint64_t h = side_white ? ZSIDE : 0;
    for (int f = 0; f < W; f++)
        for (int r = 1; r <= R; r++)
            if (sq[f][r]) h ^= Z[f][r][(int)sq[f][r]];
    if (epf >= 0) h ^= ZEP[epf][epr];
    return h;
}

typedef struct { signed char ff, fr, tf, tr, cf, cr, epf, epr; } Move; /* cf/cr: captured square or -1 */

/* ep target square (epf, epr) usable by the side to move, captured pawn at (epcf, epcr) */
static int negamax(int side_white, int epf, int epr, int epcf, int epcr) {
    nodes++;
    if (node_cap > 0 && nodes > node_cap) { capped = 1; return 0; }
    if ((nodes & 0xFFFF) == 0 && t_end > 0 && now() > t_end) { capped = 1; return 0; }
    uint64_t key = 0;
    size_t slot = 0;
    if (use_tt) {
        key = hash_pos(side_white, epf, epr);
        slot = key & ((1ULL << TTBITS) - 1);
        if (tt_key[slot] == key && tt_val[slot]) return tt_val[slot];
    }
    int me = side_white ? 1 : 2, them = side_white ? 2 : 1;
    int d = side_white ? 1 : -1, start = side_white ? 2 : R - 1;
    Move mv[128];
    int n = 0;
    for (int f = 0; f < W; f++) {
        for (int r = 1; r <= R; r++) {
            if (sq[f][r] != me) continue;
            int r1 = r + d;
            if (r1 < 1 || r1 > R) continue;
            if (!sq[f][r1]) {
                mv[n++] = (Move){f, r, f, r1, -1, -1, -1, -1};
                int r2 = r + 2 * d;
                if (r == start && !sq[f][r2]) mv[n++] = (Move){f, r, f, r2, -1, -1, f, r1};
            }
            for (int k = 0; k < 2; k++) {
                int g = nb(f, k == 0 ? -1 : 1);
                if (g < 0) continue;
                if (sq[g][r1] == them) mv[n++] = (Move){f, r, g, r1, g, r1, -1, -1};
                else if (epf == g && epr == r1) mv[n++] = (Move){f, r, g, r1, epcf, epcr, -1, -1};
            }
        }
    }
    int best = -1;
    for (int i = 0; i < n; i++) {
        Move m = mv[i];
        int captured = 0;
        if (m.cf >= 0) { captured = sq[(int)m.cf][(int)m.cr]; sq[(int)m.cf][(int)m.cr] = 0; }
        sq[(int)m.ff][(int)m.fr] = 0;
        sq[(int)m.tf][(int)m.tr] = me;
        refresh(m.ff);
        if (m.tf != m.ff) refresh(m.tf);
        if (m.epf >= 0) { /* double step: is the pawn passed, and could the opponent take it en passant? */
            int a = nb(m.tf, -1), b = nb(m.tf, 1);
            if (((a >= 0 && sq[a][(int)m.tr] == them) || (b >= 0 && sq[b][(int)m.tr] == them))
                && pawn_passed(me, m.tf, m.tr))
                ep_events++;
        }
        int wp, bp, v;
        if (full_mode) { wp = has_passer(1); bp = has_passer(2); }
        else { wp = passer_near(1, m.ff, m.tf); bp = passer_near(2, m.ff, m.tf); }
        if (wp != bp) v = (wp == side_white) ? 1 : -1;
        else if (wp) {
            int dm = dist(me), dop = dist(them);
            v = dop <= dm ? -1 : 1;
        } else {
            v = -negamax(!side_white, m.epf, m.epr, m.tf, m.tr);
        }
        sq[(int)m.tf][(int)m.tr] = 0;
        sq[(int)m.ff][(int)m.fr] = me;
        if (m.cf >= 0) sq[(int)m.cf][(int)m.cr] = captured;
        refresh(m.ff);
        if (m.tf != m.ff) refresh(m.tf);
        if (capped) return 0;
        if (v > best) best = v;
        if (best == 1) break;
    }
    if (use_tt) { tt_key[slot] = key; tt_val[slot] = (signed char)best; }
    return best;
}

int main(void) {
    for (int f = 0; f < MAXF; f++)
        for (int r = 0; r < R + 2; r++) {
            for (int c = 0; c < 3; c++) Z[f][r][c] = rnd();
            ZEP[f][r] = rnd();
        }
    ZSIDE = rnd();
    tt_key = calloc((size_t)1 << TTBITS, sizeof(uint64_t));
    tt_val = calloc((size_t)1 << TTBITS, 1);
    int side, tt;
    double tcap;
    while (scanf("%d %d %d %d %lld %lf", &W, &WRAP, &side, &tt, &node_cap, &tcap) == 6) {
        memset(sq, 0, sizeof sq);
        for (int c = 1; c <= 2; c++) {
            int k, f, r;
            if (scanf("%d", &k) != 1) return 1;
            for (int i = 0; i < k; i++) {
                if (scanf("%d %d", &f, &r) != 2) return 1;
                sq[f][r] = c;
            }
        }
        for (int f = 0; f < W; f++) refresh(f);
        full_mode = has_passer(1) || has_passer(2);
        use_tt = tt;
        if (use_tt) { memset(tt_key, 0, sizeof(uint64_t) << TTBITS); memset(tt_val, 0, (size_t)1 << TTBITS); }
        nodes = 0; capped = 0; ep_events = 0;
        double t0 = now();
        t_end = tcap > 0 ? t0 + tcap : 0;
        int v = negamax(side, -1, -1, -1, -1);
        printf("%d %lld %.6f %lld\n", capped ? 0 : v, nodes, now() - t0, ep_events);
        fflush(stdout);
    }
    return 0;
}
