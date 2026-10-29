/* grp.c -- K15: classify king groups on a cylinder as frozen / on / off / dud / over / under / other.
 *
 * Own move generator (written for this task, independent of kpsolve.c and of cylcgt).
 *
 * MODEL.  The "local game" of a group is the promotion model P of LOOPY (first promotion wins) played with
 * real kings on the whole W x H cylinder, with ONLY the group's pieces on the board (empty context), and with
 * free passes for both sides (a pass is illegal in check).  This is the game Z (+) dud_D of Theorem 3.4(a)
 * with the group Z as the short part.  V*(position, side to move) in {win, loss, draw} for the mover is solved
 * exactly (least fixed point, infinite play = draw) for every placement of both kings (anywhere) and every
 * set of group pawns with <= WM white and <= BM black pawns on the files 0..F-1 (ranks 2..H-1).
 *
 * A Z-move m of side s (king move or Z-pawn move; a pass is not a Z-move) from position y to y' is
 *    a SUICIDE   if V*(y', opponent to move) = win for the opponent  (decisively punished, Def. 2.5 local form)
 *    WINNING     if m is a promotion, or V*(y', opponent to move) = loss for the opponent (a forced local win
 *                for s against a passing opponent: a decisive threat)
 *    SAFE        otherwise (V* = draw).
 * Classification of a root placement x (both kings on files 0..F-1):
 *    check   : some king of some state of the closure is attacked by a pawn            -> other
 *    threat  : some side has a WINNING move at some state of the closure               -> other
 *    leak    : some SAFE move takes the mover's king off the files 0..F-1               -> other
 *    frozen  : no SAFE move for either side at x (every Z-move is a suicide)
 *    on      : closure C of x under White's safe moves (Black has none): every y in C has >= 1 White safe move,
 *              no Black safe move, no check, no threat, no leak           (bisimilar to on_D, Prop 3.2)
 *    off     : mirror
 *    dud     : closure C of x under safe moves of BOTH sides: every y in C has >= 1 White and >= 1 Black safe
 *              move, no check/threat/leak                                  (bisimilar to dud_D)
 *    over    : Black passes: A-states (Black has >= 1 safe move) have >= 1 White safe move, all Black safe
 *              moves lead to A-states, all White safe moves lead to Z-states (no safe move for either side, no
 *              check/threat/leak)                                          (bisimilar to over_D = {0|over_D})
 *    under   : mirror (White passes)
 *    other   : everything else (subtype: mixed)
 * Self-check: every root labelled frozen/on/off/dud/over/under must have V*(x,W)=V*(x,B)=draw.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

typedef uint64_t u64;
typedef uint32_t u32;

static int W, H, F, N, NN, WM, BM, NOPASS = 0, ALLOWPASSER = 0, IGNORELEAK = 0, FLAT = 0;
static int PW;               /* number of pawn squares = F*(H-2) */
static int psq[40];          /* pawn index -> board square */
static int sqp[64];          /* board square -> pawn index or -1 */
static int nb[64][8], nnb[64];
static u64 kmask[64];
static u64 wFrom[64], bFrom[64]; /* squares from which a white (black) pawn attacks sq */

#define BIT(s) (1ULL << (s))
#define SQ(f, r) ((r) * W + (f))

/* ---------- layers ---------- */
static int L;
static u32 *LWm, *LBm;       /* pawn-index masks */
static u64 *HK; static int *HV; static int HS;
static uint8_t *tab;         /* L * 2*NN bytes: 0 draw, 1 win(mover), 2 loss(mover), 3 illegal */

static inline u64 hkey(u32 w, u32 b) { return ((u64)w << 32) | b; }
static inline u64 hmix(u64 k) { k ^= k >> 33; k *= 0xff51afd7ed558ccdULL; k ^= k >> 33; k *= 0xc4ceb9fe1a85ec53ULL; k ^= k >> 33; return k; }
static void hput(u32 w, u32 b, int v) {
  u64 k = hkey(w, b) + 1; u64 h = hmix(k) & (HS - 1);
  while (HK[h]) h = (h + 1) & (HS - 1);
  HK[h] = k; HV[h] = v;
}
static int getLayer(u32 w, u32 b) {
  u64 k = hkey(w, b) + 1; u64 h = hmix(k) & (HS - 1);
  while (HK[h]) { if (HK[h] == k) return HV[h]; h = (h + 1) & (HS - 1); }
  fprintf(stderr, "getLayer failure w=%u b=%u\n", w, b); exit(2);
}
static u64 bb_of(u32 m) { u64 r = 0; while (m) { int i = __builtin_ctz(m); m &= m - 1; r |= BIT(psq[i]); } return r; }

/* ---------- geometry ---------- */
static void init_geo(void) {
  N = W * H; NN = N * N;
  for (int s = 0; s < N; s++) {
    int f = s % W, r = s / W; nnb[s] = 0; kmask[s] = 0; wFrom[s] = bFrom[s] = 0;
    for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
      if (!df && !dr) continue;
      int g = ((f + df) % W + W) % W, q = r + dr;
      if (q < 0 || q >= H) continue;
      if (FLAT && (f + df < 0 || f + df >= W)) continue;
      int t = SQ(g, q);
      int dup = 0; for (int i = 0; i < nnb[s]; i++) if (nb[s][i] == t) dup = 1;
      if (!dup && t != s) { nb[s][nnb[s]++] = t; kmask[s] |= BIT(t); }
    }
    /* white pawn on (f+-1, r-1) attacks (f, r): wFrom[s] = {(f+-1, r-1)} */
    for (int df = -1; df <= 1; df += 2) {
      int g = ((f + df) % W + W) % W;
      if (FLAT && (f + df < 0 || f + df >= W)) continue;
      if (r - 1 >= 0) wFrom[s] |= BIT(SQ(g, r - 1));
      if (r + 1 < H) bFrom[s] |= BIT(SQ(g, r + 1));
    }
  }
  PW = F * (H - 2);
  memset(sqp, -1, sizeof sqp);
  for (int f = 0; f < F; f++) for (int r = 1; r <= H - 2; r++) { int i = f * (H - 2) + (r - 1); psq[i] = SQ(f, r); sqp[SQ(f, r)] = i; }
}

