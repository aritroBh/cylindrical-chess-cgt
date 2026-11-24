/* enumerate.c - Fast enumeration of KPKP and KPPK positions */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 8
#define FILES "abcdefgh"

static int king_dist[64][64];
static int pawn_attacks[2][64][64];

static inline void sqname(int s, char *out) {
    sprintf(out, "%c%d", FILES[s % N], s / N + 1);
}

static void build_tables(int wrap) {
    for (int a = 0; a < 64; a++) {
        for (int b = 0; b < 64; b++) {
            int df = abs(a % N - b % N);
            if (wrap) df = df < N - df ? df : N - df;
            king_dist[a][b] = df > abs(a / N - b / N) ? df : abs(a / N - b / N);
        }
    }
    memset(pawn_attacks, 0, sizeof(pawn_attacks));
    for (int color = 0; color < 2; color++) {
        for (int p = 0; p < 64; p++) {
            int f = p % N, r = p / N;
            for (int df = -1; df <= 1; df += 2) {
                int g = f + df;
                if (wrap) g = (g % N + N) % N;
                else if (g < 0 || g >= N) continue;
                int t = color == 0 ? (r + 1) * N + g : (r - 1) * N + g;
                if (t >= 0 && t < 64) pawn_attacks[color][p][t] = 1;
            }
        }
    }
}

static inline int in_check(int wk, int bk, const int *wp, int nwp, const int *bp, int nbp, int side) {
    if (side == 0) { /* White king */
        if (king_dist[bk][wk] <= 1) return 1;
        for (int i = 0; i < nbp; i++) if (pawn_attacks[1][bp[i]][wk]) return 1;
    } else { /* Black king */
        if (king_dist[wk][bk] <= 1) return 1;
        for (int i = 0; i < nwp; i++) if (pawn_attacks[0][wp[i]][bk]) return 1;
    }
    return 0;
}

void enumerate_kpkp(int wrap, FILE *out) {
    build_tables(wrap);
    long long count = 0;
    char wk_s[4], bk_s[4], wp_s[4], bp_s[4];
    for (int wk = 0; wk < 64; wk++) {
        sqname(wk, wk_s);
        for (int bk = 0; bk < 64; bk++) {
            if (bk == wk || king_dist[wk][bk] <= 1) continue;
            sqname(bk, bk_s);
            for (int wp = 8; wp < 56; wp++) {
                if (wp == wk || wp == bk) continue;
                sqname(wp, wp_s);
                for (int bp = 8; bp < 56; bp++) {
                    if (bp == wk || bp == bk || bp == wp) continue;
                    sqname(bp, bp_s);
                    if (!in_check(wk, bk, &wp, 1, &bp, 1, 1)) {
                        fprintf(out, "K%s P%s k%s P%s w -\n", wk_s, wp_s, bk_s, bp_s);
                        count++;
                    }
                    if (!in_check(wk, bk, &wp, 1, &bp, 1, 0)) {
                        fprintf(out, "K%s P%s k%s P%s b -\n", wk_s, wp_s, bk_s, bp_s);
                        count++;
                    }
                }
            }
        }
    }
    fprintf(stderr, "KPKP %s: %lld positions\n", wrap ? "cyl" : "flat", count);
}

void enumerate_kppk(int wrap, FILE *out) {
    build_tables(wrap);
    long long count = 0;
    char wk_s[4], bk_s[4], wp1_s[4], wp2_s[4], bp_s[4];
    int wp[2];
    for (int wk = 0; wk < 64; wk++) {
        sqname(wk, wk_s);
        for (int bk = 0; bk < 64; bk++) {
            if (bk == wk || king_dist[wk][bk] <= 1) continue;
            sqname(bk, bk_s);
            for (int wp1 = 8; wp1 < 56; wp1++) {
                if (wp1 == wk || wp1 == bk) continue;
                sqname(wp1, wp1_s);
                for (int wp2 = wp1 + 1; wp2 < 56; wp2++) {
                    if (wp2 == wk || wp2 == bk) continue;
                    sqname(wp2, wp2_s);
                    wp[0] = wp1; wp[1] = wp2;
                    for (int bp = 8; bp < 56; bp++) {
                        if (bp == wk || bp == bk || bp == wp1 || bp == wp2) continue;
                        sqname(bp, bp_s);
                        if (!in_check(wk, bk, wp, 2, &bp, 1, 1)) {
                            fprintf(out, "K%s P%s P%s k%s P%s w -\n", wk_s, wp1_s, wp2_s, bk_s, bp_s);
                            count++;
                        }
                        if (!in_check(wk, bk, wp, 2, &bp, 1, 0)) {
                            fprintf(out, "K%s P%s P%s k%s P%s b -\n", wk_s, wp1_s, wp2_s, bk_s, bp_s);
                            count++;
                        }
                    }
                }
            }
        }
    }
    fprintf(stderr, "KPPK %s: %lld positions\n", wrap ? "cyl" : "flat", count);
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s <flat|cyl> <kpkp|kppk>\n", argv[0]);
        return 1;
    }
    int wrap = strcmp(argv[1], "cyl") == 0;
    if (strcmp(argv[2], "kpkp") == 0) {
        enumerate_kpkp(wrap, stdout);
    } else if (strcmp(argv[2], "kppk") == 0) {
        enumerate_kppk(wrap, stdout);
    } else {
        fprintf(stderr, "unknown type: %s\n", argv[2]);
        return 1;
    }
    return 0;
}