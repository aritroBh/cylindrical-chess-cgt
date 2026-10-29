// K32 enumerator: all finite stoppers (terminal-free loopy games) on exactly N nodes, every node reachable from node 0.
// Node i has Left option set Lm[i] and Right option set Rm[i] (bitmasks over 0..N-1; self loops and cycles allowed
// but no infinite alternating play).  BFS-order restriction removes most relabellings; the printed form is the
// canonical form under permutations of nodes 1..N-1 (lexicographically least), so "sort -u" gives isomorphism classes.
// usage: enum N [count|print]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int N;
static int Lm[8], Rm[8];
static long long leaves = 0;
static int mode = 0;
static int perm[8];

// alternating-cycle test on nodes 0..k-1 (edges only among assigned nodes)
static int has_cycle(int k) {
  // state s = 2*x+m ; m=0 Left to move: edges to (y,1) for y in Lm[x]; m=1: to (y,0) for y in Rm[x]
  int col[16]; memset(col, 0, sizeof col);
  int stack[64], itpos[16];
  for (int s0 = 0; s0 < 2 * k; s0++) {
    if (col[s0]) continue;
    int sp = 0; stack[sp++] = s0; col[s0] = 1; itpos[s0] = 0;
    while (sp) {
      int s = stack[sp - 1]; int x = s >> 1, m = s & 1;
      int mask = m ? Rm[x] : Lm[x];
      int adv = 0;
      while (itpos[s] < N) {
        int y = itpos[s]++;
        if (!(mask >> y & 1) || y >= k) continue;
        int t = 2 * y + (1 - m);
        if (col[t] == 1) return 1;
        if (col[t] == 0) { col[t] = 1; itpos[t] = 0; stack[sp++] = t; adv = 1; break; }
      }
      if (!adv) { col[s] = 2; sp--; }
    }
  }
  return 0;
}

static void canon_print(void) {
  // permutations of 1..N-1 (root fixed); encode as the sequence (Lm[0],Rm[0],Lm[1],Rm[1],...) after relabelling
  int p[8]; for (int i = 0; i < N; i++) p[i] = i;
  long long best = -1; int bL[8], bR[8];
  // iterate all perms of 1..N-1 via Heap-like simple recursion using next_permutation
  int a[8]; for (int i = 1; i < N; i++) a[i] = i;
  while (1) {
    // new label of old node i is a[i] (a[0]=0). relabelled node a[i] has masks mapped
    int nL[8], nR[8];
    a[0] = 0;
    for (int i = 0; i < N; i++) {
      int l = 0, r = 0;
      for (int y = 0; y < N; y++) {
        if (Lm[i] >> y & 1) l |= 1 << a[y];
        if (Rm[i] >> y & 1) r |= 1 << a[y];
      }
      nL[a[i]] = l; nR[a[i]] = r;
    }
    long long code = 0;
    for (int i = 0; i < N; i++) code = (code << (2 * N)) | ((long long)nL[i] << N) | nR[i];
    if (best < 0 || code < best) { best = code; memcpy(bL, nL, sizeof nL); memcpy(bR, nR, sizeof nR); }
    // next permutation of a[1..N-1]
    int i = N - 2; while (i >= 1 && a[i] > a[i + 1]) i--;
    if (i < 1) break;
    int j = N - 1; while (a[j] < a[i]) j--;
    int t = a[i]; a[i] = a[j]; a[j] = t;
    for (int l = i + 1, r = N - 1; l < r; l++, r--) { t = a[l]; a[l] = a[r]; a[r] = t; }
  }
  for (int i = 0; i < N; i++) printf("%x/%x%c", bL[i], bR[i], i + 1 < N ? ' ' : '\n');
}

// m = number of discovered nodes so far (nodes 0..m-1)
static void rec(int i, int m) {
  if (i == N) { if (m == N) { leaves++; if (mode) canon_print(); } return; }
  if (i >= m) return;  // node i not reachable
  int full = (1 << N) - 1;
  for (int l = 0; l <= full; l++) {
    for (int r = 0; r <= full; r++) {
      int u = (l | r) >> m;  // bits for undiscovered nodes
      if (u & (u + 1)) continue;  // must be a contiguous block starting at m: u in {0,1,3,7,...}
      int t = 0; while ((u >> t) & 1) t++;
      Lm[i] = l; Rm[i] = r;
      if (has_cycle(i + 1)) continue;
      rec(i + 1, m + t);
    }
  }
  Lm[i] = Rm[i] = 0;
}
int main(int argc, char **argv) {
  N = atoi(argv[1]); mode = (argc > 2 && !strcmp(argv[2], "print"));
  rec(0, 1);
  fprintf(stderr, "N=%d leaves=%lld\n", N, leaves);
  return 0;
}
