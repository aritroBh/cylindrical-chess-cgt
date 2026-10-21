/* pcgt.c -- exact canonical CGT values of pawn-only positions, in C.
 *
 * Workstream A3-targets (2026-10-16). A port of the *model and algorithm* of
 * cylcgt (cylcgt/cgt.py canonical forms + cylcgt/pawns.py rules, read-only),
 * written so that the Elkies-target hunt can go beyond what Python manages on
 * a heavily loaded machine (wider boards, 6-pawn cylinder rings). It is NOT an
 * independent derivation: it follows cylcgt's design (sum of components, the
 * e.p. right attached to its component, the passed test, the race rules, the
 * canonicalisation loop). Its job is speed; correctness is established by
 * reproducing cylcgt's database string-for-string (see check_db.py).
 *
 * Model (Elkies 1996 conventions, as in cylcgt):
 *   White = Left, Black = Right, normal play.
 *   A position where exactly one side has a passed pawn = +BIG / -BIG (BIG 256).
 *   A move giving both sides a passer = race, scored by the race rule:
 *     count    : the mover's opponent moves first; fewer moves to promote wins,
 *                ties to the opponent;
 *     mover    : the mover wins;   opponent : the mover loses.
 *   Board: W files (1..8) x 8 ranks, flat or cylinder (files a and last adjacent).
 *   Pawns: single step, double step from the 2nd/7th rank, diagonal capture,
 *   en passant (when enabled). An e.p. right lives until someone moves in the
 *   component that holds it (the cylcgt short-game convention).
 *   Passed test: textbook, or --aware 1: a pawn that can still be taken e.p. now
 *   is not passed (cylcgt.pawns.PASSED_RESPECTS_EP in the ep-aware-passed branch).
 *   A position splits into components separated by empty files; its value is
 *   the sum (after checking the whole board for a one-sided passer first).
 *
 * Build:  cc -O2 -o pcgt pcgt.c
 * Input (stdin): lines  "W: a2 c2 / B: b7 d7<TAB>width<TAB>wrap(0|1)[<TAB>race<TAB>ep<TAB>aware]"
 *   (the optional columns override the command-line defaults per line; the game
 *   store is shared, so value ids are comparable across settings and boards)
 * Options: --race count|mover|opponent|white|black  --ep 0|1  --aware 0|1
 *          --printlimit N (print show/key of a +-W game only if its tree has <= N nodes)
 *          --enum W wrap nmin nmax connected : print root positions and exit
 *            (pawns on ranks 2-7, w,b >= 1, no passed pawn; flat: files a and the
 *            W-th occupied, mirror-reduced; cylinder: dihedral-reduced; connected=1:
 *            every file occupied); 4th column = number of board positions (orbit size)
 *   (white / black: every race is won by that side; by monotonicity of game
 *   values in their options, a value equal under both holds for every way of
 *   scoring the races)
 * Output: per input line "position<TAB>width<TAB>wrap<TAB>race<TAB>ep<TAB>aware<TAB>gid<TAB>outcome";
 *         then "#V<TAB>gid<TAB>big<TAB>hash128<TAB>show<TAB>key" for every distinct root value
 *         (big = 1 if a number with |x| >= 128, i.e. a +-W, occurs in the game), where
 *         show = cgt.show with option lists sorted (norm_show) and key = exact
 *         injective canonical key (numbers exact, *k as "*k", else
 *         "{sorted L keys|sorted R keys}"), as atlas/cylinder/atlas_run.py vkey.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef int64_t fx; /* dyadic number, value = v / 2^SHIFT */
#define SHIFT 32
#define ONE ((fx)1 << SHIFT)
#define BIG 256

static void *xmalloc(size_t n) { void *p = malloc(n); if (!p) { fprintf(stderr, "oom\n"); exit(1); } return p; }
static void *xrealloc(void *q, size_t n) { void *p = realloc(q, n); if (!p) { fprintf(stderr, "oom\n"); exit(1); } return p; }
static void *xcalloc(size_t a, size_t b) { void *p = calloc(a, b); if (!p) { fprintf(stderr, "oom\n"); exit(1); } return p; }

static inline uint64_t mix(uint64_t x) {
    x += 0x9E3779B97F4A7C15ull;
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ull;
    x = (x ^ (x >> 27)) * 0x94D049BB133111EBull;
    return x ^ (x >> 31);
}

/* ======================================================= game store */
typedef struct {
    int nL, nR;
    int *o;      /* nL left ids, then nR right ids */
    int isnum;
    fx num;
    int nim;     /* -1 if not a nimber */
    char *show, *key;
} Node;
static Node *N; static int NN, NCAP;

static int new_node(const int *L, int nL, const int *R, int nR) {
    if (NN == NCAP) { NCAP = NCAP ? NCAP * 2 : 1 << 16; N = xrealloc(N, (size_t)NCAP * sizeof(Node)); }
    Node *g = &N[NN];
    g->nL = nL; g->nR = nR;
    g->o = xmalloc(sizeof(int) * (size_t)(nL + nR + 1));
    if (nL) memcpy(g->o, L, sizeof(int) * (size_t)nL);
    if (nR) memcpy(g->o + nL, R, sizeof(int) * (size_t)nR);
    g->isnum = 0; g->num = 0; g->nim = -1; g->show = NULL; g->key = NULL;
    return NN++;
}
/* The temporary game {L | R} that make() compares against lives in one scratch
 * slot RAWN with a fresh id RAWID >= RAWBASE each time (ids are never reused, so
 * no memo entry can be confused with a later game). */
#define RAWBASE (1 << 30)
static Node RAWN; static int RAWID = -1; static int64_t rawctr = RAWBASE;
#define ND(g) ((g) == RAWID ? &RAWN : &N[g])
#define LOPT(g, i) (ND(g)->o[i])
#define ROPT(g, i) (ND(g)->o[ND(g)->nL + (i)])

/* ---- hash-cons table for interned (canonical) games */
static int *HC; static uint64_t HCcap, HCcount;
static uint64_t hash_opts(const int *L, int nL, const int *R, int nR) {
    uint64_t h = mix((uint64_t)nL * 1000003u + (uint64_t)nR);
    for (int i = 0; i < nL; i++) h = mix(h ^ (uint64_t)(uint32_t)L[i]);
    h = mix(h ^ 0xABCDEFull);
    for (int i = 0; i < nR; i++) h = mix(h ^ (uint64_t)(uint32_t)R[i]);
    return h;
}
static int same_opts(int g, const int *L, int nL, const int *R, int nR) {
    if (N[g].nL != nL || N[g].nR != nR) return 0;
    return !memcmp(N[g].o, L, sizeof(int) * (size_t)nL) && !memcmp(N[g].o + nL, R, sizeof(int) * (size_t)nR);
}
static void hc_grow(void) {
    uint64_t oc = HCcap; int *old = HC;
    HCcap = oc ? oc * 2 : 1 << 16;
    HC = xmalloc(sizeof(int) * HCcap);
    for (uint64_t i = 0; i < HCcap; i++) HC[i] = -1;
    for (uint64_t i = 0; i < oc; i++) if (old[i] >= 0) {
        int g = old[i];
        uint64_t h = hash_opts(N[g].o, N[g].nL, N[g].o + N[g].nL, N[g].nR) & (HCcap - 1);
        while (HC[h] >= 0) h = (h + 1) & (HCcap - 1);
        HC[h] = g;
    }
    free(old);
}

