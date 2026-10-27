/* kpk2.c -- K24: independent exact tables for K+Q vs K and K+P vs K (A has the pawn or queen, D has a bare king)
 * on a W x 8-style board, flat or cylinder.  Written from the rules of kings/SPEC.md only.
 *
 * KQK is solved exactly (least fixed point of "A can force mate"; a D king that captures the queen leaves K vs K,
 * a draw; a D king with no move and not in check is stalemated, a draw).
 * KPK: A's moves are king moves, the push, the double step and the promotion to a QUEEN only (under-promotion is
 * not generated, so a KPK "win" is a sound lower bound: if the table says A wins, A wins chess; the table can
 * only miss a win that needs a rook, bishop or knight).  D has no pawn, so nothing else can differ.
 *
 * Build: cc -O2 -o kpk2 kpk2.c
 * Run:   ./kpk2 W H WRAP < queries        (WRAP 1 = cylinder, 0 = flat)
 *   query: "<dir> <ak> <dk> <p> <A|D>" with dir '+' (A's pawn moves towards rank H) or '-' (towards rank 1),
 *          squares like h5, last token the side to move; prints the query then W (A wins) or D (draw), and
 *          with "q" instead of a pawn square... no: for KQK use the keyword Q:   "Q <ak> <dk> <q> <A|D>".
 *   special: "dump <dir>" prints the whole KPK table as lines "<ak> <dk> <p> <A|D> <W|D>" for legal positions.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int W, H, WRAP, NSQ;
static inline int sqf(int s) { return s % W; }
static inline int sqr(int s) { return s / W; }
static int stepsq(int s, int df, int dr) {
  int f = sqf(s) + df, r = sqr(s) + dr;
  if (r < 0 || r >= H) return -1;
  if (WRAP) f = ((f % W) + W) % W; else if (f < 0 || f >= W) return -1;
  return r * W + f;
}
static int adj(int a, int b) {
  if (a == b) return 1;
  int dr = sqr(a) - sqr(b); if (dr < -1 || dr > 1) return 0;
  int df = sqf(a) - sqf(b); if (df < 0) df = -df;
  if (WRAP && W - df < df) df = W - df;
  return df <= 1;
}
static const int DF[8] = {0, 0, 1, -1, 1, 1, -1, -1}, DR[8] = {1, -1, 0, 0, 1, -1, 1, -1};

/* does a queen on q attack square t, with only square blk (the A king) as blocker? */
static int queen_attacks(int q, int t, int blk) {
  if (q == t) return 0;
  for (int d = 0; d < 8; d++) {
    int s = q;
    for (int k = 0; k < 2 * (W > H ? W : H); k++) {
      s = stepsq(s, DF[d], DR[d]);
      if (s < 0 || s == q) break;
      if (s == t) return 1;
      if (s == blk) break;
    }
  }
  return 0;
}

#define IDX(ak, dk, x) (((ak) * NSQ + (dk)) * NSQ + (x))
static unsigned char *KQ[2]; /* KQ[stm][..] = 1 if A wins; stm 0 = A to move, 1 = D to move */
static unsigned char *KP[2][2]; /* KP[dirIdx][stm][..] */

static int legal_kq(int stm, int ak, int dk, int q) {
  if (ak == dk || ak == q || dk == q) return 0;
  if (adj(ak, dk)) return 0;
  if (stm == 0 && queen_attacks(q, dk, ak)) return 0; /* D in check with A to move */
  return 1;
}

