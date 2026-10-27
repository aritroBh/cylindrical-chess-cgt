/* mine.c -- K24: an independent exact solver for king-and-pawn positions in the *promotion models*.
 * Written from the rules of kings/SPEC.md only (not from kpsolve.c or kings/ref).  Method: forward
 * exploration of the reachable positions from the queries into a hash table, then counting retrograde
 * analysis on the explicit move graph (least fixed point: whatever is never resolved is a draw).
 *
 * Models (--model):
 *   p     P: chess, but the first promotion ends the game as a win for the promoter (LOOPY Definition 1.5).
 *         Checkmate wins, stalemate and infinite play are draws.
 *   bb    "Black may not usefully promote": every promotion by either side is a WIN FOR WHITE.
 *         If White cannot force a win here, Black has a chess strategy that never promotes and White never wins C.
 *   bw    every promotion by either side is a WIN FOR BLACK (the mirror): if Black cannot force a win here,
 *         White has a strategy that never lets Black win C.
 * Board: --board cyl:WxH | flat:WxH, --ep on|off.  Input: lines "Kh5 Pa4 kb4 pa5 w -" (SPEC.md format, the last
 * token is the e.p. target square or -).  Output "<line> | R" with R in W D L (White's point of view),
 * plus with --moves the value after each legal move (promotions print as 'W' or 'L' with a '=' sign).
 *
 * Build: cc -O2 -o mine mine.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXP 3
static int W, H, WRAP = 1, EPON = 1, MODEL = 0; /* 0 p, 1 bb, 2 bw */
static int NSQ;

typedef struct {
  int stm;         /* 0 white, 1 black */
  int k[2];        /* king squares */
  int np[2];
  int p[2][MAXP];  /* sorted pawn squares */
  int ep;          /* e.p. target square or -1 */
} Pos;

static inline int sqf(int s) { return s % W; }
static inline int sqr(int s) { return s / W; }
static int dirof(int c) { return c == 0 ? 1 : -1; }
static int lastrank(int c) { return c == 0 ? H - 1 : 0; }
static int startrank(int c) { return c == 0 ? 1 : H - 2; }

/* the square at (f+df, r+dr), or -1 */
static int stepsq(int s, int df, int dr) {
  int f = sqf(s) + df, r = sqr(s) + dr;
  if (r < 0 || r >= H) return -1;
  if (WRAP) f = ((f % W) + W) % W;
  else if (f < 0 || f >= W) return -1;
  return r * W + f;
}

static int kings_adjacent(int a, int b) {
  if (a == b) return 1;
  int dr = sqr(a) - sqr(b);
  if (dr < -1 || dr > 1) return 0;
  int df = sqf(a) - sqf(b);
  if (df < 0) df = -df;
  if (WRAP && W - df < df) df = W - df;
  return df <= 1;
}

static int has_pawn(const Pos *q, int c, int s) {
  for (int i = 0; i < q->np[c]; i++) if (q->p[c][i] == s) return 1;
  return 0;
}
static int pawn_color_at(const Pos *q, int s) { /* -1 none, 0 white pawn, 1 black pawn */
  if (has_pawn(q, 0, s)) return 0;
  if (has_pawn(q, 1, s)) return 1;
  return -1;
}
static int occupied(const Pos *q, int s) { return q->k[0] == s || q->k[1] == s || pawn_color_at(q, s) >= 0; }

/* is square s attacked by a pawn of colour c? */
static int attacked_by_pawn(const Pos *q, int s, int c) {
  int r0 = sqr(s) - dirof(c);
  if (r0 < 0 || r0 >= H) return 0;
  for (int df = -1; df <= 1; df += 2) {
    int f = sqf(s) + df;
    if (WRAP) f = ((f % W) + W) % W;
    else if (f < 0 || f >= W) continue;
    if (has_pawn(q, c, r0 * W + f)) return 1;
  }
  return 0;
}
/* is the king of colour c in check? (only pawns can give check here) */
static int in_check(const Pos *q, int c) { return attacked_by_pawn(q, q->k[c], 1 - c); }

