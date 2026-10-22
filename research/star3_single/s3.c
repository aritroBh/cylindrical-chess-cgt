/* s3.c -- scanner / evaluator / local search for single-component *3 in the default setting.
 *
 * The solver core (masks, passed test, race distance, memo table, gen, child_mask, solve) is copied
 * UNCHANGED from research/star26_rings/frontier_split1_fixed2.c (see base_fixed2.c in this directory).
 * What is new:
 *   --single      keep only roots with every file occupied (one cylcgt component on a flat board; rings always)
 *   --colsym      (only with nw == nb) also identify a root with its colour-reversed image
 *   --count       only count the roots
 *   --eval FILE   evaluate listed positions ("W: a4 b3 / B: a7 b7"), print outcome, nimber, outcome string of G+*k
 *   --search ...  local search (see below)
 * Setting: --setting K, K as in the base scanner (0..8), default 2 = count / e.p. on / e.p.-aware.
 *
 * Build: cc -O2 -o s3 s3.c
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>
#include <math.h>

#define KMAX 64
#define FULL UINT64_MAX

static int W;          /* board width, 1..8 */
static int WRAP;       /* cylindrical file adjacency */
static int RACE;       /* 0 count, 1 mover, 2 opponent */
static int EPON;       /* e.p. allowed */
static int AWARE;      /* e.p.-capturable pawn does not count as passed */

static inline int SQ(int f, int r) { return (r - 1) * 8 + f; }
static inline uint64_t B(int f, int r) { return UINT64_C(1) << SQ(f, r); }
static inline int FILEOF(int s) { return s & 7; }
static inline int RANKOF(int s) { return (s >> 3) + 1; }

static uint64_t frontW[64], frontB[64];
static uint64_t filemask[8];

static int CHUNK_I = 0, CHUNK_N = 1;

static uint64_t comb(int n, int k) {
    uint64_t r = 1;
    for (int i = 0; i < k; i++) r = r * (uint64_t)(n - i) / (uint64_t)(i + 1);
    return r;
}

static void init_masks(void) {
    for (int f = 0; f < 8; f++) {
        filemask[f] = 0;
        for (int r = 1; r <= 8; r++) filemask[f] |= B(f, r);
    }
    memset(frontW, 0, sizeof frontW); memset(frontB, 0, sizeof frontB);
    for (int f = 0; f < W; f++)
        for (int r = 1; r <= 8; r++) {
            uint64_t mw = 0, mb = 0;
            for (int d = -1; d <= 1; d++) {
                int g = f + d;
                if (WRAP) g = (g + W) % W;
                else if (g < 0 || g >= W) continue;
                for (int s = 1; s <= 8; s++) {
                    if (s > r) mw |= B(g, s);
                    if (s < r) mb |= B(g, s);
                }
            }
            frontW[SQ(f, r)] = mw;
            frontB[SQ(f, r)] = mb;
        }
}

static int ep_capturable(uint64_t ep3, uint64_t ep6, int white, int s) {
    return white ? (RANKOF(s) == 4 && (ep3 & B(FILEOF(s), 3)))
                 : (RANKOF(s) == 5 && (ep6 & B(FILEOF(s), 6)));
}

static int passedW(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6) {
    for (uint64_t m = wm; m; m &= m - 1) {
        int s = __builtin_ctzll(m);
        if (!(bm & frontW[s])) {
            if (AWARE && ep_capturable(ep3, ep6, 1, s)) continue;
            return 1;
        }
    }
    return 0;
}
static int passedB(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6) {
    for (uint64_t m = bm; m; m &= m - 1) {
        int s = __builtin_ctzll(m);
        if (!(wm & frontB[s])) {
            if (AWARE && ep_capturable(ep3, ep6, 0, s)) continue;
            return 1;
        }
    }
    return 0;
}

static int dist(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6, int white) {
    int best = 1000000;
    uint64_t occ = wm | bm;
    if (white) {
        for (uint64_t m = wm; m; m &= m - 1) {
            int s = __builtin_ctzll(m), f = FILEOF(s), r = RANKOF(s);
            if (bm & frontW[s]) continue;
            if (AWARE && ep_capturable(ep3, ep6, 1, s)) continue;
            int front = 1;
            for (int q = r + 1; q <= 8; q++) if (occ & B(f, q)) front = 0;
            if (!front) continue;
            int d = 8 - r - (r == 2);
            if (d < best) best = d;
        }
    } else {
        for (uint64_t m = bm; m; m &= m - 1) {
            int s = __builtin_ctzll(m), f = FILEOF(s), r = RANKOF(s);
            if (wm & frontB[s]) continue;
            if (AWARE && ep_capturable(ep3, ep6, 0, s)) continue;
            int front = 1;
            for (int q = 1; q < r; q++) if (occ & B(f, q)) front = 0;
            if (!front) continue;
            int d = r - 1 - (r == 7);
            if (d < best) best = d;
        }
    }
    return best;
}

