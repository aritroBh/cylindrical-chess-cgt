/* wb.c - independent whole-board solver for pawn-only games (C4 refute check).
 * Written from scratch for this verification; shares no code with cylcgt, bench/ab.c
 * or crosscheck/.
 *
 * Game: pawns only, W files x 8 ranks, flat or cylinder (wrap). Normal play.
 * Real-chess en passant: a double step gives the opponent an e.p. right for the very
 * next ply only (it expires after ANY other move, anywhere on the board).
 * Passed-pawn test: "e.p.-aware" (default) = textbook test, except that a pawn that may be
 * taken e.p. right now is not passed.  Option aware=0 gives the textbook test.
 * As soon as exactly one side has a passed pawn the game ends and that side wins.
 * If a move gives both sides passed pawns: race rule (0 count, 1 mover, 2 opponent).
 *   count: the opponent of the mover wins iff dist(opp) <= dist(mover), where dist is the
 *   smallest promotion distance among that side's passed front pawns (e.p.-capturable pawns
 *   skipped when aware=1); d = 8 - r - (r == 2) for White, r - 1 - (r == 7) for Black.
 * Optional extra summand H (explicit finite game DAG, node 0 = root), played alongside
 * the pawns: Left = White.  A move in H also lets any e.p. right expire. When the pawn part
 * reaches a passer the game is decided for that side (valid when |H| << BIG = 256).
 *
 * Input, one job per line:
 *   id files wrap rule aware ep cap stop nW f r ... nB f r ... nH {nl l.. nr r..}*nH
 *   (files 0-based, ranks 1..8; nH = 0 means no H summand; cap = node cap)
 * Output per job:
 *   J id
 *   M side ff fr tf tr res      (one per root pawn move; res 1 = mover wins, 0 = loses, -1 = unknown)
 *   H side opt res              (one per root H move)
 *   E nodes ep_capture_available_nodes ep_test_differs_positions aborted
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXF 26
#define NR 8
#define MAXH 200000

static int NF, WRAP, RULE, AWARE, EPON, STOP;
static signed char bd[MAXF][NR + 2];
static int ep_holder, ep_tf, ep_tr, ep_cf, ep_cr; /* holder 0 = none, 1 = W may capture, 2 = B may capture */
static int hcur, Hn;
static int *Hlo, *Hln, *Hro, *Hrn, *Hopt;
static long long nodes, cap, ep_avail, ep_diff;
static int aborted;
static uint64_t Z1[MAXF][NR + 2][3], Z2[MAXF][NR + 2][3], ZE1[MAXF][NR + 2], ZE2[MAXF][NR + 2], ZS1, ZS2;
static uint64_t h1, h2;

static uint64_t sm(uint64_t x) {
    x += 0x9E3779B97F4A7C15ULL;
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ULL;
    x = (x ^ (x >> 27)) * 0x94D049BB133111EBULL;
    return x ^ (x >> 31);
}
static uint64_t zh1(int n) { return sm(0xA5A5ULL + 2 * (uint64_t)n); }
static uint64_t zh2(int n) { return sm(0x5A5A0000ULL + 2 * (uint64_t)n + 1); }

#define TTB 22
#define TTN (1u << TTB)
typedef struct { uint64_t a; uint64_t b; uint32_t gen; int8_t v; } TTE;
static TTE *tt;
static uint32_t gen = 0;

static int nb(int f, int d) {
    int g = f + d;
    if (WRAP) return ((g % NF) + NF) % NF;
    return (g >= 0 && g < NF) ? g : -1;
}

/* is the pawn of colour c on (f,r) capturable e.p. right now? */
static int ep_capt(int c, int f, int r) {
    if (!ep_holder || ep_holder == c || ep_cf != f || ep_cr != r) return 0;
    for (int d = -1; d <= 1; d += 2) {
        int g = nb(f, d);
        if (g >= 0 && bd[g][r] == ep_holder) return 1;
    }
    return 0;
}

/* textbook passed test for one pawn */
static int pawn_passed_tb(int c, int f, int r) {
    int fs[3] = {f, nb(f, -1), nb(f, 1)};
    for (int i = 0; i < 3; i++) {
        int g = fs[i];
        if (g < 0) continue;
        if (c == 1) { for (int s = r + 1; s <= NR; s++) if (bd[g][s] == 2) return 0; }
        else { for (int s = 1; s < r; s++) if (bd[g][s] == 1) return 0; }
    }
    return 1;
}

