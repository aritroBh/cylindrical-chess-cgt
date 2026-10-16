/* replica.c -- independent 4-man endgame solver: K + up to two white men vs lone K
 * on an 8x8 board that is a plane, a cylinder (files a and h glued) or a torus
 * (files and ranks glued).
 *
 * Written without looking at ../egt_prototype.c, as the second implementation the
 * verification protocol asks for.
 *
 * Rules: standard moves, with wraparound where the board is glued. A slider stops
 * when its ray comes back to its own square, so there is no null move round a
 * rank. No castling, no 50-move rule, stalemate is a draw. When the black king
 * takes a white man the game continues in the smaller table; bare kings are a draw.
 *
 * Method: forward iteration on depth in plies. Pass p (odd) marks a white-to-move
 * position won in p if some white move reaches a black-to-move position lost in
 * p-1. Pass p (even) marks a black-to-move position lost in p if every black move
 * reaches a white win in at most p-1 plies (captures are read from the sub-table).
 * Only forward move generation is used; there is no un-move generator.
 *
 * Usage:
 *   replica <plane|cyl|torus> <men> [check]          solve, print statistics
 *   replica <plane|cyl|torus> <men> probe "<pos>"    value and mating line of one
 *                                                     white-to-move position
 * <men> are the white men besides the king, e.g. Q, R, BB, BN, RB, QR.
 * A position looks like "Ka1 Rb2 Bc3 kh8" (upper case white, k = black king).
 * "check" re-verifies every value against the Bellman equations and checks that
 * the table is invariant under the board's symmetries.
 */
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define ILLEGAL (-2) /* not a legal position */
#define UNK (-1)     /* not (yet) a forced mate; a draw once solving ends */
#define DRAWN (-3)   /* known draw: stalemate, or black can take into a drawn table */
#define BIT(s) (1ULL << (s))

/* ---------- geometry ---------- */

static int wrapF, wrapR;
static const char *topoName;

static int kingN[64], kingL[64][8];
static int knightN[64], knightL[64][8];
static uint64_t kingBB[64], knightBB[64];
/* dirs 0-3 orthogonal, 4-7 diagonal */
static const int DF[8] = {0, 0, 1, -1, 1, 1, -1, -1};
static const int DR[8] = {1, -1, 0, 0, 1, -1, 1, -1};
static int rayN[64][8], rayL[64][8][8];
static int8_t rayIdx[64][8][64];      /* position of target along ray, or -1 */
static uint64_t rayBefore[64][8][8];  /* squares strictly before index k */

static int step(int sq, int df, int dr) {
  int f = (sq & 7) + df, r = (sq >> 3) + dr;
  if (wrapF) f = (f + 8) & 7;
  else if (f < 0 || f > 7) return -1;
  if (wrapR) r = (r + 8) & 7;
  else if (r < 0 || r > 7) return -1;
  return r * 8 + f;
}

static void add_unique(int *n, int *list, int s) {
  for (int i = 0; i < *n; i++)
    if (list[i] == s) return;
  list[(*n)++] = s;
}

static void init_geometry(void) {
  static const int NF[8] = {1, 2, -1, -2, 1, 2, -1, -2};
  static const int NR[8] = {2, 1, 2, 1, -2, -1, -2, -1};
  memset(rayIdx, -1, sizeof rayIdx);
  for (int sq = 0; sq < 64; sq++) {
    kingN[sq] = knightN[sq] = 0;
    kingBB[sq] = knightBB[sq] = 0;
    for (int d = 0; d < 8; d++) {
      int t = step(sq, DF[d], DR[d]);
      if (t >= 0 && t != sq) add_unique(&kingN[sq], kingL[sq], t);
      t = step(sq, NF[d], NR[d]);
      if (t >= 0 && t != sq) add_unique(&knightN[sq], knightL[sq], t);
    }
    for (int i = 0; i < kingN[sq]; i++) kingBB[sq] |= BIT(kingL[sq][i]);
    for (int i = 0; i < knightN[sq]; i++) knightBB[sq] |= BIT(knightL[sq][i]);
    for (int d = 0; d < 8; d++) {
      int cur = sq;
      uint64_t before = 0;
      rayN[sq][d] = 0;
      for (;;) {
        cur = step(cur, DF[d], DR[d]);
        if (cur < 0 || cur == sq) break; /* off the board, or back home */
        int k = rayN[sq][d]++;
        rayL[sq][d][k] = cur;
        rayIdx[sq][d][cur] = (int8_t)k;
        rayBefore[sq][d][k] = before;
        before |= BIT(cur);
      }
    }
  }
}

