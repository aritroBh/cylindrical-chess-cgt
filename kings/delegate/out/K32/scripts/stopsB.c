/* K32 implementation B (C), written independently of stopsA.c.  Input (stdin): graph lines "n L0 R0 L1 R1 ..." (masks).
 * Output: one line per graph "G [lam rho LS RS] ..." with the stops in sixteenths (+inf/-inf), same text as `stopsA eval p`.
 * Differences from A: (1) a single generic solver for two-component sums (Gauss-Seidel sweeps to the least fixed point of
 * "Left wins" and of "Right wins", checks that every state is won by exactly one side); (2) the number -x is an explicit game
 * node (no sign trick); the grid is finer (1/32); the sup is resolved to sixteenths by the parity rule; (3) the reserves are
 * read from the sum with explicit token chains; (4) D1 is a memoised DFS recursion, the number clause is an equality test
 * (second player wins g - x); (5) the stopper test is a DFS cycle search. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define KB 5
#define ONE (1<<KB)
#define OUTONE 16
#define INF 1000000000
#define NINF (-1000000000)
#define CINF 99
typedef struct { int n; uint8_t L[8], R[8]; } Gr;
static Gr G;
/* number games on the grid: node v (index = m + OFF) is the number m/ONE */
static int M, GN, OFF;
static int nL[800], nR[800]; /* single option or -1 */
static void build_numbers(int Mv) {
  M = Mv; GN = 2 * M * ONE + 1; OFF = M * ONE;
  for (int i = 0; i < GN; i++) { int m = i - OFF; nL[i] = nR[i] = -1;
    if (m == 0) continue;
    if (m % ONE == 0) { if (m > 0) nL[i] = i - ONE; else nR[i] = i + ONE; continue; }
    int a = m < 0 ? -m : m, t = 0; while (a % 2 == 0) { a /= 2; t++; }
    nL[i] = i - (1 << t); nR[i] = i + (1 << t); }
}
/* generic sum solver for  G + H  where H is described by (hl[], hr[], hn nodes; each node has <=1 option per side).
 * W[side][g][h][mover], side 0 = Left wins, 1 = Right wins, mover 0 = Left to move.  Returns 0 and fills the arrays. */
