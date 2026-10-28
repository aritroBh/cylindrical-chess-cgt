/* chk.c (K16) -- own checker of the hypotheses of the real-king square rule CONJECTURE (LOOPY Remark 2.11),
 * with its own move generator, and generators of test positions. Independent of kpsolve.c / kp_p.c / cylcgt.
 *
 * Hypotheses (as stated in the Remark), for a legal position y, side to move s, beneficiary beta, pawn p of beta:
 *   (H2) shelter: no pawn of either colour on a file adjacent to the file of beta's king.
 *   (H1) p passed (e.p.-aware: no omega pawn on files f-1,f,f+1 with rho > rho(p); p not capturable e.p. at y)
 *        and every square of p's file ahead of p (promotion square included) is empty of pawns AND kings.
 *   (H4) every other beta pawn on a file adjacent to p's file has rho <= rho(p)+1.
 *   (H5) mu_omega(y;p) >= e+1 in G_omega: p deleted, only omega moves, omega pawns move as in chess, omega's KING
 *        may move one step (not onto its own pawn, not onto beta's king, not adjacent to beta's king; variant KV)
 *        and capture beta's other pawns; e.p. capture offered by y only as first move and only if s = omega.
 *        mu = least number of omega moves after which some omega pawn is on its last rank.
 *        e = d if s = omega, d-1 if s = beta; d = H - rho(p) - [rho(p)=2].
 *   (SQ) d(k_omega, q_j) >= n_j + 2 for j = 0..d (j = 0 only if s = omega); q_0 = p's square, q_1.. after each push of
 *        the strategy "double step first from rho = 2, then single steps", q_d = promotion square;
 *        n_j = j if s = omega, j-1 if s = beta.
 * Variants: KV=0 king step legal ignoring attacks (default), KV=1 also not onto a square attacked by a remaining
 * beta pawn, KV=2 omega king may not move in G_omega.  --drop a,b,c removes hypotheses (controls).
 *
 * Modes:
 *   cert  : read positions on stdin, print "<pos> | <certificates>" (certificate = beta:p ...) or "-".
 *   enum  : exhaustive enumeration (beta = White), --maxw a --maxb b, --shard i/n; writes <out>.pos and <out>.meta
 *   rand  : random positions, --n N --seed S --style uniform|scene|tight; both colours as beta
 * Usage: chk --board cyl:WxH|flat:WxH --mode ... [--kv 0|1|2] [--drop h2,h1k,h1ep,h4,h5,sq] [--out prefix]
 */
#include <ctype.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BIT(s) (1ULL << (s))
enum { WHITE = 0, BLACK = 1 };

static int W, H, N, WRAP, KV = 0;
static int DROP_H2, DROP_H1K, DROP_H1EP, DROP_H4, DROP_H5, DROP_SQ;

typedef struct {
  int wk, bk, stm, ep;
  uint64_t wp, bp;
} Pos;

static inline int fl(int s) { return s % W; }
static inline int rk(int s) { return s / W; }
static int nbfile(int f, int d) {
  int g = f + d;
  if (WRAP) return ((g % W) + W) % W;
  return (g < 0 || g >= W) ? -1 : g;
}
static int kdist(int a, int b) {
  int df = abs(fl(a) - fl(b)), dr = abs(rk(a) - rk(b));
  if (WRAP && W - df < df) df = W - df;
  return df > dr ? df : dr;
}
/* squares attacked by a pawn of colour c standing on s */
static uint64_t patt(int c, int s) {
  int r = rk(s) + (c == WHITE ? 1 : -1);
  if (r < 0 || r >= H) return 0;
  uint64_t m = 0;
  for (int d = -1; d <= 1; d += 2) {
    int f = nbfile(fl(s), d);
    if (f >= 0) m |= BIT(r * W + f);
  }
  return m;
}
static inline int pdir(int c) { return c == WHITE ? 1 : -1; }
static inline int rho(int s, int beta) { return beta == WHITE ? rk(s) + 1 : H - rk(s); }
static int pawn_d(int rh) { return H - rh - (rh == 2); }

/* ---------- legality ---------- */
static int popc(uint64_t x) { return __builtin_popcountll(x); }
static int legal(const Pos *p) {
  if (p->wk == p->bk || kdist(p->wk, p->bk) <= 1) return 0;
  if (p->wp & p->bp) return 0;
  if ((p->wp | p->bp) & (BIT(p->wk) | BIT(p->bk))) return 0;
  for (int s = 0; s < N; s++) {
    if (((p->wp | p->bp) >> s) & 1) {
      int r = rk(s);
      if (r == 0 || r == H - 1) return 0;
    }
  }
  /* side not to move must not be in check by a pawn */
  if (p->stm == WHITE) {
    for (int s = 0; s < N; s++)
      if ((p->wp >> s) & 1 && (patt(WHITE, s) >> p->bk & 1)) return 0;
  } else {
    for (int s = 0; s < N; s++)
      if ((p->bp >> s) & 1 && (patt(BLACK, s) >> p->wk & 1)) return 0;
  }
  if (p->ep >= 0) {
    int mover = !p->stm, sk = p->ep, d = pdir(mover);
    int landed = sk + d * W, origin = sk - d * W;
    if (rk(sk) != (mover == WHITE ? 2 : H - 3)) return 0;
    uint64_t mp = mover == WHITE ? p->wp : p->bp, op = mover == WHITE ? p->bp : p->wp;
    if (!((mp >> landed) & 1)) return 0;
    uint64_t occ = p->wp | p->bp | BIT(p->wk) | BIT(p->bk);
    if (((occ >> sk) & 1) || ((occ >> origin) & 1)) return 0;
    /* we only generate genuine rights: some pawn of the side to move attacks the skipped square */
    int ok = 0;
    for (int s = 0; s < N; s++)
      if ((op >> s) & 1 && (patt(p->stm, s) >> sk & 1)) ok = 1;
    if (!ok) return 0;
  }
  return 1;
}