static void sortp(Pos *q) {
  for (int c = 0; c < 2; c++)
    for (int i = 1; i < q->np[c]; i++) {
      int v = q->p[c][i], j = i - 1;
      while (j >= 0 && q->p[c][j] > v) { q->p[c][j + 1] = q->p[c][j]; j--; }
      q->p[c][j + 1] = v;
    }
}
static void del_pawn(Pos *q, int c, int s) {
  int j = 0;
  for (int i = 0; i < q->np[c]; i++) if (q->p[c][i] != s) q->p[c][j++] = q->p[c][i];
  q->np[c] = j;
}
static void move_pawn(Pos *q, int c, int from, int to) {
  for (int i = 0; i < q->np[c]; i++) if (q->p[c][i] == from) q->p[c][i] = to;
}

static uint64_t pack(const Pos *q) {
  uint64_t key = (uint64_t)q->k[0] | ((uint64_t)q->k[1] << 6) | ((uint64_t)q->stm << 12) | ((uint64_t)(q->ep + 1) << 13);
  int sh = 20;
  for (int c = 0; c < 2; c++)
    for (int i = 0; i < MAXP; i++, sh += 7) key |= (uint64_t)(i < q->np[c] ? q->p[c][i] + 1 : 0) << sh;
  return key;
}
static void unpack(uint64_t key, Pos *q) {
  q->k[0] = key & 63; q->k[1] = (key >> 6) & 63; q->stm = (key >> 12) & 1; q->ep = (int)((key >> 13) & 127) - 1;
  int sh = 20;
  for (int c = 0; c < 2; c++) {
    q->np[c] = 0;
    for (int i = 0; i < MAXP; i++, sh += 7) {
      int v = (int)((key >> sh) & 127);
      if (v) q->p[c][q->np[c]++] = v - 1;
    }
  }
}

/* ---- move generation ---- */
typedef struct {
  int nsucc;           /* normal successors */
  Pos succ[160];
  char txt[160][12];
  int nwin;            /* promotions that win for the mover */
  int nbad;            /* promotions that lose for the mover */
  char wtxt[16][12], btxt[16][12];
} Moves;

static const int KDF[8] = {0, 0, 1, -1, 1, 1, -1, -1};
static const int KDR[8] = {1, -1, 0, 0, 1, -1, 1, -1};

static void sqname(int s, char *o) { o[0] = 'a' + sqf(s); o[1] = '1' + sqr(s); o[2] = 0; }

static void add_succ(Moves *m, Pos *n, const char *t) {
  n->stm = 1 - n->stm;
  sortp(n);
  m->succ[m->nsucc] = *n;
  strncpy(m->txt[m->nsucc], t, 11);
  m->txt[m->nsucc][11] = 0;
  m->nsucc++;
}
static void add_promo(Moves *m, int mover, const char *t) {
  /* who wins: model p -> the promoter; bb -> White; bw -> Black */
  int winner = MODEL == 0 ? mover : (MODEL == 1 ? 0 : 1);
  if (winner == mover) { strncpy(m->wtxt[m->nwin++], t, 11); }
  else { strncpy(m->btxt[m->nbad++], t, 11); }
}

