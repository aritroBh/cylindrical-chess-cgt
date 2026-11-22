/*
 * twist.c  --  endgame solver for K + up to two pieces (Q,R,B,N) vs K on an 8x8 board
 * with twisted gluings.  Written from the chess rules only (task T61, solver "B").
 *
 * Geometries (files f, ranks r in 0..7):
 *   plane   no gluing
 *   cyl     files wrap (f mod 8)
 *   torus   files and ranks wrap
 *   mobius  crossing the a/h edge wraps the file and flips the rank r -> 7-r; rank edges are walls
 *   klein   a/h edge as mobius; ranks also wrap, without flip
 *   rp2     a/h edge as mobius; crossing the rank edge wraps the rank and flips the file f -> 7-f
 *
 * Every square is a lattice point (F,R) of the "cover" plane.  The gluings are glide
 * reflections g1:(F,R)->(F+8,7-R) and g2:(F,R)->(F,R+8) [klein] or (7-F,R+8) [rp2].
 * canon() reduces any cover point to the 8x8 fundamental domain by undoing gluings.
 * A king step, a knight jump or one slider step is the cover offset, reduced by canon().
 * A slider ray is a straight line in the cover (so on a flipped region the local direction
 * is reflected: geodesic rule, RAYMODE 0).  RAYMODE 1 and 2 are two "naive" variants that
 * keep the local direction label after a crossing (sensitivity runs only).
 * Rays stop at the first occupied square, and stop if a ray revisits a square (its own too).
 *
 * Solving: plain value iteration on mate-in-n.  W[pos] (white to move) = 1 + min over white
 * moves of B[child];  B[pos] (black to move) = max over black moves of W[child], 0 if mated.
 * Black captures go to the solved sub-table (K+one piece vs K), bare kings are a draw.
 *
 * build:  cc -O2 -Wall -o twist twist.c
 * usage:  twist <geom> <mat|all> [-r N] [-d DIR] [-p "Ka1 Qb2 kf5"] [-s] [-g] [-G FILE]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stddef.h>
#include <ctype.h>

typedef uint64_t u64;
typedef uint8_t u8;

enum { PLANE, CYL, TORUS, MOBIUS, KLEIN, RP2, NGEOM };
static const char *gname[NGEOM] = {"plane", "cyl", "torus", "mobius", "klein", "rp2"};
static int GEOM = PLANE, RAYMODE = 0;

#define UNSET 254   /* white to move: not (yet) won; black to move: not (yet) lost */
#define ILLEGAL 255
#define DRAWN 253   /* black to move: can capture into a non-winning table */
#define STALE 252   /* black to move: stalemate */
#define MAXVAL 250  /* values below this are real mate-in-n counts */

static const char TCH[4] = {'Q', 'R', 'B', 'N'};

/* ------------------------------------------------------------------ geometry */

/* reduce cover point (F,R) to the board; returns 0 if it falls off a wall.
   *sf,*sr = accumulated reflection signs of the file and rank axes. */
static int canon(int F, int R, int *of, int *orr, int *sf, int *sr)
{
    int s_f = 1, s_r = 1;
    for (int it = 0; it < 64; it++) {
        if (F < 0 || F > 7) {
            if (GEOM == PLANE) return 0;
            F += (F < 0) ? 8 : -8;
            if (GEOM >= MOBIUS) { R = 7 - R; s_r = -s_r; }
            continue;
        }
        if (R < 0 || R > 7) {
            switch (GEOM) {
            case PLANE: case CYL: case MOBIUS: return 0;
            case TORUS: case KLEIN: R += (R < 0) ? 8 : -8; break;
            case RP2: R += (R < 0) ? 8 : -8; F = 7 - F; s_f = -s_f; break;
            }
            continue;
        }
        *of = F; *orr = R; *sf = s_f; *sr = s_r;
        return 1;
    }
    return 0;
}

/* canon, other reduction order (rank first) -- used only to test order independence */
static int canon_rank_first(int F, int R, int *of, int *orr)
{
    for (int it = 0; it < 64; it++) {
        if (R < 0 || R > 7) {
            switch (GEOM) {
            case PLANE: case CYL: case MOBIUS: return 0;
            case TORUS: case KLEIN: R += (R < 0) ? 8 : -8; break;
            case RP2: R += (R < 0) ? 8 : -8; F = 7 - F; break;
            }
            continue;
        }
        if (F < 0 || F > 7) {
            if (GEOM == PLANE) return 0;
            F += (F < 0) ? 8 : -8;
            if (GEOM >= MOBIUS) R = 7 - R;
            continue;
        }
        *of = F; *orr = R;
        return 1;
    }
    return 0;
}

/* mode 2: "flip first, then add the rank step" naive stepping, direction label kept */
static int step2(int f, int r, int df, int dr, int *nf, int *nr)
{
    int F = f + df, R = r;
    if (F < 0 || F > 7) {
        if (GEOM == PLANE) return 0;
        F = (F + 8) & 7;
        if (GEOM >= MOBIUS) R = 7 - R;
    }
    R += dr;
    if (R < 0 || R > 7) {
        switch (GEOM) {
        case PLANE: case CYL: case MOBIUS: return 0;
        case TORUS: case KLEIN: R = (R + 8) & 7; break;
        case RP2: R = (R + 8) & 7; F = 7 - F; break;
        }
    }
    *nf = F; *nr = R;
    return 1;
}

