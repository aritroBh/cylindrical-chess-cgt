/* K32 referee, own implementation V (written without reading stopsA.c / stopsB.c beyond their headers).
 * Graphs: n <= 6 nodes, node i has Left options Lm[i], Right options Rm[i] (bit masks); a mover without option loses.
 * Modes:
 *   vref all N K          every labelled graph on N nodes that is a stopper; every node evaluated; plus the rooted classes
 *                         (root = node 0, all nodes reachable, canonical = minimum over permutations of 1..N-1)
 *   vref rand N K count seed pct   random labelled stoppers (edge probability pct/100 per ordered pair and side)
 * Per node: lam, rho (least C >= 0 with Left wins y + C second / Right wins y - C second), LS, RS by Siegel's recursion with the
 * number clause (y equals a number x iff Left AND Right win y - x second, x on the grid 1/2^K), and the check of the stops
 * against the grid (D2): x < RS => Left wins y - x second, x > RS => Left does not; x < LS => Left wins y - x first, x > LS => not.
 * Sums are solved by a plain fixed-point iteration to the least fixed points (Left wins, Right wins). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXN 6
#define MAXG 1100
#define BIG 1000000
typedef struct { int n; int Lm[MAXN], Rm[MAXN]; } G;
static int K, M, ONE, GN, OFF;           /* grid: index p+OFF stands for the number p/ONE, |p/ONE| <= M */
static int NL[MAXG], NR[MAXG];           /* the single canonical option of a number node, or -1 */
static void build(int k, int m) {
  K = k; ONE = 1 << k; M = m; GN = 2 * M * ONE + 1; OFF = M * ONE;
  for (int i = 0; i < GN; i++) { int p = i - OFF; NL[i] = NR[i] = -1; if (p == 0) continue;
    if (p % ONE == 0) { if (p > 0) NL[i] = i - ONE; else NR[i] = i + ONE; continue; }
    int a = abs(p), t = 0; while (!(a & 1)) { a >>= 1; t++; }
    NL[i] = i - (1 << t); NR[i] = i + (1 << t); }
}
static uint8_t WL[MAXN][MAXG][2], WR[MAXN][MAXG][2];   /* [y][x][mover], mover 0 = Left to move */
static int stopper(const G *g) {            /* acyclic (node,mover) graph, by repeated removal of sinks */
  int alive[2 * MAXN], na = 2 * g->n, ch = 1;
  for (int s = 0; s < na; s++) alive[s] = 1;
  while (ch && na) { ch = 0;
    for (int s = 0; s < 2 * g->n; s++) if (alive[s]) { int i = s >> 1, m = s & 1, o = m ? g->Rm[i] : g->Lm[i], h = 0;
      for (int j = 0; j < g->n; j++) if ((o >> j & 1) && alive[2 * j + (1 - m)]) h = 1;
      if (!h) { alive[s] = 0; na--; ch = 1; } } }
  return na == 0;
}
static int solve(const G *g) {              /* returns 0 ok, 1 if some state is neither or both */
  int n = g->n;
  for (int side = 0; side < 2; side++) { uint8_t (*W)[MAXG][2] = side ? WR : WL;
    memset(W, 0, sizeof(uint8_t) * MAXN * MAXG * 2);
    int ch = 1;
    while (ch) { ch = 0;
      for (int i = 0; i < n; i++) for (int x = 0; x < GN; x++) for (int m = 0; m < 2; m++) { if (W[i][x][m]) continue;
        int v; /* does 'side' win with mover m at (i,x)? */
        int sideIsMover = (side == m);  /* side 0 = Left, mover 0 = Left */
        if (sideIsMover) { v = 0;
          if (m == 0) { for (int j = 0; j < n; j++) if (g->Lm[i] >> j & 1) v |= W[j][x][1]; if (NL[x] >= 0) v |= W[i][NL[x]][1]; }
          else        { for (int j = 0; j < n; j++) if (g->Rm[i] >> j & 1) v |= W[j][x][0]; if (NR[x] >= 0) v |= W[i][NR[x]][0]; } }
        else { v = 1;
          if (m == 0) { for (int j = 0; j < n; j++) if (g->Lm[i] >> j & 1) v &= W[j][x][1]; if (NL[x] >= 0) v &= W[i][NL[x]][1]; }
          else        { for (int j = 0; j < n; j++) if (g->Rm[i] >> j & 1) v &= W[j][x][0]; if (NR[x] >= 0) v &= W[i][NR[x]][0]; } }
        if (v) { W[i][x][m] = 1; ch = 1; } } } }
  for (int i = 0; i < n; i++) for (int x = 0; x < GN; x++) for (int m = 0; m < 2; m++) if (WL[i][x][m] + WR[i][x][m] != 1) return 1;
  return 0;
}
static int numnode[MAXN], isnum[MAXN];
/* Siegel's recursion with the number clause; S[i][0] = LS(i), S[i][1] = RS(i) in units of 1/ONE; BIG = +inf */
static int S[MAXN][2], done[MAXN][2];
static int stop(const G *g, int i, int m) {
  if (done[i][m]) return S[i][m];
  int r;
  if (isnum[i]) r = numnode[i];
  else if (m == 0) { r = -BIG; for (int j = 0; j < g->n; j++) if (g->Lm[i] >> j & 1) { int t = stop(g, j, 1); if (t > r) r = t; } }
  else { r = BIG; for (int j = 0; j < g->n; j++) if (g->Rm[i] >> j & 1) { int t = stop(g, j, 0); if (t < r) r = t; } }
  done[i][m] = 1; S[i][m] = r; return r;
}
typedef struct { long nodes, litL, litR, corrL, corrR, infpair, d12bad, ambig, nosolve, litOut, litIn; } T;
static long hist[3][64]; /* unused */
/* evaluate all nodes of g; update tally t; if root >= 0 also update rt (rooted tally) with that node; if pr print per node */
static void evalg(const G *g, T *t, T *rt, int root, int pr) {
  int n = g->n;
  if (solve(g)) { t->nosolve++; return; }
  memset(done, 0, sizeof done);
  for (int i = 0; i < n; i++) { isnum[i] = 0; int cnt = 0;
    for (int x = 0; x < GN; x++) { int q = GN - 1 - x;           /* index of -x */
      if (WL[i][q][1] && WR[i][q][0]) { isnum[i] = 1; numnode[i] = x - OFF; cnt++; } }
    if (cnt > 1) t->ambig++; }
  for (int i = 0; i < n; i++) {
    int LS = stop(g, i, 0), RS = stop(g, i, 1);
    /* D2 check on the grid */
    for (int x = 0; x < GN; x++) { int p = x - OFF, q = GN - 1 - x;
      int leftSecond = WL[i][q][1], leftFirst = WL[i][q][0];
      if (p < RS && !leftSecond) t->d12bad++;
      if (p > RS && leftSecond) t->d12bad++;
      if (p < LS && !leftFirst) t->d12bad++;
      if (p > LS && leftFirst) t->d12bad++; }
    int lam = -1, rho = -1;
    for (int C = 0; C <= M && lam < 0; C++) if (WL[i][OFF + C * ONE][1]) lam = C;      /* y + C, Right to move, Left wins */
    for (int C = 0; C <= M && rho < 0; C++) if (WR[i][OFF - C * ONE][0]) rho = C;      /* y - C, Left to move, Right wins */
    /* corrected relation */
    T *tt[2] = { t, rt };
    for (int a = 0; a < 2; a++) { T *u = tt[a]; if (!u || (a == 1 && root < 0)) continue; if (a == 1 && i != root) continue;
      u->nodes++;
      /* lambda vs RS */
      int okc = 1, okl = 1;
      if (lam < 0) { if (RS != -BIG) okc = 0; }
      else if (RS == -BIG) okc = 0;
      else if (RS == BIG) { if (lam != 0) okc = 0; }
      else { int uu = -RS;                                            /* u in units of 1/ONE */
        int cl = uu >= 0 ? (uu + ONE - 1) / ONE : -((-uu) / ONE);      /* ceil(u) */
        int fl = uu >= 0 ? uu / ONE : -((-uu + ONE - 1) / ONE);        /* floor(u) */
        int lo = cl > 0 ? cl : 0, hi = fl + 1 > 0 ? fl + 1 : 0;
        if (lam < lo || lam > hi) okc = 0;
        /* literal: lam == ceil(u) or ceil(u)+1 */
        if (!(lam == cl || lam == cl + 1)) okl = 0;
        if (!okl && RS < 2 * ONE) u->litOut++; if (okl && RS >= 2 * ONE) u->litIn++; }
      if (!okc) u->corrL++; if (!okl) u->litL++;
      int okc2 = 1, okl2 = 1;
      if (rho < 0) { if (LS != BIG) okc2 = 0; }
      else if (LS == BIG) okc2 = 0;
      else if (LS == -BIG) { if (rho != 0) okc2 = 0; }
      else { int uu = LS;
        int cl = uu >= 0 ? (uu + ONE - 1) / ONE : -((-uu) / ONE);
        int fl = uu >= 0 ? uu / ONE : -((-uu + ONE - 1) / ONE);
        int lo = cl > 0 ? cl : 0, hi = fl + 1 > 0 ? fl + 1 : 0;
        if (rho < lo || rho > hi) okc2 = 0;
        if (!(rho == cl || rho == cl + 1)) okl2 = 0;
        if (!okl2 && LS > -2 * ONE) u->litOut++; if (okl2 && LS <= -2 * ONE) u->litIn++; }
      if (!okc2) u->corrR++; if (!okl2) u->litR++;
      if ((lam < 0) != (RS == -BIG)) u->infpair++; if ((rho < 0) != (LS == BIG)) u->infpair++;
    }
    if (pr) { printf("%d", i); printf(" lam=%d rho=%d LS=", lam, rho); if (LS == BIG) printf("+inf"); else if (LS == -BIG) printf("-inf"); else printf("%d/%d", LS, ONE);
      printf(" RS="); if (RS == BIG) printf("+inf"); else if (RS == -BIG) printf("-inf"); else printf("%d/%d", RS, ONE); printf("\n"); }
    if (rt && root == i) { /* signature tally */
      extern void sig(int, int, int, int);
      sig(lam, rho, LS, RS); }
  }
}
/* signature table of rooted classes */
static struct { int lam, rho, LS, RS; long c; } sg[400]; static int nsg = 0;
void sig(int lam, int rho, int LS, int RS) {
  for (int i = 0; i < nsg; i++) if (sg[i].lam == lam && sg[i].rho == rho && sg[i].LS == LS && sg[i].RS == RS) { sg[i].c++; return; }
  sg[nsg].lam = lam; sg[nsg].rho = rho; sg[nsg].LS = LS; sg[nsg].RS = RS; sg[nsg].c = 1; nsg++;
}
static int cmpsg(const void *a, const void *b) { const typeof(sg[0]) *x = a, *y = b;
  if (x->lam != y->lam) return (x->lam < 0 ? 99 : x->lam) - (y->lam < 0 ? 99 : y->lam);
  if (x->rho != y->rho) return (x->rho < 0 ? 99 : x->rho) - (y->rho < 0 ? 99 : y->rho);
  if (x->LS != y->LS) return x->LS < y->LS ? -1 : 1; if (x->RS != y->RS) return x->RS < y->RS ? -1 : 1; return 0; }