static int dir_lo(char t) { return t == 'B' ? 4 : 0; }
static int dir_hi(char t) { return t == 'R' ? 4 : 8; }

/* does a white man of type t on `from` attack `target`, given occupancy occ? */
static inline int man_attacks(char t, int from, int target, uint64_t occ) {
  if (t == 'N') return (knightBB[from] >> target) & 1;
  for (int d = dir_lo(t); d < dir_hi(t); d++) {
    int k = rayIdx[from][d][target];
    if (k >= 0 && !(rayBefore[from][d][k] & occ)) return 1;
  }
  return 0;
}

/* ---------- tables ---------- */

typedef struct Table {
  int np;          /* number of white men besides the king: 0, 1 or 2 */
  char t[2];       /* their types */
  char name[8];    /* e.g. "RB" */
  size_t n;        /* 64^(np+2) */
  int16_t *w, *b;  /* white-to-move and black-to-move values */
  struct Table *sub[2]; /* table after black takes man i; NULL = bare kings */
  int maxw;        /* longest white win, plies */
} Table;

static inline void decode(const Table *T, size_t idx, int *wk, int *bk, int p[2]) {
  p[0] = p[1] = -1;
  if (T->np == 2) { p[1] = (int)(idx & 63); idx >>= 6; }
  if (T->np >= 1) { p[0] = (int)(idx & 63); idx >>= 6; }
  *bk = (int)(idx & 63);
  *wk = (int)(idx >> 6);
}

static inline size_t encode(int np, int wk, int bk, const int p[2]) {
  size_t i = (size_t)wk * 64 + bk;
  if (np >= 1) i = i * 64 + p[0];
  if (np == 2) i = i * 64 + p[1];
  return i;
}

/* is s attacked by white? occ must not contain the black king; man `skip` is ignored */
static inline int wattacked(const Table *T, int s, int wk, const int p[2], uint64_t occ, int skip) {
  if ((kingBB[wk] >> s) & 1) return 1;
  for (int i = 0; i < T->np; i++)
    if (i != skip && man_attacks(T->t[i], p[i], s, occ)) return 1;
  return 0;
}

/* value of the white-to-move position after black takes man `cap`, landing on n */
static inline int capture_value(const Table *T, int cap, int wk, int n, const int p[2]) {
  const Table *S = T->sub[cap];
  if (!S) return UNK; /* bare kings */
  int q[2] = {p[1 - cap], -1};
  return S->w[encode(S->np, wk, n, q)];
}

static uint64_t white_occ(const Table *T, int wk, const int p[2]) {
  uint64_t o = BIT(wk);
  for (int i = 0; i < T->np; i++) o |= BIT(p[i]);
  return o;
}

/* ---------- parallel passes ---------- */

static int NT = 8;
#define CHUNK 65536
typedef void (*RangeFn)(Table *T, size_t lo, size_t hi, int p, long *cnt);
typedef struct { Table *T; int p; RangeFn fn; long cnt; } Work;
static size_t gNext;

static void *worker(void *arg) {
  Work *wk = arg;
  long cnt = 0;
  for (;;) {
    size_t lo = __atomic_fetch_add(&gNext, CHUNK, __ATOMIC_RELAXED);
    if (lo >= wk->T->n) break;
    size_t hi = lo + CHUNK < wk->T->n ? lo + CHUNK : wk->T->n;
    wk->fn(wk->T, lo, hi, wk->p, &cnt);
  }
  wk->cnt = cnt;
  return NULL;
}

static long run_parallel(Table *T, int p, RangeFn fn) {
  pthread_t th[64];
  Work w[64];
  gNext = 0;
  for (int i = 0; i < NT; i++) {
    w[i] = (Work){T, p, fn, 0};
    pthread_create(&th[i], NULL, worker, &w[i]);
  }
  long total = 0;
  for (int i = 0; i < NT; i++) {
    pthread_join(th[i], NULL);
    total += w[i].cnt;
  }
  return total;
}