static void solve_kqk(void) {
  size_t n = (size_t)NSQ * NSQ * NSQ;
  KQ[0] = calloc(n, 1); KQ[1] = calloc(n, 1);
  int changed = 1;
  while (changed) {
    changed = 0;
    for (int ak = 0; ak < NSQ; ak++) for (int dk = 0; dk < NSQ; dk++) for (int q = 0; q < NSQ; q++) {
      /* A to move */
      if (!KQ[0][IDX(ak, dk, q)] && legal_kq(0, ak, dk, q)) {
        int win = 0;
        for (int d = 0; d < 8 && !win; d++) { /* king moves */
          int t = stepsq(ak, DF[d], DR[d]);
          if (t < 0 || t == q || adj(t, dk)) continue;
          if (KQ[1][IDX(t, dk, q)]) win = 1;
        }
        for (int d = 0; d < 8 && !win; d++) { /* queen moves */
          int s = q;
          for (int k = 0; k < 2 * (W > H ? W : H); k++) {
            s = stepsq(s, DF[d], DR[d]);
            if (s < 0 || s == q || s == ak || s == dk) break;
            if (KQ[1][IDX(ak, dk, s)]) { win = 1; break; }
          }
        }
        if (win) { KQ[0][IDX(ak, dk, q)] = 1; changed = 1; }
      }
      /* D to move */
      if (!KQ[1][IDX(ak, dk, q)] && legal_kq(1, ak, dk, q)) {
        int nmoves = 0, allwin = 1;
        for (int d = 0; d < 8; d++) {
          int t = stepsq(dk, DF[d], DR[d]);
          if (t < 0 || t == ak || adj(t, ak)) continue;
          if (t == q) { nmoves++; allwin = 0; continue; } /* captures the queen: K vs K, drawn */
          if (queen_attacks(q, t, ak)) continue;
          nmoves++;
          if (!KQ[0][IDX(ak, t, q)]) allwin = 0;
        }
        int win = 0;
        if (nmoves == 0) win = queen_attacks(q, dk, ak); /* mate, else stalemate */
        else win = allwin;
        if (win) { KQ[1][IDX(ak, dk, q)] = 1; changed = 1; }
      }
    }
  }
}

static int legal_kp(int dirIdx, int stm, int ak, int dk, int p) {
  int dir = dirIdx == 0 ? 1 : -1;
  if (ak == dk || ak == p || dk == p || adj(ak, dk)) return 0;
  if (sqr(p) == 0 || sqr(p) == H - 1) return 0;
  if (stm == 0) { /* D to have just moved: D must not be in check from the pawn */
    int r0 = sqr(dk) - dir;
    if (r0 >= 0 && r0 < H) for (int df = -1; df <= 1; df += 2) { int f = sqf(dk) + df; if (WRAP) f = ((f % W) + W) % W; else if (f < 0 || f >= W) continue; if (r0 * W + f == p) return 0; }
  }
  return 1;
}
static int pawn_attacks(int dirIdx, int p, int t) {
  int dir = dirIdx == 0 ? 1 : -1;
  int r0 = sqr(t) - dir;
  if (r0 != sqr(p)) return 0;
  for (int df = -1; df <= 1; df += 2) { int f = sqf(t) + df; if (WRAP) f = ((f % W) + W) % W; else if (f < 0 || f >= W) continue; if (r0 * W + f == p) return 1; }
  return 0;
}

static void solve_kpk(int dirIdx) {
  int dir = dirIdx == 0 ? 1 : -1, start = dirIdx == 0 ? 1 : H - 2, last = dirIdx == 0 ? H - 1 : 0;
  size_t n = (size_t)NSQ * NSQ * NSQ;
  KP[dirIdx][0] = calloc(n, 1); KP[dirIdx][1] = calloc(n, 1);
  unsigned char *a0 = KP[dirIdx][0], *a1 = KP[dirIdx][1];
  int changed = 1;
  while (changed) {
    changed = 0;
    for (int ak = 0; ak < NSQ; ak++) for (int dk = 0; dk < NSQ; dk++) for (int p = 0; p < NSQ; p++) {
      if (!a0[IDX(ak, dk, p)] && legal_kp(dirIdx, 0, ak, dk, p)) {
        int win = 0;
        for (int d = 0; d < 8 && !win; d++) {
          int t = stepsq(ak, DF[d], DR[d]);
          if (t < 0 || t == p || adj(t, dk)) continue;
          if (a1[IDX(t, dk, p)]) win = 1;
        }
        if (!win) {
          int one = stepsq(p, 0, dir);
          if (one >= 0 && one != ak && one != dk) {
            if (sqr(one) == last) { if (KQ[1][IDX(ak, dk, one)]) win = 1; }
            else {
              if (a1[IDX(ak, dk, one)]) win = 1;
              if (!win && sqr(p) == start) {
                int two = stepsq(one, 0, dir);
                if (two >= 0 && two != ak && two != dk) {
                  if (sqr(two) == last) { if (KQ[1][IDX(ak, dk, two)]) win = 1; }
                  else if (a1[IDX(ak, dk, two)]) win = 1;
                }
              }
            }
          }
        }
        if (win) { a0[IDX(ak, dk, p)] = 1; changed = 1; }
      }
      if (!a1[IDX(ak, dk, p)] && legal_kp(dirIdx, 1, ak, dk, p)) {
        int nmoves = 0, allwin = 1;
        for (int d = 0; d < 8; d++) {
          int t = stepsq(dk, DF[d], DR[d]);
          if (t < 0 || t == ak || adj(t, ak)) continue;
          if (t == p) { nmoves++; allwin = 0; continue; } /* captures the pawn (it is unprotected: t not adjacent to ak) */
          if (pawn_attacks(dirIdx, p, t)) continue;
          nmoves++;
          if (!a0[IDX(ak, t, p)]) allwin = 0;
        }
        int win = 0;
        if (nmoves == 0) win = pawn_attacks(dirIdx, p, dk);
        else win = allwin;
        if (win) { a1[IDX(ak, dk, p)] = 1; changed = 1; }
      }
    }
  }
}

