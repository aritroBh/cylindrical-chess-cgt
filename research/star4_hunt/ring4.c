/* ring4.c -- extension / annealing / evaluation on cylinders (and flat boards) of width up to 10.
 * The solver core is a copy of research/ring_family/ringeval.c (itself a re-layout of the scanner core) with a node budget.
 * Modes: --eval FILE | --extend FILE --k K [--rot N0] [--newonly] | --anneal FILE ...
 * Build: cc -O2 -DSTRIDE=10 -o ring4 ring4.c -lm
 */
#define main ringeval_main
#include "ringeval_budget.c"
#undef main
#include <math.h>

static int SINGLE = 1;
static int CH_I = 0, CH_N = 1;
static uint64_t rng_state = 88172645463325252ull;
static inline uint64_t rnd(void) { rng_state ^= rng_state << 13; rng_state ^= rng_state >> 7; rng_state ^= rng_state << 17; return rng_state; }

static int parse_pos(const char *s, uint64_t *wm, uint64_t *bm) {
    *wm = *bm = 0; uint64_t *cur = NULL; const char *p = s;
    while (*p) {
        if (*p == 'W' && p[1] == ':') { cur = wm; p += 2; continue; }
        if (*p == 'B' && p[1] == ':') { cur = bm; p += 2; continue; }
        if (*p >= 'a' && *p <= 'j' && p[1] >= '2' && p[1] <= '7' && cur) {
            int f = *p - 'a', r = p[1] - '0';
            if (f >= W) { fprintf(stderr, "file %c outside width %d\n", *p, W); exit(2); }
            *cur |= B(f, r); p += 2; continue;
        }
        p++;
    }
    return 0;
}
static int valid_root(uint64_t wm, uint64_t bm) {
    if (wm & bm) return 0;
    if (passedW(wm, bm, 0, 0) || passedB(wm, bm, 0, 0)) return 0;
    if (SINGLE) { uint64_t occ = wm | bm; for (int f = 0; f < W; f++) if (!(occ & filemask[f])) return 0; }
    return 1;
}
static int solve_budget(uint64_t wm, uint64_t bm, Value *out) {
    g_calls = 0;
    if (setjmp(g_jb)) return 0;
    *out = solve(wm, bm, 0, 0);
    return 1;
}
static int RESET_PCT = 50;
static void reset_if_big(void) { if (TAB_CAP && tcount * 100 >= TAB_CAP * RESET_PCT) tab_init(1u << 18); }

typedef struct { uint64_t wm, bm; } PP;
static PP *hs_tab; static uint64_t hs_cap, hs_cnt;
static void hs_init(uint64_t cap) { free(hs_tab); hs_cap = cap; hs_cnt = 0; hs_tab = calloc(cap, sizeof(PP)); if (!hs_tab) { fprintf(stderr, "oom hs\n"); exit(1); } }
static int hs_insert(uint64_t wm, uint64_t bm) {
    uint64_t h = mix(wm ^ mix(bm)) & (hs_cap - 1);
    while (hs_tab[h].wm || hs_tab[h].bm) { if (hs_tab[h].wm == wm && hs_tab[h].bm == bm) return 0; h = (h + 1) & (hs_cap - 1); }
    hs_tab[h].wm = wm; hs_tab[h].bm = bm; hs_cnt++; return 1;
}