static int pawn_passed(int c, int f, int r) {
    if (!pawn_passed_tb(c, f, r)) return 0;
    if (ep_capt(c, f, r)) { ep_diff++; if (AWARE) return 0; }
    return 1;
}

static int has_passer(int c) {
    for (int f = 0; f < NF; f++)
        for (int r = 1; r <= NR; r++)
            if (bd[f][r] == c && pawn_passed(c, f, r)) return 1;
    return 0;
}

static int dist(int c) {
    int best = 1000000;
    for (int f = 0; f < NF; f++)
        for (int r = 1; r <= NR; r++) {
            if (bd[f][r] != c) continue;
            if (!pawn_passed_tb(c, f, r)) continue;
            if (ep_capt(c, f, r)) { ep_diff++; if (AWARE) continue; }
            int ahead = 0;
            if (c == 1) { for (int s = r + 1; s <= NR; s++) if (bd[f][s]) ahead = 1; }
            else { for (int s = 1; s < r; s++) if (bd[f][s]) ahead = 1; }
            if (ahead) continue;
            int d = (c == 1) ? (NR - r - (r == 2)) : (r - 1 - (r == NR - 1));
            if (d < best) best = d;
        }
    return best;
}

/* evaluate the position just after `mover` moved: 0 = not terminal, else winner colour */
static int terminal(int mover) {
    int wp = has_passer(1), bp = has_passer(2);
    if (wp && !bp) return 1;
    if (bp && !wp) return 2;
    if (!wp && !bp) return 0;
    int opp = 3 - mover;
    if (RULE == 1) return mover;
    if (RULE == 2) return opp;
    return dist(opp) <= dist(mover) ? opp : mover;
}

typedef struct { signed char ff, fr, tf, tr, ty; } Mv; /* ty 0 push, 1 double, 2 capture, 3 e.p. */

static int gen_moves(int c, Mv *out) {
    int n = 0, d = (c == 1) ? 1 : -1, start = (c == 1) ? 2 : NR - 1;
    for (int f = 0; f < NF; f++)
        for (int r = 1; r <= NR; r++) {
            if (bd[f][r] != c) continue;
            int r1 = r + d;
            if (r1 < 1 || r1 > NR) continue;
            if (!bd[f][r1]) {
                out[n++] = (Mv){f, r, f, r1, 0};
                int r2 = r + 2 * d;
                if (r == start && r2 >= 1 && r2 <= NR && !bd[f][r2]) out[n++] = (Mv){f, r, f, r2, 1};
            }
            for (int dd = -1; dd <= 1; dd += 2) {
                int g = nb(f, dd);
                if (g < 0) continue;
                if (bd[g][r1] == 3 - c) out[n++] = (Mv){f, r, g, r1, 2};
                else if (ep_holder == c && ep_tf == g && ep_tr == r1 && !bd[g][r1]) out[n++] = (Mv){f, r, g, r1, 3};
            }
        }
    return n;
}

typedef struct { int holder, tf, tr, cf, cr; signed char capd; int capf, capr; } Undo;

static void ep_hash(void) {
    if (ep_holder) { h1 ^= ZE1[ep_tf][ep_tr] ^ (uint64_t)ep_holder; h2 ^= ZE2[ep_tf][ep_tr] ^ ((uint64_t)ep_holder << 7); }
}

static void make(int c, Mv m, Undo *u) {
    u->holder = ep_holder; u->tf = ep_tf; u->tr = ep_tr; u->cf = ep_cf; u->cr = ep_cr;
    u->capd = 0;
    ep_hash(); /* remove old e.p. key */
    bd[m.ff][m.fr] = 0; h1 ^= Z1[m.ff][m.fr][c]; h2 ^= Z2[m.ff][m.fr][c];
    if (m.ty == 2) { u->capd = 1; u->capf = m.tf; u->capr = m.tr; bd[m.tf][m.tr] = 0; h1 ^= Z1[m.tf][m.tr][3 - c]; h2 ^= Z2[m.tf][m.tr][3 - c]; }
    if (m.ty == 3) { u->capd = 1; u->capf = ep_cf; u->capr = ep_cr; bd[ep_cf][ep_cr] = 0; h1 ^= Z1[ep_cf][ep_cr][3 - c]; h2 ^= Z2[ep_cf][ep_cr][3 - c]; }
    bd[m.tf][m.tr] = c; h1 ^= Z1[m.tf][m.tr][c]; h2 ^= Z2[m.tf][m.tr][c];
    ep_holder = 0;
    if (m.ty == 1 && EPON) {
        ep_holder = 3 - c; ep_tf = m.ff; ep_tr = (m.fr + m.tr) / 2; ep_cf = m.tf; ep_cr = m.tr;
    }
    ep_hash();
    h1 ^= ZS1; h2 ^= ZS2;
}