/* ---- le memo: packed entries, bit 63 = used, bit 62 = result, a << 31 | b */
static uint64_t *LM; static uint64_t LMcap, LMcount;
#define LM_KEYMASK ((1ull << 62) - 1)
static void lm_grow(void) {
    uint64_t oc = LMcap; uint64_t *old = LM;
    LMcap = oc ? oc * 2 : 1 << 20;
    LM = xcalloc(LMcap, sizeof(uint64_t));
    for (uint64_t i = 0; i < oc; i++) if (old[i]) {
        uint64_t h = mix(old[i] & LM_KEYMASK) & (LMcap - 1);
        while (LM[h]) h = (h + 1) & (LMcap - 1);
        LM[h] = old[i];
    }
    free(old);
}
/* memo for comparisons with the current scratch game (invalidated by generation) */
typedef struct { uint32_t other, gen; uint8_t dir, v; } RmE;
static RmE *RM; static uint64_t RMcap, RMcount; static uint32_t RMgen = 1;
static RmE *rm_find(uint32_t other, int dir) {
    uint64_t h = mix(((uint64_t)other << 1) | (uint64_t)dir) & (RMcap - 1);
    while (RM[h].gen == RMgen && !(RM[h].other == other && RM[h].dir == dir)) h = (h + 1) & (RMcap - 1);
    return &RM[h];
}
static void rm_grow(void) {
    uint64_t oc = RMcap; RmE *old = RM;
    RMcap = oc ? oc * 2 : 1 << 12;
    RM = xcalloc(RMcap, sizeof(RmE));
    for (uint64_t i = 0; i < oc; i++) if (old[i].gen == RMgen) *rm_find(old[i].other, old[i].dir) = old[i];
    free(old);
}

static int le(int a, int b) {
    if (a == b) return 1;
    Node *A = ND(a), *Bn = ND(b);
    if (A->isnum && Bn->isnum) return A->num <= Bn->num;
    if (a == RAWID || b == RAWID) {
        uint32_t other = (uint32_t)(a == RAWID ? b : a); int dir = a == RAWID ? 0 : 1;
        if (!RMcap || (RMcount + 1) * 2 > RMcap) rm_grow();
        RmE *e = rm_find(other, dir);
        if (e->gen == RMgen) return e->v;
        int r = 1;
        for (int i = 0; r && i < A->nL; i++) if (le(b, A->o[i])) r = 0;
        for (int i = 0; r && i < Bn->nR; i++) if (le(Bn->o[Bn->nL + i], a)) r = 0;
        if ((RMcount + 1) * 2 > RMcap) rm_grow();
        e = rm_find(other, dir);
        if (e->gen != RMgen) { e->other = other; e->dir = (uint8_t)dir; e->gen = RMgen; e->v = (uint8_t)r; RMcount++; }
        return r;
    }
    uint64_t k = ((uint64_t)(uint32_t)a << 31) | (uint32_t)b;
    if ((LMcount + 1) * 2 > LMcap) lm_grow();
    uint64_t h = mix(k) & (LMcap - 1);
    while (LM[h] && (LM[h] & LM_KEYMASK) != k) h = (h + 1) & (LMcap - 1);
    if (LM[h]) return (int)((LM[h] >> 62) & 1);
    int r = 1;
    for (int i = 0; r && i < A->nL; i++) if (le(b, A->o[i])) r = 0;
    for (int i = 0; r && i < Bn->nR; i++) if (le(Bn->o[Bn->nL + i], a)) r = 0;
    /* the recursion may have grown the table: find the slot again */
    if ((LMcount + 1) * 2 > LMcap) lm_grow();
    h = mix(k) & (LMcap - 1);
    while (LM[h] && (LM[h] & LM_KEYMASK) != k) h = (h + 1) & (LMcap - 1);
    if (!LM[h]) { LM[h] = k | ((uint64_t)r << 62) | (1ull << 63); LMcount++; }
    return r;
}

/* ---- numbers */
static int64_t floor_div(fx v, fx d) { /* floor(v / d), d > 0 */
    return v >= 0 ? v / d : -((-v + d - 1) / d);
}
static int64_t ifloor(fx v) { return floor_div(v, ONE); }
static int64_t iceil(fx v) { return -floor_div(-v, ONE); }

static fx simplest_between(int haslo, fx lo, int hashi, fx hi) {
    if (!haslo && !hashi) return 0;
    if (!haslo) return hi > 0 ? 0 : (fx)(iceil(hi) - 1) * ONE;
    if (!hashi) return lo < 0 ? 0 : (fx)(ifloor(lo) + 1) * ONE;
    if (lo < 0 && 0 < hi) return 0;
    if (hi > 0) { int64_t n = ifloor(lo) + 1; if ((fx)n * ONE < hi) return (fx)n * ONE; }
    else { int64_t n = iceil(hi) - 1; if ((fx)n * ONE > lo) return (fx)n * ONE; }
    for (int j = 1; j <= SHIFT; j++) {
        int64_t k = floor_div(lo, (fx)1 << (SHIFT - j)) + 1; /* floor(lo * 2^j) + 1 */
        fx c = (fx)k << (SHIFT - j);
        if (c < hi) return c;
    }
    fprintf(stderr, "simplest_between: precision exceeded\n"); exit(3);
}

static int intern(int *L, int nL, int *R, int nR);

static int cmp_int(const void *a, const void *b) { int x = *(const int *)a, y = *(const int *)b; return (x > y) - (x < y); }

static int intern(int *L, int nL, int *R, int nR) {
    qsort(L, (size_t)nL, sizeof(int), cmp_int);
    qsort(R, (size_t)nR, sizeof(int), cmp_int);
    if ((HCcount + 1) * 2 > HCcap) hc_grow();
    uint64_t h = hash_opts(L, nL, R, nR) & (HCcap - 1);
    while (HC[h] >= 0) {
        if (same_opts(HC[h], L, nL, R, nR)) return HC[h];
        h = (h + 1) & (HCcap - 1);
    }
    int g = new_node(L, nL, R, nR);
    HC[h] = g; HCcount++;
    /* number recognition (valid: the form is canonical) */
    if (nL <= 1 && nR <= 1) {
        int ok = 1;
        for (int i = 0; i < nL; i++) if (!N[L[i]].isnum) ok = 0;
        for (int i = 0; i < nR; i++) if (!N[R[i]].isnum) ok = 0;
        if (ok) {
            int hl = nL == 1, hh = nR == 1;
            fx lo = hl ? N[L[0]].num : 0, hi = hh ? N[R[0]].num : 0;
            if (!hl || !hh || lo < hi) { N[g].isnum = 1; N[g].num = simplest_between(hl, lo, hh, hi); }
        }
    }
    /* nimber recognition */
    if (nL == nR && !memcmp(L, R, sizeof(int) * (size_t)nL)) {
        int ok = 1; char seen[256] = {0};
        for (int i = 0; i < nL; i++) {
            int k = N[L[i]].nim;
            if (k < 0 || k >= nL || k >= 256 || seen[k]) { ok = 0; break; }
            seen[k] = 1;
        }
        if (ok) N[g].nim = nL;
    }
    if (nL == 0 && nR == 0) N[g].nim = 0;
    return g;
}

