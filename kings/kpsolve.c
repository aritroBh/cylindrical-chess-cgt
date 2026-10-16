/* kpsolve.c -- exact solver for chess positions with kings, pawns and promoted
 * officers (Q, R, B, N) on a small flat or cylindrical board.
 * Rules and file formats: SPEC.md. Written independently of kings/ref/.
 *
 * Method. Positions are grouped into layers by (white pawns, black pawns,
 * officer types). Pawn moves, captures and promotions leave the layer and never
 * come back, so a layer is solved after every layer it can reach (on demand,
 * recursively). Inside a layer only kings and officers move, reversibly, so
 * every placement of them is solved together: counting retrograde analysis on
 * the explicit in-layer move graph, or repeated passes for very large layers.
 * Values are win / loss / draw for the side to move; whatever is never resolved
 * is a draw (the least fixed point, i.e. infinite play is a draw).
 *
 * Extra options beyond SPEC.md, for experiments:
 *   --frozen   kings may not move: a king move loses at once for the mover, and
 *              a promotion wins at once for the promoter (the pawn-only
 *              convention with real races instead of "passed pawn = win")
 *   --moves    after the result, list every legal move with the value it leads to
 *   --threads  worker threads for large layers (default 1)
 */
#include <ctype.h>
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXOFF 3
#define MAXMOVES 320
#define BIT(s) (1ULL << (s))
#define PASS_THRESHOLD 6000000u /* layers with more states use repeated passes */

enum { VUNK = 0, VWIN, VLOSS, VDRAW, VILL };
enum { WHITE = 0, BLACK = 1 };
enum { TQ = 1, TR, TB, TN }; /* officer code = type + 8 * colour */
static const char TYPECH[] = "?QRBN";

static int W, H, N, WRAP, EPON = 1, CAP = 1, FROZEN = 0, BOUND = 0, cappedSeen = 0, WANTMOVES = 0;
static int promoType[4], nPromo;

/* ---------- geometry ---------- */

static int kingN[64], kingL[64][8], knightN[64], knightL[64][8];
static uint64_t kingBB[64], knightBB[64];
static uint64_t pawnAtt[2][64]; /* squares from which a pawn of colour c attacks s */
static int capN[2][64], capL[2][64][2];
static const int DF[8] = {0, 0, 1, -1, 1, 1, -1, -1};
static const int DR[8] = {1, -1, 0, 0, 1, -1, 1, -1};
static int rayN[64][8], rayL[64][8][8];
static int8_t rayIdx[64][8][64];
static uint64_t rayBefore[64][8][8];

static int step(int s, int df, int dr) {
  int f = s % W + df, r = s / W + dr;
  if (r < 0 || r >= H) return -1;
  if (WRAP) f = ((f % W) + W) % W;
  else if (f < 0 || f >= W) return -1;
  return r * W + f;
}

static void add_unique(int *n, int *l, int s) {
  for (int i = 0; i < *n; i++)
    if (l[i] == s) return;
  l[(*n)++] = s;
}

static void init_geometry(void) {
  static const int NF[8] = {1, 2, -1, -2, 1, 2, -1, -2};
  static const int NR[8] = {2, 1, 2, 1, -2, -1, -2, -1};
  memset(rayIdx, -1, sizeof rayIdx);
  memset(pawnAtt, 0, sizeof pawnAtt);
  for (int s = 0; s < N; s++) {
    kingN[s] = knightN[s] = 0;
    kingBB[s] = knightBB[s] = 0;
    for (int d = 0; d < 8; d++) {
      int t = step(s, DF[d], DR[d]);
      if (t >= 0 && t != s) add_unique(&kingN[s], kingL[s], t);
      t = step(s, NF[d], NR[d]);
      if (t >= 0 && t != s) add_unique(&knightN[s], knightL[s], t);
    }
    for (int i = 0; i < kingN[s]; i++) kingBB[s] |= BIT(kingL[s][i]);
    for (int i = 0; i < knightN[s]; i++) knightBB[s] |= BIT(knightL[s][i]);
    for (int d = 0; d < 8; d++) {
      int cur = s;
      uint64_t before = 0;
      rayN[s][d] = 0;
      for (;;) {
        cur = step(cur, DF[d], DR[d]);
        if (cur < 0 || cur == s) break; /* edge, or back home: no null move */
        int k = rayN[s][d]++;
        rayL[s][d][k] = cur;
        rayIdx[s][d][cur] = (int8_t)k;
        rayBefore[s][d][k] = before;
        before |= BIT(cur);
      }
    }
    for (int c = 0; c < 2; c++) {
      capN[c][s] = 0;
      for (int df = -1; df <= 1; df += 2) {
        int t = step(s, df, c == WHITE ? 1 : -1);
        if (t >= 0 && t != s) add_unique(&capN[c][s], capL[c][s], t);
      }
    }
  }
  for (int c = 0; c < 2; c++)
    for (int s = 0; s < N; s++)
      for (int i = 0; i < capN[c][s]; i++) pawnAtt[c][capL[c][s][i]] |= BIT(s);
}

/* ---------- positions ---------- */

typedef struct {
  uint64_t wp, bp;
  int wk, bk, no, stm, ep;
  int osq[MAXOFF], ot[MAXOFF];
} Pos;

