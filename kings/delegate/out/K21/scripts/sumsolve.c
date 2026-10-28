/* K21: second, independent implementation of the D-sum and CGT-sum solvers (dense product, naive
 * Jacobi iteration to the least fixed point; the translation y -> y^B is re-implemented here).
 * Input (stdin), one instance per line:  B k  then for each component:  n root  then for each node:
 *   nl o... nr o...      (option: node index, -1 = PLUS, -2 = MINUS)
 * Output per instance:  D(L-to-move) D(R-to-move) C(L) C(R)   at the root tuple, results W/D/L for Left. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXC 4
typedef struct { int n, root; int *nl, *nr; int **L, **R; } Comp;

static int translate_into(Comp *c, int B, Comp *o) {
  int n = c->n, up = 0, um = 0;
  for (int x = 0; x < n; x++) {
    for (int i = 0; i < c->nl[x]; i++) { if (c->L[x][i] == -1) up = 1; if (c->L[x][i] == -2) um = 1; }
    for (int i = 0; i < c->nr[x]; i++) { if (c->R[x][i] == -1) up = 1; if (c->R[x][i] == -2) um = 1; }
  }
  int tot = n + (up ? B + 1 : 0) + (um ? B + 1 : 0);
  o->n = tot; o->root = c->root;
  o->nl = calloc(tot, sizeof(int)); o->nr = calloc(tot, sizeof(int));
  o->L = calloc(tot, sizeof(int *)); o->R = calloc(tot, sizeof(int *));
  int pb = up ? n : -1, mb = um ? n + (up ? B + 1 : 0) : -1;
  for (int x = 0; x < tot; x++) { o->L[x] = calloc(8, sizeof(int)); o->R[x] = calloc(8, sizeof(int)); }
  for (int x = 0; x < n; x++) {
    for (int i = 0; i < c->nl[x]; i++) { int v = c->L[x][i]; o->L[x][o->nl[x]++] = v == -1 ? pb + B : v == -2 ? mb + B : v; }
    for (int i = 0; i < c->nr[x]; i++) { int v = c->R[x][i]; o->R[x][o->nr[x]++] = v == -1 ? pb + B : v == -2 ? mb + B : v; }
  }
  if (up) for (int i = 1; i <= B; i++) o->L[pb + i][o->nl[pb + i]++] = pb + i - 1;
  if (um) for (int i = 1; i <= B; i++) o->R[mb + i][o->nr[mb + i]++] = mb + i - 1;
  return 0;
}

static int k; static Comp *cs; static long total; static int stride[MAXC];

/* res[s] for s = 2*tupleIndex + mover: 'W','D','L' */
static void solve(Comp *cp, char *res) {
  long T = 1; for (int c = 0; c < k; c++) { stride[c] = (int)T; T *= cp[c].n; }
  long S = 2 * T;
  char *W[2]; W[0] = calloc(S, 1); W[1] = calloc(S, 1);   /* W[0]: Left forced win, W[1]: Right forced win */
  for (int sg = 0; sg < 2; sg++) {
    int changed = 1;
    while (changed) {
      changed = 0;
      for (long t = 0; t < T; t++) {
        int node[MAXC]; long r = t; for (int c = 0; c < k; c++) { node[c] = r % cp[c].n; r /= cp[c].n; }
        for (int m = 0; m < 2; m++) {
          long s = 2 * t + m; if (W[sg][s]) continue;
          int anyw = 0, allw = 1, hasopt = 0, theirs = 0;
          for (int c = 0; c < k; c++) {
            int cnt = m == 0 ? cp[c].nl[node[c]] : cp[c].nr[node[c]];
            int *op = m == 0 ? cp[c].L[node[c]] : cp[c].R[node[c]];
            for (int i = 0; i < cnt; i++) {
              hasopt = 1; int o = op[i];
              if (o == -1 || o == -2) { int who = (o == -1) ? 0 : 1; if (who == sg) anyw = 1; else { theirs = 1; allw = 0; } }
              else { long t2 = t + (long)(o - node[c]) * stride[c]; if (W[sg][2 * t2 + 1 - m]) anyw = 1; else allw = 0; }
            }
          }
          int win;
          if (m == sg) win = anyw; else win = (!hasopt) ? 1 : (allw && !theirs);
          if (win) { W[sg][s] = 1; changed = 1; }
        }
      }
    }
  }
  for (long s = 0; s < S; s++) res[s] = W[0][s] ? 'W' : (W[1][s] ? 'L' : 'D');
  free(W[0]); free(W[1]);
}

int main(void) {
  int B;
  while (scanf("%d %d", &B, &k) == 2) {
    Comp c[MAXC], t[MAXC];
    for (int i = 0; i < k; i++) {
      scanf("%d %d", &c[i].n, &c[i].root);
      c[i].nl = calloc(c[i].n, sizeof(int)); c[i].nr = calloc(c[i].n, sizeof(int));
      c[i].L = calloc(c[i].n, sizeof(int *)); c[i].R = calloc(c[i].n, sizeof(int *));
      for (int x = 0; x < c[i].n; x++) {
        scanf("%d", &c[i].nl[x]); c[i].L[x] = calloc(c[i].nl[x] + 1, sizeof(int));
        for (int j = 0; j < c[i].nl[x]; j++) scanf("%d", &c[i].L[x][j]);
        scanf("%d", &c[i].nr[x]); c[i].R[x] = calloc(c[i].nr[x] + 1, sizeof(int));
        for (int j = 0; j < c[i].nr[x]; j++) scanf("%d", &c[i].R[x][j]);
      }
      translate_into(&c[i], B, &t[i]);
    }
    long T = 1; for (int i = 0; i < k; i++) T *= c[i].n;
    char *rd = malloc(2 * T), *rc;
    solve(c, rd);
    long T2 = 1; for (int i = 0; i < k; i++) T2 *= t[i].n;
    rc = malloc(2 * T2);
    solve(t, rc);
    long idxd = 0, idxc = 0, sd = 1, sc = 1;
    for (int i = 0; i < k; i++) { idxd += c[i].root * sd; sd *= c[i].n; idxc += t[i].root * sc; sc *= t[i].n; }
    if (getenv("K21_ALL")) {
      /* every tuple of original nodes: D(L) D(R) C(L) C(R), in mixed-radix order of the original nodes */
      long Tn = 1; for (int i = 0; i < k; i++) Tn *= c[i].n;
      for (long tt = 0; tt < Tn; tt++) {
        long r = tt, ic = 0, sc2 = 1; int node[MAXC];
        for (int i = 0; i < k; i++) { node[i] = r % c[i].n; r /= c[i].n; }
        for (int i = 0; i < k; i++) { ic += (long)node[i] * sc2; sc2 *= t[i].n; }
        printf("%c%c%c%c ", rd[2 * tt], rd[2 * tt + 1], rc[2 * ic], rc[2 * ic + 1]);
      }
      printf("\n");
    } else
    printf("%c %c %c %c\n", rd[2 * idxd], rd[2 * idxd + 1], rc[2 * idxc], rc[2 * idxc + 1]);
    free(rd); free(rc);
  }
  return 0;
}
