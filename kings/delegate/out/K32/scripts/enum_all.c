// K32 independent count: all labelled graphs on nodes 0..N-1 with root 0, every node reachable from 0, no infinite
// alternating play, with NO relabelling restriction (a different enumeration from enum.c).  Also prints
// sum over enum.c's classes of the orbit sizes for comparison when given a class file.
// usage: enum_all N            -> prints the number of labelled rooted reachable stoppers
//        enum_all N classes.txt -> also computes sum over classes of (N-1)!/|Aut| and compares
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int N, Lm[8], Rm[8];
static long long cnt = 0;
static int cyc(int k) {  // alternating cycle test on the graph induced by the assigned nodes 0..k-1
  int col[16] = {0}, st[64], ip[16];
  for (int s0 = 0; s0 < 2 * k; s0++) {
    if (col[s0]) continue;
    int sp = 0; st[sp++] = s0; col[s0] = 1; ip[s0] = 0;
    while (sp) {
      int s = st[sp - 1], x = s >> 1, m = s & 1, mask = m ? Rm[x] : Lm[x], adv = 0;
      while (ip[s] < N) {
        int y = ip[s]++;
        if (!(mask >> y & 1) || y >= k) continue;
        int t = 2 * y + 1 - m;
        if (col[t] == 1) return 1;
        if (!col[t]) { col[t] = 1; ip[t] = 0; st[sp++] = t; adv = 1; break; }
      }
      if (!adv) { col[s] = 2; sp--; }
    }
  }
  return 0;
}
static int reachall(void) {
  int seen = 1, ch = 1;
  while (ch) { ch = 0; for (int x = 0; x < N; x++) if (seen >> x & 1) { int o = (Lm[x] | Rm[x]) & ~seen; if (o) { seen |= o; ch = 1; } } }
  return seen == (1 << N) - 1;
}
static void rec(int i) {
  if (i == N) { if (reachall()) cnt++; return; }
  for (int l = 0; l < (1 << N); l++) for (int r = 0; r < (1 << N); r++) { Lm[i] = l; Rm[i] = r; if (!cyc(i + 1)) rec(i + 1); }
}
int main(int argc, char **argv) {
  N = atoi(argv[1]);
  rec(0);
  printf("N=%d labelled rooted reachable stoppers: %lld\n", N, cnt);
  if (argc > 2) {
    FILE *f = fopen(argv[2], "r"); char line[256]; long long tot = 0;
    int fact = 1; for (int i = 2; i < N; i++) fact *= i;
    while (fgets(line, sizeof line, f)) {
      int n = 0; char *t = strtok(line, " \n");
      while (t) { sscanf(t, "%x/%x", &Lm[n], &Rm[n]); n++; t = strtok(NULL, " \n"); }
      // |orbit| = (N-1)!/|Aut fixing root|
      int a[8], aut = 0; for (int i = 0; i < N; i++) a[i] = i;
      while (1) {
        int ok = 1;
        for (int x = 0; x < N && ok; x++) { int l = 0, r = 0; for (int y = 0; y < N; y++) { if (Lm[x] >> y & 1) l |= 1 << a[y]; if (Rm[x] >> y & 1) r |= 1 << a[y]; } if (l != Lm[a[x]] || r != Rm[a[x]]) ok = 0; }
        aut += ok;
        int i = N - 2; while (i >= 1 && a[i] > a[i + 1]) i--;
        if (i < 1) break;
        int j = N - 1; while (a[j] < a[i]) j--;
        int tt = a[i]; a[i] = a[j]; a[j] = tt;
        for (int l = i + 1, r = N - 1; l < r; l++, r--) { tt = a[l]; a[l] = a[r]; a[r] = tt; }
      }
      tot += fact / aut;
    }
    printf("sum of orbit sizes over the class file: %lld\n", tot);
  }
  return 0;
}