/* ---------- per-layer data ---------- */
typedef struct { int side, from, to, promo, dbl, cap, tl, epT, epC; u64 oppAfter; } PMv;
typedef struct { u32 w, b; u64 WP, BP; int npm; PMv pm[48]; } LD;

static void prep(int li, LD *d) {
  u32 w = LWm[li], b = LBm[li]; d->w = w; d->b = b; d->WP = bb_of(w); d->BP = bb_of(b); d->npm = 0;
  for (int side = 0; side < 2; side++) {
    u32 mine = side ? b : w, theirsm = side ? w : b; u64 myP = side ? d->BP : d->WP, opP = side ? d->WP : d->BP;
    int dir = side ? -1 : 1; int start = side ? H - 2 : 1; int last = side ? 0 : H - 1;
    u32 m = mine;
    while (m) {
      int pi = __builtin_ctz(m); m &= m - 1; int s = psq[pi]; int f = s % W, r = s / W;
      int r1 = r + dir;
      { int t = SQ(f, r1);
        if (r1 == last) { PMv *p = &d->pm[d->npm++]; p->side = side; p->from = s; p->to = t; p->promo = 1; p->dbl = 0; p->cap = -1; p->tl = -1; p->epT = p->epC = -1; p->oppAfter = opP; }
        else if (!((myP | opP) >> t & 1)) {
          u32 nm = mine ^ BIT(pi) ^ BIT(sqp[t]);
          PMv *p = &d->pm[d->npm++];
          p->side = side; p->from = s; p->to = t; p->promo = 0; p->dbl = 0; p->cap = -1; p->epT = p->epC = -1; p->oppAfter = opP;
          p->tl = side ? getLayer(theirsm, nm) : getLayer(nm, theirsm);
          if (r == start) {
            int r2 = r + 2 * dir; int t2 = SQ(f, r2);
            if (!((myP | opP) >> t2 & 1)) {
              PMv *q = &d->pm[d->npm++]; u32 nm2 = mine ^ BIT(pi) ^ BIT(sqp[t2]);
              q->side = side; q->from = s; q->to = t2; q->promo = 0; q->dbl = 1; q->cap = -1; q->epT = t; q->epC = t2; q->oppAfter = opP;
              q->tl = side ? getLayer(theirsm, nm2) : getLayer(nm2, theirsm);
            }
          }
        }
      }
      for (int df = -1; df <= 1; df += 2) {
        int g = ((f + df) % W + W) % W; if (g >= F) continue;
        if (FLAT && (f + df < 0 || f + df >= W)) continue;
        if (r1 < 0 || r1 >= H) continue;
        int t = SQ(g, r1);
        if (opP >> t & 1) {
          PMv *p = &d->pm[d->npm++]; u32 nm = mine ^ BIT(pi) ^ BIT(sqp[t]); u32 no = theirsm ^ BIT(sqp[t]);
          p->side = side; p->from = s; p->to = t; p->promo = 0; p->dbl = 0; p->cap = t; p->epT = p->epC = -1; p->oppAfter = opP & ~BIT(t);
          p->tl = side ? getLayer(no, nm) : getLayer(nm, no);
        }
      }
    }
  }
}

/* ---------- move generation ---------- */
typedef struct { int tl, su, val, term, kleave, kind; } Mv;  /* val=-1: lookup tab[tl][su]; kind 0 pass,1 king,2 pawn */

static int value_of(int li, int stm, int wk, int bk, int epT, int epC);