static void init_range(Table *T, size_t lo, size_t hi, int p_unused, long *cnt) {
  (void)p_unused; (void)cnt;
  for (size_t idx = lo; idx < hi; idx++) {
    int wk, bk, p[2];
    decode(T, idx, &wk, &bk, p);
    int bad = wk == bk || ((kingBB[wk] >> bk) & 1);
    for (int i = 0; i < T->np; i++) {
      if (p[i] == wk || p[i] == bk) bad = 1;
      if (i == 1 && p[1] == p[0]) bad = 1;
    }
    if (bad) { T->w[idx] = T->b[idx] = ILLEGAL; continue; }
    uint64_t occ = white_occ(T, wk, p);
    int check = wattacked(T, bk, wk, p, occ, -1);
    T->w[idx] = check ? ILLEGAL : UNK; /* side not to move may not be in check */
    int moves = 0;
    for (int j = 0; j < kingN[bk] && !moves; j++) {
      int n = kingL[bk][j];
      if (n == wk || ((kingBB[wk] >> n) & 1)) continue;
      int cap = n == p[0] ? 0 : (n == p[1] ? 1 : -1);
      if (!wattacked(T, n, wk, p, occ & ~BIT(n), cap)) moves = 1;
    }
    T->b[idx] = moves ? UNK : (check ? 0 : DRAWN);
  }
}

static void white_range(Table *T, size_t lo, size_t hi, int p, long *cnt) {
  const int np = T->np;
  for (size_t idx = lo; idx < hi; idx++) {
    if (T->w[idx] != UNK) continue;
    int wk, bk, q[2];
    decode(T, idx, &wk, &bk, q);
    uint64_t occ = white_occ(T, wk, q) | BIT(bk);
    int win = 0;
    for (int j = 0; j < kingN[wk] && !win; j++) {
      int n = kingL[wk][j];
      if (((occ >> n) & 1) || ((kingBB[bk] >> n) & 1)) continue;
      if (T->b[encode(np, n, bk, q)] >= 0) win = 1;
    }
    for (int i = 0; i < np && !win; i++) {
      int r[2] = {q[0], q[1]};
      if (T->t[i] == 'N') {
        for (int j = 0; j < knightN[q[i]] && !win; j++) {
          int n = knightL[q[i]][j];
          if ((occ >> n) & 1) continue;
          r[i] = n;
          if (T->b[encode(np, wk, bk, r)] >= 0) win = 1;
        }
      } else {
        for (int d = dir_lo(T->t[i]); d < dir_hi(T->t[i]) && !win; d++)
          for (int k = 0; k < rayN[q[i]][d] && !win; k++) {
            int s = rayL[q[i]][d][k];
            if ((occ >> s) & 1) break;
            r[i] = s;
            if (T->b[encode(np, wk, bk, r)] >= 0) win = 1;
          }
      }
    }
    if (win) { T->w[idx] = (int16_t)p; (*cnt)++; }
  }
}

static void black_range(Table *T, size_t lo, size_t hi, int p, long *cnt) {
  const int np = T->np;
  for (size_t idx = lo; idx < hi; idx++) {
    if (T->b[idx] != UNK) continue;
    int wk, bk, q[2];
    decode(T, idx, &wk, &bk, q);
    uint64_t occ = white_occ(T, wk, q); /* black king lifted off its square */
    int allwon = 1, drawn = 0;
    for (int j = 0; j < kingN[bk]; j++) {
      int n = kingL[bk][j];
      if (n == wk || ((kingBB[wk] >> n) & 1)) continue;
      int cap = n == q[0] ? 0 : (n == q[1] ? 1 : -1);
      int v;
      if (cap < 0) {
        if (wattacked(T, n, wk, q, occ, -1)) continue;
        v = T->w[encode(np, wk, n, q)];
      } else {
        if (wattacked(T, n, wk, q, occ & ~BIT(n), cap)) continue;
        v = capture_value(T, cap, wk, n, q);
        if (v < 0) { drawn = 1; break; }
      }
      if (v < 0 || v > p - 1) { allwon = 0; break; }
    }
    if (drawn) T->b[idx] = DRAWN;
    else if (allwon) { T->b[idx] = (int16_t)p; (*cnt)++; }
  }
}