static void printsig(void) { qsort(sg, nsg, sizeof sg[0], cmpsg);
  for (int i = 0; i < nsg; i++) { printf("lam=%d rho=%d LS=", sg[i].lam, sg[i].rho);
    if (sg[i].LS == BIG) printf("+inf"); else if (sg[i].LS == -BIG) printf("-inf"); else printf("%d/%d", sg[i].LS, ONE);
    printf(" RS="); if (sg[i].RS == BIG) printf("+inf"); else if (sg[i].RS == -BIG) printf("-inf"); else printf("%d/%d", sg[i].RS, ONE);
    printf(" count=%ld\n", sg[i].c); } }
static void printT(const char *name, const T *t) {
  printf("%s: nodes %ld  corrected-viol lam %ld rho %ld  literal-viol lam %ld rho %ld  infinity-pair-viol %ld  D2-grid-viol %ld  ambiguous-number %ld  unsolved %ld  literal-fails-outside-RS>=2 %ld  literal-holds-inside %ld\n",
         name, t->nodes, t->corrL, t->corrR, t->litL, t->litR, t->infpair, t->d12bad, t->ambig, t->nosolve, t->litOut, t->litIn); }
static int reach_all(const G *g, int r) { int seen = 1 << r, ch = 1;
  while (ch) { ch = 0; for (int i = 0; i < g->n; i++) if (seen >> i & 1) { int o = g->Lm[i] | g->Rm[i]; if ((seen | o) != seen) { seen |= o; ch = 1; } } }
  return seen == (1 << g->n) - 1; }
