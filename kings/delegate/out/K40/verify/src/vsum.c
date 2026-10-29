/* vsum.c -- K40 referee's own solver for (K+P vs K) [+] T on cyl:WxH, written from kings/SPEC.md
 * and LOOPY Definitions 1.2/1.3/1.5 only (not from K40's kpsum.c / ksum2.py).
 *
 * x = K+P vs K, White pawn, cylinder (files wrap).  P model: any promotion = White wins at once.
 * Kxp = draw at once (K v K is dead; Lemma 1 is checked separately by --kvk).
 * T = one node of a fixed test graph (disjoint union of integers -M..M, on, off, dud, over, under, *, up, down,
 * +-1, on+*).  A T-move is illegal for a side in check (only Black can be in check).
 * Side with no option at all:  conv N: it loses;  conv C: in check -> loses (mate), else draw (stalemate).
 * Options: --kxploss  Kxp counts as a Black win (diagnostic);  --atlas  T=0 only, the atlas promotion rule
 *   (queen; Kxq -> draw; stalemate -> draw; else win), computed from my own queen-attack code.
 * Output (stdout): one line per legal (mover,k): "<pos> <s>\t<results over T nodes>" with W/L/D.
 * Usage: vsum W H N|C [M] [--kxploss] [--atlas]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int W, H, NS, M = 12, KXPLOSS = 0, ATLAS = 0, CONV_N = 1;
static int fileof(int s) { return s % W; }
static int rankof(int s) { return s / W; }
static int sq(int f, int r) { if (r < 0 || r >= H) return -1; f = ((f % W) + W) % W; return r * W + f; }
static int adj(int a, int b) {
  if (a == b) return 0;
  int dr = abs(rankof(a) - rankof(b)); if (dr > 1) return 0;
  int df = abs(fileof(a) - fileof(b)); if (W - df < df) df = W - df;
  return df <= 1;
}
static int patt(int p, int t) { /* white pawn on p attacks t */
  return rankof(t) == rankof(p) + 1 && (sq(fileof(p) - 1, rankof(p) + 1) == t || sq(fileof(p) + 1, rankof(p) + 1) == t);
}
/* T graph */
enum { MAXT = 64 };
static int NT; static int TL[MAXT][3], nTL[MAXT], TR[MAXT][3], nTR[MAXT]; static char tname[MAXT][16];
static int addt(const char *nm) { strcpy(tname[NT], nm); nTL[NT] = nTR[NT] = 0; return NT++; }
static int IDX0;
static void build_T(void) {
  NT = 0;
  for (int m = -M; m <= M; m++) { char b[16]; sprintf(b, "%d", m); addt(b); }
  IDX0 = M;
  for (int m = -M; m <= M; m++) { int i = m + M; if (m > 0) TL[i][nTL[i]++] = i - 1; if (m < 0) TR[i][nTR[i]++] = i + 1; }
  int on = addt("on"), off = addt("off"), dud = addt("dud"), over = addt("over"), under = addt("under"),
      st = addt("*"), up = addt("up"), dn = addt("down"), pm = addt("pm1"), ons = addt("on*");
  TL[on][nTL[on]++] = on; TR[off][nTR[off]++] = off;
  TL[dud][nTL[dud]++] = dud; TR[dud][nTR[dud]++] = dud;
  TL[over][nTL[over]++] = IDX0; TR[over][nTR[over]++] = over;
  TL[under][nTL[under]++] = under; TR[under][nTR[under]++] = IDX0;
  TL[st][nTL[st]++] = IDX0; TR[st][nTR[st]++] = IDX0;
  TL[up][nTL[up]++] = IDX0; TR[up][nTR[up]++] = st;
  TL[dn][nTL[dn]++] = st; TR[dn][nTR[dn]++] = IDX0;
  TL[pm][nTL[pm]++] = IDX0 + 1; TR[pm][nTR[pm]++] = IDX0 - 1;
  TL[ons][nTL[ons]++] = ons; TL[ons][nTL[ons]++] = on; TR[ons][nTR[ons]++] = on;
}
/* kpk moves */
#define PROMO (-1)
#define KXP (-2)
#define PROMO_D (-3) /* atlas: promotion scored draw */
static int NK; static unsigned char *legal[2], *incheck; static int *mv[2]; static unsigned char *nmv[2];
static int kidx(int wk, int bk, int p) { return (wk * NS + bk) * NS + p; }
static int qatt(int q, int t, int wk) { /* queen on q attacks t; blockers wk only (bk removed) */
  static const int D[8][2] = {{1,0},{-1,0},{0,1},{0,-1},{1,1},{1,-1},{-1,1},{-1,-1}};
  for (int d = 0; d < 8; d++) {
    int f = fileof(q), r = rankof(q);
    for (int k = 0; k < 2 * (W + H); k++) {
      f += D[d][0]; r += D[d][1];
      int s = sq(f, r); if (s < 0 || s == q) break;
      if (s == t) return 1;
      if (s == wk) break;
    }
  }
  return 0;
}
static int atlas_promo(int wk, int bk, int q) { /* 1 = win, 0 = draw; Black to move after queening on q */
  int any = 0;
  for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
    if (!df && !dr) continue;
    int d = sq(fileof(bk) + df, rankof(bk) + dr); if (d < 0 || d == bk) continue;
    if (d == wk || adj(d, wk)) continue;
    if (d == q) return 0;
    if (qatt(q, d, wk)) continue;
    any = 1;
  }
  if (any) return 1;
  return qatt(q, bk, wk) ? 1 : 0;
}
static void gen(void) {
  NK = NS * NS * NS;
  for (int s = 0; s < 2; s++) { legal[s] = calloc(NK, 1); mv[s] = malloc(sizeof(int) * NK * 10); nmv[s] = calloc(NK, 1); }
  incheck = calloc(NK, 1);
  for (int wk = 0; wk < NS; wk++) for (int bk = 0; bk < NS; bk++) for (int p = 0; p < NS; p++) {
    if (wk == bk || wk == p || bk == p || adj(wk, bk)) continue;
    if (rankof(p) < 1 || rankof(p) > H - 2) continue;
    int k = kidx(wk, bk, p), chk = patt(p, bk);
    incheck[k] = chk;
    legal[1][k] = 1; legal[0][k] = !chk;
    /* white moves */
    if (legal[0][k]) {
      int *o = mv[0] + 10 * k, n = 0;
      for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
        if (!df && !dr) continue;
        int d = sq(fileof(wk) + df, rankof(wk) + dr); if (d < 0) continue;
        if (d == p || d == bk || adj(d, bk)) continue;
        int dup = 0; for (int i = 0; i < n; i++) if (o[i] == kidx(d, bk, p)) dup = 1;
        if (!dup) o[n++] = kidx(d, bk, p);
      }
      int p1 = sq(fileof(p), rankof(p) + 1);
      if (p1 != wk && p1 != bk) {
        if (rankof(p1) == H - 1) o[n++] = ATLAS ? (atlas_promo(wk, bk, p1) ? PROMO : PROMO_D) : PROMO;
        else o[n++] = kidx(wk, bk, p1);
        if (rankof(p) == 1) { int p2 = sq(fileof(p), 3); if (p2 != wk && p2 != bk) {
          if (rankof(p2) == H - 1) o[n++] = ATLAS ? (atlas_promo(wk, bk, p2) ? PROMO : PROMO_D) : PROMO;
          else o[n++] = kidx(wk, bk, p2); } }
      }
      nmv[0][k] = n;
    }
    { int *o = mv[1] + 10 * k, n = 0;
      for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
        if (!df && !dr) continue;
        int d = sq(fileof(bk) + df, rankof(bk) + dr); if (d < 0) continue;
        if (d == wk || adj(d, wk) || patt(p, d)) continue;
        int code = (d == p) ? KXP : kidx(wk, d, p);
        int dup = 0; for (int i = 0; i < n; i++) if (o[i] == code) dup = 1;
        if (!dup) o[n++] = code;
      }
      nmv[1][k] = n; }
  }
}
static unsigned char *res[2]; /* [s][t*NK+k]: 0 unknown, 1 W, 2 L */
#define R(s, t, k) res[s][(size_t)(t) * NK + (k)]
static void solve(void) {
  for (int s = 0; s < 2; s++) res[s] = calloc((size_t)NT * NK, 1);
  int changed = 1, it = 0;
  while (changed) {
    changed = 0; it++;
    for (int t = 0; t < NT; t++) for (int k = 0; k < NK; k++) {
      if (legal[0][k] && !R(0, t, k)) { /* White to move */
        int nopt = 0, win = 0, alll = 1;
        for (int i = 0; i < nmv[0][k]; i++) {
          int c = mv[0][10 * k + i]; nopt++;
          if (c == PROMO) { win = 1; alll = 0; }
          else if (c == PROMO_D) alll = 0;
          else { int r = R(1, t, c); if (r == 1) win = 1; if (r != 2) alll = 0; }
        }
        for (int i = 0; i < nTL[t]; i++) { nopt++; int r = R(1, TL[t][i], k); if (r == 1) win = 1; if (r != 2) alll = 0; }
        int v = 0;
        if (nopt == 0) v = CONV_N ? 2 : 0; else if (win) v = 1; else if (alll) v = 2;
        if (v) { R(0, t, k) = v; changed = 1; }
      }
      if (legal[1][k] && !R(1, t, k)) { /* Black to move */
        int nopt = 0, loss = 0, allw = 1;
        for (int i = 0; i < nmv[1][k]; i++) {
          int c = mv[1][10 * k + i]; nopt++;
          if (c == KXP) { if (KXPLOSS) loss = 1; allw = 0; }
          else { int r = R(0, t, c); if (r == 2) loss = 1; if (r != 1) allw = 0; }
        }
        if (!incheck[k]) for (int i = 0; i < nTR[t]; i++) { nopt++; int r = R(0, TR[t][i], k); if (r == 2) loss = 1; if (r != 1) allw = 0; }
        int v = 0;
        if (nopt == 0) v = (incheck[k] || CONV_N) ? 1 : 0; else if (loss) v = 2; else if (allw) v = 1;
        if (v) { R(1, t, k) = v; changed = 1; }
      }
    }
  }
  fprintf(stderr, "solved in %d sweeps\n", it);
}
static void sqname(int s, char *b) { sprintf(b, "%c%d", 'a' + fileof(s), rankof(s) + 1); }
int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage\n"); return 1; }
  W = atoi(argv[1]); H = atoi(argv[2]); CONV_N = argv[3][0] == 'N';
  for (int i = 4; i < argc; i++) {
    if (!strcmp(argv[i], "--kxploss")) KXPLOSS = 1;
    else if (!strcmp(argv[i], "--atlas")) ATLAS = 1;
    else if (!strcmp(argv[i], "--kvk")) { /* Lemma 1 brute force: does any K v K position leave a king without a move? */
      NS = W * H; int bad = 0;
      for (int a = 0; a < NS; a++) for (int b = 0; b < NS; b++) {
        if (a == b || adj(a, b)) continue;
        int any = 0;
        for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
          if (!df && !dr) continue; int d = sq(fileof(a) + df, rankof(a) + dr);
          if (d >= 0 && d != a && !adj(d, b) && d != b) any = 1; }
        if (!any) bad++;
      }
      printf("kvk %dx%d stuck=%d\n", W, H, bad); return 0;
    }
    else M = atoi(argv[i]);
  }
  NS = W * H; build_T(); gen(); solve();
  int nt = ATLAS ? 0 : NT;
  printf("#T");
  for (int t = 0; t < NT; t++) printf(" %s", tname[t]);
  printf("\n");
  for (int s = 0; s < 2; s++) for (int wk = 0; wk < NS; wk++) for (int bk = 0; bk < NS; bk++) for (int p = 0; p < NS; p++) {
    int k = kidx(wk, bk, p); if (!legal[s][k]) continue;
    char a[8], b[8], c[8]; sqname(wk, a); sqname(bk, b); sqname(p, c);
    printf("K%s P%s k%s %c\t", a, c, b, s ? 'b' : 'w');
    if (ATLAS) { int r = R(s, IDX0, k); putchar(r == 1 ? 'W' : r == 2 ? 'L' : 'D'); }
    else for (int t = 0; t < nt; t++) { int r = R(s, t, k); putchar(r == 1 ? 'W' : r == 2 ? 'L' : 'D'); }
    putchar('\n');
  }
  return 0;
}