static long ev_count = 0, hist_n[66], hist_near[8], budget_aborts = 0;
static int REPORT_NIM = 3, NEAR_REPORT = 3;
static void near_info(Value v, int *cnt, int *at) {
    *cnt = 0; *at = -1;
    for (int h = 0; h < 8; h++) if (!(((v.WL >> h) & 1) && ((v.WR >> h) & 1))) { (*cnt)++; *at = h; }
}
static int visit4(uint64_t wm, uint64_t bm, const char *tag) {
    Value v;
    if (!solve_budget(wm, bm, &v)) { budget_aborts++; return -2; }
    int nim = nimber_of(v); ev_count++;
    hist_n[nim < 0 ? 65 : nim]++;
    int cnt, at; near_info(v, &cnt, &at);
    if (cnt == 1) hist_near[at]++;
    if (nim >= REPORT_NIM || (cnt == 1 && at >= NEAR_REPORT && nim < 0)) {
        char buf[1024], d[128]; pos_str(buf, wm, bm); describe_value(d, v);
        printf("%s\t%s\t%d\t%s\t%s\n", nim >= REPORT_NIM ? "NIM" : "NEAR", buf, __builtin_popcountll(wm) + __builtin_popcountll(bm), d, tag);
        fflush(stdout);
    }
    return nim;
}

static uint64_t rotate_files(uint64_t m, int rot, int n0) {
    uint64_t out = 0;
    for (; m; m &= m - 1) { int s = __builtin_ctzll(m); out |= B((FILEOF(s) + rot) % n0, RANKOF(s)); }
    return out;
}
static uint64_t shift_files(uint64_t m, int off) {
    uint64_t out = 0;
    for (; m; m &= m - 1) { int s = __builtin_ctzll(m); out |= B(FILEOF(s) + off, RANKOF(s)); }
    return out;
}
static int min_file(uint64_t m) { int mn = 99; for (; m; m &= m - 1) { int f = FILEOF(__builtin_ctzll(m)); if (f < mn) mn = f; } return mn; }
static int max_file(uint64_t m) { int mx = -1; for (; m; m &= m - 1) { int f = FILEOF(__builtin_ctzll(m)); if (f > mx) mx = f; } return mx; }