typedef struct {
  uint64_t wp, bp;
  int no;
  int ot[MAXOFF];
} Key;

static int colour_of(int code) { return code >> 3; }
static int type_of(int code) { return code & 7; }

static uint64_t occupancy(const Pos *p) {
  uint64_t o = p->wp | p->bp | BIT(p->wk) | BIT(p->bk);
  for (int j = 0; j < p->no; j++) o |= BIT(p->osq[j]);
  return o;
}

static int man_attacks(int type, int from, int target, uint64_t occ) {
  if (type == TN) return (int)((knightBB[from] >> target) & 1);
  int lo = type == TB ? 4 : 0, hi = type == TR ? 4 : 8;
  for (int d = lo; d < hi; d++) {
    int k = rayIdx[from][d][target];
    if (k >= 0 && !(rayBefore[from][d][k] & occ)) return 1;
  }
  return 0;
}

/* is square s attacked by colour `by`? */
static int attacked(const Pos *p, int s, int by) {
  int k = by == BLACK ? p->bk : p->wk;
  if ((kingBB[k] >> s) & 1) return 1;
  if ((by == BLACK ? p->bp : p->wp) & pawnAtt[by][s]) return 1;
  uint64_t occ = occupancy(p);
  for (int j = 0; j < p->no; j++)
    if (colour_of(p->ot[j]) == by && p->osq[j] != s && man_attacks(type_of(p->ot[j]), p->osq[j], s, occ))
      return 1;
  return 0;
}

static int in_check(const Pos *p, int side) {
  return attacked(p, side == BLACK ? p->bk : p->wk, !side);
}

static void canonicalize(Pos *p) {
  for (int i = 1; i < p->no; i++)
    for (int j = i; j > 0; j--) {
      int a = p->ot[j - 1] * 64 + p->osq[j - 1], b = p->ot[j] * 64 + p->osq[j];
      if (a <= b) break;
      int t = p->ot[j]; p->ot[j] = p->ot[j - 1]; p->ot[j - 1] = t;
      t = p->osq[j]; p->osq[j] = p->osq[j - 1]; p->osq[j - 1] = t;
    }
}

static void key_of(const Pos *p, Key *k) {
  memset(k, 0, sizeof *k);
  k->wp = p->wp;
  k->bp = p->bp;
  k->no = p->no;
  for (int j = 0; j < p->no; j++) k->ot[j] = p->ot[j];
}

static int key_eq(const Key *a, const Key *b) {
  if (a->wp != b->wp || a->bp != b->bp || a->no != b->no) return 0;
  for (int j = 0; j < a->no; j++)
    if (a->ot[j] != b->ot[j]) return 0;
  return 1;
}

static int pos_in_key(const Pos *p, const Key *k) {
  if (p->wp != k->wp || p->bp != k->bp || p->no != k->no) return 0;
  for (int j = 0; j < p->no; j++)
    if (p->ot[j] != k->ot[j]) return 0;
  return 1;
}

static size_t layer_size(int no) {
  size_t n = 2;
  for (int i = 0; i < 2 + no; i++) n *= (size_t)N;
  return n;
}

static size_t pos_index(const Pos *p) {
  size_t i = (size_t)p->stm;
  i = i * N + p->wk;
  i = i * N + p->bk;
  for (int j = 0; j < p->no; j++) i = i * N + p->osq[j];
  return i;
}

static void pos_decode(const Key *k, size_t idx, Pos *p) {
  p->wp = k->wp;
  p->bp = k->bp;
  p->no = k->no;
  p->ep = -1;
  for (int j = k->no - 1; j >= 0; j--) {
    p->osq[j] = (int)(idx % N);
    idx /= N;
    p->ot[j] = k->ot[j];
  }
  p->bk = (int)(idx % N);
  idx /= N;
  p->wk = (int)(idx % N);
  idx /= N;
  p->stm = (int)idx;
}

/* legal as a stored state: no overlaps, kings apart, canonical officer order,
 * side not to move not in check (pawn ranks are guaranteed by the key) */
static int legal_state(const Pos *p) {
  if (p->wp & p->bp) return 0;
  uint64_t seen = p->wp | p->bp;
  if (((seen >> p->wk) & 1) || ((seen >> p->bk) & 1) || p->wk == p->bk) return 0;
  seen |= BIT(p->wk) | BIT(p->bk);
  for (int j = 0; j < p->no; j++) {
    if ((seen >> p->osq[j]) & 1) return 0;
    seen |= BIT(p->osq[j]);
    if (j > 0 && p->ot[j] == p->ot[j - 1] && p->osq[j] < p->osq[j - 1]) return 0;
  }
  if ((kingBB[p->wk] >> p->bk) & 1) return 0;
  if (in_check(p, !p->stm)) return 0;
  return 1;
}

/* ---------- move generation ---------- */

typedef struct {
  int kind;   /* 0 position, 1 fixed result, 2 transient (e.p. right pending) */
  int winner; /* kind 1 */
  Pos pos;    /* the position after the move; pos.stm is the side to move there */
  int piece, from, to, promo;
} Child;

