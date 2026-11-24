/* variants.c -- Dawson's chess on new surfaces (Mobius strip, 2-row ring, torus) and on
 * wider boards (4 x n, 5 x n), solved directly from the pawn rules.
 *
 * Independent implementation (variants.py is a second one).
 *
 * Rules implemented (Dawson's chess):
 *   - a pawn on (f,r) moves one square forward (rank r+d) to an empty square, or
 *     captures an enemy pawn one square diagonally forward;
 *   - captures are compulsory: if the side to move has any capture it must capture;
 *   - a pawn with no forward square (on the last rank) has no moves (promotion is
 *     modelled as an inert pawn, as in dawson/pawnboard.py);
 *   - no double step (the boards are too small), so no en passant.
 *
 * Surfaces:
 *   FLAT     n x R board, files do not wrap.
 *   CYL      n x R board, files wrap (a and h glued).
 *   TORUS    n x R board, files wrap AND ranks wrap.
 *   MOBIUS_M Mobius, convention M: crossing the seam reverses the direction of the
 *             crossing pawn; the pawn steps to rank r+d and the direction flips
 *             afterwards ("a pawn crossing the seam becomes the other colour's
 *             direction").
 *   MOBIUS_T Mobius, convention T: the board is the quotient of the rectangle with
 *             (0,r) identified with (n-1,R-1-r); each pawn carries a frame bit, so
 *             the seam target row is R-2-r for a White pawn in frame 0.
 *
 * Output per configuration:
 *   surface files ranks  normW normB  misW misB  positions
 * where normW = 1 iff the side to move (White) wins in normal play, misW likewise
 * in misere play (the player with no move wins).
 *
 * Build: cc -O2 -o research/dawson_variants/variants research/dawson_variants/variants.c
 * Run:   research/dawson_variants/variants flat 4 5
 *        research/dawson_variants/variants   (reads configs on stdin)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXF 64
#define MAXR 8
#define MAXPOS (MAXF * 4 + 1)
#define MAXSUCC (MAXF * MAXR * 2)

enum { S_FLAT = 0, S_CYL = 1, S_TORUS = 2, S_MOBIUS_M = 3, S_MOBIUS_T = 4 };

static int F, R, S;
static int NBYTES;
static int MOB;

static int nbr_files(int f, int *out)
{
    int k = 0;
    if (f > 0) out[k++] = f - 1;
    else if (S != S_FLAT) out[k++] = F - 1;
    if (f < F - 1) out[k++] = f + 1;
    else if (S != S_FLAT) out[k++] = 0;
    if (k == 2 && out[0] == out[1]) k = 1;
    return k;
}

static int seam_cross(int f, int g)
{
    if (!MOB) return 0;
    return (f == 0 && g == F - 1) || (f == F - 1 && g == 0);
}

static int bit_set(uint8_t m, int r) { return (m >> r) & 1; }

/* per-file masks: 0 = W up, 1 = W down, 2 = B up, 3 = B down */
#define PWUP(f) pos[4 * (f) + 0]
#define PWDN(f) pos[4 * (f) + 1]
#define PBUP(f) pos[4 * (f) + 2]
#define PBDN(f) pos[4 * (f) + 3]
#define WUP(f) dst[4 * (f) + 0]
#define WDN(f) dst[4 * (f) + 1]
#define BUP(f) dst[4 * (f) + 2]
#define BDN(f) dst[4 * (f) + 3]

/* Write the successor obtained by moving the pawn of `side` at (f,r) to (g,rr),
 * with new direction nd (+1 up / -1 down), capturing whatever is on (g,rr). */
static void make_move(const uint8_t *pos, int side, int f, int r, int g, int rr,
                      int nd, uint8_t *dst)
{
    memcpy(dst, pos, NBYTES);
    if (side == 0) { WUP(f) &= (uint8_t)~(1u << r); WDN(f) &= (uint8_t)~(1u << r); }
    else { BUP(f) &= (uint8_t)~(1u << r); BDN(f) &= (uint8_t)~(1u << r); }
    /* remove any piece on the target square */
    WUP(g) &= (uint8_t)~(1u << rr); WDN(g) &= (uint8_t)~(1u << rr);
    BUP(g) &= (uint8_t)~(1u << rr); BDN(g) &= (uint8_t)~(1u << rr);
    if (side == 0) { if (nd == +1) WUP(g) |= (uint8_t)(1u << rr); else WDN(g) |= (uint8_t)(1u << rr); }
    else { if (nd == +1) BUP(g) |= (uint8_t)(1u << rr); else BDN(g) |= (uint8_t)(1u << rr); }
    dst[NBYTES - 1] = (uint8_t)(1 - side);
}

