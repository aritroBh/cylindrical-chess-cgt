/*
 * t32_search.c -- forward DFS for pawn-only histories (T32).
 *
 * Independent C port of research/five_file_legal/pawnhist.py (find_history, prune=True).
 * Same conventions: pawn-only game, no promotion, en passant included, exact counts
 * (the target is reached exactly), pruning by matching cost (rank advance >= file shift)
 * and by the budget "cost <= enemy pawns still to be removed".
 *
 * Board bit index = (rank-1)*8 + file, files 0..7 = a..h.
 * A state is (W, B, last); last = 0 (none), 1+f (last move: black double step to file f),
 * 9+f (last move: white double step to file f).  The visited table keys on (W,B,last).
 *
 * Usage:
 *   t32_search LOG2_TABLE NODE_CAP [W0_hex B0_hex]
 *     stdin : one target per line, "TW TB" as decimal unsigned 64-bit masks
 *     default start = standard 8-pawn start; the optional hex pair overrides it.
 *   stdout: per target
 *     RESULT FOUND nodes N moves M   then M lines "MV kind side f r tf tr"
 *     RESULT EXHAUSTED nodes N       (proof of impossibility under the conventions)
 *     RESULT CAP nodes N             (undecided)
 *
 * Build: cc -O2 -o t32_search t32_search.c
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef uint64_t u64;
#define INF 1000000000
#define EMPTY_KEY (~(u64)0)

typedef struct {
    unsigned char kind; /* 0 push, 1 double, 2 capture, 3 ep */
    unsigned char side; /* 0 White, 1 Black */
    unsigned char f, r, tf, tr;
} Mv;

static u64 TW, TB;               /* current target masks */
static int NWt, NBt;             /* target pawn counts */
static int TWf[16], TWr[16], TBf[16], TBr[16];
static u64 *T1, *T2;             /* visited table: key1 = W | last<<56, key2 = B */
static u64 TMASK, TCAP, TCOUNT;
static long long NODES, NODECAP;
static int CAPPED;
static int FOUND_DEPTH;
static Mv PATH[512];
static u64 START_W, START_B;
static int ORDERED = 0;          /* 1: try children in order of the matching-cost score */

static inline u64 bit(int f, int r) { return 1ULL << ((r - 1) * 8 + f); }

static int ins(u64 k1, u64 k2) {
    u64 h = (k1 * 0x9E3779B97F4A7C15ULL) ^ (k2 * 0xC2B2AE3D27D4EB4FULL);
    h ^= h >> 31;
    h &= TMASK;
    for (;;) {
        if (T1[h] == EMPTY_KEY) {
            if (TCOUNT >= TCAP) { CAPPED = 1; return 0; }
            T1[h] = k1;
            T2[h] = k2;
            TCOUNT++;
            return 1;
        }
        if (T1[h] == k1 && T2[h] == k2) return 0;
        h = (h + 1) & TMASK;
    }
}

static void unpack(u64 m, int *f, int *r, int *n) {
    int c = 0;
    for (int i = 0; i < 64; i++)
        if ((m >> i) & 1ULL) { f[c] = i % 8; r[c] = i / 8 + 1; c++; }
    *n = c;
}

/* min total file shift over injective matchings of targets to current pawns;
   side 0 = White (advance s-r), side 1 = Black (advance r-s); INF if none. */
static int match_cost(const int *cf, const int *cr, int nc,
                      const int *tf, const int *tr, int nt, int side) {
    static int dp[256], nd[256];
    int S = 1 << nc;
    for (int m = 0; m < S; m++) dp[m] = INF;
    dp[0] = 0;
    for (int t = 0; t < nt; t++) {
        for (int m = 0; m < S; m++) nd[m] = INF;
        for (int m = 0; m < S; m++) {
            if (dp[m] >= INF) continue;
            for (int j = 0; j < nc; j++) {
                if ((m >> j) & 1) continue;
                int adv = (side == 0) ? (tr[t] - cr[j]) : (cr[j] - tr[t]);
                int d = abs(tf[t] - cf[j]);
                if (adv < d) continue;
                int nm = m | (1 << j);
                int c = dp[m] + d;
                if (c < nd[nm]) nd[nm] = c;
            }
        }
        memcpy(dp, nd, sizeof(int) * S);
    }
    int best = INF;
    for (int m = 0; m < S; m++) if (dp[m] < best) best = dp[m];
    return best;
}

