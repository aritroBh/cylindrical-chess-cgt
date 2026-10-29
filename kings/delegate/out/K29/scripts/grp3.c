/* grp.c -- K29 screening tool.  Exact P-model / frozen-model solver for K+pawns v K+pawns (flat or cylinder),
 * derived from the K23 agent's pk2.c (layers = pawn sets; inside a layer only kings move).  Changes against pk2.c:
 *   * one hash table per model (P, frozen, P-with-depth);
 *   * a depth mode: win/loss depth in plies (promotion = 1 ply), computed by synchronous rounds;
 *   * mode "enum": all bare groups (kings and Z-pawns on the files of F_Z) whose P value is (L,W), with sortie depths;
 *   * mode "test": groups x all contexts, Phi (P with the group) against Psi (frozen model, kings parked, no Z-pawns).
 * This is a COMPUTED-1 screening tool.  Every number that goes into FINDINGS.md is re-run with kp_p and ref3.
 *
 * usage:
 *   grp --board cyl:7x6 --mode enum --zs 0 --fz 3 --zw 2 --zb 2 [--rlo 2 --rhi 5]            > bare groups
 *   grp --board cyl:7x6 --mode test --zs 0 --fz 3 --cw 2 --cb 2 [--rlo 2 --rhi 5] [--first N] [--table] < groups
 *   grp --board B --mode pos [--frozen] [--depth] < positions      (like pk2; with --depth prints plies)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef uint64_t u64;
static int W, H, N, WRAP, FROZEN = 0, NOEP = 0, DEPTHM = 0;
enum { UNK = 0, WIN = 1, LOSS = 2, DRAW = 3, ILL = 4 };

static int sq(int f, int r) { return r * W + f; }
static int nb(int s, int df, int dr) {
  int f = s % W + df, r = s / W + dr;
  if (r < 0 || r >= H) return -1;
  if (WRAP) f = ((f % W) + W) % W; else if (f < 0 || f >= W) return -1;
  return sq(f, r);
}

typedef struct Layer {
  u64 wp, bp; int ep;
  unsigned char *v, *d;
  struct Layer *next;
} Layer;
#define HS (1 << 20)
static Layer *tab[3][HS];
static long nlayers[3];
static int tabsel(void) { return DEPTHM ? 2 : (FROZEN ? 1 : 0); }

static void free_table(int m) {
  for (int h = 0; h < HS; h++) {
    Layer *L = tab[m][h];
    while (L) { Layer *n = L->next; free(L->v); free(L->d); free(L); L = n; }
    tab[m][h] = 0;
  }
  nlayers[m] = 0;
}

static unsigned hsh(u64 wp, u64 bp, int ep) {
  u64 x = wp * 0x9E3779B97F4A7C15ULL ^ (bp + 0x1234567ULL) * 0xC2B2AE3D27D4EB4FULL ^ (u64)(ep + 2) * 0x165667B19E3779F9ULL;
  x ^= x >> 29; x *= 0xBF58476D1CE4E5B9ULL; x ^= x >> 32;
  return (unsigned)(x & (HS - 1));
}

static int pawn_attacks(u64 pc, int c, int t) {
  int dr = c == 0 ? -1 : 1;
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
typedef struct { Layer *L; int idx; int term; } Child;

static int legalpos(u64 wp, u64 bp, int wk, int bk, int stm, int ep) {
  if (wk < 0 || bk < 0) return 0;
  if (wk == bk || adjacent(wk, bk)) return 0;
  if ((wp >> wk & 1) || (bp >> wk & 1) || (wp >> bk & 1) || (bp >> bk & 1)) return 0;
  if (wp & bp) return 0;
  for (int s = 0; s < N; s++) {
    if ((wp >> s & 1) && (s / W == 0 || s / W == H - 1)) return 0;
    if ((bp >> s & 1) && (s / W == 0 || s / W == H - 1)) return 0;
  }
  if (stm == 0) { if (pawn_attacks(wp, 0, bk)) return 0; }
  else { if (pawn_attacks(bp, 1, wk)) return 0; }
  (void)ep;
  return 1;
}

static int gen(u64 wp, u64 bp, int wk, int bk, int stm, int ep, Child *out, int *ischeck) {
  int n = 0, us = stm;
  u64 mine = us == 0 ? wp : bp, theirs = us == 0 ? bp : wp;
  int ok = us == 0 ? wk : bk, ek = us == 0 ? bk : wk;
  *ischeck = pawn_attacks(theirs, !us, ok);
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
  int m = tabsel();
  unsigned h = hsh(wp, bp, ep);
  for (Layer *L = tab[m][h]; L; L = L->next) if (L->wp == wp && L->bp == bp && L->ep == ep) return L;
  Layer *L = calloc(1, sizeof *L);
  L->wp = wp; L->bp = bp; L->ep = ep;
  int NP = N * N * 2;
  L->v = calloc((size_t)NP, 1);
  if (DEPTHM) L->d = calloc((size_t)NP, 1);
  L->next = tab[m][h]; tab[m][h] = L; nlayers[m]++;
  Child (*ch)[48] = malloc(sizeof(Child[48]) * (size_t)NP);
  unsigned char *nc = calloc(NP, 1), *chk = calloc(NP, 1);
  int maxcd = 0;
  for (int wk = 0; wk < N; wk++) for (int bk = 0; bk < N; bk++) for (int stm = 0; stm < 2; stm++) {
    int i = (wk * N + bk) * 2 + stm;
    if (!legalpos(wp, bp, wk, bk, stm, ep)) { L->v[i] = ILL; continue; }
    int ic;
    Child tmp[64];
    int n = gen(wp, bp, wk, bk, stm, ep, tmp, &ic);
    if (FROZEN) for (int k = 0; k < n; k++) tmp[k].term = 2;
    n = genpawn(wp, bp, wk, bk, stm, ep, tmp, n);
    if (n > 48) { fprintf(stderr, "too many moves %d\n", n); exit(3); }
    memcpy(ch[i], tmp, sizeof(Child) * n);
    nc[i] = n; chk[i] = ic;
    if (DEPTHM) for (int k = 0; k < n; k++) if (tmp[k].term == 0 && tmp[k].L != L) {
      int cd = tmp[k].L->d[tmp[k].idx]; if (cd > maxcd) maxcd = cd;
    }
  }
  if (!DEPTHM) {
    int changed = 1;
    while (changed) {
      changed = 0;
      for (int i = 0; i < NP; i++) {
        if (L->v[i] == WIN || L->v[i] == LOSS || L->v[i] == ILL) continue;
        int n = nc[i];
        if (n == 0) { L->v[i] = chk[i] ? LOSS : DRAW; if (chk[i]) changed = 1; continue; }
        int allwin = 1, anyloss = 0;
        for (int k = 0; k < n; k++) {
          int cv; Child *c = &ch[i][k];
          if (c->term == 1) cv = LOSS;
          else if (c->term == 2) cv = WIN;
          else cv = c->L->v[c->idx];
          if (cv == LOSS) { anyloss = 1; break; }
          if (cv != WIN) allwin = 0;
        }
        if (anyloss) { L->v[i] = WIN; changed = 1; }
        else if (allwin) { L->v[i] = LOSS; changed = 1; }
        else L->v[i] = UNK;
      }
    }
    for (int i = 0; i < NP; i++) if (L->v[i] == UNK) L->v[i] = DRAW;
  } else {
    /* depth mode: synchronous rounds; a state decided at round r has depth r (plies; promotion = 1) */
    int *work = malloc(sizeof(int) * (size_t)NP), nw = 0;
    unsigned char *nv = calloc(NP, 1);
    for (int i = 0; i < NP; i++) {
      if (L->v[i] == ILL) continue;
      if (nc[i] == 0) { L->v[i] = chk[i] ? LOSS : DRAW; L->d[i] = 0; continue; }
      work[nw++] = i;
    }
    for (int r = 1; r < 250; r++) {
      int ndec = 0;
      for (int a = 0; a < nw; a++) {
        int i = work[a], n = nc[i]; nv[i] = 0;
        int anyloss = 0, allwin = 1;
        for (int k = 0; k < n; k++) {
          Child *c = &ch[i][k]; int cv, cd;
          if (c->term == 1) { cv = LOSS; cd = 0; }
          else { cv = c->L->v[c->idx]; cd = c->L->d[c->idx]; if (c->L == L && cv != WIN && cv != LOSS) cv = UNK; }
          if (cv == LOSS && cd <= r - 1) { anyloss = 1; break; }
          if (!(cv == WIN && cd <= r - 1)) allwin = 0;
        }
        if (anyloss) nv[i] = WIN; else if (allwin) nv[i] = LOSS;
        if (nv[i]) ndec++;
      }
      int w2 = 0;
      for (int a = 0; a < nw; a++) {
        int i = work[a];
        if (nv[i]) { L->v[i] = nv[i]; L->d[i] = r; } else work[w2++] = i;
      }
      nw = w2;
      if (!ndec && r > maxcd + 1) break;
    }
    for (int a = 0; a < nw; a++) L->v[work[a]] = DRAW;
    free(work); free(nv);
  }
  free(ch); free(nc); free(chk);
  return L;
}