/* ---------- table construction ---------- */

static Table *cache[32];
static int ncache;
static int verbose = 1;

static Table *get_table(const char *men);

static Table *solve_table(const char *men) {
  Table *T = calloc(1, sizeof *T);
  T->np = (int)strlen(men);
  memcpy(T->t, men, T->np);
  strcpy(T->name, men);
  T->n = (size_t)1 << (6 * (T->np + 2));
  T->w = malloc(T->n * sizeof(int16_t));
  T->b = malloc(T->n * sizeof(int16_t));
  int maxsub = 0;
  for (int i = 0; i < T->np; i++) {
    char rest[3] = {0};
    if (T->np == 2) rest[0] = men[1 - i];
    T->sub[i] = rest[0] ? get_table(rest) : NULL;
    if (T->sub[i] && T->sub[i]->maxw > maxsub) maxsub = T->sub[i]->maxw;
  }
  run_parallel(T, 0, init_range);
  long prev = -1;
  int p;
  for (p = 1;; p++) {
    long c = run_parallel(T, p, (p & 1) ? white_range : black_range);
    if (c > 0) {
      if (p & 1) T->maxw = p;
    } else if (prev == 0 && p > maxsub + 2) break;
    prev = c;
  }
  /* DRAWN only marks some draws early (which ones depends on scan order); merge it */
  for (size_t i = 0; i < T->n; i++)
    if (T->b[i] == DRAWN) T->b[i] = UNK;
  if (verbose) fprintf(stderr, "[%s %s: solved in %d passes, longest win %d plies]\n",
                       topoName, men, p, T->maxw);
  return T;
}

static Table *get_table(const char *men) {
  for (int i = 0; i < ncache; i++)
    if (!strcmp(cache[i]->name, men)) return cache[i];
  Table *T = solve_table(men);
  cache[ncache++] = T;
  return T;
}

/* ---------- printing ---------- */

static void sqname(int s, char *out) {
  out[0] = (char)('a' + (s & 7));
  out[1] = (char)('1' + (s >> 3));
  out[2] = 0;
}

static void pos_string(const Table *T, size_t idx, char *out) {
  int wk, bk, p[2];
  char a[3];
  decode(T, idx, &wk, &bk, p);
  sqname(wk, a);
  out += sprintf(out, "K%s", a);
  for (int i = 0; i < T->np; i++) {
    sqname(p[i], a);
    out += sprintf(out, " %c%s", T->t[i], a);
  }
  sqname(bk, a);
  sprintf(out, " k%s", a);
}

/* ---------- generic move lists (used by checks and lines, not by the solver) ---------- */

typedef struct { const Table *T; size_t idx; char txt[24]; } Child;
static int wantText; /* move text only for printed lines; sprintf is slow */

static int gen_white(const Table *T, size_t idx, Child *out) {
  int wk, bk, p[2], m = 0;
  decode(T, idx, &wk, &bk, p);
  uint64_t occ = white_occ(T, wk, p) | BIT(bk);
  char a[3], c[3];
  for (int j = 0; j < kingN[wk]; j++) {
    int n = kingL[wk][j];
    if (((occ >> n) & 1) || ((kingBB[bk] >> n) & 1)) continue;
    out[m].T = T;
    out[m].idx = encode(T->np, n, bk, p);
    sqname(wk, a); sqname(n, c);
    if (wantText) sprintf(out[m].txt, "K%s-%s", a, c);
    m++;
  }
  for (int i = 0; i < T->np; i++) {
    uint64_t dest = 0;
    if (T->t[i] == 'N') dest = knightBB[p[i]] & ~occ;
    else
      for (int d = dir_lo(T->t[i]); d < dir_hi(T->t[i]); d++)
        for (int k = 0; k < rayN[p[i]][d]; k++) {
          int s = rayL[p[i]][d][k];
          if ((occ >> s) & 1) break;
          dest |= BIT(s);
        }
    for (int s = 0; s < 64; s++)
      if ((dest >> s) & 1) {
        int r[2] = {p[0], p[1]};
        r[i] = s;
        out[m].T = T;
        out[m].idx = encode(T->np, wk, bk, r);
        sqname(p[i], a); sqname(s, c);
        if (wantText) sprintf(out[m].txt, "%c%s-%s", T->t[i], a, c);
        m++;
      }
  }
  return m;
}

