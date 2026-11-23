/* tw.c -- pawn game solver for boards of F files x R ranks (F*R <= 64, R <= 12), flat or cylinder.
 * Whole-board model of cylcgt/pawns.py (components=[p]): one e.p. right, cleared by any move; count race rule;
 * e.p.-aware passed test; game ends at the first passed pawn.  State = (white mask, black mask, e.p. code),
 * square index s = (rank-1)*F + file, so any F*R <= 64 fits one 64-bit word per colour.
 * e.p. code: 0 none; 1+sq = White just double-stepped, skipped square sq (Black may capture);
 *            65+sq = Black just double-stepped, skipped square sq (White may capture).
 * Value of a position G = byte WL (bit k: Left wins G+*k moving first) and byte WR (Right), k = 0..7.
 * Signature = 8 chars, char k = outcome of G+*k (N, L, R, P).
 *
 *   tw --eval FILE        lines "F wrap | W: a2 b3 / B: a7 ..."  -> prints signature
 *   tw --scan F wrap R nw nb [--chunk i n] [--tlimit s] [--count] [--maxtab LOG2]
 *       exhaustive single-component roots (every file occupied, no passed pawn, W ranks 2..R-2, B ranks 3..R-1),
 *       up to mirror (flat) / rotation+reflection (cylinder); colour reversal identified when nw == nb.
 * Build: cc -O2 -o tw tw.c
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef uint64_t u64;
static int F, R, WRAP, EPON = 1;
static int sqf[64], sqr[64];
static u64 frontW[64], frontB[64], above[64], below[64];
#define SQ(f, r) (((r) - 1) * F + (f))
static inline u64 BIT(int s) { return 1ULL << s; }

static void init_board(int f, int r, int wrap) {
    F = f; R = r; WRAP = wrap;
    for (int s = 0; s < 64; s++) { sqf[s] = s % F; sqr[s] = s / F + 1; frontW[s] = frontB[s] = above[s] = below[s] = 0; }
    for (int fl = 0; fl < F; fl++) for (int rk = 1; rk <= R; rk++) {
        int s = SQ(fl, rk); u64 mw = 0, mb = 0, a = 0, b = 0;
        for (int d = -1; d <= 1; d++) {
            int g = fl + d;
            if (WRAP) g = (g + F) % F; else if (g < 0 || g >= F) continue;
            for (int t = 1; t <= R; t++) { if (t > rk) mw |= BIT(SQ(g, t)); if (t < rk) mb |= BIT(SQ(g, t)); }
        }
        for (int t = 1; t <= R; t++) { if (t > rk) a |= BIT(SQ(fl, t)); if (t < rk) b |= BIT(SQ(fl, t)); }
        frontW[s] = mw; frontB[s] = mb; above[s] = a; below[s] = b;
    }
}

static inline int epW_cap(int ep, int s) { return ep >= 1 && ep <= 64 && (ep - 1) + F == s; }
static inline int epB_cap(int ep, int s) { return ep >= 65 && (ep - 65) - F == s; }

static int passedW(u64 wm, u64 bm, int ep) {
    for (u64 m = wm; m; m &= m - 1) { int s = __builtin_ctzll(m);
        if (!(bm & frontW[s]) && !epW_cap(ep, s)) return 1; }
    return 0;
}
static int passedB(u64 wm, u64 bm, int ep) {
    for (u64 m = bm; m; m &= m - 1) { int s = __builtin_ctzll(m);
        if (!(wm & frontB[s]) && !epB_cap(ep, s)) return 1; }
    return 0;
}
static int dist(u64 wm, u64 bm, int ep, int white) {
    int best = 1000000; u64 occ = wm | bm;
    if (white) {
        for (u64 m = wm; m; m &= m - 1) { int s = __builtin_ctzll(m), r = sqr[s];
            if (bm & frontW[s]) continue; if (epW_cap(ep, s)) continue; if (occ & above[s]) continue;
            int d = R - r - (r == 2); if (d < best) best = d; }
    } else {
        for (u64 m = bm; m; m &= m - 1) { int s = __builtin_ctzll(m), r = sqr[s];
            if (wm & frontB[s]) continue; if (epB_cap(ep, s)) continue; if (occ & below[s]) continue;
            int d = r - 1 - (r == R - 1); if (d < best) best = d; }
    }
    return best;
}

/* ---------------------------------------------------------------- memo */
typedef struct { u64 wm, bm; uint8_t ep, wl, wr, used; } Entry;
static Entry *tab; static u64 tcap, tcount; static int TABLOG = 24;
static inline u64 mix(u64 x) { x += 0x9E3779B97F4A7C15ull; x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ull;
    x = (x ^ (x >> 27)) * 0x94D049BB133111EBull; return x ^ (x >> 31); }