static int parsesq(const char *s) { return sq(s[0] - 'a', s[1] - '1'); }
static void sqname(int s, char *o) { o[0] = 'a' + s % W; o[1] = '1' + s / W; o[2] = 0; }

static char letter(int v, int stm) { return v == DRAW ? 'D' : ((v == WIN) == (stm == 0) ? 'W' : 'L'); }

/* parse a group string "Ka4 Pb3 kc3 pb4" */
static int parse_group(const char *s, int *wk, int *bk, u64 *wp, u64 *bp) {
  char buf[256]; strncpy(buf, s, 255); buf[255] = 0;
  *wk = *bk = -1; *wp = *bp = 0;
  for (char *t = strtok(buf, " "); t; t = strtok(0, " ")) {
    if (t[0] == 'K') *wk = parsesq(t + 1);
    else if (t[0] == 'k') *bk = parsesq(t + 1);
    else if (t[0] == 'P') *wp |= 1ULL << parsesq(t + 1);
    else if (t[0] == 'p') *bp |= 1ULL << parsesq(t + 1);
  }
  return *wk >= 0 && *bk >= 0;
}

/* ---------- F_Z geometry ---------- */
static int zs = 0, fz = 3;
static int in_fz(int f) { /* file f in the arc zs .. zs+fz-1 */
  if (WRAP) { int d = ((f - zs) % W + W) % W; return d < fz; }
  return f >= zs && f < zs + fz;
}
static int fdist(int f) { /* distance of file f from F_Z (0 inside) */
  int best = 99;
  for (int g = 0; g < W; g++) if (in_fz(g)) {
    int d = abs(f - g); if (WRAP && W - d < d) d = W - d;
    if (d < best) best = d;
  }
  return best;
}