static int gen_moves(const uint8_t *pos, int side, uint8_t *buf, uint8_t *pbuf, int *has_cap)
{
    int ncap = 0, npush = 0;
    int nbr[2];
    *has_cap = 0;
    for (int f = 0; f < F; f++) {
        for (int r = 0; r < R; r++) {
            int d, localdir;
            if (side == 0) {
                if (bit_set(PWUP(f), r)) { d = +1; localdir = +1; }
                else if (bit_set(PWDN(f), r)) { d = -1; localdir = +1; }
                else continue;
            } else {
                if (bit_set(PBDN(f), r)) { d = -1; localdir = -1; }
                else if (bit_set(PBUP(f), r)) { d = +1; localdir = -1; }
                else continue;
            }
            int frame = 0;
            if (MOB && S == S_MOBIUS_T)
                frame = (side == 0) ? (d == +1 ? 0 : 1) : (d == -1 ? 0 : 1);

            /* --- straight push: same file, no seam crossing --- */
            {
                int rr, nd;
                if (MOB && S == S_MOBIUS_T) {
                    int lam = (frame == 0) ? r : (R - 1 - r);
                    int lam2 = lam + localdir;
                    if (lam2 < 0 || lam2 >= R) rr = -1;
                    else rr = (frame == 0) ? lam2 : (R - 1 - lam2);
                    if (rr >= 0)
                        nd = (side == 0) ? (frame == 0 ? +1 : -1) : (frame == 0 ? -1 : +1);
                } else {
                    rr = r + d;
                    if (S == S_TORUS) rr = ((rr % R) + R) % R;
                    else if (rr < 0 || rr >= R) rr = -1;
                    nd = d;
                }
                if (rr >= 0) {
                    /* a push is legal only onto a completely empty square */
                    int occ = bit_set(PWUP(f), rr) || bit_set(PWDN(f), rr) ||
                              bit_set(PBUP(f), rr) || bit_set(PBDN(f), rr);
                    if (!occ) {
                        make_move(pos, side, f, r, f, rr, nd, pbuf + (size_t)npush * NBYTES);
                        npush++;
                    }
                }
            }

            /* --- diagonal captures: adjacent files --- */
            int nf = nbr_files(f, nbr);
            for (int i = 0; i < nf; i++) {
                int g = nbr[i];
                int cross = seam_cross(f, g);
                int rr, nd;
                if (MOB && S == S_MOBIUS_T) {
                    int lam = (frame == 0) ? r : (R - 1 - r);
                    int lam2 = lam + localdir;
                    if (lam2 < 0 || lam2 >= R) continue;
                    int nframe = frame ^ (cross ? 1 : 0);
                    rr = (nframe == 0) ? lam2 : (R - 1 - lam2);
                    nd = (side == 0) ? (nframe == 0 ? +1 : -1) : (nframe == 0 ? -1 : +1);
                } else {
                    rr = r + d;
                    if (S == S_TORUS) rr = ((rr % R) + R) % R;
                    else if (rr < 0 || rr >= R) continue;
                    nd = cross ? -d : d;
                }
                int enemy = (side == 0) ? (bit_set(PBUP(g), rr) || bit_set(PBDN(g), rr))
                                        : (bit_set(PWUP(g), rr) || bit_set(PWDN(g), rr));
                if (enemy) {
                    make_move(pos, side, f, r, g, rr, nd, buf + (size_t)ncap * NBYTES);
                    ncap++;
                }
            }
        }
    }
    if (ncap) { *has_cap = 1; return ncap; }
    if (npush) memcpy(buf, pbuf, (size_t)npush * NBYTES);
    return npush;
}

/* ---------------- hash table ---------------- */
static uint64_t CAP = 0, CNT = 0;
static uint8_t *KEY, *VAL;
static uint64_t *HSH;

static uint64_t fnv(const uint8_t *p, int n)
{
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < n; i++) { h ^= p[i]; h *= 1099511628211ULL; }
    return h;
}

static void rehash(uint64_t newcap)
{
    uint8_t *nk = malloc(newcap * NBYTES);
    uint8_t *nv = malloc(newcap);
    uint64_t *nh = malloc(newcap * sizeof(uint64_t));
    memset(nk, 0, newcap * NBYTES);
    memset(nv, 0, newcap);
    memset(nh, 0, newcap * sizeof(uint64_t));
    for (uint64_t i = 0; i < CAP; i++) {
        if (!HSH[i]) continue;
        uint64_t j = HSH[i] & (newcap - 1);
        while (nh[j]) j = (j + 1) & (newcap - 1);
        nh[j] = HSH[i];
        memcpy(nk + j * NBYTES, KEY + i * NBYTES, NBYTES);
        nv[j] = VAL[i];
    }
    free(KEY); free(VAL); free(HSH);
    KEY = nk; VAL = nv; HSH = nh; CAP = newcap;
}

static void init_table(uint64_t cap)
{
    CAP = 0; CNT = 0;
    rehash(cap);
}

static int lookup(const uint8_t *key, uint8_t *val)
{
    uint64_t h = fnv(key, NBYTES);
    uint64_t j = h & (CAP - 1);
    while (HSH[j]) {
        if (HSH[j] == h && memcmp(KEY + j * NBYTES, key, NBYTES) == 0) {
            *val = VAL[j];
            return 1;
        }
        j = (j + 1) & (CAP - 1);
    }
    return 0;
}