/* generate all legal moves of `stm` in layer li. allowPass: include the pass. */
static int gen(int li, const LD *d, int stm, int wk, int bk, int epT, int epC, int allowPass, Mv *out) {
  int n = 0; int ks = stm ? bk : wk, ko = stm ? wk : bk;
  u64 myP = stm ? d->BP : d->WP, opP = stm ? d->WP : d->BP;
  const u64 *from = stm ? wFrom : bFrom; /* squares from which an OPPONENT pawn attacks sq */
  int inCheck = (opP & from[ks]) != 0;
  if (allowPass && !NOPASS && !inCheck) {
    Mv *m = &out[n++]; m->tl = li; m->su = (1 - stm) * NN + wk * N + bk; m->val = -1; m->term = 0; m->kleave = 0; m->kind = 0;
  }
  for (int i = 0; i < nnb[ks]; i++) {
    int t = nb[ks][i];
    if (myP >> t & 1) continue;
    if (t == ko || (kmask[ko] >> t & 1)) continue;
    int cap = (opP >> t & 1);
    u64 opAfter = cap ? (opP & ~BIT(t)) : opP;
    if (opAfter & from[t]) continue;
    Mv *m = &out[n++]; m->term = 0; m->val = -1; m->kind = 1; m->kleave = ((t % W) >= F);
    int nwk = stm ? wk : t, nbk = stm ? t : bk; m->su = (1 - stm) * NN + nwk * N + nbk;
    if (!cap) m->tl = li;
    else { u32 w2 = d->w, b2 = d->b; if (stm) w2 ^= BIT(sqp[t]); else b2 ^= BIT(sqp[t]); m->tl = getLayer(w2, b2); }
  }
  for (int k = 0; k < d->npm; k++) {
    const PMv *p = &d->pm[k]; if (p->side != stm) continue;
    if (p->promo) {
      if (p->to == wk || p->to == bk) continue;
      if (p->oppAfter & from[ks]) continue;
      Mv *m = &out[n++]; m->term = 1; m->tl = -1; m->su = 0; m->val = -1; m->kleave = 0; m->kind = 2; continue;
    }
    if (p->cap < 0) {
      if (p->to == wk || p->to == bk) continue;
      if (p->dbl && (p->epT == wk || p->epT == bk)) continue;
    }
    if (p->oppAfter & from[ks]) continue;
    Mv *m = &out[n++]; m->term = 0; m->kleave = 0; m->kind = 2; m->tl = p->tl;
    m->su = (1 - stm) * NN + wk * N + bk; m->val = -1;
    if (p->dbl) m->val = value_of(p->tl, 1 - stm, wk, bk, p->epT, p->epC);
  }
  if (epT >= 0) {
    int ef = epT % W, er = epC / W;
    for (int df = -1; df <= 1; df += 2) {
      int g = ((ef + df) % W + W) % W; if (g >= F) continue;
      if (FLAT && (ef + df < 0 || ef + df >= W)) continue;
      int s = SQ(g, er); if (!(myP >> s & 1)) continue;
      u64 opAfter = opP & ~BIT(epC);
      if (opAfter & from[ks]) continue;
      u32 mw = stm ? d->b : d->w, ow = stm ? d->w : d->b;
      u32 nm = mw ^ BIT(sqp[s]) ^ BIT(sqp[epT]); u32 no = ow ^ BIT(sqp[epC]);
      Mv *m = &out[n++]; m->term = 0; m->kleave = 0; m->kind = 2; m->val = -1; m->su = (1 - stm) * NN + wk * N + bk;
      m->tl = stm ? getLayer(no, nm) : getLayer(nm, no);
    }
  }
  return n;
}

/* value for the mover at an arbitrary state of a COMPLETE layer (used for ep states) */
static int value_of(int li, int stm, int wk, int bk, int epT, int epC) {
  LD d; prep(li, &d); Mv mv[64];
  int n = gen(li, &d, stm, wk, bk, epT, epC, 1, mv);
  int ks = stm ? bk : wk; u64 opP = stm ? d.WP : d.BP; const u64 *from = stm ? wFrom : bFrom;
  int inCheck = (opP & from[ks]) != 0;
  int anyDraw = 0;
  if (n == 0) return inCheck ? 2 : 0;
  for (int i = 0; i < n; i++) {
    if (mv[i].term) return 1;
    int v = mv[i].val >= 0 ? mv[i].val : tab[(size_t)mv[i].tl * 2 * NN + mv[i].su];
    if (v == 2) return 1;
    if (v == 0) anyDraw = 1;
  }
  return anyDraw ? 0 : 2;
}

/* ---------- layer solve ---------- */
static int *edU, *edV, *predOff, *predList, *cnt, *fillp; static uint8_t *hasDraw; static int *queue;
static void solve_layer(int li) {
  LD d; prep(li, &d); uint8_t *val = tab + (size_t)li * 2 * NN; int NS = 2 * NN;
  int ne = 0; Mv mv[64];
  u64 occP = d.WP | d.BP;
  for (int u = 0; u < NS; u++) {
    int stm = u / NN, wk = (u % NN) / N, bk = u % N;
    val[u] = 3; cnt[u] = 0; hasDraw[u] = 0;
    if (wk == bk || (kmask[wk] >> bk & 1)) continue;
    if ((occP >> wk & 1) || (occP >> bk & 1)) continue;
    if (stm == 0) { if (d.WP & wFrom[bk]) continue; } else { if (d.BP & bFrom[wk]) continue; }
    val[u] = 0;
  }
  int qh = 0, qt = 0;
  for (int u = 0; u < NS; u++) {
    if (val[u] == 3) continue;
    int stm = u / NN, wk = (u % NN) / N, bk = u % N;
    int n = gen(li, &d, stm, wk, bk, -1, -1, 1, mv);
    int win = 0, c = 0, dr = 0; int ne0 = ne;
    for (int i = 0; i < n; i++) {
      if (mv[i].term) { win = 1; break; }
      if (mv[i].val < 0 && mv[i].tl == li) { c++; edU[ne] = u; edV[ne] = mv[i].su; ne++; continue; }
      int v = mv[i].val >= 0 ? mv[i].val : tab[(size_t)mv[i].tl * 2 * NN + mv[i].su];
      if (v == 2) { win = 1; break; }
      if (v == 0) dr = 1;
    }
    if (win) { val[u] = 1; queue[qt++] = u; ne = ne0; continue; }
    cnt[u] = c; hasDraw[u] = dr;
    if (n == 0) { int ks = stm ? bk : wk; u64 opP = stm ? d.WP : d.BP; const u64 *from = stm ? wFrom : bFrom;
      if (opP & from[ks]) { val[u] = 2; queue[qt++] = u; } continue; }
    if (c == 0 && !dr) { val[u] = 2; queue[qt++] = u; }
  }
  memset(predOff, 0, sizeof(int) * (NS + 2));
  for (int e = 0; e < ne; e++) predOff[edV[e] + 1]++;
  for (int u = 0; u < NS; u++) predOff[u + 1] += predOff[u];
  memcpy(fillp, predOff, sizeof(int) * (NS + 1));
  for (int e = 0; e < ne; e++) predList[fillp[edV[e]]++] = edU[e];
  while (qh < qt) {
    int v = queue[qh++]; int vv = val[v];
    for (int k = predOff[v]; k < predOff[v + 1]; k++) {
      int u = predList[k]; if (val[u] != 0) continue;
      if (vv == 2) { val[u] = 1; queue[qt++] = u; }
      else if (vv == 1) { if (--cnt[u] == 0 && !hasDraw[u]) { val[u] = 2; queue[qt++] = u; } }
    }
  }
}