typedef struct { char z[96]; int wk, bk; u64 wp, bp; int dw, db; } Grp;

static int cmp_pawns(const void *a, const void *b) {
  const Grp *x = a, *y = b;
  if (x->wp != y->wp) return x->wp < y->wp ? -1 : 1;
  if (x->bp != y->bp) return x->bp < y->bp ? -1 : 1;
  return 0;
}

static void zstring(const Grp *g, char *o) {
  char t[4]; o[0] = 0;
  sqname(g->wk, t); strcat(o, "K"); strcat(o, t);
  for (int s = 0; s < N; s++) if (g->wp >> s & 1) { sqname(s, t); strcat(o, " P"); strcat(o, t); }
  sqname(g->bk, t); strcat(o, " k"); strcat(o, t);
  for (int s = 0; s < N; s++) if (g->bp >> s & 1) { sqname(s, t); strcat(o, " p"); strcat(o, t); }
}

static int rlo = 2, rhi = 5, dmin = 2;
static long maxlayers = 200000;  /* free a table when it holds more layers than this (memory guard) */

static void run_enum(int zw, int zb) {
  /* squares for Z-pawns */
  int sqs[64], ns = 0;
  for (int f = 0; f < W; f++) if (in_fz(f)) for (int r = rlo - 1; r <= rhi - 1; r++) sqs[ns++] = sq(f, r);
  /* all pawn subsets up to zw (white) and zb (black) */
  static u64 wsets[100000]; int nws = 0;
  for (u64 m = 0; m < (1ULL << ns); m++) { int pc = __builtin_popcountll(m); if (pc > zw && pc > zb) continue; (void)0; }
  /* generate subsets of size<=max(zw,zb) as masks over sqs */
  int mx = zw > zb ? zw : zb;
  static u64 subs[200000]; int nsub = 0;
  for (u64 m = 0; m < (1ULL << ns); m++) if (__builtin_popcountll(m) <= mx) subs[nsub++] = m;
  (void)wsets; (void)nws;
  Grp *cands = malloc(sizeof(Grp) * 400000); long nc = 0;
  for (int a = 0; a < nsub; a++) for (int b = 0; b < nsub; b++) {
    int pa = __builtin_popcountll(subs[a]), pb = __builtin_popcountll(subs[b]);
    if (pa > zw || pb > zb || pa + pb == 0) continue;
    if (subs[a] & subs[b]) continue;
    u64 wp = 0, bp = 0;
    for (int i = 0; i < ns; i++) { if (subs[a] >> i & 1) wp |= 1ULL << sqs[i]; if (subs[b] >> i & 1) bp |= 1ULL << sqs[i]; }
    if (wp & bp) continue;
    Layer *L = solve_layer(wp, bp, -1);
    for (int wk = 0; wk < N; wk++) { if (!in_fz(wk % W)) continue;
      for (int bk = 0; bk < N; bk++) { if (!in_fz(bk % W)) continue;
        int i0 = (wk * N + bk) * 2;
        if (L->v[i0] != LOSS || L->v[i0 + 1] != LOSS) continue;
        if (nc >= 400000) { fprintf(stderr, "too many\n"); exit(4); }
        Grp *g = &cands[nc++]; g->wk = wk; g->bk = bk; g->wp = wp; g->bp = bp; g->dw = g->db = -1;
      } }
  }
  fprintf(stderr, "layers(P)=%ld candidates (bare P = (L,W)) = %ld\n", nlayers[0], nc);
  free_table(0);
  /* depth pass, grouped by pawn config */
  qsort(cands, nc, sizeof(Grp), cmp_pawns);
  DEPTHM = 1;
  for (long i = 0; i < nc; ) {
    long j = i; while (j < nc && cands[j].wp == cands[i].wp && cands[j].bp == cands[i].bp) j++;
    Layer *L = solve_layer(cands[i].wp, cands[i].bp, -1);
    for (long k = i; k < j; k++) {
      int i0 = (cands[k].wk * N + cands[k].bk) * 2;
      cands[k].dw = L->d[i0]; cands[k].db = L->d[i0 + 1];
      if (L->v[i0] != LOSS || L->v[i0 + 1] != LOSS) { fprintf(stderr, "depth pass disagrees with P pass\n"); exit(5); }
    }
    i = j;
    if (nlayers[2] > 400000) free_table(2);
  }
  for (long k = 0; k < nc; k++) {
    char z[96]; zstring(&cands[k], z);
    printf("%s | %d %d\n", z, cands[k].dw, cands[k].db);
  }
}