/* dynamic int vector */
typedef struct { int *a; int n, cap; } Vec;
static void vpush(Vec *v, int x) { if (v->n == v->cap) { v->cap = v->cap ? v->cap * 2 : 8; v->a = xrealloc(v->a, sizeof(int) * (size_t)v->cap); } v->a[v->n++] = x; }

static void dedupe(Vec *v) {
    int m = 0;
    for (int i = 0; i < v->n; i++) {
        int dup = 0;
        for (int j = 0; j < m; j++) if (v->a[j] == v->a[i]) { dup = 1; break; }
        if (!dup) v->a[m++] = v->a[i];
    }
    v->n = m;
}
static void keep_maximal(Vec *v) {
    dedupe(v);
    int *keep = xmalloc(sizeof(int) * (size_t)(v->n + 1)); int m = 0;
    for (int i = 0; i < v->n; i++) {
        int dom = 0;
        for (int j = 0; j < v->n && !dom; j++) if (j != i && le(v->a[i], v->a[j])) dom = 1;
        if (!dom) keep[m++] = v->a[i];
    }
    memcpy(v->a, keep, sizeof(int) * (size_t)m); v->n = m; free(keep);
}
static void keep_minimal(Vec *v) {
    dedupe(v);
    int *keep = xmalloc(sizeof(int) * (size_t)(v->n + 1)); int m = 0;
    for (int i = 0; i < v->n; i++) {
        int dom = 0;
        for (int j = 0; j < v->n && !dom; j++) if (j != i && le(v->a[j], v->a[i])) dom = 1;
        if (!dom) keep[m++] = v->a[i];
    }
    memcpy(v->a, keep, sizeof(int) * (size_t)m); v->n = m; free(keep);
}

/* canonical form of {L | R} for canonical options (cgt.make) */
static int make(const int *L0, int nL0, const int *R0, int nR0) {
    Vec L = {0}, R = {0};
    for (int i = 0; i < nL0; i++) vpush(&L, L0[i]);
    for (int i = 0; i < nR0; i++) vpush(&R, R0[i]);
    for (;;) {
        keep_maximal(&L); keep_minimal(&R);
        /* scratch game with the same value, not interned */
        if (rawctr >= ((int64_t)1 << 31) - 1) { fprintf(stderr, "scratch ids exhausted\n"); exit(5); }
        RAWID = (int)rawctr++; RMgen++; RMcount = 0;
        RAWN.nL = L.n; RAWN.nR = R.n; RAWN.isnum = 0; RAWN.nim = -1;
        RAWN.o = xrealloc(RAWN.o, sizeof(int) * (size_t)(L.n + R.n + 1));
        if (L.n) memcpy(RAWN.o, L.a, sizeof(int) * (size_t)L.n);
        if (R.n) memcpy(RAWN.o + L.n, R.a, sizeof(int) * (size_t)R.n);
        int raw = RAWID;
        int changed = 0;
        Vec nL = {0}, nR = {0};
        for (int i = 0; i < L.n; i++) {
            int gl = L.a[i], rev = -1;
            for (int j = 0; j < N[gl].nR; j++) if (le(N[gl].o[N[gl].nL + j], raw)) { rev = N[gl].o[N[gl].nL + j]; break; }
            if (rev < 0) vpush(&nL, gl);
            else { for (int j = 0; j < N[rev].nL; j++) vpush(&nL, LOPT(rev, j)); changed = 1; }
        }
        for (int i = 0; i < R.n; i++) {
            int gr = R.a[i], rev = -1;
            for (int j = 0; j < N[gr].nL; j++) if (le(raw, N[gr].o[j])) { rev = N[gr].o[j]; break; }
            if (rev < 0) vpush(&nR, gr);
            else { for (int j = 0; j < N[rev].nR; j++) vpush(&nR, ROPT(rev, j)); changed = 1; }
        }
        RAWID = -1; /* the scratch game is never referenced again */
        if (!changed) {
            int g = intern(L.a, L.n, R.a, R.n);
            free(L.a); free(R.a); free(nL.a); free(nR.a);
            return g;
        }
        free(L.a); free(R.a); L = nL; R = nR;
    }
}

static int ZERO, STAR;

/* number memo: open addressing on fx */
typedef struct { fx k; int g; int used; } NumE;
static NumE *NM; static uint64_t NMcap, NMcount;
static int num_lookup(fx x) {
    if (!NMcap) return -1;
    uint64_t h = mix((uint64_t)x) & (NMcap - 1);
    while (NM[h].used) { if (NM[h].k == x) return NM[h].g; h = (h + 1) & (NMcap - 1); }
    return -1;
}
static void num_store(fx x, int g) {
    if ((NMcount + 1) * 2 > NMcap) {
        uint64_t oc = NMcap; NumE *old = NM;
        NMcap = oc ? oc * 2 : 1024; NM = xcalloc(NMcap, sizeof(NumE));
        for (uint64_t i = 0; i < oc; i++) if (old[i].used) {
            uint64_t h = mix((uint64_t)old[i].k) & (NMcap - 1);
            while (NM[h].used) h = (h + 1) & (NMcap - 1);
            NM[h] = old[i];
        }
        free(old);
    }
    uint64_t h = mix((uint64_t)x) & (NMcap - 1);
    while (NM[h].used) h = (h + 1) & (NMcap - 1);
    NM[h].k = x; NM[h].g = g; NM[h].used = 1; NMcount++;
}
static int number(fx x) {
    int g = num_lookup(x);
    if (g >= 0) return g;
    if (x % ONE == 0) {
        int64_t n = x / ONE;
        if (n == 0) g = ZERO;
        else if (n > 0) { int p = number(x - ONE); g = make(&p, 1, NULL, 0); }
        else { int p = number(x + ONE); g = make(NULL, 0, &p, 1); }
    } else {
        fx unit = x & (-x); /* 1/d */
        int a = number(x - unit), b = number(x + unit);
        g = make(&a, 1, &b, 1);
    }
    num_store(x, g);
    return g;
}