/* returns 1 if the state passes the prunes; *cost = min file-shift cost of White + Black
   (a heuristic score: lower means closer to the target, used only in ordered mode) */
static int feas_cost(u64 W, u64 B, int *cost) {
    int cwf[16], cwr[16], cbf[16], cbr[16], ncw, ncb;
    unpack(W, cwf, cwr, &ncw);
    unpack(B, cbf, cbr, &ncb);
    if (ncw < NWt || ncb < NBt) return 0;
    /* a White pawn on rank 7 can never move (promotion is excluded) and can never be
       captured (no Black pawn can stand on rank 8), so it must already be on a target
       square; symmetrically a Black pawn on rank 2 must already be on a target square. */
    for (int j = 0; j < ncw; j++)
        if (cwr[j] == 7 && !((TW >> ((7 - 1) * 8 + cwf[j])) & 1ULL)) return 0;
    for (int j = 0; j < ncb; j++)
        if (cbr[j] == 2 && !((TB >> ((2 - 1) * 8 + cbf[j])) & 1ULL)) return 0;
    int cw = match_cost(cwf, cwr, ncw, TWf, TWr, NWt, 0);
    if (cw >= INF || cw > ncb - NBt) return 0;
    int cb = match_cost(cbf, cbr, ncb, TBf, TBr, NBt, 1);
    if (cb >= INF || cb > ncw - NWt) return 0;
    *cost = cw + cb;
    return 1;
}

static int feasible(u64 W, u64 B) {
    int c;
    return feas_cost(W, B, &c);
}

static int gen(u64 W, u64 B, int last, Mv *out) {
    u64 occ = W | B;
    int n = 0;
    for (int f = 0; f < 8; f++) {
        for (int r = 2; r <= 7; r++) {           /* White pawns on ranks 2..7 */
            if (!(W & bit(f, r))) continue;
            if (r + 1 <= 7 && !(occ & bit(f, r + 1)))
                out[n++] = (Mv){0, 0, f, r, f, r + 1};
            if (r == 2 && !(occ & bit(f, 3)) && !(occ & bit(f, 4)))
                out[n++] = (Mv){1, 0, f, 2, f, 4};
            if (r + 1 <= 7) {
                for (int d = -1; d <= 1; d += 2) {
                    int g = f + d;
                    if (g >= 0 && g <= 7 && (B & bit(g, r + 1)))
                        out[n++] = (Mv){2, 0, f, r, g, r + 1};
                }
            }
            if (r == 5 && last >= 1 && last <= 8) {
                int fb = last - 1;
                if (abs(fb - f) == 1) out[n++] = (Mv){3, 0, f, 5, fb, 6};
            }
        }
        for (int r = 3; r <= 7; r++) {           /* Black pawns on ranks 3..7 can move */
            if (!(B & bit(f, r))) continue;
            if (r - 1 >= 2 && !(occ & bit(f, r - 1)))
                out[n++] = (Mv){0, 1, f, r, f, r - 1};
            if (r == 7 && !(occ & bit(f, 6)) && !(occ & bit(f, 5)))
                out[n++] = (Mv){1, 1, f, 7, f, 5};
            if (r - 1 >= 2) {
                for (int d = -1; d <= 1; d += 2) {
                    int g = f + d;
                    if (g >= 0 && g <= 7 && (W & bit(g, r - 1)))
                        out[n++] = (Mv){2, 1, f, r, g, r - 1};
                }
            }
            if (r == 4 && last >= 9 && last <= 16) {
                int fw = last - 9;
                if (abs(fw - f) == 1) out[n++] = (Mv){3, 1, f, 4, fw, 3};
            }
        }
    }
    return n;
}

static void apply_mv(u64 *W, u64 *B, int *last, Mv m) {
    u64 from = bit(m.f, m.r), to = bit(m.tf, m.tr);
    if (m.side == 0) {
        *W = (*W & ~from) | to;
        if (m.kind == 2) *B &= ~to;
        else if (m.kind == 3) *B &= ~bit(m.tf, m.r);
        *last = (m.kind == 1) ? 9 + m.f : 0;
    } else {
        *B = (*B & ~from) | to;
        if (m.kind == 2) *W &= ~to;
        else if (m.kind == 3) *W &= ~bit(m.tf, m.r);
        *last = (m.kind == 1) ? 1 + m.f : 0;
    }
}

