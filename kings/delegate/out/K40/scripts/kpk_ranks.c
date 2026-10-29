/* KPK (king + pawn vs king) solver on an N-file x 8-rank board, flat or
 * cylindrical (files wrap: a and the last file are adjacent).
 *
 * Written for the atlas/cylinder workstream to test whether a trebuchet is a
 * real mutual zugzwang.  Single implementation; see REPORT.md for caveats.
 *
 * Promotion model: the pawn promotes to a queen only.  After promotion with
 * the defender to move:
 *   - if the defending king can capture the queen (queen adjacent, not
 *     protected by the other king) -> draw (KK);
 *   - if the defender has no legal move: mate -> win, otherwise stalemate -> draw;
 *   - otherwise -> win.  This assumes KQK is a forced win with the attacker
 *     to move, which is classical on the flat board and is what the project's
 *     4-man prototype reports for the 8x8 cylinder (one implementation).
 * Under-promotion is not considered (it matters in a handful of flat-board
 * KPK stalemate positions only).
 *
 * The pawn is always White's; Black-pawn positions are handled by the caller
 * via colour reversal (flip ranks, swap colours).
 *
 * Build:  cc -O2 -o kpk kpk.c
 * Use:    ./kpk N WRAP [UNDERPROMO] < queries   (WRAP = 1 cylinder, 0 flat;
 *         UNDERPROMO = 1 also credits a rook promotion on a flat board)
 * Query line: "WK BK P STM" with squares like h5 and STM in {W,B}; the pawn is
 * White's.  Output: the query followed by W (White wins) or D (draw).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int N, WRAP;
#ifndef RANKS
#define RANKS 8
#endif
#define R RANKS
static unsigned char res[2][64][64][64]; /* [stm][wk][bk][p] : 1 = White wins */

static int sqf(int s) { return s % N; }
static int sqr(int s) { return s / N; }
static int mk(int f, int r) { return r * N + f; }

static int step_file(int f, int df) {
    int g = f + df;
    if (WRAP) return (g % N + N) % N;
    return (g < 0 || g >= N) ? -1 : g;
}

static int kadj(int a, int b) {
    if (a == b) return 0;
    int fa = sqf(a), fb = sqf(b), ra = sqr(a), rb = sqr(b);
    if (abs(ra - rb) > 1) return 0;
    int d = abs(fa - fb);
    if (WRAP && N - d < d) d = N - d;
    return d <= 1;
}

static int king_moves(int s, int *out) {
    int n = 0, f = sqf(s), r = sqr(s);
    for (int df = -1; df <= 1; df++)
        for (int dr = -1; dr <= 1; dr++) {
            if (!df && !dr) continue;
            int g = step_file(f, df), q = r + dr;
            if (g < 0 || q < 0 || q >= R) continue;
            int t = mk(g, q);
            int dup = 0;
            for (int i = 0; i < n; i++) if (out[i] == t) dup = 1;
            if (!dup && t != s) out[n++] = t;
        }
    return n;
}

/* does a White pawn on p attack square t? */
static int pawn_att(int p, int t) {
    int pf = sqf(p), pr = sqr(p);
    if (sqr(t) != pr + 1) return 0;
    int a = step_file(pf, -1), b = step_file(pf, 1);
    return sqf(t) == a || sqf(t) == b;
}

/* is square t attacked by a queen on q, with blockers wk (and bk unless ignore_bk)? */
static int queen_att(int q, int t, int wk, int bk) {
    static const int D[8][2] = {{1,0},{-1,0},{0,1},{0,-1},{1,1},{1,-1},{-1,1},{-1,-1}};
    for (int d = 0; d < 8; d++) {
        int f = sqf(q), r = sqr(q);
        for (int k = 0; k < 64; k++) {
            f = step_file(f, D[d][0]);
            r += D[d][1];
            if (f < 0 || r < 0 || r >= R) break;
            int s = mk(f, r);
            if (s == q) break; /* wrapped all the way round */
            if (s == t) return 1;
            if (s == wk || s == bk) break;
        }
    }
    return 0;
}

static int UNDERPROMO = 0; /* credit rook promotion (flat boards only) */

