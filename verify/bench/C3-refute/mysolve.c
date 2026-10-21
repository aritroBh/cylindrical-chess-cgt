/* mysolve.c - independent whole-board solver for the ChessSums pawn game
 * (verifier C3-refute; written from scratch, shares no code with bench/ab.c).
 *
 * Rules: pawns only, W files x 8 ranks, flat or cylinder (wrap). Single step,
 * double step from rank 2 / 7, diagonal capture (across the seam on a
 * cylinder), en passant with the real-chess lifetime (next ply only).
 * Normal play: side with no move loses. After every move: if exactly one side
 * has a passed pawn that side wins; if both, a race resolved by RULE.
 *
 * MODE 0: textbook passed test, e.p. on.
 * MODE 1: e.p.-aware passed test, e.p. on: the pawn that has just double-
 *         stepped and stands beside an enemy pawn (so may be taken e.p.) is
 *         not passed and is skipped in the race distance.
 * MODE 2: e.p. off (textbook test; the two tests coincide).
 * RULE 0: count (opponent of the mover moves first; fewer moves to promote
 *         wins; tie -> opponent).  1: mover wins.  2: opponent wins.
 *
 * Search: boolean negamax, captures first, files scanned from the last file
 * down (a different order from ab.c), 128-bit Zobrist transposition table.
 *
 * stdin, one job per line:
 *   tag NF CYL MODE RULE TCAP nW f r ... nB f r ...      (files 0-based)
 * stdout: tag MODE RULE resW resB nodes races epcap_gen diffjudged rootpass
 *   res: 1 side to move wins, 0 side to move loses, -1 cap reached
 *   races: race evaluations met; epcap_gen: e.p. captures generated;
 *   diffjudged: (MODE 0) double steps after which the moved pawn is
 *   textbook-passed and has an enemy pawn beside it.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXW 32
static int NF, CYL, MODE, RULE;
static unsigned wm[MAXW], bm[MAXW]; /* bit r set = pawn on rank r (1..8) */
static long long nodes, races, epcap, diffj;
static int capped;
static double t_end;

static uint64_t Z1[MAXW][10][2], Z2[MAXW][10][2], S1, S2, E1[MAXW][10], E2[MAXW][10];
typedef struct { uint64_t a, b; uint32_t gen; int8_t v; } Ent;
#define TTB 22
static Ent *tt;
static uint32_t gen_id;

static double cpu(void) { return (double)clock() / CLOCKS_PER_SEC; }

static uint64_t sm = 0x1234567887654321ULL;
static uint64_t rnd64(void) {
    sm ^= sm << 13; sm ^= sm >> 7; sm ^= sm << 17;
    return sm * 0x2545F4914F6CDD1DULL;
}

static int lf(int f) { return f > 0 ? f - 1 : (CYL ? NF - 1 : -1); }
static int rf(int f) { return f < NF - 1 ? f + 1 : (CYL ? 0 : -1); }

/* ranks strictly above r / strictly below r */
#define ABOVE(m, r) ((m) >> ((r) + 1))
#define BELOW(m, r) ((m) & ((1u << (r)) - 1u))

static int w_passed(int f, int r) {
    int a = lf(f), b = rf(f);
    if (ABOVE(bm[f], r)) return 0;
    if (a >= 0 && ABOVE(bm[a], r)) return 0;
    if (b >= 0 && ABOVE(bm[b], r)) return 0;
    return 1;
}
static int b_passed(int f, int r) {
    int a = lf(f), b = rf(f);
    if (BELOW(wm[f], r)) return 0;
    if (a >= 0 && BELOW(wm[a], r)) return 0;
    if (b >= 0 && BELOW(wm[b], r)) return 0;
    return 1;
}