static int xsq_n; static uint64_t xsq_bit[128]; static int xsq_white[128];
static int NEWONLY = 0, core_lo = 0, core_hi = 0, XPMAX = 99; static long ext_seq = 0, ext_cand = 0, ext_skip = 0;
static void ext_rec(uint64_t wm, uint64_t bm, int start, int left, const char *tag) {
    for (int i = start; i < xsq_n; i++) {
        uint64_t bit = xsq_bit[i];
        if ((wm | bm) & bit) continue;
        if (NEWONLY) { int ff = FILEOF(__builtin_ctzll(bit)); if (ff >= core_lo && ff <= core_hi) continue; }
        uint64_t nw2 = xsq_white[i] ? wm | bit : wm, nb2 = xsq_white[i] ? bm : bm | bit;
        if (__builtin_popcountll(nw2) + __builtin_popcountll(nb2) > XPMAX) continue;
        ext_seq++;
        if (CH_N > 1 && (ext_seq % CH_N) != CH_I) { if (left > 1) ext_rec(nw2, nb2, i + 1, left - 1, tag); continue; }
        if (valid_root(nw2, nb2) && hs_insert(nw2, nb2)) {
            if (hs_cnt > 12000000) hs_init(1u << 24);
            reset_if_big();
            visit4(nw2, nb2, tag); ext_cand++;
        } else ext_skip++;
        if (left > 1) ext_rec(nw2, nb2, i + 1, left - 1, tag);
    }
}
static void extend_mode(const char *fn, int K, int rot_n0) {
    static PP seeds[2048]; int ns = 0;
    FILE *fp = fopen(fn, "r"); if (!fp) { perror(fn); exit(1); }
    char line[2048];
    while (fgets(line, sizeof line, fp) && ns < 2048) {
        if (line[0] == '#' || strlen(line) < 5) continue;
        uint64_t wm, bm; parse_pos(line, &wm, &bm); seeds[ns].wm = wm; seeds[ns].bm = bm; ns++;
    }
    fclose(fp);
    xsq_n = 0;
    for (int f = 0; f < W; f++) {
        for (int r = 2; r <= 6; r++) { xsq_bit[xsq_n] = B(f, r); xsq_white[xsq_n++] = 1; }
        for (int r = 3; r <= 7; r++) { xsq_bit[xsq_n] = B(f, r); xsq_white[xsq_n++] = 0; }
    }
    tab_init(1u << 18); hs_init(1u << 24);
    printf("#extend width=%d wrap=%d K=%d seeds=%d rot=%d newonly=%d budget=%llu chunk=%d/%d\n", W, WRAP, K, ns, rot_n0, NEWONLY, (unsigned long long)g_budget, CH_I, CH_N);
    for (int si = 0; si < ns; si++) {
        uint64_t sw = seeds[si].wm, sb = seeds[si].bm;
        int lo = min_file(sw | sb), hi = max_file(sw | sb), span = hi - lo + 1;
        int nrot = rot_n0 > 0 ? rot_n0 : 0;
        for (int off = 0; nrot ? off < nrot : off + span <= W; off++) {
            if (WRAP && !nrot && off > 0) break;
            uint64_t w2, b2;
            if (nrot) { w2 = rotate_files(sw, off, rot_n0); b2 = rotate_files(sb, off, rot_n0); core_lo = 0; core_hi = rot_n0 - 1; }
            else { w2 = shift_files(sw, off - lo); b2 = shift_files(sb, off - lo); core_lo = off; core_hi = off + span - 1; }
            char tag[64]; sprintf(tag, "X%d.%d", si, off);
            long c0 = ext_cand;
            if (valid_root(w2, b2) && hs_insert(w2, b2)) visit4(w2, b2, tag);
            ext_rec(w2, b2, 0, K, tag);
            fprintf(stderr, "seed %d off %d: new candidates %ld (evals %ld, aborts %ld, states %llu)\n", si, off, ext_cand - c0, ev_count, budget_aborts, (unsigned long long)tcount);
        }
    }
    printf("#extend done evals=%ld skipped=%ld budget_aborts=%ld\n#hist_nim", ev_count, ext_skip, budget_aborts);
    for (int q = 0; q < 66; q++) if (hist_n[q]) printf(" nim%d=%ld", q, hist_n[q]);
    printf("\n#hist_near"); for (int q = 0; q < 8; q++) printf(" n%d=%ld", q, hist_near[q]);
    printf("\n");
}