/* ---------- position I/O ---------- */
static void sqname(int s, char *o) { o[0] = 'a' + s % W; o[1] = '1' + s / W; o[2] = 0; }
static void posstr(int li, int wk, int bk, int stm, char *o) {
  char t[4]; o[0] = 0; sqname(wk, t); strcat(o, "K"); strcat(o, t);
  sqname(bk, t); strcat(o, " k"); strcat(o, t);
  for (int i = 0; i < PW; i++) if (LWm[li] >> i & 1) { sqname(psq[i], t); strcat(o, " P"); strcat(o, t); }
  for (int i = 0; i < PW; i++) if (LBm[li] >> i & 1) { sqname(psq[i], t); strcat(o, " p"); strcat(o, t); }
  strcat(o, stm ? " b -" : " w -");
}

/* cylcgt.passed at a root without e.p. right */
static int passed_side(u32 w, u32 b, int side) {
  u32 mine = side ? b : w, theirs = side ? w : b; u32 m = mine;
  while (m) {
    int pi = __builtin_ctz(m); m &= m - 1; int s = psq[pi]; int f = s % W, r = s / W; int blocked = 0;
    u32 t = theirs;
    while (t) {
      int qi = __builtin_ctz(t); t &= t - 1; int q = psq[qi]; int g = q % W, rr = q / W;
      int dfile = ((g - f) % W + W) % W;
      if (FLAT) { if (!(g - f >= -1 && g - f <= 1)) continue; } else if (!(dfile == 0 || dfile == 1 || dfile == W - 1)) continue;
      if (side == 0 ? rr > r : rr < r) { blocked = 1; break; }
    }
    if (!blocked) return 1;
  }
  return 0;
}
static int root_has_passer(u32 w, u32 b) { return passed_side(w, b, 0) || passed_side(w, b, 1); }

/* ---------- classification ---------- */
typedef struct { int tl, wk, bk; } St;
typedef struct {
  int nSafe[2], nWin[2], nSuic[2], leak, check, nlegal[2];
  St safe[2][48];
} Info;

static void analyze(int li, int wk, int bk, Info *I) {
  LD d; prep(li, &d); Mv mv[64];
  memset(I->nSafe, 0, sizeof I->nSafe); memset(I->nWin, 0, sizeof I->nWin); memset(I->nSuic, 0, sizeof I->nSuic);
  I->leak = 0; I->check = 0;
  if ((d.WP & wFrom[bk]) || (d.BP & bFrom[wk])) I->check = 1;
  for (int s = 0; s < 2; s++) {
    int n = gen(li, &d, s, wk, bk, -1, -1, 0, mv); I->nlegal[s] = n;
    for (int i = 0; i < n; i++) {
      if (mv[i].term) { I->nWin[s]++; continue; }
      int v = mv[i].val >= 0 ? mv[i].val : tab[(size_t)mv[i].tl * 2 * NN + mv[i].su];
      if (v == 1) { I->nSuic[s]++; continue; }
      if (v == 2) { I->nWin[s]++; continue; }
      if (mv[i].kleave) { if (IGNORELEAK) continue; I->leak = 1; }
      int su = mv[i].su % NN; St *t = &I->safe[s][I->nSafe[s]++];
      t->tl = mv[i].tl; t->wk = su / N; t->bk = su % N;
    }
  }
}

#define VS 16384
static u64 vk[VS]; static int vstamp[VS]; static int curstamp = 0; static int vcount = 0;
static u64 stid(const St *s) { return ((u64)s->tl * N + s->wk) * N + s->bk; }
static int vis_add(u64 id) { u64 h = hmix(id) & (VS - 1); while (vstamp[h] == curstamp) { if (vk[h] == id) return 0; h = (h + 1) & (VS - 1); } vstamp[h] = curstamp; vk[h] = id; vcount++; return 1; }

enum { C_FROZEN, C_ON, C_OFF, C_DUD, C_OVER, C_UNDER, C_CHECK, C_THREAT, C_LEAK, C_MIXED, NCLS };
static const char *CN[] = {"frozen", "on", "off", "dud", "over", "under", "check", "threat", "leak", "mixed"};

typedef struct { int cls; int csize; u64 canon; int maxq; int pure; int two; int why; int near; } Res;

static int bad(const Info *I) { return I->check || I->nWin[0] || I->nWin[1] || I->leak; }
#define MAXCLOSURE 6000

/* does side s have a safe non-capturing king 2-cycle inside the files 0..F-1 at root (li,wk,bk)?
   if needFrozenOther: at both ends the other side has no safe move, no winning move, no check. */
static int has_shuttle(int li, int wk, int bk, int s, const Info *I, int needFrozenOther) {
  static Info J;
  for (int i = 0; i < I->nSafe[s]; i++) {
    const St *t = &I->safe[s][i]; if (t->tl != li) continue;
    int nk = s ? t->bk : t->wk; if ((nk % W) >= F) continue;
    analyze(li, t->wk, t->bk, &J);
    if (J.check || J.nWin[0] || J.nWin[1]) continue;
    if (needFrozenOther && J.nSafe[1 - s]) continue;
    int back = 0;
    for (int k = 0; k < J.nSafe[s]; k++) if (J.safe[s][k].tl == li && J.safe[s][k].wk == wk && J.safe[s][k].bk == bk) back = 1;
    if (back) return 1;
  }
  return 0;
}

