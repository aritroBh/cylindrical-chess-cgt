/* K32 implementation A (C).  Terminal-free finite games as graphs: node i has Left options L[i] and Right options R[i]
 * (bit masks, n <= 8).  A node with no option of the mover loses (normal play).  Only stoppers are evaluated.
 *   enum n          exhaustive: every rooted stopper graph on exactly n nodes (all reachable from node 0), one per
 *                   isomorphism class; every node of every graph is evaluated
 *   dump n          print those graphs ("n L0 R0 L1 R1 ...", masks in decimal), no evaluation
 *   gen n count seed pct   print random stopper graphs (edge probability pct/100)
 *   eval            read graph lines from stdin and evaluate
 * Per node: lam, rho (reserves, by a token DP), LS, RS (Siegel's recursion D1 with the number clause; and D2: sup of the
 * dyadic x with Left winning g-x first / second), scaled by 2^KB.  Tally printed at the end (the same text in stopsB.c). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define KB 4
#define ONE (1<<KB)
#define INF 1000000000
#define NINF (-1000000000)
#define CINF 99
typedef struct { int n; uint8_t L[8], R[8]; } Gr;

/* ---------- stopper test and topological order of the (node,mover) states: s = 2*i+m, m=0 Left to move ---------- */
static int topo(const Gr *g, int *ord) {
  int n = g->n, alive[16], na = 2 * n, cnt = 0;
  for (int s = 0; s < 2 * n; s++) alive[s] = 1;
  int ch = 1;
  while (ch && na) { ch = 0;
    for (int s = 0; s < 2 * n; s++) if (alive[s]) {
      int i = s >> 1, m = s & 1; uint8_t o = m ? g->R[i] : g->L[i]; int has = 0;
      for (int j = 0; j < n; j++) if ((o >> j & 1) && alive[2 * j + (1 - m)]) { has = 1; break; }
      if (!has) { alive[s] = 0; na--; ord[cnt++] = s; ch = 1; } } }
  return na == 0 ? cnt : -1;
}
static int reachcount(const Gr *g, int r) {
  int seen = 1 << r, st[8], sp = 0; st[sp++] = r;
  while (sp) { int x = st[--sp]; int o = g->L[x] | g->R[x];
    for (int j = 0; j < g->n; j++) if ((o >> j & 1) && !(seen >> j & 1)) { seen |= 1 << j; st[sp++] = j; } }
  return __builtin_popcount(seen);
}

/* ---------- number grid ---------- */
static int Mcur = -1, GN, OFF, xL[400], xR[400], xrank[400], xordr[400];
static void setgrid(int M) {
  if (M == Mcur) return; Mcur = M; GN = 2 * M * ONE + 1; OFF = M * ONE;
  for (int i = 0; i < GN; i++) {
    int m = i - OFF; xL[i] = xR[i] = -1;
    if (m == 0) continue;
    if (m % ONE == 0) { if (m > 0) xL[i] = (m - ONE) + OFF; else xR[i] = (m + ONE) + OFF; }
    else { int a = m < 0 ? -m : m, t = 0; while (!(a & 1)) { a >>= 1; t++; } xL[i] = m - (1 << t) + OFF; xR[i] = m + (1 << t) + OFF; }
  }
  /* rank: options first.  integers: |m|/ONE; dyadic: 1+max(rank of options) */
  for (int i = 0; i < GN; i++) xrank[i] = -2;
  int done = 0;
  while (done < GN) for (int i = 0; i < GN; i++) if (xrank[i] == -2) {
    int a = xL[i] < 0 ? -1 : xrank[xL[i]], b = xR[i] < 0 ? -1 : xrank[xR[i]];
    if (a == -2 || b == -2) continue; xrank[i] = 1 + (a > b ? a : b); done++; }
  int c = 0; for (int r = 0; c < GN; r++) for (int i = 0; i < GN; i++) if (xrank[i] == r) xordr[c++] = i;
}

typedef struct { int lam[8], rho[8], LS1[8], RS1[8], LS2[8], RS2[8]; int tokbad, mono_bad, num_bad, big_bad; } Res;