static const int DF[8] = {1, -1, 0, 0, 1, 1, -1, -1};
static const int DR[8] = {0, 0, 1, -1, 1, -1, 1, -1};
static int ksq[64][8];          /* king step destination per direction, -1 if none */
static u64 kadj[64];            /* king neighbourhood */
static int nj[64][8], nnj[64];  /* knight destinations */
static u64 nattk[64];
static int rayl[64][8];
static int rays[64][8][64];     /* dir 0..3 orthogonal, 4..7 diagonal */

static inline u64 bit(int s) { return s >= 0 ? 1ULL << s : 0; }

static void build_geometry(void)
{
    static const int KN[8][2] = {{1, 2}, {2, 1}, {-1, 2}, {-2, 1}, {1, -2}, {2, -1}, {-1, -2}, {-2, -1}};
    for (int sq = 0; sq < 64; sq++) {
        int f = sq & 7, r = sq >> 3, nf, nr, sf, sr;
        kadj[sq] = 0; nattk[sq] = 0; nnj[sq] = 0;
        for (int d = 0; d < 8; d++) {
            ksq[sq][d] = -1;
            if (canon(f + DF[d], r + DR[d], &nf, &nr, &sf, &sr) && (nf + 8 * nr) != sq) {
                ksq[sq][d] = nf + 8 * nr;
                kadj[sq] |= bit(nf + 8 * nr);
            }
        }
        for (int k = 0; k < 8; k++) {
            if (!canon(f + KN[k][0], r + KN[k][1], &nf, &nr, &sf, &sr)) continue;
            int t = nf + 8 * nr;
            if (t == sq || (nattk[sq] >> t & 1)) continue;
            nattk[sq] |= bit(t);
            nj[sq][nnj[sq]++] = t;
        }
        for (int d = 0; d < 8; d++) {
            int cf = f, cr = r, df = DF[d], dr = DR[d];
            u64 seen = bit(sq);
            int len = 0;
            for (;;) {
                int ok;
                if (RAYMODE == 2) {
                    ok = step2(cf, cr, df, dr, &nf, &nr);
                } else {
                    ok = canon(cf + df, cr + dr, &nf, &nr, &sf, &sr);
                    if (ok && RAYMODE == 0) { df *= sf; dr *= sr; }
                }
                if (!ok) break;
                int t = nf + 8 * nr;
                if (seen >> t & 1) break;       /* ray revisits a square: stop */
                seen |= bit(t);
                rays[sq][d][len++] = t;
                cf = nf; cr = nr;
            }
            rayl[sq][d] = len;
        }
    }
}

static void sq2s(int s, char *o) { o[0] = 'a' + (s & 7); o[1] = '1' + (s >> 3); o[2] = 0; }

/* attack set of a piece (type 0=Q,1=R,2=B,3=N) from sq; sliders stop at (and include) first occupied square */
static u64 attacks(int type, int sq, u64 occ)
{
    if (type == 3) return nattk[sq];
    int d0 = (type == 2) ? 4 : 0, d1 = (type == 1) ? 4 : 8;
    u64 a = 0;
    for (int d = d0; d < d1; d++)
        for (int k = 0; k < rayl[sq][d]; k++) {
            int t = rays[sq][d][k];
            a |= bit(t);
            if (occ >> t & 1) break;
        }
    return a;
}

/* ------------------------------------------------------------------ tables */

typedef struct Table {
    int np, type[2];
    size_t N;
    u8 *W, *B, *bm, *bc;
    int sWK, sP1, sP2;
    /* statistics */
    u64 legal, won, bmates, bstale, blegal, imm;   /* imm: not won, and every white move loses a man or stalemates at once (or none exist) */
    int maxW, maxB, iters;
    size_t exidx;
    u64 same_legal, same_won, opp_legal, opp_won;   /* two-piece same-type tables: bishop-square parity classes */
} Table;

static Table *tab1[4];
static Table *tab2[4][4];

static inline void decode(const Table *t, size_t idx, int *wk, int *p1, int *p2, int *bk)
{
    *bk = idx & 63;
    if (t->np == 2) { *p2 = (idx >> 6) & 63; *p1 = (idx >> 12) & 63; *wk = idx >> 18; }
    else { *p2 = -1; *p1 = (idx >> 6) & 63; *wk = idx >> 12; }
}
static inline size_t encode(const Table *t, int wk, int p1, int p2, int bk)
{
    if (t->np == 2) return ((((size_t)wk << 6 | p1) << 6 | p2) << 6) | bk;
    return (((size_t)wk << 6 | p1) << 6) | bk;
}

typedef struct { int d, to, cap, val; } BMove;   /* cap: 0 none, 1 took piece 1, 2 took piece 2 */

/* value of white-to-move position after black captured piece c (1 or 2) landing on s */
static int subval(const Table *t, int c, int wk, int q, int s)
{
    if (t->np == 1) return UNSET;                       /* bare kings */
    const Table *sub = tab1[c == 1 ? t->type[1] : t->type[0]];
    u8 v = sub->W[encode(sub, wk, q, -1, s)];
    return v < MAXVAL ? v : UNSET;
}

/* legal black king moves.  AK,A1,A2: attack sets of white king / piece1 / piece2 computed with
   the black king removed from the board (so it does not shield squares behind it). */