static int *NEGM; static int NEGcap;
static void neg_reserve(int m) {
    if (m < NEGcap) return;
    int oc = NEGcap; NEGcap = (m + 1) * 2;
    NEGM = xrealloc(NEGM, sizeof(int) * (size_t)NEGcap);
    for (int i = oc; i < NEGcap; i++) NEGM[i] = -1;
}
static int neg(int g) {
    neg_reserve(g);
    if (NEGM[g] >= 0) return NEGM[g];
    int r;
    if (N[g].isnum) r = number(-N[g].num);
    else {
        int nL = N[g].nR, nR = N[g].nL;
        int *L = xmalloc(sizeof(int) * (size_t)(nL + 1)), *R = xmalloc(sizeof(int) * (size_t)(nR + 1));
        for (int i = 0; i < nL; i++) L[i] = neg(ROPT(g, i));
        for (int i = 0; i < nR; i++) R[i] = neg(LOPT(g, i));
        r = make(L, nL, R, nR); free(L); free(R);
    }
    neg_reserve(g > r ? g : r);
    NEGM[g] = r;
    return r;
}

typedef struct { uint64_t k; int g; } AddE;
static AddE *AM; static uint64_t AMcap, AMcount;
static int add(int a, int b) {
    if (a == ZERO) return b;
    if (b == ZERO) return a;
    if (N[a].isnum && N[b].isnum) return number(N[a].num + N[b].num);
    if (a > b) { int t = a; a = b; b = t; }
    uint64_t k = ((uint64_t)(uint32_t)a << 32) | (uint32_t)b;
    if (AMcap) {
        uint64_t h = mix(k) & (AMcap - 1);
        while (AM[h].k) { if (AM[h].k == k) return AM[h].g; h = (h + 1) & (AMcap - 1); }
    }
    int nL = N[a].nL + N[b].nL, nR = N[a].nR + N[b].nR;
    int *L = xmalloc(sizeof(int) * (size_t)(nL + 1)), *R = xmalloc(sizeof(int) * (size_t)(nR + 1));
    int i = 0;
    for (int j = 0; j < N[a].nL; j++) L[i++] = add(LOPT(a, j), b);
    for (int j = 0; j < N[b].nL; j++) L[i++] = add(a, LOPT(b, j));
    i = 0;
    for (int j = 0; j < N[a].nR; j++) R[i++] = add(ROPT(a, j), b);
    for (int j = 0; j < N[b].nR; j++) R[i++] = add(a, ROPT(b, j));
    int r = make(L, nL, R, nR); free(L); free(R);
    if ((AMcount + 1) * 2 > AMcap) {
        uint64_t oc = AMcap; AddE *old = AM;
        AMcap = oc ? oc * 2 : 1 << 16; AM = xcalloc(AMcap, sizeof(AddE));
        for (uint64_t q = 0; q < oc; q++) if (old[q].k) {
            uint64_t h = mix(old[q].k) & (AMcap - 1);
            while (AM[h].k) h = (h + 1) & (AMcap - 1);
            AM[h] = old[q];
        }
        free(old);
    }
    uint64_t h = mix(k) & (AMcap - 1);
    while (AM[h].k) h = (h + 1) & (AMcap - 1);
    AM[h].k = k; AM[h].g = r; AMcount++;
    return r;
}

/* ======================================================= display */
static int UP, DOWN, UPSTAR, DOWNSTAR, DUP, DDOWN, DUPSTAR, DDOWNSTAR, TUP, TDOWN;

static char *sdup(const char *s) { size_t n = strlen(s) + 1; char *p = xmalloc(n); memcpy(p, s, n); return p; }

static void fmt_num(char *buf, fx x, int bigabbr) {
    if (bigabbr && (x >= (fx)128 * ONE || x <= -(fx)128 * ONE)) { strcpy(buf, x > 0 ? "+W" : "-W"); return; }
    if (x % ONE == 0) { sprintf(buf, "%lld", (long long)(x / ONE)); return; }
    int64_t n = x, d = ONE;
    while ((n % 2) == 0) { n /= 2; d /= 2; }
    sprintf(buf, "%lld/%lld", (long long)n, (long long)d);
}

static int cmp_str(const void *a, const void *b) { return strcmp(*(char *const *)a, *(char *const *)b); }

static const char *show(int g);
static char *join_sorted(int g, int side) { /* side 0 = L, 1 = R */
    int n = side ? N[g].nR : N[g].nL;
    const char **xs = xmalloc(sizeof(char *) * (size_t)(n + 1));
    size_t tot = 1;
    for (int i = 0; i < n; i++) { xs[i] = show(side ? ROPT(g, i) : LOPT(g, i)); tot += strlen(xs[i]) + 2; }
    qsort(xs, (size_t)n, sizeof(char *), cmp_str);
    char *out = xmalloc(tot); out[0] = 0;
    for (int i = 0; i < n; i++) { if (i) strcat(out, ", "); strcat(out, xs[i]); }
    free(xs);
    return out;
}

static const char *show(int g) {
    if (N[g].show) return N[g].show;
    char buf[128];
    if (N[g].isnum) { fmt_num(buf, N[g].num, 1); return N[g].show = sdup(buf); }
    if (N[g].nim >= 0) { if (N[g].nim == 1) strcpy(buf, "*"); else sprintf(buf, "*%d", N[g].nim); return N[g].show = sdup(buf); }
    const char *nm = NULL;
    if (g == UP) nm = "↑"; else if (g == DOWN) nm = "↓"; else if (g == UPSTAR) nm = "↑*"; else if (g == DOWNSTAR) nm = "↓*";
    else if (g == DUP) nm = "⇑"; else if (g == DDOWN) nm = "⇓"; else if (g == DUPSTAR) nm = "⇑*"; else if (g == DDOWNSTAR) nm = "⇓*";
    else if (g == TUP) nm = "3↑"; else if (g == TDOWN) nm = "3↓";
    if (nm) return N[g].show = sdup(nm);
    int nL = N[g].nL, nR = N[g].nR;
    if (nL == 1 && nR == 1 && N[LOPT(g, 0)].isnum && N[ROPT(g, 0)].isnum) {
        fx a = N[LOPT(g, 0)].num, b = N[ROPT(g, 0)].num;
        char x[64], y[64];
        if (a == b) { fmt_num(x, a, 1); sprintf(buf, "%s*", x); return N[g].show = sdup(buf); }
        fx m = (a + b) / 2, d = (a - b) / 2;
        fmt_num(y, d, 1);
        if (m == 0) sprintf(buf, "±%s", y); else { fmt_num(x, m, 1); sprintf(buf, "%s±%s", x, y); }
        return N[g].show = sdup(buf);
    }
    if (nL == 1 && LOPT(g, 0) == ZERO && nR == 1) {
        int r = ROPT(g, 0);
        if (N[r].nL == 1 && LOPT(r, 0) == ZERO && N[r].nR == 1 && N[ROPT(r, 0)].isnum) {
            char x[64]; fmt_num(x, -N[ROPT(r, 0)].num, 1); sprintf(buf, "tiny(%s)", x); return N[g].show = sdup(buf);
        }
    }
    if (nR == 1 && ROPT(g, 0) == ZERO && nL == 1) {
        int l = LOPT(g, 0);
        if (N[l].nR == 1 && ROPT(l, 0) == ZERO && N[l].nL == 1 && N[LOPT(l, 0)].isnum) {
            char x[64]; fmt_num(x, N[LOPT(l, 0)].num, 1); sprintf(buf, "miny(%s)", x); return N[g].show = sdup(buf);
        }
    }
    char *ls = join_sorted(g, 0), *rs = join_sorted(g, 1);
    char *out = xmalloc(strlen(ls) + strlen(rs) + 8);
    sprintf(out, "{%s | %s}", ls, rs);
    free(ls); free(rs);
    return N[g].show = out;
}

