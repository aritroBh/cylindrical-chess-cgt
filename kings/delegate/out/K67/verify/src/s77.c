/* s77.c -- K77 referee: the P game of a king-and-pawn group on flat 8x8 in a D-sum with one small D-game T.
 *
 * Written for K77 from the definitions in kings/theory/LOOPY.md (Definitions 1.1-1.3, the sum's rule of K40 quoted in
 * Lemma 4.15, Theorem 4.18 (c)); it shares no code with ax65, pk_sum, k66, p74, ref3m, kp_p, p45a or r48.
 *
 * Board game: kings and pawns, flat 8x8 (no wrap), double steps and en passant; a promotion ends the play as a win for
 * the promoter; checkmate: the side in check has no move.  Sum's rule: a move in T is a move elsewhere; it is not
 * allowed while in check and it clears the mover's e.p. right; a side with no move (in either component) loses.
 * T (option -t):
 *   zero      T = 0 (no moves).                         Infinite play: draw.
 *   p         the P game alone: as zero, but a stalemate (no move, not in check) is a draw, as in P.
 *   minus1    T = -1: Black may once move M -> Z.        Infinite play: draw.        Start state M.
 *   ladderN   T_N of Theorem 4.18 (c): u_0..u_N, z; White u_i -> u_{i+1}, u_N -> (+) (White wins); Black u_i -> z.
 *             Infinite play: draw.  Start state u_0.
 *   aux       Aux = G + under_D: White may pass U -> U at will, Black may once move U -> Z.  Infinite play: a White win
 *             iff White passed infinitely often (Buchi), else a Black win.  Start state U.
 * Method: pawn configurations change irreversibly and so does T apart from the pass; blocks (config, T state) are
 * solved so that every move leaving a block goes to a solved block.  Inside a block: retrograde analysis with move
 * counters (3 values; in aux mode the state Z has no passes, so undecided = Black win), and for aux state U the Buchi
 * fixpoint nu Y. mu X. (White wins an exit, or White moves into X, or White passes into Y; Black has a move and all its
 * moves go to X or to White-won exits).  Positions with a live e.p. right are not stored; they are valued by one ply.
 * Input (stdin): "Kd5 kf4 Pa2 Pb3 Pe2 pa5 pb4 pe5 b -" (pieces, side to move, e.p. square or -), T in its start state.
 * Output: value in White's view (W, D, L); with -m also every legal move (board and T) and the value after it.
 * Memory: configurations are counted first; exit with status 3 if the tables would pass 2.0e9 bytes.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef uint64_t u64;
#define B1(s) (1ULL << (s))
#define FA 0x0101010101010101ULL
#define FH 0x8080808080808080ULL
#define R1 0x00000000000000FFULL
#define R8 0xFF00000000000000ULL
enum { WH = 0, BL = 1 };
enum { VD = 0, VW = 1, VL = 2, VX = 3 };   /* value codes in White's view; VX illegal */

static u64 KA[64];
static u64 watt(u64 w) { return ((w & ~FA) << 7) | ((w & ~FH) << 9); }
static u64 batt(u64 b) { return ((b & ~FA) >> 9) | ((b & ~FH) >> 7); }

/* ---------------- T ---------------- */
#define TWIN (-1)    /* White's move to (+) */
#define MAXT 16
static int NT, TSTART, pmode = 0, auxmode = 0;
static int tW[MAXT], tB[MAXT];   /* one White move and one Black move per state at most: target, TWIN, or -9 none */
static int tPass[MAXT];          /* White pass (self-loop, Buchi accepting) */
static int torder[MAXT];         /* solving order: successors first */

static void setT(const char *s) {
  for (int i = 0; i < MAXT; i++) { tW[i] = tB[i] = -9; tPass[i] = 0; }
  if (!strcmp(s, "zero") || !strcmp(s, "p")) { NT = 1; TSTART = 0; torder[0] = 0; pmode = !strcmp(s, "p"); }
  else if (!strcmp(s, "minus1")) { NT = 2; TSTART = 0; tB[0] = 1; torder[0] = 1; torder[1] = 0; }
  else if (!strcmp(s, "aux")) { NT = 2; TSTART = 0; tPass[0] = 1; tB[0] = 1; torder[0] = 1; torder[1] = 0; auxmode = 1; }
  else if (!strncmp(s, "ladder", 6)) {
    int N = atoi(s + 6); if (N < 0 || N + 2 > MAXT) { fprintf(stderr, "bad N\n"); exit(2); }
    NT = N + 2; TSTART = 0;                       /* u_i = i, z = N+1 */
    for (int i = 0; i <= N; i++) { tW[i] = i < N ? i + 1 : TWIN; tB[i] = N + 1; }
    torder[0] = N + 1; for (int i = 0; i <= N; i++) torder[1 + i] = N - i;
  } else { fprintf(stderr, "unknown T %s\n", s); exit(2); }
}

