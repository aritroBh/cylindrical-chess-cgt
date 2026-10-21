/* Independent verifier for claim C3 (dawson ring rule). Written from scratch by the
 * C3 verifier; it shares no code with dawson/pawnboard.py or cylcgt/.
 *
 * Dawson's chess on a 3 x n board (ranks 0,1,2; White pawns start on rank 0 and move
 * up, Black pawns start on rank 2 and move down; rank 1 empty).  A pawn moves one square
 * straight forward onto an empty square, or one square diagonally forward onto a square
 * holding an enemy pawn (capture).  Captures are compulsory.  On the cylinder files 0 and
 * n-1 are adjacent.  A pawn on its last rank has no move (we count whether this happens).
 *
 * Mode "solve n wrap": memoised minimax from the start position, side to move White and
 * (separately) Black; prints normal-play and misere outcome for the side to move.
 *
 * Mode "lemma nmin nmax": for every ring n in [nmin, nmax], for both colours and every
 * first push, follows ALL forced-capture continuations (while the side to move has a
 * capture) to quiet positions and checks that each quiet endpoint has: the opponent of the
 * first mover to move; exactly n-3 untouched files forming one contiguous arc; the other
 * three files f-1, f, f+1 with f-1 and f+1 empty and file f holding exactly one W and one B
 * pawn on adjacent ranks, W directly below B (blocked); no capture available to either
 * side; every legal push of either side starts from an untouched file.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef unsigned __int128 u128;
static int N, WRAP;
static long promo_count = 0;

#define GET(k, f, r) ((int)(((k) >> (2 * (3 * (f) + (r)))) & 3))
static inline u128 SET(u128 k, int f, int r, int v) {
    int sh = 2 * (3 * f + r);
    k &= ~(((u128)3) << sh);
    k |= ((u128)v) << sh;
    return k;
}
#define SIDEBIT (((u128)1) << 127)

static int nbrs(int f, int *out) {
    int c = 0;
    for (int d = -1; d <= 1; d += 2) {
        int g = f + d;
        if (WRAP) g = (g + N) % N;
        if (g < 0 || g >= N) continue;
        if (c == 1 && out[0] == g) continue;
        if (g == f) continue;
        out[c++] = g;
    }
    return c;
}

/* generate successors of k for side s; returns count, sets *cap if captures */
static int gen(u128 k, int s, u128 *out, int *cap) {
    int me = s ? 2 : 1, them = s ? 1 : 2, dir = s ? -1 : 1;
    int nc = 0, np = 0;
    u128 caps[256], pushes[256];
    for (int f = 0; f < N; f++)
        for (int r = 0; r < 3; r++) {
            if (GET(k, f, r) != me) continue;
            int r1 = r + dir;
            if (r1 < 0 || r1 > 2) continue;
            int nb[2];
            int c = nbrs(f, nb);
            for (int i = 0; i < c; i++)
                if (GET(k, nb[i], r1) == them) {
                    u128 q = SET(SET(k, f, r, 0), nb[i], r1, me);
                    caps[nc++] = q;
                }
            if (GET(k, f, r1) == 0) pushes[np++] = SET(SET(k, f, r, 0), f, r1, me);
        }
    *cap = nc > 0;
    u128 *src = nc ? caps : pushes;
    int m = nc ? nc : np, o = 0;
    for (int i = 0; i < m; i++) {
        int dup = 0;
        for (int j = 0; j < o; j++) if (out[j] == src[i]) { dup = 1; break; }
        if (!dup) out[o++] = src[i];
    }
    return o;
}

/* hash table */
static u128 *HK;
static uint8_t *HV;
static uint64_t HMASK;
static long nstored = 0;