static int bmoves(const Table *t, int wk, int p1, int p2, int bk, u64 AK, u64 A1, u64 A2, BMove *out)
{
    int n = 0;
    for (int d = 0; d < 8; d++) {
        int s = ksq[bk][d];
        if (s < 0) continue;
        if (s == wk || (AK >> s & 1)) continue;
        BMove m = {d, s, 0, 0};
        if (s == p1) {
            if (((AK | A2) >> s) & 1) continue;
            m.cap = 1; m.val = subval(t, 1, wk, p2, s);
        } else if (s == p2) {
            if (((AK | A1) >> s) & 1) continue;
            m.cap = 2; m.val = subval(t, 2, wk, p1, s);
        } else {
            if (((AK | A1 | A2) >> s) & 1) continue;
        }
        out[n++] = m;
    }
    return n;
}

static void config_attacks(const Table *t, int wk, int p1, int p2, u64 *AK, u64 *A1, u64 *A2)
{
    u64 occ = bit(wk) | bit(p1) | bit(p2);
    *AK = kadj[wk];
    *A1 = attacks(t->type[0], p1, occ);
    *A2 = (t->np == 2) ? attacks(t->type[1], p2, occ) : 0;
}

static Table *build_table(int np, int a, int b)
{
    Table *t = calloc(1, sizeof(Table));
    t->np = np; t->type[0] = a; t->type[1] = b;
    t->N = (np == 2) ? (size_t)1 << 24 : (size_t)1 << 18;
    t->sWK = (np == 2) ? 18 : 12; t->sP1 = (np == 2) ? 12 : 6; t->sP2 = 6;
    t->W = malloc(t->N); t->B = malloc(t->N); t->bm = calloc(t->N, 1); t->bc = calloc(t->N, 1);
    memset(t->W, ILLEGAL, t->N); memset(t->B, ILLEGAL, t->N);
    int p2lo = (np == 2) ? 0 : -1, p2hi = (np == 2) ? 64 : 0;
    for (int wk = 0; wk < 64; wk++)
        for (int p1 = 0; p1 < 64; p1++) {
            if (p1 == wk) continue;
            for (int p2 = p2lo; p2 < p2hi; p2++) {
                if (np == 2 && (p2 == wk || p2 == p1)) continue;
                u64 AK, A1, A2;
                config_attacks(t, wk, p1, p2, &AK, &A1, &A2);
                u64 occ = bit(wk) | bit(p1) | bit(p2);
                for (int bk = 0; bk < 64; bk++) {
                    if ((occ >> bk & 1) || (AK >> bk & 1)) continue;
                    size_t idx = encode(t, wk, p1, p2, bk);
                    int incheck = ((A1 | A2) >> bk) & 1;
                    if (!incheck) t->W[idx] = UNSET;
                    BMove mv[8];
                    int n = bmoves(t, wk, p1, p2, bk, AK, A1, A2, mv);
                    if (n == 0) {
                        t->B[idx] = incheck ? 0 : STALE;
                        continue;
                    }
                    int mask = 0, capmax = 0, drawn = 0;
                    for (int i = 0; i < n; i++) {
                        if (mv[i].cap == 0) mask |= 1 << mv[i].d;
                        else { if (mv[i].val >= MAXVAL) drawn = 1; else if (mv[i].val > capmax) capmax = mv[i].val; }
                    }
                    t->bm[idx] = mask; t->bc[idx] = capmax;
                    t->B[idx] = drawn ? DRAWN : UNSET;
                }
            }
        }
    return t;
}

/* does white have a legal move from this position into a black-to-move position with value target? */
static int w_has_child(const Table *t, size_t idx, int wk, int p1, int p2, int bk, int target)
{
    const u8 *B = t->B;
    u64 occ = bit(wk) | bit(p1) | bit(p2) | bit(bk);
    for (int d = 0; d < 8; d++) {
        int s = ksq[wk][d];
        if (s < 0 || (occ >> s & 1) || (kadj[bk] >> s & 1)) continue;
        if (B[idx + (ptrdiff_t)(s - wk) * (1 << t->sWK)] == target) return 1;
    }
    for (int pc = 0; pc < t->np; pc++) {
        int from = pc ? p2 : p1, ty = t->type[pc], sh = pc ? t->sP2 : t->sP1;
        if (ty == 3) {
            for (int i = 0; i < nnj[from]; i++) {
                int s = nj[from][i];
                if (occ >> s & 1) continue;
                if (B[idx + (ptrdiff_t)(s - from) * (1 << sh)] == target) return 1;
            }
        } else {
            int d0 = (ty == 2) ? 4 : 0, d1 = (ty == 1) ? 4 : 8;
            for (int d = d0; d < d1; d++)
                for (int k = 0; k < rayl[from][d]; k++) {
                    int s = rays[from][d][k];
                    if (occ >> s & 1) break;
                    if (B[idx + (ptrdiff_t)(s - from) * (1 << sh)] == target) return 1;
                }
        }
    }
    return 0;
}

/* 1 if every legal white move leads to a black-to-move position that is DRAWN (black can take a man
   into a non-winning ending) or STALE (stalemate), or if white has no legal move at all */
