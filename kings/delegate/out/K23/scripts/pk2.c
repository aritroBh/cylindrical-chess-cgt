/* pk2.c -- independent exact solver for the P model (K23).
 * Kings + pawns only, flat or cylinder, first promotion by either side ends the game as a win for the promoter,
 * stalemate = draw, checkmate = loss, infinite play = draw (least fixed point).
 * Optional --frozen: a king move loses at once for the mover (the "convention" model), promotion wins at once.
 * Written from the rules only (not from kpsolve.c). Layers = (white pawns, black pawns, e.p. square);
 * inside a layer only kings move (naive value iteration to the least fixed point); pawn moves leave the layer.
 * Usage: pk2 --board cyl:WxH|flat:WxH [--frozen] [--noep] < positions > results
 * Position: tokens like Ka4 pb3 ... then w|b then e.p. square or -
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef uint64_t u64;
static int W, H, N, WRAP, FROZEN = 0, NOEP = 0;
enum { UNK = 0, WIN = 1, LOSS = 2, DRAW = 3, ILL = 4 };

static int sq(int f, int r) { return r * W + f; }
/* neighbour with file offset df (wrap if cylinder); -1 if off board */
static int nb(int s, int df, int dr) {
  int f = s % W + df, r = s / W + dr;
  if (r < 0 || r >= H) return -1;
  if (WRAP) f = ((f % W) + W) % W; else if (f < 0 || f >= W) return -1;
  return sq(f, r);
}

typedef struct Layer {
  u64 wp, bp; int ep; /* ep: target square or -1 (the pawn to be captured stands behind it) */
  unsigned char *v;   /* index ((wk*N+bk)*2+stm) */
  struct Layer *next;
} Layer;
#define HS (1 << 20)
static Layer *tab[HS];

static unsigned hsh(u64 wp, u64 bp, int ep) {
  u64 x = wp * 0x9E3779B97F4A7C15ULL ^ (bp + 0x1234567ULL) * 0xC2B2AE3D27D4EB4FULL ^ (u64)(ep + 2) * 0x165667B19E3779F9ULL;
  x ^= x >> 29; x *= 0xBF58476D1CE4E5B9ULL; x ^= x >> 32;
  return (unsigned)(x & (HS - 1));
}

/* is square t attacked by a pawn of colour c, given the pawn set pc of that colour? colour 0 white (moves up) */
static int pawn_attacks(u64 pc, int c, int t) {
  int dr = c == 0 ? -1 : 1; /* attacker stands one rank behind t */
  for (int df = -1; df <= 1; df += 2) {
    int s = nb(t, df, dr);
    if (s >= 0 && (pc >> s & 1)) return 1;
  }
  return 0;
}
static int adjacent(int a, int b) {
  if (a == b) return 0;
  for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
    if (!df && !dr) continue;
    if (nb(a, df, dr) == b) return 1;
  }
  return 0;
}

static Layer *solve_layer(u64 wp, u64 bp, int ep);

/* child description */
typedef struct { Layer *L; int idx; int term; /* term: 0 normal, 1 = mover wins at once (promotion) */ } Child;

static int legalpos(u64 wp, u64 bp, int wk, int bk, int stm, int ep) {
  if (wk == bk || adjacent(wk, bk)) return 0;
  if ((wp >> wk & 1) || (bp >> wk & 1) || (wp >> bk & 1) || (bp >> bk & 1)) return 0;
  if (wp & bp) return 0;
  for (int s = 0; s < N; s++) {
    if ((wp >> s & 1) && (s / W == 0 || s / W == H - 1)) return 0;
    if ((bp >> s & 1) && (s / W == 0 || s / W == H - 1)) return 0;
  }
  /* side not to move must not be in check */
  if (stm == 0) { if (pawn_attacks(wp, 0, bk)) return 0; }
  else { if (pawn_attacks(bp, 1, wk)) return 0; }
  (void)ep;
  return 1;
}

/* generate children of position; returns count. ischeck set to whether mover is in check. */
static int gen(u64 wp, u64 bp, int wk, int bk, int stm, int ep, Child *out, int *ischeck) {
  int n = 0, us = stm;
  u64 mine = us == 0 ? wp : bp, theirs = us == 0 ? bp : wp;
  int ok = us == 0 ? wk : bk, ek = us == 0 ? bk : wk;
  *ischeck = pawn_attacks(theirs, !us, ok);
  /* king moves */
  for (int df = -1; df <= 1; df++) for (int dr = -1; dr <= 1; dr++) {
    if (!df && !dr) continue;
    int t = nb(ok, df, dr);
    if (t < 0 || t == ek || adjacent(t, ek)) continue;
    if (mine >> t & 1) continue;
    u64 th2 = theirs & ~(1ULL << t);
    if (pawn_attacks(th2, !us, t)) continue;
    Child c; c.term = 0;
    int nwk = us == 0 ? t : wk, nbk = us == 0 ? bk : t;
    u64 nwp = us == 0 ? wp : th2, nbp = us == 0 ? th2 : bp;
    c.L = solve_layer(nwp, nbp, -1);
    c.idx = ((nwk * N + nbk) * 2 + !us);
    out[n++] = c;
  }
  if (FROZEN) return n; /* pawn moves below are still generated; king moves are handled by caller */
  return n;
}