static Res classify_root(int li, int wk, int bk) {
  Res R; R.cls = C_MIXED; R.csize = 0; R.canon = 0; R.maxq = 0; R.pure = 0; R.two = 0; R.why = 0; R.near = 0; Info I; analyze(li, wk, bk, &I);
  if (I.check) { R.cls = C_CHECK; return R; }
  if (I.nWin[0] || I.nWin[1]) { R.cls = C_THREAT; return R; }
  if (!I.nSafe[0] && !I.nSafe[1]) { R.cls = C_FROZEN; R.csize = 1; R.canon = ((u64)li * N + wk) * N + bk; return R; }
  static St stack[VS]; static Info II, ZZ;
  /* on / off with possible extra options of the passing side (Prop. 3.2: Z >= on_D, Z <= on_D... = on_D if no extras) */
  if (I.nSafe[0] && !I.nSafe[1] && has_shuttle(li, wk, bk, 0, &I, 1)) R.cls = C_ON;
  else if (I.nSafe[1] && !I.nSafe[0] && has_shuttle(li, wk, bk, 1, &I, 1)) R.cls = C_OFF;
  else if (I.nSafe[0] && I.nSafe[1]) R.two = has_shuttle(li, wk, bk, 0, &I, 0) && has_shuttle(li, wk, bk, 1, &I, 0);
  if (R.cls == C_ON || R.cls == C_OFF) R.canon = ((u64)li * N + wk) * N + bk;
  if (I.nSafe[0] && I.nSafe[1]) { /* root-level near-over / near-under: p passes (has a shuttle), every q safe move leads to a frozen state */
    static Info NZ;
    for (int p = 1; p >= 0; p--) { int q = 1 - p; int allz = 1;
      if (!has_shuttle(li, wk, bk, p, &I, 0)) continue;
      for (int i = 0; i < I.nSafe[q] && allz; i++) { analyze(I.safe[q][i].tl, I.safe[q][i].wk, I.safe[q][i].bk, &NZ); if (bad(&NZ) || NZ.nSafe[0] || NZ.nSafe[1]) allz = 0; }
      if (allz) R.near |= (p == 1 ? 1 : 2); }
  }
  for (int mode = 0; mode < 5; mode++) {
    /* 0 on (pure), 1 off (pure), 2 dud, 3 over (Black passes), 4 under (White passes) */
    if (mode == 0 && !(I.nSafe[0] && !I.nSafe[1])) continue;
    if (mode == 1 && !(I.nSafe[1] && !I.nSafe[0])) continue;
    if (mode >= 2 && !(I.nSafe[0] && I.nSafe[1])) continue;
    if (mode >= 2 && I.leak) continue;
    curstamp++; vcount = 0; int sp = 0, ok = 1, maxq = 0; u64 canon = ~0ULL; int cs = 0;
    St r0 = {li, wk, bk}; vis_add(stid(&r0)); stack[sp++] = r0;
    int p = (mode == 3) ? 1 : 0, q = 1 - p; /* over: p = Black passes; under: p = White passes */
    while (sp && ok) {
      St y = stack[--sp]; cs++; u64 id = stid(&y); if (id < canon) canon = id;
      if (vcount > MAXCLOSURE) { ok = 0; if (mode == 2) R.why = 6; break; }
      analyze(y.tl, y.wk, y.bk, &II);
      if (bad(&II)) { ok = 0; if (mode == 2) R.why = II.check ? 1 : (II.nWin[0] || II.nWin[1]) ? 2 : 3; break; }
      if (mode == 0) { if (!(II.nSafe[0] >= 1 && II.nSafe[1] == 0)) { ok = 0; break; } for (int i = 0; i < II.nSafe[0]; i++) if (vis_add(stid(&II.safe[0][i]))) stack[sp++] = II.safe[0][i]; }
      else if (mode == 1) { if (!(II.nSafe[1] >= 1 && II.nSafe[0] == 0)) { ok = 0; break; } for (int i = 0; i < II.nSafe[1]; i++) if (vis_add(stid(&II.safe[1][i]))) stack[sp++] = II.safe[1][i]; }
      else if (mode == 2) { if (!(II.nSafe[0] >= 1 && II.nSafe[1] >= 1)) { ok = 0; R.why = II.nSafe[0] < 1 ? 4 : 5; break; }
        for (int s = 0; s < 2; s++) for (int i = 0; i < II.nSafe[s]; i++) if (vis_add(stid(&II.safe[s][i]))) stack[sp++] = II.safe[s][i]; }
      else {
        /* over/under: every popped state must be an A-state: p has >= 1 safe move, q has >= 1 safe move,
           p's successors are A-states (checked when popped), q's successors are Z-states (checked now) */
        if (II.nSafe[p] < 1 || II.nSafe[q] < 1) { ok = 0; break; }
        if (II.nSafe[q] > maxq) maxq = II.nSafe[q];
        for (int i = 0; i < II.nSafe[p]; i++) { St *t = &II.safe[p][i]; if (vis_add(stid(t))) stack[sp++] = *t; }
        for (int i = 0; i < II.nSafe[q]; i++) { St *t = &II.safe[q][i];
          analyze(t->tl, t->wk, t->bk, &ZZ);
          if (bad(&ZZ) || ZZ.nSafe[0] || ZZ.nSafe[1]) { ok = 0; break; }
          u64 zid = stid(t); if (zid < canon) canon = zid; cs++; }
      }
    }
    if (ok) {
      if (mode <= 1) { R.pure = 1; if (R.cls != (mode == 0 ? C_ON : C_OFF)) { R.cls = mode == 0 ? C_ON : C_OFF; } R.csize = cs; R.canon = canon; return R; }
      R.cls = mode == 2 ? C_DUD : mode == 3 ? C_OVER : C_UNDER; R.csize = cs; R.canon = canon; R.maxq = maxq; return R; }
  }
  if (R.cls == C_ON || R.cls == C_OFF) return R;
  if (I.leak) R.cls = C_LEAK; else R.cls = C_MIXED;
  return R;
}