static void gen(const Pos *q, Moves *m) {
  int c = q->stm, e = 1 - c, d = dirof(c);
  char a[4], b[4], t[12];
  m->nsucc = m->nwin = m->nbad = 0;
  /* king moves */
  for (int i = 0; i < 8; i++) {
    int to = stepsq(q->k[c], KDF[i], KDR[i]);
    if (to < 0) continue;
    if (has_pawn(q, c, to)) continue;
    if (kings_adjacent(to, q->k[e])) continue;
    Pos n = *q;
    n.ep = -1;
    n.k[c] = to;
    if (has_pawn(&n, e, to)) del_pawn(&n, e, to);
    if (attacked_by_pawn(&n, to, e)) continue;
    sqname(q->k[c], a); sqname(to, b);
    snprintf(t, sizeof t, "K%s%s", a, b);
    add_succ(m, &n, t);
  }
  /* pawn moves */
  for (int i = 0; i < q->np[c]; i++) {
    int s = q->p[c][i];
    int one = stepsq(s, 0, d);
    if (one < 0) continue;
    int lastr = (sqr(one) == lastrank(c));
    if (!occupied(q, one)) {
      Pos n = *q;
      n.ep = -1;
      if (lastr) {
        del_pawn(&n, c, s);
        if (!attacked_by_pawn(&n, n.k[c], e)) { sqname(s, a); sqname(one, b); snprintf(t, sizeof t, "P%s%s=", a, b); add_promo(m, c, t); }
      } else {
        move_pawn(&n, c, s, one);
        if (!attacked_by_pawn(&n, n.k[c], e)) {
          sqname(s, a); sqname(one, b); snprintf(t, sizeof t, "P%s%s", a, b);
          add_succ(m, &n, t);
        }
      }
      /* double step */
      if (sqr(s) == startrank(c)) {
        int two = stepsq(one, 0, d);
        if (two >= 0 && !occupied(q, two)) {
          Pos n2 = *q;
          n2.ep = -1;
          if (sqr(two) == lastrank(c)) { /* H = 4: lands on the last rank, promotes */
            del_pawn(&n2, c, s);
            if (!attacked_by_pawn(&n2, n2.k[c], e)) { sqname(s, a); sqname(two, b); snprintf(t, sizeof t, "P%s%s=", a, b); add_promo(m, c, t); }
          } else {
            move_pawn(&n2, c, s, two);
            if (!attacked_by_pawn(&n2, n2.k[c], e)) {
              if (EPON) {
                for (int df = -1; df <= 1; df += 2) {
                  int es = stepsq(two, df, 0);
                  if (es >= 0 && has_pawn(&n2, e, es)) { n2.ep = one; break; }
                }
              }
              sqname(s, a); sqname(two, b); snprintf(t, sizeof t, "P%s%s", a, b);
              add_succ(m, &n2, t);
            }
          }
        }
      }
    }
    /* captures */
    for (int df = -1; df <= 1; df += 2) {
      int to = stepsq(s, df, d);
      if (to < 0) continue;
      int pc = pawn_color_at(q, to);
      int epcap = 0;
      if (pc == e) { /* ordinary capture */ }
      else if (pc < 0 && q->ep == to && !occupied(q, to)) epcap = 1;
      else continue;
      Pos n = *q;
      n.ep = -1;
      if (epcap) {
        int victim = stepsq(to, 0, -d);
        if (victim < 0 || !has_pawn(&n, e, victim)) continue;
        del_pawn(&n, e, victim);
      } else del_pawn(&n, e, to);
      if (sqr(to) == lastrank(c)) {
        del_pawn(&n, c, s);
        if (!attacked_by_pawn(&n, n.k[c], e)) { sqname(s, a); sqname(to, b); snprintf(t, sizeof t, "P%sx%s=", a, b); add_promo(m, c, t); }
      } else {
        move_pawn(&n, c, s, to);
        if (!attacked_by_pawn(&n, n.k[c], e)) {
          sqname(s, a); sqname(to, b);
          snprintf(t, sizeof t, "P%sx%s%s", a, b, epcap ? "ep" : "");
          add_succ(m, &n, t);
        }
      }
    }
  }
}

/* ---- parsing ---- */
static int parse_sq(const char *s) {
  if (s[0] < 'a' || s[0] >= 'a' + W || s[1] < '1' || s[1] >= '1' + H) return -1;
  return (s[1] - '1') * W + (s[0] - 'a');
}
static int parse_pos(const char *line, Pos *q) {
  memset(q, 0, sizeof *q);
  q->k[0] = q->k[1] = -1; q->ep = -1;
  char buf[256];
  strncpy(buf, line, 255); buf[255] = 0;
  char *save, *tok;
  int stmset = 0;
  for (tok = strtok_r(buf, " \t\r\n", &save); tok; tok = strtok_r(NULL, " \t\r\n", &save)) {
    if (!strcmp(tok, "w") || !strcmp(tok, "b")) { q->stm = tok[0] == 'b'; stmset = 1; continue; }
    if (!strcmp(tok, "-")) continue;
    char ch = tok[0];
    int s = parse_sq(tok + 1);
    if (ch == 'K' || ch == 'k' || ch == 'P' || ch == 'p') {
      if (s < 0) return 0;
      int c = (ch == 'K' || ch == 'P') ? 0 : 1;
      if (ch == 'K' || ch == 'k') q->k[c] = s;
      else { if (q->np[c] >= MAXP) return 0; q->p[c][q->np[c]++] = s; }
    } else {
      s = parse_sq(tok);
      if (s < 0) return 0;
      q->ep = s;
    }
  }
  if (!stmset || q->k[0] < 0 || q->k[1] < 0) return 0;
  sortp(q);
  /* legality */
  if (kings_adjacent(q->k[0], q->k[1])) return 0;
  for (int c = 0; c < 2; c++) for (int i = 0; i < q->np[c]; i++) {
    int s = q->p[c][i];
    if (sqr(s) == 0 || sqr(s) == H - 1) return 0;
    if (s == q->k[0] || s == q->k[1]) return 0;
    for (int j = 0; j < q->np[1 - c]; j++) if (q->p[1 - c][j] == s) return 0;
  }
  if (in_check(q, 1 - q->stm)) return 0;
  return 1;
}