static const char *key(int g) {
    if (N[g].key) return N[g].key;
    char buf[128];
    if (N[g].isnum) { fmt_num(buf, N[g].num, 0); return N[g].key = sdup(buf); }
    if (N[g].nim >= 0) { sprintf(buf, "*%d", N[g].nim); return N[g].key = sdup(buf); }
    int nL = N[g].nL, nR = N[g].nR;
    const char **xs = xmalloc(sizeof(char *) * (size_t)(nL + nR + 1));
    size_t tot = 4;
    for (int i = 0; i < nL; i++) { xs[i] = key(LOPT(g, i)); tot += strlen(xs[i]) + 1; }
    for (int i = 0; i < nR; i++) { xs[nL + i] = key(ROPT(g, i)); tot += strlen(xs[nL + i]) + 1; }
    qsort(xs, (size_t)nL, sizeof(char *), cmp_str);
    qsort(xs + nL, (size_t)nR, sizeof(char *), cmp_str);
    char *out = xmalloc(tot); char *p = out;
    *p++ = '{';
    for (int i = 0; i < nL; i++) { if (i) *p++ = ','; size_t n = strlen(xs[i]); memcpy(p, xs[i], n); p += n; }
    *p++ = '|';
    for (int i = 0; i < nR; i++) { if (i) *p++ = ','; size_t n = strlen(xs[nL + i]); memcpy(p, xs[nL + i], n); p += n; }
    *p++ = '}'; *p = 0;
    free(xs);
    return N[g].key = out;
}

static signed char *BIGM; static int BIGcap;
static int has_big(int g) {
    if (g >= BIGcap) { int oc = BIGcap; BIGcap = (g + 1) * 2; BIGM = xrealloc(BIGM, (size_t)BIGcap); memset(BIGM + oc, -1, (size_t)(BIGcap - oc)); }
    if (BIGM[g] >= 0) return BIGM[g];
    int r = 0;
    if (N[g].isnum) r = N[g].num >= (fx)128 * ONE || N[g].num <= -(fx)128 * ONE;
    else {
        for (int i = 0; !r && i < N[g].nL; i++) r = has_big(LOPT(g, i));
        for (int i = 0; !r && i < N[g].nR; i++) r = has_big(ROPT(g, i));
    }
    BIGM[g] = (signed char)r;
    return r;
}

static char outcome(int g) {
    int ge0 = le(ZERO, g), le0 = le(g, ZERO);
    if (ge0 && le0) return 'P';
    if (ge0) return 'L';
    if (le0) return 'R';
    return 'N';
}

/* ======================================================= pawn rules */
static int W = 4, WRAP = 0, RACE = 0, EPON = 1, AWARE = 0;
/* square s = (r-1)*8 + f, r = 1..8, f = 0..7 */
static inline int SQ(int f, int r) { return (r - 1) * 8 + f; }
static inline uint64_t BB(int f, int r) { return 1ull << SQ(f, r); }
static inline int FILEOF(int s) { return s & 7; }
static inline int RANKOF(int s) { return (s >> 3) + 1; }
static uint64_t frontW[64], frontB[64], filemask[8];

static int nbf(int f, int d) {
    int g = f + d;
    if (WRAP) return ((g % W) + W) % W;
    return (g >= 0 && g < W) ? g : -1;
}
static void init_masks(void) {
    memset(frontW, 0, sizeof frontW); memset(frontB, 0, sizeof frontB);
    for (int f = 0; f < 8; f++) { filemask[f] = 0; for (int r = 1; r <= 8; r++) filemask[f] |= BB(f, r); }
    for (int f = 0; f < W; f++)
        for (int r = 1; r <= 8; r++) {
            int fs[3] = {f, nbf(f, -1), nbf(f, 1)};
            for (int i = 0; i < 3; i++) {
                int g = fs[i]; if (g < 0) continue;
                for (int s = 1; s <= 8; s++) {
                    if (s > r) frontW[SQ(f, r)] |= BB(g, s);
                    if (s < r) frontB[SQ(f, r)] |= BB(g, s);
                }
            }
        }
}

/* e.p. right: ep = 0 or 1 + target square. Target on rank 3: a white pawn just
 * went x2-x4, Black may capture onto x3 (victim on x4). Target on rank 6: Black
 * went x7-x5, White may capture onto x6 (victim x5). Stored only when an enemy
 * pawn stands beside the victim (otherwise the right can never be used, and the
 * value is the same as with no right). */
static inline int ep_holder_white(int ep) { return RANKOF(ep - 1) == 6; }
static inline int ep_victim(int ep) { int t = ep - 1; return RANKOF(t) == 3 ? SQ(FILEOF(t), 4) : SQ(FILEOF(t), 5); }

static int capturable(uint64_t wm, uint64_t bm, int ep, int white, int s) {
    if (!AWARE || !ep) return 0;
    if (ep_victim(ep) != s) return 0;
    if (ep_holder_white(ep) == white) return 0;
    int f = FILEOF(s), r = RANKOF(s);
    uint64_t theirs = white ? bm : wm;
    for (int d = -1; d <= 1; d += 2) { int g = nbf(f, d); if (g >= 0 && (theirs & BB(g, r))) return 1; }
    return 0;
}
static int passedW(uint64_t wm, uint64_t bm, int ep) {
    for (uint64_t m = wm; m; m &= m - 1) {
        int s = __builtin_ctzll(m);
        if (!(bm & frontW[s]) && !capturable(wm, bm, ep, 1, s)) return 1;
    }
    return 0;
}
static int passedB(uint64_t wm, uint64_t bm, int ep) {
    for (uint64_t m = bm; m; m &= m - 1) {
        int s = __builtin_ctzll(m);
        if (!(wm & frontB[s]) && !capturable(wm, bm, ep, 0, s)) return 1;
    }
    return 0;
}
/* cylcgt.pawns.promote_distance */
static int dist(uint64_t wm, uint64_t bm, int ep, int white) {
    int best = 1000000;
    uint64_t occ = wm | bm, mine = white ? wm : bm, theirs = white ? bm : wm;
    for (uint64_t m = mine; m; m &= m - 1) {
        int s = __builtin_ctzll(m), f = FILEOF(s), r = RANKOF(s);
        if (theirs & (white ? frontW[s] : frontB[s])) continue;
        if (capturable(wm, bm, ep, white, s)) continue;
        int front = 1;
        if (white) { for (int q = r + 1; q <= 8; q++) if (occ & BB(f, q)) front = 0; }
        else { for (int q = 1; q < r; q++) if (occ & BB(f, q)) front = 0; }
        if (!front) continue;
        int d = white ? 8 - r - (r == 2) : r - 1 - (r == 7);
        if (d < best) best = d;
    }
    return best;
}

