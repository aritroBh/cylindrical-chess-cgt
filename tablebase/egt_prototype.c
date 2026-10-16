// Tiny DTM retrograde solver: K + (1 or 2 white pieces) vs lone K on 8x8 plane / cylinder / torus.
// Usage: egt <plane|cyl|torus> <pieces, e.g. Q or BN>
// Brute-force layered iteration (no symmetry), for sanity-checking mating-material claims only.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef uint64_t BB;
static int WF, WR; // wrap files / wrap ranks
static int sqstep(int s, int df, int dr) {
  int f = s & 7, r = s >> 3;
  f += df; r += dr;
  if (WF) f = (f + 8) & 7; else if (f < 0 || f > 7) return -1;
  if (WR) r = (r + 8) & 7; else if (r < 0 || r > 7) return -1;
  return r * 8 + f;
}
static BB KA[64], NA[64];
static int RAY[64][8][8], RAYN[64][8];
static const int DIR[8][2] = {{1,0},{-1,0},{0,1},{0,-1},{1,1},{1,-1},{-1,1},{-1,-1}};
static void init(void) {
  for (int s = 0; s < 64; s++) {
    KA[s] = NA[s] = 0;
    for (int d = 0; d < 8; d++) { int t = sqstep(s, DIR[d][0], DIR[d][1]); if (t >= 0 && t != s) KA[s] |= 1ULL << t; }
    static const int nd[8][2] = {{1,2},{2,1},{-1,2},{-2,1},{1,-2},{2,-1},{-1,-2},{-2,-1}};
    for (int d = 0; d < 8; d++) { int t = sqstep(s, nd[d][0], nd[d][1]); if (t >= 0 && t != s) NA[s] |= 1ULL << t; }
    for (int d = 0; d < 8; d++) {
      int n = 0, t = s;
      for (;;) { t = sqstep(t, DIR[d][0], DIR[d][1]); if (t < 0 || t == s) break; RAY[s][d][n++] = t; }
      RAYN[s][d] = n;
    }
  }
}
static BB slide(int s, BB occ, int d0, int d1) {
  BB a = 0;
  for (int d = d0; d < d1; d++)
    for (int i = 0; i < RAYN[s][d]; i++) { int t = RAY[s][d][i]; a |= 1ULL << t; if (occ >> t & 1) break; }
  return a;
}
static BB attacks(char p, int s, BB occ) {
  switch (p) {
    case 'K': return KA[s];
    case 'N': return NA[s];
    case 'R': return slide(s, occ, 0, 4);
    case 'B': return slide(s, occ, 4, 8);
    case 'Q': return slide(s, occ, 0, 8);
  }
  return 0;
}

// Table layout: idx = ((wk*64 + bk)*64 + p1)*64 + p2  (p2 only if np==2)
typedef struct { int np; char pc[2]; int8_t *w, *b; size_t n; } Tab; // w: wtm DTM (>0 won in n), b: btm lost-in n (>=0 lost), -1 = not (yet) won/lost, -2 illegal
static Tab sub[2]; // sub[i] = table with piece i removed (only for np==2)
static Tab T;
static size_t IDX(int np, int wk, int bk, const int *p) {
  size_t i = (size_t)wk * 64 + bk; for (int k = 0; k < np; k++) i = i * 64 + p[k]; return i;
}
static void decode(int np, size_t i, int *wk, int *bk, int *p) {
  for (int k = np - 1; k >= 0; k--) { p[k] = i & 63; i >>= 6; }
  *bk = i & 63; i >>= 6; *wk = (int)i;
}