/* ---------- G_omega search ---------- */
typedef struct {
  int om;               /* omega colour */
  int bk;               /* beta's king */
  int ep;               /* e.p. target usable at the first move, or -1 */
  int epvictim;         /* square of the pawn that could be taken e.p. */
} GCtx;

/* can omega put a pawn on its last rank within L moves?  ops[]: omega pawn squares, bm: beta pawns that remain,
 * ok: omega king square, first: 1 at the root (e.p. allowed) */
static int gsearch(const GCtx *g, int *ops, int no, uint64_t bm, int ok, int L, int first) {
  if (L <= 0) return 0;
  int om = g->om, dir = pdir(om) * W, lastr = om == WHITE ? H - 1 : 0, startr = om == WHITE ? 1 : H - 2;
  /* lower bound prune */
  int best = 99;
  for (int i = 0; i < no; i++) {
    int r = rk(ops[i]);
    int rem = om == WHITE ? lastr - r : r - lastr;
    if (r == startr) rem -= 1;
    if (rem < best) best = rem;
  }
  if (best > L) return 0;
  uint64_t occ = bm | BIT(g->bk) | BIT(ok);
  for (int i = 0; i < no; i++) occ |= BIT(ops[i]);
  for (int i = 0; i < no; i++) {
    int s = ops[i], t = s + dir;
    if (t < 0 || t >= N) continue;
    if (!((occ >> t) & 1)) {
      if (rk(t) == lastr) return 1;
      int save = ops[i];
      ops[i] = t;
      int r = gsearch(g, ops, no, bm, ok, L - 1, 0);
      ops[i] = save;
      if (r) return 1;
      int t2 = t + dir;
      if (rk(s) == startr && !((occ >> t2) & 1)) {
        ops[i] = t2;
        r = gsearch(g, ops, no, bm, ok, L - 1, 0);
        ops[i] = save;
        if (r) return 1;
      }
    }
    uint64_t a = patt(om, s);
    uint64_t cap = a & bm;
    while (cap) {
      int c = __builtin_ctzll(cap);
      cap &= cap - 1;
      int save = ops[i];
      ops[i] = c;
      int r = gsearch(g, ops, no, bm & ~BIT(c), ok, L - 1, 0);
      ops[i] = save;
      if (r) return 1;
    }
    if (first && g->ep >= 0 && ((a >> g->ep) & 1) && ((bm >> g->epvictim) & 1)) {
      int save = ops[i];
      ops[i] = g->ep;
      int r = gsearch(g, ops, no, bm & ~BIT(g->epvictim), ok, L - 1, 0);
      ops[i] = save;
      if (r) return 1;
    }
  }
  if (KV != 2) {
    uint64_t own = 0;
    for (int i = 0; i < no; i++) own |= BIT(ops[i]);
    uint64_t attacked = 0;
    if (KV == 1) {
      uint64_t b = bm;
      int bc = !om;
      while (b) {
        int c = __builtin_ctzll(b);
        b &= b - 1;
        attacked |= patt(bc, c);
      }
    }
    int fo = fl(ok), ro = rk(ok);
    for (int df = -1; df <= 1; df++)
      for (int dr = -1; dr <= 1; dr++) {
        if (!df && !dr) continue;
        int f = nbfile(fo, df), r = ro + dr;
        if (f < 0 || r < 0 || r >= H) continue;
        int t = r * W + f;
        if (t == ok) continue;
        if ((own >> t) & 1) continue;
        if (t == g->bk || kdist(t, g->bk) <= 1) continue;
        if (KV == 1 && ((attacked >> t) & 1)) continue;
        if (gsearch(g, ops, no, bm & ~BIT(t), t, L - 1, 0)) return 1;
      }
  }
  return 0;
}

/* ---------- certificate ---------- */
typedef struct { int d, e, mu_ok; int sqmin; int tightmu; } Info;

