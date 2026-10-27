/* samp.c -- uniform random sample of valid core-in-wall rings (no passed pawn), by DP-uniform tuple sampling + rejection.
 * usage: samp W P L PHASE NSAMPLES SEED   -> prints NSAMPLES ring lines (may contain duplicates), stats to stderr.
 * No mirror reduction here: every ordered core tuple (valid) is equally likely. For L=4 only phase 0 is meaningful (phase 1 = mirror).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef struct { int w, b; } Cfg;
static Cfg cfgs[4096]; static int ncfg, cnt[4096];
static int W, P, L, PH;
static int wallw[16], wallb[16];
static double ways[16][64];
static uint64_t s[2];
static uint64_t rnd(void) { uint64_t s1 = s[0], s0 = s[1]; s[0] = s0; s1 ^= s1 << 23; s[1] = s1 ^ s0 ^ (s1 >> 18) ^ (s0 >> 5); return s[1] + s0; }
static double rnd01(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static int pc(int m) { return __builtin_popcount(m); }
static int cur[16];
static void getm(int i, int *wm, int *bm) {
    if (i < 0) { *wm = wallw[L - 1]; *bm = wallb[L - 1]; }
    else if (i >= W) { *wm = wallw[0]; *bm = wallb[0]; }
    else { *wm = cfgs[cur[i]].w; *bm = cfgs[cur[i]].b; }
}
static int file_ok(int i) {
    int wl, bl, wc, bc, wr, br;
    getm(i - 1, &wl, &bl); getm(i, &wc, &bc); getm(i + 1, &wr, &br);
    int bn = bl | bc | br, wn = wl | wc | wr;
    for (int r = 2; r <= 7; r++) {
        if ((wc >> r & 1) && (bn >> (r + 1)) == 0) return 0;
        if ((bc >> r & 1) && (wn & ((1 << r) - 1) & ~1) == 0) return 0;
    }
    return 1;
}
int main(int argc, char **argv) {
    W = atoi(argv[1]); P = atoi(argv[2]); L = atoi(argv[3]); PH = atoi(argv[4]);
    long NS = atol(argv[5]); uint64_t seed = strtoull(argv[6], 0, 10);
    s[0] = seed * 0x9E3779B97F4A7C15ULL + 1; s[1] = seed ^ 0xDEADBEEFCAFEF00DULL; for (int i = 0; i < 20; i++) rnd();
    for (int j = 0; j < L; j++) { int isw = ((j + PH) % 2 == 0); wallw[j] = isw ? (1 << 2) : 0; wallb[j] = isw ? 0 : (1 << 4); }
    int maxk = P - (W - 1);
    for (int wm = 0; wm < 32; wm++) for (int bm = 0; bm < 32; bm++) {
        int w = wm << 2, b = bm << 3; if (w & b) continue;
        int k = pc(w) + pc(b); if (k < 1 || k > maxk) continue;
        cfgs[ncfg].w = w; cfgs[ncfg].b = b; cnt[ncfg] = k; ncfg++;
    }
    /* ways[i][rem]: number of tuples for files i..W-1 with total rem */
    for (int r = 0; r < 64; r++) ways[W][r] = (r == 0);
    for (int i = W - 1; i >= 0; i--) for (int r = 0; r < 64; r++) { double t = 0; for (int c = 0; c < ncfg; c++) if (cnt[c] <= r) t += ways[i + 1][r - cnt[c]]; ways[i][r] = t; }
    long out = 0, tries = 0;
    while (out < NS) {
        int rem = P; tries++;
        for (int i = 0; i < W; i++) {
            double x = rnd01() * ways[i][rem], acc = 0; int pick = -1;
            for (int c = 0; c < ncfg; c++) if (cnt[c] <= rem) { acc += ways[i + 1][rem - cnt[c]]; if (x < acc) { pick = c; break; } }
            if (pick < 0) { for (int c = ncfg - 1; c >= 0; c--) if (cnt[c] <= rem && ways[i + 1][rem - cnt[c]] > 0) { pick = c; break; } }
            cur[i] = pick; rem -= cnt[pick];
        }
        int ok = 1; for (int i = 0; i < W && ok; i++) ok = file_ok(i);
        if (!ok) continue;
        char line[512]; line[0] = 0; char tmp[64];
        for (int i = 0; i < W + L; i++) {
            int wm, bm;
            if (i < W) { wm = cfgs[cur[i]].w; bm = cfgs[cur[i]].b; } else { wm = wallw[i - W]; bm = wallb[i - W]; }
            tmp[0] = 0;
            if (wm) { strcat(tmp, "W"); for (int r = 1; r <= 8; r++) if (wm >> r & 1) { char c[2] = {'0' + r, 0}; strcat(tmp, c); } }
            if (bm) { strcat(tmp, "B"); for (int r = 1; r <= 8; r++) if (bm >> r & 1) { char c[2] = {'0' + r, 0}; strcat(tmp, c); } }
            strcat(line, tmp); if (i < W + L - 1) strcat(line, " ");
        }
        puts(line); out++;
    }
    fprintf(stderr, "W=%d P=%d L=%d PH=%d: %ld valid in %ld tries (accept %.5f), total tuples %.4g\n", W, P, L, PH, out, tries, (double)out / tries, ways[0][P]);
    return 0;
}