static int ceil_div(int a, int b) { /* ceil(a/b), b>0 */ return a >= 0 ? (a + b - 1) / b : -((-a) / b); }
static int floor_div(int a, int b) { return a >= 0 ? a / b : -((-a + b - 1) / b); }

static int evalA(const Gr *g, Res *r) {
  int ord[16], n = g->n, M = n + 1, Cmax = n + 2;
  if (topo(g, ord) < 0) return -1;
  setgrid(M);
  static uint8_t A[8][400], B[8][400];
  for (int q = 0; q < GN; q++) { int xi = xordr[q];
    for (int k = 0; k < 2 * n; k++) { int s = ord[k], i = s >> 1, m = s & 1;
      if (m) { int v = 1; for (int j = 0; j < n; j++) if (g->R[i] >> j & 1) v &= B[j][xi]; if (xL[xi] >= 0) v &= B[i][xL[xi]]; A[i][xi] = v; }
      else   { int v = 0; for (int j = 0; j < n; j++) if (g->L[i] >> j & 1) v |= A[j][xi]; if (xR[xi] >= 0) v |= A[i][xR[xi]]; B[i][xi] = v; } } }
  /* token DP */
  uint8_t a[8][16], b[8][16], c[8][16], d[8][16];
  for (int C = 0; C <= Cmax; C++) for (int k = 0; k < 2 * n; k++) { int s = ord[k], i = s >> 1, m = s & 1;
    if (m) { int v = 1; for (int j = 0; j < n; j++) if (g->R[i] >> j & 1) v &= b[j][C]; a[i][C] = v;
             int w = (C >= 1) ? c[i][C - 1] : 0; for (int j = 0; j < n; j++) if (g->R[i] >> j & 1) w |= c[j][C]; d[i][C] = w; }
    else   { int v = (C >= 1) ? a[i][C - 1] : 0; for (int j = 0; j < n; j++) if (g->L[i] >> j & 1) v |= a[j][C]; b[i][C] = v;
             int w = 1; for (int j = 0; j < n; j++) if (g->L[i] >> j & 1) w &= d[j][C]; c[i][C] = w; } }
  /* NB: c[i][C] = Right wins i - C with Left to move; d[i][C] = Right wins with Right to move (Right tokens C) */
  r->tokbad = r->mono_bad = r->num_bad = r->big_bad = 0;
  for (int i = 0; i < n; i++) {
    int lam = CINF, rho = CINF;
    for (int C = 0; C <= Cmax; C++) if (a[i][C]) { lam = C; break; }
    for (int C = 0; C <= Cmax; C++) if (c[i][C]) { rho = C; break; }
    r->lam[i] = lam; r->rho[i] = rho;
    /* self check: lam from the profile, A(g,-C); rho from the profile: B(g,C) false */
    int l2 = CINF, r2 = CINF;
    for (int C = 0; C <= Cmax && C <= M; C++) if (A[i][OFF - C * ONE]) { l2 = C; break; }
    for (int C = 0; C <= Cmax && C <= M; C++) if (!B[i][OFF + C * ONE]) { r2 = C; break; }
    if (Cmax > M) { if (l2 == CINF && lam <= Cmax) l2 = lam > M ? lam : l2; if (r2 == CINF && rho <= Cmax) r2 = rho > M ? rho : r2; }
    if (l2 != lam || r2 != rho) r->tokbad++;
    /* monotonicity of A and B in x */
    for (int xi = 1; xi < GN; xi++) { if (A[i][xi] && !A[i][xi - 1]) r->mono_bad++; if (B[i][xi] && !B[i][xi - 1]) r->mono_bad++; }
    /* D2 */
    int top = GN - 1;
    for (int pass = 0; pass < 2; pass++) { uint8_t *P = pass ? B[i] : A[i]; int val;
      if (P[top]) val = INF; else if (!P[0]) val = NINF;
      else { int xm = 0; for (int xi = 0; xi < GN; xi++) if (P[xi]) xm = xi; int m = xm - OFF;
             val = (m % 2 == 0) ? m : m + 1; }
      if (pass) r->LS2[i] = val; else r->RS2[i] = val; }
  }
  /* D1: number clause then recursion in the topological order */
  int eq[8], eqv[8];
  for (int i = 0; i < n; i++) { eq[i] = 0; eqv[i] = 0; int cnt = 0;
    for (int xi = 0; xi < GN; xi++) if (A[i][xi] && !B[i][xi]) { eq[i] = 1; eqv[i] = xi - OFF; cnt++; }
    if (cnt > 1) r->num_bad++; }
  int LS[8], RS[8];
  for (int k = 0; k < 2 * n; k++) { int s = ord[k], i = s >> 1, m = s & 1;
    if (m == 0) { if (eq[i]) LS[i] = eqv[i]; else { int v = NINF; for (int j = 0; j < n; j++) if (g->L[i] >> j & 1) if (RS[j] > v) v = RS[j]; LS[i] = v; } }
    else        { if (eq[i]) RS[i] = eqv[i]; else { int v = INF;  for (int j = 0; j < n; j++) if (g->R[i] >> j & 1) if (LS[j] < v) v = LS[j]; RS[i] = v; } } }
  for (int i = 0; i < n; i++) { r->LS1[i] = LS[i]; r->RS1[i] = RS[i];
    if ((LS[i] != INF && LS[i] != NINF && (LS[i] >= (n * ONE) || LS[i] <= -(n * ONE))) || (RS[i] != INF && RS[i] != NINF && (RS[i] >= n * ONE || RS[i] <= -(n * ONE)))) r->big_bad++; }
  return 0;
}