/* ------------------------------------------------------------------ memo */
typedef struct { uint64_t WL, WR; } Value;
typedef struct { uint64_t wm, bm, ep3, ep6; Value val; uint8_t used; } Entry;
static Entry *tab;
static uint64_t tcap, tcount;
static uint64_t TAB_CAP = 0;
static Entry *tab_dummy = NULL;

static inline uint64_t mix(uint64_t x) {
    x += 0x9E3779B97F4A7C15ull;
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ull;
    x = (x ^ (x >> 27)) * 0x94D049BB133111EBull;
    return x ^ (x >> 31);
}
static void tab_init(uint64_t cap) {
    free(tab);
    tcap = cap; tcount = 0;
    if (TAB_CAP && tcap > TAB_CAP) tcap = TAB_CAP;
    tab = calloc(tcap, sizeof(Entry));
    if (!tab) { fprintf(stderr, "out of memory\n"); exit(1); }
    if (!tab_dummy) {
        tab_dummy = calloc(1, sizeof(Entry));
        if (!tab_dummy) { fprintf(stderr, "out of memory\n"); exit(1); }
    }
}
static Entry *tab_find(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6) {
    uint64_t h = mix(wm ^ mix(bm) ^ mix(ep3) ^ mix(ep6)) & (tcap - 1);
    uint64_t start = h;
    while (tab[h].used && !(tab[h].wm == wm && tab[h].bm == bm &&
                            tab[h].ep3 == ep3 && tab[h].ep6 == ep6)) {
        h = (h + 1) & (tcap - 1);
        if (h == start) return tab_dummy;
    }
    return &tab[h];
}
static void tab_grow(void) {
    if (TAB_CAP && tcap >= TAB_CAP) return;
    Entry *old = tab; uint64_t oc = tcap;
    tab = calloc(oc * 2, sizeof(Entry)); tcap = oc * 2;
    if (!tab) { fprintf(stderr, "out of memory\n"); exit(1); }
    for (uint64_t i = 0; i < oc; i++) if (old[i].used)
        *tab_find(old[i].wm, old[i].bm, old[i].ep3, old[i].ep6) = old[i];
    free(old);
}

/* ------------------------------------------------------------------ search */
static Value solve(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6);

static uint32_t component_files(uint64_t occ, int g) {
    uint32_t comp = 1u << g;
    int changed;
    do {
        changed = 0;
        for (int f = 0; f < W; f++) if (comp & (1u << f))
            for (int d = -1; d <= 1; d += 2) {
                int q = f + d;
                if (WRAP) q = (q + W) % W;
                else if (q < 0 || q >= W) continue;
                uint32_t bit = 1u << q;
                if (!(comp & bit) && (occ & filemask[q])) { comp |= bit; changed = 1; }
            }
    } while (changed);
    return comp;
}

static uint64_t clear_component_ep(uint64_t ep, uint32_t files) {
    for (int f = 0; f < W; f++) if (files & (1u << f)) ep &= ~filemask[f];
    return ep;
}

static uint64_t child_mask(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6, int white) {
    int pw = passedW(wm, bm, ep3, ep6), pb = passedB(wm, bm, ep3, ep6);
    if (pw && pb) {
        int winner_white;
        if (RACE == 1) winner_white = white;
        else if (RACE == 2) winner_white = !white;
        else {
            int dm = dist(wm, bm, ep3, ep6, white), dop = dist(wm, bm, ep3, ep6, !white);
            winner_white = (dop <= dm) ? !white : white;
        }
        return (winner_white == white) ? FULL : 0;
    }
    if (pw) return white ? FULL : 0;
    if (pb) return white ? 0 : FULL;
    Value v = solve(wm, bm, ep3, ep6);
    uint64_t opp_wins = white ? v.WR : v.WL;
    return (~opp_wins) & FULL;
}

static int has_ep_capturer(uint64_t pawns, int f, int r) {
    for (int d = -1; d <= 1; d += 2) {
        int g = f + d;
        if (WRAP) g = (g + W) % W;
        else if (g < 0 || g >= W) continue;
        if (pawns & B(g, r)) return 1;
    }
    return 0;
}