static int w_dead(const Table *t, int wk, int p1, int p2, int bk, size_t idx)
{
    const u8 *B = t->B;
    u64 occ = bit(wk) | bit(p1) | bit(p2) | bit(bk);
    for (int d = 0; d < 8; d++) {
        int s = ksq[wk][d];
        if (s < 0 || (occ >> s & 1) || (kadj[bk] >> s & 1)) continue;
        u8 b = B[idx + (ptrdiff_t)(s - wk) * (1 << t->sWK)];
        if (b != DRAWN && b != STALE) return 0;
    }
    for (int pc = 0; pc < t->np; pc++) {
        int from = pc ? p2 : p1, ty = t->type[pc], sh = pc ? t->sP2 : t->sP1;
        if (ty == 3) {
            for (int i = 0; i < nnj[from]; i++) {
                int s = nj[from][i];
                if (occ >> s & 1) continue;
                u8 b = B[idx + (ptrdiff_t)(s - from) * (1 << sh)];
                if (b != DRAWN && b != STALE) return 0;
            }
        } else {
            int d0 = (ty == 2) ? 4 : 0, d1 = (ty == 1) ? 4 : 8;
            for (int d = d0; d < d1; d++)
                for (int k = 0; k < rayl[from][d]; k++) {
                    int s = rays[from][d][k];
                    if (occ >> s & 1) break;
                    u8 b = B[idx + (ptrdiff_t)(s - from) * (1 << sh)];
                    if (b != DRAWN && b != STALE) return 0;
                }
        }
    }
    return 1;
}

static void solve_loop(Table *t)
{
    size_t N = t->N;
    int capglob = 0;
    for (size_t i = 0; i < N; i++)
        if (t->B[i] == UNSET && t->bc[i] > capglob) capglob = t->bc[i];
    for (int n = 1; n < MAXVAL; n++) {
        long chA = 0, chB = 0;
        for (size_t idx = 0; idx < N; idx++) {
            if (t->W[idx] != UNSET) continue;
            int wk, p1, p2, bk;
            decode(t, idx, &wk, &p1, &p2, &bk);
            if (w_has_child(t, idx, wk, p1, p2, bk, n - 1)) { t->W[idx] = n; chA++; }
        }
        for (size_t idx = 0; idx < N; idx++) {
            if (t->B[idx] != UNSET || t->bc[idx] > n) continue;
            int bk = idx & 63, ok = 1, m = t->bm[idx];
            for (int d = 0; d < 8 && ok; d++)
                if (m >> d & 1) {
                    int s = ksq[bk][d];
                    if (t->W[idx + (s - bk)] > n) ok = 0;
                }
            if (ok) { t->B[idx] = n; chB++; }
        }
        t->iters = n;
        if (!chA && !chB && n >= capglob) break;
    }
}

static void stats(Table *t)
{
    t->legal = t->won = t->bmates = t->bstale = t->blegal = t->imm = 0;
    t->maxW = 0; t->maxB = 0; t->exidx = 0;
    t->same_legal = t->same_won = t->opp_legal = t->opp_won = 0;
    for (size_t i = 0; i < t->N; i++) {
        u8 w = t->W[i], b = t->B[i];
        if (b != ILLEGAL) {
            t->blegal++;
            if (b == 0) t->bmates++;
            if (b == STALE) t->bstale++;
            if (b < MAXVAL && b > t->maxB) t->maxB = b;
        }
        if (w == ILLEGAL) continue;
        t->legal++;
        int win = w < MAXVAL;
        if (!win) {
            int a, b2, c, d;
            decode(t, i, &a, &b2, &c, &d);
            t->imm += w_dead(t, a, b2, c, d, i);
        }
        if (win) { t->won++; if (w > t->maxW) { t->maxW = w; t->exidx = i; } }
        if (t->np == 2) {
            int wk, p1, p2, bk;
            decode(t, i, &wk, &p1, &p2, &bk);
            int same = (((p1 & 7) + (p1 >> 3)) & 1) == (((p2 & 7) + (p2 >> 3)) & 1);
            if (same) { t->same_legal++; t->same_won += win; } else { t->opp_legal++; t->opp_won += win; }
        }
    }
}

static Table *get_table(int np, int a, int b)
{
    if (np == 1) {
        if (!tab1[a]) {
            Table *t = build_table(1, a, 0);
            solve_loop(t); stats(t); tab1[a] = t;
        }
        return tab1[a];
    }
    if (a > b) { int x = a; a = b; b = x; }
    if (!tab2[a][b]) {
        get_table(1, a, 0); get_table(1, b, 0);
        Table *t = build_table(2, a, b);
        solve_loop(t); stats(t); tab2[a][b] = t;
    }
    return tab2[a][b];
}

/* ------------------------------------------------------------------ printing, probe */

static void matname(const Table *t, char *o)
{
    int n = 0; o[n++] = 'K';
    for (int i = 0; i < t->np; i++) o[n++] = TCH[t->type[i]];
    o[n++] = 'K'; o[n] = 0;
}

static void posstr(const Table *t, size_t idx, char *o)
{
    int wk, p1, p2, bk;
    char a[3], b[3], c[3], d[3];
    decode(t, idx, &wk, &p1, &p2, &bk);
    sq2s(wk, a); sq2s(p1, b); sq2s(bk, d);
    if (t->np == 2) { sq2s(p2, c); sprintf(o, "K%s %c%s %c%s k%s", a, TCH[t->type[0]], b, TCH[t->type[1]], c, d); }
    else sprintf(o, "K%s %c%s k%s", a, TCH[t->type[0]], b, d);
}