/* exclude (xf, xr) = a pawn of `white` side that is skipped (e.p.-aware) */
static int any_passer(int white, int xf, int xr) {
    for (int f = 0; f < NF; f++) {
        unsigned m = white ? wm[f] : bm[f];
        for (int r = 1; r <= 8; r++) {
            if (!(m >> r & 1u)) continue;
            if (f == xf && r == xr) continue;
            if (white ? w_passed(f, r) : b_passed(f, r)) return 1;
        }
    }
    return 0;
}

static int race_dist(int white, int xf, int xr) {
    int best = 1 << 20;
    for (int f = 0; f < NF; f++) {
        unsigned m = white ? wm[f] : bm[f];
        unsigned occ = wm[f] | bm[f];
        for (int r = 1; r <= 8; r++) {
            if (!(m >> r & 1u)) continue;
            if (f == xf && r == xr) continue;
            if (white) {
                if (!w_passed(f, r) || ABOVE(occ, r)) continue;
                int d = 8 - r - (r == 2);
                if (d < best) best = d;
            } else {
                if (!b_passed(f, r) || BELOW(occ, r)) continue;
                int d = r - 1 - (r == 7);
                if (d < best) best = d;
            }
        }
    }
    return best;
}

static void key(int white, int ef, int er, uint64_t *a, uint64_t *b) {
    uint64_t x = white ? S1 : 0, y = white ? S2 : 0;
    for (int f = 0; f < NF; f++)
        for (int r = 1; r <= 8; r++) {
            if (wm[f] >> r & 1u) { x ^= Z1[f][r][0]; y ^= Z2[f][r][0]; }
            if (bm[f] >> r & 1u) { x ^= Z1[f][r][1]; y ^= Z2[f][r][1]; }
        }
    if (ef >= 0) { x ^= E1[ef][er]; y ^= E2[ef][er]; }
    *a = x; *b = y;
}

typedef struct { int8_t ff, fr, tf, tr, xf, xr, dbl; } Mv; /* xf/xr: removed enemy pawn */

/* side to move `white`; (ef, er) = enemy pawn that has just double-stepped and
 * may be captured e.p. by the side to move (-1 if none). Returns 1 = win. */
