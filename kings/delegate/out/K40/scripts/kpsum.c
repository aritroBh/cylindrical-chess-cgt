/* kpsum.c (K40) -- K+P vs K in the promotion model P of kings/theory/LOOPY.md, summed with a
 * terminal-free test game T (Left = White, Right = Black).  Written for K40 from SPEC/LOOPY only.
 *
 * Sum x (+) T, state (wk, bk, p, t, s):
 *  - s moves in x (any legal chess move) or in T (an s-option of t);
 *  - a move in T is illegal while s is in check (only Black can be in check: by the pawn);
 *  - P model: a pawn move onto the last rank ends the play, White wins (any promotion; the
 *    promoted piece is never looked at);  Kxp ends the play as a draw (K v K: no decisive event
 *    can occur any more, both kings move forever);
 *  - a side with no move at all: checkmated (Black in check) = White wins; otherwise stalemate =
 *    draw (chess / P rule).  Infinite play = draw.
 * Black has no decisive event of its own and White always keeps a king move or is stalemated
 * (draw), so in P every result is W or D.  With --normal, White can lose by having no move at
 * all; the solver computes the W set and the L set as least fixed points (repeated sweeps).
 *
 * Usage: kpsum W H WRAP TEST > out      TEST in: ints on off dud over under star up down pm1 zero
 *   "ints" is the chain -K..K (K = 12) in one graph; the output gives one column per root.
 * Output lines: "wk bk p s | r1 r2 ..." (squares like e4, s in w/b, r = W or D), for every legal
 * position: kings not adjacent, distinct squares, pawn on ranks 2..H-1, and with White to move
 * Black not in check.
 * --normal as 5th argument: a side with no move loses (normal play) instead of stalemate = draw.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int W, H, WRAP, N, NORMAL = 0, KXPLOSS = 0; /* --kxploss: Kxp counts as a Black win (diagnostic) */
#define MAXT 64
static int tn, tl[MAXT][4], tln[MAXT], tr[MAXT][4], trn[MAXT];
static int roots[MAXT], nroots;
static char rootname[MAXT][16];
static unsigned char *win; /* [((t*2+s)*N+wk)*N+bk)*N+p] */
static unsigned char *los; /* White loses (possible only with --normal) */

static int fl(int s) { return s % W; }
static int rk(int s) { return s / W; }
static int sq(int f, int r) {
    if (r < 0 || r >= H) return -1;
    if (WRAP) f = ((f % W) + W) % W; else if (f < 0 || f >= W) return -1;
    return r * W + f;
}
static int kn[64], kl[64][8];
static int adj[64][64];
static int patt[64][64]; /* patt[p][t]: white pawn on p attacks t */

static void geom(void) {
    for (int s = 0; s < N; s++) {
        kn[s] = 0;
        for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
            if (!df && !dr) continue;
            int t = sq(fl(s) + df, rk(s) + dr);
            if (t < 0 || t == s) continue;
            int dup = 0;
            for (int i = 0; i < kn[s]; i++) if (kl[s][i] == t) dup = 1;
            if (!dup) kl[s][kn[s]++] = t;
        }
    }
    memset(adj, 0, sizeof adj); memset(patt, 0, sizeof patt);
    for (int s = 0; s < N; s++) for (int i = 0; i < kn[s]; i++) adj[s][kl[s][i]] = 1;
    for (int p = 0; p < N; p++) for (int df = -1; df <= 1; df += 2) {
        int t = sq(fl(p) + df, rk(p) + 1);
        if (t >= 0) patt[p][t] = 1;
    }
}

static int legal(int s, int wk, int bk, int p) {
    if (wk == bk || wk == p || bk == p) return 0;
    if (rk(p) < 1 || rk(p) > H - 2) return 0;
    if (adj[wk][bk]) return 0;
    if (s == 0 && patt[p][bk]) return 0;
    return 1;
}

static size_t IX(int t, int s, int wk, int bk, int p) {
    return ((((size_t)t * 2 + s) * N + wk) * N + bk) * N + p;
}