/* ---------- test mode ---------- */
static int cmp_u64pair_n(const void *a, const void *b) {
  const u64 *x = a, *y = b;
  int px = __builtin_popcountll(x[0]) + __builtin_popcountll(x[1]), py = __builtin_popcountll(y[0]) + __builtin_popcountll(y[1]);
  if (px != py) return px - py;
  if (x[0] != y[0]) return x[0] < y[0] ? -1 : 1;
  if (x[1] != y[1]) return x[1] < y[1] ? -1 : 1;
  return 0;
}

static long CTXLO = 0, CTXHI = -1; static const char *CFILES = ""; /* grp3: only context files named in CFILES (e.g. "ef") */  /* grp2: only contexts with sorted index in [CTXLO, CTXHI) (CTXHI<0: all) */
static void run_test(int cw, int cb, int first, int table, int parkalt) {
  int sqs[64], ns = 0;
  for (int f = 0; f < W; f++) if (fdist(f) >= dmin && (!CFILES[0] || strchr(CFILES, 'a' + f))) for (int r = rlo - 1; r <= rhi - 1; r++) sqs[ns++] = sq(f, r);
  /* contexts */
  int mx = cw > cb ? cw : cb;
  static u64 subs[2000000]; long nsub = 0;
  if (ns > 24) { fprintf(stderr, "too many context squares\n"); exit(6); }
  for (u64 m = 0; m < (1ULL << ns); m++) if (__builtin_popcountll(m) <= mx) subs[nsub++] = m;
  u64 (*ctx)[2] = malloc(sizeof(u64[2]) * 1000000); long nctx = 0;
  for (long a = 0; a < nsub; a++) for (long b = 0; b < nsub; b++) {
    if (__builtin_popcountll(subs[a]) > cw || __builtin_popcountll(subs[b]) > cb) continue;
    if (subs[a] & subs[b]) continue;
    u64 wp = 0, bp = 0;
    for (int i = 0; i < ns; i++) { if (subs[a] >> i & 1) wp |= 1ULL << sqs[i]; if (subs[b] >> i & 1) bp |= 1ULL << sqs[i]; }
    if (nctx >= 1000000) { fprintf(stderr, "too many contexts\n"); exit(7); }
    ctx[nctx][0] = wp; ctx[nctx][1] = bp; nctx++;
  }
  qsort(ctx, nctx, sizeof(u64[2]), cmp_u64pair_n);
  fprintf(stderr, "context squares %d, contexts %ld\n", ns, nctx);
  long clo = CTXLO, chi = CTXHI < 0 || CTXHI > nctx ? nctx : CTXHI;
  /* parked kings: two parkings */
  int pw0 = sq(zs % W, 0), pb0 = sq(zs % W, H - 1);
  int pw1 = sq((zs + 1) % W, 0), pb1 = sq((zs + fz - 1) % W, H - 1);
  /* read groups */
  Grp *gs = malloc(sizeof(Grp) * 200000); long ng = 0;
  char line[512];
  while (fgets(line, sizeof line, stdin)) {
    line[strcspn(line, "\n")] = 0;
    if (!line[0] || line[0] == '#') continue;
    char *bar = strstr(line, " | "); if (bar) *bar = 0;
    Grp *g = &gs[ng];
    if (!parse_group(line, &g->wk, &g->bk, &g->wp, &g->bp)) continue;
    strncpy(g->z, line, 95); g->z[95] = 0; ng++;
  }
  qsort(gs, ng, sizeof(Grp), cmp_pawns);
  long *ndiff = calloc(ng, sizeof(long)), *ndiffpair = calloc(ng, sizeof(long)), *npark = calloc(ng, sizeof(long));
  long *nfail_ctx_printed = calloc(ng, sizeof(long));
  long *ncheck = calloc(ng, sizeof(long));
  int *done = calloc(ng, sizeof(int));
  char (*firstfail)[160] = calloc(ng, 160);
  for (long i = 0; i < ng; ) {
    long j = i; while (j < ng && gs[j].wp == gs[i].wp && gs[j].bp == gs[i].bp) j++;
    long active = j - i;
    for (long c = clo; c < chi && active > 0; c++) {
      if (nlayers[0] > maxlayers) free_table(0);
      if (nlayers[1] > maxlayers) free_table(1);
      u64 cwp = ctx[c][0], cbp = ctx[c][1];
      char cs[200]; cs[0] = 0; char t[4];
      for (int s = 0; s < N; s++) if (cwp >> s & 1) { sqname(s, t); strcat(cs, " P"); strcat(cs, t); }
      for (int s = 0; s < N; s++) if (cbp >> s & 1) { sqname(s, t); strcat(cs, " p"); strcat(cs, t); }
      /* Psi: frozen model, parked kings, context pawns only */
      FROZEN = 1; DEPTHM = 0;
      Layer *LF = solve_layer(cwp, cbp, -1);
      int psi[2], psiA[2];
      for (int stm = 0; stm < 2; stm++) {
        psi[stm] = letter(LF->v[(pw0 * N + pb0) * 2 + stm], stm);
        psiA[stm] = letter(LF->v[(pw1 * N + pb1) * 2 + stm], stm);
      }
      FROZEN = 0;
      Layer *LP = solve_layer(gs[i].wp | cwp, gs[i].bp | cbp, -1);
      for (long k = i; k < j; k++) {
        if (done[k]) continue;
        ncheck[k]++;
        int ph[2]; int bad = 0;
        for (int stm = 0; stm < 2; stm++) {
          int v = LP->v[(gs[k].wk * N + gs[k].bk) * 2 + stm];
          ph[stm] = v == ILL ? 'X' : letter(v, stm);
          if (ph[stm] != psi[stm]) bad = 1;
          if (psi[stm] != psiA[stm]) npark[k]++;
        }
        if (table) printf("T %s |%s | P=%c%c F=%c%c %s\n", gs[k].z, cs, ph[0], ph[1], psi[0], psi[1], bad ? "DIFF" : "same");
        if (bad) {
          ndiff[k]++;
          if (!firstfail[k][0]) snprintf(firstfail[k], 160, "%s | P=%c%c F=%c%c", cs, ph[0], ph[1], psi[0], psi[1]);
          if (first > 0 && ndiff[k] >= first) { done[k] = 1; active--; }
        }
      }
    }
    free_table(0);
    if (nlayers[1] > maxlayers) free_table(1);
    i = j;
  }
  for (long k = 0; k < ng; k++)
    printf("R %s | contexts_checked %ld differ %ld parking_mismatch %ld | first fail:%s\n", gs[k].z, ncheck[k], ndiff[k], npark[k], firstfail[k][0] ? firstfail[k] : " none");
  (void)ndiffpair; (void)nfail_ctx_printed; (void)parkalt;
}