static uint8_t W[2][8][800][2];
static int hn; static int *hl, *hr;
static int solve_sum(void) {
  int n = G.n;
  memset(W, 0, sizeof W);
  for (int side = 0; side < 2; side++) {
    int ch = 1;
    while (ch) { ch = 0;
      for (int g = n - 1; g >= 0; g--) for (int h = 0; h < hn; h++) for (int mv = 0; mv < 2; mv++) {
        if (W[side][g][h][mv]) continue;
        int mine = (mv == side);   /* the player who moves is the one we ask about */
        int anyw = 0, allw = 1, has = 0;
        uint8_t o = mv ? G.R[g] : G.L[g];
        for (int j = 0; j < n; j++) if (o >> j & 1) { has = 1; if (W[side][j][h][1 - mv]) anyw = 1; else allw = 0; }
        int hop = mv ? hr[h] : hl[h];
        if (hop >= 0) { has = 1; if (W[side][g][hop][1 - mv]) anyw = 1; else allw = 0; }
        int win = mine ? anyw : (has ? allw : 1);
        if (win) { W[side][g][h][mv] = 1; ch = 1; }
      } }
  }
  for (int g = 0; g < n; g++) for (int h = 0; h < hn; h++) for (int mv = 0; mv < 2; mv++) if (W[0][g][h][mv] == W[1][g][h][mv]) return -1;
  return 0;
}
static int stopper(const Gr *g) { /* DFS cycle search on (node,mover) */
  int col[16] = {0}; int stk[64], it[64], sp;
  for (int s0 = 0; s0 < 2 * g->n; s0++) { if (col[s0]) continue; sp = 0; stk[0] = s0; it[0] = 0; col[s0] = 1; sp = 1;
    while (sp) { int s = stk[sp - 1], i = s >> 1, m = s & 1; uint8_t o = m ? g->R[i] : g->L[i]; int j = it[sp - 1];
      while (j < g->n && !(o >> j & 1)) j++;
      if (j == g->n) { col[s] = 2; sp--; continue; }
      it[sp - 1] = j + 1; int t = 2 * j + (1 - m);
      if (col[t] == 1) return 0; if (col[t] == 0) { col[t] = 1; stk[sp] = t; it[sp] = 0; sp++; } } }
  return 1;
}
static int memo[2][8], have[2][8], eqv[8], iseq[8];
static int stopr(int side, int i) { /* side 0: LS(i); side 1: RS(i) */
  if (have[side][i]) return memo[side][i];
  int v;
  if (iseq[i]) v = eqv[i];
  else if (side == 0) { v = NINF; for (int j = 0; j < G.n; j++) if (G.L[i] >> j & 1) { int q = stopr(1, j); if (q > v) v = q; } }
  else { v = INF; for (int j = 0; j < G.n; j++) if (G.R[i] >> j & 1) { int q = stopr(0, j); if (q < v) v = q; } }
  have[side][i] = 1; memo[side][i] = v; return v;
}
static void fmt(char *b, int s) { if (s == INF) strcpy(b, "+inf"); else if (s == NINF) strcpy(b, "-inf"); else sprintf(b, "%d/%d", s, OUTONE); }
int main(void) {
  char line[512];
  int hlN[800], hrN[800];
  while (fgets(line, sizeof line, stdin)) {
    char *p = line; int n = (int)strtol(p, &p, 10); G.n = n;
    for (int i = 0; i < n; i++) { G.L[i] = (uint8_t)strtol(p, &p, 10); G.R[i] = (uint8_t)strtol(p, &p, 10); }
    if (!stopper(&G)) { printf("NONSTOPPER %s", line); continue; }
    int Mv = n + 1, Cmax = n + 2;
    build_numbers(Mv);
    /* H = the number -x for each grid x: use the number node for value -x, i.e. node index (GN-1-i) for x = node i */
    hn = GN; for (int i = 0; i < GN; i++) { hlN[i] = nL[i]; hrN[i] = nR[i]; } hl = hlN; hr = hrN;
    if (solve_sum() < 0) { printf("SOLVEFAIL %s", line); continue; }
    /* profile in terms of x: Lsecond(g,x) = W[0][g][node(-x)][mover Right=1], Lfirst(g,x) = W[0][g][node(-x)][0] */
    int lam[8], rho[8], LS2[8], RS2[8];
    int LSr[8], RSr[8];
    for (int g = 0; g < n; g++) {
      /* D2 */
      for (int pass = 0; pass < 2; pass++) {
        int val, topx = GN - 1, botx = 0; int mvv = pass ? 0 : 1;
        #define P(x) W[0][g][GN - 1 - (x)][mvv]
        if (P(topx)) val = INF; else if (!P(botx)) val = NINF;
        else { int xm = botx; for (int x = botx; x <= topx; x++) if (P(x)) xm = x;
               int m = xm - OFF; /* in 1/32 units; target multiples of 1/16 = 2 units */
               int r = (m % 2 == 0) ? m : m + 1; val = r / 2; }
        if (pass) LS2[g] = val; else RS2[g] = val;
      }
    }
    /* number clause and D1 */
    memset(have, 0, sizeof have);
    for (int g = 0; g < n; g++) { iseq[g] = 0; eqv[g] = 0;
      for (int x = 0; x < GN; x++) { int hi = GN - 1 - x; if (W[0][g][hi][1] && W[1][g][hi][0]) { iseq[g] = 1; eqv[g] = (x - OFF); } }
      /* eqv in 1/32 units: only multiples of 1/16 are expected; convert */
      if (iseq[g]) { if (eqv[g] % 2) eqv[g] = 1000001; else eqv[g] /= 2; } }
    for (int g = 0; g < n; g++) { LSr[g] = stopr(0, g); RSr[g] = stopr(1, g); }
    /* reserves: explicit chains */
    int cl[40], cr[40];
    hn = Cmax + 1;
    for (int c = 0; c <= Cmax; c++) { cl[c] = c ? c - 1 : -1; cr[c] = -1; }
    hl = cl; hr = cr; if (solve_sum() < 0) { printf("SOLVEFAIL2 %s", line); continue; }
    for (int g = 0; g < n; g++) { lam[g] = CINF; for (int c = 0; c <= Cmax; c++) if (W[0][g][c][1]) { lam[g] = c; break; } }
    for (int c = 0; c <= Cmax; c++) { cl[c] = -1; cr[c] = c ? c - 1 : -1; }
    if (solve_sum() < 0) { printf("SOLVEFAIL3 %s", line); continue; }
    for (int g = 0; g < n; g++) { rho[g] = CINF; for (int c = 0; c <= Cmax; c++) if (W[1][g][c][0]) { rho[g] = c; break; } }
    printf("G");
    for (int g = 0; g < n; g++) { char a[32], b[32]; fmt(a, LSr[g]); fmt(b, RSr[g]); printf(" [%d %d %s %s]", lam[g], rho[g], a, b);
      if (LSr[g] != LS2[g] || RSr[g] != RS2[g]) printf("!D1D2"); }
    printf("\n");
  }
  return 0;
}