/* ---------- main ---------- */
static int cmpL(const void *a, const void *b) { long long x = ((const long long *)a)[0], y = ((const long long *)b)[0]; return x < y ? -1 : x > y; }

static int parse_pos(const char *s, int *wk, int *bk, u32 *w, u32 *b) {
  *w = *b = 0; *wk = *bk = -1; char buf[256]; strncpy(buf, s, 255); buf[255] = 0;
  for (char *t = strtok(buf, " "); t; t = strtok(NULL, " ")) {
    char c = t[0]; if (strlen(t) < 3 || !strchr("KkPp", c)) continue;
    int f = t[1] - 'a', r = atoi(t + 2) - 1; int sq = SQ(f, r);
    if (c == 'K') *wk = sq; else if (c == 'k') *bk = sq;
    else { if (sqp[sq] < 0) return 0; if (c == 'P') *w |= BIT(sqp[sq]); else *b |= BIT(sqp[sq]); }
  }
  return *wk >= 0 && *bk >= 0;
}

static int MAXCAND = 5000; static FILE *dumpf = NULL; static clock_t t0; static const char *outprefix_g = "grp";
static void census(const char *tag) {
  const char *outprefix = outprefix_g;
  /* census */
  long long cnt_ij[16][16][NCLS]; long long placements_ij[16][16]; long long near_over = 0, near_under = 0, why_cnt[8], two_by_cls[NCLS], pure_on = 0, pure_off = 0, over_one = 0, under_one = 0; memset(cnt_ij,0,sizeof cnt_ij); memset(placements_ij,0,sizeof placements_ij); memset(why_cnt,0,sizeof why_cnt); memset(two_by_cls,0,sizeof two_by_cls);
  long long selfviol = 0; long long nroots = 0, nskippedpasser = 0;
  char fn[512]; snprintf(fn, sizeof fn, "%s_%s_cands.txt", outprefix, tag); FILE *fc = fopen(fn, "w");
  size_t CS = 1 << 22; u64 *cset = calloc(CS, 8); int ncand_written[NCLS]; memset(ncand_written, 0, sizeof ncand_written);
  long long distinct[NCLS]; memset(distinct, 0, sizeof distinct); int near_written = 0;
  for (int li = 0; li < L; li++) {
    int i = __builtin_popcount(LWm[li]), j = __builtin_popcount(LBm[li]); if (i + j == 0) continue;
    if (!ALLOWPASSER && root_has_passer(LWm[li], LBm[li])) { nskippedpasser++; continue; }
    u64 occ = bb_of(LWm[li]) | bb_of(LBm[li]);
    for (int wf = 0; wf < F; wf++) for (int wr = 0; wr < H; wr++) {
      int wk = SQ(wf, wr); if (occ >> wk & 1) continue;
      for (int bf = 0; bf < F; bf++) for (int br = 0; br < H; br++) {
        int bk = SQ(bf, br); if (bk == wk || (occ >> bk & 1) || (kmask[wk] >> bk & 1)) continue;
        nroots++; placements_ij[i][j]++;
        Res R = classify_root(li, wk, bk);
        if (dumpf) { char s3[256]; posstr(li, wk, bk, 0, s3); fprintf(dumpf, "%s\t%s\n", s3, CN[R.cls]); }
        cnt_ij[i][j][R.cls]++; if (R.two) two_by_cls[R.cls]++; if (R.near && R.cls != C_OVER && R.cls != C_UNDER) { if (R.near & 1) near_over++; if (R.near & 2) near_under++; if (near_written < 40) { char s2[256]; posstr(li, wk, bk, 0, s2); fprintf(fc, "near%s\t%s\t%d,%d\n", (R.near & 1) ? "over" : "under", s2, i, j); near_written++; } } if (R.why && R.cls != C_DUD) why_cnt[R.why]++;
        if (R.cls == C_ON && R.pure) pure_on++; if (R.cls == C_OFF && R.pure) pure_off++;
        if (R.cls == C_OVER && R.maxq == 1) over_one++; if (R.cls == C_UNDER && R.maxq == 1) under_one++;
        if (R.cls <= C_UNDER) {
          uint8_t a = tab[(size_t)li * 2 * NN + wk * N + bk], bq = tab[(size_t)li * 2 * NN + NN + wk * N + bk];
          if (a != 0 || bq != 0) { selfviol++; fprintf(stderr, "SELFCHECK VIOLATION class=%s li=%d wk=%d bk=%d\n", CN[R.cls], li, wk, bk); }
          u64 key = R.canon * 8 + R.cls + 1; u64 h = hmix(key) & (CS - 1); int found = 0;
          while (cset[h]) { if (cset[h] == key) { found = 1; break; } h = (h + 1) & (CS - 1); }
          if (!found) { cset[h] = key; distinct[R.cls]++;
            int lim = (R.cls >= C_DUD) ? MAXCAND : 20;
            if (ncand_written[R.cls] < lim) {
              char s[256]; posstr(li, wk, bk, 0, s); fprintf(fc, "%s\t%s\t%d,%d\tcsize=%d\tmaxq=%d\n", CN[R.cls], s, i, j, R.csize, R.maxq); ncand_written[R.cls]++; }
          }
        }
      }
    }
    if ((li & 4095) == 4095) { fprintf(stderr, "classified through layer %d/%d, %.1fs cpu\n", li + 1, L, (double)(clock() - t0) / CLOCKS_PER_SEC); }
  }
  fclose(fc); free(cset);
  printf("{\"variant\":\"%s\",\"board\":\"%s:%dx%d\",\"files\":%d,\"wmax\":%d,\"bmax\":%d,\"root_passers\":\"%s\",\"ignore_leak\":%d,\"layers\":%d,\"roots\":%lld,\"skipped_passer_layers\":%lld,\"selfcheck_violations\":%lld,\n \"by_ij\":{",
         tag, FLAT ? "flat" : "cyl", W, H, F, WM, BM, ALLOWPASSER ? "allowed" : "excluded", IGNORELEAK, L, nroots, nskippedpasser, selfviol);
  int firstij = 1;
  for (int i = 0; i <= WM; i++) for (int j = 0; j <= BM; j++) { if (!placements_ij[i][j]) continue;
    printf("%s\"%d+%d\":{\"placements\":%lld", firstij ? "" : ",", i, j, placements_ij[i][j]); firstij = 0;
    for (int c = 0; c < NCLS; c++) printf(",\"%s\":%lld", CN[c], cnt_ij[i][j][c]); printf("}"); }
  printf("},\n \"total\":{");
  for (int c = 0; c < NCLS; c++) { long long s = 0; for (int i = 0; i < 16; i++) for (int j = 0; j < 16; j++) s += cnt_ij[i][j][c]; printf("%s\"%s\":%lld", c ? "," : "", CN[c], s); }
  printf("},\n \"distinct_groups\":{");
  for (int c = 0; c <= C_UNDER; c++) printf("%s\"%s\":%lld", c ? "," : "", CN[c], distinct[c]);
  printf("},\n \"two_sided_shuttle_roots_by_final_class\":{");
  for (int c = 0; c < NCLS; c++) printf("%s\"%s\":%lld", c ? "," : "", CN[c], two_by_cls[c]);
  printf("},\n \"dud_attempt_failure_reasons\":{\"check\":%lld,\"threat\":%lld,\"leak\":%lld,\"white_state_without_safe_move\":%lld,\"black_state_without_safe_move\":%lld,\"closure_too_big\":%lld},\n \"near_over_roots\":%lld,\"near_under_roots\":%lld,\"on_pure\":%lld,\"off_pure\":%lld,\"over_exactly_one_white_move\":%lld,\"under_exactly_one\":%lld}\n", why_cnt[1], why_cnt[2], why_cnt[3], why_cnt[4], why_cnt[5], why_cnt[6], near_over, near_under, pure_on, pure_off, over_one, under_one);
  fprintf(stderr, "census done %.1fs cpu\n", (double)(clock() - t0) / CLOCKS_PER_SEC);
}