int main(int argc, char **argv) {
  const char *bd = 0, *mode = "pos";
  int zw = 2, zb = 2, cw = 2, cb = 2, first = 0, table = 0;
  for (int i = 1; i < argc; i++) {
    if (!strcmp(argv[i], "--board") && i + 1 < argc) bd = argv[++i];
    else if (!strcmp(argv[i], "--mode") && i + 1 < argc) mode = argv[++i];
    else if (!strcmp(argv[i], "--frozen")) FROZEN = 1;
    else if (!strcmp(argv[i], "--depth")) DEPTHM = 1;
    else if (!strcmp(argv[i], "--noep")) NOEP = 1;
    else if (!strcmp(argv[i], "--zs")) zs = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--fz")) fz = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--zw")) zw = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--zb")) zb = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--cw")) cw = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--cb")) cb = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--rlo")) rlo = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--rhi")) rhi = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--first")) first = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--dmin")) dmin = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--maxlayers")) maxlayers = atol(argv[++i]);
    else if (!strcmp(argv[i], "--table")) table = 1;
    else if (!strcmp(argv[i], "--cfiles")) CFILES = argv[++i];
    else if (!strcmp(argv[i], "--ctxlo")) CTXLO = atol(argv[++i]);
    else if (!strcmp(argv[i], "--ctxhi")) CTXHI = atol(argv[++i]);
    else { fprintf(stderr, "bad arg %s\n", argv[i]); return 2; }
  }
  if (!bd) return 2;
  char kind[8]; if (sscanf(bd, "%7[a-z]:%dx%d", kind, &W, &H) != 3) return 2;
  WRAP = !strcmp(kind, "cyl"); N = W * H;
  if (!strcmp(mode, "enum")) { run_enum(zw, zb); return 0; }
  if (!strcmp(mode, "test")) { run_test(cw, cb, first, table, 0); return 0; }
  char line[512];
  while (fgets(line, sizeof line, stdin)) {
    line[strcspn(line, "\n")] = 0;
    if (line[0] == '#' || !line[0]) { puts(line); continue; }
    char buf[512]; strcpy(buf, line);
    u64 wp = 0, bp = 0; int wk = -1, bk = -1, stm = 0, ep = -1;
    for (char *tok = strtok(buf, " "); tok; tok = strtok(0, " ")) {
      if (!strcmp(tok, "w")) stm = 0;
      else if (!strcmp(tok, "b")) stm = 1;
      else if (!strcmp(tok, "-")) ep = -1;
      else if (tok[0] == 'K') wk = parsesq(tok + 1);
      else if (tok[0] == 'k') bk = parsesq(tok + 1);
      else if (tok[0] == 'P') wp |= 1ULL << parsesq(tok + 1);
      else if (tok[0] == 'p') bp |= 1ULL << parsesq(tok + 1);
      else if (tok[0] >= 'a' && tok[0] <= 'h' && tok[1] >= '1' && tok[1] <= '8') ep = parsesq(tok);
    }
    if (!legalpos(wp, bp, wk, bk, stm, ep)) { printf("%s | X X\n", line); continue; }
    Layer *L = solve_layer(wp, bp, ep);
    int i = (wk * N + bk) * 2 + stm;
    int v = L->v[i];
    if (DEPTHM) printf("%s | %c %c depth %d\n", line, letter(v, stm), letter(v, stm), L->d[i]);
    else printf("%s | %c %c\n", line, letter(v, stm), letter(v, stm));
  }
  return 0;
}