/* returns 1 if (y, beta, p) is certified. */
static int cert_one(const Pos *y, int beta, int ps, Info *info) {
  int om = !beta, s = y->stm;
  uint64_t bp = beta == WHITE ? y->wp : y->bp, op = beta == WHITE ? y->bp : y->wp;
  int bk = beta == WHITE ? y->wk : y->bk, ok = beta == WHITE ? y->bk : y->wk;
  int f = fl(ps), rp = rho(ps, beta), db = pdir(beta);
  /* (H2) */
  if (!DROP_H2) {
    for (int d = -1; d <= 1; d += 2) {
      int g = nbfile(fl(bk), d);
      if (g < 0) continue;
      for (int r = 0; r < H; r++)
        if (((y->wp | y->bp) >> (r * W + g)) & 1) return 0;
    }
  }
  /* (H1) passed: omega pawns on files f-1,f,f+1 with rho > rho(p) */
  {
    uint64_t o = op;
    while (o) {
      int q = __builtin_ctzll(o);
      o &= o - 1;
      int g = fl(q);
      int dfm = abs(g - f);
      if (WRAP && W - dfm < dfm) dfm = W - dfm;
      if (dfm <= 1 && rho(q, beta) > rp) return 0;
    }
    if (!DROP_H1EP && s == om && y->ep >= 0 && y->ep == ps - db * W) {
      /* p just double-stepped (mover = beta, landed on ps); capturable if an omega pawn attacks ep */
      uint64_t o2 = op;
      while (o2) {
        int q = __builtin_ctzll(o2);
        o2 &= o2 - 1;
        if ((patt(om, q) >> y->ep) & 1) return 0;
      }
    }
    /* path */
    for (int r = rk(ps) + db; r >= 0 && r < H; r += db) {
      int t = r * W + f;
      if (((y->wp | y->bp) >> t) & 1) return 0;
      if (!DROP_H1K && (t == y->wk || t == y->bk)) return 0;
    }
  }
  /* (H4) */
  if (!DROP_H4) {
    uint64_t b = bp & ~BIT(ps);
    while (b) {
      int q = __builtin_ctzll(b);
      b &= b - 1;
      int dfm = abs(fl(q) - f);
      if (WRAP && W - dfm < dfm) dfm = W - dfm;
      if (dfm == 1 && rho(q, beta) > rp + 1) return 0;
    }
  }
  int d = pawn_d(rp), e = (s == om) ? d : d - 1;
  info->d = d;
  info->e = e;
  /* (SQ) */
  info->sqmin = 99;
  {
    for (int j = 0; j <= d; j++) {
      if (j == 0 && s != om) continue;
      int rj = j == 0 ? rp : (rp == 2 ? rp + j + 1 : rp + j);
      int rank0 = beta == WHITE ? rj - 1 : H - rj;
      int q = rank0 * W + f;
      int nj = s == om ? j : j - 1;
      int m = kdist(ok, q) - (nj + 2);
      if (m < info->sqmin) info->sqmin = m;
      if (!DROP_SQ && m < 0) return 0;
    }
  }
  /* (H5) */
  info->mu_ok = 1;
  info->tightmu = 0;
  if (!DROP_H5 && e >= 1) {
    int ops[8], no = 0;
    uint64_t o = op;
    while (o) {
      int q = __builtin_ctzll(o);
      o &= o - 1;
      ops[no++] = q;
    }
    if (no) {
      GCtx g;
      g.om = om;
      g.bk = bk;
      g.ep = (s == om) ? y->ep : -1;
      g.epvictim = (g.ep >= 0) ? g.ep + db * W : -1;
      if (gsearch(&g, ops, no, bp & ~BIT(ps), ok, e, 1)) return 0;
      info->tightmu = gsearch(&g, ops, no, bp & ~BIT(ps), ok, e + 1, 1);
    }
  }
  return 1;
}

static Info LASTINFO[8];
static int certify(const Pos *y, int beta, int *plist) {
  uint64_t bp = beta == WHITE ? y->wp : y->bp;
  int n = 0;
  while (bp) {
    int ps = __builtin_ctzll(bp);
    bp &= bp - 1;
    Info in;
    if (cert_one(y, beta, ps, &in)) { LASTINFO[n] = in; plist[n++] = ps; }
  }
  return n;
}


/* ---------- full legal move generator (kings and pawns, P model) and the strategy simulation ---------- */
typedef struct { Pos pos; int promo; } Child;
static uint64_t attBy[2][64]; /* attBy[c][s]: squares from which a pawn of colour c attacks s */
static int attInit;
static void init_att(void) {
  if (attInit) return;
  attInit = 1;
  for (int c = 0; c < 2; c++)
    for (int s = 0; s < N; s++) attBy[c][s] = 0;
  for (int c = 0; c < 2; c++)
    for (int s = 0; s < N; s++) {
      uint64_t a = patt(c, s);
      while (a) { int t = __builtin_ctzll(a); a &= a - 1; attBy[c][t] |= BIT(s); }
    }
}
static int gen_moves(const Pos *p, Child *out) {
  int us = p->stm, them = !us, n = 0;
  uint64_t own = us == WHITE ? p->wp : p->bp, opp = us == WHITE ? p->bp : p->wp;
  int ok = us == WHITE ? p->wk : p->bk, ek = us == WHITE ? p->bk : p->wk;
  uint64_t occ = p->wp | p->bp | BIT(p->wk) | BIT(p->bk);
  int fo = fl(ok), ro = rk(ok);
#define SETP(c, mine, theirs, nk) do { Pos q = *p; q.stm = them; q.ep = -1; \
    if (us == WHITE) { q.wp = (mine); q.bp = (theirs); q.wk = (nk); } else { q.bp = (mine); q.wp = (theirs); q.bk = (nk); } \
    out[n].pos = q; out[n].promo = (c); n++; } while (0)
  for (int df = -1; df <= 1; df++)
    for (int dr = -1; dr <= 1; dr++) {
      if (!df && !dr) continue;
      int f = nbfile(fo, df), r = ro + dr;
      if (f < 0 || r < 0 || r >= H) continue;
      int t = r * W + f;
      if (t == ok || ((own >> t) & 1) || t == ek || kdist(t, ek) <= 1) continue;
      uint64_t nopp = opp & ~BIT(t);
      if (nopp & attBy[them][t]) continue;
      SETP(0, own, nopp, t);
    }
  int dir = pdir(us) * W, start = us == WHITE ? 1 : H - 2, last = us == WHITE ? H - 1 : 0;
  int incheck = (opp & attBy[them][ok]) != 0;
  uint64_t o = own;
  while (o) {
    int s = __builtin_ctzll(o);
    o &= o - 1;
    int t = s + dir;
    if (!((occ >> t) & 1) && !incheck) {
      uint64_t nown = (own & ~BIT(s)) | BIT(t);
      if (rk(t) == last) SETP(1, nown, opp, ok);
      else {
        SETP(0, nown, opp, ok);
        int t2 = t + dir;
        if (rk(s) == start && !((occ >> t2) & 1) && rk(t2) != last) {
          uint64_t nown2 = (own & ~BIT(s)) | BIT(t2);
          SETP(0, nown2, opp, ok);
          if (opp & attBy[them][t]) out[n - 1].pos.ep = t; /* genuine e.p. right */
        }
      }
    }
    uint64_t a = patt(us, s);
    while (a) {
      int c = __builtin_ctzll(a);
      a &= a - 1;
      int victim = -1;
      if ((opp >> c) & 1) victim = c;
      else if (c == p->ep) victim = c - dir;
      if (victim < 0 || !((opp >> victim) & 1)) continue;
      uint64_t nopp = opp & ~BIT(victim);
      if (nopp & attBy[them][ok]) continue;
      uint64_t nown = (own & ~BIT(s)) | BIT(c);
      SETP(rk(c) == last, nown, nopp, ok);
    }
  }