/* children of a black-to-move position; T == NULL marks bare kings */
static int gen_black(const Table *T, size_t idx, Child *out) {
  int wk, bk, p[2], m = 0;
  decode(T, idx, &wk, &bk, p);
  uint64_t occ = white_occ(T, wk, p);
  char a[3], c[3];
  for (int j = 0; j < kingN[bk]; j++) {
    int n = kingL[bk][j];
    if (n == wk || ((kingBB[wk] >> n) & 1)) continue;
    int cap = n == p[0] ? 0 : (n == p[1] ? 1 : -1);
    if (wattacked(T, n, wk, p, cap < 0 ? occ : occ & ~BIT(n), cap)) continue;
    sqname(bk, a); sqname(n, c);
    if (cap < 0) {
      out[m].T = T;
      out[m].idx = encode(T->np, wk, n, p);
      if (wantText) sprintf(out[m].txt, "k%s-%s", a, c);
    } else {
      int q[2] = {p[1 - cap], -1};
      out[m].T = T->sub[cap];
      out[m].idx = T->sub[cap] ? encode(T->sub[cap]->np, wk, n, q) : 0;
      if (wantText) sprintf(out[m].txt, "kx%c%s", T->t[cap], c);
    }
    m++;
  }
  return m;
}

static int child_wvalue(const Child *c) { return c->T ? c->T->w[c->idx] : UNK; }

/* ---------- checks ---------- */

static long nerr;
static pthread_mutex_t errmu = PTHREAD_MUTEX_INITIALIZER;

static void report_err(const Table *T, size_t idx, const char *side, const char *why) {
  pthread_mutex_lock(&errmu);
  if (nerr++ < 10) {
    char buf[64];
    pos_string(T, idx, buf);
    fprintf(stderr, "CHECK FAILED %s %s [%s] %s: %s w=%d b=%d\n", topoName, T->name, buf,
            side, why, T->w[idx], T->b[idx]);
  }
  pthread_mutex_unlock(&errmu);
}

/* every value must satisfy the minimax (Bellman) equations */
static void bellman_range(Table *T, size_t lo, size_t hi, int p_unused, long *cnt) {
  (void)p_unused; (void)cnt;
  Child ch[64];
  for (size_t idx = lo; idx < hi; idx++) {
    int v = T->w[idx];
    if (v != ILLEGAL) {
      int m = gen_white(T, idx, ch), best = 1 << 20;
      for (int i = 0; i < m; i++) {
        int b = ch[i].T->b[ch[i].idx];
        if (b == ILLEGAL) report_err(T, idx, "wtm", "illegal child");
        if (b >= 0 && b < best) best = b;
      }
      if (v >= 0 && best != v - 1) report_err(T, idx, "wtm", "win value");
      if (v < 0 && best != 1 << 20) report_err(T, idx, "wtm", "missed win");
    }
    v = T->b[idx];
    if (v == ILLEGAL) continue;
    int wk, bk, p[2];
    decode(T, idx, &wk, &bk, p);
    int check = wattacked(T, bk, wk, p, white_occ(T, wk, p), -1);
    int m = gen_black(T, idx, ch);
    if (m == 0) {
      if ((check && v != 0) || (!check && v >= 0)) report_err(T, idx, "btm", "mate/stalemate");
      continue;
    }
    int allwon = 1, worst = -1;
    for (int i = 0; i < m; i++) {
      int w = child_wvalue(&ch[i]);
      if (ch[i].T && w == ILLEGAL) report_err(T, idx, "btm", "illegal child");
      if (w < 0) allwon = 0;
      else if (w > worst) worst = w;
    }
    if (v >= 0 && !(allwon && worst == v - 1)) report_err(T, idx, "btm", "loss value");
    if (v < 0 && allwon) report_err(T, idx, "btm", "missed loss");
  }
}