static void print_pv(const Table *t0, int wk, int p1, int p2, int bk)
{
    const Table *t = t0;
    int ply = 1;
    char x[3], y[3];
    for (;;) {
        size_t idx = encode(t, wk, p1, p2, bk);
        int v = t->W[idx];
        if (v >= MAXVAL) { printf("  (no forced win)\n"); return; }
        /* find a white move to a black position of value v-1 */
        u64 occ = bit(wk) | bit(p1) | bit(p2) | bit(bk);
        int found = 0, mp = -1, to = -1;
        for (int d = 0; d < 8 && !found; d++) {
            int s = ksq[wk][d];
            if (s < 0 || (occ >> s & 1) || (kadj[bk] >> s & 1)) continue;
            if (t->B[idx + (ptrdiff_t)(s - wk) * (1 << t->sWK)] == v - 1) { found = 1; mp = 0; to = s; }
        }
        for (int pc = 0; pc < t->np && !found; pc++) {
            int from = pc ? p2 : p1, ty = t->type[pc], sh = pc ? t->sP2 : t->sP1;
            if (ty == 3) {
                for (int i = 0; i < nnj[from] && !found; i++) {
                    int s = nj[from][i];
                    if (occ >> s & 1) continue;
                    if (t->B[idx + (ptrdiff_t)(s - from) * (1 << sh)] == v - 1) { found = 1; mp = pc + 1; to = s; }
                }
            } else {
                int d0 = (ty == 2) ? 4 : 0, d1 = (ty == 1) ? 4 : 8;
                for (int d = d0; d < d1 && !found; d++)
                    for (int k = 0; k < rayl[from][d]; k++) {
                        int s = rays[from][d][k];
                        if (occ >> s & 1) break;
                        if (t->B[idx + (ptrdiff_t)(s - from) * (1 << sh)] == v - 1) { found = 1; mp = pc + 1; to = s; break; }
                    }
            }
        }
        if (!found) { printf("  (pv error)\n"); return; }
        int from = mp == 0 ? wk : (mp == 1 ? p1 : p2);
        char pch = mp == 0 ? 'K' : TCH[t->type[mp - 1]];
        sq2s(from, x); sq2s(to, y);
        printf(" %d.%c%s-%s", ply, pch, x, y);
        if (mp == 0) wk = to; else if (mp == 1) p1 = to; else p2 = to;
        size_t bidx = encode(t, wk, p1, p2, bk);
        int bv = t->B[bidx];
        if (bv == 0) { printf("#\n"); return; }
        u64 AK, A1, A2;
        config_attacks(t, wk, p1, p2, &AK, &A1, &A2);
        BMove mv[8];
        int n = bmoves(t, wk, p1, p2, bk, AK, A1, A2, mv);
        int pick = -1;
        for (int i = 0; i < n; i++) {
            int val = mv[i].cap ? mv[i].val : t->W[bidx + (mv[i].to - bk)];
            if (val == bv) { pick = i; break; }
        }
        if (pick < 0) { printf("  (pv error black)\n"); return; }
        sq2s(bk, x); sq2s(mv[pick].to, y);
        if (mv[pick].cap) {
            int captype = t->type[mv[pick].cap - 1];
            printf(" k%sx%c%s", x, TCH[captype], y);
            int rem = (mv[pick].cap == 1) ? p2 : p1;
            const Table *sub = tab1[mv[pick].cap == 1 ? t->type[1] : t->type[0]];
            t = sub; p1 = rem; p2 = -1; bk = mv[pick].to;
        } else {
            printf(" k%s-%s", x, y);
            bk = mv[pick].to;
        }
        ply++;
    }
}

static int parse_pos(const Table *t, const char *s, int *wk, int *p1, int *p2, int *bk)
{
    int sq[8], ty[8], n = 0;
    const char *p = s;
    while (*p) {
        while (*p == ' ') p++;
        if (!*p) break;
        char c = *p++;
        if (!isalpha((unsigned char)c) || !*p || !*(p + 1)) return 0;
        int f = p[0] - 'a', r = p[1] - '1';
        if (f < 0 || f > 7 || r < 0 || r > 7) return 0;
        p += 2;
        if (n >= 8) return 0;
        sq[n] = f + 8 * r;
        ty[n] = (c == 'K') ? 10 : (c == 'k') ? 11 : -1;
        if (ty[n] < 0) { for (int i = 0; i < 4; i++) if (TCH[i] == c) ty[n] = i; if (ty[n] < 0) return 0; }
        n++;
    }
    *wk = *bk = -1; *p1 = *p2 = -1;
    int used[2] = {0, 0};
    for (int i = 0; i < n; i++) {
        if (ty[i] == 10) *wk = sq[i];
        else if (ty[i] == 11) *bk = sq[i];
        else {
            for (int j = 0; j < t->np; j++)
                if (!used[j] && t->type[j] == ty[i]) { used[j] = 1; if (j == 0) *p1 = sq[i]; else *p2 = sq[i]; break; }
        }
    }
    if (*wk < 0 || *bk < 0 || *p1 < 0 || (t->np == 2 && *p2 < 0)) return 0;
    return 1;
}

static void probe(const Table *t, const char *s)
{
    int wk, p1, p2, bk;
    if (!parse_pos(t, s, &wk, &p1, &p2, &bk)) { printf("probe: cannot parse '%s' for this material\n", s); return; }
    size_t idx = encode(t, wk, p1, p2, bk);
    int w = t->W[idx], b = t->B[idx];
    printf("probe %s [%s]: white to move: %s", s, gname[GEOM],
           w == ILLEGAL ? "illegal" : (w < MAXVAL ? "win" : "no win"));
    if (w < MAXVAL) printf(" in %d", w);
    printf("; black to move: %s", b == ILLEGAL ? "illegal" : (b == STALE ? "stalemate" : (b < MAXVAL ? "lost" : "no loss")));
    if (b < MAXVAL) printf(" in %d", b);
    printf("\n");
    if (w < MAXVAL) { printf("  line:"); print_pv(t, wk, p1, p2, bk); }
}

/* ------------------------------------------------------------------ geometry analysis */