/* ---------------- configurations ---------------- */
typedef struct { u64 w, b; } Cf;
static Cf *cf; static int32_t *hs; static u64 hcap; static int32_t ncf = 0, maxcf;
static u64 hh(u64 w, u64 b) { u64 x = (w ^ 0x5bd1e9955bd1e995ULL) * 0xff51afd7ed558ccdULL + b * 0xc4ceb9fe1a85ec53ULL; x ^= x >> 31; x *= 0x9e3779b97f4a7c15ULL; return x ^ (x >> 29); }
static int32_t cfind(u64 w, u64 b) {
  u64 h = hh(w, b) & (hcap - 1);
  for (;;) { int32_t i = hs[h]; if (i < 0) return -1; if (cf[i].w == w && cf[i].b == b) return i; h = (h + 1) & (hcap - 1); }
}
static void cadd(u64 w, u64 b) {
  if (cfind(w, b) >= 0) return;
  if (ncf >= maxcf) { fprintf(stderr, "s77: more than %d configs\n", maxcf); exit(3); }
  u64 h = hh(w, b) & (hcap - 1); while (hs[h] >= 0) h = (h + 1) & (hcap - 1);
  cf[ncf].w = w; cf[ncf].b = b; hs[h] = ncf++;
}
/* every configuration a legal move can lead to (a superset is harmless) */
static void succcfgs(u64 w, u64 b) {
  u64 occ = w | b, p;
  for (p = w; p; p &= p - 1) { int s = __builtin_ctzll(p), f = s & 7, r = s >> 3;
    if (r < 6 && !(occ & B1(s + 8))) { cadd(w ^ B1(s) ^ B1(s + 8), b);
      if (r == 1 && !(occ & B1(s + 16))) cadd(w ^ B1(s) ^ B1(s + 16), b); }
    if (r < 6) { if (f > 0 && (b & B1(s + 7))) cadd(w ^ B1(s) ^ B1(s + 7), b ^ B1(s + 7));
                 if (f < 7 && (b & B1(s + 9))) cadd(w ^ B1(s) ^ B1(s + 9), b ^ B1(s + 9)); }
    if (r == 4) { if (f > 0 && (b & B1(s - 1))) cadd(w ^ B1(s) ^ B1(s + 7), b ^ B1(s - 1));   /* e.p. */
                  if (f < 7 && (b & B1(s + 1))) cadd(w ^ B1(s) ^ B1(s + 9), b ^ B1(s + 1)); } }
  for (p = b; p; p &= p - 1) { int s = __builtin_ctzll(p), f = s & 7, r = s >> 3;
    if (r > 1 && !(occ & B1(s - 8))) { cadd(w, b ^ B1(s) ^ B1(s - 8));
      if (r == 6 && !(occ & B1(s - 16))) cadd(w, b ^ B1(s) ^ B1(s - 16)); }
    if (r > 1) { if (f > 0 && (w & B1(s - 9))) cadd(w ^ B1(s - 9), b ^ B1(s) ^ B1(s - 9));
                 if (f < 7 && (w & B1(s - 7))) cadd(w ^ B1(s - 7), b ^ B1(s) ^ B1(s - 7)); }
    if (r == 3) { if (f > 0 && (w & B1(s - 1))) cadd(w ^ B1(s - 1), b ^ B1(s) ^ B1(s - 9));
                  if (f < 7 && (w & B1(s + 1))) cadd(w ^ B1(s + 1), b ^ B1(s) ^ B1(s - 7)); } }
  for (p = b; p; p &= p - 1) { int s = __builtin_ctzll(p); if (!(batt(b ^ B1(s)) & B1(s))) cadd(w, b ^ B1(s)); }  /* White king takes */
  for (p = w; p; p &= p - 1) { int s = __builtin_ctzll(p); if (!(watt(w ^ B1(s)) & B1(s))) cadd(w ^ B1(s), b); }
}
static int prog(Cf c) { int s = 0; u64 p; for (p = c.w; p; p &= p - 1) s += __builtin_ctzll(p) >> 3; for (p = c.b; p; p &= p - 1) s += 7 - (__builtin_ctzll(p) >> 3); return s; }
static int ccmp(const void *x, const void *y) {
  const Cf *a = x, *c = y; int na = __builtin_popcountll(a->w | a->b), nc = __builtin_popcountll(c->w | c->b);
  if (na != nc) return na - nc; return prog(*c) - prog(*a);
}