static int node(void) { tln[tn] = trn[tn] = 0; return tn++; }
static void L(int a, int b) { tl[a][tln[a]++] = b; }
static void R(int a, int b) { tr[a][trn[a]++] = b; }
static void root(int a, const char *nm) { roots[nroots] = a; snprintf(rootname[nroots], 16, "%s", nm); nroots++; }

static void build(const char *T) {
    tn = nroots = 0;
    if (!strcmp(T, "ints")) {
        int K = 12, z = node(), prevp = z, prevn = z;
        int pos[13], negs[13]; pos[0] = negs[0] = z;
        for (int i = 1; i <= K; i++) { int a = node(); L(a, prevp); prevp = pos[i] = a; }
        for (int i = 1; i <= K; i++) { int a = node(); R(a, prevn); prevn = negs[i] = a; }
        char b[16];
        for (int i = K; i >= 1; i--) { snprintf(b, 16, "%d", -i); root(negs[i], b); }
        root(z, "0");
        for (int i = 1; i <= K; i++) { snprintf(b, 16, "%d", i); root(pos[i], b); }
    } else if (!strcmp(T, "zero")) { root(node(), "0");
    } else if (!strcmp(T, "on")) { int a = node(); L(a, a); root(a, "on");
    } else if (!strcmp(T, "off")) { int a = node(); R(a, a); root(a, "off");
    } else if (!strcmp(T, "dud")) { int a = node(); L(a, a); R(a, a); root(a, "dud");
    } else if (!strcmp(T, "over")) { int a = node(), z = node(); L(a, z); R(a, a); root(a, "over");
    } else if (!strcmp(T, "under")) { int a = node(), z = node(); L(a, a); R(a, z); root(a, "under");
    } else if (!strcmp(T, "star")) { int a = node(), z = node(); L(a, z); R(a, z); root(a, "*");
    } else if (!strcmp(T, "up")) { int a = node(), z = node(), st = node(); L(st, z); R(st, z); L(a, z); R(a, st); root(a, "up");
    } else if (!strcmp(T, "down")) { int a = node(), z = node(), st = node(); L(st, z); R(st, z); L(a, st); R(a, z); root(a, "down");
    } else if (!strcmp(T, "pm1")) { int a = node(), z = node(), o = node(), m = node(); L(o, z); R(m, z); L(a, o); R(a, m); root(a, "+-1");
    } else { fprintf(stderr, "unknown test %s\n", T); exit(1); }
}

/* evaluate state; returns 1 if White wins given current table */
static int eval(int t, int s, int wk, int bk, int p) {
    int nmoves = 0;
    if (s == 0) {
        for (int i = 0; i < kn[wk]; i++) {
            int d = kl[wk][i];
            if (d == p || d == bk || adj[d][bk]) continue;
            nmoves++;
            if (win[IX(t, 1, d, bk, p)]) return 1;
        }
        int p1 = sq(fl(p), rk(p) + 1);
        if (p1 != wk && p1 != bk) {
            nmoves++;
            if (rk(p1) == H - 1) return 1;
            if (win[IX(t, 1, wk, bk, p1)]) return 1;
            if (rk(p) == 1) {
                int p2 = sq(fl(p), 3);
                if (p2 != wk && p2 != bk) {
                    nmoves++;
                    if (rk(p2) == H - 1) return 1;
                    if (win[IX(t, 1, wk, bk, p2)]) return 1;
                }
            }
        }
        for (int i = 0; i < tln[t]; i++) { nmoves++; if (win[IX(tl[t][i], 1, wk, bk, p)]) return 1; }
        if (nmoves == 0 && NORMAL) return 0; /* White loses: not a White win */
        return 0;
    } else {
        int check = patt[p][bk];
        for (int i = 0; i < kn[bk]; i++) {
            int d = kl[bk][i];
            if (d == wk || adj[d][wk] || patt[p][d]) continue;
            nmoves++;
            if (d == p) return 0; /* Kxp: draw */
            if (!win[IX(t, 0, wk, d, p)]) return 0;
        }
        if (!check) for (int i = 0; i < trn[t]; i++) { nmoves++; if (!win[IX(tr[t][i], 0, wk, bk, p)]) return 0; }
        if (nmoves == 0) return (check || NORMAL) ? 1 : 0;
        return 1;
    }
}