static void remove_officer(Pos *q, int j) {
  for (int i = j; i + 1 < q->no; i++) {
    q->osq[i] = q->osq[i + 1];
    q->ot[i] = q->ot[i + 1];
  }
  q->no--;
}

/* remove a piece of colour `victim` standing on s (pawn or officer), if any */
static void capture_at(Pos *q, int s, int victim) {
  uint64_t *pp = victim == BLACK ? &q->bp : &q->wp;
  if ((*pp >> s) & 1) {
    *pp &= ~BIT(s);
    return;
  }
  for (int j = 0; j < q->no; j++)
    if (q->osq[j] == s && colour_of(q->ot[j]) == victim) {
      remove_officer(q, j);
      return;
    }
}

static void emit(Child *out, int *m, Pos *q, int kind, int winner, int piece, int from, int to,
                 int promo) {
  Child *c = &out[(*m)++];
  canonicalize(q);
  c->kind = kind;
  c->winner = winner;
  c->pos = *q;
  c->piece = piece;
  c->from = from;
  c->to = to;
  c->promo = promo;
}

static void pawn_move(const Pos *p, int from, int to, int capsq, Child *out, int *m) {
  int us = p->stm, them = !us, last = us == WHITE ? H - 1 : 0;
  Pos q = *p;
  q.ep = -1;
  if (us == WHITE) q.wp &= ~BIT(from);
  else q.bp &= ~BIT(from);
  if (capsq >= 0) capture_at(&q, capsq, them);
  if (to / W == last) {
    Pos r = q;
    r.osq[r.no] = to;
    r.ot[r.no] = TQ + 8 * us; /* the promoted piece's type does not affect king safety */
    r.no++;
    if (in_check(&r, us)) return;
    for (int i = 0; i < nPromo; i++) {
      Pos s = q;
      s.osq[s.no] = to;
      s.ot[s.no] = promoType[i] + 8 * us;
      s.no++;
      s.stm = them;
      if (FROZEN) emit(out, m, &s, 1, us, 'P', from, to, promoType[i]);
      else if (s.no > CAP) {
        __atomic_store_n(&cappedSeen, 1, __ATOMIC_RELAXED);
        emit(out, m, &s, 1, BOUND == 0 ? WHITE : BLACK, 'P', from, to, promoType[i]);
      } else emit(out, m, &s, 0, 0, 'P', from, to, promoType[i]);
    }
    return;
  }
  if (us == WHITE) q.wp |= BIT(to);
  else q.bp |= BIT(to);
  if (in_check(&q, us)) return;
  q.stm = them;
  emit(out, m, &q, 0, 0, 'P', from, to, 0);
}

static int gen_moves(const Pos *p, Child *out) {
  int m = 0, us = p->stm, them = !us;
  uint64_t ownP = us == BLACK ? p->bp : p->wp, oppP = us == BLACK ? p->wp : p->bp;
  uint64_t ownO = 0, oppO = 0;
  for (int j = 0; j < p->no; j++) {
    if (colour_of(p->ot[j]) == us) ownO |= BIT(p->osq[j]);
    else oppO |= BIT(p->osq[j]);
  }
  int ok = us == BLACK ? p->bk : p->wk, ek = us == BLACK ? p->wk : p->bk;
  uint64_t occ = p->wp | p->bp | ownO | oppO | BIT(ok) | BIT(ek);
  uint64_t ownAll = ownP | ownO | BIT(ok);

  /* king */
  for (int i = 0; i < kingN[ok]; i++) {
    int n = kingL[ok][i];
    if (((ownAll >> n) & 1) || n == ek || ((kingBB[ek] >> n) & 1)) continue;
    Pos q = *p;
    q.ep = -1;
    if (us == BLACK) q.bk = n;
    else q.wk = n;
    capture_at(&q, n, them);
    if (in_check(&q, us)) continue;
    q.stm = them;
    if (FROZEN) emit(out, &m, &q, 1, them, 'K', ok, n, 0);
    else emit(out, &m, &q, 0, 0, 'K', ok, n, 0);
  }

  /* officers */
  for (int j = 0; j < p->no; j++) {
    if (colour_of(p->ot[j]) != us) continue;
    int t = type_of(p->ot[j]), from = p->osq[j];
    uint64_t dest = 0;
    if (t == TN) dest = knightBB[from];
    else {
      int lo = t == TB ? 4 : 0, hi = t == TR ? 4 : 8;
      for (int d = lo; d < hi; d++)
        for (int k = 0; k < rayN[from][d]; k++) {
          int s = rayL[from][d][k];
          dest |= BIT(s);
          if ((occ >> s) & 1) break;
        }
    }
    dest &= ~(ownAll | BIT(ek));
    for (int s = 0; s < N; s++) {
      if (!((dest >> s) & 1)) continue;
      Pos q = *p;
      q.ep = -1;
      q.osq[j] = s;
      capture_at(&q, s, them);
      if (in_check(&q, us)) continue;
      q.stm = them;
      emit(out, &m, &q, 0, 0, TYPECH[t], from, s, 0);
    }
  }

  /* pawns */
  int dir = us == WHITE ? W : -W, start = us == WHITE ? 1 : H - 2;
  for (int s = 0; s < N; s++) {
    if (!((ownP >> s) & 1)) continue;
    int t = s + dir;
    if (!((occ >> t) & 1)) {
      pawn_move(p, s, t, -1, out, &m);
      int t2 = t + dir;
      if (s / W == start && !((occ >> t2) & 1)) {
        Pos q = *p;
        q.ep = -1;
        if (us == WHITE) q.wp = (q.wp & ~BIT(s)) | BIT(t2);
        else q.bp = (q.bp & ~BIT(s)) | BIT(t2);
        if (!in_check(&q, us)) {
          q.stm = them;
          if (EPON && (oppP & pawnAtt[them][t])) {
            q.ep = t;
            emit(out, &m, &q, 2, 0, 'P', s, t2, 0);
          } else emit(out, &m, &q, 0, 0, 'P', s, t2, 0);
        }
      }
    }
    for (int i = 0; i < capN[us][s]; i++) {
      int c = capL[us][s][i];
      if (((oppP | oppO) >> c) & 1) pawn_move(p, s, c, c, out, &m);
      else if (c == p->ep) pawn_move(p, s, c, c - dir, out, &m);
    }
  }
  return m;
}