/* ---------------- moves ---------------- */
enum { MK, MX, MP, MT };   /* king move inside the config, move to another config, promotion, move in T */
typedef struct { int ty; u64 w, b; int wk, bk, ep, t, pass; int fr, to; char pc; } Mv;

static int incheck(u64 w, u64 b, int wk, int bk, int stm) { return stm == WH ? (batt(b) & B1(wk)) != 0 : (watt(w) & B1(bk)) != 0; }

static int genboard(u64 w, u64 b, int wk, int bk, int stm, int ep, Mv *m) {
  int n = 0; u64 occ = w | b | B1(wk) | B1(bk);
  if (stm == WH) {
    for (u64 t = KA[wk] & ~w & ~KA[bk]; t; t &= t - 1) { int s = __builtin_ctzll(t); u64 nb = b & ~B1(s);
      if (batt(nb) & B1(s)) continue;
      m[n++] = (Mv){ nb == b ? MK : MX, w, nb, s, bk, -1, 0, 0, wk, s, 'K' }; }
    for (u64 p = w; p; p &= p - 1) { int s = __builtin_ctzll(p), f = s & 7, r = s >> 3;
      int tg[4], nt = 0; u64 cb[4];
      if (!(occ & B1(s + 8))) { tg[nt] = s + 8; cb[nt++] = 0; }
      if (f > 0 && (b & B1(s + 7))) { tg[nt] = s + 7; cb[nt++] = B1(s + 7); }
      if (f < 7 && (b & B1(s + 9))) { tg[nt] = s + 9; cb[nt++] = B1(s + 9); }
      if (ep >= 0 && r == 4 && ((f > 0 && ep == s + 7) || (f < 7 && ep == s + 9))) { tg[nt] = ep; cb[nt++] = B1(ep - 8); }
      for (int k = 0; k < nt; k++) { u64 nb = b & ~cb[k];
        if (batt(nb) & B1(wk)) continue;                     /* own king left in check */
        if ((tg[k] >> 3) == 7) { m[n++] = (Mv){ MP, 0, 0, wk, bk, -1, 0, 0, s, tg[k], 'P' }; continue; }
        m[n++] = (Mv){ MX, w ^ B1(s) ^ B1(tg[k]), nb, wk, bk, -1, 0, 0, s, tg[k], 'P' }; }
      if (r == 1 && !(occ & B1(s + 8)) && !(occ & B1(s + 16)) && !(batt(b) & B1(wk)))
        m[n++] = (Mv){ MX, w ^ B1(s) ^ B1(s + 16), b, wk, bk, s + 8, 0, 0, s, s + 16, 'P' }; }
  } else {
    for (u64 t = KA[bk] & ~b & ~KA[wk]; t; t &= t - 1) { int s = __builtin_ctzll(t); u64 nw = w & ~B1(s);
      if (watt(nw) & B1(s)) continue;
      m[n++] = (Mv){ nw == w ? MK : MX, nw, b, wk, s, -1, 0, 0, bk, s, 'K' }; }
    for (u64 p = b; p; p &= p - 1) { int s = __builtin_ctzll(p), f = s & 7, r = s >> 3;
      int tg[4], nt = 0; u64 cw[4];
      if (!(occ & B1(s - 8))) { tg[nt] = s - 8; cw[nt++] = 0; }
      if (f > 0 && (w & B1(s - 9))) { tg[nt] = s - 9; cw[nt++] = B1(s - 9); }
      if (f < 7 && (w & B1(s - 7))) { tg[nt] = s - 7; cw[nt++] = B1(s - 7); }
      if (ep >= 0 && r == 3 && ((f > 0 && ep == s - 9) || (f < 7 && ep == s - 7))) { tg[nt] = ep; cw[nt++] = B1(ep + 8); }
      for (int k = 0; k < nt; k++) { u64 nw = w & ~cw[k];
        if (watt(nw) & B1(bk)) continue;
        if ((tg[k] >> 3) == 0) { m[n++] = (Mv){ MP, 0, 0, wk, bk, -1, 0, 0, s, tg[k], 'P' }; continue; }
        m[n++] = (Mv){ MX, nw, b ^ B1(s) ^ B1(tg[k]), wk, bk, -1, 0, 0, s, tg[k], 'P' }; }
      if (r == 6 && !(occ & B1(s - 8)) && !(occ & B1(s - 16)) && !(watt(w) & B1(bk)))
        m[n++] = (Mv){ MX, w, b ^ B1(s) ^ B1(s - 16), wk, bk, s - 8, 0, 0, s, s - 16, 'P' }; }
  }
  return n;
}
/* T moves of stm in state t (none while in check) */
static int gent(u64 w, u64 b, int wk, int bk, int stm, int t, Mv *m) {
  int n = 0; if (incheck(w, b, wk, bk, stm)) return 0;
  if (stm == WH) { if (tW[t] != -9) m[n++] = (Mv){ MT, w, b, wk, bk, -1, tW[t], 0, -1, -1, 'T' };
                   if (tPass[t]) m[n++] = (Mv){ MT, w, b, wk, bk, -1, t, 1, -1, -1, 'T' }; }
  else if (tB[t] != -9) m[n++] = (Mv){ MT, w, b, wk, bk, -1, tB[t], 0, -1, -1, 'T' };
  return n;
}