static int genpawn(u64 wp, u64 bp, int wk, int bk, int stm, int ep, Child *out, int firstidx) {
  int n = firstidx, us = stm;
  u64 mine = us == 0 ? wp : bp, theirs = us == 0 ? bp : wp;
  int ok = us == 0 ? wk : bk, ek = us == 0 ? bk : wk;
  int dir = us == 0 ? 1 : -1, last = us == 0 ? H - 1 : 0, start = us == 0 ? 1 : H - 2;
  u64 occ = wp | bp | (1ULL << wk) | (1ULL << bk);
  for (int s = 0; s < N; s++) {
    if (!(mine >> s & 1)) continue;
    int r = s / W;
    /* pushes */
    int t1 = nb(s, 0, dir);
    if (t1 >= 0 && !(occ >> t1 & 1)) {
      u64 nm = (mine & ~(1ULL << s)) | (t1 / W == last ? 0 : (1ULL << t1));
      u64 nwp = us == 0 ? nm : theirs, nbp = us == 0 ? theirs : nm;
      if (!pawn_attacks(us == 0 ? nbp : nwp, !us, ok)) {
        Child c;
        if (t1 / W == last) { c.term = 1; c.L = 0; c.idx = 0; }
        else { c.term = 0; c.L = solve_layer(nwp, nbp, -1); c.idx = ((wk * N + bk) * 2 + !us); }
        out[n++] = c;
      }
      if (r == start) {
        int t2 = nb(t1, 0, dir);
        if (t2 >= 0 && !(occ >> t2 & 1)) {
          u64 nm2 = (mine & ~(1ULL << s)) | (1ULL << t2);
          u64 nwp2 = us == 0 ? nm2 : theirs, nbp2 = us == 0 ? theirs : nm2;
          if (!pawn_attacks(us == 0 ? nbp2 : nwp2, !us, ok)) {
            int e = -1;
            if (!NOEP) {
              /* an enemy pawn adjacent to t2 on the same rank could capture e.p. */
              for (int df = -1; df <= 1; df += 2) {
                int a = nb(t2, df, 0);
                if (a >= 0 && (theirs >> a & 1)) e = t1;
              }
            }
            Child c; c.term = 0; c.L = solve_layer(nwp2, nbp2, e); c.idx = ((wk * N + bk) * 2 + !us);
            out[n++] = c;
          }
        }
      }
    }
    /* captures */
    for (int df = -1; df <= 1; df += 2) {
      int t = nb(s, df, dir);
      if (t < 0) continue;
      int cap = (theirs >> t & 1);
      int epcap = (ep == t && !cap);
      if (!cap && !epcap) continue;
      if (t == ek) continue;
      u64 nth = theirs;
      if (cap) nth &= ~(1ULL << t);
      if (epcap) { int victim = nb(t, 0, -dir); nth &= ~(1ULL << victim); }
      u64 nm = (mine & ~(1ULL << s)) | (t / W == last ? 0 : (1ULL << t));
      u64 nwp = us == 0 ? nm : nth, nbp = us == 0 ? nth : nm;
      if (pawn_attacks(us == 0 ? nbp : nwp, !us, ok)) continue;
      Child c;
      if (t / W == last) { c.term = 1; c.L = 0; c.idx = 0; }
      else { c.term = 0; c.L = solve_layer(nwp, nbp, -1); c.idx = ((wk * N + bk) * 2 + !us); }
      out[n++] = c;
    }
  }
  return n;
}

