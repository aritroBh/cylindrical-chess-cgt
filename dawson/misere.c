/* Misere Dawson's chess (octal 0.137) by exhaustive search over all multisets of heap
 * sizes with total <= T.  Second, independent implementation of dawson/misere.py.
 *
 * A position is a partition (multiset of heaps). Exact simplifications: heaps of size 0 are
 * dropped, and a heap of size 2 is replaced by a heap of size 1 (both have exactly one
 * option, the empty position, so their game trees are identical). Positions are indexed by
 * a ranking of partitions into parts != 2, ordered by total; every option has a smaller
 * total, so one pass over totals 0..T is a valid bottom-up evaluation.
 *
 * Build:  cc -O2 -o dawson/misere_c dawson/misere.c
 * Run:    dawson/misere_c T [outfile]
 *   prints per-total counts and the single-heap / single-ring outcomes; with outfile, writes
 *   one byte per position (1 = misere P) in index order, for later analysis.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXT 128
static int T;
static int64_t q[MAXT + 1][MAXT + 1];   /* q[t][m]: partitions of t, parts <= m, no part 2 */
static int64_t S[MAXT + 1][MAXT + 1];   /* S[t][j] = sum_{k=1..j, k!=2, k<=t} q[t-k][k] */
static int64_t off[MAXT + 2];
static uint8_t *P;                       /* 0 = not computed/N, 1 = P */
static int64_t npos;

static int64_t rank_of(const int *lam, int len) {   /* lam descending, all parts != 2 */
    int t = 0;
    for (int i = 0; i < len; i++) t += lam[i];
    int64_t r = off[t];
    for (int i = 0; i < len; i++) {
        r += S[t][lam[i] - 1];
        t -= lam[i];
    }
    return r;
}

/* scratch */
static int cur[MAXT + 2];
static int curlen;
static int64_t cntP[MAXT + 1], cnt[MAXT + 1], tamefail[MAXT + 1];
static int g[MAXT + 8];

static int build(int *dst, const int *src, int len, int skip, int a, int b) {
    /* copy src minus index skip, insert parts a, b (0 = none; 2 -> 1), keep descending */
    int tmp[MAXT + 4], n = 0;
    for (int i = 0; i < len; i++) if (i != skip) tmp[n++] = src[i];
    int ins[2], ni = 0;
    if (a == 2) a = 1;
    if (b == 2) b = 1;
    if (a > 0) ins[ni++] = a;
    if (b > 0) ins[ni++] = b;
    for (int k = 0; k < ni; k++) {
        int x = ins[k], j = n;
        while (j > 0 && tmp[j - 1] < x) { tmp[j] = tmp[j - 1]; j--; }
        tmp[j] = x;
        n++;
    }
    memcpy(dst, tmp, n * sizeof(int));
    return n;
}

static int isP_opt(const int *lam, int len, int skip, int a, int b) {
    int d[MAXT + 4];
    int n = build(d, lam, len, skip, a, b);
    return P[rank_of(d, n)];
}

static int evaluate(const int *lam, int len) {
    if (len == 0) return 0;               /* empty position: misere N */
    for (int i = 0; i < len; i++) {
        if (i > 0 && lam[i] == lam[i - 1]) continue;
        int h = lam[i];
        if (h == 1) { if (isP_opt(lam, len, i, 0, 0)) return 0; continue; }
        /* h >= 3 : remove 2 from an end -> h-2 ; remove 3 -> h-3 or split a + (h-3-a) */
        if (isP_opt(lam, len, i, h - 2, 0)) return 0;
        if (isP_opt(lam, len, i, h - 3, 0)) return 0;
        for (int a = 1; a <= (h - 3) / 2; a++)
            if (isP_opt(lam, len, i, a, h - 3 - a)) return 0;
    }
    return 1;
}