static uint64_t gen(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6, int white) {
    uint64_t acc = 0;
    uint64_t occ = wm | bm;
    uint64_t mine = white ? wm : bm, theirs = white ? bm : wm;
    int d = white ? 1 : -1, start = white ? 2 : 7;
    for (uint64_t m = mine; m && acc != FULL; m &= m - 1) {
        int s = __builtin_ctzll(m), f = FILEOF(s), r = RANKOF(s);
        int r1 = r + d;
        if (r1 < 1 || r1 > 8) continue;
        uint32_t epcomp = (ep3 | ep6) ? component_files(occ, f) : 0;
        uint64_t base_ep3 = clear_component_ep(ep3, epcomp);
        uint64_t base_ep6 = clear_component_ep(ep6, epcomp);
        uint64_t rest = mine & ~B(f, r);
        if (!(occ & B(f, r1))) {
            uint64_t nm = rest | B(f, r1);
            acc |= white ? child_mask(nm, theirs, base_ep3, base_ep6, 1)
                         : child_mask(theirs, nm, base_ep3, base_ep6, 0);
            int r2 = r + 2 * d;
            if (r == start && !(occ & B(f, r2))) {
                uint64_t nm2 = rest | B(f, r2), cep3 = base_ep3, cep6 = base_ep6;
                if (EPON && has_ep_capturer(theirs, f, r2)) {
                    if (white) cep3 |= B(f, r1); else cep6 |= B(f, r1);
                }
                acc |= white ? child_mask(nm2, theirs, cep3, cep6, 1)
                             : child_mask(theirs, nm2, cep3, cep6, 0);
            }
        }
        for (int side = -1; side <= 1; side += 2) {
            int g = f + side;
            if (WRAP) g = (g + W) % W;
            else if (g < 0 || g >= W) continue;
            if (theirs & B(g, r1)) {
                uint64_t nm = rest | B(g, r1), nt = theirs & ~B(g, r1);
                acc |= white ? child_mask(nm, nt, base_ep3, base_ep6, 1)
                             : child_mask(nt, nm, base_ep3, base_ep6, 0);
            } else if ((white && (ep6 & B(g, r1))) || (!white && (ep3 & B(g, r1)))) {
                int victim_r = white ? r1 - 1 : r1 + 1;
                uint64_t nm = rest | B(g, r1), nt = theirs & ~B(g, victim_r);
                acc |= white ? child_mask(nm, nt, base_ep3, base_ep6, 1)
                             : child_mask(nt, nm, base_ep3, base_ep6, 0);
            }
        }
    }
    return acc;
}

static Value solve(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6) {
    Entry *e = tab_find(wm, bm, ep3, ep6);
    if (e->used) return e->val;
    uint64_t AL = gen(wm, bm, ep3, ep6, 1), AR = gen(wm, bm, ep3, ep6, 0);
    uint64_t WL = 0, WR = 0;
    int lose_L_seen = 0, lose_R_seen = 0;
    for (int k = 0; k < KMAX; k++) {
        int wl = ((AL >> k) & 1) || lose_R_seen;
        int wr = ((AR >> k) & 1) || lose_L_seen;
        if (wl) WL |= UINT64_C(1) << k;
        if (wr) WR |= UINT64_C(1) << k;
        if (!wr) lose_R_seen = 1;
        if (!wl) lose_L_seen = 1;
    }
    Value v = {WL, WR};
    if ((tcount + 1) * 2 > tcap) tab_grow();
    e = tab_find(wm, bm, ep3, ep6);
    if (e == tab_dummy || e->used) return v;
    if (tcount + 1 >= (tcap / 16) * 15) {
        uint64_t h = mix(wm ^ mix(bm) ^ mix(ep3) ^ mix(ep6)) & (tcap - 1);
        Entry *r = &tab[h];
        r->wm = wm; r->bm = bm; r->ep3 = ep3; r->ep6 = ep6; r->val = v; r->used = 1;
        return v;
    }
    e->wm = wm; e->bm = bm; e->ep3 = ep3; e->ep6 = ep6; e->val = v; e->used = 1; tcount++;
    return v;
}

/* ------------------------------------------------------------------ helpers on a solved root */
static char outcome_of(Value v) {
    return (v.WL & 1) && (v.WR & 1) ? 'N' : (v.WL & 1) ? 'L' : (v.WR & 1) ? 'R' : 'P';
}
static int nimber_of(Value v) {
    for (int q = 0; q < KMAX; q++) if (!((v.WL >> q) & 1) && !((v.WR >> q) & 1)) return q;
    return -1;
}

/* ------------------------------------------------------------------ roots */
typedef struct { uint64_t wm, bm; int n; } Root;
static Root *roots; static int nroots, rcap;
static int SINGLE = 0, COLSYM = 0, COUNT_ONLY = 0;

static uint64_t transform(uint64_t m, int shift, int reflect) {
    uint64_t out = 0;
    for (; m; m &= m - 1) {
        int s = __builtin_ctzll(m), f = FILEOF(s), r = RANKOF(s);
        if (reflect) f = W - 1 - f;
        f = (f + shift) % W;
        out |= B(f, r);
    }
    return out;
}
static uint64_t flip_ranks(uint64_t m) {
    uint64_t out = 0;
    for (; m; m &= m - 1) {
        int s = __builtin_ctzll(m), f = FILEOF(s), r = RANKOF(s);
        out |= B(f, 9 - r);
    }
    return out;
}