static int solve(int white, int ef, int er) {
    nodes++;
    if ((nodes & 0x3FFFF) == 0 && t_end > 0 && cpu() > t_end) capped = 1;
    if (capped) return 0;
    uint64_t ka, kb;
    key(white, ef, er, &ka, &kb);
    Ent *e = &tt[ka & ((1u << TTB) - 1)];
    if (e->gen == gen_id && e->a == ka && e->b == kb) return e->v;

    unsigned *me = white ? wm : bm, *op = white ? bm : wm;
    int d = white ? 1 : -1, home = white ? 2 : 7;
    Mv mv[160];
    int n = 0;
    /* captures (incl. e.p.) */
    for (int f = NF - 1; f >= 0; f--)
        for (int r = 8; r >= 1; r--) {
            if (!(me[f] >> r & 1u)) continue;
            int t = r + d;
            if (t < 1 || t > 8) continue;
            int g2[2] = {rf(f), lf(f)};
            for (int k = 0; k < 2; k++) {
                int g = g2[k];
                if (g < 0) continue;
                if (k == 1 && g == g2[0]) continue; /* 2-file cylinder: same file twice */
                if (op[g] >> t & 1u) mv[n++] = (Mv){f, r, g, t, g, t, 0};
                else if (ef == g && er == r && !((wm[g] | bm[g]) >> t & 1u)) {
                    mv[n++] = (Mv){f, r, g, t, g, r, 0};
                    epcap++;
                }
            }
        }
    /* double steps, then single steps */
    for (int pass = 0; pass < 2; pass++)
        for (int f = NF - 1; f >= 0; f--)
            for (int r = 8; r >= 1; r--) {
                if (!(me[f] >> r & 1u)) continue;
                int t = r + d;
                if (t < 1 || t > 8) continue;
                unsigned occ = wm[f] | bm[f];
                if (occ >> t & 1u) continue;
                if (pass == 0) {
                    int t2 = r + 2 * d;
                    if (r == home && !(occ >> t2 & 1u)) mv[n++] = (Mv){f, r, f, t2, -1, -1, 1};
                } else {
                    mv[n++] = (Mv){f, r, f, t, -1, -1, 0};
                }
            }

    int res = 0;
    for (int i = 0; i < n && !res; i++) {
        Mv m = mv[i];
        me[(int)m.ff] &= ~(1u << m.fr);
        if (m.xf >= 0) op[(int)m.xf] &= ~(1u << m.xr);
        me[(int)m.tf] |= 1u << m.tr;
        int nef = -1, ner = -1, xf = -1, xr = -1;
        if (m.dbl && MODE != 2) {
            int a = lf(m.tf), b = rf(m.tf);
            int beside = (a >= 0 && (op[a] >> m.tr & 1u)) || (b >= 0 && (op[b] >> m.tr & 1u));
            if (beside) {
                nef = m.tf; ner = m.tr;
                int pp = white ? w_passed(m.tf, m.tr) : b_passed(m.tf, m.tr);
                if (MODE == 0 && pp) diffj++;
                if (MODE == 1) { xf = m.tf; xr = m.tr; }
            }
        }
        /* exclusion applies to the mover's own pawn only */
        int wp = any_passer(1, white ? xf : -1, white ? xr : -1);
        int bp = any_passer(0, white ? -1 : xf, white ? -1 : xr);
        int v; /* 1 = mover wins */
        if (wp && bp) {
            races++;
            if (RULE == 1) v = 1;
            else if (RULE == 2) v = 0;
            else {
                int dm = race_dist(white, xf, xr);
                int dop = race_dist(!white, -1, -1);
                v = dop <= dm ? 0 : 1;
            }
        } else if (wp || bp) {
            v = (wp && white) || (bp && !white);
        } else {
            v = !solve(!white, nef, ner);
        }
        me[(int)m.tf] &= ~(1u << m.tr);
        if (m.xf >= 0) op[(int)m.xf] |= 1u << m.xr;
        me[(int)m.ff] |= 1u << m.fr;
        if (capped) return 0;
        res = v;
    }
    e->a = ka; e->b = kb; e->gen = gen_id; e->v = (int8_t)res;
    return res;
}

int main(void) {
    for (int f = 0; f < MAXW; f++)
        for (int r = 0; r < 10; r++) {
            Z1[f][r][0] = rnd64(); Z1[f][r][1] = rnd64();
            Z2[f][r][0] = rnd64(); Z2[f][r][1] = rnd64();
            E1[f][r] = rnd64(); E2[f][r] = rnd64();
        }
    S1 = rnd64(); S2 = rnd64();
    tt = calloc((size_t)1 << TTB, sizeof(Ent));
    char tag[64];
    double tcap;
    while (scanf("%63s %d %d %d %d %lf", tag, &NF, &CYL, &MODE, &RULE, &tcap) == 6) {
        memset(wm, 0, sizeof wm); memset(bm, 0, sizeof bm);
        for (int c = 0; c < 2; c++) {
            int k, f, r;
            if (scanf("%d", &k) != 1) return 1;
            for (int i = 0; i < k; i++) {
                if (scanf("%d %d", &f, &r) != 2) return 1;
                if (c == 0) wm[f] |= 1u << r; else bm[f] |= 1u << r;
            }
        }
        int rootpass = any_passer(1, -1, -1) || any_passer(0, -1, -1);
        int res[2];
        nodes = races = epcap = diffj = 0;
        for (int s = 0; s < 2; s++) {
            gen_id++;
            capped = 0;
            t_end = tcap > 0 ? cpu() + tcap : 0;
            int v = solve(s == 0, -1, -1);
            res[s] = capped ? -1 : v;
        }
        printf("%s %d %d %d %d %lld %lld %lld %lld %d\n", tag, MODE, RULE, res[0], res[1], nodes, races,
               epcap, diffj, rootpass);
        fflush(stdout);
    }
    return 0;
}
