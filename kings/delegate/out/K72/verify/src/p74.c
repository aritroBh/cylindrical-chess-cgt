/* p74.c -- K74 referee's own solver of the promotion game P on the flat 8x8 board.
 *
 * Written for the K74 referee from the rules only (kings/SPEC.md, LOOPY.md Definition 1.5): kings and pawns, the
 * first promotion ends the game as a win for the promoter, checkmate loses, stalemate and infinite play are draws,
 * double steps and en passant.  It shares no code with pk.cpp, ref3m.cpp or any other solver of the project.
 *
 * Method.  A pawn configuration (White pawn set, Black pawn set) is a "config".  Pawn moves and captures leave the
 * config and never come back, so configs are solved in an order where every successor config is already solved:
 * fewer pawns first, and among equal counts the configs with more pawn progress first.  Inside a config only king
 * moves remain; they are solved by retrograde analysis with move counters, processed in order of plies to the end
 * (bucket queue), so that the optional depth is the minimax number of plies to the first decisive event.
 * Positions with an e.p. right are never stored: they are evaluated by one ply over stored positions.
 *
 * Input (stdin): one position per line, "Kd4 kb4 Pb6 Pc2 pb7 ... b -" (piece list, side to move w/b, e.p. square
 * or -) or a FEN board field followed by the side to move.  Blank lines and lines starting with # are ignored.
 * Output: one line per position: the position and its value in White's view (W, L, D), with -d also the depth.
 * Flags: -c only count the configs and exit; -d keep depths (needs 16 KB more per config), -m print every legal move and its value, -l N print a line
 * of up to N plies (winner shortest, loser longest; in a draw the first drawing move, a pawn move if there is one).
 * Memory: the program counts the configs first and exits with status 3 if its tables would pass 2.0e9 bytes.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef uint64_t u64;
#define BIT(s) (1ULL << (s))
#define FILEA 0x0101010101010101ULL
#define FILEH 0x8080808080808080ULL
#define WHITE 0
#define BLACK 1
#define MAXD 4000
#define LIMIT 2000000000ULL

static u64 KA[64];
static int dflag = 0;

static u64 watt(u64 w) { return ((w & ~FILEA) << 7) | ((w & ~FILEH) << 9); }
static u64 batt(u64 b) { return ((b & ~FILEA) >> 9) | ((b & ~FILEH) >> 7); }

/* ---------------- config hash ---------------- */
typedef struct { u64 w, b; } Cfg;
static Cfg *keys; static int32_t *slot; static u64 hcap; static int32_t ncfg = 0, maxcfg;
static uint8_t *vals;    /* ncfg * 2048 bytes: 2 bits per position, 0 D, 1 W, 2 L, 3 illegal */
static uint16_t *deps;   /* ncfg * 8192 (only with -d) */
static uint8_t *solved;
static Cfg *list;