static int legal(u64 w, u64 b, int wk, int bk, int stm) {
  if (wk == bk || ((w | b) & (B1(wk) | B1(bk))) || (KA[wk] & B1(bk)) || ((w | b) & (R1 | R8)) || (w & b)) return 0;
  if (stm == WH && (watt(w) & B1(bk))) return 0;
  if (stm == BL && (batt(b) & B1(wk))) return 0;
  return 1;
}
static int eplive(u64 w, u64 b, int stm, int ep) {
  if (ep < 0) return 0;
  return stm == WH ? (batt(B1(ep)) & w) != 0 : (watt(B1(ep)) & b) != 0;
}

/* ---------------- tables ---------------- */
static uint8_t *val;  /* [config][t][2048] */
static uint8_t *done; /* [config][t] */
static int getv(int32_t c, int t, int idx) { return (val[((size_t)c * NT + t) * 2048 + (idx >> 2)] >> (2 * (idx & 3))) & 3; }
static void setv(int32_t c, int t, int idx, int v) { uint8_t *p = &val[((size_t)c * NT + t) * 2048 + (idx >> 2)]; *p = (*p & ~(3 << (2 * (idx & 3)))) | (v << (2 * (idx & 3))); }
static int value(u64 w, u64 b, int wk, int bk, int stm, int ep, int t);

/* value of the position after move mv by stm (state t before the move) */
static int after(const Mv *mv, int stm, int t) {
  if (mv->ty == MP) return stm == WH ? VW : VL;
  if (mv->ty == MT) { if (mv->t == TWIN) return VW; return value(mv->w, mv->b, mv->wk, mv->bk, 1 - stm, -1, mv->t); }
  return value(mv->w, mv->b, mv->wk, mv->bk, 1 - stm, mv->ep, t);
}
static int nomove(u64 w, u64 b, int wk, int bk, int stm) {
  if (pmode && !incheck(w, b, wk, bk, stm)) return VD;
  return stm == WH ? VL : VW;
}
/* one ply (positions with a live e.p. right; also for -m) */
static int ply1(u64 w, u64 b, int wk, int bk, int stm, int ep, int t) {
  Mv m[80]; int n = genboard(w, b, wk, bk, stm, ep, m); n += gent(w, b, wk, bk, stm, t, m + n);
  if (n == 0) return nomove(w, b, wk, bk, stm);
  int good = stm == WH ? VW : VL, bad = stm == WH ? VL : VW, best = bad;
  for (int i = 0; i < n; i++) { int v = after(&m[i], stm, t); if (v == good) return good; if (v == VD) best = VD; }
  return best;
}
static int value(u64 w, u64 b, int wk, int bk, int stm, int ep, int t) {
  if (eplive(w, b, stm, ep)) return ply1(w, b, wk, bk, stm, ep, t);
  int32_t c = cfind(w, b);
  if (c < 0 || !done[(size_t)c * NT + t]) { fprintf(stderr, "s77 internal: block not solved\n"); exit(4); }
  int v = getv(c, t, (stm << 12) | (wk << 6) | bk);
  if (v == VX) { fprintf(stderr, "s77 internal: illegal position looked up\n"); exit(4); }
  return v;
}