static int rook_att(int q, int t, int wk, int bk) {
    static const int D[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
    for (int d = 0; d < 4; d++) {
        int f = sqf(q), r = sqr(q);
        for (int k = 0; k < 64; k++) {
            f = step_file(f, D[d][0]);
            r += D[d][1];
            if (f < 0 || r < 0 || r >= R) break;
            int s = mk(f, r);
            if (s == q) break;
            if (s == t) return 1;
            if (s == wk || s == bk) break;
        }
    }
    return 0;
}

static int rook_promo_value(int wk, int bk, int q) {
    int mv[8], n = king_moves(bk, mv), legal = 0;
    for (int i = 0; i < n; i++) {
        int d = mv[i];
        if (d == wk || kadj(d, wk)) continue;
        if (d == q) return 0;
        if (rook_att(q, d, wk, -1)) continue;
        legal++;
    }
    if (legal) return 1;
    return rook_att(q, bk, wk, -1) ? 1 : 0;
}

/* value after White promotes on q, Black to move: 1 win, 0 draw */
static int promo_value(int wk, int bk, int q) {
#ifdef PMODEL
    (void)wk; (void)bk; (void)q; return 1; /* K40 diagnostic: P model, a promotion wins at once */
#endif
    if (UNDERPROMO && !WRAP && rook_promo_value(wk, bk, q)) return 1;
    int mv[8], n = king_moves(bk, mv), legal = 0;
    for (int i = 0; i < n; i++) {
        int d = mv[i];
        if (d == wk || kadj(d, wk)) continue;
        if (d == q) return 0; /* queen unprotected (d not adjacent to wk) -> capture -> KK */
        if (queen_att(q, d, wk, -1)) continue; /* bk removed from blockers */
        legal++;
    }
    if (legal) return 1;
    return queen_att(q, bk, wk, -1) ? 1 : 0; /* mate : stalemate */
}

static int legal_state(int stm, int wk, int bk, int p) {
    if (wk == bk || wk == p || bk == p) return 0;
    if (sqr(p) < 1 || sqr(p) > R - 2) return 0;
    if (kadj(wk, bk)) return 0;
    if (stm == 0 && pawn_att(p, bk)) return 0; /* Black in check with White to move */
    return 1;
}

static void solve(void) {
    memset(res, 0, sizeof res);
    int S = N * R, changed = 1, it = 0;
    while (changed) {
        changed = 0; it++;
        for (int wk = 0; wk < S; wk++) for (int bk = 0; bk < S; bk++) for (int p = 0; p < S; p++) {
            /* White to move */
            if (!res[0][wk][bk][p] && legal_state(0, wk, bk, p)) {
                int win = 0, mv[8], n = king_moves(wk, mv);
                for (int i = 0; i < n && !win; i++) {
                    int d = mv[i];
                    if (d == p || d == bk || kadj(d, bk)) continue;
                    if (res[1][d][bk][p]) win = 1;
                }
                int f = sqf(p), r = sqr(p);
                int p1 = mk(f, r + 1);
                if (!win && p1 != wk && p1 != bk) {
                    if (r + 1 == R - 1) win = promo_value(wk, bk, p1);
                    else if (res[1][wk][bk][p1]) win = 1;
                    if (!win && r == 1) {
                        int p2 = mk(f, 3);
                        if (p2 != wk && p2 != bk && res[1][wk][bk][p2]) win = 1;
                    }
                }
                if (win) { res[0][wk][bk][p] = 1; changed = 1; }
            }
            /* Black to move */
            if (!res[1][wk][bk][p] && legal_state(1, wk, bk, p)) {
                int mv[8], n = king_moves(bk, mv), legal = 0, escape = 0;
                for (int i = 0; i < n && !escape; i++) {
                    int d = mv[i];
                    if (d == wk || kadj(d, wk) || pawn_att(p, d)) continue;
                    legal++;
                    if (d == p) { escape = 1; break; } /* pawn unprotected: capture -> draw */
                    if (!res[0][wk][d][p]) escape = 1;
                }
                int lost;
                if (escape) lost = 0;
                else if (legal) lost = 1;
                else lost = pawn_att(p, bk); /* mate if in check, else stalemate */
                if (lost) { res[1][wk][bk][p] = 1; changed = 1; }
            }
        }
    }
    long tot[2] = {0, 0}, won[2] = {0, 0};
    for (int stm = 0; stm < 2; stm++)
        for (int wk = 0; wk < S; wk++) for (int bk = 0; bk < S; bk++) for (int p = 0; p < S; p++)
            if (legal_state(stm, wk, bk, p)) { tot[stm]++; won[stm] += res[stm][wk][bk][p]; }
    fprintf(stderr, "KPK N=%d %s: %d sweeps; WTM won %ld/%ld (%.3f%%), BTM won %ld/%ld (%.3f%%)\n",
            N, WRAP ? "cylinder" : "flat", it, won[0], tot[0], 100.0 * won[0] / tot[0],
            won[1], tot[1], 100.0 * won[1] / tot[1]);
}

static int parse_sq(const char *s) {
    int f = s[0] - 'a', r = atoi(s + 1) - 1;
    if (f < 0 || f >= N || r < 0 || r >= R) return -1;
    return mk(f, r);
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: kpk N WRAP < queries\n"); return 1; }
    N = atoi(argv[1]); WRAP = atoi(argv[2]);
    if (argc > 3) UNDERPROMO = atoi(argv[3]);
    if (N < 3 || N > 8) { fprintf(stderr, "N must be 3..8\n"); return 1; }
    solve();
    char a[8], b[8], c[8], d[8];
    while (scanf("%7s %7s %7s %7s", a, b, c, d) == 4) {
        int wk = parse_sq(a), bk = parse_sq(b), p = parse_sq(c), stm = d[0] == 'B';
        if (wk < 0 || bk < 0 || p < 0 || !legal_state(stm, wk, bk, p)) { printf("%s %s %s %s ILLEGAL\n", a, b, c, d); continue; }
        printf("%s %s %s %s %c\n", a, b, c, d, res[stm][wk][bk][p] ? 'W' : 'D');
    }
    return 0;
}