static int uf[64];
static int find(int x) { while (uf[x] != x) x = uf[x] = uf[uf[x]]; return x; }

static int components(int kind, int *sizes /* up to 64 */)
{
    for (int i = 0; i < 64; i++) uf[i] = i;
    for (int s = 0; s < 64; s++) {
        if (kind == 0) for (int d = 0; d < 4; d++) { int t = ksq[s][d]; if (t >= 0) uf[find(s)] = find(t); }
        if (kind == 1) for (int d = 4; d < 8; d++) { int t = ksq[s][d]; if (t >= 0) uf[find(s)] = find(t); }
        if (kind == 2) for (int i = 0; i < nnj[s]; i++) uf[find(s)] = find(nj[s][i]);
    }
    int cnt[64] = {0}, nc = 0;
    for (int s = 0; s < 64; s++) cnt[find(s)]++;
    for (int s = 0; s < 64; s++) if (cnt[s]) sizes[nc++] = cnt[s];
    return nc;
}

/* 2-colourability of a graph (kind: 0 orthogonal king steps, 1 diagonal king steps, 2 knight jumps) */
static int bipartite(int kind)
{
    int col[64];
    for (int i = 0; i < 64; i++) col[i] = -1;
    for (int s0 = 0; s0 < 64; s0++) {
        if (col[s0] >= 0) continue;
        int stack[64], sp = 0;
        col[s0] = 0; stack[sp++] = s0;
        while (sp) {
            int s = stack[--sp];
            int nb[8], nn = 0;
            if (kind == 0) for (int d = 0; d < 4; d++) { if (ksq[s][d] >= 0) nb[nn++] = ksq[s][d]; }
            if (kind == 1) for (int d = 4; d < 8; d++) { if (ksq[s][d] >= 0) nb[nn++] = ksq[s][d]; }
            if (kind == 2) for (int i = 0; i < nnj[s]; i++) nb[nn++] = nj[s][i];
            for (int i = 0; i < nn; i++) {
                int t = nb[i];
                if (col[t] < 0) { col[t] = !col[s]; stack[sp++] = t; }
                else if (col[t] == col[s]) return 0;
            }
        }
    }
    return 1;
}

static void geom_report(void)
{
    int sz[64], nc;
    printf("GEOM %s ray=%d\n", gname[GEOM], RAYMODE);
    nc = components(0, sz); printf("  orthogonal-step graph: %d component(s)%s", nc, bipartite(0) ? ", 2-colourable (chessboard colouring exists)" : ", NOT 2-colourable (odd cycle: no chessboard colouring)"); printf("\n");
    nc = components(1, sz);
    printf("  bishop (diagonal-step) orbits: %d, sizes:", nc);
    for (int i = 0; i < nc; i++) printf(" %d", sz[i]);
    printf("\n");
    /* does (f+r) parity survive diagonal steps? */
    int flips = 0, tot = 0;
    for (int s = 0; s < 64; s++) for (int d = 4; d < 8; d++) { int t = ksq[s][d]; if (t < 0) continue; tot++; if ((((s & 7) + (s >> 3)) & 1) != (((t & 7) + (t >> 3)) & 1)) flips++; }
    printf("  diagonal steps that change nominal (f+r) parity: %d of %d\n", flips, tot);
    int of = 0, tf = 0;
    for (int s = 0; s < 64; s++) for (int d = 0; d < 4; d++) { int t = ksq[s][d]; if (t < 0) continue; tf++; if ((((s & 7) + (s >> 3)) & 1) == (((t & 7) + (t >> 3)) & 1)) of++; }
    printf("  orthogonal steps that keep nominal (f+r) parity: %d of %d\n", of, tf);
    nc = components(2, sz);
    printf("  knight orbits: %d, sizes:", nc);
    for (int i = 0; i < nc; i++) printf(" %d", sz[i]);
    printf("; knight graph %s\n", bipartite(2) ? "bipartite (knight always changes side)" : "NOT bipartite");
    printf("  diagonal-step graph %s\n", bipartite(1) ? "bipartite" : "NOT bipartite");
    int rmin = 99, rmax = 0, bmin = 99, bmax = 0, nmin = 99, nmax = 0;
    for (int s = 0; s < 64; s++) {
        int rl = 0, bl = 0;
        for (int d = 0; d < 4; d++) rl += rayl[s][d];
        for (int d = 4; d < 8; d++) bl += rayl[s][d];
        if (rl < rmin) rmin = rl;
        if (rl > rmax) rmax = rl;
        if (bl < bmin) bmin = bl;
        if (bl > bmax) bmax = bl;
        if (nnj[s] < nmin) nmin = nnj[s];
        if (nnj[s] > nmax) nmax = nnj[s];
    }
    printf("  empty-board rook range %d..%d squares, bishop range %d..%d, knight range %d..%d\n", rmin, rmax, bmin, bmax, nmin, nmax);
}

/* ------------------------------------------------------------------ self tests */