/* ---- annealing (outcome-vector score) */
static int score_of(Value v, int *nim_out, int *near_out) {
    int cnt, at; near_info(v, &cnt, &at);
    int nim = nimber_of(v);
    *nim_out = nim; *near_out = (cnt == 1) ? at : -1;
    if (nim >= 0 && nim < 8) return 40 + 10 * nim;
    if (cnt == 1) return 25 + 5 * at;
    if (cnt == 2) return 12;
    if (cnt == 0) return 0;
    return 5;
}
static void anneal_mode(const char *fn, long iters, double temp, int pmin, int pmax) {
    static PP seeds[1024]; int ns = 0;
    FILE *fp = fopen(fn, "r"); if (!fp) { perror(fn); exit(1); }
    char line[2048];
    while (fgets(line, sizeof line, fp) && ns < 1024) {
        if (line[0] == '#' || strlen(line) < 5) continue;
        uint64_t wm, bm; parse_pos(line, &wm, &bm); seeds[ns].wm = wm; seeds[ns].bm = bm; ns++;
    }
    fclose(fp);
    tab_init(1u << 18); hs_init(1u << 22);
    printf("#anneal width=%d wrap=%d iters=%ld temp=%.1f pmin=%d pmax=%d seeds=%d budget=%llu\n", W, WRAP, iters, temp, pmin, pmax, ns, (unsigned long long)g_budget);
    long total = 0;
    for (int si = 0; si < ns; si++) {
        uint64_t cw = seeds[si].wm, cb = seeds[si].bm;
        if (!valid_root(cw, cb)) { fprintf(stderr, "seed %d invalid\n", si); continue; }
        Value v; int nim, nr;
        if (!solve_budget(cw, cb, &v)) continue;
        int cs = score_of(v, &nim, &nr);
        for (long it = 0; it < iters; it++) {
            uint64_t nw_ = cw, nb_ = cb;
            int n = __builtin_popcountll(cw) + __builtin_popcountll(cb);
            int kind = (int)(rnd() % 12), white = (int)(rnd() & 1);
            uint64_t *mine = white ? &nw_ : &nb_;
            int rlo = white ? 2 : 3, rhi = white ? 6 : 7, cnt = __builtin_popcountll(*mine);
            if (kind < 6) {
                if (!cnt) continue;
                int pick = (int)(rnd() % cnt); uint64_t m = *mine; while (pick--) m &= m - 1;
                int s = __builtin_ctzll(m); int f = FILEOF(s) + (int)(rnd() % 3) - 1, r = RANKOF(s) + (int)(rnd() % 3) - 1;
                if (WRAP) f = (f + W) % W;
                if (f < 0 || f >= W || r < rlo || r > rhi) continue;
                *mine &= ~(m & -m); *mine |= B(f, r);
            } else if (kind < 7) {
                if (!cnt) continue;
                int pick = (int)(rnd() % cnt); uint64_t m = *mine; while (pick--) m &= m - 1;
                *mine &= ~(m & -m);
                *mine |= B((int)(rnd() % W), rlo + (int)(rnd() % (rhi - rlo + 1)));
            } else if (kind < 9) {
                if (n >= pmax) continue;
                *mine |= B((int)(rnd() % W), rlo + (int)(rnd() % (rhi - rlo + 1)));
            } else if (kind < 10) {
                if (n + 2 > pmax) continue;
                int f = (int)(rnd() % W), r = 2 + (int)(rnd() % 4), gap = 1 + 2 * (int)(rnd() % 2);
                if (r + gap + 1 > 7) continue;
                nw_ |= B(f, r); nb_ |= B(f, r + gap + 1);
            } else {
                if (n <= pmin || cnt <= 1) continue;
                int pick = (int)(rnd() % cnt); uint64_t m = *mine; while (pick--) m &= m - 1;
                *mine &= ~(m & -m);
            }
            if (nw_ == cw && nb_ == cb) continue;
            { int n2 = __builtin_popcountll(nw_) + __builtin_popcountll(nb_); if (n2 < pmin || n2 > pmax) continue; }
            if (!valid_root(nw_, nb_)) continue;
            reset_if_big();
            int fresh = hs_insert(nw_, nb_);
            if (hs_cnt > 3000000) hs_init(1u << 22);
            if (!solve_budget(nw_, nb_, &v)) { budget_aborts++; continue; }
            int nim2, nr2; int ns_ = score_of(v, &nim2, &nr2); total++;
            if (fresh) {
                hist_n[nim2 < 0 ? 65 : nim2]++; if (nr2 >= 0) hist_near[nr2]++;
                if (nim2 >= 4 || nr2 >= 4 || nim2 == 3) {
                    char buf[1024], d[128]; pos_str(buf, nw_, nb_); describe_value(d, v);
                    printf("%s\t%s\t%d\t%s\n", nim2 >= 4 || nr2 >= 4 ? "HIT" : "L3", buf, __builtin_popcountll(nw_) + __builtin_popcountll(nb_), d); fflush(stdout);
                }
            }
            double d = ns_ - cs;
            if (d >= 0 || (double)(rnd() % 1000000) / 1e6 < exp(d / temp)) { cw = nw_; cb = nb_; cs = ns_; }
            if ((it + 1) % 5000 == 0) fprintf(stderr, "seed %d it %ld evals=%ld aborts=%ld score=%d\n", si, it + 1, total, budget_aborts, cs);
        }
    }
    printf("#anneal done evals=%ld aborts=%ld\n#hist_nim", total, budget_aborts);
    for (int q = 0; q < 66; q++) if (hist_n[q]) printf(" nim%d=%ld", q, hist_n[q]);
    printf("\n#hist_near"); for (int q = 0; q < 8; q++) printf(" n%d=%ld", q, hist_near[q]);
    printf("\n");
}

