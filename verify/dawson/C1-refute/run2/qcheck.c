/* C1-refute run2: independent verifier for a candidate misere quotient of 0.137 (Dawson's chess)
 * restricted to strips of length <= 32.  Written from scratch; reads only a data file.
 *
 * Input: N; N x N table; N bits P; phi(0..32) (phi(0) must be the identity).
 *
 * Proof obligation checked.  Let Psi(G) = product of phi over the strips of G.  We show, by
 * induction on G, that for EVERY finite sum G of strips of length <= 32,
 *        G is a misere P-position  <=>  Psi(G) in P.                                   (*)
 * Misere: G empty is N (mover has no move and wins); G nonempty is P iff every option is N.
 * Options of a strip n (0.137): n=1 -> empty; n>=2 -> strip n-2; n>=3 -> strips a,b, a+b=n-3.
 * (Strips of length 0 are empty.)
 * Inductive step needs, for every G:  Psi(G) in P  ==  [G nonempty and no option G' has Psi(G') in P].
 * Option G' = G - h_n + o, Psi(G') = Psi(G - h_n) * Psi(o).  Define bad_n(z) = exists option o of
 * strip n with z*Psi(o) in P.  So G has a "P-image" option iff exists n in supp(G) with
 * bad_n(Psi(G - h_n)).
 *
 * Exhaustion over the infinitely many G: process strip lengths k = 1..32 in order, choosing the
 * multiplicity c_k.  The state after stage k is (x = Psi(G_k), ne = [G_k nonempty], U) where
 *    U = { q in Q : some n<=k in supp(G_k) has bad_n(Psi(G_k - h_n) * q) }.
 * For the final G = G_k + R (R uses strips > k), G has a P-image option among strips <= k iff
 * Psi(R) in U.  Adding c copies of strip k (a = phi(k)):
 *    x' = x a^c,   U' = { q : a^c q in U }  union  (c>=1 ? { q : bad_k(x a^(c-1) q) } : {}).
 * The new state depends on c only through (a^c, a^(c-1), [c>=1]), so with a^(m+p) = a^m it
 * suffices to try c = 0..m+p.  At the end (R empty, Psi(R)=identity e) every G is represented,
 * and the check is   P[x] == (ne && e not in U)   for every final state.
 * Plus: identity unique, table commutative + associative (Psi well defined), phi onto Q
 * (surjective), Q reduced (rows {z : xz in P} pairwise distinct).  Then the misere quotient of
 * the strips <= 32 is isomorphic to (Q,P): order N, P-portion |P|.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define K 32
#define MAXQ 2048
#define WMAX (MAXQ / 64)

static int N, W;
static int *M;
static unsigned char Pb[MAXQ];
static int phi[K + 1];
static int e;
#define MUL(x, y) M[(size_t)(x) * N + (y)]

static unsigned char badk[K + 1][MAXQ];

typedef struct {
    int x, ne, par, c;
    uint64_t U[WMAX];
} St;

static St *stage[K + 1];
static long nst[K + 1];

static inline int getb(const uint64_t *U, int q) { return (U[q >> 6] >> (q & 63)) & 1; }
static inline void setb(uint64_t *U, int q) { U[q >> 6] |= (uint64_t)1 << (q & 63); }

static uint64_t hst(const St *s) {
    uint64_t h = 1469598103934665603ULL ^ (uint64_t)s->x * 1000003u ^ (uint64_t)s->ne;
    for (int i = 0; i < W; i++) { h ^= s->U[i]; h *= 1099511628211ULL; h ^= h >> 29; }
    return h;
}
static int eqst(const St *a, const St *b) {
    return a->x == b->x && a->ne == b->ne && memcmp(a->U, b->U, sizeof(uint64_t) * W) == 0;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: qcheck cert.txt [cap] [skipassoc]\n"); return 2; }
    long cap = argc > 2 ? atol(argv[2]) : 20000000L;
    FILE *f = fopen(argv[1], "r");
    if (!f || fscanf(f, "%d", &N) != 1 || N < 1 || N > MAXQ) { fprintf(stderr, "bad N\n"); return 2; }
    W = (N + 63) / 64;
    M = malloc(sizeof(int) * (size_t)N * N);
    for (long i = 0; i < (long)N * N; i++)
        if (fscanf(f, "%d", &M[i]) != 1 || M[i] < 0 || M[i] >= N) { fprintf(stderr, "bad table\n"); return 2; }
    int np = 0;
    for (int i = 0; i < N; i++) { int b; if (fscanf(f, "%d", &b) != 1) return 2; Pb[i] = b != 0; np += Pb[i]; }
    for (int n = 0; n <= K; n++) if (fscanf(f, "%d", &phi[n]) != 1 || phi[n] < 0 || phi[n] >= N) { fprintf(stderr, "bad phi\n"); return 2; }
    fclose(f);
    int fail = 0;

    /* identity */
    int nid = 0; e = -1;
    for (int x = 0; x < N; x++) {
        int ok = 1;
        for (int y = 0; y < N && ok; y++) if (MUL(x, y) != y || MUL(y, x) != y) ok = 0;
        if (ok) { nid++; e = x; }
    }
    printf("N=%d |P|=%d identities=%d (e=%d) phi(0)=%d\n", N, np, nid, e, phi[0]);
    if (nid != 1 || phi[0] != e) { printf("FAIL identity\n"); fail = 1; }
    /* commutative, associative */
    long bad = 0;
    for (int x = 0; x < N; x++) for (int y = 0; y < N; y++) if (MUL(x, y) != MUL(y, x)) bad++;
    printf("commutativity violations: %ld\n", bad); if (bad) fail = 1;
    bad = 0;
    if (!(argc > 3 && atoi(argv[3]) == 1))  /* argv[3]==1: skip (table unchanged in P/phi mutants) */
    for (int x = 0; x < N; x++) for (int y = 0; y < N; y++) { int xy = MUL(x, y);
        for (int z = 0; z < N; z++) if (MUL(xy, z) != MUL(x, MUL(y, z))) bad++; }
    printf("associativity violations over %ld triples: %ld\n", (long)N * N * N, bad); if (bad) fail = 1;
    /* surjectivity: closure of {e} under right multiplication by phi(1..32) */
    {
        unsigned char *seen = calloc(N, 1); int *q = malloc(sizeof(int) * N); int h = 0, t = 0;
        seen[e] = 1; q[t++] = e;
        while (h < t) { int x = q[h++]; for (int n = 1; n <= K; n++) { int y = MUL(x, phi[n]); if (!seen[y]) { seen[y] = 1; q[t++] = y; } } }
        int npr = 0; for (int i = 0; i < N; i++) if (seen[i] && Pb[i]) npr++;
        printf("reachable elements: %d of %d (P among reachable: %d)\n", t, N, npr);
        if (t != N) fail = 1;
        free(seen); free(q);
    }
    if (Pb[e]) { printf("FAIL: identity in P (empty position is a misere N-position)\n"); fail = 1; }
    /* reduced */
    {
        uint64_t *rows = calloc((size_t)N * W, 8);
        for (int x = 0; x < N; x++) for (int z = 0; z < N; z++) if (Pb[MUL(x, z)]) setb(rows + (size_t)x * W, z);
        long dup = 0;
        for (int x = 0; x < N; x++) for (int y = x + 1; y < N; y++)
            if (memcmp(rows + (size_t)x * W, rows + (size_t)y * W, 8 * W) == 0) dup++;
        printf("indistinguishable pairs of distinct elements: %ld (reduced iff 0)\n", dup);
        if (dup) fail = 1;
        free(rows);
    }
    /* options and bad_k */
    for (int k = 1; k <= K; k++) {
        int o[64], no = 0;
        if (k == 1) o[no++] = e;
        if (k >= 2) o[no++] = phi[k - 2];
        if (k >= 3) for (int a = 0; a <= k - 3; a++) o[no++] = MUL(phi[a], phi[k - 3 - a]);
        for (int z = 0; z < N; z++) { int b = 0; for (int i = 0; i < no && !b; i++) if (Pb[MUL(z, o[i])]) b = 1; badk[k][z] = b; }
    }
    /* stage DP */
    stage[0] = calloc(1, sizeof(St)); nst[0] = 1;
    stage[0][0].x = e; stage[0][0].ne = 0; stage[0][0].par = -1; stage[0][0].c = 0;
    long total = 1;
    uint64_t *L = calloc((size_t)N * W, 8);   /* L[y] = { q : bad_k(y q) } */
    for (int k = 1; k <= K; k++) {
        int a = phi[k], pw[64], m = -1, p = -1, j;
        pw[0] = e;
        for (j = 1; j < 64; j++) {
            pw[j] = MUL(pw[j - 1], a);
            for (int i = 0; i < j; i++) if (pw[i] == pw[j]) { m = i; p = j - i; break; }
            if (m >= 0) break;
        }
        if (m < 0) { printf("index/period too large\n"); return 2; }
        int cmax = m + p;
        memset(L, 0, (size_t)N * W * 8);
        for (int y = 0; y < N; y++) for (int q = 0; q < N; q++) if (badk[k][MUL(y, q)]) setb(L + (size_t)y * W, q);
        long hcap = 1; while (hcap < 4 * (nst[k - 1] * (cmax + 1) + 16)) hcap <<= 1;
        long *ht = malloc(sizeof(long) * hcap); for (long i = 0; i < hcap; i++) ht[i] = -1;
        long alloc = nst[k - 1] * 2 + 16, n = 0;
        St *nx = malloc(sizeof(St) * alloc);
        St t;
        for (long i = 0; i < nst[k - 1]; i++) {
            St *s = &stage[k - 1][i];
            for (int c = 0; c <= cmax; c++) {
                memset(&t, 0, sizeof t);
                t.par = (int)i; t.c = c;
                if (c == 0) { t.x = s->x; t.ne = s->ne; memcpy(t.U, s->U, 8 * W); }
                else {
                    t.x = MUL(s->x, pw[c]); t.ne = 1;
                    int y = MUL(s->x, pw[c - 1]);
                    for (int q = 0; q < N; q++) if (getb(s->U, MUL(pw[c], q))) setb(t.U, q);
                    for (int w = 0; w < W; w++) t.U[w] |= L[(size_t)y * W + w];
                }
                uint64_t h = hst(&t) & (hcap - 1);
                while (ht[h] >= 0 && !eqst(&nx[ht[h]], &t)) h = (h + 1) & (hcap - 1);
                if (ht[h] < 0) {
                    if (n == alloc) { alloc *= 2; nx = realloc(nx, sizeof(St) * alloc); }
                    nx[n] = t; ht[h] = n; n++;
                    if (n > cap) { printf("state cap exceeded at k=%d\n", k); return 3; }
                    if (4 * n > hcap) { /* rehash */
                        long nh = hcap * 2; long *h2 = malloc(sizeof(long) * nh); for (long r = 0; r < nh; r++) h2[r] = -1;
                        for (long r = 0; r < n; r++) { uint64_t g = hst(&nx[r]) & (nh - 1); while (h2[g] >= 0) g = (g + 1) & (nh - 1); h2[g] = r; }
                        free(ht); ht = h2; hcap = nh;
                    }
                }
            }
        }
        free(ht);
        stage[k] = nx; nst[k] = n; total += n;
        printf("stage k=%2d phi=%3d index m=%d period p=%d: %ld states\n", k, a, m, p, n);
        fflush(stdout);
    }
    /* final check */
    long nbad = 0, nP = 0, nN = 0; int shown = 0;
    for (long i = 0; i < nst[K]; i++) {
        St *s = &stage[K][i];
        int predP = s->ne && !getb(s->U, e);
        if (Pb[s->x]) nP++; else nN++;
        if (predP != Pb[s->x]) {
            nbad++;
            if (shown < 5) {
                shown++;
                int mult[K + 1]; long idx = i;
                for (int k = K; k >= 1; k--) { mult[k] = stage[k][idx].c; idx = stage[k][idx].par; }
                printf("  FAILURE: Psi=%d P[Psi]=%d but recursion says %s; position (strip:mult):", s->x, Pb[s->x], predP ? "P" : "N");
                for (int k = 1; k <= K; k++) if (mult[k]) printf(" %d:%d", k, mult[k]);
                printf("\n");
            }
        }
    }
    printf("final states: %ld (P-labelled %ld, N-labelled %ld); total states over stages %ld\n", nst[K], nP, nN, total);
    printf("recursion check failures: %ld\n", nbad);
    if (nbad) fail = 1;
    printf(fail ? "RESULT: FAIL\n" : "RESULT: PASS -> misere quotient of 0.137 strips <= 32 has order %d, P-portion %d\n", N, np);
    return fail;
}
