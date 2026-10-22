/* enum_kpkp.c -- enumerate every legal K+P vs K+P position (8x8 flat or cylinder), ep target '-'.
 * Fixes the bug in ../enumerate.c, which printed the Black pawn as 'P' (a second White pawn).
 * usage: enum_kpkp <flat|cyl> [chunk nchunks]    (chunk i of n splits on the White king square)
 * Order: wk, bk, wp, bp, then 'w' line before 'b' line.  Legal = squares distinct, kings not adjacent,
 * pawns on ranks 2..7, side NOT to move not attacked (by a king or by an enemy pawn).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 8
static int wrap;
static int kdist(int a, int b) {
  int df = abs(a % N - b % N); if (wrap && N - df < df) df = N - df;
  int dr = abs(a / N - b / N); return df > dr ? df : dr;
}
/* does a pawn of colour c (0 white, 1 black) on p attack square t */
static int pattack(int c, int p, int t) {
  int f = p % N, r = p / N, tr = t / N, tf = t % N;
  if (tr != r + (c == 0 ? 1 : -1)) return 0;
  int d = (tf - f + N) % N;
  if (wrap) return d == 1 || d == N - 1;
  return abs(tf - f) == 1;
}
static void nm(int s, char *o) { o[0] = 'a' + s % N; o[1] = '1' + s / N; o[2] = 0; }
int main(int argc, char **argv) {
  if (argc < 2) return 1;
  wrap = !strcmp(argv[1], "cyl");
  int chunk = 0, nch = 1;
  if (argc >= 4) { chunk = atoi(argv[2]); nch = atoi(argv[3]); }
  long long cnt = 0;
  char a[3], b[3], c[3], d[3];
  for (int wk = 0; wk < 64; wk++) {
    if (wk * nch / 64 != chunk) continue;
    for (int bk = 0; bk < 64; bk++) {
      if (bk == wk || kdist(wk, bk) <= 1) continue;
      for (int wp = 8; wp < 56; wp++) {
        if (wp == wk || wp == bk) continue;
        for (int bp = 8; bp < 56; bp++) {
          if (bp == wk || bp == bk || bp == wp) continue;
          nm(wk, a); nm(bk, b); nm(wp, c); nm(bp, d);
          if (!pattack(0, wp, bk)) { printf("K%s P%s k%s p%s w -\n", a, c, b, d); cnt++; }
          if (!pattack(1, bp, wk)) { printf("K%s P%s k%s p%s b -\n", a, c, b, d); cnt++; }
        }
      }
    }
  }
  fprintf(stderr, "enum_kpkp %s chunk %d/%d: %lld positions\n", wrap ? "cyl" : "flat", chunk, nch, cnt);
  return 0;
}