static void tab_init(void) { free(tab); tcap = 1ULL << TABLOG; tcount = 0; tab = calloc(tcap, sizeof(Entry));
    if (!tab) { fprintf(stderr, "oom\n"); exit(1); } }
static void tab_clear(void) { memset(tab, 0, tcap * sizeof(Entry)); tcount = 0; }
static inline u64 hkey(u64 wm, u64 bm, int ep) { return mix(wm ^ mix(bm ^ ((u64)ep << 56))) & (tcap - 1); }

static uint16_t solve(u64 wm, u64 bm, int ep);

static inline int child(u64 wm, u64 bm, int ep, int white) {
    int pw = passedW(wm, bm, ep), pb = passedB(wm, bm, ep);
    if (pw && pb) {
        int dm = dist(wm, bm, ep, white), dop = dist(wm, bm, ep, !white);
        int winner_white = (dop <= dm) ? !white : white;
        return (winner_white == white) ? 0xFF : 0;
    }
    if (pw) return white ? 0xFF : 0;
    if (pb) return white ? 0 : 0xFF;
    uint16_t v = solve(wm, bm, ep);
    int opp = white ? (v >> 8) : (v & 0xFF);
    return (~opp) & 0xFF;
}

static int gen(u64 wm, u64 bm, int ep, int white) {
    int acc = 0; u64 occ = wm | bm;
    u64 mine = white ? wm : bm, theirs = white ? bm : wm;
    int d = white ? 1 : -1, start = white ? 2 : R - 1;
#define CH(nm, nt, e) (white ? child((nm), (nt), (e), 1) : child((nt), (nm), (e), 0))
    for (u64 m = mine; m && acc != 0xFF; m &= m - 1) {
        int s = __builtin_ctzll(m), f = sqf[s], r = sqr[s], r1 = r + d;
        if (r1 < 1 || r1 > R) continue;
        u64 rest = mine & ~BIT(s);
        int t = s + d * F;
        if (!(occ & BIT(t))) {
            acc |= CH(rest | BIT(t), theirs, 0);
            int r2 = r + 2 * d;
            if (r == start && r2 >= 1 && r2 <= R && !(occ & BIT(t + d * F))) {
                int e = 0;
                if (EPON) {
                    int t2 = t + d * F, has = 0;
                    for (int sg = -1; sg <= 1; sg += 2) { int g = f + sg;
                        if (WRAP) g = (g + F) % F; else if (g < 0 || g >= F) continue;
                        if (theirs & BIT(SQ(g, r2))) has = 1; }
                    (void)t2;
                    if (has) e = white ? 1 + t : 65 + t;
                }
                acc |= CH(rest | BIT(t + d * F), theirs, e);
            }
        }
        for (int sg = -1; sg <= 1; sg += 2) {
            int g = f + sg;
            if (WRAP) g = (g + F) % F; else if (g < 0 || g >= F) continue;
            int tt = SQ(g, r1);
            if (theirs & BIT(tt)) acc |= CH(rest | BIT(tt), theirs & ~BIT(tt), 0);
            else if (white ? (ep >= 65 && ep - 65 == tt) : (ep >= 1 && ep <= 64 && ep - 1 == tt)) {
                int victim = white ? tt - F : tt + F;
                acc |= CH(rest | BIT(tt), theirs & ~BIT(victim), 0);
            }
        }
    }
    return acc;
}

static uint16_t solve(u64 wm, u64 bm, int ep) {
    u64 h = hkey(wm, bm, ep), st = h;
    while (tab[h].used) {
        if (tab[h].wm == wm && tab[h].bm == bm && tab[h].ep == ep) return tab[h].wl | (tab[h].wr << 8);
        h = (h + 1) & (tcap - 1); if (h == st) break;
    }
    int AL = gen(wm, bm, ep, 1), AR = gen(wm, bm, ep, 0);
    int WL = 0, WR = 0, loseL = 0, loseR = 0;
    for (int k = 0; k < 8; k++) {
        int wl = ((AL >> k) & 1) || loseR, wr = ((AR >> k) & 1) || loseL;
        if (wl) WL |= 1 << k; if (wr) WR |= 1 << k;
        if (!wr) loseR = 1; if (!wl) loseL = 1;
    }
    if (tcount + 1 < (tcap / 16) * 15) {
        h = hkey(wm, bm, ep);
        while (tab[h].used) { if (tab[h].wm == wm && tab[h].bm == bm && tab[h].ep == ep) return WL | (WR << 8); h = (h + 1) & (tcap - 1); }
        tab[h] = (Entry){wm, bm, (uint8_t)ep, (uint8_t)WL, (uint8_t)WR, 1}; tcount++;
    }
    return WL | (WR << 8);
}

