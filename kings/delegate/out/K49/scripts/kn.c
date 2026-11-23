/* K49: own solver for x (+) T, x a K+P v K position on cyl:WxH in the P model, T a finite terminal-free test game.
 * Written from kings/SPEC.md and LOOPY Definitions 1.2, 1.3, 1.5 only (not from K40's kpsum.c or ksum2.py).
 * Rules: a promotion is a White win at once (P); Kxp is a draw terminal (K v K is dead, K40 Lemma 1);
 * a T-move is illegal while Black is in check (only Black can be in check, by the pawn);
 * a side with no move: Black in check = mated = White wins; otherwise (N) the side to move loses,
 * or (C, flag -c) stalemate is a draw.  White never wins by anything else; Black never wins on W != 4 (K40 Cor. 3),
 * but the code computes the Black-win set as well under (N).
 * Usage: kn W H TFILE [-c]
 *   TFILE: line 1 "n", then n lines "L: a b ... ; R: c d ..." (node ids 0..n-1), then root lines "name node".
 * Output: one line per legal (wk,bk,p,stm): "wk bk p stm | r_root1 r_root2 ..." (W/D/L), header "#roots: ...".
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int W, H, N, NT, CHESS = 0, KXPLOSS = 0;
static int tl[64][16], tln[64], tr[64][16], trn[64];
static unsigned char *val; /* 0 unknown(draw), 1 White wins, 2 Black wins */