static int misere_nim_P(const int *lam, int len) {
    int big = 0, x = 0, ones = 0;
    for (int i = 0; i < len; i++) { int v = g[lam[i]]; if (v >= 2) big = 1; x ^= v; ones += (v == 1); }
    if (!big) return ones % 2 == 1;
    return x == 0;
}

static void gen(int t, int rem, int maxp) {
    if (rem == 0) {
        int64_t r = rank_of(cur, curlen);
        int v = evaluate(cur, curlen);
        P[r] = (uint8_t)v;
        cnt[t]++;
        cntP[t] += v;
        if (v != misere_nim_P(cur, curlen)) tamefail[t]++;
        return;
    }
    for (int k = (maxp < rem ? maxp : rem); k >= 1; k--) {
        if (k == 2) continue;
        cur[curlen++] = k;
        gen(t, rem - k, k);
        curlen--;
    }
}

int main(int argc, char **argv) {
    T = argc > 1 ? atoi(argv[1]) : 40;
    if (T > MAXT) { fprintf(stderr, "T too large\n"); return 1; }
    /* normal-play Grundy values of 0.137 for the tame comparison */
    g[0] = 0;
    for (int n = 1; n <= T + 4; n++) {
        int seen[256] = {0};
        if (n == 1 || n == 2) seen[0] = 1;
        if (n >= 3) {
            seen[g[n - 2]] = 1;
            for (int a = 0; a <= n - 3; a++) seen[g[a] ^ g[n - 3 - a]] = 1;
        }
        int m = 0; while (seen[m]) m++;
        g[n] = m;
    }
    for (int m = 0; m <= T; m++) q[0][m] = 1;
    for (int t = 1; t <= T; t++) {
        q[t][0] = 0;
        for (int m = 1; m <= T; m++)
            q[t][m] = q[t][m - 1] + ((m != 2 && m <= t) ? q[t - m][m] : 0);
    }
    for (int t = 0; t <= T; t++) {
        S[t][0] = 0;
        for (int j = 1; j <= T; j++)
            S[t][j] = S[t][j - 1] + ((j != 2 && j <= t) ? q[t - j][j] : 0);
    }
    off[0] = 0;
    for (int t = 0; t <= T; t++) off[t + 1] = off[t] + q[t][t];
    npos = off[T + 1];
    P = calloc(npos, 1);
    if (!P) { fprintf(stderr, "alloc failed\n"); return 1; }
    printf("misere 0.137: %lld canonical positions with total <= %d\n", (long long)npos, T);
    fflush(stdout);
    for (int t = 0; t <= T; t++) {
        curlen = 0;
        gen(t, t, t);
        printf("total %3d: %10lld positions %9lld P   misere-Nim-rule failures %9lld\n", t,
               (long long)cnt[t], (long long)cntP[t], (long long)tamefail[t]);
        fflush(stdout);
    }
    printf("single strip n=0..%d: ", T);
    for (int n = 0; n <= T; n++) {
        int lam[1] = {n == 2 ? 1 : n};
        int v = n == 0 ? 0 : P[rank_of(lam, 1)];
        putchar(v ? 'P' : 'N');
    }
    printf("\nsingle strips that are misere P:");
    for (int n = 1; n <= T; n++) { int lam[1] = {n == 2 ? 1 : n}; if (P[rank_of(lam, 1)]) printf(" %d", n); }
    printf("\nsingle rings (n = 3..%d) that are misere N (first player wins):", T + 3);
    for (int n = 3; n <= T + 3; n++) {
        int s = n - 3, v;
        if (s == 0) v = 0; else { int lam[1] = {s == 2 ? 1 : s}; v = P[rank_of(lam, 1)]; }
        if (v) printf(" %d", n);
    }
    printf("\n");
    if (argc > 2) {
        FILE *f = fopen(argv[2], "wb");
        fwrite(P, 1, npos, f);
        fclose(f);
        printf("wrote %s\n", argv[2]);
    }
    return 0;
}
