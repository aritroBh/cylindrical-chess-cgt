/* Independent verifier for claim C4 (verify/dawson/C4-reproduce).
 * Written from the game definitions, not from dawson/octal.py or cylcgt/dawson.py.
 *
 * Game A ("pins"): a row of n pins; a move picks pin i (0-based) and removes it together
 *   with whichever of pins i-1, i+1 exist. Left remainder: max(i-1,0) pins; right
 *   remainder: max(n-i-2,0) pins.  This is octal 0.137.
 * Game B (Dawson's Kayles 0.07): a row of m pins; a move removes two ADJACENT pins
 *   j, j+1 (0 <= j <= m-2); remainders j and m-j-2.
 * Prints: g_A(0..N), checks g_A(n) == g_B(n+1), lists every n <= N-34 with
 * g_A(n) != g_A(n+34), the Guy-Smith certificate for (n0=52, p=34, k=3), and least
 * eventual period on [N/2, N].
 * Usage: ./indep_grundy N
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int mexset(const unsigned char *seen, int lim) { int m = 0; while (m < lim && seen[m]) m++; return m; }

int main(int argc, char **argv) {
    int N = argc > 1 ? atoi(argv[1]) : 300;
    int *gA = calloc(N + 2, sizeof(int)), *gB = calloc(N + 3, sizeof(int));
    unsigned char seen[1024];
    for (int n = 0; n <= N; n++) {
        memset(seen, 0, sizeof seen);
        for (int i = 0; i < n; i++) {
            int a = i - 1 > 0 ? i - 1 : 0;
            int b = n - i - 2 > 0 ? n - i - 2 : 0;
            int x = gA[a] ^ gA[b];
            if (x >= 1024) { fprintf(stderr, "overflow\n"); return 1; }
            seen[x] = 1;
        }
        gA[n] = mexset(seen, 1024);
    }
    for (int m = 0; m <= N + 1; m++) {
        memset(seen, 0, sizeof seen);
        for (int j = 0; j + 1 < m; j++) { int x = gB[j] ^ gB[m - j - 2]; seen[x] = 1; }
        gB[m] = mexset(seen, 1024);
    }
    int shift_ok = 1, maxg = 0;
    for (int n = 0; n <= N; n++) { if (gA[n] != gB[n + 1]) shift_ok = 0; if (gA[n] > maxg) maxg = gA[n]; }
    printf("N=%d\n", N);
    printf("gA(0..33):  "); for (int n = 0; n <= 33 && n <= N; n++) printf("%d ", gA[n]); printf("\n");
    printf("gA(52..85): "); for (int n = 52; n <= 85 && n <= N; n++) printf("%d ", gA[n]); printf("\n");
    printf("max gA(n), n<=N: %d\n", maxg);
    printf("gA(n)==gB(n+1) for all n<=N: %s\n", shift_ok ? "yes" : "NO");
    printf("n<=N-34 with gA(n)!=gA(n+34):");
    int last = -1;
    for (int n = 0; n + 34 <= N; n++) if (gA[n] != gA[n + 34]) { printf(" %d", n); last = n; }
    printf("\nlast exception: %d\n", last);
    /* Guy-Smith certificate: g(n+p)=g(n) for n0 <= n < 2 n0 + p + k */
    int n0 = 52, p = 34, k = 3, cert = 1, hi = 2 * n0 + p + k;
    if (hi - 1 + p > N) { printf("certificate range exceeds data\n"); cert = 0; }
    else for (int n = n0; n < hi; n++) if (gA[n] != gA[n + p]) cert = 0;
    printf("Guy-Smith certificate n0=52 p=34 k=3 (check %d<=n<%d, uses g up to %d): %s\n", n0, hi, hi - 1 + p, cert ? "PASS" : "FAIL");
    /* least period on second half */
    for (int q = 1; q <= 34; q++) {
        int ok = 1;
        for (int n = N / 2; n + q <= N; n++) if (gA[n] != gA[n + q]) { ok = 0; break; }
        if (ok) { printf("least period on [N/2,N]: %d\n", q); break; }
    }
    /* g=0 list n<=200 */
    printf("gA(n)=0, n<=200:"); for (int n = 0; n <= 200 && n <= N; n++) if (!gA[n]) printf(" %d", n); printf("\n");
    return 0;
}