/* ---- hash table of positions ---- */
static uint64_t *keys; static int32_t *tab; static size_t tabsz, nn, capn;
static uint64_t hsh(uint64_t x) { x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ULL; x ^= x >> 33; return x; }
static void tab_init(size_t sz) { tabsz = sz; tab = malloc(sizeof(int32_t) * sz); memset(tab, -1, sizeof(int32_t) * sz); }
static int32_t tab_find_or_add(uint64_t key, int *added) {
  size_t h = hsh(key) & (tabsz - 1);
  while (tab[h] >= 0) { if (keys[tab[h]] == key) { *added = 0; return tab[h]; } h = (h + 1) & (tabsz - 1); }
  if (nn == capn) { capn *= 2; keys = realloc(keys, capn * sizeof *keys); }
  keys[nn] = key; tab[h] = (int32_t)nn; *added = 1;
  return (int32_t)(nn++);
}
static void tab_grow(void) {
  free(tab); tab_init(tabsz * 2);
  for (size_t i = 0; i < nn; i++) {
    size_t h = hsh(keys[i]) & (tabsz - 1);
    while (tab[h] >= 0) h = (h + 1) & (tabsz - 1);
    tab[h] = (int32_t)i;
  }
}
static int32_t lookup(uint64_t key) {
  size_t h = hsh(key) & (tabsz - 1);
  while (tab[h] >= 0) { if (keys[tab[h]] == key) return tab[h]; h = (h + 1) & (tabsz - 1); }
  return -1;
}