static void sigstr(uint16_t v, char *o) {
    for (int k = 0; k < 8; k++) { int l = (v >> k) & 1, r = (v >> (8 + k)) & 1; o[k] = l && r ? 'N' : l ? 'L' : r ? 'R' : 'P'; }
    o[8] = 0;
}
static int nimber_of(const char *s) { /* exactly one P at q, all else N */
    int q = -1; for (int k = 0; k < 8; k++) { if (s[k] == 'P') { if (q >= 0) return -1; q = k; } else if (s[k] != 'N') return -1; }
    return q;
}

/* ---------------------------------------------------------------- position text */
static void pos_str(char *b, u64 wm, u64 bm) {
    char *p = b; p += sprintf(p, "W:");
    for (int r = 1; r <= R; r++) for (int f = 0; f < F; f++) if (wm & BIT(SQ(f, r))) p += sprintf(p, " %c%d", 'a' + f, r);
    p += sprintf(p, " / B:");
    for (int r = 1; r <= R; r++) for (int f = 0; f < F; f++) if (bm & BIT(SQ(f, r))) p += sprintf(p, " %c%d", 'a' + f, r);
}
static int parse_pos(const char *s, u64 *wm, u64 *bm) {
    *wm = *bm = 0; u64 *cur = NULL;
    while (*s) {
        if (*s == 'W') { cur = wm; s++; } else if (*s == 'B') { cur = bm; s++; }
        else if (*s >= 'a' && *s <= 'z') { int f = *s - 'a'; s++; int r = 0; while (*s >= '0' && *s <= '9') r = r * 10 + *s++ - '0';
            if (!cur || f >= F || r < 1 || r > R) return 0; *cur |= BIT(SQ(f, r)); }
        else s++;
    }
    return 1;
}

/* ---------------------------------------------------------------- root enumeration */
#define MAXCFG 30000
static int ncfg, cfg_nw[MAXCFG], cfg_nb[MAXCFG], cfg_maxW[MAXCFG], cfg_minW[MAXCFG], cfg_maxB[MAXCFG], cfg_minB[MAXCFG], cfg_rev[MAXCFG];
static uint32_t cfg_w[MAXCFG], cfg_b[MAXCFG];   /* bit r = rank r */
static int *idx_of; static int *lst[16][16], lcnt[16][16];

static void build_cfgs(void) {
    int nd = R - 2; /* ranks 2..R-1, ternary digit */
    long tot = 1; for (int i = 0; i < nd; i++) tot *= 3;
    idx_of = malloc(sizeof(int) * tot); for (long i = 0; i < tot; i++) idx_of[i] = -1;
    ncfg = 0;
    for (long c = 0; c < tot; c++) {
        uint32_t w = 0, b = 0; long x = c; int ok = 1;
        for (int i = 0; i < nd; i++) { int dgt = x % 3; x /= 3; int rk = i + 2;
            if (dgt == 1) { if (rk > R - 2) ok = 0; w |= 1u << rk; } else if (dgt == 2) { if (rk < 3) ok = 0; b |= 1u << rk; } }
        if (!ok || (!w && !b)) continue;
        int id = ncfg++; idx_of[c] = id; cfg_w[id] = w; cfg_b[id] = b;
        cfg_nw[id] = __builtin_popcount(w); cfg_nb[id] = __builtin_popcount(b);
        cfg_maxW[id] = w ? 31 - __builtin_clz(w) : 0; cfg_minW[id] = w ? __builtin_ctz(w) : 99;
        cfg_maxB[id] = b ? 31 - __builtin_clz(b) : 0; cfg_minB[id] = b ? __builtin_ctz(b) : 99;
    }
    for (int id = 0; id < ncfg; id++) { /* colour reverse: W rank r <-> B rank R+1-r */
        uint32_t w2 = 0, b2 = 0;
        for (int r = 1; r <= R; r++) { if (cfg_b[id] >> r & 1) w2 |= 1u << (R + 1 - r); if (cfg_w[id] >> r & 1) b2 |= 1u << (R + 1 - r); }
        long c = 0, mul = 1; for (int i = 0; i < nd; i++) { int rk = i + 2; int dgt = (w2 >> rk & 1) ? 1 : (b2 >> rk & 1) ? 2 : 0; c += dgt * mul; mul *= 3; }
        cfg_rev[id] = idx_of[c];
    }
    for (int a = 0; a < 16; a++) for (int b = 0; b < 16; b++) { lcnt[a][b] = 0; lst[a][b] = NULL; }
    for (int id = 0; id < ncfg; id++) lcnt[cfg_nw[id]][cfg_nb[id]]++;
    for (int a = 0; a < 16; a++) for (int b = 0; b < 16; b++) if (lcnt[a][b]) { lst[a][b] = malloc(sizeof(int) * lcnt[a][b]); lcnt[a][b] = 0; }
    for (int id = 0; id < ncfg; id++) { int a = cfg_nw[id], b = cfg_nb[id]; lst[a][b][lcnt[a][b]++] = id; }
}