/* ---- pawn-value memo: (wm, bm, ep) -> game id */
typedef struct { uint64_t wm, bm; int g; uint8_t ep, used; } PE;
static PE *PM; static uint64_t PMcap, PMcount;
static void pm_clear(void) { free(PM); PM = NULL; PMcap = PMcount = 0; }
static PE *pm_find(uint64_t wm, uint64_t bm, int ep) {
    uint64_t h = mix(wm ^ mix(bm ^ ((uint64_t)ep << 56))) & (PMcap - 1);
    while (PM[h].used && !(PM[h].wm == wm && PM[h].bm == bm && PM[h].ep == ep)) h = (h + 1) & (PMcap - 1);
    return &PM[h];
}
static void pm_store(uint64_t wm, uint64_t bm, int ep, int g) {
    if ((PMcount + 1) * 2 > PMcap) {
        uint64_t oc = PMcap; PE *old = PM;
        PMcap = oc ? oc * 2 : 1 << 16; PM = xcalloc(PMcap, sizeof(PE));
        for (uint64_t i = 0; i < oc; i++) if (old[i].used) *pm_find(old[i].wm, old[i].bm, old[i].ep) = old[i];
        free(old);
    }
    PE *e = pm_find(wm, bm, ep);
    e->wm = wm; e->bm = bm; e->ep = (uint8_t)ep; e->g = g; e->used = 1; PMcount++;
}

static int value(uint64_t wm, uint64_t bm, int ep);
static long race_count;

static int child_value(uint64_t wm, uint64_t bm, int ep, int moverWhite) {
    int pw = passedW(wm, bm, ep), pb = passedB(wm, bm, ep);
    if (pw && pb) {
        race_count++;
        int winnerWhite;
        if (RACE == 1) winnerWhite = moverWhite;
        else if (RACE == 2) winnerWhite = !moverWhite;
        else if (RACE == 3) winnerWhite = 1;  /* every race won by White */
        else if (RACE == 4) winnerWhite = 0;  /* every race won by Black */
        else {
            int dm = dist(wm, bm, ep, moverWhite), dop = dist(wm, bm, ep, !moverWhite);
            winnerWhite = (dop <= dm) ? !moverWhite : moverWhite;
        }
        return number((fx)(winnerWhite ? BIG : -BIG) * ONE);
    }
    return value(wm, bm, ep);
}

/* options of one side from a single-component position */
static void gen(uint64_t wm, uint64_t bm, int ep, int white, Vec *out) {
    uint64_t occ = wm | bm, mine = white ? wm : bm, theirs = white ? bm : wm;
    int d = white ? 1 : -1, start = white ? 2 : 7;
    int myep = (ep && ep_holder_white(ep) == white) ? ep : 0; /* the other side's right dies */
    for (uint64_t m = mine; m; m &= m - 1) {
        int s = __builtin_ctzll(m), f = FILEOF(s), r = RANKOF(s);
        int r1 = r + d;
        if (r1 < 1 || r1 > 8) continue;
        uint64_t rest = mine & ~(1ull << s);
        if (!(occ & BB(f, r1))) {
            uint64_t nm = rest | BB(f, r1);
            vpush(out, white ? child_value(nm, theirs, 0, 1) : child_value(theirs, nm, 0, 0));
            int r2 = r + 2 * d;
            if (r == start && r2 >= 1 && r2 <= 8 && !(occ & BB(f, r2))) {
                uint64_t nm2 = rest | BB(f, r2);
                int nep = 0;
                if (EPON)
                    for (int q = -1; q <= 1; q += 2) { int g = nbf(f, q); if (g >= 0 && (theirs & BB(g, r2))) nep = 1 + SQ(f, r1); }
                vpush(out, white ? child_value(nm2, theirs, nep, 1) : child_value(theirs, nm2, nep, 0));
            }
        }
        for (int q = -1; q <= 1; q += 2) {
            int g = nbf(f, q);
            if (g < 0) continue;
            int t = SQ(g, r1);
            if (theirs & (1ull << t)) {
                uint64_t nm = rest | (1ull << t), nt = theirs & ~(1ull << t);
                vpush(out, white ? child_value(nm, nt, 0, 1) : child_value(nt, nm, 0, 0));
            } else if (myep && (myep - 1) == t) {
                uint64_t nm = rest | (1ull << t), nt = theirs & ~(1ull << ep_victim(myep));
                vpush(out, white ? child_value(nm, nt, 0, 1) : child_value(nt, nm, 0, 0));
            }
        }
    }
}

static int comp_value(uint64_t wm, uint64_t bm, int ep) {
    if (PMcap) { PE *e = pm_find(wm, bm, ep); if (e->used) return e->g; }
    Vec L = {0}, R = {0};
    gen(wm, bm, ep, 1, &L);
    gen(wm, bm, ep, 0, &R);
    int g = make(L.a, L.n, R.a, R.n);
    free(L.a); free(R.a);
    pm_store(wm, bm, ep, g);
    return g;
}

/* split into components separated by empty files (cylcgt.pawns.components) */
static int value(uint64_t wm, uint64_t bm, int ep) {
    int pw = passedW(wm, bm, ep), pb = passedB(wm, bm, ep);
    if (pw != pb) return number((fx)(pw ? BIG : -BIG) * ONE);
    if (pw && pb) { fprintf(stderr, "race at a root position\n"); exit(4); }
    uint64_t occ = wm | bm;
    int occf = 0;
    for (int f = 0; f < W; f++) if (occ & filemask[f]) occf |= 1 << f;
    if (occf == (1 << W) - 1) return comp_value(wm, bm, ep);
    /* groups of consecutive occupied files; on a cylinder start after an empty file */
    int startf = 0;
    if (WRAP) { for (int f = 0; f < W; f++) if (!(occf & (1 << f))) { startf = (f + 1) % W; break; } }
    uint64_t gm[8]; int ng = 0, in = 0;
    for (int i = 0; i < W; i++) {
        int f = (startf + i) % W;
        if (occf & (1 << f)) { if (!in) { gm[ng++] = 0; in = 1; } gm[ng - 1] |= filemask[f]; }
        else in = 0;
    }
    if (ng == 1) return comp_value(wm, bm, ep);
    int tot = ZERO;
    for (int i = 0; i < ng; i++) {
        int cep = (ep && (gm[i] & (1ull << (ep - 1)))) ? ep : 0;
        tot = add(tot, comp_value(wm & gm[i], bm & gm[i], cep));
    }
    return tot;
}