static int canonical_root(uint64_t wm, uint64_t bm) {
    uint64_t bestw = wm, bestb = bm;
    int variants = WRAP ? 2 * W : 1;
    for (int cs = 0; cs <= (COLSYM ? 1 : 0); cs++) {
        uint64_t cw = cs ? flip_ranks(bm) : wm, cb = cs ? flip_ranks(wm) : bm;
        for (int v = 0; v < variants; v++) {
            int refl = WRAP ? v / W : 1;
            int shift = WRAP ? v % W : 0;
            uint64_t tw = transform(cw, shift, refl), tb = transform(cb, shift, refl);
            if (tw < bestw || (tw == bestw && tb < bestb)) { bestw = tw; bestb = tb; }
        }
        if (!WRAP) {  /* flat: identity (not covered by the loop above, which only tries the reflection) */
            if (cs && (cw < bestw || (cw == bestw && cb < bestb))) { bestw = cw; bestb = cb; }
        }
    }
    return wm == bestw && bm == bestb;
}

static void add_root(uint64_t wm, uint64_t bm, int n) {
    if (!canonical_root(wm, bm)) return;
    if (COUNT_ONLY) { nroots++; return; }
    if (nroots == rcap) {
        rcap = rcap ? rcap * 2 : 1024;
        roots = realloc(roots, (size_t)rcap * sizeof(Root));
        if (!roots) { fprintf(stderr, "root allocation failed\n"); exit(1); }
    }
    roots[nroots++] = (Root){wm, bm, n};
}

static void enum_roots(int nw, int nb, int n) {
    int wc[64], bc[64], nwc = 0, nbc = 0;
    for (int f = 0; f < W; f++) {
        for (int r = 2; r <= 6; r++) wc[nwc++] = SQ(f, r);
        for (int r = 3; r <= 7; r++) bc[nbc++] = SQ(f, r);
    }
    if (nw > nwc || nb > nbc) return;
    int iw[16], ib[16];
    for (int i = 0; i < nw; i++) iw[i] = i;
    uint64_t wseq = 0;
    uint64_t total = comb(nwc, nw);
    while (1) {
        uint64_t wm = 0;
        for (int i = 0; i < nw; i++) wm |= B(wc[iw[i]] % 8, (wc[iw[i]] / 8) + 1);
        int in_chunk = 1;
        if (CHUNK_N > 1) {
            uint64_t lo = (uint64_t)CHUNK_I * total / CHUNK_N;
            uint64_t hi = (uint64_t)(CHUNK_I + 1) * total / CHUNK_N;
            in_chunk = (wseq >= lo && wseq < hi);
        }
        for (int i = 0; i < nb; i++) ib[i] = i;
        while (in_chunk) {
            uint64_t bm = 0;
            for (int i = 0; i < nb; i++) bm |= B(bc[ib[i]] % 8, (bc[ib[i]] / 8) + 1);
            if (!(wm & bm)) {
                uint64_t occ = wm | bm;
                int edge_ok = 1;
                for (int f = 0; f < W; f++) {
                    int need = SINGLE || WRAP || f == 0 || f == W - 1;
                    if (need && !(occ & filemask[f])) edge_ok = 0;
                }
                if (edge_ok && !passedW(wm, bm, 0, 0) && !passedB(wm, bm, 0, 0)) add_root(wm, bm, n);
            }
            int i = nb - 1;
            while (i >= 0 && ib[i] == nbc - nb + i) i--;
            if (i < 0) break;
            ib[i]++;
            for (int j = i + 1; j < nb; j++) ib[j] = ib[j - 1] + 1;
        }
        wseq++;
        int i = nw - 1;
        while (i >= 0 && iw[i] == nwc - nw + i) i--;
        if (i < 0) break;
        iw[i]++;
        for (int j = i + 1; j < nw; j++) iw[j] = iw[j - 1] + 1;
    }
}

static void pos_str(char *out, uint64_t wm, uint64_t bm) {
    char *p = out;
    p += sprintf(p, "W:");
    for (int f = 0; f < W; f++) for (int r = 1; r <= 8; r++) if (wm & B(f, r)) p += sprintf(p, " %c%d", 'a' + f, r);
    p += sprintf(p, " / B:");
    for (int f = 0; f < W; f++) for (int r = 1; r <= 8; r++) if (bm & B(f, r)) p += sprintf(p, " %c%d", 'a' + f, r);
}

static int parse_pos(const char *s, uint64_t *wm, uint64_t *bm) {
    *wm = *bm = 0;
    uint64_t *cur = NULL;
    const char *p = s;
    int maxf = -1;
    while (*p) {
        if (*p == 'W' && p[1] == ':') { cur = wm; p += 2; continue; }
        if (*p == 'B' && p[1] == ':') { cur = bm; p += 2; continue; }
        if (*p >= 'a' && *p <= 'h' && p[1] >= '1' && p[1] <= '8' && cur) {
            int f = *p - 'a', r = p[1] - '0';
            if (f >= W) { fprintf(stderr, "file %c outside width %d\n", *p, W); exit(2); }
            *cur |= B(f, r);
            if (f > maxf) maxf = f;
            p += 2; continue;
        }
        p++;
    }
    return maxf;
}