static int sel[8], NW, NB, NOCOLSYM = 0, COUNT_ONLY, CH_I = 0, CH_N = 1;
static long nroots = 0, rseq = 0, processed = 0;
static double TLIMIT = 0; static clock_t T0; static int timed_out = 0;
static long hist[1 << 16]; static long nhit = 0;

static u64 maskcache_w(int f, int id) { u64 m = 0; for (int r = 1; r <= R; r++) if (cfg_w[id] >> r & 1) m |= BIT(SQ(f, r)); return m; }
static u64 maskcache_b(int f, int id) { u64 m = 0; for (int r = 1; r <= R; r++) if (cfg_b[id] >> r & 1) m |= BIT(SQ(f, r)); return m; }

static int file_ok(int g) { /* no passed pawn on file g, neighbours per board type; neighbours must be assigned */
    int mb = 0, mw = 99;
    for (int d = -1; d <= 1; d++) { int h = g + d; if (WRAP) h = (h + F) % F; else if (h < 0 || h >= F) continue;
        int id = sel[h]; if (cfg_maxB[id] > mb) mb = cfg_maxB[id]; if (cfg_minW[id] < mw) mw = cfg_minW[id]; }
    int id = sel[g];
    if (cfg_nw[id] && cfg_maxW[id] >= mb) return 0;   /* W pawn passed */
    if (cfg_nb[id] && cfg_minB[id] <= mw) return 0;   /* B pawn passed */
    return 1;
}

static int canonical(int cs) {
    int nv = WRAP ? 2 * F : 2;
    for (int c = 0; c <= cs; c++) for (int v = 0; v < nv; v++) {
        if (c == 0 && !WRAP && v == 0) continue; /* identity */
        int refl, shift;
        if (WRAP) { refl = v / F; shift = v % F; } else { refl = v; shift = 0; }
        if (c == 0 && refl == 0 && shift == 0) continue;
        int cmp = 0;
        for (int i = 0; i < F && !cmp; i++) {
            int j = refl ? (F - 1 - i) : i; j = (j + shift) % F;
            int id = sel[j]; if (c) id = cfg_rev[id];
            if (id < sel[i]) cmp = -1; else if (id > sel[i]) cmp = 1;
        }
        if (cmp < 0) return 0;
    }
    return 1;
}

static void leaf(void) {
    if (!WRAP && !file_ok(F - 1)) return;
    if (WRAP && (!file_ok(F - 1) || !file_ok(0))) return;
    if (!canonical((NW == NB && !NOCOLSYM) ? 1 : 0)) return;
    if ((rseq++ % CH_N) != CH_I) return;
    nroots++;
    if (COUNT_ONLY) { if (TLIMIT && (nroots & 0xFFFFF) == 0 && (double)(clock() - T0) / CLOCKS_PER_SEC > TLIMIT) timed_out = 1; return; }
    if (TLIMIT && (processed & 255) == 0 && (double)(clock() - T0) / CLOCKS_PER_SEC > TLIMIT) { timed_out = 1; return; }
    u64 wm = 0, bm = 0;
    for (int f = 0; f < F; f++) { wm |= maskcache_w(f, sel[f]); bm |= maskcache_b(f, sel[f]); }
    if (tcount * 2 > tcap) tab_clear();
    uint16_t v = solve(wm, bm, 0);
    processed++;
    char sg[9]; sigstr(v, sg);
    int key = 0; for (int k = 0; k < 8; k++) key |= (sg[k] == 'N' ? 0 : sg[k] == 'L' ? 1 : sg[k] == 'R' ? 2 : 3) << (2 * k);
    hist[key]++;
    int q = nimber_of(sg);
    if (q >= 2) { char b[512]; pos_str(b, wm, bm); printf("HIT\t*%d\t%d\t%d\t%s\t%s\n", q, NW, NB, b, sg); fflush(stdout); nhit++; }
}