static Layer *solve_layer(u64 wp, u64 bp, int ep) {
  unsigned h = hsh(wp, bp, ep);
  for (Layer *L = tab[h]; L; L = L->next) if (L->wp == wp && L->bp == bp && L->ep == ep) return L;
  Layer *L = calloc(1, sizeof *L);
  L->wp = wp; L->bp = bp; L->ep = ep;
  L->v = calloc((size_t)N * N * 2, 1);
  L->next = tab[h]; tab[h] = L; /* register before recursion is safe: children are different layers except king-moves (ep=-1 same layer) */
  int NP = N * N * 2;
  Child (*ch)[48] = malloc(sizeof(Child[48]) * (size_t)NP);
  unsigned char *nc = calloc(NP, 1), *chk = calloc(NP, 1);
  /* children: king moves stay in this layer (ep = -1) or go to the ep=-1 layer of the same pawns (if ep>=0) */
  for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) for (int stm = 0; stm < 2; stm++) {
    int i = (wk * N + bk) * 2 + stm;
    if (!legalpos(wp, bp, wk, bk, stm, ep)) { L->v[i] = ILL; continue; }
    int ic;
    Child tmp[64];
    int n = gen(wp, bp, wk, bk, stm, ep, tmp, &ic);
    if (FROZEN) { /* a king move loses at once for its maker: treat it as a move to a LOSS-for-mover... */
      for (int k = 0; k < n; k++) { tmp[k].term = 2; } /* term 2: king move in frozen model, mover loses */
    }
    n = genpawn(wp, bp, wk, bk, stm, ep, tmp, n);
    if (n > 48) { fprintf(stderr, "too many moves %d\n", n); exit(3); }
    memcpy(ch[i], tmp, sizeof(Child) * n);
    nc[i] = n; chk[i] = ic;
  }
  /* value iteration */
  int changed = 1;
  while (changed) {
    changed = 0;
    for (int i = 0; i < NP; i++) {
      if (L->v[i] == WIN || L->v[i] == LOSS || L->v[i] == ILL) continue;
      int n = nc[i];
      if (n == 0) {
        int nv = chk[i] ? LOSS : DRAW;
        if (L->v[i] != nv) { L->v[i] = nv; if (nv != DRAW) changed = 1; else L->v[i] = DRAW; }
        continue;
      }
      int allwin = 1, anyloss = 0;
      for (int k = 0; k < n; k++) {
        int cv; /* value for the opponent (child mover) */
        Child *c = &ch[i][k];
        if (c->term == 1) cv = LOSS;       /* mover promotes: opponent loses */
        else if (c->term == 2) cv = WIN;   /* frozen king move: opponent (child mover) wins */
        else {
          Layer *CL = c->L;
          cv = CL->v[c->idx];
          if (CL == L) { /* same layer: value may be UNK/DRAW so far */ }
        }
        if (cv == LOSS) { anyloss = 1; break; }
        if (cv != WIN) allwin = 0;
      }
      if (anyloss) { L->v[i] = WIN; changed = 1; }
      else if (allwin) { L->v[i] = LOSS; changed = 1; }
      else L->v[i] = UNK;
    }
  }
  for (int i = 0; i < NP; i++) if (L->v[i] == UNK) L->v[i] = DRAW;
  free(ch); free(nc); free(chk);
  return L;
}

static int parsesq(const char *s) { return sq(s[0] - 'a', s[1] - '1'); }

int main(int argc, char **argv) {
  const char *bd = 0;
  for (int i = 1; i < argc; i++) {
    if (!strcmp(argv[i], "--board") && i + 1 < argc) bd = argv[++i];
    else if (!strcmp(argv[i], "--frozen")) FROZEN = 1;
    else if (!strcmp(argv[i], "--noep")) NOEP = 1;
    else { fprintf(stderr, "bad arg\n"); return 2; }
  }
  if (!bd) return 2;
  char kind[8]; if (sscanf(bd, "%7[a-z]:%dx%d", kind, &W, &H) != 3) return 2;
  WRAP = !strcmp(kind, "cyl"); N = W * H;
  char line[512];
  while (fgets(line, sizeof line, stdin)) {
    line[strcspn(line, "\n")] = 0;
    if (line[0] == '#' || !line[0]) { puts(line); continue; }
    char buf[512]; strcpy(buf, line);
    u64 wp = 0, bp = 0; int wk = -1, bk = -1, stm = 0, ep = -1;
    char *tok = strtok(buf, " ");
    while (tok) {
      if (!strcmp(tok, "w")) stm = 0;
      else if (!strcmp(tok, "b")) stm = 1;
      else if (!strcmp(tok, "-")) ep = -1;
      else if (tok[0] == 'K') wk = parsesq(tok + 1);
      else if (tok[0] == 'k') bk = parsesq(tok + 1);
      else if (tok[0] == 'P') wp |= 1ULL << parsesq(tok + 1);
      else if (tok[0] == 'p') bp |= 1ULL << parsesq(tok + 1);
      else if (tok[0] >= 'a' && tok[0] <= 'h' && tok[1] >= '1' && tok[1] <= '8') ep = parsesq(tok);
      tok = strtok(0, " ");
    }
    if (!legalpos(wp, bp, wk, bk, stm, ep)) { printf("%s | X X\n", line); continue; }
    Layer *L = solve_layer(wp, bp, ep);
    int v = L->v[(wk * N + bk) * 2 + stm];
    /* from White's point of view */
    int r = v == DRAW ? 'D' : ((v == WIN) == (stm == 0) ? 'W' : 'L');
    printf("%s | %c %c\n", line, r, r);
  }
  return 0;
}