/* symmetry generators of the board, as maps on squares */
static int sym_apply(int g, int s) {
  int f = s & 7, r = s >> 3;
  switch (g) {
    case 0: f = 7 - f; break;       /* mirror files */
    case 1: r = 7 - r; break;       /* mirror ranks */
    case 2: { int t = f; f = r; r = t; } break; /* transpose */
    case 3: f = (f + 1) & 7; break; /* shift files */
    case 4: r = (r + 1) & 7; break; /* shift ranks */
  }
  return r * 8 + f;
}

static int gSym;
static void sym_range(Table *T, size_t lo, size_t hi, int p_unused, long *cnt) {
  (void)p_unused; (void)cnt;
  for (size_t idx = lo; idx < hi; idx++) {
    int wk, bk, p[2], q[2] = {-1, -1};
    decode(T, idx, &wk, &bk, p);
    for (int i = 0; i < T->np; i++) q[i] = sym_apply(gSym, p[i]);
    size_t j = encode(T->np, sym_apply(gSym, wk), sym_apply(gSym, bk), q);
    if (T->w[idx] != T->w[j]) report_err(T, idx, "wtm", "symmetry");
    if (T->b[idx] != T->b[j]) report_err(T, idx, "btm", "symmetry");
  }
}

static void run_checks(Table *T) {
  nerr = 0;
  run_parallel(T, 0, bellman_range);
  int gens[4], ng = 0;
  if (!wrapF && !wrapR) { gens[ng++] = 0; gens[ng++] = 1; gens[ng++] = 2; }
  else if (wrapF && !wrapR) { gens[ng++] = 0; gens[ng++] = 1; gens[ng++] = 3; }
  else { gens[ng++] = 0; gens[ng++] = 2; gens[ng++] = 3; gens[ng++] = 4; }
  for (int g = 0; g < ng; g++) {
    gSym = gens[g];
    run_parallel(T, 0, sym_range);
  }
  printf("checks %s %s: %s (%ld errors)\n", topoName, T->name, nerr ? "FAILED" : "passed", nerr);
}

/* ---------- statistics ---------- */

static int sqcolor(int s) { return ((s & 7) + (s >> 3)) & 1; }

/* subset: 0 all, 1 bishops on opposite colours, 2 bishops on the same colour */
static void stats(const Table *T, int subset, const char *label) {
  long legal = 0, won = 0, blegal = 0, blost = 0;
  int maxw = -1, maxb = -1;
  size_t argw = 0, argb = 0;
  for (size_t idx = 0; idx < T->n; idx++) {
    if (subset) {
      int wk, bk, p[2];
      decode(T, idx, &wk, &bk, p);
      int opp = sqcolor(p[0]) != sqcolor(p[1]);
      if ((subset == 1) != opp) continue;
    }
    int v = T->w[idx];
    if (v != ILLEGAL) {
      legal++;
      if (v >= 0) {
        won++;
        if (v > maxw) { maxw = v; argw = idx; }
      }
    }
    v = T->b[idx];
    if (v != ILLEGAL) {
      blegal++;
      if (v >= 0) {
        blost++;
        if (v > maxb) { maxb = v; argb = idx; }
      }
    }
  }
  char pw[64] = "-", pb[64] = "-";
  if (maxw >= 0) pos_string(T, argw, pw);
  if (maxb >= 0) pos_string(T, argb, pb);
  printf("%-6s K%sK %-9s wtm legal %9ld won %9ld (%8.4f%%) maxDTM %3d moves  e.g. %s w\n",
         topoName, T->name, label, legal, won, legal ? 100.0 * won / legal : 0.0,
         maxw >= 0 ? (maxw + 1) / 2 : 0, pw);
  printf("%-6s K%sK %-9s btm legal %9ld lost %8ld (%8.4f%%) maxDTM %3d moves  e.g. %s b\n",
         topoName, T->name, label, blegal, blost, blegal ? 100.0 * blost / blegal : 0.0,
         maxb >= 0 ? maxb / 2 : 0, pb);
}

/* ---------- probing ---------- */