#undef SETP
  return n;
}

enum { F_STALE = 1, F_PROMO = 2, F_CAPT = 4, F_BLOCK = 8, F_STALE_ROOT = 16 };
static int simmask;
#define MEMO 16384
static uint64_t memo_key[MEMO];
static int memo_stamp[MEMO], cur_stamp;
static int memo_seen(const Pos *y, int psq) {
  uint64_t h = y->wp * 0x9E3779B97F4A7C15ULL;
  h ^= (y->bp + 0x1234567ULL) * 0xC2B2AE3D27D4EB4FULL;
  h ^= (uint64_t)(y->wk + 64 * y->bk + 4096 * y->stm + 8192 * (y->ep + 1) + 1000000ULL * psq) * 0x165667B19E3779F9ULL;
  h ^= h >> 29;
  uint64_t key = h | 1;
  size_t i = (size_t)(h >> 7) % MEMO;
  for (int k = 0; k < MEMO; k++, i = (i + 1) % MEMO) {
    if (memo_stamp[i] != cur_stamp) { memo_stamp[i] = cur_stamp; memo_key[i] = key; return 0; }
    if (memo_key[i] == key) return 1;
  }
  return 0;
}
/* all lines: beta pushes p (double step first from rho = 2), omega plays every legal move */
static void sim(const Pos *y, int beta, int psq, int depth) {
  if (depth > 12) return;
  if ((simmask & 15) == 15) return;
  if (memo_seen(y, psq)) return;
  int om = !beta;
  Child ch[96];
  int n = gen_moves(y, ch);
  uint64_t bpw = beta == WHITE ? y->wp : y->bp;
  if (y->stm == beta) {
    int rp = rho(psq, beta);
    int db = pdir(beta);
    int tgt = psq + db * W * (rp == 2 ? 2 : 1);
    int found = -1;
    for (int i = 0; i < n; i++) {
      uint64_t nb = beta == WHITE ? ch[i].pos.wp : ch[i].pos.bp;
      if ((nb & ~bpw) == BIT(tgt) && (bpw & ~nb) == BIT(psq)) found = i;
    }
    if (found < 0) { simmask |= F_BLOCK; return; }
    if (ch[found].promo) return; /* beta wins */
    sim(&ch[found].pos, beta, tgt, depth + 1);
  } else {
    if (n == 0) {
      int ok = om == WHITE ? y->wk : y->bk;
      if (!(bpw & attBy[beta][ok])) { simmask |= F_STALE; if (depth == 0) simmask |= F_STALE_ROOT; }
      return;
    }
    for (int i = 0; i < n; i++) {
      if (ch[i].promo) { simmask |= F_PROMO; continue; }
      uint64_t nb = beta == WHITE ? ch[i].pos.wp : ch[i].pos.bp;
      if (!((nb >> psq) & 1)) { simmask |= F_CAPT; continue; }
      sim(&ch[i].pos, beta, psq, depth + 1);
    }
  }
}
static int NOSIM;
static int run_sim(const Pos *y, int beta, int psq) {
  if (NOSIM) return 0;
  init_att();
  simmask = 0;
  cur_stamp++;
  sim(y, beta, psq, 0);
  return simmask;
}
/* static escape hypothesis (H3K): for every square x within distance e-1 of omega's king there is a neighbour t of x,
 * not adjacent to (or on) beta's king, with no pawn of either colour on the files of t, t-1, t+1 */