static void dfs(int f, int remW, int remB) {
    if (timed_out) return;
    if (f == F) { if (!remW && !remB) leaf(); return; }
    for (int a = 0; a <= remW; a++) for (int b = 0; b <= remB; b++) {
        if (a + b < 1) continue;
        if ((F - f - 1) > (remW - a) + (remB - b)) continue;
        if (f == F - 1 && (remW - a || remB - b)) continue;
        for (int i = 0; i < lcnt[a][b]; i++) {
            sel[f] = lst[a][b][i];
            if (f >= 1 && (!WRAP || f >= 2) && !file_ok(f - 1)) continue;
            if (f >= 2 && 0) continue;
            dfs(f + 1, remW - a, remB - b);
            if (timed_out) return;
        }
    }
}

static void keystr(int key, char *o) { for (int k = 0; k < 8; k++) { int c = (key >> (2 * k)) & 3; o[k] = "NLRP"[c]; } o[8] = 0; }

int main(int argc, char **argv) {
    if (argc >= 3 && !strcmp(argv[1], "--eval")) {
        FILE *fp = fopen(argv[2], "r"); if (!fp) return 1;
        for (int i = 3; i + 1 < argc; i++) if (!strcmp(argv[i], "--maxtab")) TABLOG = atoi(argv[i + 1]);
        char line[4096]; int pf = -1, pr = -1, pw = -1; tab_init();
        while (fgets(line, sizeof line, fp)) {
            int f, w, r; char *bar = strchr(line, '|'); if (!bar) continue;
            if (sscanf(line, "%d %d %d", &f, &w, &r) != 3) continue;
            if (f != pf || r != pr || w != pw) { init_board(f, r, w); tab_clear(); pf = f; pr = r; pw = w; }
            u64 wm, bm; if (!parse_pos(bar + 1, &wm, &bm)) { printf("BAD\n"); continue; }
            if (tcount * 2 > tcap) tab_clear();
            int pwp = passedW(wm, bm, 0), pbp = passedB(wm, bm, 0); char sg[9];
            if (pwp && pbp) { printf("RACE\n"); continue; }
            if (pwp) strcpy(sg, "LLLLLLLL"); else if (pbp) strcpy(sg, "RRRRRRRR"); else sigstr(solve(wm, bm, 0), sg);
            printf("%s\n", sg); fflush(stdout);
        }
        return 0;
    }
    if (argc >= 7 && !strcmp(argv[1], "--scan")) {
        int f = atoi(argv[2]), w = atoi(argv[3]), r = atoi(argv[4]); NW = atoi(argv[5]); NB = atoi(argv[6]);
        for (int i = 7; i < argc; i++) {
            if (!strcmp(argv[i], "--chunk")) { CH_I = atoi(argv[i + 1]); CH_N = atoi(argv[i + 2]); i += 2; }
            else if (!strcmp(argv[i], "--tlimit")) TLIMIT = atof(argv[++i]);
            else if (!strcmp(argv[i], "--count")) COUNT_ONLY = 1;
            else if (!strcmp(argv[i], "--nocolsym")) NOCOLSYM = 1;
            else if (!strcmp(argv[i], "--maxtab")) TABLOG = atoi(argv[++i]);
        }
        if (f * r > 64 || r > 12 || r < 5) { fprintf(stderr, "bad board\n"); return 1; }
        init_board(f, r, w); build_cfgs(); if (!COUNT_ONLY) tab_init();
        T0 = clock();
        dfs(0, NW, NB);
        printf("#scan F=%d wrap=%d R=%d split=%d+%d chunk=%d/%d roots=%ld%s\n", F, WRAP, R, NW, NB, CH_I, CH_N, nroots, timed_out ? " INCOMPLETE" : "");
        if (!COUNT_ONLY) {
            for (int key = 0; key < (1 << 16); key++) if (hist[key]) { char s[9]; keystr(key, s); printf("#hist\t%s\t%ld\n", s, hist[key]); }
            printf("#done complete=%d processed=%ld hits=%ld cpu=%.1f states=%llu\n", !timed_out, processed, nhit,
                   (double)(clock() - T0) / CLOCKS_PER_SEC, (unsigned long long)tcount);
        }
        return 0;
    }
    fprintf(stderr, "usage\n"); return 1;
}