static const char *ostr(Value v, int K, char *buf) {
    for (int k = 0; k < K; k++) {
        int l = (v.WL >> k) & 1, r = (v.WR >> k) & 1;
        buf[k] = l && r ? 'N' : l ? 'L' : r ? 'R' : 'P';
    }
    buf[K] = 0; return buf;
}

/* ------------------------------------------------------------------ search / fitness */
static uint64_t rng_state = 88172645463325252ull;
static inline uint64_t rnd(void) {
    rng_state ^= rng_state << 13; rng_state ^= rng_state >> 7; rng_state ^= rng_state << 17; return rng_state;
}

/* distance of the outcome vector of G+*k (k < 8) from that of the nimber *target; lower is better, 0 iff WL,WR low
 * bytes are those of *target.  Beyond k = 7 nothing is looked at. */
static int fitness(Value v, int target) {
    uint64_t want = 0xFFull & ~(1ull << target);
    uint64_t wl = v.WL & 0xFF, wr = v.WR & 0xFF;
    return __builtin_popcountll(wl ^ want) + __builtin_popcountll(wr ^ want);
}

static int valid_root(uint64_t wm, uint64_t bm) {
    if (wm & bm) return 0;
    if (passedW(wm, bm, 0, 0) || passedB(wm, bm, 0, 0)) return 0;
    if (SINGLE) {
        uint64_t occ = wm | bm;
        for (int f = 0; f < W; f++) if (!(occ & filemask[f])) return 0;
    }
    return 1;
}


/* ------------------------------------------------------------------ edit-distance balls */
typedef struct { uint64_t wm, bm; } PP;
static PP *hs_tab; static uint64_t hs_cap, hs_cnt;
static void hs_init(uint64_t cap) { free(hs_tab); hs_cap = cap; hs_cnt = 0; hs_tab = calloc(cap, sizeof(PP)); if (!hs_tab) { fprintf(stderr, "oom hs\n"); exit(1); } }
/* returns 1 if newly inserted; (0,0) is never a real position */
static int hs_insert(uint64_t wm, uint64_t bm) {
    uint64_t h = mix(wm ^ mix(bm)) & (hs_cap - 1);
    while (hs_tab[h].wm || hs_tab[h].bm) {
        if (hs_tab[h].wm == wm && hs_tab[h].bm == bm) return 0;
        h = (h + 1) & (hs_cap - 1);
    }
    hs_tab[h].wm = wm; hs_tab[h].bm = bm; hs_cnt++;
    return 1;
}

static long ball_found, ball_eval, ball_star2, ball_star1;
static void ball_visit(uint64_t wm, uint64_t bm, int target, int level, int radius, uint64_t *cnt_by_nim) {
    if (!valid_root(wm, bm)) return;
    Value v = solve(wm, bm, 0, 0);
    int nim = nimber_of(v);
    ball_eval++;
    if (nim == 1) ball_star1++;
    if (nim == 2) ball_star2++;
    if (nim >= 0 && nim < 8) cnt_by_nim[nim]++;
    if (nim >= 3) {
        char buf[1024];
        pos_str(buf, wm, bm);
        printf("FOUND\t%s\t%d\t%c\t%d\tlevel=%d\n", buf, __builtin_popcountll(wm) + __builtin_popcountll(bm), outcome_of(v), nim, level);
        fflush(stdout); ball_found++;
    }
}