/* ---------------- one block ---------------- */
static int nsc[8192], sc[8192][10], scacc[8192][10], cnt[8192], dex[8192], wex[8192], allw[8192], nmv[8192];
static int rs[8193], radj[8192 * 10], rfill[8192];
static uint8_t st[8192];   /* 0 open, 1 win for mover, 2 loss for mover, 3 draw, 255 illegal */
static int qu[8192 * 2];

static void solveblock(int32_t c, int t) {
  u64 w = cf[c].w, b = cf[c].b; Mv m[80];
  int buchi = auxmode && tPass[t];
  for (int idx = 0; idx < 8192; idx++) {
    int stm = idx >> 12, wk = (idx >> 6) & 63, bk = idx & 63; nsc[idx] = 0;
    if (!legal(w, b, wk, bk, stm)) { st[idx] = 255; continue; }
    int n = genboard(w, b, wk, bk, stm, -1, m); n += gent(w, b, wk, bk, stm, t, m + n);
    nmv[idx] = n; st[idx] = 0; dex[idx] = 0; wex[idx] = 0; allw[idx] = 1;
    int good = stm == WH ? VW : VL;
    for (int i = 0; i < n; i++) {
      int inb = (m[i].ty == MK) || (m[i].ty == MT && m[i].pass);
      if (inb) { int k = nsc[idx]++; sc[idx][k] = ((1 - stm) << 12) | (m[i].wk << 6) | m[i].bk; scacc[idx][k] = m[i].ty == MT; continue; }
      int v = after(&m[i], stm, t);
      if (v == good) wex[idx] = 1; else if (v == VD) dex[idx] = 1;
      if (v != VW) allw[idx] = 0;
    }
  }
  if (!buchi) {
    int qh = 0, qt = 0;
    for (int idx = 0; idx < 8192; idx++) { if (st[idx] == 255) continue; cnt[idx] = nsc[idx];
      if (nmv[idx] == 0) { int v = nomove(w, b, (idx >> 6) & 63, idx & 63, idx >> 12); int stm = idx >> 12;
        st[idx] = v == VD ? 3 : ((v == VW) == (stm == WH)) ? 1 : 2; if (st[idx] != 3) qu[qt++] = idx; continue; }
      if (wex[idx]) { st[idx] = 1; qu[qt++] = idx; }
      else if (nsc[idx] == 0) { st[idx] = dex[idx] ? 3 : 2; if (st[idx] == 2) qu[qt++] = idx; } }
    memset(rs, 0, sizeof rs);
    for (int i = 0; i < 8192; i++) if (st[i] != 255) for (int k = 0; k < nsc[i]; k++) rs[sc[i][k] + 1]++;
    for (int i = 0; i < 8192; i++) rs[i + 1] += rs[i];
    memcpy(rfill, rs, sizeof rfill);
    for (int i = 0; i < 8192; i++) if (st[i] != 255) for (int k = 0; k < nsc[i]; k++) radj[rfill[sc[i][k]]++] = i;
    while (qh < qt) { int x = qu[qh++];
      for (int k = rs[x]; k < rs[x + 1]; k++) { int q = radj[k]; if (st[q] != 0) continue;
        if (st[x] == 2) { st[q] = 1; qu[qt++] = q; }
        else if (st[x] == 1) { if (--cnt[q] == 0) { if (dex[q]) st[q] = 3; else { st[q] = 2; qu[qt++] = q; } } } } }
    for (int idx = 0; idx < 8192; idx++) { int v, stm = idx >> 12;
      if (st[idx] == 255) v = VX;
      else if (st[idx] == 1) v = stm == WH ? VW : VL;
      else if (st[idx] == 2) v = stm == WH ? VL : VW;
      else v = auxmode ? VL : VD;            /* open or draw; in aux mode an endless play without passes is Black's */
      setv(c, t, idx, v); }
  } else {
    /* Buchi: Y = nu, X = mu; White wins from X */
    static uint8_t inY[8192], inX[8192];
    memset(rs, 0, sizeof rs);
    for (int i = 0; i < 8192; i++) if (st[i] != 255) for (int k = 0; k < nsc[i]; k++) if (!scacc[i][k]) rs[sc[i][k] + 1]++;
    for (int i = 0; i < 8192; i++) rs[i + 1] += rs[i];
    memcpy(rfill, rs, sizeof rfill);
    for (int i = 0; i < 8192; i++) if (st[i] != 255) for (int k = 0; k < nsc[i]; k++) if (!scacc[i][k]) radj[rfill[sc[i][k]]++] = i;
    for (int i = 0; i < 8192; i++) inY[i] = st[i] != 255;
    for (;;) {
      int qt = 0, qh = 0;
      for (int i = 0; i < 8192; i++) { inX[i] = 0; if (st[i] == 255) continue; int stm = i >> 12;
        if (stm == WH) { int ok = wex[i]; for (int k = 0; k < nsc[i] && !ok; k++) if (scacc[i][k] && inY[sc[i][k]]) ok = 1;
          if (ok) { inX[i] = 1; qu[qt++] = i; } }
        else { cnt[i] = nsc[i]; if (nmv[i] == 0 || (allw[i] && nsc[i] == 0)) { inX[i] = 1; qu[qt++] = i; } } }
      while (qh < qt) { int x = qu[qh++];
        for (int k = rs[x]; k < rs[x + 1]; k++) { int q = radj[k]; if (inX[q]) continue;
          if ((q >> 12) == WH) { inX[q] = 1; qu[qt++] = q; }
          else if (--cnt[q] == 0 && allw[q]) { inX[q] = 1; qu[qt++] = q; } } }
      int same = 1; for (int i = 0; i < 8192; i++) if (inX[i] != inY[i]) { same = 0; break; }
      if (same) break;
      memcpy(inY, inX, sizeof inY);
    }
    for (int idx = 0; idx < 8192; idx++) setv(c, t, idx, st[idx] == 255 ? VX : inY[idx] ? VW : VL);
  }
  done[(size_t)c * NT + t] = 1;
}