int main(int argc, char **argv) {
  int wantmoves = 0;
  for (int i = 1; i < argc; i++) {
    if (!strcmp(argv[i], "--board") && i + 1 < argc) {
      char kind[8];
      if (sscanf(argv[++i], "%7[a-z]:%dx%d", kind, &W, &H) != 3) return 2;
      WRAP = !strcmp(kind, "cyl");
    } else if (!strcmp(argv[i], "--ep") && i + 1 < argc) EPON = !strcmp(argv[++i], "on");
    else if (!strcmp(argv[i], "--model") && i + 1 < argc) { i++; MODEL = !strcmp(argv[i], "p") ? 0 : !strcmp(argv[i], "bb") ? 1 : 2; }
    else if (!strcmp(argv[i], "--moves")) wantmoves = 1;
    else return 2;
  }
  NSQ = W * H;
  capn = 1 << 16; keys = malloc(capn * sizeof *keys); tab_init(1 << 18);
  /* read queries */
  char (*lines)[256] = malloc(256 * 4096); Pos *roots = malloc(sizeof(Pos) * 4096); int *okq = malloc(sizeof(int) * 4096);
  int nl = 0;
  while (nl < 4096 && fgets(lines[nl], 256, stdin)) {
    size_t L = strlen(lines[nl]); while (L && (lines[nl][L - 1] == '\n' || lines[nl][L - 1] == '\r')) lines[nl][--L] = 0;
    okq[nl] = (L > 0 && lines[nl][0] != '#') ? parse_pos(lines[nl], &roots[nl]) : -1;
    nl++;
  }
  /* explore */
  size_t ecap = 1 << 20, ne = 0; int32_t *succ = malloc(ecap * sizeof *succ);
  size_t ncap = 1 << 16; size_t *off = malloc(ncap * sizeof *off);
  int16_t *nwin = malloc(ncap * 2), *nbad = malloc(ncap * 2); uint8_t *chk = malloc(ncap), *nolegal = malloc(ncap);
  for (int i = 0; i < nl; i++) if (okq[i] > 0) { int ad; tab_find_or_add(pack(&roots[i]), &ad); if (nn * 2 > tabsz) tab_grow(); }
  Moves *mv = malloc(sizeof *mv);
  for (size_t i = 0; i < nn; i++) {
    Pos q; unpack(keys[i], &q);
    gen(&q, mv);
    if (i >= ncap) { ncap *= 2; off = realloc(off, ncap * sizeof *off); nwin = realloc(nwin, ncap * 2); nbad = realloc(nbad, ncap * 2); chk = realloc(chk, ncap); nolegal = realloc(nolegal, ncap); }
    off[i] = ne;
    nwin[i] = (int16_t)mv->nwin; nbad[i] = (int16_t)mv->nbad;
    chk[i] = (uint8_t)in_check(&q, q.stm);
    nolegal[i] = (mv->nsucc + mv->nwin + mv->nbad == 0);
    for (int j = 0; j < mv->nsucc; j++) {
      int ad; int32_t id = tab_find_or_add(pack(&mv->succ[j]), &ad);
      if (nn * 2 > tabsz) tab_grow();
      if (ne == ecap) { ecap *= 2; succ = realloc(succ, ecap * sizeof *succ); }
      succ[ne++] = id;
    }
  }
  off = realloc(off, (nn + 1) * sizeof *off); off[nn] = ne;
  /* reverse graph */
  int32_t *indeg = calloc(nn + 1, sizeof *indeg);
  for (size_t e = 0; e < ne; e++) indeg[succ[e]]++;
  size_t *roff = malloc((nn + 1) * sizeof *roff); roff[0] = 0;
  for (size_t i = 0; i < nn; i++) roff[i + 1] = roff[i] + (size_t)indeg[i];
  int32_t *pred = malloc((ne + 1) * sizeof *pred); int32_t *fillp = calloc(nn + 1, sizeof *fillp);
  for (size_t i = 0; i < nn; i++) for (size_t e = off[i]; e < off[i + 1]; e++) { int32_t j = succ[e]; pred[roff[j] + (size_t)fillp[j]++] = (int32_t)i; }
  /* retrograde: 0 unknown(draw), 1 win, 2 loss for the side to move */
  uint8_t *val = calloc(nn, 1); int32_t *cnt = malloc(nn * sizeof *cnt); int32_t *queue = malloc(nn * sizeof *queue); size_t qh = 0, qt = 0;
  for (size_t i = 0; i < nn; i++) {
    cnt[i] = (int32_t)(off[i + 1] - off[i]);
    if (nwin[i] > 0) { val[i] = 1; queue[qt++] = (int32_t)i; }
    else if (nolegal[i]) { if (chk[i]) { val[i] = 2; queue[qt++] = (int32_t)i; } else val[i] = 3; }
    else if (cnt[i] == 0) { /* only losing promotions */ val[i] = 2; queue[qt++] = (int32_t)i; }
  }
  while (qh < qt) {
    int32_t x = queue[qh++];
    for (size_t e = roff[x]; e < roff[x + 1]; e++) {
      int32_t p = pred[e];
      if (val[p]) continue;
      if (val[x] == 2) { val[p] = 1; queue[qt++] = p; }
      else if (val[x] == 1) { if (--cnt[p] == 0) { val[p] = 2; queue[qt++] = p; } }
    }
  }
  /* answer */
  for (int i = 0; i < nl; i++) {
    if (okq[i] < 0) { printf("%s\n", lines[i]); continue; }
    if (okq[i] == 0) { printf("%s | X\n", lines[i]); continue; }
    int32_t id = lookup(pack(&roots[i]));
    int v = val[id], stm = roots[i].stm;
    char r = v == 1 ? (stm == 0 ? 'W' : 'L') : v == 2 ? (stm == 0 ? 'L' : 'W') : 'D';
    printf("%s | %c", lines[i], r);
    if (wantmoves) {
      gen(&roots[i], mv);
      printf(" |");
      for (int j = 0; j < mv->nwin; j++) printf(" %s:%c", mv->wtxt[j], stm == 0 ? 'W' : 'L');
      for (int j = 0; j < mv->nbad; j++) printf(" %s:%c", mv->btxt[j], stm == 0 ? 'L' : 'W');
      for (int j = 0; j < mv->nsucc; j++) {
        int32_t sid = lookup(pack(&mv->succ[j]));
        int sv = val[sid]; /* from the new side to move */
        int ns = mv->succ[j].stm;
        char rr = sv == 1 ? (ns == 0 ? 'W' : 'L') : sv == 2 ? (ns == 0 ? 'L' : 'W') : 'D';
        printf(" %s:%c", mv->txt[j], rr);
      }
    }
    printf("\n");
  }
  fprintf(stderr, "[mine %s:%dx%d ep=%s model=%s: %zu positions, %zu moves]\n", WRAP ? "cyl" : "flat", W, H, EPON ? "on" : "off",
          MODEL == 0 ? "p" : MODEL == 1 ? "bb" : "bw", nn, ne);
  return 0;
}
