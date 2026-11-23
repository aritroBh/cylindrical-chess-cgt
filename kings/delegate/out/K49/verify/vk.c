/* K49 referee: own solver for x (+) T, x = K+P v K on cyl:WxH (P model), T a finite test game.
   Written from kings/SPEC.md and LOOPY Defs 1.2, 1.3, 1.5 only (K49's kn.c not read).
   Convention (N): a side with no move loses. Check rule: Black in check may not move in T.
   Promotion = White win; Kxp = dead draw (or Black win with -k).
   Usage: vk W H TFILE [-k] [-q QUERYFILE]
   TFILE: first line n, then n lines "name nl l1.. nr r1.." (node 0 is the root by default).
   Output (no -q): one line per legal (wk,p,bk,side,t-root):  "wk p bk s res" for every T node? no: we print for t=0 only.
   Squares printed as algebraic. res in W D L. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int W, H, NT, KXPL = 0;
static int nl[64], nr[64], lo[64][8], ro[64][8];
static char tname[64][32];

static int sq(int f, int r) { return r * W + f; }
static int fil(int s) { return s % W; }
static int rnk(int s) { return s / W; }
static int fd(int a, int b) { int d = abs(a - b); return d < W - d ? d : W - d; }
static int adj(int a, int b) { return a != b && fd(fil(a), fil(b)) <= 1 && abs(rnk(a) - rnk(b)) <= 1; }
static int pattacks(int p, int s) { return rnk(s) == rnk(p) + 1 && fd(fil(s), fil(p)) == 1; }

static int NS;
static int idx(int wk, int p, int bk, int side, int t) { return ((((t * 2 + side) * NS + wk) * NS + p) * NS + bk); }
static int legal(int wk, int p, int bk, int side) {
    if (wk == p || wk == bk || p == bk) return 0;
    if (rnk(p) < 1 || rnk(p) > H - 2) return 0;
    if (adj(wk, bk)) return 0;
    if (side == 0 && pattacks(p, bk)) return 0; /* White to move, Black in check: illegal */
    return 1;
}
/* value codes: 0 unknown, 1 W, 2 L */
static unsigned char *val;

/* enumerate options; returns codes: -1 = promotion (W), -2 = Kxp (D or L), else index */
static int opts(int wk, int p, int bk, int side, int t, int *o) {
    int n = 0;
    if (side == 0) { /* White */
        for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
            if (!df && !dr) continue;
            int r = rnk(wk) + dr; if (r < 0 || r >= H) continue;
            int s = sq((fil(wk) + df + W) % W, r);
            if (s == p || s == bk || adj(s, bk)) continue;
            o[n++] = idx(s, p, bk, 1, t);
        }
        int f = fil(p), r = rnk(p);
        int s1 = sq(f, r + 1);
        if (s1 != wk && s1 != bk) {
            if (r + 1 == H - 1) o[n++] = -1;
            else {
                o[n++] = idx(wk, s1, bk, 1, t);
                if (r == 1) { int s2 = sq(f, r + 2); if (s2 != wk && s2 != bk) { if (r + 2 == H - 1) o[n++] = -1; else o[n++] = idx(wk, s2, bk, 1, t); } }
            }
        }
        for (int i = 0; i < nl[t]; i++) o[n++] = idx(wk, p, bk, 1, lo[t][i]);
    } else {
        int check = pattacks(p, bk);
        for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
            if (!df && !dr) continue;
            int r = rnk(bk) + dr; if (r < 0 || r >= H) continue;
            int s = sq((fil(bk) + df + W) % W, r);
            if (s == wk || adj(s, wk) || pattacks(p, s)) continue;
            if (s == p) { o[n++] = -2; continue; }
            o[n++] = idx(wk, p, s, 0, t);
        }
        if (!check) for (int i = 0; i < nr[t]; i++) o[n++] = idx(wk, p, bk, 0, ro[t][i]);
    }
    return n;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage\n"); return 1; }
    W = atoi(argv[1]); H = atoi(argv[2]);
    for (int i = 4; i < argc; i++) if (!strcmp(argv[i], "-k")) KXPL = 1;
    FILE *tf = fopen(argv[3], "r"); if (!tf) return 1;
    if (fscanf(tf, "%d", &NT) != 1) return 1;
    for (int i = 0; i < NT; i++) {
        if (fscanf(tf, "%31s %d", tname[i], &nl[i]) != 2) return 1;
        for (int j = 0; j < nl[i]; j++) if (fscanf(tf, "%d", &lo[i][j]) != 1) return 1;
        if (fscanf(tf, "%d", &nr[i]) != 1) return 1;
        for (int j = 0; j < nr[i]; j++) if (fscanf(tf, "%d", &ro[i][j]) != 1) return 1;
    }
    fclose(tf);
    NS = W * H;
    long N = (long)NT * 2 * NS * NS * NS;
    val = calloc(N, 1);
    int o[64];
    /* White-win least fixed point, then Black-win least fixed point (simple sweeps) */
    for (int pass = 1; pass <= 2; pass++) {
        int changed = 1;
        while (changed) {
            changed = 0;
            for (int t = 0; t < NT; t++) for (int side = 0; side < 2; side++)
            for (int wk = 0; wk < NS; wk++) for (int p = 0; p < NS; p++) for (int bk = 0; bk < NS; bk++) {
                int i = idx(wk, p, bk, side, t);
                if (val[i] || !legal(wk, p, bk, side)) continue;
                int n = opts(wk, p, bk, side, t, o);
                int mover_wins_code = (side == 0) ? 1 : 2;
                if (pass == 1 && mover_wins_code != 1 && 0) {}
                int target = pass; /* computing set of 'target' wins */
                int win = 0;
                if ((side == 0 && target == 1) || (side == 1 && target == 2)) {
                    /* mover is the target: needs one option winning */
                    for (int k = 0; k < n; k++) {
                        if (o[k] == -1) { if (target == 1) win = 1; }
                        else if (o[k] == -2) { if (target == 2 && KXPL) win = 1; }
                        else if (val[o[k]] == target) win = 1;
                        if (win) break;
                    }
                } else {
                    /* opponent moves: all options must be target wins (no options -> target wins, (N)) */
                    win = 1;
                    for (int k = 0; k < n; k++) {
                        if (o[k] == -1) { if (target != 1) { win = 0; break; } }
                        else if (o[k] == -2) { if (!(target == 2 && KXPL)) { win = 0; break; } }
                        else if (val[o[k]] != target) { win = 0; break; }
                    }
                }
                (void)mover_wins_code;
                if (win) { val[i] = target; changed = 1; }
            }
        }
    }
    /* print root (t=0) results for every legal position */
    for (int side = 0; side < 2; side++)
    for (int wk = 0; wk < NS; wk++) for (int p = 0; p < NS; p++) for (int bk = 0; bk < NS; bk++) {
        if (!legal(wk, p, bk, side)) continue;
        int v = val[idx(wk, p, bk, side, 0)];
        printf("K%c%d P%c%d k%c%d %c %c\n", 'a' + fil(wk), rnk(wk) + 1, 'a' + fil(p), rnk(p) + 1, 'a' + fil(bk), rnk(bk) + 1,
               side ? 'b' : 'w', v == 1 ? 'W' : v == 2 ? 'L' : 'D');
    }
    free(val);
    return 0;
}