static void geometry_selftest(void)
{
    int bad = 0;
    /* canon: reduction order independence and invariance under the gluing maps, on a window of the cover */
    for (int F = -26; F < 34; F++)
        for (int R = -26; R < 34; R++) {
            int a, b, sf, sr, c, d;
            int v1 = canon(F, R, &a, &b, &sf, &sr), v2 = canon_rank_first(F, R, &c, &d);
            if (v1 != v2 || (v1 && (a != c || b != d))) { bad++; continue; }
            if (!v1) continue;
            /* images under g1 and g2 (generators of the gluing group) must reduce to the same cell */
            if (GEOM >= MOBIUS) {
                int e, f2, s1, s2;
                int v3 = canon(F + 8, 7 - R, &e, &f2, &s1, &s2);
                if (!v3 || e != a || f2 != b) bad++;
            }
            if (GEOM >= KLEIN) {
                int e, f2, s1, s2, v3;
                if (GEOM == KLEIN) v3 = canon(F, R + 8, &e, &f2, &s1, &s2); else v3 = canon(7 - F, R + 8, &e, &f2, &s1, &s2);
                if (!v3 || e != a || f2 != b) bad++;
            }
            if (GEOM == TORUS || GEOM == CYL) {
                int e, f2, s1, s2;
                if (!canon(F + 8, R, &e, &f2, &s1, &s2) || e != a || f2 != b) bad++;
            }
            if (GEOM == TORUS) {
                int e, f2, s1, s2;
                if (!canon(F, R + 8, &e, &f2, &s1, &s2) || e != a || f2 != b) bad++;
            }
        }
    /* reversibility of rays (geodesic rule): t on ray(s,d) at position k  =>  s on ray(t,-d) at position k */
    int asym = 0;
    for (int s = 0; s < 64; s++)
        for (int d = 0; d < 8; d++)
            for (int k = 0; k < rayl[s][d]; k++) {
                int t = rays[s][d][k], found = 0;
                for (int e = 0; e < 8 && !found; e++) {
                    if (rayl[t][e] < k + 1) continue;
                    if (rays[t][e][k] == s) {
                        int ok = 1;
                        for (int j = 0; j < k; j++) if (rays[t][e][j] != rays[s][d][k - 1 - j]) ok = 0;
                        if (ok) found = 1;
                    }
                }
                if (!found) asym++;
            }
    printf("SELFTEST geom=%s ray=%d: canon/gluing inconsistencies=%d, non-reversible ray squares=%d\n", gname[GEOM], RAYMODE, bad, asym);
}

typedef struct { const char *name; int mode; } Sym;

static int symmetry_perm(int mode, int *perm)
{
    int seen[64] = {0};
    for (int s = 0; s < 64; s++) {
        int F = s & 7, R = s >> 3, a, b, sf, sr, G, H;
        switch (mode) {
        case 0: G = F + 1; H = R; break;          /* shift file */
        case 1: G = F; H = R + 1; break;          /* shift rank */
        case 2: G = 7 - F; H = R; break;          /* mirror files */
        case 3: G = F; H = 7 - R; break;          /* mirror ranks */
        case 4: G = R; H = F; break;              /* transpose */
        default: G = 7 - F; H = 7 - R; break;     /* rotate 180 */
        }
        if (!canon(G, H, &a, &b, &sf, &sr)) return 0;
        perm[s] = a + 8 * b;
        if (seen[perm[s]]) return 0;
        seen[perm[s]] = 1;
    }
    return 1;
}

static int structure_preserved(const int *perm)
{
    for (int s = 0; s < 64; s++) {
        u64 img = 0;
        for (int d = 0; d < 8; d++) if (ksq[s][d] >= 0) img |= bit(perm[ksq[s][d]]);
        if (img != kadj[perm[s]]) return 0;
        img = 0;
        for (int i = 0; i < nnj[s]; i++) img |= bit(perm[nj[s][i]]);
        if (img != nattk[perm[s]]) return 0;
    }
    /* rays: every ray of s must map onto a ray of perm[s]; directions used must be a permutation */
    for (int s = 0; s < 64; s++) {
        int used[8] = {0};
        for (int d = 0; d < 8; d++) {
            int match = -1;
            for (int e = 0; e < 8 && match < 0; e++) {
                if (used[e] || rayl[perm[s]][e] != rayl[s][d]) continue;
                int ok = 1;
                for (int k = 0; k < rayl[s][d]; k++) if (perm[rays[s][d][k]] != rays[perm[s]][e][k]) { ok = 0; break; }
                if (ok) match = e;
            }
            if (match < 0) return 0;
            used[match] = 1;
        }
    }
    return 1;
}

static void symmetry_test(const Table *t)
{
    static const char *nm[6] = {"file shift", "rank shift", "file mirror", "rank mirror", "transpose", "rotate 180"};
    char mn[16]; matname(t, mn);
    for (int mode = 0; mode < 6; mode++) {
        int perm[64];
        if (!symmetry_perm(mode, perm)) { printf("  sym %-11s %s: not a board map\n", nm[mode], mn); continue; }
        if (!structure_preserved(perm)) { printf("  sym %-11s %s: not a symmetry of the move structure\n", nm[mode], mn); continue; }
        size_t diffW = 0, diffB = 0;
        for (size_t i = 0; i < t->N; i++) {
            int wk, p1, p2, bk;
            decode(t, i, &wk, &p1, &p2, &bk);
            size_t j = encode(t, perm[wk], perm[p1], p2 >= 0 ? perm[p2] : -1, perm[bk]);
            if (t->W[i] != t->W[j]) diffW++;
            if (t->B[i] != t->B[j]) diffB++;
        }
        printf("  sym %-11s %s: W differences %zu, B differences %zu\n", nm[mode], mn, diffW, diffB);
    }
}