static void solve(Tab *t, int verbose, const char *topo) {
  int np = t->np; t->n = (size_t)1 << (6 * (np + 2));
  t->w = malloc(t->n); t->b = malloc(t->n);
  int wk, bk, p[2];
  size_t legalW = 0, legalB = 0;
  for (size_t i = 0; i < t->n; i++) {
    decode(np, i, &wk, &bk, p);
    BB occ = (1ULL << wk) | (1ULL << bk); int ok = wk != bk && !(KA[wk] >> bk & 1);
    for (int k = 0; k < np && ok; k++) { if (occ >> p[k] & 1) ok = 0; occ |= 1ULL << p[k]; }
    if (!ok) { t->w[i] = t->b[i] = -2; continue; }
    // wtm legal iff bK not attacked
    BB att = 0; for (int k = 0; k < np; k++) att |= attacks(t->pc[k], p[k], occ);
    t->w[i] = (att >> bk & 1) ? -2 : -1; if (t->w[i] == -1) legalW++;
    t->b[i] = -1; legalB++;
  }
  int maxd = 0, changed = 1;
  for (int n = 0; changed && n < 120; n++) {
    changed = 0;
    // btm lost in n: all black moves go to wtm won in <= n (n==0: mate)
    for (size_t i = 0; i < t->n; i++) {
      if (t->b[i] != -1) continue;
      decode(np, i, &wk, &bk, p);
      BB occ = (1ULL << wk) | (1ULL << bk); for (int k = 0; k < np; k++) occ |= 1ULL << p[k];
      BB occNoBK = occ & ~(1ULL << bk);
      BB att = KA[wk]; for (int k = 0; k < np; k++) att |= attacks(t->pc[k], p[k], occNoBK);
      int inCheck = att >> bk & 1;
      BB mv = KA[bk] & ~att; // includes captures of undefended pieces
      int any = 0, allwon = 1;
      while (mv) {
        int to = __builtin_ctzll(mv); mv &= mv - 1;
        any = 1;
        int cap = -1; for (int k = 0; k < np; k++) if (p[k] == to) cap = k;
        if (cap < 0) {
          int8_t v = t->w[IDX(np, wk, to, p)];
          if (!(v > 0 && v <= n)) { allwon = 0; break; }
        } else {
          if (np == 1) { allwon = 0; break; } // K vs K
          int q[1] = { p[1 - cap] };
          int8_t v = sub[cap].w[IDX(1, wk, to, q)];
          if (!(v > 0 && v <= n)) { allwon = 0; break; }
        }
      }
      if (!any) { if (inCheck && n == 0) { t->b[i] = 0; changed = 1; } else if (!inCheck) t->b[i] = -3; /* stalemate */ continue; }
      if (n > 0 && allwon) { t->b[i] = n; changed = 1; }
    }
    // wtm won in n+1: some move to btm lost in n
    for (size_t i = 0; i < t->n; i++) {
      if (t->w[i] != -1) continue;
      decode(np, i, &wk, &bk, p);
      BB occ = (1ULL << wk) | (1ULL << bk); for (int k = 0; k < np; k++) occ |= 1ULL << p[k];
      int found = 0;
      BB mv = KA[wk] & ~occ & ~KA[bk];
      while (mv && !found) { int to = __builtin_ctzll(mv); mv &= mv - 1; if (t->b[IDX(np, to, bk, p)] == n) found = 1; }
      for (int k = 0; k < np && !found; k++) {
        BB m2 = attacks(t->pc[k], p[k], occ) & ~occ;
        while (m2 && !found) { int to = __builtin_ctzll(m2); m2 &= m2 - 1; int q[2] = { p[0], p[1] }; q[k] = to; if (t->b[IDX(np, wk, bk, q)] == n) found = 1; }
      }
      if (found) { t->w[i] = n + 1; changed = 1; if (n + 1 > maxd) maxd = n + 1; }
    }
  }
  if (verbose) {
    size_t wonW = 0, mates = 0, stale = 0;
    for (size_t i = 0; i < t->n; i++) { if (t->w[i] > 0) wonW++; if (t->b[i] == 0) mates++; if (t->b[i] == -3) stale++; }
    if (getenv("SHOW")) {
      const char *F="abcdefgh"; int shown=0;
      for (size_t i = 0; i < t->n && shown < 3; i++) if (t->b[i] == 0) { decode(np,i,&wk,&bk,p);
        printf("  mate(btm): WK %c%d BK %c%d", F[wk&7], (wk>>3)+1, F[bk&7], (bk>>3)+1);
        for (int k=0;k<np;k++) printf(" %c %c%d", t->pc[k], F[p[k]&7], (p[k]>>3)+1); printf("\n"); shown++; }
      for (size_t i = 0; i < t->n; i++) if (t->w[i] == maxd && maxd > 0) { decode(np,i,&wk,&bk,p);
        printf("  maxDTM(wtm): WK %c%d BK %c%d", F[wk&7], (wk>>3)+1, F[bk&7], (bk>>3)+1);
        for (int k=0;k<np;k++) printf(" %c %c%d", t->pc[k], F[p[k]&7], (p[k]>>3)+1); printf("\n"); break; }
    }
    if (np==2 && t->pc[0]=='B' && t->pc[1]=='B') { size_t oc=0, ocw=0;
      for (size_t i = 0; i < t->n; i++) if (t->w[i] != -2) { decode(np,i,&wk,&bk,p);
        if ((((p[0]&7)+(p[0]>>3)) ^ ((p[1]&7)+(p[1]>>3))) & 1) { oc++; if (t->w[i] > 0) ocw++; } }
      printf("  opposite-coloured bishops: legal wtm=%zu won=%zu (%.3f%%)\n", oc, ocw, 100.0*ocw/oc); }
    printf("%-6s K%.*svK: legal wtm=%zu won=%zu (%.3f%%) maxDTM=%d | btm mates=%zu stalemates=%zu\n",
           topo, np, t->pc, legalW, wonW, 100.0 * wonW / legalW, maxd, mates, stale);
  }
}

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: egt plane|cyl|torus PIECES\n"); return 1; }
  WF = strcmp(argv[1], "plane") != 0; WR = strcmp(argv[1], "torus") == 0;
  init();
  int np = (int)strlen(argv[2]);
  T.np = np; memcpy(T.pc, argv[2], np);
  if (np == 2) {
    for (int c = 0; c < 2; c++) { sub[c].np = 1; sub[c].pc[0] = argv[2][1 - c]; solve(&sub[c], 1, argv[1]); }
  }
  solve(&T, 1, argv[1]);
  return 0;
}