static u64 hh(u64 w, u64 b) { u64 x = w * 0x9E3779B97F4A7C15ULL ^ (b + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL; x ^= x >> 29; return x; }
static int32_t find(u64 w, u64 b) {
  u64 h = hh(w, b) & (hcap - 1);
  while (slot[h] >= 0) { if (keys[slot[h]].w == w && keys[slot[h]].b == b) return slot[h]; h = (h + 1) & (hcap - 1); }
  return -1;
}
static int32_t insert(u64 w, u64 b) {
  u64 h = hh(w, b) & (hcap - 1);
  while (slot[h] >= 0) { if (keys[slot[h]].w == w && keys[slot[h]].b == b) return -1; h = (h + 1) & (hcap - 1); }
  if (ncfg >= maxcfg) { fprintf(stderr, "too many configs (> %d)\n", maxcfg); exit(3); }
  keys[ncfg].w = w; keys[ncfg].b = b; slot[h] = ncfg; return ncfg++;
}

/* ---------------- moves ---------------- */
enum { INCONF, EXIT, PROMO };
typedef struct { int type; u64 w, b; int wk, bk, ep; int from, to, cap; char piece; } Move;

/* all legal moves of stm; ep = e.p. target square or -1 */
static int gen(u64 w, u64 b, int wk, int bk, int stm, int ep, Move *mv) {
  int n = 0; u64 occ = w | b | BIT(wk) | BIT(bk);
  if (stm == WHITE) {
    int chk = (batt(b) & BIT(wk)) != 0;
    u64 t = KA[wk] & ~w & ~KA[bk];
    while (t) { int s = __builtin_ctzll(t); t &= t - 1;
      u64 nb = b & ~BIT(s);
      if (batt(nb) & BIT(s)) continue;
      Move m = { nb == b ? INCONF : EXIT, w, nb, s, bk, -1, wk, s, nb != b, 'K' }; mv[n++] = m; }
    u64 p = w;
    while (p) { int s = __builtin_ctzll(p); p &= p - 1; int r = s >> 3, f = s & 7;
      int u = s + 8;
      if (!(occ & BIT(u)) && !chk) {
        if ((u >> 3) == 7) { Move m = { PROMO, 0, 0, wk, bk, -1, s, u, 0, 'P' }; mv[n++] = m; }
        else { Move m = { EXIT, (w & ~BIT(s)) | BIT(u), b, wk, bk, -1, s, u, 0, 'P' }; mv[n++] = m;
          if (r == 1 && !(occ & BIT(s + 16))) { Move m2 = { EXIT, (w & ~BIT(s)) | BIT(s + 16), b, wk, bk, u, s, s + 16, 0, 'P' }; mv[n++] = m2; } } }
      for (int d = 7; d <= 9; d += 2) {
        if ((d == 7 && f == 0) || (d == 9 && f == 7)) continue;
        int c = s + d;
        if (b & BIT(c)) { u64 nb = b & ~BIT(c); if (batt(nb) & BIT(wk)) continue;
          if ((c >> 3) == 7) { Move m = { PROMO, 0, 0, wk, bk, -1, s, c, 1, 'P' }; mv[n++] = m; }
          else { Move m = { EXIT, (w & ~BIT(s)) | BIT(c), nb, wk, bk, -1, s, c, 1, 'P' }; mv[n++] = m; } }
        else if (c == ep) { u64 nb = b & ~BIT(ep - 8); if (batt(nb) & BIT(wk)) continue;
          Move m = { EXIT, (w & ~BIT(s)) | BIT(c), nb, wk, bk, -1, s, c, 1, 'P' }; mv[n++] = m; } } }
  } else {
    int chk = (watt(w) & BIT(bk)) != 0;
    u64 t = KA[bk] & ~b & ~KA[wk];
    while (t) { int s = __builtin_ctzll(t); t &= t - 1;
      u64 nw = w & ~BIT(s);
      if (watt(nw) & BIT(s)) continue;
      Move m = { nw == w ? INCONF : EXIT, nw, b, wk, s, -1, bk, s, nw != w, 'K' }; mv[n++] = m; }
    u64 p = b;
    while (p) { int s = __builtin_ctzll(p); p &= p - 1; int r = s >> 3, f = s & 7;
      int u = s - 8;
      if (!(occ & BIT(u)) && !chk) {
        if ((u >> 3) == 0) { Move m = { PROMO, 0, 0, wk, bk, -1, s, u, 0, 'P' }; mv[n++] = m; }
        else { Move m = { EXIT, w, (b & ~BIT(s)) | BIT(u), wk, bk, -1, s, u, 0, 'P' }; mv[n++] = m;
          if (r == 6 && !(occ & BIT(s - 16))) { Move m2 = { EXIT, w, (b & ~BIT(s)) | BIT(s - 16), wk, bk, u, s, s - 16, 0, 'P' }; mv[n++] = m2; } } }
      for (int d = 7; d <= 9; d += 2) {
        if ((d == 9 && f == 0) || (d == 7 && f == 7)) continue;
        int c = s - d;
        if (w & BIT(c)) { u64 nw = w & ~BIT(c); if (watt(nw) & BIT(bk)) continue;
          if ((c >> 3) == 0) { Move m = { PROMO, 0, 0, wk, bk, -1, s, c, 1, 'P' }; mv[n++] = m; }
          else { Move m = { EXIT, nw, (b & ~BIT(s)) | BIT(c), wk, bk, -1, s, c, 1, 'P' }; mv[n++] = m; } }
        else if (c == ep) { u64 nw = w & ~BIT(ep + 8); if (watt(nw) & BIT(bk)) continue;
          Move m = { EXIT, nw, (b & ~BIT(s)) | BIT(c), wk, bk, -1, s, c, 1, 'P' }; mv[n++] = m; } } }
  }
  return n;
}

static int legalpos(u64 w, u64 b, int wk, int bk, int stm) {
  if (wk == bk) return 0;
  if ((w | b) & (BIT(wk) | BIT(bk))) return 0;
  if (KA[wk] & BIT(bk)) return 0;
  if ((w | b) & 0xFF000000000000FFULL) return 0;          /* no pawn on rank 1 or 8 */
  if (stm == WHITE && (watt(w) & BIT(bk))) return 0;       /* side not to move in check */
  if (stm == BLACK && (batt(b) & BIT(wk))) return 0;
  return 1;
}

/* e.p. right exists for real only if a capture is possible */
static int eplive(u64 w, u64 b, int stm, int ep) {
  if (ep < 0) return 0;
  if (stm == WHITE) return (batt(BIT(ep)) & w) != 0;   /* White pawns that attack ep */
  return (watt(BIT(ep)) & b) != 0;
}

/* value in White's view: 1 W, 2 L, 0 D; *dep plies to the decisive event */
static int value(u64 w, u64 b, int wk, int bk, int stm, int ep, int *dep);

static Cfg cw[256]; static int32_t ci[256];   /* small cache of config lookups */
static int tablev(u64 w, u64 b, int wk, int bk, int stm, int *dep) {
  unsigned h = (unsigned)((w ^ (b * 31) ^ (w >> 29) ^ (b >> 17)) & 255);
  int32_t c;
  if (ci[h] >= 0 && cw[h].w == w && cw[h].b == b) c = ci[h];
  else { c = find(w, b); cw[h].w = w; cw[h].b = b; ci[h] = c; }
  if (c < 0 || !solved[c]) { fprintf(stderr, "internal: config not solved\n"); exit(4); }
  int idx = (stm << 12) | (wk << 6) | bk;
  int v = (vals[(size_t)c * 2048 + (idx >> 2)] >> (2 * (idx & 3))) & 3;
  if (v == 3) { fprintf(stderr, "internal: illegal successor\n"); exit(4); }
  *dep = dflag ? deps[(size_t)c * 8192 + idx] : 0;
  return v;
}

/* one-ply evaluation (used for positions with a live e.p. right, and for -m) */
static int ply1(u64 w, u64 b, int wk, int bk, int stm, int ep, int *dep) {
  Move mv[64]; int n = gen(w, b, wk, bk, stm, ep, mv);
  int win = stm == WHITE ? 1 : 2, loss = stm == WHITE ? 2 : 1;
  if (n == 0) { *dep = 0; int chk = stm == WHITE ? (batt(b) & BIT(wk)) != 0 : (watt(w) & BIT(bk)) != 0; return chk ? loss : 0; }
  int best = loss, bd = -1, wd = 1 << 30, ld = 0;
  for (int i = 0; i < n; i++) { int d, v;
    if (mv[i].type == PROMO) { v = win; d = 0; }
    else v = value(mv[i].w, mv[i].b, mv[i].wk, mv[i].bk, 1 - stm, mv[i].ep, &d);
    if (v == win) { best = win; if (d + 1 < wd) wd = d + 1; }
    else if (v == 0) { if (best != win) best = 0; }
    else { if (d + 1 > ld) ld = d + 1; } }
  (void)bd;
  *dep = best == win ? wd : best == loss ? ld : 0;
  return best;
}

static int value(u64 w, u64 b, int wk, int bk, int stm, int ep, int *dep) {
  if (eplive(w, b, stm, ep)) return ply1(w, b, wk, bk, stm, ep, dep);
  return tablev(w, b, wk, bk, stm, dep);
}

/* ---------------- config enumeration (a superset of the reachable configs) ---------------- */
static void enumerate(void) {
  for (int32_t i = 0; i < ncfg; i++) {
    u64 w = keys[i].w, b = keys[i].b, occ = w | b;
    u64 p = w;
    while (p) { int s = __builtin_ctzll(p); p &= p - 1; int f = s & 7, u = s + 8;
      if (!(occ & BIT(u)) && (u >> 3) < 7) { insert((w & ~BIT(s)) | BIT(u), b);
        if ((s >> 3) == 1 && !(occ & BIT(s + 16))) {
          u64 w2 = (w & ~BIT(s)) | BIT(s + 16); insert(w2, b);
          u64 q = b & ((BIT(u) & ~FILEA) << 7 | (BIT(u) & ~FILEH) << 9);   /* Black pawns that attack u */
          while (q) { int bs = __builtin_ctzll(q); q &= q - 1; insert(w2 & ~BIT(s + 16), (b & ~BIT(bs)) | BIT(u)); } } }
      for (int d = 7; d <= 9; d += 2) { if ((d == 7 && f == 0) || (d == 9 && f == 7)) continue; int c = s + d;
        if ((b & BIT(c)) && (c >> 3) < 7) insert((w & ~BIT(s)) | BIT(c), b & ~BIT(c)); } }
    p = b;
    while (p) { int s = __builtin_ctzll(p); p &= p - 1; int f = s & 7, u = s - 8;
      if (!(occ & BIT(u)) && (u >> 3) > 0) { insert(w, (b & ~BIT(s)) | BIT(u));
        if ((s >> 3) == 6 && !(occ & BIT(s - 16))) {
          u64 b2 = (b & ~BIT(s)) | BIT(s - 16); insert(w, b2);
          u64 q = w & ((BIT(u) & ~FILEA) >> 9 | (BIT(u) & ~FILEH) >> 7);
          while (q) { int ws = __builtin_ctzll(q); q &= q - 1; insert((w & ~BIT(ws)) | BIT(u), b2 & ~BIT(s - 16)); } } }
      for (int d = 7; d <= 9; d += 2) { if ((d == 9 && f == 0) || (d == 7 && f == 7)) continue; int c = s - d;
        if ((w & BIT(c)) && (c >> 3) > 0) insert(w & ~BIT(c), (b & ~BIT(s)) | BIT(c)); } }
    /* king captures: an enemy pawn not guarded by another enemy pawn */
    p = b; while (p) { int s = __builtin_ctzll(p); p &= p - 1; if (!(batt(b & ~BIT(s)) & BIT(s))) insert(w, b & ~BIT(s)); }
    p = w; while (p) { int s = __builtin_ctzll(p); p &= p - 1; if (!(watt(w & ~BIT(s)) & BIT(s))) insert(w & ~BIT(s), b); }
  }
}

static int progress(Cfg c) {
  int s = 0; u64 p = c.w; while (p) { s += __builtin_ctzll(p) >> 3; p &= p - 1; }
  p = c.b; while (p) { s += 7 - (__builtin_ctzll(p) >> 3); p &= p - 1; }
  return s;
}
static int cmpcfg(const void *x, const void *y) {
  const Cfg *a = x, *b = y;
  int na = __builtin_popcountll(a->w) + __builtin_popcountll(a->b), nb = __builtin_popcountll(b->w) + __builtin_popcountll(b->b);
  if (na != nb) return na - nb;
  return progress(*b) - progress(*a);
}

/* ---------------- retrograde inside one config ---------------- */
static uint8_t tv[8192], fin[8192], cnt[8192], bex[8192];  /* tv: 0 none, 1 win for mover, 2 loss for mover, 3 draw */
static uint16_t td[8192], lexd[8192];
static int32_t nsucc[8192], succ[8192][8], rstart[8193], radj[8192 * 8];
static int32_t *pool_idx, *pool_next, head[MAXD + 1], npool;

static void push(int idx, int d) {
  if (d > MAXD) { fprintf(stderr, "depth overflow\n"); exit(4); }
  pool_idx[npool] = idx; pool_next[npool] = head[d]; head[d] = npool++;
}

static void solve(int32_t c) {
  u64 w = keys[c].w, b = keys[c].b; Move mv[64];
  npool = 0; for (int d = 0; d <= MAXD; d++) head[d] = -1;
  memset(fin, 0, sizeof fin); memset(tv, 0, sizeof tv);
  for (int idx = 0; idx < 8192; idx++) {
    int stm = idx >> 12, wk = (idx >> 6) & 63, bk = idx & 63; nsucc[idx] = 0;
    if (!legalpos(w, b, wk, bk, stm)) { tv[idx] = 255; fin[idx] = 1; continue; }
    int n = gen(w, b, wk, bk, stm, -1, mv);
    int win = stm == WHITE ? 1 : 2;
    if (n == 0) { int chk = stm == WHITE ? (batt(b) & BIT(wk)) != 0 : (watt(w) & BIT(bk)) != 0;
      tv[idx] = chk ? 2 : 3; td[idx] = 0; if (chk) push(idx, 0); else fin[idx] = 1; continue; }
    int haswin = 0, wd = 1 << 30, hasdraw = 0, ld = 0;
    for (int i = 0; i < n; i++) {
      if (mv[i].type == PROMO) { haswin = 1; if (1 < wd) wd = 1; continue; }
      if (mv[i].type == INCONF) { succ[idx][nsucc[idx]++] = (((1 - stm) << 12) | (mv[i].wk << 6) | mv[i].bk); continue; }
      int d, v = value(mv[i].w, mv[i].b, mv[i].wk, mv[i].bk, 1 - stm, mv[i].ep, &d);
      if (v == win) { haswin = 1; if (d + 1 < wd) wd = d + 1; }
      else if (v == 0) hasdraw = 1;
      else if (d + 1 > ld) ld = d + 1; }
    cnt[idx] = nsucc[idx]; bex[idx] = hasdraw; lexd[idx] = ld;
    if (haswin) { tv[idx] = 1; td[idx] = wd; push(idx, wd); }
    else if (nsucc[idx] == 0) { if (hasdraw) { tv[idx] = 3; fin[idx] = 1; } else { tv[idx] = 2; td[idx] = ld; push(idx, ld); } }
  }
  /* reverse adjacency */
  memset(rstart, 0, sizeof rstart);
  for (int i = 0; i < 8192; i++) for (int k = 0; k < nsucc[i]; k++) rstart[succ[i][k] + 1]++;
  for (int i = 0; i < 8192; i++) rstart[i + 1] += rstart[i];
  static int32_t fillp[8192]; memcpy(fillp, rstart, sizeof fillp);
  for (int i = 0; i < 8192; i++) for (int k = 0; k < nsucc[i]; k++) radj[fillp[succ[i][k]]++] = i;
  for (int d = 0; d <= MAXD; d++) {
    while (head[d] >= 0) {
      int e = head[d]; head[d] = pool_next[e]; int idx = pool_idx[e];
      if (fin[idx] || td[idx] != d) continue;
      fin[idx] = 1;
      for (int k = rstart[idx]; k < rstart[idx + 1]; k++) { int q = radj[k]; if (fin[q]) continue;
        if (tv[idx] == 2) { if (tv[q] != 1 || td[q] > d + 1) { tv[q] = 1; td[q] = d + 1; push(q, d + 1); } }
        else { if (--cnt[q] == 0 && tv[q] != 1 && !bex[q]) { tv[q] = 2; td[q] = (d + 1 > lexd[q]) ? d + 1 : lexd[q]; push(q, td[q]); } } }
    }
  }
  uint8_t *V = vals + (size_t)c * 2048; memset(V, 0, 2048);
  for (int idx = 0; idx < 8192; idx++) {
    int stm = idx >> 12, code;
    if (tv[idx] == 255) code = 3;
    else if (!fin[idx] || tv[idx] == 3 || tv[idx] == 0) code = 0;
    else if (tv[idx] == 1) code = stm == WHITE ? 1 : 2;
    else code = stm == WHITE ? 2 : 1;
    if (tv[idx] != 255 && !fin[idx]) code = 0;
    V[idx >> 2] |= code << (2 * (idx & 3));
    if (dflag) deps[(size_t)c * 8192 + idx] = (code == 1 || code == 2) ? td[idx] : 0;
  }
  solved[c] = 1;
}

/* ---------------- input ---------------- */
typedef struct { u64 w, b; int wk, bk, stm, ep; char text[160]; } Pos;
static int sqn(const char *s) { if (s[0] < 'a' || s[0] > 'h' || s[1] < '1' || s[1] > '8') return -1; return (s[0] - 'a') + 8 * (s[1] - '1'); }
static void sqname(int s, char *o) { o[0] = 'a' + (s & 7); o[1] = '1' + (s >> 3); o[2] = 0; }

static int parse(char *line, Pos *P) {
  char buf[400]; strncpy(buf, line, 399); buf[399] = 0;
  char *nl = strchr(buf, '\n'); if (nl) *nl = 0;
  strncpy(P->text, buf, 159); P->text[159] = 0;
  P->w = P->b = 0; P->wk = P->bk = -1; P->stm = -1; P->ep = -1;
  char *tok = strtok(buf, " \t");
  if (!tok) return 0;
  if (strchr(tok, '/')) {           /* FEN board */
    int r = 7, f = 0;
    for (char *c = tok; *c; c++) {
      if (*c == '/') { r--; f = 0; continue; }
      if (*c >= '1' && *c <= '8') { f += *c - '0'; continue; }
      int s = r * 8 + f++;
      if (*c == 'K') P->wk = s; else if (*c == 'k') P->bk = s; else if (*c == 'P') P->w |= BIT(s); else if (*c == 'p') P->b |= BIT(s); else return -1; }
    tok = strtok(NULL, " \t"); if (!tok) return -1;
    P->stm = tok[0] == 'w' ? WHITE : tok[0] == 'b' ? BLACK : -1;
    tok = strtok(NULL, " \t"); if (tok && strcmp(tok, "-")) P->ep = sqn(tok);
  } else {
    for (; tok; tok = strtok(NULL, " \t")) {
      if (strlen(tok) == 3 && strchr("KkPp", tok[0])) { int s = sqn(tok + 1); if (s < 0) return -1;
        if (tok[0] == 'K') P->wk = s; else if (tok[0] == 'k') P->bk = s; else if (tok[0] == 'P') P->w |= BIT(s); else P->b |= BIT(s); }
      else if (!strcmp(tok, "w")) P->stm = WHITE; else if (!strcmp(tok, "b")) P->stm = BLACK;
      else if (!strcmp(tok, "-")) ; else if (strlen(tok) == 2 && sqn(tok) >= 0) P->ep = sqn(tok);
      else return -1; }
  }
  if (P->wk < 0 || P->bk < 0 || P->stm < 0) return -1;
  if (!legalpos(P->w, P->b, P->wk, P->bk, P->stm)) return -2;
  return 1;
}

static void mvname(const Move *m, u64 b0, u64 w0, int stm, char *o) {
  char f[3], t[3]; sqname(m->from, f); sqname(m->to, t);
  if (m->piece == 'K') sprintf(o, "K%s%s%s", f, m->cap ? "x" : "-", t);
  else sprintf(o, "%s%s%s%s", f, m->cap ? "x" : "-", t, m->type == PROMO ? "=" : "");
  (void)b0; (void)w0; (void)stm;
}
static char vc(int v) { return v == 1 ? 'W' : v == 2 ? 'L' : 'D'; }

int main(int argc, char **argv) {
  int mflag = 0, lplies = 0, cflag = 0;
  for (int i = 1; i < argc; i++) { if (!strcmp(argv[i], "-d")) dflag = 1; else if (!strcmp(argv[i], "-m")) mflag = 1;
    else if (!strcmp(argv[i], "-c")) cflag = 1;
    else if (!strcmp(argv[i], "-l") && i + 1 < argc) { lplies = atoi(argv[++i]); dflag = 1; } else { fprintf(stderr, "usage: p74 [-d] [-m] [-l N] < positions\n"); return 2; } }
  for (int s = 0; s < 64; s++) { KA[s] = 0; for (int dr = -1; dr <= 1; dr++) for (int df = -1; df <= 1; df++) {
      if (!dr && !df) continue; int r = (s >> 3) + dr, f = (s & 7) + df; if (r >= 0 && r < 8 && f >= 0 && f < 8) KA[s] |= BIT(r * 8 + f); } }
  int np = 0, cap = 1024; Pos *ps = malloc(sizeof(Pos) * cap); char line[400];
  while (fgets(line, sizeof line, stdin)) {
    if (line[0] == '#' || line[0] == '\n') continue;
    if (np == cap) { cap *= 2; ps = realloc(ps, sizeof(Pos) * cap); }
    int r = parse(line, &ps[np]);
    if (r == -1) { fprintf(stderr, "bad line: %s", line); return 2; }
    if (r == -2) { fprintf(stderr, "illegal position: %s", line); return 2; }
    if (r == 1) np++; }
  /* sizes: hash and key array fixed, checked before allocation */
  hcap = 1ULL << 22; maxcfg = 1 << 21;
  u64 fixedb = hcap * 4 + (u64)maxcfg * (sizeof(Cfg) + 1) + (u64)(8192 * 9 + 8192) * 8;
  if (fixedb > LIMIT) { fprintf(stderr, "fixed tables too large\n"); return 3; }
  for (int i = 0; i < 256; i++) ci[i] = -1;
  keys = malloc(sizeof(Cfg) * maxcfg); slot = malloc(4 * hcap); memset(slot, 0xff, 4 * hcap);
  for (int i = 0; i < np; i++) insert(ps[i].w, ps[i].b);
  enumerate();
  u64 per = 2048 + (dflag ? 16384 : 0);
  u64 need = fixedb + (u64)ncfg * (per + sizeof(Cfg));
  fprintf(stderr, "p74: %d positions, %d configs, tables %.3f GB\n", np, ncfg, need / 1e9);
  if (need > LIMIT) { fprintf(stderr, "p74: would pass 2.0 GB, exit\n"); return 3; }
  if (cflag) return 0;
  vals = malloc((size_t)ncfg * 2048); solved = calloc(ncfg, 1);
  if (dflag) deps = malloc((size_t)ncfg * 8192 * 2);
  pool_idx = malloc(sizeof(int32_t) * (8192 * 9 + 8192)); pool_next = malloc(sizeof(int32_t) * (8192 * 9 + 8192));
  list = malloc(sizeof(Cfg) * ncfg); memcpy(list, keys, sizeof(Cfg) * ncfg);
  qsort(list, ncfg, sizeof(Cfg), cmpcfg);
  /* rebuild hash in sorted order so that index = solving order */
  memset(slot, 0xff, 4 * hcap); int32_t n0 = ncfg; ncfg = 0;
  for (int32_t i = 0; i < n0; i++) insert(list[i].w, list[i].b);
  for (int32_t i = 0; i < ncfg; i++) solve(i);
  for (int i = 0; i < np; i++) {
    Pos *P = &ps[i]; int d, v = value(P->w, P->b, P->wk, P->bk, P->stm, P->ep, &d);
    if (dflag) printf("%s  P=%c%d\n", P->text, vc(v), d); else printf("%s  P=%c\n", P->text, vc(v));
    if (mflag) { Move mv[64]; int n = gen(P->w, P->b, P->wk, P->bk, P->stm, P->ep, mv);
      for (int k = 0; k < n; k++) { char nm[16]; mvname(&mv[k], P->b, P->w, P->stm, nm); int dd, vv;
        if (mv[k].type == PROMO) { vv = P->stm == WHITE ? 1 : 2; dd = 0; } else vv = value(mv[k].w, mv[k].b, mv[k].wk, mv[k].bk, 1 - P->stm, mv[k].ep, &dd);
        if (dflag) printf("   %-10s %c%d\n", nm, vc(vv), dd); else printf("   %-10s %c\n", nm, vc(vv)); } }
    if (lplies) {
      u64 w = P->w, b = P->b; int wk = P->wk, bk = P->bk, stm = P->stm, ep = P->ep, pl = 0, mno = 1; printf("   line:");
      while (pl < lplies) {
        int dd, cv = value(w, b, wk, bk, stm, ep, &dd); Move mv[64]; int n = gen(w, b, wk, bk, stm, ep, mv);
        if (n == 0) { printf(" (no move)"); break; }
        int win = stm == WHITE ? 1 : 2, pick = -1, pd = 0, ppawn = 0;
        for (int k = 0; k < n; k++) { int vv, d2;
          if (mv[k].type == PROMO) { vv = win; d2 = 0; } else vv = value(mv[k].w, mv[k].b, mv[k].wk, mv[k].bk, 1 - stm, mv[k].ep, &d2);
          if (cv == win) { if (vv == win && (pick < 0 || d2 < pd)) { pick = k; pd = d2; } }
          else if (cv == 0) { if (vv == 0 && (pick < 0 || (!ppawn && mv[k].piece == 'P'))) { pick = k; ppawn = mv[k].piece == 'P'; } }
          else { if (pick < 0 || d2 > pd) { pick = k; pd = d2; } } }
        char nm[16]; mvname(&mv[pick], b, w, stm, nm);
        if (stm == WHITE) printf(" %d.%s", mno, nm); else { printf(" %s%s", pl == 0 ? "1..." : "", nm); mno++; }
        pl++;
        if (mv[pick].type == PROMO) { printf(" (promotes)"); break; }
        w = mv[pick].w; b = mv[pick].b; wk = mv[pick].wk; bk = mv[pick].bk; ep = mv[pick].ep; stm = 1 - stm; }
      printf("\n"); }
  }
  fprintf(stderr, "p74: done\n");
  return 0;
}