static int parse_square(const char *s) {
  if (s[0] < 'a' || s[0] > 'h' || s[1] < '1' || s[1] > '8') return -1;
  return (s[1] - '1') * 8 + (s[0] - 'a');
}

static int parse_pos(const Table *T, const char *str, size_t *idx) {
  int wk = -1, bk = -1, p[2] = {-1, -1}, used[2] = {0, 0};
  char buf[256];
  snprintf(buf, sizeof buf, "%s", str);
  for (char *tok = strtok(buf, " "); tok; tok = strtok(NULL, " ")) {
    int s = parse_square(tok + 1);
    if (s < 0) return 0;
    if (tok[0] == 'K') wk = s;
    else if (tok[0] == 'k') bk = s;
    else {
      int i;
      for (i = 0; i < T->np; i++)
        if (!used[i] && T->t[i] == tok[0]) break;
      if (i == T->np) return 0;
      used[i] = 1;
      p[i] = s;
    }
  }
  if (wk < 0 || bk < 0) return 0;
  for (int i = 0; i < T->np; i++)
    if (!used[i]) return 0;
  *idx = encode(T->np, wk, bk, p);
  return 1;
}

/* print a mating line: white takes a fastest mate, black a slowest */
static void print_line(const Table *T, size_t idx) {
  Child ch[64];
  wantText = 1;
  int move = 1;
  for (;;) {
    int v = T->w[idx];
    if (v < 0) { printf(" (draw)\n"); return; }
    int m = gen_white(T, idx, ch), k;
    for (k = 0; k < m; k++)
      if (ch[k].T->b[ch[k].idx] == v - 1) break;
    printf(" %d.%s", move++, ch[k].txt);
    idx = ch[k].idx;
    m = gen_black(T, idx, ch);
    if (m == 0) { printf("#\n"); return; }
    int best = -1, bi = 0;
    for (k = 0; k < m; k++) {
      int w = child_wvalue(&ch[k]);
      if (w > best) { best = w; bi = k; }
    }
    printf(" %s", ch[bi].txt);
    T = ch[bi].T;
    idx = ch[bi].idx;
  }
}

int main(int argc, char **argv) {
  if (argc < 3) {
    fprintf(stderr, "usage: %s <plane|cyl|torus> <men> [check | probe \"<pos>\"]\n", argv[0]);
    return 2;
  }
  topoName = argv[1];
  if (!strcmp(topoName, "plane")) wrapF = wrapR = 0;
  else if (!strcmp(topoName, "cyl")) { wrapF = 1; wrapR = 0; }
  else if (!strcmp(topoName, "torus")) wrapF = wrapR = 1;
  else { fprintf(stderr, "unknown board %s\n", topoName); return 2; }
  const char *men = argv[2];
  if (strlen(men) < 1 || strlen(men) > 2 || strspn(men, "QRBN") != strlen(men)) {
    fprintf(stderr, "men must be one or two of Q R B N\n");
    return 2;
  }
  long ncpu = sysconf(_SC_NPROCESSORS_ONLN);
  NT = ncpu > 0 ? (ncpu > 64 ? 64 : (int)ncpu) : 8;
  init_geometry();
  Table *T = get_table(men);

  if (argc >= 5 && !strcmp(argv[3], "probe")) {
    size_t idx;
    if (!parse_pos(T, argv[4], &idx)) { fprintf(stderr, "bad position\n"); return 2; }
    int v = T->w[idx];
    char buf[64];
    pos_string(T, idx, buf);
    if (v == ILLEGAL) printf("%s w: illegal\n", buf);
    else if (v < 0) printf("%s w: draw\n", buf);
    else {
      printf("%s w: white mates in %d (%d plies)\n", buf, (v + 1) / 2, v);
      print_line(T, idx);
    }
    return 0;
  }
  stats(T, 0, "all");
  if (T->np == 2 && T->t[0] == 'B' && T->t[1] == 'B') {
    stats(T, 1, "opp-col");
    stats(T, 2, "same-col");
  }
  if (argc >= 4 && !strcmp(argv[3], "check")) {
    for (int i = 0; i < ncache; i++) run_checks(cache[i]);
  }
  return 0;
}