static int sq(int f, int r) { if (r < 0 || r >= H) return -1; return r * W + ((f % W) + W) % W; }
static int adj(int a, int b) {
    int fa = a % W, ra = a / W, fb = b % W, rb = b / W;
    int df = (fa - fb + W) % W; if (df > W - df) df = W - df;
    int dr = ra > rb ? ra - rb : rb - ra;
    return a != b && df <= 1 && dr <= 1;
}
static int patt(int p, int s) { /* white pawn on p attacks s */
    int f = p % W, r = p / W;
    return (s == sq(f - 1, r + 1) || s == sq(f + 1, r + 1));
}
static long IX(int t, int stm, int wk, int bk, int p) { return ((((long)t * 2 + stm) * N + wk) * N + bk) * N + p; }
static int legal(int wk, int bk, int p, int stm) {
    if (wk == bk || wk == p || bk == p) return 0;
    if (p / W < 1 || p / W > H - 2) return 0;
    if (adj(wk, bk)) return 0;
    if (stm == 0 && patt(p, bk)) return 0; /* side not to move (Black) in check */
    return 1;
}
/* value from White's view: returns 1 win, 2 loss, 0 undecided */
static int eval(int t, int stm, int wk, int bk, int p) {
    int nm = 0, anyD = 0, allW = 1;
    if (stm == 0) { /* White */
        int f = wk % W, r = wk / W;
        for (int a = -1; a <= 1; a++) for (int b = -1; b <= 1; b++) {
            if (!a && !b) continue; int s = sq(f + a, r + b); if (s < 0 || s == wk || s == p || adj(s, bk) || s == bk) continue;
            nm++; int v = val[IX(t, 1, s, bk, p)]; if (v == 1) return 1; if (v != 2) allW = 0;
        }
        int pf = p % W, pr = p / W, s1 = sq(pf, pr + 1);
        if (s1 != bk && s1 != wk) {
            nm++; if (pr + 1 == H - 1) return 1;
            int v = val[IX(t, 1, wk, bk, s1)]; if (v == 1) return 1; if (v != 2) allW = 0;
            if (pr == 1) { int s2 = sq(pf, 3); if (s2 >= 0 && s2 != bk && s2 != wk) { nm++; if (3 == H - 1) return 1;
                v = val[IX(t, 1, wk, bk, s2)]; if (v == 1) return 1; if (v != 2) allW = 0; } }
        }
        for (int i = 0; i < tln[t]; i++) { nm++; int v = val[IX(tl[t][i], 1, wk, bk, p)]; if (v == 1) return 1; if (v != 2) allW = 0; }
        if (nm == 0) return CHESS ? 0 : 2;
        return allW ? 2 : 0;
    } else { /* Black: want a non-win for White */
        int check = patt(p, bk), f = bk % W, r = bk / W; int allwin = 1, anyL = 0;
        for (int a = -1; a <= 1; a++) for (int b = -1; b <= 1; b++) {
            if (!a && !b) continue; int s = sq(f + a, r + b); if (s < 0 || s == bk || adj(s, wk) || s == wk || patt(p, s)) continue;
            nm++;
            if (s == p) { allwin = 0; if (KXPLOSS) anyL = 1; continue; } /* Kxp: dead draw (p unprotected since s not adjacent to wk) */
            int v = val[IX(t, 0, wk, s, p)]; if (v == 2) anyL = 1; if (v != 1) allwin = 0;
        }
        if (!check) for (int i = 0; i < trn[t]; i++) { nm++; int v = val[IX(tr[t][i], 0, wk, bk, p)]; if (v == 2) anyL = 1; if (v != 1) allwin = 0; }
        (void)anyD;
        if (nm == 0) return (check || !CHESS) ? 1 : 0;
        if (anyL) return 2;
        return allwin ? 1 : 0;
    }
}
int main(int argc, char **argv) {
    W = atoi(argv[1]); H = atoi(argv[2]); N = W * H; for (int a = 4; a < argc; a++) { if (!strcmp(argv[a], "-c")) CHESS = 1; if (!strcmp(argv[a], "-k")) KXPLOSS = 1; }
    FILE *fh = fopen(argv[3], "r"); char ln[4096]; char names[64][32]; int roots[64], nr = 0;
    fgets(ln, sizeof ln, fh); NT = atoi(ln);
    for (int i = 0; i < NT; i++) {
        fgets(ln, sizeof ln, fh); char *q = strstr(ln, "L:"), *rr = strstr(ln, "R:"); tln[i] = trn[i] = 0;
        char *e = q + 2; while (e < rr) { while (*e == ' ') e++; if (*e >= '0' && *e <= '9') { tl[i][tln[i]++] = strtol(e, &e, 10); } else e++; }
        e = rr + 2; while (*e) { while (*e == ' ') e++; if (*e >= '0' && *e <= '9') { tr[i][trn[i]++] = strtol(e, &e, 10); } else if (*e) e++; }
    }
    while (fgets(ln, sizeof ln, fh)) { if (sscanf(ln, "%31s %d", names[nr], &roots[nr]) == 2) nr++; }
    fclose(fh);
    long tot = (long)NT * 2 * N * N * N; val = calloc(tot, 1);
    int ch = 1, sweeps = 0;
    while (ch) { ch = 0; sweeps++;
        for (int t = 0; t < NT; t++) for (int stm = 0; stm < 2; stm++) for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) for (int p = 0; p < N; p++) {
            long i = IX(t, stm, wk, bk, p); if (val[i] || !legal(wk, bk, p, stm)) continue;
            int v = eval(t, stm, wk, bk, p); if (v) { val[i] = v; ch = 1; }
        }
    }
    printf("#roots:"); for (int k = 0; k < nr; k++) printf(" %s", names[k]); printf("\n");
    for (int stm = 0; stm < 2; stm++) for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) for (int p = 0; p < N; p++) {
        if (!legal(wk, bk, p, stm)) continue;
        printf("%c%d %c%d %c%d %c |", 'a' + wk % W, wk / W + 1, 'a' + bk % W, bk / W + 1, 'a' + p % W, p / W + 1, stm ? 'b' : 'w');
        for (int k = 0; k < nr; k++) printf(" %c", "WDL"[val[IX(roots[k], stm, wk, bk, p)] == 1 ? 0 : val[IX(roots[k], stm, wk, bk, p)] == 2 ? 2 : 1]);
        printf("\n");
    }
    fprintf(stderr, "sweeps %d\n", sweeps);
    return 0;
}