/* ---------- tally (identical text in stopsB.c) ---------- */
typedef struct { long cnt; int lam, rho, LS, RS; } Sig;
static Sig *sigs; static long nsig = 0, capsig = 0;
static long NG = 0, NN = 0, d1d2 = 0, tokbad = 0, monobad = 0, numbad = 0, bigbad = 0;
static long lit_viol[2] = {0, 0}, fix_viol[2] = {0, 0}, inf_viol[2] = {0, 0};
static long dh[2][6];   /* [0]: lam vs RS, [1]: rho vs LS ; index: 0=d0 integer boundary(-RS int>=0) base, 1=d1 boundary, 2=d0 nonint, 3=d1 nonint (impossible), 4=0 (RS>0) , 5=other */
static uint64_t hsh = 1469598103934665603ULL;
static int bestsz[4] = {99, 99, 99, 99}; static char bestg[4][200];
static void hmix(long v) { hsh ^= (uint64_t)v; hsh *= 1099511628211ULL; }
static void addsig(int lam, int rho, int LS, int RS) {
  for (long i = 0; i < nsig; i++) if (sigs[i].lam == lam && sigs[i].rho == rho && sigs[i].LS == LS && sigs[i].RS == RS) { sigs[i].cnt++; return; }
  if (nsig == capsig) { capsig = capsig ? 2 * capsig : 256; sigs = realloc(sigs, capsig * sizeof(Sig)); }
  sigs[nsig++] = (Sig){1, lam, rho, LS, RS};
}
static void gstr(const Gr *g, int root, char *buf) {
  /* reachable subgraph, renumbered in index order */
  int seen = 1 << root, st[8], sp = 0; st[sp++] = root;
  while (sp) { int x = st[--sp]; int o = g->L[x] | g->R[x]; for (int j = 0; j < g->n; j++) if ((o >> j & 1) && !(seen >> j & 1)) { seen |= 1 << j; st[sp++] = j; } }
  int mp[8], c = 0; mp[root] = c++; for (int j = 0; j < g->n; j++) if ((seen >> j & 1) && j != root) mp[j] = c++;
  char *p = buf; p += sprintf(p, "root=0");
  int inv[8]; for (int j = 0; j < g->n; j++) if (seen >> j & 1) inv[mp[j]] = j;
  for (int k = 0; k < c; k++) { int j = inv[k]; p += sprintf(p, " %d:{", k); int f = 1;
    for (int q = 0; q < g->n; q++) if (g->L[j] >> q & 1) { p += sprintf(p, f ? "%d" : ",%d", mp[q]); f = 0; }
    p += sprintf(p, "|"); f = 1;
    for (int q = 0; q < g->n; q++) if (g->R[j] >> q & 1) { p += sprintf(p, f ? "%d" : ",%d", mp[q]); f = 0; } p += sprintf(p, "}"); }
}
static void tally(const Gr *g, const Res *r) {
  NG++; tokbad += r->tokbad; monobad += r->mono_bad; numbad += r->num_bad; bigbad += r->big_bad;
  static int rootonly = -1; if (rootonly < 0) rootonly = getenv("K32_ROOT") != NULL;
  for (int i = 0; i < (rootonly ? 1 : g->n); i++) {
    NN++;
    int lam = r->lam[i], rho = r->rho[i], LS = r->LS1[i], RS = r->RS1[i];
    if (LS != r->LS2[i] || RS != r->RS2[i]) d1d2++;
    hmix(lam); hmix(rho); hmix(LS); hmix(RS);
    addsig(lam, rho, LS, RS);
    for (int w = 0; w < 2; w++) {
      /* w=0: lam vs RS.  w=1: rho vs LS (mirror: use -LS) */
      int res = w ? rho : lam; int st = w ? LS : RS; int mst = w ? st : -st; /* mst = "-RS" resp. "LS" */
      int bad_lit = 0, bad_fix = 0;
      int stinf = (st == INF || st == NINF);
      /* the bad infinite pairing: reserve infinite iff the relevant stop is the extreme on the wrong side.  w=0: RS=-inf <=> lam=inf ; w=1: LS=+inf <=> rho=inf */
      int extreme = w ? (st == INF) : (st == NINF);
      if (extreme != (res == CINF)) inf_viol[w]++;
      if (!stinf && res != CINF) {
        int lo = ceil_div(w ? st : -st, ONE), hi = floor_div(w ? st : -st, ONE) + 1;
        if (!(res == lo || res == lo + 1)) { bad_lit = 1; lit_viol[w]++; }
        int lo2 = lo > 0 ? lo : 0, hi2 = hi > 0 ? hi : 0;
        if (res < lo2 || res > hi2) { bad_fix = 1; fix_viol[w]++; }
        int isint = (mst % ONE == 0);
        if (mst > 0 && isint) dh[w][res == lo ? 0 : (res == lo + 1 ? 1 : 5)]++;
        else if (mst == 0) dh[w][res == 0 ? 0 : (res == 1 ? 1 : 5)]++;
        else if (mst < 0) dh[w][res == 0 ? 4 : 5]++;
        else dh[w][res == lo ? 2 : 5]++;
      } else if (!stinf && res == CINF) { bad_fix = 1; fix_viol[w]++; bad_lit = 1; lit_viol[w]++; }
      if (stinf && res != CINF && !extreme) { /* stop = +inf for lam (res must be 0) / -inf for rho (res must be 0) */
        if (res != 0) { bad_fix = 1; fix_viol[w]++; } }
      int rc = reachcount(g, i);
      int flags[2] = {bad_lit, bad_fix};
      for (int f = 0; f < 2; f++) if (flags[f] && rc < bestsz[2 * w + f]) { bestsz[2 * w + f] = rc; gstr(g, i, bestg[2 * w + f]); }
    }
  }
}
static int cmpsig(const void *x, const void *y) { const Sig *a = x, *b = y;
  if (a->lam != b->lam) return a->lam - b->lam; if (a->rho != b->rho) return a->rho - b->rho; if (a->LS != b->LS) return a->LS < b->LS ? -1 : 1; if (a->RS != b->RS) return a->RS < b->RS ? -1 : 1; return 0; }