static int dfs(u64 W, u64 B, int last, int depth) {
    if (W == TW && B == TB) { FOUND_DEPTH = depth; return 1; }
    /* prune first: infeasible states never reach the target, so they are not stored */
    if (!feasible(W, B)) return 0;
    if (!ins(W | ((u64)last << 56), B)) return 0;
    NODES++;
    if (NODES > NODECAP) { CAPPED = 1; return 0; }
    /* children that pass the prunes; in ORDERED mode try the lowest score first.
       The search stays exhaustive either way, so EXHAUSTED is still a proof. */
    typedef struct { Mv mv; u64 W2, B2; int l2, score; } Cand;
    Mv mv[96];
    int n = gen(W, B, last, mv);
    Cand cand[96];
    int k = 0;
    for (int i = 0; i < n; i++) {
        u64 W2 = W, B2 = B;
        int l2 = last, sc = 0;
        apply_mv(&W2, &B2, &l2, mv[i]);
        if (!feas_cost(W2, B2, &sc)) continue;
        cand[k].mv = mv[i];
        cand[k].W2 = W2;
        cand[k].B2 = B2;
        cand[k].l2 = l2;
        cand[k].score = sc;
        k++;
    }
    if (ORDERED) {
        for (int i = 1; i < k; i++) {
            Cand t = cand[i];
            int j = i - 1;
            while (j >= 0 && cand[j].score > t.score) { cand[j + 1] = cand[j]; j--; }
            cand[j + 1] = t;
        }
    }
    for (int i = 0; i < k; i++) {
        PATH[depth] = cand[i].mv;
        if (dfs(cand[i].W2, cand[i].B2, cand[i].l2, depth + 1)) return 1;
        if (CAPPED) return 0;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s LOG2_TABLE NODE_CAP [W0_hex B0_hex]\n", argv[0]); return 2; }
    int lg = atoi(argv[1]);
    NODECAP = atoll(argv[2]);
    START_W = 0; START_B = 0;
    for (int f = 0; f < 8; f++) { START_W |= bit(f, 2); START_B |= bit(f, 7); }
    if (argc >= 5) { START_W = strtoull(argv[3], NULL, 16); START_B = strtoull(argv[4], NULL, 16); }
    if (argc >= 6 && strcmp(argv[5], "ordered") == 0) ORDERED = 1;
    u64 size = 1ULL << lg;
    TMASK = size - 1;
    TCAP = (size / 4) * 3;
    T1 = malloc(size * sizeof(u64));
    T2 = malloc(size * sizeof(u64));
    if (!T1 || !T2) { fprintf(stderr, "out of memory\n"); return 3; }

    char line[256];
    while (fgets(line, sizeof line, stdin)) {
        unsigned long long tw, tb;
        if (sscanf(line, "%llu %llu", &tw, &tb) != 2) continue;
        TW = tw; TB = tb;
        int n;
        unpack(TW, TWf, TWr, &n); NWt = n;
        unpack(TB, TBf, TBr, &n); NBt = n;
        for (u64 i = 0; i < size; i++) T1[i] = EMPTY_KEY;
        TCOUNT = 0; NODES = 0; CAPPED = 0; FOUND_DEPTH = -1;
        static const char *kname[4] = {"push", "double", "capture", "ep"};
        int found = dfs(START_W, START_B, 0, 0);
        if (found) {
            printf("RESULT FOUND nodes %lld moves %d\n", NODES, FOUND_DEPTH);
            for (int i = 0; i < FOUND_DEPTH; i++) {
                Mv m = PATH[i];
                printf("MV %s %s %d %d %d %d\n", kname[m.kind], m.side ? "B" : "W",
                       m.f, m.r, m.tf, m.tr);
            }
        } else if (CAPPED) {
            printf("RESULT CAP nodes %lld\n", NODES);
        } else {
            printf("RESULT EXHAUSTED nodes %lld\n", NODES);
        }
        fflush(stdout);
    }
    return 0;
}