static int h3k_r(const Pos *y, int beta, int R) {
  int om = !beta, ok = om == WHITE ? y->wk : y->bk, bk = beta == WHITE ? y->wk : y->bk;
  if (R < 0) return 1;
  uint64_t pawns = y->wp | y->bp;
  int filepawn[16] = {0};
  for (int s = 0; s < N; s++) if ((pawns >> s) & 1) filepawn[fl(s)] = 1;
  for (int x = 0; x < N; x++) {
    if (kdist(x, ok) > R) continue;
    int good = 0;
    for (int df = -1; df <= 1 && !good; df++)
      for (int dr = -1; dr <= 1 && !good; dr++) {
        if (!df && !dr) continue;
        int f = nbfile(fl(x), df), r = rk(x) + dr;
        if (f < 0 || r < 0 || r >= H) continue;
        int t = r * W + f;
        if (t == x || kdist(t, bk) <= 1) continue;
        int clean = !filepawn[f];
        for (int d = -1; d <= 1; d += 2) { int g = nbfile(f, d); if (g >= 0 && filepawn[g]) clean = 0; }
        if (clean) good = 1;
      }
    if (!good) return 0;
  }
  return 1;
}

static int h3k(const Pos *y, int beta, int e) { return h3k_r(y, beta, e - 1); }
static int h3_frozen(const Pos *y, int beta) { return h3k_r(y, beta, 0); }

/* ---------- I/O ---------- */
static void sqname(int s, char *o) { sprintf(o, "%c%d", 'a' + fl(s), rk(s) + 1); }
static void fmt_pos(const Pos *p, char *out) {
  char a[8];
  out[0] = 0;
  sqname(p->wk, a); strcat(out, "K"); strcat(out, a);
  sqname(p->bk, a); strcat(out, " k"); strcat(out, a);
  for (int s = 0; s < N; s++)
    if ((p->wp >> s) & 1) { sqname(s, a); strcat(out, " P"); strcat(out, a); }
  for (int s = 0; s < N; s++)
    if ((p->bp >> s) & 1) { sqname(s, a); strcat(out, " p"); strcat(out, a); }
  strcat(out, p->stm == WHITE ? " w " : " b ");
  if (p->ep >= 0) { sqname(p->ep, a); strcat(out, a); }
  else strcat(out, "-");
}
static int parse_sq(const char *s) {
  if (s[0] < 'a' || s[0] >= 'a' + W) return -1;
  int r = atoi(s + 1);
  if (r < 1 || r > H) return -1;
  return (r - 1) * W + (s[0] - 'a');
}
static int parse_pos(const char *line, Pos *p) {
  char buf[512];
  snprintf(buf, sizeof buf, "%s", line);
  memset(p, 0, sizeof *p);
  p->wk = p->bk = -1; p->ep = -1; p->stm = -1;
  int epSeen = 0;
  for (char *t = strtok(buf, " \t\r\n"); t; t = strtok(NULL, " \t\r\n")) {
    if (p->stm < 0 && (!strcmp(t, "w") || !strcmp(t, "b"))) { p->stm = t[0] == 'b'; continue; }
    if (p->stm >= 0 && !epSeen) {
      epSeen = 1;
      if (!strcmp(t, "-")) continue;
      p->ep = parse_sq(t);
      if (p->ep < 0) return 0;
      continue;
    }
    int s = parse_sq(t + 1);
    if (s < 0) return 0;
    switch (t[0]) {
      case 'K': p->wk = s; break;
      case 'k': p->bk = s; break;
      case 'P': p->wp |= BIT(s); break;
      case 'p': p->bp |= BIT(s); break;
      default: return 0;
    }
  }
  if (p->wk < 0 || p->bk < 0 || p->stm < 0 || !epSeen) return 0;
  return legal(p);
}