int main(int argc, char **argv) {
  const char *mode = "census"; const char *posarg = NULL; const char *outprefix = "grp"; int variants = 0; int nrand = 0; unsigned seed = 1;
  W = 8; H = 6; F = 3; WM = 2; BM = 2;
  for (int i = 1; i < argc; i++) {
    if (!strcmp(argv[i], "--W")) W = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--H")) H = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--F")) F = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--wmax")) WM = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--bmax")) BM = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--nopass")) NOPASS = 1;
    else if (!strcmp(argv[i], "--flat")) FLAT = 1;
    else if (!strcmp(argv[i], "--allow-passer")) ALLOWPASSER = 1;
    else if (!strcmp(argv[i], "--ignore-leak")) IGNORELEAK = 1;
    else if (!strcmp(argv[i], "--classify")) { mode = "classify"; posarg = argv[++i]; }
    else if (!strcmp(argv[i], "--dumprand")) { mode = "dumprand"; nrand = atoi(argv[++i]); seed = atoi(argv[++i]); }
    else if (!strcmp(argv[i], "--census")) mode = "census";
    else if (!strcmp(argv[i], "--out")) outprefix = argv[++i];
    else if (!strcmp(argv[i], "--variants")) variants = 1;
    else if (!strcmp(argv[i], "--strict-variants")) variants = 2;
    else if (!strcmp(argv[i], "--sp-variants")) variants = 3;
    else if (!strcmp(argv[i], "--dumproots")) dumpf = fopen(argv[++i], "w");
    else if (!strcmp(argv[i], "--maxcand")) MAXCAND = atoi(argv[++i]);
    else { fprintf(stderr, "bad arg %s\n", argv[i]); return 1; }
  }
  init_geo();
  int cwk = 0, cbk = 0; u32 cw = 0, cb = 0;
  if (!strcmp(mode, "classify")) { char *d0 = strdup(posarg); char *f0 = strtok(d0, ";"); if (!parse_pos(f0, &cwk, &cbk, &cw, &cb)) { fprintf(stderr, "bad pos\n"); return 1; } }
  int nm = 1 << PW; u32 *ml = malloc(sizeof(u32) * nm); int nl = 0; int MX = WM > BM ? WM : BM;
  for (u32 m = 0; m < (u32)nm; m++) { int c = __builtin_popcount(m); if (c <= MX) ml[nl++] = m; }
  long long lc = 0;
  for (int a = 0; a < nl; a++) for (int c = 0; c < nl; c++) if (!(ml[a] & ml[c]) && __builtin_popcount(ml[a]) <= WM && __builtin_popcount(ml[c]) <= BM) lc++;
  L = (int)lc;
  long long (*keys)[3] = malloc(sizeof(long long) * 3 * lc); long long k = 0;
  for (int a = 0; a < nl; a++) for (int c = 0; c < nl; c++) if (!(ml[a] & ml[c]) && __builtin_popcount(ml[a]) <= WM && __builtin_popcount(ml[c]) <= BM) {
    u32 w = ml[a], b = ml[c]; int adv = 0; u32 t = w; while (t) { int i = __builtin_ctz(t); t &= t - 1; adv += psq[i] / W; }
    t = b; while (t) { int i = __builtin_ctz(t); t &= t - 1; adv += (H - 1) - psq[i] / W; }
    int cntp = __builtin_popcount(w) + __builtin_popcount(b);
    keys[k][0] = (long long)cntp * 1000 + (500 - adv); keys[k][1] = w; keys[k][2] = b; k++; }
  qsort(keys, lc, sizeof keys[0], cmpL);
  LWm = malloc(4 * lc); LBm = malloc(4 * lc);
  HS = 1; while (HS < 4 * lc) HS <<= 1; HK = calloc(HS, 8); HV = malloc(HS * sizeof(int));
  for (long long i = 0; i < lc; i++) { LWm[i] = (u32)keys[i][1]; LBm[i] = (u32)keys[i][2]; hput(LWm[i], LBm[i], (int)i); }
  free(keys); free(ml);
  size_t tsz = (size_t)L * 2 * NN; tab = malloc(tsz);
  fprintf(stderr, "board %s:%dx%d F=%d wmax=%d bmax=%d layers=%d table=%.1f MB nopass=%d\n", FLAT ? "flat" : "cyl", W, H, F, WM, BM, L, tsz / 1e6, NOPASS);
  edU = malloc(sizeof(int) * 2 * NN * 12); edV = malloc(sizeof(int) * 2 * NN * 12); predOff = malloc(sizeof(int) * (2 * NN + 2)); fillp = malloc(sizeof(int) * (2 * NN + 2));
  predList = malloc(sizeof(int) * 2 * NN * 12); cnt = malloc(sizeof(int) * 2 * NN); hasDraw = malloc(2 * NN); queue = malloc(sizeof(int) * (2 * NN + 64));
  t0 = clock();
  for (int li = 0; li < L; li++) { solve_layer(li); if ((li & 8191) == 8191) fprintf(stderr, "solved %d/%d layers, %.1fs cpu\n", li + 1, L, (double)(clock() - t0) / CLOCKS_PER_SEC); }
  fprintf(stderr, "solve done %.1fs cpu\n", (double)(clock() - t0) / CLOCKS_PER_SEC);

  if (!strcmp(mode, "dumprand")) {
    srand(seed); char buf[256]; int emitted = 0;
    while (emitted < nrand) {
      int li = rand() % L, stm = rand() & 1, wk = rand() % N, bk = rand() % N;
      uint8_t v = tab[(size_t)li * 2 * NN + stm * NN + wk * N + bk]; if (v == 3) continue;
      int wv = v == 0 ? 0 : ((v == 1) == (stm == 0) ? 1 : -1);
      posstr(li, wk, bk, stm, buf);
      printf("%s | %c\n", buf, wv == 1 ? 'W' : wv == 0 ? 'D' : 'L'); emitted++;
    }
    return 0;
  }
  if (!strcmp(mode, "classify")) {
    char *dup = strdup(posarg); char *save = NULL;
    for (char *pp = strtok_r(dup, ";", &save); pp; pp = strtok_r(NULL, ";", &save)) {
      int wk, bk; u32 w, b; if (!parse_pos(pp, &wk, &bk, &w, &b)) { printf("bad pos %s\n", pp); continue; }
      int li = getLayer(w, b);
      Info I; analyze(li, wk, bk, &I); Res R = classify_root(li, wk, bk);
      printf("== %s\nclass=%s csize=%d maxq=%d  V*(W to move)=%d V*(B to move)=%d (0 draw,1 win,2 loss for mover)\n", pp, CN[R.cls], R.csize, R.maxq,
             tab[(size_t)li * 2 * NN + wk * N + bk], tab[(size_t)li * 2 * NN + NN + wk * N + bk]);
      printf("safe W=%d B=%d  suicide W=%d B=%d  winning W=%d B=%d  leak=%d check=%d  legal W=%d B=%d\n", I.nSafe[0], I.nSafe[1], I.nSuic[0], I.nSuic[1], I.nWin[0], I.nWin[1], I.leak, I.check, I.nlegal[0], I.nlegal[1]);
      char s2[256];
      for (int sd = 0; sd < 2; sd++) for (int i = 0; i < I.nSafe[sd]; i++) { posstr(I.safe[sd][i].tl, I.safe[sd][i].wk, I.safe[sd][i].bk, 1 - sd, s2); printf("  safe %c-move -> %s\n", sd ? 'b' : 'w', s2); }
    }
    return 0;
  }

  outprefix_g = outprefix;
  if (!variants) { census(ALLOWPASSER ? (IGNORELEAK ? "passer_il" : "passer") : (IGNORELEAK ? "strict_il" : "strict")); }
  else { for (int v = 0; v < (variants == 2 ? 2 : 4); v++) { if (variants == 3 && (v & 1)) continue; ALLOWPASSER = v >> 1; IGNORELEAK = v & 1; census(v == 0 ? "strict" : v == 1 ? "strict_il" : v == 2 ? "passer" : "passer_il"); } }
  return 0;
}