static void unmake(int c, Mv m, Undo *u) {
    h1 ^= ZS1; h2 ^= ZS2;
    ep_hash();
    bd[m.tf][m.tr] = 0; h1 ^= Z1[m.tf][m.tr][c]; h2 ^= Z2[m.tf][m.tr][c];
    if (u->capd) { bd[u->capf][u->capr] = 3 - c; h1 ^= Z1[u->capf][u->capr][3 - c]; h2 ^= Z2[u->capf][u->capr][3 - c]; }
    bd[m.ff][m.fr] = c; h1 ^= Z1[m.ff][m.fr][c]; h2 ^= Z2[m.ff][m.fr][c];
    ep_holder = u->holder; ep_tf = u->tf; ep_tr = u->tr; ep_cf = u->cf; ep_cr = u->cr;
    ep_hash();
}

/* H move by colour c to node nn: e.p. right expires */
static void hmake(int nn, Undo *u, int *old) {
    *old = hcur;
    u->holder = ep_holder; u->tf = ep_tf; u->tr = ep_tr; u->cf = ep_cf; u->cr = ep_cr;
    ep_hash(); ep_holder = 0; ep_hash();
    h1 ^= zh1(hcur) ^ zh1(nn); h2 ^= zh2(hcur) ^ zh2(nn); hcur = nn;
    h1 ^= ZS1; h2 ^= ZS2;
}
static void hunmake(Undo *u, int old) {
    h1 ^= ZS1; h2 ^= ZS2;
    h1 ^= zh1(hcur) ^ zh1(old); h2 ^= zh2(hcur) ^ zh2(old); hcur = old;
    ep_hash(); ep_holder = u->holder; ep_tf = u->tf; ep_tr = u->tr; ep_cf = u->cf; ep_cr = u->cr; ep_hash();
}

static int solve(int c);

/* result for the mover c of pawn move m: 1 win, 0 loss, -1 abort */
static int try_pawn(int c, Mv m) {
    Undo u; make(c, m, &u);
    int t = terminal(c), res;
    if (t) res = (t == c);
    else { int r = solve(3 - c); res = (r < 0) ? -1 : !r; }
    unmake(c, m, &u);
    return res;
}

static int try_h(int c, int nn) {
    Undo u; int old, res;
    int had_ep = ep_holder;
    hmake(nn, &u, &old);
    int t = had_ep ? terminal(c) : 0; /* expiry of an e.p. right can create a passer */
    if (t) res = (t == c);
    else { int r = solve(3 - c); res = (r < 0) ? -1 : !r; }
    hunmake(&u, old);
    return res;
}

static int solve(int c) {
    if (aborted) return -1;
    if (++nodes > cap) { aborted = 1; return -1; }
    uint64_t k1 = h1 ^ (c == 1 ? 0x1234567ULL : 0x7654321ULL), k2 = h2;
    TTE *e = &tt[k1 & (TTN - 1)];
    if (e->gen == gen && e->a == k1 && e->b == k2) return e->v;
    Mv mv[200];
    int n = gen_moves(c, mv);
    for (int i = 0; i < n; i++) if (mv[i].ty == 3) { ep_avail++; break; }
    int win = 0;
    /* pass 1: immediate decisions */
    signed char term[200];
    for (int i = 0; i < n && !win; i++) {
        Undo u; make(c, mv[i], &u);
        term[i] = (signed char)terminal(c);
        unmake(c, mv[i], &u);
        if (term[i] == c) win = 1;
    }
    for (int i = 0; i < n && !win; i++) {
        if (term[i]) continue;
        Undo u; make(c, mv[i], &u);
        int r = solve(3 - c);
        unmake(c, mv[i], &u);
        if (r < 0) return -1;
        if (!r) win = 1;
    }
    if (!win && Hn) {
        int lo = (c == 1) ? Hlo[hcur] : Hro[hcur], cnt = (c == 1) ? Hln[hcur] : Hrn[hcur];
        for (int j = 0; j < cnt && !win; j++) {
            int r = try_h(c, Hopt[lo + j]);
            if (r < 0) return -1;
            if (r) win = 1;
        }
    }
    e = &tt[k1 & (TTN - 1)];
    e->a = k1; e->b = k2; e->gen = gen; e->v = (int8_t)win;
    return win;
}

