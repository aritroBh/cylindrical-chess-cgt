/* gen.c -- enumerate core-in-wall rings.
 * usage: gen W P L PHASE [count]   (PHASE 0: wall starts W2 next to core's last file; 1: starts B4)
 * Core: W consecutive files, each non-empty, P core pawns, no passed pawn in the whole ring.
 * Ring order: c_0 .. c_{W-1}, x_0 .. x_{L-1} (cyclic), x alternates W2/B4 starting with W2 (phase 0) or B4 (phase 1).
 * Mirror reduction: L odd -> core <= reverse(core); L even -> only phase 0 is generated (phase 1 is the mirror image of phase 0 with reversed core).
 * White ranks 2..6, black ranks 3..7 (W on 7 / B on 2 is always passed; 1/8 impossible).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct { int w, b; } Cfg;     /* bit r set = pawn on rank r (r=1..8) */
static Cfg cfgs[4096]; static int ncfg, cnt[4096];
static int W, P, L, PH, countonly;
static int cur[16];
static long total = 0;
static int wallw[16], wallb[16]; /* wall file masks, index 0..L-1 */

static int pc(int m) { return __builtin_popcount(m); }
/* is white pawn at rank r on file with neighbours a,b,c (cfg masks of black) blocked? black pawn rank > r on any of 3 files */
static int wblocked(int r, int bn) { return (bn >> (r + 1)) != 0; }     /* ranks > r : bits r+1.. */
static int bblocked(int r, int wn) { return (wn & ((1 << r) - 1) & ~1) != 0; } /* white pawns rank < r: bits 1..r-1 */

static void emit(void) {
    total++;
    if (countonly) return;
    char line[512]; line[0] = 0; char tmp[64];
    for (int i = 0; i < W + L; i++) {
        int wm, bm;
        if (i < W) { wm = cfgs[cur[i]].w; bm = cfgs[cur[i]].b; } else { wm = wallw[i - W]; bm = wallb[i - W]; }
        tmp[0] = 0;
        if (wm) { strcat(tmp, "W"); for (int r = 1; r <= 8; r++) if (wm >> r & 1) { char c[2] = {'0' + r, 0}; strcat(tmp, c); } }
        if (bm) { strcat(tmp, "B"); for (int r = 1; r <= 8; r++) if (bm >> r & 1) { char c[2] = {'0' + r, 0}; strcat(tmp, c); } }
        strcat(line, tmp); if (i < W + L - 1) strcat(line, " ");
    }
    puts(line);
}

/* masks for file index in core with neighbours: left of 0 is wall[L-1], right of W-1 is wall[0] */
static void getm(int i, int *wm, int *bm) {
    if (i < 0) { *wm = wallw[L - 1]; *bm = wallb[L - 1]; }
    else if (i >= W) { *wm = wallw[0]; *bm = wallb[0]; }
    else { *wm = cfgs[cur[i]].w; *bm = cfgs[cur[i]].b; }
}
static int file_ok(int i) { /* check no passed pawn on core file i; neighbours must be assigned */
    int wl, bl, wc, bc, wr, br;
    getm(i - 1, &wl, &bl); getm(i, &wc, &bc); getm(i + 1, &wr, &br);
    int bn = bl | bc | br, wn = wl | wc | wr;
    for (int r = 2; r <= 7; r++) {
        if ((wc >> r & 1) && !wblocked(r, bn)) return 0;
        if ((bc >> r & 1) && !bblocked(r, wn)) return 0;
    }
    return 1;
}

static void dfs(int i, int used) {
    if (i == W) {
        if (used != P) return;
        if (!file_ok(W - 1) || !file_ok(0)) return;
        if (L % 2 == 1) { /* core <= reverse(core) */
            for (int k = 0; k < W; k++) { int a = cur[k], b = cur[W - 1 - k]; if (a < b) break; if (a > b) return; }
        }
        emit(); return;
    }
    int rem = W - i - 1; /* files after this */
    for (int c = 0; c < ncfg; c++) {
        int u = used + cnt[c];
        if (u + rem > P) continue;           /* each remaining file needs >= 1 */
        if (u + rem * 5 < P) continue;       /* upper bound */
        cur[i] = c;
        if (i >= 1 && !file_ok(i - 1)) continue;   /* file i-1 now has both neighbours (i-2, i) */
        dfs(i + 1, u);
    }
}

int main(int argc, char **argv) {
    W = atoi(argv[1]); P = atoi(argv[2]); L = atoi(argv[3]); PH = atoi(argv[4]); countonly = argc > 5;
    if (L % 2 == 0 && PH == 1) { return 0; }
    for (int j = 0; j < L; j++) {
        int isw = ((j + PH) % 2 == 0);
        wallw[j] = isw ? (1 << 2) : 0; wallb[j] = isw ? 0 : (1 << 4);
    }
    int maxk = P - (W - 1);
    for (int wm = 0; wm < 32; wm++) for (int bm = 0; bm < 32; bm++) {
        int w = wm << 2, b = bm << 3;   /* W ranks 2..6, B ranks 3..7 */
        if (w & b) continue;
        int k = pc(w) + pc(b);
        if (k < 1 || k > maxk) continue;
        cfgs[ncfg].w = w; cfgs[ncfg].b = b; cnt[ncfg] = k; ncfg++;
    }
    dfs(0, 0);
    if (countonly) printf("W=%d P=%d L=%d PH=%d cores=%ld\n", W, P, L, PH, total);
    return 0;
}