/* ======================================================= driver */
static int parse_pos(const char *s, uint64_t *wm, uint64_t *bm) {
    *wm = *bm = 0;
    const char *wp = strstr(s, "W:"), *bp = strstr(s, "B:");
    if (!wp || !bp) return 0;
    for (const char *p = wp + 2; p < bp; p++)
        if (*p >= 'a' && *p <= 'h' && p[1] >= '1' && p[1] <= '8') { *wm |= BB(*p - 'a', p[1] - '0'); p++; }
    for (const char *p = bp + 2; *p && *p != '\t'; p++)
        if (*p >= 'a' && *p <= 'h' && p[1] >= '1' && p[1] <= '8') { *bm |= BB(*p - 'a', p[1] - '0'); p++; }
    return 1;
}
static void pos_str(char *out, uint64_t wm, uint64_t bm) {
    char *p = out;
    p += sprintf(p, "W:");
    for (int f = 0; f < 8; f++) for (int r = 1; r <= 8; r++) if (wm & BB(f, r)) p += sprintf(p, " %c%d", 'a' + f, r);
    p += sprintf(p, " / B:");
    for (int f = 0; f < 8; f++) for (int r = 1; r <= 8; r++) if (bm & BB(f, r)) p += sprintf(p, " %c%d", 'a' + f, r);
}

/* structural 128-bit hash of a canonical game (identifies values across runs).
 * Two independent 64-bit lanes. Each lane seeds with BOTH option counts and ends
 * with a final avalanche, so the state after absorbing a prefix of the options is
 * never the hash of the game made of that prefix. (A first version seeded with nL
 * only and had no finalisation; then every game {L | Y, {L | Y}} -- e.g. the
 * down-star {0 | 0, *} -- hashed to the same value. Fixed 2026-10-16.) */
typedef struct { uint64_t a, b; } H128;
static H128 *HSH; static int HSHcap;
static int cmp_h128(const void *x, const void *y) {
    const H128 *p = x, *q = y;
    if (p->a != q->a) return (p->a > q->a) - (p->a < q->a);
    return (p->b > q->b) - (p->b < q->b);
}
static inline uint64_t mix2(uint64_t x) { /* a second, different 64-bit finaliser (murmur3 fmix64) */
    x ^= x >> 33; x *= 0xff51afd7ed558ccdull; x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ull; x ^= x >> 33;
    return x;
}
static void hsh_reserve(int g) {
    if (g < HSHcap) return;
    int oc = HSHcap; HSHcap = (g + 1) * 2;
    HSH = xrealloc(HSH, sizeof(H128) * (size_t)HSHcap);
    memset(HSH + oc, 0, sizeof(H128) * (size_t)(HSHcap - oc));
}
static H128 ghash(int g) {
    hsh_reserve(g);
    if (HSH[g].a || HSH[g].b) return HSH[g];
    H128 h;
    if (N[g].isnum) {
        h.a = mix((uint64_t)N[g].num ^ 0x1234567ull);
        h.b = mix2((uint64_t)N[g].num + 0x7654321ull);
    } else {
        int nL = N[g].nL, nR = N[g].nR;
        H128 *c = xmalloc(sizeof(H128) * (size_t)(nL + nR + 1));
        for (int i = 0; i < nL; i++) c[i] = ghash(LOPT(g, i));
        for (int i = 0; i < nR; i++) c[nL + i] = ghash(ROPT(g, i));
        qsort(c, (size_t)nL, sizeof(H128), cmp_h128);
        qsort(c + nL, (size_t)nR, sizeof(H128), cmp_h128);
        uint64_t a = mix(0x9999ull + ((uint64_t)nL << 20) + (uint64_t)nR);
        uint64_t b = mix2(0x5555ull + ((uint64_t)nR << 24) + (uint64_t)nL * 7);
        for (int i = 0; i < nL; i++) { a = mix(a ^ c[i].a); b = mix2(b + c[i].b * 0x9E3779B97F4A7C15ull); }
        a = mix(a ^ 0x7777ull); b = mix2(b ^ 0x3333ull);
        for (int i = 0; i < nR; i++) { a = mix(a ^ c[nL + i].a); b = mix2(b + c[nL + i].b * 0xC2B2AE3D27D4EB4Full); }
        h.a = mix2(a + 0x632BE59BD9B4E019ull);   /* final avalanche (different finaliser) */
        h.b = mix(b ^ 0x85EBCA77C2B2AE63ull);
        free(c);
    }
    if (!h.a && !h.b) h.a = 1;
    hsh_reserve(g);
    HSH[g] = h;
    return h;
}
/* size of the game written out as a tree (saturating), to skip printing huge +-W games */
static double *TSZ; static int TSZcap;
static double tsize(int g) {
    if (g >= TSZcap) { int oc = TSZcap; TSZcap = (g + 1) * 2; TSZ = xrealloc(TSZ, sizeof(double) * (size_t)TSZcap); for (int i = oc; i < TSZcap; i++) TSZ[i] = -1; }
    if (TSZ[g] >= 0) return TSZ[g];
    double t = 1;
    if (!N[g].isnum && N[g].nim < 0) {
        for (int i = 0; i < N[g].nL && t < 1e9; i++) t += tsize(LOPT(g, i));
        for (int i = 0; i < N[g].nR && t < 1e9; i++) t += tsize(ROPT(g, i));
    }
    if (t > 1e9) t = 1e9;
    if (g >= TSZcap) { int oc = TSZcap; TSZcap = (g + 1) * 2; TSZ = xrealloc(TSZ, sizeof(double) * (size_t)TSZcap); for (int i = oc; i < TSZcap; i++) TSZ[i] = -1; }
    TSZ[g] = t;
    return t;
}