/* emit certified position to files */
static FILE *fpos, *fmeta;
static long nout, nseen, ncertW, ncertB, nemit;
static const char *flagstr(const Pos *y, int beta, int ps, char *buf) {
  int e = pawn_d(rho(ps, beta));
  if (y->stm != beta) { /* omega to move */ } else e -= 1;
  sprintf(buf, "%x.%d.%d", run_sim(y, beta, ps), h3k(y, beta, e), h3_frozen(y, beta));
  return buf;
}
static void emit_cert(const Pos *y, int sidew, int sideb, int *pw, int *pb) {
  char b[256], a[8], fb[16];
  fmt_pos(y, b);
  fprintf(fpos, "%s\n", b);
  fprintf(fmeta, "%s |", b);
  for (int i = 0; i < sidew; i++) { sqname(pw[i], a); fprintf(fmeta, " W:%s:%s", a, flagstr(y, WHITE, pw[i], fb)); }
  for (int i = 0; i < sideb; i++) { sqname(pb[i], a); fprintf(fmeta, " B:%s:%s", a, flagstr(y, BLACK, pb[i], fb)); }
  fprintf(fmeta, "\n");
  nemit++;
}
static int BETA_ONLY = -1; /* -1 both, else colour tested as beta */
static int SIMONLY, ONLYSTALE;
static long T_s3, T_s3stale, T_s3s1stale_dummy, T_inst, T_s1, T_gap, T_stale, T_staleroot, T_s2, T_s2stale, T_s3, T_s3stale, T_ep, T_tightmu, T_tightsq, T_incheck, T_both, T_gapk[4];
static int tally(const Pos *y, int beta, int ps, const Info *in) {
  char fb[16];
  int e = in->e;
  int mask = run_sim(y, beta, ps);
  int h = h3k(y, beta, e);
  T_inst++;
  if (!(mask & 1)) T_s1++;
  if (mask & 14) T_gap++;
  if (mask & 2) T_gapk[0]++;
  if (mask & 4) T_gapk[1]++;
  if (mask & 8) T_gapk[2]++;
  if (mask & 1) T_stale++;
  if (mask & 16) T_staleroot++;
  if (h) T_s2++;
  if (h && (mask & 1)) T_s2stale++;
  { int h3 = h3_frozen(y, beta); if (h3) T_s3++; if (h3 && (mask & 1)) T_s3stale++; }
  if (y->ep >= 0) T_ep++;
  if (in->tightmu) T_tightmu++;
  if (in->sqmin == 0) T_tightsq++;
  int om = !beta, ok = om == WHITE ? y->wk : y->bk;
  uint64_t bpw = beta == WHITE ? y->wp : y->bp;
  if (bpw & attBy[beta][ok]) T_incheck++;
  (void)fb;
  return mask != 0;
}
static void test_pos(const Pos *y) {
  nseen++;
  int pw[8], pb[8], nw = 0, nb = 0;
  Info iw[8], ib[8];
  if (BETA_ONLY != BLACK) { nw = certify(y, WHITE, pw); memcpy(iw, LASTINFO, sizeof iw); }
  if (BETA_ONLY != WHITE) { nb = certify(y, BLACK, pb); memcpy(ib, LASTINFO, sizeof ib); }
  if (nw) ncertW++;
  if (nb) ncertB++;
  if (nw || nb) {
    if (SIMONLY || ONLYSTALE) {
      init_att();
      nout++;
      if (nw && nb) T_both++;
      int any = 0;
      for (int i = 0; i < nw; i++) { if (tally(y, WHITE, pw[i], &iw[i])) any = 1; }
      for (int i = 0; i < nb; i++) { if (tally(y, BLACK, pb[i], &ib[i])) any = 1; }
      if (ONLYSTALE && any) emit_cert(y, nw, nb, pw, pb);
    } else { nout++; emit_cert(y, nw, nb, pw, pb); }
  }
}

/* ---------- RNG ---------- */
static uint64_t rs[2];
static uint64_t rnext(void) {
  uint64_t s1 = rs[0], s0 = rs[1];
  rs[0] = s0;
  s1 ^= s1 << 23;
  rs[1] = s1 ^ s0 ^ (s1 >> 18) ^ (s0 >> 5);
  return rs[1] + s0;
}
static int rint_(int n) { return (int)(rnext() % (uint64_t)n); }

/* ---------- ep generation: for a position with ep=-1, try all genuine rights ---------- */
static void test_with_eps(Pos *y, int allow_ep) {
  y->ep = -1;
  if (legal(y)) test_pos(y);
  if (!allow_ep) return;
  int mover = !y->stm, d = pdir(mover);
  uint64_t mp = mover == WHITE ? y->wp : y->bp;
  int lr = mover == WHITE ? 3 : H - 4;
  for (int s = 0; s < N; s++) {
    if (!((mp >> s) & 1) || rk(s) != lr) continue;
    y->ep = s - d * W;
    if (legal(y)) test_pos(y);
  }
  y->ep = -1;
}

/* ---------- exhaustive enumeration, beta = White ---------- */
static int sqlist[64], nsq;
static long shard_i, shard_n, shard_ctr;
static int MAXW = 2, MAXB = 2, ALLOWEP = 1, ONLYWK = -1, ONLYBK = -1;

static void enum_black_pawns(Pos *y, int start, int left, int fixed_bk_unused) {
  (void)fixed_bk_unused;
  /* position has white pawns and black pawns chosen so far; place kings and test */
  /* black king anywhere */
  for (int bk = 0; bk < N; bk++) {
    if ((y->wp | y->bp) >> bk & 1) continue;
    if (bk == y->wk || kdist(bk, y->wk) <= 1) continue;
    if (ONLYBK >= 0 && bk != ONLYBK) continue;
    y->bk = bk;
    for (int stm = 0; stm < 2; stm++) {
      y->stm = stm;
      test_with_eps(y, ALLOWEP);
    }
  }
  if (left == 0) return;
  for (int i = start; i < nsq; i++) {
    int s = sqlist[i];
    if ((y->wp >> s) & 1) continue;
    y->bp |= BIT(s);
    enum_black_pawns(y, i + 1, left - 1, 0);
    y->bp &= ~BIT(s);
  }
}
static void enum_white_pawns(Pos *y, int start, int left, int nw) {
  if (nw >= 1) {
    /* shard on (wk, white pawn set) */
    if ((shard_ctr++ % shard_n) == shard_i) enum_black_pawns(y, 0, MAXB, 0);
  }
  if (left == 0) return;
  for (int i = start; i < nsq; i++) {
    int s = sqlist[i];
    y->wp |= BIT(s);
    enum_white_pawns(y, i + 1, left - 1, nw + 1);
    y->wp &= ~BIT(s);
  }
}
static void run_enum(void) {
  for (int wk = 0; wk < N; wk++) {
    if (WRAP && fl(wk) != 0) continue; /* cylinder: rotate so that beta's king stands on file a */
    if (ONLYWK >= 0 && wk != ONLYWK) continue;
    /* H2 shelter: squares of pawns exclude neighbour files of wk's file (unless H2 dropped) */
    nsq = 0;
    for (int s = 0; s < N; s++) {
      int r = rk(s);
      if (r == 0 || r == H - 1) continue;
      if (!DROP_H2) {
        int bad = 0;
        for (int d = -1; d <= 1; d += 2) if (nbfile(fl(wk), d) == fl(s)) bad = 1;
        if (bad) continue;
      }
      if (s == wk) continue;
      sqlist[nsq++] = s;
    }
    Pos y;
    memset(&y, 0, sizeof y);
    y.wk = wk; y.ep = -1;
    enum_white_pawns(&y, 0, MAXW, 0);
  }
}