static void ball(const char *seedfile, int radius, int pmin, int pmax, int target, uint64_t maxnodes) {
    Root seeds[8192]; int ns = 0;
    FILE *fp = fopen(seedfile, "r"); if (!fp) { perror("seeds"); exit(1); }
    char line[2048];
    while (fgets(line, sizeof line, fp) && ns < 8192) {
        if (line[0] == '#' || strlen(line) < 5) continue;
        uint64_t wm, bm; parse_pos(line, &wm, &bm);
        seeds[ns++] = (Root){wm, bm, 0};
    }
    fclose(fp);
    printf("#ball width=%d wrap=%d single=%d radius=%d pmin=%d pmax=%d seeds=%d\n", W, WRAP, SINGLE, radius, pmin, pmax, ns);
    tab_init(1u << 20);
    int wsq[64], bsq[64], nwsq = 0, nbsq = 0;
    for (int f = 0; f < W; f++) {
        for (int r = 2; r <= 6; r++) wsq[nwsq++] = SQ(f, r);
        for (int r = 3; r <= 7; r++) bsq[nbsq++] = SQ(f, r);
    }
    for (int si = 0; si < ns; si++) {
        uint64_t cnt_by_nim[8] = {0};
        ball_eval = ball_star1 = ball_star2 = 0;
        long found0 = ball_found;
        hs_init(1u << 22);
        PP *cur = malloc(sizeof(PP)), *nxt = NULL; uint64_t ncur = 1, cap_next = 0;
        cur[0].wm = seeds[si].wm; cur[0].bm = seeds[si].bm;
        hs_insert(cur[0].wm, cur[0].bm);
        ball_visit(cur[0].wm, cur[0].bm, target, 0, radius, cnt_by_nim);
        for (int level = 1; level <= radius; level++) {
            uint64_t nn = 0;
            for (uint64_t ci = 0; ci < ncur; ci++) {
                uint64_t cw = cur[ci].wm, cb = cur[ci].bm;
                int n = __builtin_popcountll(cw) + __builtin_popcountll(cb);
                for (int col = 0; col < 2; col++) {
                    uint64_t mine = col ? cb : cw;
                    const int *sqs = col ? bsq : wsq; int nsqs = col ? nbsq : nwsq;
                    for (uint64_t m = mine; m; m &= m - 1) {
                        uint64_t bit = m & -m;
                        uint64_t rest = mine & ~bit;
                        for (int t = -1; t < nsqs; t++) {       /* t = -1: removal */
                            uint64_t nm;
                            if (t < 0) { if (n - 1 < pmin) continue; nm = rest; }
                            else {
                                uint64_t tb = UINT64_C(1) << sqs[t];
                                if ((mine | (col ? cw : cb)) & tb) continue;
                                nm = rest | tb;
                            }
                            uint64_t nw2 = col ? cw : nm, nb2 = col ? nm : cb;
                            if (!(nw2 | nb2)) continue;
                            if (!hs_insert(nw2, nb2)) continue;
                            if (nn == cap_next) { cap_next = cap_next ? cap_next * 2 : 4096; nxt = realloc(nxt, cap_next * sizeof(PP)); }
                            nxt[nn].wm = nw2; nxt[nn].bm = nb2; nn++;
                            ball_visit(nw2, nb2, target, level, radius, cnt_by_nim);
                        }
                    }
                    if (n + 1 <= pmax) {
                        for (int t = 0; t < nsqs; t++) {         /* addition */
                            uint64_t tb = UINT64_C(1) << sqs[t];
                            if ((cw | cb) & tb) continue;
                            uint64_t nw2 = col ? cw : cw | tb, nb2 = col ? cb | tb : cb;
                            if (!hs_insert(nw2, nb2)) continue;
                            if (nn == cap_next) { cap_next = cap_next ? cap_next * 2 : 4096; nxt = realloc(nxt, cap_next * sizeof(PP)); }
                            nxt[nn].wm = nw2; nxt[nn].bm = nb2; nn++;
                            ball_visit(nw2, nb2, target, level, radius, cnt_by_nim);
                        }
                    }
                }
                if (hs_cnt > maxnodes) break;
            }
            free(cur); cur = nxt; nxt = NULL; cap_next = 0; ncur = nn;
            if (hs_cnt > maxnodes) { fprintf(stderr, "seed %d: node cap reached at level %d\n", si, level); break; }
        }
        free(cur); free(nxt);
        char buf[1024]; pos_str(buf, seeds[si].wm, seeds[si].bm);
        printf("#seed %d %s nodes=%llu valid_evals=%ld nim0=%llu nim1=%llu nim2=%llu nim3+=%ld\n", si, buf, (unsigned long long)hs_cnt, ball_eval,
               (unsigned long long)cnt_by_nim[0], (unsigned long long)cnt_by_nim[1], (unsigned long long)cnt_by_nim[2], ball_found - found0);
        fflush(stdout);
    }
}