/* ---------------- input / output ---------------- */
typedef struct { u64 w, b; int wk, bk, stm, ep; char txt[200]; } Pos;
static int sqn(const char *s) { return (s[0] >= 'a' && s[0] <= 'h' && s[1] >= '1' && s[1] <= '8') ? (s[0] - 'a') + 8 * (s[1] - '1') : -1; }
static void sqs(int s, char *o) { o[0] = 'a' + (s & 7); o[1] = '1' + (s >> 3); o[2] = 0; }
static char vch(int v) { return v == VW ? 'W' : v == VL ? 'L' : v == VD ? 'D' : '?'; }

int main(int argc, char **argv) {
  int mflag = 0; const char *T = "zero";
  for (int i = 1; i < argc; i++) { if (!strcmp(argv[i], "-m")) mflag = 1; else if (!strcmp(argv[i], "-t") && i + 1 < argc) T = argv[++i];
    else { fprintf(stderr, "usage: s77 [-t zero|p|minus1|ladderN|aux] [-m] < positions\n"); return 2; } }
  setT(T);
  for (int s = 0; s < 64; s++) { KA[s] = 0; for (int dr = -1; dr <= 1; dr++) for (int df = -1; df <= 1; df++) { if (!dr && !df) continue;
    int r = (s >> 3) + dr, f = (s & 7) + df; if (r >= 0 && r < 8 && f >= 0 && f < 8) KA[s] |= B1(r * 8 + f); } }
  int np = 0, cap = 256; Pos *ps = malloc(sizeof(Pos) * cap); char line[400];
  while (fgets(line, sizeof line, stdin)) {
    if (line[0] == '#' || line[0] == '\n') continue;
    if (np == cap) { cap *= 2; ps = realloc(ps, sizeof(Pos) * cap); }
    Pos *P = &ps[np]; P->w = P->b = 0; P->wk = P->bk = P->stm = P->ep = -1;
    char *nl = strchr(line, '\n'); if (nl) *nl = 0; snprintf(P->txt, sizeof P->txt, "%s", line);
    for (char *tok = strtok(line, " \t"); tok; tok = strtok(NULL, " \t")) {
      if (strlen(tok) == 3 && strchr("KkPp", tok[0]) && sqn(tok + 1) >= 0) { int s = sqn(tok + 1);
        if (tok[0] == 'K') P->wk = s; else if (tok[0] == 'k') P->bk = s; else if (tok[0] == 'P') P->w |= B1(s); else P->b |= B1(s); }
      else if (!strcmp(tok, "w")) P->stm = WH; else if (!strcmp(tok, "b")) P->stm = BL; else if (!strcmp(tok, "-")) ;
      else if (strlen(tok) == 2 && sqn(tok) >= 0) P->ep = sqn(tok);
      else { fprintf(stderr, "bad token %s\n", tok); return 2; } }
    if (P->wk < 0 || P->bk < 0 || P->stm < 0 || !legal(P->w, P->b, P->wk, P->bk, P->stm)) { fprintf(stderr, "bad or illegal: %s\n", P->txt); return 2; }
    np++; }
  hcap = 1ULL << 21; maxcf = 1 << 20;
  cf = malloc(sizeof(Cf) * maxcf); hs = malloc(4 * hcap); memset(hs, 0xff, 4 * hcap);
  for (int i = 0; i < np; i++) cadd(ps[i].w, ps[i].b);
  for (int32_t i = 0; i < ncf; i++) succcfgs(cf[i].w, cf[i].b);
  double need = (double)ncf * NT * 2049 + 4.0 * hcap + 16.0 * maxcf + 2.0e6;
  fprintf(stderr, "s77: T=%s, %d positions, %d configs, tables %.3f GB\n", T, np, ncf, need / 1e9);
  if (need > 2.0e9) { fprintf(stderr, "s77: would pass 2.0 GB, exit\n"); return 3; }
  val = calloc((size_t)ncf * NT, 2048); done = calloc((size_t)ncf * NT, 1);
  if (!val || !done) { fprintf(stderr, "alloc failed\n"); return 3; }
  qsort(cf, ncf, sizeof(Cf), ccmp);
  memset(hs, 0xff, 4 * hcap); { int32_t n0 = ncf; ncf = 0; Cf *tmp = malloc(sizeof(Cf) * n0); memcpy(tmp, cf, sizeof(Cf) * n0);
    for (int32_t i = 0; i < n0; i++) cadd(tmp[i].w, tmp[i].b); free(tmp); }
  for (int32_t c = 0; c < ncf; c++) for (int k = 0; k < NT; k++) solveblock(c, torder[k]);
  for (int i = 0; i < np; i++) { Pos *P = &ps[i];
    int v = value(P->w, P->b, P->wk, P->bk, P->stm, P->ep, TSTART);
    printf("%s  %s=%c\n", P->txt, T, vch(v));
    if (mflag) { Mv m[80]; int n = genboard(P->w, P->b, P->wk, P->bk, P->stm, P->ep, m); n += gent(P->w, P->b, P->wk, P->bk, P->stm, TSTART, m + n);
      for (int k = 0; k < n; k++) { char a[3], z[3], nm[24];
        if (m[k].ty == MT) snprintf(nm, sizeof nm, "%s", m[k].pass ? "pass" : "T-move");
        else { sqs(m[k].fr, a); sqs(m[k].to, z); int cap = m[k].ty == MX && (__builtin_popcountll(m[k].w | m[k].b) < __builtin_popcountll(P->w | P->b));
          snprintf(nm, sizeof nm, "%s%s%s%s%s", m[k].pc == 'K' ? "K" : "", a, cap ? "x" : "-", z, m[k].ty == MP ? "=" : ""); }
        printf("   %-10s %c\n", nm, vch(after(&m[k], P->stm, TSTART))); } } }
  fprintf(stderr, "s77: done\n");
  return 0;
}