/* returns 1 if White loses given current tables (only reachable under --normal) */
static int evall(int t, int s, int wk, int bk, int p) {
    int nmoves = 0;
    if (s == 0) {
        for (int i = 0; i < kn[wk]; i++) {
            int d = kl[wk][i];
            if (d == p || d == bk || adj[d][bk]) continue;
            nmoves++;
            if (!los[IX(t, 1, d, bk, p)]) return 0;
        }
        int p1 = sq(fl(p), rk(p) + 1);
        if (p1 != wk && p1 != bk) {
            nmoves++;
            if (rk(p1) == H - 1) return 0;
            if (!los[IX(t, 1, wk, bk, p1)]) return 0;
            if (rk(p) == 1) {
                int p2 = sq(fl(p), 3);
                if (p2 != wk && p2 != bk) {
                    nmoves++;
                    if (rk(p2) == H - 1) return 0;
                    if (!los[IX(t, 1, wk, bk, p2)]) return 0;
                }
            }
        }
        for (int i = 0; i < tln[t]; i++) { nmoves++; if (!los[IX(tl[t][i], 1, wk, bk, p)]) return 0; }
        if (nmoves == 0) return NORMAL;
        return 1;
    } else {
        int check = patt[p][bk];
        for (int i = 0; i < kn[bk]; i++) {
            int d = kl[bk][i];
            if (d == wk || adj[d][wk] || patt[p][d]) continue;
            if (d == p) { if (KXPLOSS) return 1; continue; } /* Kxp: draw, not a Black win */
            if (los[IX(t, 0, wk, d, p)]) return 1;
        }
        if (!check) for (int i = 0; i < trn[t]; i++) if (los[IX(tr[t][i], 0, wk, bk, p)]) return 1;
        return 0;
    }
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: kpsum W H WRAP TEST [--normal]\n"); return 1; }
    W = atoi(argv[1]); H = atoi(argv[2]); WRAP = atoi(argv[3]); N = W * H;
    for (int i = 5; i < argc; i++) {
        if (!strcmp(argv[i], "--normal")) NORMAL = 1;
        if (!strcmp(argv[i], "--kxploss")) KXPLOSS = 1;
    }
    if (N > 64) { fprintf(stderr, "board too big\n"); return 1; }
    geom(); build(argv[4]);
    size_t tot = (size_t)tn * 2 * N * N * N;
    win = calloc(tot, 1); los = calloc(tot, 1);
    int changed = 1, sweeps = 0;
    while (changed) {
        changed = 0; sweeps++;
        for (int t = 0; t < tn; t++) for (int s = 0; s < 2; s++)
            for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) for (int p = 0; p < N; p++) {
                size_t i = IX(t, s, wk, bk, p);
                if (win[i] || !legal(s, wk, bk, p)) continue;
                if (eval(t, s, wk, bk, p)) { win[i] = 1; changed = 1; }
                else if (!los[i] && evall(t, s, wk, bk, p)) { los[i] = 1; changed = 1; }
            }
    }
    fprintf(stderr, "kpsum %s:%dx%d %s: %d test nodes, %d sweeps\n", WRAP ? "cyl" : "flat", W, H, argv[4], tn, sweeps);
    printf("# roots:");
    for (int r = 0; r < nroots; r++) printf(" %s", rootname[r]);
    printf("\n");
    for (int s = 0; s < 2; s++) for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) for (int p = 0; p < N; p++) {
        if (!legal(s, wk, bk, p)) continue;
        printf("%c%d %c%d %c%d %c |", 'a' + fl(wk), rk(wk) + 1, 'a' + fl(bk), rk(bk) + 1, 'a' + fl(p), rk(p) + 1, s ? 'b' : 'w');
        for (int r = 0; r < nroots; r++) printf(" %c", win[IX(roots[r], s, wk, bk, p)] ? 'W' : los[IX(roots[r], s, wk, bk, p)] ? 'L' : 'D');
        printf("\n");
    }
    free(win); free(los);
    return 0;
}