/* ---------- layers ---------- */

typedef struct Layer {
  Key key;
  size_t n;
  int8_t *val;
  struct Layer *next;
} Layer;

#define HBITS 22
static Layer **htab;
static size_t nlayers, nstatesTotal;
static int depthNow, depthMax;

static size_t key_hash(const Key *k) {
  uint64_t h = k->wp * 0x9E3779B97F4A7C15ULL ^ (k->bp + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL;
  for (int j = 0; j < k->no; j++) h = (h ^ (uint64_t)(k->ot[j] + 16 * j + 1)) * 0x100000001B3ULL;
  h ^= (uint64_t)k->no * 0x165667B19E3779F9ULL;
  h ^= h >> 29;
  return (size_t)(h & ((1u << HBITS) - 1));
}

static Layer *find_layer(const Key *k) {
  for (Layer *L = htab[key_hash(k)]; L; L = L->next)
    if (key_eq(&L->key, k)) return L;
  return NULL;
}

static void reset_tables(void) {
  if (htab)
    for (size_t i = 0; i < (1u << HBITS); i++)
      for (Layer *L = htab[i], *nx; L; L = nx) {
        nx = L->next;
        free(L->val);
        free(L);
      }
  free(htab);
  htab = calloc((size_t)1 << HBITS, sizeof *htab);
  nlayers = nstatesTotal = 0;
}

static Layer *get_layer(const Key *k);
static int transient_value(const Pos *p);
static int NT = 1;          /* worker threads */
static int inParallel = 0;  /* while workers run, every layer they look up must already exist */

static int pos_value(const Pos *p) {
  Key k;
  key_of(p, &k);
  Layer *L = find_layer(&k);
  if (!L) {
    if (inParallel) {
      fprintf(stderr, "kpsolve: internal error: a child layer was not solved before the parallel phase\n");
      exit(3);
    }
    L = get_layer(&k);
  }
  return L->val[pos_index(p)];
}

/* value of a child for the side to move in it */
static int child_value(const Child *c) {
  if (c->kind == 1) return c->winner == c->pos.stm ? VWIN : VLOSS;
  if (c->kind == 2) return transient_value(&c->pos);
  return pos_value(&c->pos);
}

static int transient_value(const Pos *p) {
  Child *ch = malloc(sizeof(Child) * MAXMOVES);
  int m = gen_moves(p, ch), v = VLOSS, draw = 0;
  if (m == 0) v = in_check(p, p->stm) ? VLOSS : VDRAW;
  for (int i = 0; i < m; i++) {
    int cv = child_value(&ch[i]);
    if (cv == VLOSS) { v = VWIN; break; }
    if (cv != VWIN) draw = 1;
  }
  if (m && v != VWIN) v = draw ? VDRAW : VLOSS;
  free(ch);
  return v;
}

typedef struct { uint32_t *a; size_t n, cap; } Vec;
static void vpush(Vec *v, uint32_t x) {
  if (v->n == v->cap) {
    v->cap = v->cap ? 2 * v->cap : 1 << 12;
    v->a = realloc(v->a, v->cap * sizeof *v->a);
  }
  v->a[v->n++] = x;
}

/* a set of layer keys (open addressing) */
typedef struct { Key *a; uint8_t *used; size_t cap, n; } KeySet;

static uint64_t key_hash64(const Key *k) {
  uint64_t h = k->wp * 0x9E3779B97F4A7C15ULL ^ (k->bp + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL;
  for (int j = 0; j < k->no; j++) h = (h ^ (uint64_t)(k->ot[j] + 16 * j + 1)) * 0x100000001B3ULL;
  h ^= (uint64_t)k->no * 0x165667B19E3779F9ULL;
  return h ^ (h >> 31);
}

static void ks_add(KeySet *s, const Key *k) {
  if (2 * (s->n + 1) > s->cap) {
    KeySet t = {0};
    t.cap = s->cap ? 2 * s->cap : 256;
    t.a = malloc(t.cap * sizeof *t.a);
    t.used = calloc(t.cap, 1);
    for (size_t i = 0; i < s->cap; i++)
      if (s->used[i]) ks_add(&t, &s->a[i]);
    free(s->a);
    free(s->used);
    *s = t;
  }
  size_t i = (size_t)key_hash64(k) & (s->cap - 1);
  while (s->used[i]) {
    if (key_eq(&s->a[i], k)) return;
    i = (i + 1) & (s->cap - 1);
  }
  s->used[i] = 1;
  s->a[i] = *k;
  s->n++;
}

/* keys of every other layer a child (and, through e.p. transients, its children) reaches */
static void child_keys(const Child *c, const Key *self, KeySet *ks) {
  if (c->kind == 1) return;
  if (c->kind == 0) {
    if (!pos_in_key(&c->pos, self)) {
      Key k;
      key_of(&c->pos, &k);
      ks_add(ks, &k);
    }
    return;
  }
  Child *ch = malloc(sizeof(Child) * MAXMOVES);
  int m = gen_moves(&c->pos, ch);
  for (int i = 0; i < m; i++) child_keys(&ch[i], self, ks);
  free(ch);
}

/* ---- parallel driver: workers take chunks of [0, n) ---- */

typedef struct Job Job;
typedef void (*Work)(Job *j, size_t lo, size_t hi);
struct Job {
  Layer *L;
  Work fn;
  size_t *next;
  Child *ch;
  KeySet ks;
  Vec src, dst;
  uint8_t *aux;
  size_t changed;
};
#define CHUNK 4096

static void *worker(void *arg) {
  Job *j = arg;
  for (;;) {
    size_t lo = __atomic_fetch_add(j->next, CHUNK, __ATOMIC_RELAXED);
    if (lo >= j->L->n) break;
    size_t hi = lo + CHUNK < j->L->n ? lo + CHUNK : j->L->n;
    j->fn(j, lo, hi);
  }
  return NULL;
}

/* run fn over the layer on all threads (inline when the layer is small) */
static Job *run_jobs(Layer *L, Work fn, uint8_t *aux, int *njobs) {
  int nt = L->n >= 65536 ? NT : 1;
  Job *jobs = calloc((size_t)nt, sizeof *jobs);
  size_t next = 0;
  for (int t = 0; t < nt; t++) {
    jobs[t].L = L;
    jobs[t].fn = fn;
    jobs[t].next = &next;
    jobs[t].ch = malloc(sizeof(Child) * MAXMOVES);
    jobs[t].aux = aux;
  }
  if (nt == 1) worker(&jobs[0]);
  else {
    pthread_t *th = malloc(sizeof *th * (size_t)nt);
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_attr_setstacksize(&attr, (size_t)64 << 20);
    inParallel = 1;
    for (int t = 0; t < nt; t++) pthread_create(&th[t], &attr, worker, &jobs[t]);
    for (int t = 0; t < nt; t++) pthread_join(th[t], NULL);
    inParallel = 0;
    free(th);
  }
  for (int t = 0; t < nt; t++) free(jobs[t].ch);
  *njobs = nt;
  return jobs;
}

static void work_keys(Job *j, size_t lo, size_t hi) {
  for (size_t idx = lo; idx < hi; idx++) {
    Pos p;
    pos_decode(&j->L->key, idx, &p);
    if (!legal_state(&p)) continue;
    int m = gen_moves(&p, j->ch);
    for (int i = 0; i < m; i++) child_keys(&j->ch[i], &j->L->key, &j->ks);
  }
}

/* graph method, first pass: classify each state and record in-layer edges */
static void work_graph(Job *j, size_t lo, size_t hi) {
  Layer *L = j->L;
  int8_t *val = L->val;
  uint8_t *rem = j->aux;
  for (size_t idx = lo; idx < hi; idx++) {
    Pos p;
    pos_decode(&L->key, idx, &p);
    if (!legal_state(&p)) { val[idx] = VILL; continue; }
    int m = gen_moves(&p, j->ch);
    if (m == 0) { val[idx] = in_check(&p, p.stm) ? VLOSS : VDRAW; continue; }
    int win = 0, draw = 0, cnt = 0;
    for (int i = 0; i < m && !win; i++) {
      Child *c = &j->ch[i];
      if (c->kind == 0 && pos_in_key(&c->pos, &L->key)) {
        vpush(&j->src, (uint32_t)idx);
        vpush(&j->dst, (uint32_t)pos_index(&c->pos));
        cnt++;
        continue;
      }
      int v = child_value(c);
      if (v == VLOSS) win = 1;
      else if (v != VWIN) draw = 1;
    }
    if (win) val[idx] = VWIN;
    else if (cnt == 0 && !draw) val[idx] = VLOSS;
    else rem[idx] = (uint8_t)(cnt + draw);
  }
}

static void solve_graph(Layer *L) {
  size_t n = L->n;
  int8_t *val = L->val;
  uint8_t *rem = calloc(n, 1);
  int nj;
  Job *jobs = run_jobs(L, work_graph, rem, &nj);
  /* predecessor lists */
  size_t ne = 0;
  for (int t = 0; t < nj; t++) ne += jobs[t].dst.n;
  uint32_t *start = calloc(n + 1, sizeof *start), *pred = malloc((ne + 1) * sizeof *pred);
  for (int t = 0; t < nj; t++)
    for (size_t e = 0; e < jobs[t].dst.n; e++) start[jobs[t].dst.a[e] + 1]++;
  for (size_t i = 0; i < n; i++) start[i + 1] += start[i];
  uint32_t *fill = malloc((n + 1) * sizeof *fill);
  memcpy(fill, start, (n + 1) * sizeof *fill);
  for (int t = 0; t < nj; t++) {
    for (size_t e = 0; e < jobs[t].dst.n; e++) pred[fill[jobs[t].dst.a[e]]++] = jobs[t].src.a[e];
    free(jobs[t].src.a);
    free(jobs[t].dst.a);
  }
  free(fill);
  free(jobs);
  /* propagate */
  uint32_t *queue = malloc(n * sizeof *queue);
  size_t qh = 0, qt = 0;
  for (size_t i = 0; i < n; i++)
    if (val[i] == VWIN || val[i] == VLOSS) queue[qt++] = (uint32_t)i;
  while (qh < qt) {
    uint32_t t = queue[qh++];
    for (uint32_t e = start[t]; e < start[t + 1]; e++) {
      uint32_t s = pred[e];
      if (val[s] != VUNK) continue;
      if (val[t] == VLOSS) { val[s] = VWIN; queue[qt++] = s; }
      else if (--rem[s] == 0) { val[s] = VLOSS; queue[qt++] = s; }
    }
  }
  for (size_t i = 0; i < n; i++)
    if (val[i] == VUNK) val[i] = VDRAW;
  free(queue);
  free(start);
  free(pred);
  free(rem);
}

/* pass method (layers too large for an explicit graph) */
static void work_pass_init(Job *j, size_t lo, size_t hi) {
  Layer *L = j->L;
  for (size_t idx = lo; idx < hi; idx++) {
    Pos p;
    pos_decode(&L->key, idx, &p);
    if (!legal_state(&p)) { L->val[idx] = VILL; continue; }
    int m = gen_moves(&p, j->ch);
    if (m == 0) { L->val[idx] = in_check(&p, p.stm) ? VLOSS : VDRAW; continue; }
    for (int i = 0; i < m; i++) {
      if (j->ch[i].kind == 0 && pos_in_key(&j->ch[i].pos, &L->key)) continue;
      int v = child_value(&j->ch[i]);
      if (v == VLOSS) { L->val[idx] = VWIN; break; }
      if (v != VWIN) j->aux[idx] = 1; /* a drawn exit: never lost */
    }
  }
}

static void work_pass(Job *j, size_t lo, size_t hi) {
  Layer *L = j->L;
  for (size_t idx = lo; idx < hi; idx++) {
    if (__atomic_load_n(&L->val[idx], __ATOMIC_RELAXED) != VUNK) continue;
    Pos p;
    pos_decode(&L->key, idx, &p);
    int m = gen_moves(&p, j->ch), win = 0, allwon = !j->aux[idx];
    for (int i = 0; i < m && !win; i++) {
      if (!(j->ch[i].kind == 0 && pos_in_key(&j->ch[i].pos, &L->key))) continue;
      int v = __atomic_load_n(&L->val[pos_index(&j->ch[i].pos)], __ATOMIC_RELAXED);
      if (v == VLOSS) win = 1;
      else if (v != VWIN) allwon = 0;
    }
    if (win || allwon) {
      __atomic_store_n(&L->val[idx], (int8_t)(win ? VWIN : VLOSS), __ATOMIC_RELAXED);
      j->changed++;
    }
  }
}

static void solve_passes(Layer *L) {
  uint8_t *drawExit = calloc(L->n, 1);
  int nj;
  free(run_jobs(L, work_pass_init, drawExit, &nj));
  size_t changed;
  do {
    Job *jobs = run_jobs(L, work_pass, drawExit, &nj);
    changed = 0;
    for (int t = 0; t < nj; t++) changed += jobs[t].changed;
    free(jobs);
  } while (changed);
  for (size_t i = 0; i < L->n; i++)
    if (L->val[i] == VUNK) L->val[i] = VDRAW;
  free(drawExit);
}

static Layer *get_layer(const Key *k) {
  Layer *L = find_layer(k);
  if (L) return L;
  L = calloc(1, sizeof *L);
  L->key = *k;
  L->n = layer_size(k->no);
  if (++depthNow > depthMax) depthMax = depthNow;
  /* phase 1: solve every layer this one can reach (recursively), single writer */
  int nj;
  Job *jobs = run_jobs(L, work_keys, NULL, &nj);
  KeySet all = {0};
  for (int t = 0; t < nj; t++) {
    for (size_t i = 0; i < jobs[t].ks.cap; i++)
      if (jobs[t].ks.used[i]) ks_add(&all, &jobs[t].ks.a[i]);
    free(jobs[t].ks.a);
    free(jobs[t].ks.used);
  }
  free(jobs);
  for (size_t i = 0; i < all.cap; i++)
    if (all.used[i]) get_layer(&all.a[i]);
  free(all.a);
  free(all.used);
  /* phase 2: this layer, every lookup now read-only */
  L->val = calloc(L->n, 1);
  if (L->n > PASS_THRESHOLD) solve_passes(L);
  else solve_graph(L);
  depthNow--;
  size_t h = key_hash(k);
  L->next = htab[h];
  htab[h] = L;
  nlayers++;
  nstatesTotal += L->n;
  return L;
}

/* ---------- input / output ---------- */

static int parse_square(const char *s, int *sq) {
  if (s[0] < 'a' || s[0] >= 'a' + W) return 0;
  char *end;
  long r = strtol(s + 1, &end, 10);
  if (end == s + 1 || *end || r < 1 || r > H) return 0;
  *sq = (int)(r - 1) * W + (s[0] - 'a');
  return 1;
}

static void sqname(int s, char *out) { sprintf(out, "%c%d", 'a' + s % W, s / W + 1); }

/* parse a position line; returns 0 if malformed or illegal */
static int parse_pos(const char *line, Pos *p) {
  char buf[512];
  snprintf(buf, sizeof buf, "%s", line);
  memset(p, 0, sizeof *p);
  p->wk = p->bk = -1;
  p->ep = -1;
  p->stm = -1;
  int nwk = 0, nbk = 0, epSeen = 0;
  for (char *t = strtok(buf, " \t\r\n"); t; t = strtok(NULL, " \t\r\n")) {

    if (p->stm < 0 && (!strcmp(t, "w") || !strcmp(t, "b"))) { p->stm = t[0] == 'b'; continue; }
    if (p->stm >= 0 && !epSeen) {
      epSeen = 1;
      if (!strcmp(t, "-")) continue;
      int s;
      if (!parse_square(t, &s)) return 0;
      p->ep = s;
      continue;
    }
    int s;
    if (!parse_square(t + 1, &s)) return 0;
    if (occupancy(p) & BIT(s) && (p->wk == s || p->bk == s || ((p->wp | p->bp) >> s & 1))) return 0;
    for (int j = 0; j < p->no; j++)
      if (p->osq[j] == s) return 0;
    char c = t[0];
    int colour = isupper((unsigned char)c) ? WHITE : BLACK, r = s / W;
    switch (toupper((unsigned char)c)) {
      case 'K':
        if (colour == WHITE) { if (p->wk == s) return 0; p->wk = s; nwk++; }
        else { p->bk = s; nbk++; }
        break;
      case 'P':
        if (r == 0 || r == H - 1) return 0;
        if (colour == WHITE) p->wp |= BIT(s);
        else p->bp |= BIT(s);
        break;
      case 'Q': case 'R': case 'B': case 'N': {
        if (p->no >= MAXOFF) return 0;
        const char *q = strchr(TYPECH, toupper((unsigned char)c));
        p->osq[p->no] = s;
        p->ot[p->no] = (int)(q - TYPECH) + 8 * colour;
        p->no++;
        break;
      }
      default: return 0;
    }
  }
  if (nwk != 1 || nbk != 1 || p->stm < 0 || !epSeen || p->no > CAP) return 0;
  if (!EPON) p->ep = -1;
  canonicalize(p);
  if (!legal_state(p)) return 0;
  if (p->ep >= 0) { /* must be the square just skipped by an enemy double step */
    int mover = !p->stm, skipped = p->ep, landed = skipped + (mover == WHITE ? W : -W),
        origin = skipped - (mover == WHITE ? W : -W);
    if (skipped / W != (mover == WHITE ? 2 : H - 3)) return 0;
    if (!(((mover == WHITE ? p->wp : p->bp) >> landed) & 1)) return 0;
    if ((occupancy(p) >> skipped) & 1 || (occupancy(p) >> origin) & 1) return 0;
  }
  return 1;
}

static char wpov(int v, int stm) {
  if (v == VDRAW) return 'D';
  if (v == VILL) return 'X';
  return (v == VWIN) == (stm == WHITE) ? 'W' : 'L';
}

static char *strip(char *s) {
  size_t n = strlen(s);
  while (n && (s[n - 1] == '\n' || s[n - 1] == '\r')) s[--n] = 0;
  return s;
}

typedef struct { char *line; int ok; Pos pos; char res[2]; char *moves[2]; } Item;

static void move_text(const Child *c, char *out) {
  char a[8], b[8];
  sqname(c->from, a);
  sqname(c->to, b);
  if (c->promo) sprintf(out, "%c%s%s=%c", c->piece, a, b, TYPECH[c->promo]);
  else sprintf(out, "%c%s%s", c->piece, a, b);
}

static void run_bound(Item *items, int n, int bound) {
  BOUND = bound;
  reset_tables();
  Child *ch = malloc(sizeof(Child) * MAXMOVES);
  for (int i = 0; i < n; i++) {
    if (!items[i].ok) { items[i].res[bound] = 'X'; continue; }
    const Pos *p = &items[i].pos;
    int v = p->ep >= 0 ? transient_value(p) : pos_value(p);
    items[i].res[bound] = wpov(v, p->stm);
    if (WANTMOVES) {
      int m = gen_moves(p, ch);
      size_t cap = 64 + (size_t)m * 24, len = 0;
      char *s = malloc(cap);
      s[0] = 0;
      for (int j = 0; j < m; j++) {
        char mt[24];
        move_text(&ch[j], mt);
        int cv = child_value(&ch[j]);
        len += (size_t)snprintf(s + len, cap - len, "%s%s:%c", j ? " " : "", mt, wpov(cv, ch[j].pos.stm));
      }
      items[i].moves[bound] = s;
    }
  }
  free(ch);
}

static int usage(void) {
  fprintf(stderr, "usage: kpsolve --board flat:WxH|cyl:WxH [--ep on|off] [--promote QRBN] [--cap C]"
                  " [--frozen] [--moves] [--threads T] < positions > results\n");
  return 2;
}

typedef struct { int argc; char **argv; int rc; } MainArgs;

static void *real_main(void *arg) {
  MainArgs *ma = arg;
  int argc = ma->argc;
  char **argv = ma->argv;
  const char *promo = "QRBN";
  int boardSet = 0;
  for (int i = 1; i < argc; i++) {
    if (!strcmp(argv[i], "--board") && i + 1 < argc) {
      char kind[8];
      if (sscanf(argv[++i], "%7[a-z]:%dx%d", kind, &W, &H) != 3) { ma->rc = usage(); return NULL; }
      if (!strcmp(kind, "cyl")) WRAP = 1;
      else if (!strcmp(kind, "flat")) WRAP = 0;
      else { ma->rc = usage(); return NULL; }
      boardSet = 1;
    } else if (!strcmp(argv[i], "--ep") && i + 1 < argc) EPON = !strcmp(argv[++i], "on");
    else if (!strcmp(argv[i], "--promote") && i + 1 < argc) promo = argv[++i];
    else if (!strcmp(argv[i], "--cap") && i + 1 < argc) CAP = atoi(argv[++i]);
    else if (!strcmp(argv[i], "--frozen")) FROZEN = 1;
    else if (!strcmp(argv[i], "--moves")) WANTMOVES = 1;
    else if (!strcmp(argv[i], "--threads") && i + 1 < argc) NT = atoi(argv[++i]);
    else { ma->rc = usage(); return NULL; }
  }
  if (!boardSet || W < 2 || W > 8 || H < 4 || H > 8 || CAP < 0 || CAP > MAXOFF - 1) {
    ma->rc = usage();
    return NULL;
  }
  N = W * H;
  if (NT < 1) NT = 1;
  nPromo = 0;
  for (const char *c = promo; *c; c++) {
    const char *q = strchr(TYPECH + 1, toupper((unsigned char)*c));
    if (!q) { ma->rc = usage(); return NULL; }
    promoType[nPromo++] = (int)(q - TYPECH);
  }
  init_geometry();

  int n = 0, cap = 1024;
  Item *items = calloc((size_t)cap, sizeof *items);
  char line[1024];
  while (fgets(line, sizeof line, stdin)) {
    if (n == cap) items = realloc(items, sizeof *items * (size_t)(cap *= 2));
    memset(&items[n], 0, sizeof items[n]);
    items[n].line = strdup(strip(line));
    const char *t = items[n].line;
    while (*t == ' ') t++;
    if (*t == '#' || !*t) items[n].ok = -1;
    else items[n].ok = parse_pos(items[n].line, &items[n].pos);
    n++;
  }
  struct timespec t0, t1;
  clock_gettime(CLOCK_MONOTONIC, &t0);
  cappedSeen = 0;
  run_bound(items, n, 0);
  int boundsDiffer = cappedSeen;
  if (boundsDiffer) run_bound(items, n, 1);
  else
    for (int i = 0; i < n; i++) {
      items[i].res[1] = items[i].res[0];
      items[i].moves[1] = items[i].moves[0];
    }
  for (int i = 0; i < n; i++) {
    if (items[i].ok < 0) { printf("%s\n", items[i].line); continue; }
    printf("%s | %c %c", items[i].line, items[i].res[0], items[i].res[1]);
    if (WANTMOVES && items[i].moves[0]) {
      if (boundsDiffer) printf(" | A: %s | B: %s", items[i].moves[0], items[i].moves[1]);
      else printf(" | %s", items[i].moves[0]);
    }
    printf("\n");
  }
  clock_gettime(CLOCK_MONOTONIC, &t1);
  fprintf(stderr, "[kpsolve %s:%dx%d ep=%s cap=%d%s: %zu layers, %zu states, depth %d, %.1fs%s]\n",
          WRAP ? "cyl" : "flat", W, H, EPON ? "on" : "off", CAP, FROZEN ? " frozen" : "", nlayers,
          nstatesTotal, depthMax, (double)(t1.tv_sec - t0.tv_sec) + 1e-9 * (double)(t1.tv_nsec - t0.tv_nsec),
          boundsDiffer ? ", capped promotions met (two bounds)" : "");
  ma->rc = 0;
  return NULL;
}

int main(int argc, char **argv) {
  /* deep recursion through layers: run on a thread with a large stack */
  pthread_attr_t attr;
  pthread_t th;
  MainArgs ma = {argc, argv, 0};
  pthread_attr_init(&attr);
  pthread_attr_setstacksize(&attr, (size_t)1 << 29);
  pthread_create(&th, &attr, real_main, &ma);
  pthread_join(th, NULL);
  return ma.rc;
}