static int psq(const char *s) {
  if (s[0] < 'a' || s[0] >= 'a' + W || s[1] < '1' || s[1] >= '1' + H) return -1;
  return (s[1] - '1') * W + (s[0] - 'a');
}
static void sqn(int s, char *o) { o[0] = 'a' + sqf(s); o[1] = '1' + sqr(s); o[2] = 0; }

int main(int argc, char **argv) {
  if (argc < 4) return 2;
  W = atoi(argv[1]); H = atoi(argv[2]); WRAP = atoi(argv[3]); NSQ = W * H;
  solve_kqk();
  solve_kpk(0); solve_kpk(1);
  { /* statistics */
    long legal = 0, won = 0;
    for (int ak = 0; ak < NSQ; ak++) for (int dk = 0; dk < NSQ; dk++) for (int q = 0; q < NSQ; q++)
      if (legal_kq(0, ak, dk, q)) { legal++; won += KQ[0][IDX(ak, dk, q)]; }
    fprintf(stderr, "[kpk2 %s:%dx%d: KQK A-to-move legal %ld, won %ld]\n", WRAP ? "cyl" : "flat", W, H, legal, won);
  }
  char line[256];
  while (fgets(line, sizeof line, stdin)) {
    char t0[16], t1[16], t2[16], t3[16], t4[16];
    size_t L = strlen(line); while (L && (line[L - 1] == '\n' || line[L - 1] == '\r')) line[--L] = 0;
    if (!strncmp(line, "dump", 4)) {
      int di = line[5] == '-' ? 1 : 0;
      for (int stm = 0; stm < 2; stm++) for (int ak = 0; ak < NSQ; ak++) for (int dk = 0; dk < NSQ; dk++) for (int p = 0; p < NSQ; p++)
        if (legal_kp(di, stm, ak, dk, p)) {
          char a[4], b[4], c[4]; sqn(ak, a); sqn(dk, b); sqn(p, c);
          printf("%s %s %s %c %c\n", a, b, c, stm ? 'D' : 'A', KP[di][stm][IDX(ak, dk, p)] ? 'W' : 'D');
        }
      continue;
    }
    if (sscanf(line, "%15s %15s %15s %15s %15s", t0, t1, t2, t3, t4) != 5) { printf("%s | bad\n", line); continue; }
    int ak = psq(t1), dk = psq(t2), x = psq(t3), stm = t4[0] == 'D';
    if (ak < 0 || dk < 0 || x < 0) { printf("%s | bad\n", line); continue; }
    if (t0[0] == 'Q') {
      if (!legal_kq(stm, ak, dk, x)) { printf("%s | X\n", line); continue; }
      printf("%s | %c\n", line, KQ[stm][IDX(ak, dk, x)] ? 'W' : 'D');
    } else {
      int di = t0[0] == '-' ? 1 : 0;
      if (!legal_kp(di, stm, ak, dk, x)) { printf("%s | X\n", line); continue; }
      printf("%s | %c\n", line, KP[di][stm][IDX(ak, dk, x)] ? 'W' : 'D');
    }
  }
  return 0;
}