static int rd(FILE *f, long long *x) { return fscanf(f, "%lld", x) == 1; }

int main(void) {
    tt = calloc(TTN, sizeof(TTE));
    uint64_t s = 12345;
    for (int f = 0; f < MAXF; f++)
        for (int r = 0; r < NR + 2; r++) {
            for (int c = 0; c < 3; c++) { Z1[f][r][c] = sm(s++); Z2[f][r][c] = sm(s++ + 0x1000000ULL); }
            ZE1[f][r] = sm(s++ + 0x2000000ULL); ZE2[f][r] = sm(s++ + 0x3000000ULL);
        }
    ZS1 = sm(999999); ZS2 = sm(888888);
    Hlo = malloc(sizeof(int) * MAXH); Hln = malloc(sizeof(int) * MAXH);
    Hro = malloc(sizeof(int) * MAXH); Hrn = malloc(sizeof(int) * MAXH);
    Hopt = malloc(sizeof(int) * MAXH * 16);
    long long id, x;
    while (rd(stdin, &id)) {
        long long files, wrap, rule, aware, epon, cp, n;
        rd(stdin, &files); rd(stdin, &wrap); rd(stdin, &rule); rd(stdin, &aware); rd(stdin, &epon); rd(stdin, &cp);
        long long stp; rd(stdin, &stp); STOP = (int)stp;
        NF = (int)files; WRAP = (int)wrap; RULE = (int)rule; AWARE = (int)aware; EPON = (int)epon; cap = cp;
        memset(bd, 0, sizeof bd);
        h1 = h2 = 0;
        for (int c = 1; c <= 2; c++) {
            rd(stdin, &n);
            for (int i = 0; i < n; i++) {
                long long f, r; rd(stdin, &f); rd(stdin, &r);
                bd[f][r] = (signed char)c; h1 ^= Z1[f][r][c]; h2 ^= Z2[f][r][c];
            }
        }
        rd(stdin, &n); Hn = (int)n;
        int p = 0;
        for (int i = 0; i < Hn; i++) {
            long long nl, nr;
            rd(stdin, &nl); Hlo[i] = p; Hln[i] = (int)nl; for (int j = 0; j < nl; j++) { rd(stdin, &x); Hopt[p++] = (int)x; }
            if (p > MAXH * 15) { fprintf(stderr, "H too big\n"); return 1; }
            rd(stdin, &nr); Hro[i] = p; Hrn[i] = (int)nr; for (int j = 0; j < nr; j++) { rd(stdin, &x); Hopt[p++] = (int)x; }
        }
        hcur = 0; h1 ^= zh1(0); h2 ^= zh2(0);
        ep_holder = 0;
        gen++; nodes = 0; ep_avail = 0; ep_diff = 0; aborted = 0;
        printf("J %lld\n", id);
        if (has_passer(1) || has_passer(2)) { printf("X root has a passer\n"); }
        for (int c = 1; c <= 2; c++) {
            Mv mv[200]; int nm = gen_moves(c, mv); int won = 0;
            for (int i = 0; i < nm && !(STOP && won); i++) {
                int r = aborted ? -1 : try_pawn(c, mv[i]);
                if (r == 1) won = 1;
                printf("M %c %d %d %d %d %d\n", c == 1 ? 'W' : 'B', mv[i].ff, mv[i].fr, mv[i].tf, mv[i].tr, r);
            }
            if (Hn) {
                int lo = (c == 1) ? Hlo[0] : Hro[0], cnt = (c == 1) ? Hln[0] : Hrn[0];
                for (int j = 0; j < cnt && !(STOP && won); j++) {
                    int r = aborted ? -1 : try_h(c, Hopt[lo + j]);
                    if (r == 1) won = 1;
                    printf("H %c %d %d\n", c == 1 ? 'W' : 'B', j, r);
                }
            }
        }
        printf("E %lld %lld %lld %d\n", nodes, ep_avail, ep_diff, aborted);
        fflush(stdout);
    }
    return 0;
}