int main(int argc, char **argv) {
    int nw = -1, nb = -1, width = -1, setting = 2, count_only = 0;
    const char *evalfile = NULL;
    int search = 0, pmin = 6, pmax = 11, target = 3;
    long iters = 100000; double temp = 1.0;
    const char *seedfile = NULL; const char *ballfile = NULL; int radius = 2; uint64_t maxnodes = 50000000;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--width") && i + 1 < argc) width = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--nw") && i + 1 < argc) nw = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--nb") && i + 1 < argc) nb = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--setting") && i + 1 < argc) setting = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--chunk") && i + 2 < argc) { CHUNK_I = atoi(argv[++i]); CHUNK_N = atoi(argv[++i]); }
        else if (!strcmp(argv[i], "--max-entries") && i + 1 < argc) TAB_CAP = (uint64_t)atoll(argv[++i]);
        else if (!strcmp(argv[i], "--cylinder")) WRAP = 1;
        else if (!strcmp(argv[i], "--flat")) WRAP = 0;
        else if (!strcmp(argv[i], "--single")) SINGLE = 1;
        else if (!strcmp(argv[i], "--colsym")) COLSYM = 1;
        else if (!strcmp(argv[i], "--count")) { count_only = 1; COUNT_ONLY = 1; }
        else if (!strcmp(argv[i], "--eval") && i + 1 < argc) evalfile = argv[++i];
        else if (!strcmp(argv[i], "--search")) search = 1;
        else if (!strcmp(argv[i], "--seeds") && i + 1 < argc) seedfile = argv[++i];
        else if (!strcmp(argv[i], "--ball") && i + 1 < argc) ballfile = argv[++i];
        else if (!strcmp(argv[i], "--radius") && i + 1 < argc) radius = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--maxnodes") && i + 1 < argc) maxnodes = (uint64_t)atoll(argv[++i]);
        else if (!strcmp(argv[i], "--pmin") && i + 1 < argc) pmin = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--pmax") && i + 1 < argc) pmax = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--target") && i + 1 < argc) target = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--iters") && i + 1 < argc) iters = atol(argv[++i]);
        else if (!strcmp(argv[i], "--temp") && i + 1 < argc) temp = atof(argv[++i]);
        else if (!strcmp(argv[i], "--rng") && i + 1 < argc) rng_state ^= mix((uint64_t)atoll(argv[++i]));
        else { fprintf(stderr, "unknown or incomplete option %s\n", argv[i]); return 2; }
    }
    if (width < 1 || width > 8) { fprintf(stderr, "need --width 1..8\n"); return 2; }
    W = width;
    const char *rname[3] = {"count", "mover", "opponent"};
    { int r = setting / 3, t = setting % 3;
      RACE = r; EPON = (t != 1); AWARE = (t == 2); }
    init_masks();
    char buf[1024], ob[80];

    if (evalfile) {
        tab_init(1u << 18);
        FILE *fp = fopen(evalfile, "r");
        if (!fp) { perror("eval file"); return 1; }
        char line[2048];
        printf("#position\twidth\tn\toutcome\tnimber\tG+*k_k0-7\n");
        while (fgets(line, sizeof line, fp)) {
            if (line[0] == '#' || strlen(line) < 5) continue;
            line[strcspn(line, "\r\n")] = 0;
            uint64_t wm, bm; parse_pos(line, &wm, &bm);
            pos_str(buf, wm, bm);
            if (wm & bm) { printf("%s\t%d\t-\tOVERLAP\n", buf, W); continue; }
            int n = __builtin_popcountll(wm) + __builtin_popcountll(bm);
            if (passedW(wm, bm, 0, 0) || passedB(wm, bm, 0, 0)) { printf("%s\t%d\t%d\tPASSED\n", buf, W, n); continue; }
            Value v = solve(wm, bm, 0, 0);
            printf("%s\t%d\t%d\t%c\t%d\t%s\n", buf, W, n, outcome_of(v), nimber_of(v), ostr(v, 8, ob));
            fflush(stdout);
        }
        fclose(fp);
        return 0;
    }

    if (ballfile) { ball(ballfile, radius, pmin, pmax, target, maxnodes); return 0; }

    if (search) {
        /* simulated annealing over roots.  Moves: relocate one pawn to a random legal square; add a pawn;
         * remove a pawn.  Every root with nimber == target is printed. */
        if (!seedfile) { fprintf(stderr, "--search needs --seeds FILE\n"); return 2; }
        tab_init(1u << 20);
        Root seeds[4096]; int ns = 0;
        FILE *fp = fopen(seedfile, "r"); if (!fp) { perror("seeds"); return 1; }
        char line[2048];
        while (fgets(line, sizeof line, fp) && ns < 4096) {
            if (line[0] == '#' || strlen(line) < 5) continue;
            uint64_t wm, bm; parse_pos(line, &wm, &bm);
            seeds[ns++] = (Root){wm, bm, 0};
        }
        fclose(fp);
        long found = 0;
        printf("#search width=%d wrap=%d single=%d pmin=%d pmax=%d target=%d iters=%ld temp=%.2f seeds=%d\n",
               W, WRAP, SINGLE, pmin, pmax, target, iters, temp, ns);
        for (int si = 0; si < ns; si++) {
            uint64_t cw = seeds[si].wm, cb = seeds[si].bm;
            int cf;
            if (!valid_root(cw, cb)) {
                pos_str(buf, cw, cb); printf("#seed %d invalid as a root: %s\n", si, buf); continue;
            }
            { Value v = solve(cw, cb, 0, 0); cf = fitness(v, target); }
            int bestf = cf;
            for (long it = 0; it < iters; it++) {
                uint64_t nw_ = cw, nb_ = cb;
                int n = __builtin_popcountll(cw) + __builtin_popcountll(cb);
                int kind = (int)(rnd() % 10);
                int white = (rnd() & 1);
                uint64_t *mine = white ? &nw_ : &nb_;
                int rlo = white ? 2 : 3, rhi = white ? 6 : 7;
                if (kind < 6) {            /* relocate */
                    int cnt = __builtin_popcountll(*mine); if (!cnt) continue;
                    int pick = (int)(rnd() % cnt); uint64_t m = *mine;
                    while (pick--) m &= m - 1;
                    *mine &= ~(m & -m);
                    int f = (int)(rnd() % W), r = rlo + (int)(rnd() % (rhi - rlo + 1));
                    if (rnd() % 2) {   /* local move: stay near the old square */
                        int s = __builtin_ctzll(m); f = FILEOF(s) + (int)(rnd() % 3) - 1; r = RANKOF(s) + (int)(rnd() % 3) - 1;
                        if (WRAP) f = (f + W) % W;
                        if (f < 0 || f >= W || r < rlo || r > rhi) continue;
                    }
                    *mine |= B(f, r);
                } else if (kind < 8) {     /* add */
                    if (n >= pmax) continue;
                    int f = (int)(rnd() % W), r = rlo + (int)(rnd() % (rhi - rlo + 1));
                    *mine |= B(f, r);
                } else {                    /* remove */
                    if (n <= pmin) continue;
                    int cnt = __builtin_popcountll(*mine); if (cnt <= 1) continue;
                    int pick = (int)(rnd() % cnt); uint64_t m = *mine;
                    while (pick--) m &= m - 1;
                    *mine &= ~(m & -m);
                }
                if (nw_ == cw && nb_ == cb) continue;
                { int n2 = __builtin_popcountll(nw_) + __builtin_popcountll(nb_); if (n2 < pmin || n2 > pmax) continue; }
                if (!valid_root(nw_, nb_)) continue;
                Value v = solve(nw_, nb_, 0, 0);
                int nf = fitness(v, target);
                if (nimber_of(v) == target) {
                    pos_str(buf, nw_, nb_);
                    printf("FOUND\t%s\t%d\t%c\t%d\n", buf, __builtin_popcountll(nw_) + __builtin_popcountll(nb_), outcome_of(v), nimber_of(v));
                    fflush(stdout); found++;
                }
                double d = nf - cf;
                if (d <= 0 || (double)(rnd() % 1000000) / 1e6 < exp(-d / temp)) {
                    cw = nw_; cb = nb_; cf = nf;
                    if (cf < bestf) { bestf = cf; }
                }
                if ((it + 1) % 20000 == 0) {
                    pos_str(buf, cw, cb);
                    fprintf(stderr, "seed %d it %ld cur_f=%d best_f=%d states=%llu cur=%s\n", si, it + 1, cf, bestf,
                            (unsigned long long)tcount, buf);
                }
            }
        }
        printf("#search done found=%ld\n", found);
        return 0;
    }

    if (nw < 1 || nb < 1) { fprintf(stderr, "need --nw and --nb\n"); return 2; }
    clock_t t0 = clock();
    enum_roots(nw, nb, nw + nb);
    fprintf(stderr, "W=%d wrap=%d single=%d colsym=%d split=%d+%d chunk=%d/%d roots=%d enum_cpu=%.1fs\n", W, WRAP, SINGLE, COLSYM,
            nw, nb, CHUNK_I, CHUNK_N, nroots, (double)(clock() - t0) / CLOCKS_PER_SEC);
    if (count_only) { printf("roots\t%d\n", nroots); return 0; }
    tab_init(1u << 18);
    long hist_nim[KMAX + 2] = {0}; long hist_out[4] = {0};
    printf("#position\twidth\tn\toutcome\tnimber   (setting %s/%s%s, hits = nimber>=2)\n", rname[RACE], EPON ? "epon" : "epoff", AWARE ? "/aware" : "");
    for (int i = 0; i < nroots; i++) {
        Value v = solve(roots[i].wm, roots[i].bm, 0, 0);
        char o = outcome_of(v); int nim = nimber_of(v);
        hist_out[o == 'L' ? 0 : o == 'R' ? 1 : o == 'N' ? 2 : 3]++;
        hist_nim[nim < 0 ? KMAX : nim]++;
        if (nim >= 2) {
            pos_str(buf, roots[i].wm, roots[i].bm);
            printf("%s\t%d\t%d\t%c\t%d\n", buf, W, roots[i].n, o, nim);
            fflush(stdout);
        }
    }
    printf("#summary roots=%d states=%llu L=%ld R=%ld N=%ld P=%ld", nroots, (unsigned long long)tcount,
           hist_out[0], hist_out[1], hist_out[2], hist_out[3]);
    for (int q = 0; q < KMAX; q++) if (hist_nim[q]) printf(" nim%d=%ld", q, hist_nim[q]);
    printf(" cpu=%.1fs\n", (double)(clock() - t0) / CLOCKS_PER_SEC);
    return 0;
}