static void fmtstop(char *b, int s) { if (s == INF) strcpy(b, "+inf"); else if (s == NINF) strcpy(b, "-inf"); else sprintf(b, "%d/%d", s, ONE); }
static void report(void) {
  printf("graphs %ld nodes %ld\n", NG, NN);
  printf("D1-D2 mismatches %ld  token-self-check %ld  monotone-violations %ld  number-ambiguous %ld  big-stops %ld\n", d1d2, tokbad, monobad, numbad, bigbad);
  for (int w = 0; w < 2; w++) printf("%s: literal-violations %ld  corrected-violations %ld  infinity-violations %ld\n", w ? "rho/LS" : "lam/RS", lit_viol[w], fix_viol[w], inf_viol[w]);
  for (int w = 0; w < 2; w++) printf("%s boundary(-RS or LS integer>=0, base) %ld  boundary(+1) %ld  nonint(base) %ld  stop-on-wrong-side(0) %ld  other %ld\n", w ? "rho/LS" : "lam/RS", dh[w][0], dh[w][1], dh[w][2], dh[w][4], dh[w][5]);
  qsort(sigs, nsig, sizeof(Sig), cmpsig);
  printf("signatures %ld\n", nsig);
  for (long i = 0; i < nsig; i++) { char a[32], b[32]; fmtstop(a, sigs[i].LS); fmtstop(b, sigs[i].RS);
    char l1[16], r1[16]; if (sigs[i].lam == CINF) strcpy(l1, "inf"); else sprintf(l1, "%d", sigs[i].lam); if (sigs[i].rho == CINF) strcpy(r1, "inf"); else sprintf(r1, "%d", sigs[i].rho);
    printf("lam=%s rho=%s LS=%s RS=%s count=%ld\n", l1, r1, a, b, sigs[i].cnt); }
  printf("hash %016llx\n", (unsigned long long)hsh);
  const char *nm[4] = {"lam/RS literal", "lam/RS corrected", "rho/LS literal", "rho/LS corrected"};
  for (int k = 0; k < 4; k++) if (bestsz[k] < 99) printf("smallest %s violation (reach %d): %s\n", nm[k], bestsz[k], bestg[k]);
}