static void store(const uint8_t *key, uint8_t val)
{
    if ((CNT + 1) * 10 > CAP * 7) rehash(CAP * 2);
    uint64_t h = fnv(key, NBYTES);
    uint64_t j = h & (CAP - 1);
    while (HSH[j]) {
        if (HSH[j] == h && memcmp(KEY + j * NBYTES, key, NBYTES) == 0) { VAL[j] = val; return; }
        j = (j + 1) & (CAP - 1);
    }
    HSH[j] = h;
    memcpy(KEY + j * NBYTES, key, NBYTES);
    VAL[j] = val;
    CNT++;
}

/* ---------------- search ---------------- */
static uint64_t POSCOUNT = 0;
static uint8_t *BUFPOOL;      /* per-depth successor buffers */
static size_t BUFPER = 0;     /* bytes per depth level */
static int DEPTHMAX = 0;

/* The successor list of a node must survive the recursive calls made from that
 * node, so every depth level gets its own buffer. */
static void solve_depth(const uint8_t *pos, int side, uint8_t *out, int depth)
{
    uint8_t v;
    if (lookup(pos, &v)) { *out = v; return; }
    POSCOUNT++;
    uint8_t *buf = BUFPOOL + (size_t)depth * BUFPER;
    uint8_t *pbuf = buf + (size_t)(MAXSUCC) * NBYTES;   /* pushes, kept separate */
    int has_cap = 0;
    int n = gen_moves(pos, side, buf, pbuf, &has_cap);
    uint8_t res;
    if (n == 0) {
        res = 0 | (1 << 1); /* normal: loss ; misere: win */
    } else {
        int normal_win = 0, misere_win = 0;
        for (int i = 0; i < n; i++) {
            uint8_t sub;
            solve_depth(buf + (size_t)i * NBYTES, 1 - side, &sub, depth + 1);
            if (!(sub & 1)) normal_win = 1;
            if (!(sub & 2)) misere_win = 1;
            if (normal_win && misere_win) break;
        }
        res = (uint8_t)(normal_win | (misere_win << 1));
    }
    store(pos, res);
    *out = res;
}

static void solve(const uint8_t *pos, int side, uint8_t *out)
{
    solve_depth(pos, side, out, 0);
}

static void run(int surf, int files, int ranks)
{
    S = surf;
    F = files;
    R = ranks;
    MOB = (surf == S_MOBIUS_M || surf == S_MOBIUS_T);
    NBYTES = F * 4 + 1;
    init_table(1u << 16);
    POSCOUNT = 0;
    free(BUFPOOL);
    /* every move either removes a pawn or advances one, so the game is short */
    DEPTHMAX = 2 * F * R + 8;
    BUFPER = (size_t)(2 * F * R + 2) * NBYTES + (size_t)MAXSUCC * NBYTES;
    BUFPOOL = malloc((size_t)DEPTHMAX * BUFPER);

    uint8_t start[MAXPOS];
    memset(start, 0, NBYTES);
    for (int f = 0; f < F; f++) {
        start[4 * f + 0] |= (uint8_t)(1u << 0);           /* White, up, rank 0 */
        start[4 * f + 3] |= (uint8_t)(1u << (ranks - 1));  /* Black, down, last rank */
    }
    start[NBYTES - 1] = 0; /* White to move */
    uint8_t outW, outB;
    solve(start, 0, &outW);
    uint8_t s2[MAXPOS];
    memcpy(s2, start, NBYTES);
    s2[NBYTES - 1] = 1; /* Black to move */
    solve(s2, 1, &outB);

    const char *names[] = {"flat", "cyl", "torus", "mobiusM", "mobiusT"};
    printf("%-8s %3d %3d  %d %d  %d %d  %llu\n", names[surf], files, ranks,
           outW & 1, outB & 1, (outW >> 1) & 1, (outB >> 1) & 1,
           (unsigned long long)POSCOUNT);
    fflush(stdout);
}

int main(int argc, char **argv)
{
    if (argc >= 4) {
        int surf;
        if (!strcmp(argv[1], "flat")) surf = S_FLAT;
        else if (!strcmp(argv[1], "cyl")) surf = S_CYL;
        else if (!strcmp(argv[1], "torus")) surf = S_TORUS;
        else if (!strcmp(argv[1], "mobiusM")) surf = S_MOBIUS_M;
        else if (!strcmp(argv[1], "mobiusT")) surf = S_MOBIUS_T;
        else { fprintf(stderr, "unknown surface\n"); return 1; }
        run(surf, atoi(argv[2]), atoi(argv[3]));
        return 0;
    }
    char line[256];
    while (fgets(line, sizeof line, stdin)) {
        char nm[32];
        int files, ranks;
        if (sscanf(line, "%31s %d %d", nm, &files, &ranks) != 3) continue;
        int surf;
        if (!strcmp(nm, "flat")) surf = S_FLAT;
        else if (!strcmp(nm, "cyl")) surf = S_CYL;
        else if (!strcmp(nm, "torus")) surf = S_TORUS;
        else if (!strcmp(nm, "mobiusM")) surf = S_MOBIUS_M;
        else if (!strcmp(nm, "mobiusT")) surf = S_MOBIUS_T;
        else continue;
        run(surf, files, ranks);
    }
    return 0;
}
