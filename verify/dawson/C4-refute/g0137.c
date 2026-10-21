/* Second independent implementation (C) of 0.137 Grundy values, N up to 2000. */
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
  int N = argc > 1 ? atoi(argv[1]) : 300;
  int *g = calloc(N + 1, sizeof(int));
  for (int n = 1; n <= N; n++) {
    unsigned char seen[4096] = {0};
    if (n == 1) seen[0] = 1;
    if (n >= 2) seen[g[n - 2]] = 1;
    for (int a = 0; a + 3 <= n; a++) seen[g[a] ^ g[n - 3 - a]] = 1;
    int m = 0; while (seen[m]) m++;
    g[n] = m;
  }
  for (int n = 0; n <= N; n++) printf("%d%c", g[n], n == N ? '\n' : ' ');
  int last = -1; for (int n = 0; n + 34 <= N; n++) if (g[n] != g[n + 34]) { printf("exc %d\n", n); last = n; }
  printf("last %d\n", last);
  return 0;
}