static void write_geometry(const char *path)
{
    FILE *f = fopen(path, "w");
    if (!f) { perror(path); return; }
    for (int s = 0; s < 64; s++) {
        fprintf(f, "K %d", s);
        for (int d = 0; d < 8; d++) fprintf(f, " %d", ksq[s][d]);
        fprintf(f, "\nN %d", s);
        for (int i = 0; i < nnj[s]; i++) fprintf(f, " %d", nj[s][i]);
        fprintf(f, "\n");
        for (int d = 0; d < 8; d++) {
            fprintf(f, "R %d %d", s, d);
            for (int k = 0; k < rayl[s][d]; k++) fprintf(f, " %d", rays[s][d][k]);
            fprintf(f, "\n");
        }
    }
    fclose(f);
}

/* ------------------------------------------------------------------ driver */

static void report(const Table *t, int showpv)
{
    char mn[16], ex[64];
    matname(t, mn);
    posstr(t, t->exidx, ex);
    printf("RESULT\tgeom=%s\tray=%d\tmat=%s\tlegal=%llu\twon=%llu\tpct=%.4f\tmaxdtm=%d\tall=%d\tbmates=%llu\tbstale=%llu\tmaxB=%d\titers=%d\tnonwon=%llu\tnonwon_imm=%llu\tex=%s",
           gname[GEOM], RAYMODE, mn, (unsigned long long)t->legal, (unsigned long long)t->won,
           t->legal ? 100.0 * t->won / t->legal : 0.0, t->maxW, t->won == t->legal, (unsigned long long)t->bmates,
           (unsigned long long)t->bstale, t->maxB, t->iters,
           (unsigned long long)(t->legal - t->won), (unsigned long long)t->imm, t->maxW ? ex : "none");
    if (t->np == 2 && t->type[0] == t->type[1])
        printf("\tsame_legal=%llu\tsame_won=%llu\topp_legal=%llu\topp_won=%llu", (unsigned long long)t->same_legal,
               (unsigned long long)t->same_won, (unsigned long long)t->opp_legal, (unsigned long long)t->opp_won);
    printf("\n");
    if (showpv && t->maxW) {
        int wk, p1, p2, bk;
        decode(t, t->exidx, &wk, &p1, &p2, &bk);
        printf("PV\t%s\t%s\t%s\t", gname[GEOM], mn, ex);
        print_pv(t, wk, p1, p2, bk);
    }
    fflush(stdout);
}

static void dump(const Table *t, const char *dir)
{
    char mn[16], path[512];
    matname(t, mn);
    for (int w = 0; w < 2; w++) {
        snprintf(path, sizeof path, "%s/%s_%s.%c", dir, gname[GEOM], mn, w ? 'B' : 'W');
        FILE *f = fopen(path, "wb");
        if (!f) { perror(path); exit(1); }
        fwrite(w ? t->B : t->W, 1, t->N, f);
        fclose(f);
    }
}

int main(int argc, char **argv)
{
    if (argc < 3) { fprintf(stderr, "usage: %s <plane|cyl|torus|mobius|klein|rp2> <mat|all> [-r N] [-d DIR] [-p POS] [-s] [-g] [-G FILE] [-v]\n", argv[0]); return 1; }
    GEOM = -1;
    for (int i = 0; i < NGEOM; i++) if (!strcmp(argv[1], gname[i])) GEOM = i;
    if (GEOM < 0) { fprintf(stderr, "unknown geometry %s\n", argv[1]); return 1; }
    const char *mat = argv[2], *dumpdir = NULL, *probepos = NULL, *geomfile = NULL;
    int dosym = 0, dogeom = 0, selftest = 1, showpv = 1;
    for (int i = 3; i < argc; i++) {
        if (!strcmp(argv[i], "-r") && i + 1 < argc) RAYMODE = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-d") && i + 1 < argc) dumpdir = argv[++i];
        else if (!strcmp(argv[i], "-p") && i + 1 < argc) probepos = argv[++i];
        else if (!strcmp(argv[i], "-G") && i + 1 < argc) geomfile = argv[++i];
        else if (!strcmp(argv[i], "-s")) dosym = 1;
        else if (!strcmp(argv[i], "-g")) dogeom = 1;
        else if (!strcmp(argv[i], "-q")) { selftest = 0; showpv = 0; }
        else { fprintf(stderr, "bad option %s\n", argv[i]); return 1; }
    }
    build_geometry();
    if (selftest) geometry_selftest();
    if (dogeom) geom_report();
    if (geomfile) write_geometry(geomfile);

    static const char *ALL[] = {"Q", "R", "B", "N", "QR", "RR", "QQ", "BB", "NN", "BN", "RB"};
    int nm = 1;
    const char *list[16];
    list[0] = mat;
    if (!strcmp(mat, "all")) { nm = 11; for (int i = 0; i < nm; i++) list[i] = ALL[i]; }
    else if (!strcmp(mat, "none")) nm = 0;
    for (int m = 0; m < nm; m++) {
        int ty[2], np = (int)strlen(list[m]);
        if (np < 1 || np > 2) { fprintf(stderr, "material must have 1 or 2 pieces\n"); return 1; }
        for (int i = 0; i < np; i++) {
            ty[i] = -1;
            for (int j = 0; j < 4; j++) if (TCH[j] == toupper((unsigned char)list[m][i])) ty[i] = j;
            if (ty[i] < 0) { fprintf(stderr, "bad piece letter\n"); return 1; }
        }
        Table *t = get_table(np, ty[0], np == 2 ? ty[1] : 0);
        report(t, showpv);
        if (dumpdir) {
            dump(t, dumpdir);
            if (np == 2) { dump(tab1[t->type[0]], dumpdir); dump(tab1[t->type[1]], dumpdir); }
        }
        if (dosym) symmetry_test(t);
        if (probepos) probe(t, probepos);
    }
    return 0;
}