static uint64_t hsh(u128 k) {
    uint64_t a = (uint64_t)k, b = (uint64_t)(k >> 64);
    uint64_t h = a * 0x9E3779B97F4A7C15ULL ^ (b + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL;
    h ^= h >> 31;
    return h;
}

static int lookup(u128 k, uint64_t *slot) {
    uint64_t i = hsh(k) & HMASK;
    while (HV[i]) {
        if (HK[i] == k) { *slot = i; return HV[i] - 1; }
        i = (i + 1) & HMASK;
    }
    *slot = i;
    return -1;
}

/* returns bit0 = normal-play win for side to move, bit1 = misere win for side to move */
static int solve(u128 k, int s) {
    u128 key = k | (s ? SIDEBIT : 0);
    uint64_t slot;
    int v = lookup(key, &slot);
    if (v >= 0) return v;
    u128 succ[256];
    int cap;
    int m = gen(k, s, succ, &cap);
    int res;
    if (m == 0) res = 2; /* normal: loss; misere: win */
    else {
        int nw = 0, mw = 0;
        for (int i = 0; i < m; i++) {
            /* promotion check: White pawn on rank 2 or Black pawn on rank 0 */
            for (int f = 0; f < N; f++)
                if (GET(succ[i], f, 2) == 1 || GET(succ[i], f, 0) == 2) { promo_count++; break; }
            int c = solve(succ[i], 1 - s);
            if (!(c & 1)) nw = 1;
            if (!(c & 2)) mw = 1;
        }
        res = nw | (mw << 1);
    }
    lookup(key, &slot); /* table may not have moved (no rehash), but recompute slot */
    if (nstored * 10 > (long)(HMASK + 1) * 7) { fprintf(stderr, "table too full\n"); exit(2); }
    HK[slot] = key; HV[slot] = (uint8_t)(res + 1); nstored++;
    return res;
}

static u128 startpos(void) {
    u128 k = 0;
    for (int f = 0; f < N; f++) { k = SET(k, f, 0, 1); k = SET(k, f, 2, 2); }
    return k;
}

/* ---- lemma mode with plain arrays (n up to 400) ---- */
#define MAXN 400
typedef struct { uint8_t q[MAXN][3]; } A;

static int agen(const A *p, int s, A *out, int maxout, int *cap) {
    int me = s ? 2 : 1, them = s ? 1 : 2, dir = s ? -1 : 1;
    int nc = 0;
    A *tmp = malloc(sizeof(A) * 64);
    int np = 0;
    A *tp = malloc(sizeof(A) * 1024);
    for (int f = 0; f < N; f++)
        for (int r = 0; r < 3; r++) {
            if (p->q[f][r] != me) continue;
            int r1 = r + dir;
            if (r1 < 0 || r1 > 2) continue;
            int nb[2]; int c = nbrs(f, nb);
            for (int i = 0; i < c; i++)
                if (p->q[nb[i]][r1] == them) {
                    if (nc >= 64) { fprintf(stderr, "overflow\n"); exit(3); }
                    tmp[nc] = *p; tmp[nc].q[f][r] = 0; tmp[nc].q[nb[i]][r1] = me; nc++;
                }
            if (p->q[f][r1] == 0) {
                if (np >= 1024) { fprintf(stderr, "overflow p\n"); exit(3); }
                tp[np] = *p; tp[np].q[f][r] = 0; tp[np].q[f][r1] = me; np++;
            }
        }
    *cap = nc > 0;
    int m = nc ? nc : np;
    A *src = nc ? tmp : tp;
    if (m > maxout) { fprintf(stderr, "maxout\n"); exit(3); }
    for (int i = 0; i < m; i++) out[i] = src[i];
    free(tmp); free(tp);
    return m;
}

static long lemma_bad = 0, lemma_endpoints = 0;

static int is_full(const A *p, int f) { return p->q[f][0] == 1 && p->q[f][1] == 0 && p->q[f][2] == 2; }
static int is_empty(const A *p, int f) { return !p->q[f][0] && !p->q[f][1] && !p->q[f][2]; }

static void check_endpoint(const A *p, int stm, int first_side, int f0) {
    lemma_endpoints++;
    int bad = 0;
    if (stm != 1 - first_side) bad |= 1;
    int fm = (f0 - 1 + N) % N, fp = (f0 + 1) % N;
    if (!is_empty(p, fm) || !is_empty(p, fp)) bad |= 2;
    /* file f0: exactly W directly below B */
    int w = -1, b = -1, cnt = 0;
    for (int r = 0; r < 3; r++) { if (p->q[f0][r] == 1) { w = r; cnt++; } if (p->q[f0][r] == 2) { b = r; cnt++; } }
    if (cnt != 2 || w < 0 || b < 0 || b != w + 1) bad |= 4;
    /* all other files full */
    int nfull = 0;
    for (int f = 0; f < N; f++) {
        if (f == f0 || f == fm || f == fp) continue;
        if (!is_full(p, f)) bad |= 8; else nfull++;
    }
    if (nfull != N - 3) bad |= 16;
    /* no captures for either side; every push starts from a full file */
    for (int s = 0; s < 2; s++) {
        A *o = malloc(sizeof(A) * 1024);
        int cap; int m = agen(p, s, o, 1024, &cap);
        if (cap) bad |= 32;
        for (int i = 0; i < m; i++)
            for (int f = 0; f < N; f++)
                if (memcmp(o[i].q[f], p->q[f], 3) && !is_full(p, f)) bad |= 64;
        free(o);
    }
    if (bad) { lemma_bad++; if (lemma_bad < 5) fprintf(stderr, "BAD n=%d side=%d f=%d code=%d\n", N, first_side, f0, bad); }
}

static void follow(const A *p, int stm, int first_side, int f0, int depth, int *maxdepth) {
    A *o = malloc(sizeof(A) * 1024);
    int cap;
    int m = agen(p, stm, o, 1024, &cap);
    if (!cap) { if (depth > *maxdepth) *maxdepth = depth; check_endpoint(p, stm, first_side, f0); free(o); return; }
    for (int i = 0; i < m; i++) follow(&o[i], 1 - stm, first_side, f0, depth + 1, maxdepth);
    free(o);
}

int main(int argc, char **argv) {
    if (argc >= 4 && !strcmp(argv[1], "solve")) {
        N = atoi(argv[2]); WRAP = atoi(argv[3]);
        int lg = argc >= 5 ? atoi(argv[4]) : 22;
        if (N > 21) { fprintf(stderr, "n <= 21\n"); return 1; }
        HMASK = (1ULL << lg) - 1;
        HK = calloc(HMASK + 1, sizeof(u128)); HV = calloc(HMASK + 1, 1);
        if (!HK || !HV) { fprintf(stderr, "oom\n"); return 1; }
        u128 st = startpos();
        int a = solve(st, 0), b = solve(st, 1);
        printf("%s n=%d: normal W-first %s B-first %s | misere W-first %s B-first %s | positions %ld | promotions %ld\n",
               WRAP ? "cyl" : "flat", N, (a & 1) ? "win" : "loss", (b & 1) ? "win" : "loss",
               (a & 2) ? "win" : "loss", (b & 2) ? "win" : "loss", nstored, promo_count);
        return 0;
    }
    if (argc >= 4 && !strcmp(argv[1], "lemma")) {
        int lo = atoi(argv[2]), hi = atoi(argv[3]);
        WRAP = 1;
        for (N = lo; N <= hi; N++) {
            long b0 = lemma_bad, e0 = lemma_endpoints;
            int maxdepth = 0;
            A *st = calloc(1, sizeof(A));
            for (int f = 0; f < N; f++) { st->q[f][0] = 1; st->q[f][2] = 2; }
            for (int s = 0; s < 2; s++) {
                A *o = malloc(sizeof(A) * 1024);
                int cap; int m = agen(st, s, o, 1024, &cap);
                if (cap || m != N) { fprintf(stderr, "start has %d moves cap=%d\n", m, cap); lemma_bad++; }
                for (int i = 0; i < m; i++) {
                    int f0 = -1;
                    for (int f = 0; f < N; f++) if (memcmp(o[i].q[f], st->q[f], 3)) f0 = f;
                    follow(&o[i], 1 - s, s, f0, 1, &maxdepth);
                }
                free(o);
            }
            printf("ring n=%d: forced-line endpoints %ld, bad %ld, max plies in a first macro-move %d\n",
                   N, lemma_endpoints - e0, lemma_bad - b0, maxdepth);
            free(st);
        }
        printf("TOTAL bad %ld over %ld endpoints\n", lemma_bad, lemma_endpoints);
        return 0;
    }
    fprintf(stderr, "usage: solve n wrap [log2size] | lemma nmin nmax\n");
    return 1;
}