/* ---- enumeration of root positions */
static uint64_t img(uint64_t m, int refl, int rot) {
    uint64_t o = 0;
    for (; m; m &= m - 1) {
        int s = __builtin_ctzll(m), f = FILEOF(s), r = RANKOF(s);
        int g = refl ? W - 1 - f : f;
        g = (g + rot) % W;
        o |= BB(g, r);
    }
    return o;
}
static int enum_mode(int w, int wrap, int nmin, int nmax, int conn) {
    W = w; WRAP = wrap; init_masks();
    int wc[64], bc[64], nwc = 0, nbc = 0;
    for (int f = 0; f < W; f++) {
        for (int r = 2; r <= 6; r++) wc[nwc++] = SQ(f, r);
        for (int r = 3; r <= 7; r++) bc[nbc++] = SQ(f, r);
    }
    uint64_t allfiles = 0; for (int f = 0; f < W; f++) allfiles |= filemask[f];
    long count = 0;
    char buf[256];
    for (int n = nmin; n <= nmax; n++)
        for (int nw = 1; nw < n; nw++) {
            int nb = n - nw;
            int iw[16];
            for (int i = 0; i < nw; i++) iw[i] = i;
            if (nw > nwc) continue;
            for (;;) {
                uint64_t wm = 0;
                for (int i = 0; i < nw; i++) wm |= 1ull << wc[iw[i]];
                /* black candidates: squares where a black pawn is not passed */
                int zc[64], nz = 0;
                for (int i = 0; i < nbc; i++) { int s = bc[i]; if (!(wm & (1ull << s)) && (wm & frontB[s])) zc[nz++] = s; }
                if (nb <= nz) {
                    int ib[16];
                    for (int i = 0; i < nb; i++) ib[i] = i;
                    for (;;) {
                        uint64_t bm = 0;
                        for (int i = 0; i < nb; i++) bm |= 1ull << zc[ib[i]];
                        uint64_t occ = wm | bm;
                        int ok = 1;
                        if (conn) { for (int f = 0; f < W; f++) if (!(occ & filemask[f])) { ok = 0; break; } }
                        else if (!wrap) { if (!(occ & filemask[0]) || !(occ & filemask[W - 1])) ok = 0; }
                        if (ok && (passedW(wm, bm, 0) || passedB(wm, bm, 0))) ok = 0;
                        if (ok) {
                            /* symmetry: flat {id, mirror}; cylinder dihedral */
                            int nrot = wrap ? W : 1, isminimal = 1;
                            uint64_t seenw[32], seenb[32]; int ns = 0;
                            for (int refl = 0; refl < 2 && isminimal; refl++)
                                for (int rot = 0; rot < nrot; rot++) {
                                    uint64_t a = img(wm, refl, rot), b = img(bm, refl, rot);
                                    if (a < wm || (a == wm && b < bm)) { isminimal = 0; break; }
                                    int dup = 0;
                                    for (int q = 0; q < ns; q++) if (seenw[q] == a && seenb[q] == b) dup = 1;
                                    if (!dup) { seenw[ns] = a; seenb[ns] = b; ns++; }
                                }
                            if (isminimal) { pos_str(buf, wm, bm); printf("%s\t%d\t%d\t%d\n", buf, W, wrap, ns); count++; }
                        }
                        int i = nb - 1;
                        while (i >= 0 && ib[i] == nz - nb + i) i--;
                        if (i < 0) break;
                        ib[i]++;
                        for (int j = i + 1; j < nb; j++) ib[j] = ib[j - 1] + 1;
                    }
                }
                int i = nw - 1;
                while (i >= 0 && iw[i] == nwc - nw + i) i--;
                if (i < 0) break;
                iw[i]++;
                for (int j = i + 1; j < nw; j++) iw[j] = iw[j - 1] + 1;
            }
        }
    (void)allfiles;
    fprintf(stderr, "enumerated %ld positions (W=%d wrap=%d n=%d..%d conn=%d)\n", count, w, wrap, nmin, nmax, conn);
    return 0;
}

static int parse_race(const char *r) {
    return !strcmp(r, "count") ? 0 : !strcmp(r, "mover") ? 1 : !strcmp(r, "opponent") ? 2
         : !strcmp(r, "white") ? 3 : !strcmp(r, "black") ? 4 : -1;
}
static const char *RNAME[5] = {"count", "mover", "opponent", "white", "black"};

int main(int argc, char **argv) {
    int printlimit = 400;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--race") && i + 1 < argc) {
            RACE = parse_race(argv[++i]);
            if (RACE < 0) { fprintf(stderr, "bad race rule\n"); return 1; }
        } else if (!strcmp(argv[i], "--ep") && i + 1 < argc) EPON = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--aware") && i + 1 < argc) AWARE = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--printlimit") && i + 1 < argc) printlimit = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--enum") && i + 5 < argc)
            return enum_mode(atoi(argv[i + 1]), atoi(argv[i + 2]), atoi(argv[i + 3]), atoi(argv[i + 4]), atoi(argv[i + 5]));
    }
    HC = NULL; HCcap = 0; hc_grow();
    int none[1];
    ZERO = intern(none, 0, none, 0);
    { int z = ZERO; STAR = make(&z, 1, &z, 1); }
    { int z = ZERO, s = STAR; UP = make(&z, 1, &s, 1); DOWN = make(&s, 1, &z, 1);
      int zs[2] = {ZERO, STAR}; UPSTAR = make(zs, 2, &z, 1); DOWNSTAR = neg(UPSTAR);
      DUP = add(UP, UP); DDOWN = neg(DUP); DUPSTAR = add(DUP, STAR); DDOWNSTAR = neg(DUPSTAR);
      TUP = add(DUP, UP); TDOWN = neg(TUP); }
    int dRACE = RACE, dEPON = EPON, dAWARE = AWARE;
    int cur[5] = {-1, -1, -1, -1, -1};
    static char line[4096];
    int *roots = NULL; int nroots = 0, rcap = 0;
    while (fgets(line, sizeof line, stdin)) {
        if (line[0] == '#' || line[0] == '\n') continue;
        line[strcspn(line, "\n")] = 0;
        /* columns: position, width, wrap [, race, ep, aware] */
        char *col[8]; int nc = 0;
        char *p = line;
        col[nc++] = p;
        while (nc < 8 && (p = strchr(p, '\t'))) { *p++ = 0; col[nc++] = p; }
        if (nc < 2) continue;
        int w = atoi(col[1]), wrap = nc > 2 ? atoi(col[2]) : 0;
        int race = dRACE, ep = dEPON, aware = dAWARE;
        if (nc > 5) { race = parse_race(col[3]); ep = atoi(col[4]); aware = atoi(col[5]); }
        if (race < 0 || w < 1 || w > 8) { fprintf(stderr, "bad line\n"); return 1; }
        if (w != cur[0] || wrap != cur[1] || race != cur[2] || ep != cur[3] || aware != cur[4]) {
            W = w; WRAP = wrap; RACE = race; EPON = ep; AWARE = aware;
            init_masks(); pm_clear();
            cur[0] = w; cur[1] = wrap; cur[2] = race; cur[3] = ep; cur[4] = aware;
        }
        uint64_t wm, bm;
        if (!parse_pos(col[0], &wm, &bm)) continue;
        if (passedW(wm, bm, 0) || passedB(wm, bm, 0)) {
            /* a passer at the root: value is +-BIG or a race; report and skip */
            printf("%s\t%d\t%d\t%s\t%d\t%d\t-1\tX\n", col[0], W, WRAP, RNAME[RACE], EPON, AWARE);
            continue;
        }
        int g = value(wm, bm, 0);
        printf("%s\t%d\t%d\t%s\t%d\t%d\t%d\t%c\n", col[0], W, WRAP, RNAME[RACE], EPON, AWARE, g, outcome(g));
        if (nroots == rcap) { rcap = rcap ? rcap * 2 : 1024; roots = xrealloc(roots, sizeof(int) * (size_t)rcap); }
        roots[nroots++] = g;
    }
    /* distinct root values: gid, big, structural hash, show, key ("-" when huge) */
    char *seen = xcalloc((size_t)NN + 1, 1);
    for (int i = 0; i < nroots; i++) {
        int g = roots[i];
        if (seen[g]) continue;
        seen[g] = 1;
        int big = has_big(g);
        int pr = !big || tsize(g) <= printlimit;
        H128 hh = ghash(g);
        printf("#V\t%d\t%d\t%016llx%016llx\t%s\t%s\n", g, big, (unsigned long long)hh.a, (unsigned long long)hh.b,
               pr ? show(g) : "-", pr ? key(g) : "-");
    }
    fprintf(stderr, "games %d interned %llu le-memo %llu add-memo %llu pawn-memo(last setting) %llu\n", NN,
            (unsigned long long)HCcount, (unsigned long long)LMcount, (unsigned long long)AMcount, (unsigned long long)PMcount);
    return 0;
}