/* ---------- random generation ---------- */
static int rand_file_near(int pf, int style) {
  /* style 0: uniform; 1: within the strip of pf; 2: mostly within distance 2 of pf */
  if (pf < 0 || style == 0) return rint_(W);
  int f;
  if (style == 1) f = nbfile(pf, rint_(3) - 1);
  else f = (rint_(4) == 0) ? rint_(W) : nbfile(pf, rint_(5) - 2);
  return f < 0 ? rint_(W) : f;
}
/* maxw = max pawns of beta (at least 1), maxb = max pawns of omega */
static void run_rand(long n, int style, int maxw, int maxb) {
  for (long it = 0; it < n; it++) {
    Pos y;
    memset(&y, 0, sizeof y);
    y.ep = -1;
    int beta = (BETA_ONLY >= 0) ? BETA_ONLY : rint_(2);
    int bk = rint_(N), ok;
    do ok = rint_(N); while (ok == bk || kdist(ok, bk) <= 1);
    int nB = 1 + rint_(maxw), nO = rint_(maxb + 1);
    uint64_t bpm = 0, opm = 0;
    int pf = -1, fk = fl(bk);
    if (style == 3) { /* net: omega's king near an edge/corner, other pawns and (often) beta's king close to it */
      int rr = rint_(3) == 0 ? rint_(H) : (rint_(2) ? (beta == WHITE ? H - 1 - rint_(2) : rint_(2)) : (beta == WHITE ? rint_(2) : H - 1 - rint_(2)));
      ok = rr * W + rint_(W);
      if (rint_(2)) { int tries = 0; do { bk = rint_(N); tries++; } while (tries < 50 && (bk == ok || kdist(bk, ok) <= 1 || kdist(bk, ok) > 3)); }
      if (bk == ok || kdist(bk, ok) <= 1) { do bk = rint_(N); while (bk == ok || kdist(bk, ok) <= 1); }
      fk = fl(bk);
    }
    for (int i = 0; i < nB + nO; i++) {
      int isb = i < nB, s = -1;
      for (int tries = 0; tries < 50; tries++) {
        int r = 1 + rint_(H - 2), f = rand_file_near(pf, style);
        if (style == 3 && !(isb && pf < 0)) {
          r = rk(ok) + rint_(5) - 2;
          if (r < 1 || r > H - 2) continue;
          f = nbfile(fl(ok), rint_(5) - 2);
          if (f < 0) continue;
        }
        int t = r * W + f;
        if (((bpm | opm) >> t) & 1 || t == bk || t == ok) continue;
        int bad = 0;
        for (int d = -1; d <= 1; d += 2) if (nbfile(fk, d) == f) bad = 1;
        if (bad && rint_(100) < 97) continue;
        s = t;
        break;
      }
      if (s < 0) continue;
      if (isb) { bpm |= BIT(s); if (pf < 0) pf = fl(s); }
      else opm |= BIT(s);
    }
    if (!bpm) continue;
    y.wk = beta == WHITE ? bk : ok;
    y.bk = beta == WHITE ? ok : bk;
    y.wp = beta == WHITE ? bpm : opm;
    y.bp = beta == WHITE ? opm : bpm;
    for (int stm = 0; stm < 2; stm++) {
      y.stm = stm;
      test_with_eps(&y, rint_(3) == 0);
    }
  }
}

static void parse_drop(char *a) {
  for (char *t = strtok(a, ","); t; t = strtok(NULL, ",")) {
    if (!strcmp(t, "h2")) DROP_H2 = 1;
    else if (!strcmp(t, "h1k")) DROP_H1K = 1;
    else if (!strcmp(t, "h1ep")) DROP_H1EP = 1;
    else if (!strcmp(t, "h4")) DROP_H4 = 1;
    else if (!strcmp(t, "h5")) DROP_H5 = 1;
    else if (!strcmp(t, "sq")) DROP_SQ = 1;
    else { fprintf(stderr, "bad drop %s\n", t); exit(2); }
  }
}