static uint64_t enc(const G *g) { uint64_t v = 0; for (int i = 0; i < g->n; i++) v = (v << 12) | ((uint64_t)g->Lm[i] << 6) | g->Rm[i]; return v; }
static int PERM3[2][3] = {{0,1,2},{0,2,1}};
static int PERM4[6][4] = {{0,1,2,3},{0,1,3,2},{0,2,1,3},{0,2,3,1},{0,3,1,2},{0,3,2,1}};
static int permute_min(const G *g, int *isMin) {   /* is g minimal under all permutations of nodes 1..n-1 ? n <= 4 */
  int n = g->n; uint64_t me = enc(g); *isMin = 1;
  int np = n <= 2 ? 1 : (n == 3 ? 2 : 6);
  for (int p = 0; p < np; p++) { int idx[4]; for (int a = 0; a < n; a++) idx[a] = n == 3 ? PERM3[p][a] : (n == 4 ? PERM4[p][a] : a);
    G h; h.n = n; for (int a = 0; a < n; a++) { h.Lm[a] = 0; h.Rm[a] = 0; }
    for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) { if (g->Lm[a] >> b & 1) h.Lm[idx[a]] |= 1 << idx[b]; if (g->Rm[a] >> b & 1) h.Rm[idx[a]] |= 1 << idx[b]; }
    if (enc(&h) < me) { *isMin = 0; return 0; } }
  return 0;
}