int main(int argc, char **argv) {
    const char *extfile = NULL, *annfile = NULL, *evalfile = NULL; int K = 2, rot = 0, pmin = 9, pmax = 13; long iters = 20000; double temp = 8;
    W = 8; WRAP = 1; TAB_CAP = 16777216;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--width") && i + 1 < argc) W = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--flat")) WRAP = 0;
        else if (!strcmp(argv[i], "--cylinder")) WRAP = 1;
        else if (!strcmp(argv[i], "--single")) SINGLE = 1;
        else if (!strcmp(argv[i], "--nosingle")) SINGLE = 0;
        else if (!strcmp(argv[i], "--max-entries") && i + 1 < argc) TAB_CAP = (uint64_t)atoll(argv[++i]);
        else if (!strcmp(argv[i], "--extend") && i + 1 < argc) extfile = argv[++i];
        else if (!strcmp(argv[i], "--anneal") && i + 1 < argc) annfile = argv[++i];
        else if (!strcmp(argv[i], "--eval") && i + 1 < argc) evalfile = argv[++i];
        else if (!strcmp(argv[i], "--k") && i + 1 < argc) K = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--rot") && i + 1 < argc) rot = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--newonly")) NEWONLY = 1;
        else if (!strcmp(argv[i], "--xpmax") && i + 1 < argc) XPMAX = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--chunk") && i + 2 < argc) { CH_I = atoi(argv[++i]); CH_N = atoi(argv[++i]); }
        else if (!strcmp(argv[i], "--evalbudget") && i + 1 < argc) g_budget = (uint64_t)atoll(argv[++i]);
        else if (!strcmp(argv[i], "--iters") && i + 1 < argc) iters = atol(argv[++i]);
        else if (!strcmp(argv[i], "--temp") && i + 1 < argc) temp = atof(argv[++i]);
        else if (!strcmp(argv[i], "--pmin") && i + 1 < argc) pmin = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--pmax") && i + 1 < argc) pmax = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--rng") && i + 1 < argc) rng_state ^= mix((uint64_t)atoll(argv[++i]));
        else if (!strcmp(argv[i], "--rep-nim") && i + 1 < argc) REPORT_NIM = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--near") && i + 1 < argc) NEAR_REPORT = atoi(argv[++i]);
        else { fprintf(stderr, "unknown option %s\n", argv[i]); return 2; }
    }
    init_masks();
    if (evalfile) {
        tab_init(1u << 18);
        FILE *fp = fopen(evalfile, "r"); char line[2048];
        while (fgets(line, sizeof line, fp)) {
            if (line[0] == '#' || strlen(line) < 5) continue;
            line[strcspn(line, "\r\n")] = 0;
            uint64_t wm, bm; parse_pos(line, &wm, &bm);
            char buf[1024], d[128]; pos_str(buf, wm, bm);
            if (passedW(wm, bm, 0, 0) || passedB(wm, bm, 0, 0)) { printf("%s\tPASSED\n", buf); continue; }
            Value v; reset_if_big();
            if (!solve_budget(wm, bm, &v)) { printf("%s\tBUDGET\n", buf); continue; }
            describe_value(d, v); printf("%s\t%d\t%s\n", buf, __builtin_popcountll(wm) + __builtin_popcountll(bm), d); fflush(stdout);
        }
        return 0;
    }
    if (extfile) { extend_mode(extfile, K, rot); return 0; }
    if (annfile) { anneal_mode(annfile, iters, temp, pmin, pmax); return 0; }
    fprintf(stderr, "need a mode\n"); return 2;
}
