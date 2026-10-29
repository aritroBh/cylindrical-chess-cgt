/* K32 count C: independent count of isomorphism classes of rooted stopper graphs on exactly n nodes (all nodes reachable from
 * node 0), by plain labeled enumeration (every node chooses any Left set and any Right set), pruning on cycles,
 * and counting a labeling iff its encoding is the lexicographic minimum over the relabelings that fix node 0. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int n; static uint8_t L[6], R[6]; static long classes = 0, labeled = 0;
static int perm[120][6], np;
static int cyc(int upto) { /* state s=2*i+m (m=0: Left to move); closure over processed nodes */
  uint16_t succ[12]; int S = 2 * upto;
  for (int s = 0; s < S; s++) { int i = s >> 1, m = s & 1; uint8_t o = m ? R[i] : L[i]; uint16_t b = 0;
    for (int j = 0; j < upto; j++) if (o >> j & 1) b |= 1 << (2 * j + 1 - m); succ[s] = b; }
  for (int it = 0; it < 4; it++) { uint16_t nx[12];
    for (int s = 0; s < S; s++) { uint16_t b = succ[s]; for (int t = 0; t < S; t++) if (succ[s] >> t & 1) b |= succ[t]; nx[s] = b; }
    memcpy(succ, nx, sizeof(uint16_t) * S); }
  for (int s = 0; s < S; s++) if (succ[s] >> s & 1) return 1;
  return 0;
}
static void genperm(int k, int *a, int m) { if (k == m) { perm[np][0] = 0; for (int i = 0; i < m; i++) perm[np][i + 1] = a[i]; np++; return; }
  for (int i = k; i < m; i++) { int t = a[k]; a[k] = a[i]; a[i] = t; genperm(k + 1, a, m); t = a[k]; a[k] = a[i]; a[i] = t; } }
static void leaf(void) {
  /* reachability from 0 */
  int seen = 1, ch = 1; while (ch) { ch = 0; for (int i = 0; i < n; i++) if (seen >> i & 1) { int o = L[i] | R[i]; if ((seen | o) != seen) { seen |= o; ch = 1; } } }
  if (seen != (1 << n) - 1) return;
  labeled++;
  uint8_t e0[12], e1[12]; for (int i = 0; i < n; i++) { e0[2 * i] = L[i]; e0[2 * i + 1] = R[i]; }
  for (int q = 1; q < np; q++) { int *pm = perm[q]; uint8_t NL[6], NR[6];
    for (int i = 0; i < n; i++) { uint8_t l = 0, r = 0; for (int j = 0; j < n; j++) { if (L[i] >> j & 1) l |= 1 << pm[j]; if (R[i] >> j & 1) r |= 1 << pm[j]; } NL[pm[i]] = l; NR[pm[i]] = r; }
    for (int i = 0; i < n; i++) { e1[2 * i] = NL[i]; e1[2 * i + 1] = NR[i]; }
    if (memcmp(e1, e0, 2 * n) < 0) return; }
  classes++;
}
static void rec(int i) { if (i == n) { leaf(); return; }
  for (int l = 0; l < (1 << n); l++) for (int r = 0; r < (1 << n); r++) { L[i] = l; R[i] = r; if (cyc(i + 1)) continue; rec(i + 1); } }
int main(int argc, char **argv) { n = atoi(argv[1]); int a[6]; for (int i = 0; i < n - 1; i++) a[i] = i + 1; np = 0; genperm(0, a, n - 1);
  rec(0); printf("n=%d labeled rooted-reachable stoppers %ld, isomorphism classes %ld\n", n, labeled, classes); return 0; }