int main(int argc, char **argv) {
  const char *mode = "cert", *out = "chk_out", *style = "uniform";
  long n = 1000, seed = 1;
  for (int i = 1; i < argc; i++) {
    if (!strcmp(argv[i], "--board") && i + 1 < argc) {
      char kind[8];
      if (sscanf(argv[++i], "%7[a-z]:%dx%d", kind, &W, &H) != 3) return 2;
      WRAP = !strcmp(kind, "cyl");
    } else if (!strcmp(argv[i], "--mode")) mode = argv[++i];
    else if (!strcmp(argv[i], "--kv")) KV = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--drop")) parse_drop(argv[++i]);
    else if (!strcmp(argv[i], "--out")) out = argv[++i];
    else if (!strcmp(argv[i], "--maxw")) MAXW = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--maxb")) MAXB = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--n")) n = atol(argv[++i]);
    else if (!strcmp(argv[i], "--seed")) seed = atol(argv[++i]);
    else if (!strcmp(argv[i], "--style")) style = argv[++i];
    else if (!strcmp(argv[i], "--noep")) ALLOWEP = 0;
    else if (!strcmp(argv[i], "--wk")) ONLYWK = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--bk")) ONLYBK = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--nosim")) NOSIM = 1;
    else if (!strcmp(argv[i], "--simonly")) SIMONLY = 1;
    else if (!strcmp(argv[i], "--onlystale")) ONLYSTALE = 1;
    else if (!strcmp(argv[i], "--beta")) BETA_ONLY = argv[++i][0] == 'W' ? WHITE : BLACK;
    else if (!strcmp(argv[i], "--shard")) { if (sscanf(argv[++i], "%ld/%ld", &shard_i, &shard_n) != 2) return 2; }
    else { fprintf(stderr, "bad arg %s\n", argv[i]); return 2; }
  }
  if (!W) { fprintf(stderr, "need --board\n"); return 2; }
  N = W * H;
  if (!shard_n) shard_n = 1;
  rs[0] = 0x9E3779B97F4A7C15ULL ^ (uint64_t)seed * 0xD1B54A32D192ED03ULL;
  rs[1] = 0xBF58476D1CE4E5B9ULL + (uint64_t)seed;
  for (int i = 0; i < 20; i++) rnext();
  if (!strcmp(mode, "moves")) { /* debugging: list the legal moves (children) of each position */
    char line[512];
    init_att();
    while (fgets(line, sizeof line, stdin)) {
      Pos y;
      size_t L = strlen(line);
      while (L && (line[L - 1] == '\n' || line[L - 1] == '\r')) line[--L] = 0;
      if (!parse_pos(line, &y)) { printf("X\n"); continue; }
      Child ch[96];
      int n = gen_moves(&y, ch);
      printf("%d\n", n);
      for (int i = 0; i < n; i++) { char b[256]; fmt_pos(&ch[i].pos, b); printf("%s%s\n", ch[i].promo ? "PROMO " : "", b); }
    }
    return 0;
  }
  if (!strcmp(mode, "cert")) {
    char line[512];
    while (fgets(line, sizeof line, stdin)) {
      size_t L = strlen(line);
      while (L && (line[L - 1] == '\n' || line[L - 1] == '\r')) line[--L] = 0;
      if (line[0] == '#' || !line[0]) { printf("%s\n", line); continue; }
      Pos y;
      if (!parse_pos(line, &y)) { printf("%s | X\n", line); continue; }
      int pw[8], pb[8];
      int nw = certify(&y, WHITE, pw), nb = certify(&y, BLACK, pb);
      printf("%s |", line);
      char a[8];
      if (!nw && !nb) printf(" -");
      char fb[16];
      for (int i = 0; i < nw; i++) { sqname(pw[i], a); printf(" W:%s:%s", a, flagstr(&y, WHITE, pw[i], fb)); }
      for (int i = 0; i < nb; i++) { sqname(pb[i], a); printf(" B:%s:%s", a, flagstr(&y, BLACK, pb[i], fb)); }
      printf("\n");
    }
    return 0;
  }
  char fn[512];
  if (SIMONLY) { fpos = fmeta = fopen("/dev/null", "w"); }
  else {
  snprintf(fn, sizeof fn, "%s.pos", out); fpos = fopen(fn, "w");
  snprintf(fn, sizeof fn, "%s.meta", out); fmeta = fopen(fn, "w");
  }
  if (!fpos || !fmeta) return 2;
  if (!strcmp(mode, "enum")) {
    if (BETA_ONLY < 0) BETA_ONLY = WHITE; /* exhaustive runs use beta = White (flip symmetry covers Black) */
    run_enum();
  } else if (!strcmp(mode, "rand")) {
    int st = !strcmp(style, "scene") ? 1 : !strcmp(style, "tight") ? 2 : !strcmp(style, "net") ? 3 : 0;
    run_rand(n, st, MAXW, MAXB);
  } else return 2;
  fclose(fpos); if (fmeta != fpos) fclose(fmeta);
  if (SIMONLY || ONLYSTALE)
    printf("{\"seen\":%ld,\"cert_positions\":%ld,\"instances\":%ld,\"S1_instances\":%ld,\"stalemate_instances\":%ld,\"stalemate_at_y\":%ld,"
           "\"gap_instances\":%ld,\"gap_promo\":%ld,\"gap_capt\":%ld,\"gap_block\":%ld,\"S2_instances\":%ld,\"S2_but_stalemate\":%ld,"
           "\"S3_instances\":%ld,\"S3_but_stalemate\":%ld,\"with_ep\":%ld,\"tight_mu\":%ld,\"tight_sq\":%ld,\"omega_in_check\":%ld,\"both_colours\":%ld}\n",
           nseen, nout, T_inst, T_s1, T_stale, T_staleroot, T_gap, T_gapk[0], T_gapk[1], T_gapk[2], T_s2, T_s2stale, T_s3, T_s3stale, T_ep, T_tightmu, T_tightsq, T_incheck, T_both);
  fprintf(stderr, "chk: %s seen=%ld certified positions=%ld emitted=%ld (with W cert %ld, B cert %ld)\n", mode, nseen, nout, nemit, ncertW, ncertB);
  return 0;
}