static uint8_t REACH[65536];
static int stopper_bits(int L, int R) {   /* 4 nodes; row i of L is bits 4i..4i+3 */
  int AL = 15, AR = 15;
  for (;;) { int nAL = 0, nAR = 0;
    for (int i = 0; i < 4; i++) { if ((AL >> i & 1) && (((L >> (4 * i)) & 15) & AR)) nAL |= 1 << i;
                                  if ((AR >> i & 1) && (((R >> (4 * i)) & 15) & AL)) nAR |= 1 << i; }
    if (nAL == AL && nAR == AR) break; AL = nAL; AR = nAR; if (!AL && !AR) break; }
  return !AL && !AR;
}
static int enum4(long lo, long hi) {
  for (int U = 0; U < 65536; U++) { int seen = 1, ch = 1; while (ch) { ch = 0; for (int i = 0; i < 4; i++) if (seen >> i & 1) { int o = (U >> (4 * i)) & 15; if ((seen | o) != seen) { seen |= o; ch = 1; } } } REACH[U] = (seen == 15); }
  T all, root; memset(&all, 0, sizeof all); memset(&root, 0, sizeof root);
  long nlab = 0, ncl = 0;
  for (long L = lo; L < hi; L++) for (int R = 0; R < 65536; R++) {
    if (!REACH[L | R]) continue;
    if (!stopper_bits((int)L, R)) continue;
    nlab++;
    G g; g.n = 4; for (int i = 0; i < 4; i++) { g.Lm[i] = (L >> (4 * i)) & 15; g.Rm[i] = (R >> (4 * i)) & 15; }
    int isMin; permute_min(&g, &isMin); if (!isMin) continue;
    ncl++; evalg(&g, &all, &root, 0, 0); }
  printf("ENUM4 lo %ld hi %ld K %d labelled-rooted-stoppers %ld canonical-classes %ld\n", lo, hi, K, nlab, ncl);
  printT("all nodes of the classes", &all); printT("root only", &root);
  for (int i = 0; i < nsg; i++) printf("SIG %d %d %d %d %ld\n", sg[i].lam, sg[i].rho, sg[i].LS, sg[i].RS, sg[i].c);
  return 0;
}
int main(int argc, char **argv) {
  if (argc >= 5 && !strcmp(argv[1], "enum4")) { build(atoi(argv[4]), 6); return enum4(atol(argv[2]), atol(argv[3])); }
  if (argc < 4) return 1;
  int N = atoi(argv[2]), k = atoi(argv[3]);
  build(k, N + 2);
  T all, root; memset(&all, 0, sizeof all); memset(&root, 0, sizeof root);
  if (!strcmp(argv[1], "all")) {
    long total = 1L << (2 * N * N), nst = 0, nclass = 0;
    for (long code = 0; code < total; code++) { G g; g.n = N; long c = code;
      for (int i = 0; i < N; i++) { g.Lm[i] = c & ((1 << N) - 1); c >>= N; g.Rm[i] = c & ((1 << N) - 1); c >>= N; }
      if (!stopper(&g)) continue; nst++;
      int isroot = reach_all(&g, 0), isMin = 0;
      if (isroot) permute_min(&g, &isMin);
      if (!isroot || !isMin) { evalg(&g, &all, NULL, -1, 0); }
      else { nclass++; evalg(&g, &all, &root, 0, 0); } }
    printf("N=%d K=%d labelled stoppers %ld, rooted classes (root 0, all reachable) %ld\n", N, K, nst, nclass);
    printT("all labelled graphs, all nodes", &all); printT("rooted classes, root only", &root); printsig();
  } else {
    long count = atol(argv[4]); unsigned seed = atoi(argv[5]); int pct = atoi(argv[6]); srand(seed);
    long made = 0; int pr = argc > 7;
    while (made < count) { G g; g.n = N;
      for (int i = 0; i < N; i++) { g.Lm[i] = g.Rm[i] = 0; for (int j = 0; j < N; j++) { if (rand() % 100 < pct) g.Lm[i] |= 1 << j; if (rand() % 100 < pct) g.Rm[i] |= 1 << j; } }
      if (!stopper(&g)) continue; made++;
      if (pr) { printf("G %d", N); for (int i = 0; i < N; i++) printf(" %d %d", g.Lm[i], g.Rm[i]); printf("\n"); }
      evalg(&g, &all, NULL, -1, pr); }
    printT("random labelled stoppers, all nodes", &all); }
  return 0;
}