/* ---------- enumeration ---------- */
static int en; static Gr cur; static long ngraphs = 0; static int dumpmode = 0;
static int is_bfs(const Gr *g) {
  int k = 1;
  for (int i = 0; i < g->n; i++) { if (i >= k) return 0;
    for (int side = 0; side < 2; side++) { uint8_t o = side ? g->R[i] : g->L[i]; uint8_t nw = o >> k;
      if (nw & (nw + 1)) return 0; k += __builtin_popcount(nw); } }
  return k == g->n;
}
static void enc(const Gr *g, uint8_t *e) { for (int i = 0; i < g->n; i++) { e[2 * i] = g->L[i]; e[2 * i + 1] = g->R[i]; } }
static int perms[720][8], nperm;
static void genperms(int n) { int p[8]; for (int i = 0; i < n; i++) p[i] = i; nperm = 0;
  /* all permutations fixing 0 (Heap-free simple recursion) */
  int idx[8]; for (int i = 1; i < n; i++) idx[i] = i;
  int c[8] = {0}; memcpy(perms[nperm++], p, sizeof p);
  int i = 1; /* Heap's algorithm on elements 1..n-1 */
  int m = n - 1; int arr[8]; for (int j = 0; j < m; j++) arr[j] = j + 1; int cc[8] = {0};
  i = 0; while (i < m) { if (cc[i] < i) { if (i % 2 == 0) { int t = arr[0]; arr[0] = arr[i]; arr[i] = t; } else { int t = arr[cc[i]]; arr[cc[i]] = arr[i]; arr[i] = t; }
      int q[8]; q[0] = 0; for (int j = 0; j < m; j++) q[j + 1] = arr[j]; memcpy(perms[nperm++], q, sizeof q); cc[i]++; i = 0; } else { cc[i] = 0; i++; } }
  (void)c; (void)idx;
}
static int is_rep(const Gr *g) {
  uint8_t e0[16], e1[16]; enc(g, e0);
  for (int q = 1; q < nperm; q++) { Gr h; h.n = g->n; int *pm = perms[q];
    for (int i = 0; i < g->n; i++) { uint8_t l = 0, r = 0; for (int j = 0; j < g->n; j++) { if (g->L[i] >> j & 1) l |= 1 << pm[j]; if (g->R[i] >> j & 1) r |= 1 << pm[j]; } h.L[pm[i]] = l; h.R[pm[i]] = r; }
    if (!is_bfs(&h)) continue; enc(&h, e1);
    int c = memcmp(e1, e0, 2 * g->n); if (c < 0) return 0; }
  return 1;
}
static int acyc_partial(int upto) { Gr t; t.n = upto; for (int i = 0; i < upto; i++) { t.L[i] = cur.L[i] & ((1 << upto) - 1); t.R[i] = cur.R[i] & ((1 << upto) - 1); } int o[16]; return topo(&t, o) >= 0; }
static void leaf(void) {
  cur.n = en; if (!is_bfs(&cur) || !is_rep(&cur)) return;
  ngraphs++;
  if (dumpmode) { printf("%d", en); for (int i = 0; i < en; i++) printf(" %d %d", cur.L[i], cur.R[i]); printf("\n"); return; }
  Res r; if (evalA(&cur, &r) < 0) { fprintf(stderr, "internal: non-stopper at leaf\n"); exit(2); } tally(&cur, &r);
}
static void rec(int i, int k) {
  if (i == en) { if (k == en) leaf(); return; }
  if (i >= k) return;
  for (int t = 0; k + t <= en; t++) { uint32_t nm = ((1u << t) - 1) << k; int k1 = k + t;
    for (uint32_t old = 0; old < (1u << k); old++) { cur.L[i] = (uint8_t)(old | nm);
      for (int t2 = 0; k1 + t2 <= en; t2++) { uint32_t nm2 = ((1u << t2) - 1) << k1; int k2 = k1 + t2;
        for (uint32_t old2 = 0; old2 < (1u << k1); old2++) { cur.R[i] = (uint8_t)(old2 | nm2);
          if (!acyc_partial(i + 1)) continue; rec(i + 1, k2); } } } }
}
static uint64_t rs = 88172645463325252ULL; static uint64_t rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
int main(int argc, char **argv) {
  if (argc < 2) return 1;
  if (!strcmp(argv[1], "enum") || !strcmp(argv[1], "dump")) { dumpmode = !strcmp(argv[1], "dump"); en = atoi(argv[2]); genperms(en); rec(0, 1);
    if (!dumpmode) { printf("enumerated rooted stopper classes on exactly %d nodes: %ld\n", en, ngraphs); report(); } else fprintf(stderr, "dumped %ld\n", ngraphs); return 0; }
  if (!strcmp(argv[1], "gen")) { int n = atoi(argv[2]); long cnt = atol(argv[3]); rs ^= (uint64_t)atol(argv[4]) * 0x9E3779B97F4A7C15ULL; int pct = atoi(argv[5]);
    for (int w = 0; w < 20; w++) rnd();
    long got = 0; while (got < cnt) { Gr g; g.n = n; for (int i = 0; i < n; i++) { g.L[i] = g.R[i] = 0; for (int j = 0; j < n; j++) { if ((int)(rnd() % 100) < pct) g.L[i] |= 1 << j; if ((int)(rnd() % 100) < pct) g.R[i] |= 1 << j; } }
      int o[16]; if (topo(&g, o) < 0) continue; got++; printf("%d", n); for (int i = 0; i < n; i++) printf(" %d %d", g.L[i], g.R[i]); printf("\n"); } return 0; }
  if (!strcmp(argv[1], "eval")) { int perline = argc > 2; char line[512];
    while (fgets(line, sizeof line, stdin)) { Gr g; char *p = line; int n = (int)strtol(p, &p, 10); g.n = n; for (int i = 0; i < n; i++) { g.L[i] = (uint8_t)strtol(p, &p, 10); g.R[i] = (uint8_t)strtol(p, &p, 10); }
      Res r; if (evalA(&g, &r) < 0) { printf("NONSTOPPER %s", line); continue; }
      if (perline) { printf("G"); for (int i = 0; i < n; i++) { char a[32], b[32]; fmtstop(a, r.LS1[i]); fmtstop(b, r.RS1[i]); printf(" [%d %d %s %s]", r.lam[i], r.rho[i], a, b); } printf("\n"); }
      tally(&g, &r); }
    report(); return 0; }
  return 1;
}
