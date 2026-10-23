/* h4.c -- T49 (*4 hunt) tool.  Solver core (masks, passed test, race distance, memo table, gen, child_mask, solve) is the
 * unchanged core of research/star26_rings/frontier_split1_fixed2.c via research/star3_single/s3.c; setting 2 = default
 * (count race rule, e.p. on, e.p.-aware passed test).  Value = (WL, WR): bit k of WL / WR = Left / Right wins G+*k moving first.
 * G = *q  iff both bits are clear at q and set at every other k < 8 ("nimber"); "near-*q" = exactly one of k = 0..7 is not an N-position.
 * Added in this directory:
 *   (scan)   --nw --nb --single [--colsym] [--chunk i n] [--scan-mex]   exhaustive single-component roots; table reset at 50% load
 *   --extend FILE --k K [--newonly] [--rot N0] [--maxperfile m]       seeds plus up to K extra pawns (exhaustive), widths <= 8
 *   --pred FILE --pdepth d        positions d reverse moves before the seeds, with the direct-children mex
 *   --minimize FILE               greedy removal of 1-2 pawns keeping the outcome masks
 *   --children FILE               list the children of a root with their nimber codes
 *   --anneal FILE [--score-mex]   annealing over positions (nimber-aware score)
 *   --combine A B                 two cores side by side with overlap 0..2
 *   --duel                        every file holds exactly one W and one B pawn (W below B), 15 options per file
 *   --eval FILE [--evalbudget N]  evaluate listed positions, optional node budget
 * Build: cc -O2 -o h4 h4.c -lm
 */
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
#include <setjmp.h>
static jmp_buf g_jb; static uint64_t g_budget = 0, g_calls = 0;

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
static int solve_budget_fwd(uint64_t wm, uint64_t bm, Value *out);

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
    if (g_budget && ++g_calls > g_budget) longjmp(g_jb, 1);
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


/* ------------------------------------------------------------------ star4_hunt additions */
static int prefixN(Value v) {           /* number of leading heap sizes h with G+*h an N-position */
    int m = 0;
    while (m < KMAX && ((v.WL >> m) & 1) && ((v.WR >> m) & 1)) m++;
    return m;
}
static long ev_count = 0, hist_n[66], hist_m[66], hist_near[8]; static int NEAR_REPORT = 4;
static int SCAN_MEX = 0; static long hist_mex2[16], hist_mexmax[16];
static long REPORT_NIM = 3, REPORT_M = 4;
static int RESET_PCT = 50;
static void reset_if_big(void) {
    if (TAB_CAP && tcount * 100 >= TAB_CAP * RESET_PCT) { tab_init(1u << 18); }
}
/* evaluates, updates histograms, prints interesting ones; returns nimber */
static long budget_aborts = 0;
static int visit(uint64_t wm, uint64_t bm, const char *tag, int force) {
    Value v;
    if (g_budget) { if (!solve_budget_fwd(wm, bm, &v)) { budget_aborts++; return -2; } }
    else v = solve(wm, bm, 0, 0);
    int nim = nimber_of(v), m = prefixN(v);
    ev_count++;
    hist_n[nim < 0 ? 65 : nim]++;
    hist_m[m > 64 ? 64 : m]++;
    { /* near-nimber: exactly one non-N entry among h = 0..7 */
        int cnt = 0, at = -1;
        for (int h = 0; h < 8; h++) if (!(((v.WL >> h) & 1) && ((v.WR >> h) & 1))) { cnt++; at = h; }
        if (cnt == 1) { hist_near[at]++; if (at >= NEAR_REPORT && nim < 0) {
            char buf[1024], ob[80]; pos_str(buf, wm, bm);
            printf("NEAR%d\t%s\t%d\t%c\t%s\t%s\n", at, buf, __builtin_popcountll(wm) + __builtin_popcountll(bm), outcome_of(v), tag, ostr(v, 10, ob)); fflush(stdout); } }
    }
    if (force || nim >= REPORT_NIM || m >= REPORT_M) {
        char buf[1024], ob[80];
        pos_str(buf, wm, bm);
        printf("%s\t%s\t%d\t%c\tnim=%d\tm=%d\t%s\n", tag, buf, __builtin_popcountll(wm) + __builtin_popcountll(bm),
               outcome_of(v), nim, m, ostr(v, 10, ob));
        fflush(stdout);
    }
    return nim;
}

/* ------------------------------------------------------------------ children / mex fitness */
typedef struct { uint64_t wm, bm, ep3, ep6; } St;
static int root_children(uint64_t wm, uint64_t bm, int white, St *out) {
    int n = 0;
    uint64_t occ = wm | bm, mine = white ? wm : bm, theirs = white ? bm : wm;
    int d = white ? 1 : -1, start = white ? 2 : 7;
    for (uint64_t m = mine; m; m &= m - 1) {
        int s = __builtin_ctzll(m), f = FILEOF(s), r = RANKOF(s), r1 = r + d;
        if (r1 < 1 || r1 > 8) continue;
        uint64_t rest = mine & ~B(f, r);
        if (!(occ & B(f, r1))) {
            uint64_t nm = rest | B(f, r1);
            out[n++] = (St){white ? nm : theirs, white ? theirs : nm, 0, 0};
            int r2 = r + 2 * d;
            if (r == start && !(occ & B(f, r2))) {
                uint64_t nm2 = rest | B(f, r2), c3 = 0, c6 = 0;
                if (EPON && has_ep_capturer(theirs, f, r2)) { if (white) c3 |= B(f, r1); else c6 |= B(f, r1); }
                out[n++] = (St){white ? nm2 : theirs, white ? theirs : nm2, c3, c6};
            }
        }
        for (int sd = -1; sd <= 1; sd += 2) {
            int g = f + sd;
            if (WRAP) g = (g + W) % W; else if (g < 0 || g >= W) continue;
            if (theirs & B(g, r1)) {
                uint64_t nm = rest | B(g, r1), nt = theirs & ~B(g, r1);
                out[n++] = (St){white ? nm : nt, white ? nt : nm, 0, 0};
            }
        }
    }
    return n;
}
/* code of a child from the mover's point of view: >=0 nimber, -1 other, -2 mover wins at once, -3 mover loses at once */
static int child_code(St c, int white) {
    int pw = passedW(c.wm, c.bm, c.ep3, c.ep6), pb = passedB(c.wm, c.bm, c.ep3, c.ep6);
    if (pw && pb) {
        int winner_white;
        if (RACE == 1) winner_white = white; else if (RACE == 2) winner_white = !white;
        else { int dm = dist(c.wm, c.bm, c.ep3, c.ep6, white), dop = dist(c.wm, c.bm, c.ep3, c.ep6, !white);
               winner_white = (dop <= dm) ? !white : white; }
        return (winner_white == white) ? -2 : -3;
    }
    if (pw) return white ? -2 : -3;
    if (pb) return white ? -3 : -2;
    Value v = solve(c.wm, c.bm, c.ep3, c.ep6);
    return nimber_of(v);
}
typedef struct { int mexL, mexR, nL, nR, winL, winR, nimL, nimR; uint64_t setL, setR; } MexInfo;
static MexInfo mexinfo(uint64_t wm, uint64_t bm) {
    MexInfo mi; memset(&mi, 0, sizeof mi);
    St ch[256];
    for (int white = 1; white >= 0; white--) {
        int n = root_children(wm, bm, white, ch);
        uint64_t set = 0; int win = 0, nn = 0;
        for (int i = 0; i < n; i++) {
            int c = child_code(ch[i], white);
            if (c >= 0 && c < 64) { set |= UINT64_C(1) << c; nn++; }
            else if (c == -2) win = 1;
        }
        int mex = 0; while ((set >> mex) & 1) mex++;
        if (white) { mi.mexL = mex; mi.nL = n; mi.winL = win; mi.nimL = nn; mi.setL = set; }
        else       { mi.mexR = mex; mi.nR = n; mi.winR = win; mi.nimR = nn; mi.setR = set; }
    }
    return mi;
}

/* ------------------------------------------------------------------ predecessors */
typedef struct { uint64_t wm, bm; } Pr;
static int gen_preds(uint64_t wm, uint64_t bm, Pr *out, int cap) {
    int n = 0;
    for (int white = 1; white >= 0; white--) {
        uint64_t mine = white ? wm : bm, theirs = white ? bm : wm;
        int d = white ? 1 : -1, start = white ? 2 : 7;
        int lo = white ? 2 : 3, hi = white ? 6 : 7;          /* allowed ranks for this colour */
        int tlo = white ? 3 : 2, thi = white ? 7 : 6;        /* allowed ranks for the other colour */
        uint64_t occ = wm | bm;
        for (uint64_t m = mine; m; m &= m - 1) {
            int s = __builtin_ctzll(m), f = FILEOF(s), r = RANKOF(s);
            uint64_t rest = mine & ~B(f, r);
            int r0 = r - d;
            if (r0 >= lo && r0 <= hi) {
                if (!(occ & B(f, r0))) {
                    uint64_t nm = rest | B(f, r0);
                    if (n < cap) out[n++] = (Pr){white ? nm : theirs, white ? theirs : nm};
                }
                /* double-step reverse */
                int r00 = r - 2 * d;
                if (r00 == start && !(occ & B(f, r0)) && !(occ & B(f, r00))) {
                    uint64_t nm = rest | B(f, r00);
                    if (n < cap) out[n++] = (Pr){white ? nm : theirs, white ? theirs : nm};
                }
                /* capture reverse */
                if (r >= tlo && r <= thi) {
                    for (int sd = -1; sd <= 1; sd += 2) {
                        int g = f + sd;
                        if (WRAP) g = (g + W) % W; else if (g < 0 || g >= W) continue;
                        if (occ & B(g, r0)) continue;
                        uint64_t nm = rest | B(g, r0), nt = theirs | B(f, r);
                        if (n < cap) out[n++] = (Pr){white ? nm : nt, white ? nt : nm};
                    }
                }
            }
        }
    }
    return n;
}

static void pred_mode(const char *seedfile, int depth, int mexthr) {
    Root seeds[4096]; int ns = 0;
    FILE *fp = fopen(seedfile, "r"); if (!fp) { perror("seeds"); exit(1); }
    char line[2048];
    while (fgets(line, sizeof line, fp) && ns < 4096) {
        if (line[0] == '#' || strlen(line) < 5) continue;
        uint64_t wm, bm; parse_pos(line, &wm, &bm);
        seeds[ns++] = (Root){wm, bm, 0};
    }
    fclose(fp);
    tab_init(1u << 18);
    hs_init(1u << 24);
    printf("#pred width=%d wrap=%d depth=%d seeds=%d\n", W, WRAP, depth, ns);
    long hist_mex[16] = {0};
    for (int si = 0; si < ns; si++) {
        static Pr cur[2000000]; static Pr nxt[2000000];
        int nc = 1; cur[0] = (Pr){seeds[si].wm, seeds[si].bm};
        hs_insert(cur[0].wm, cur[0].bm);
        long nev = 0;
        for (int lev = 1; lev <= depth; lev++) {
            int nn = 0;
            for (int ci = 0; ci < nc; ci++) {
                Pr pr[512];
                int k = gen_preds(cur[ci].wm, cur[ci].bm, pr, 512);
                for (int j = 0; j < k; j++) {
                    if (!hs_insert(pr[j].wm, pr[j].bm)) continue;
                    if (!valid_root(pr[j].wm, pr[j].bm)) continue;
                    if (nn < 2000000) nxt[nn++] = pr[j];
                    reset_if_big();
                    Value v = solve(pr[j].wm, pr[j].bm, 0, 0);
                    int nim = nimber_of(v);
                    MexInfo mi = mexinfo(pr[j].wm, pr[j].bm);
                    int mm = (mi.winL || mi.winR) ? -1 : (mi.mexL < mi.mexR ? mi.mexL : mi.mexR);
                    hist_mex[mm < 0 ? 0 : (mm + 1 > 15 ? 15 : mm + 1)]++;
                    nev++;
                    ev_count++;
                    hist_n[nim < 0 ? 65 : nim]++;
                    if (nim >= REPORT_NIM || mm >= mexthr) {
                        char buf[1024], ob[80]; pos_str(buf, pr[j].wm, pr[j].bm);
                        printf("PRED%d.%d\t%s\t%d\t%c\tnim=%d\tmex=%d,%d\tsetL=%llx\tsetR=%llx\t%s\n", si, lev, buf,
                               __builtin_popcountll(pr[j].wm) + __builtin_popcountll(pr[j].bm), outcome_of(v), nim,
                               mi.mexL, mi.mexR, (unsigned long long)mi.setL, (unsigned long long)mi.setR, ostr(v, 10, ob));
                        fflush(stdout);
                    }
                }
            }
            memcpy(cur, nxt, (size_t)nn * sizeof(Pr)); nc = nn;
        }
        fprintf(stderr, "seed %d: evaluated %ld preds\n", si, nev);
    }
    printf("#pred done evals=%ld\n#hist_nim", ev_count);
    for (int q = 0; q < 66; q++) if (hist_n[q]) printf(" nim%d=%ld", q, hist_n[q]);
    printf("\n#hist_minmex(-1 => a winning child exists) ");
    for (int q = 0; q < 16; q++) if (hist_mex[q]) printf(" m%d=%ld", q - 1, hist_mex[q]);
    printf("\n");
}

/* ------------------------------------------------------------------ minimisation */
static void minimize_mode(const char *seedfile) {
    FILE *fp = fopen(seedfile, "r"); if (!fp) { perror("seeds"); exit(1); }
    char line[2048];
    tab_init(1u << 18);
    printf("#minimize width=%d wrap=%d\n", W, WRAP);
    while (fgets(line, sizeof line, fp)) {
        if (line[0] == '#' || strlen(line) < 5) continue;
        uint64_t wm, bm; parse_pos(line, &wm, &bm);
        if (!valid_root(wm, bm) && !SINGLE) { /* still evaluate */ }
        Value v0 = solve(wm, bm, 0, 0);
        int changed = 1;
        while (changed) {
            changed = 0;
            for (int col = 0; col < 2 && !changed; col++) {
                uint64_t mine = col ? bm : wm;
                for (uint64_t m = mine; m && !changed; m &= m - 1) {
                    uint64_t bit = m & -m;
                    uint64_t nw2 = col ? wm : wm & ~bit, nb2 = col ? bm & ~bit : bm;
                    if (!(nw2 | nb2)) continue;
                    if (passedW(nw2, nb2, 0, 0) || passedB(nw2, nb2, 0, 0)) continue;
                    reset_if_big();
                    Value v = solve(nw2, nb2, 0, 0);
                    if (v.WL == v0.WL && v.WR == v0.WR) { wm = nw2; bm = nb2; changed = 1; }
                }
            }
            if (!changed) {  /* try removing two pawns */
                uint64_t all = wm | bm;
                for (uint64_t m1 = all; m1 && !changed; m1 &= m1 - 1) {
                    uint64_t b1 = m1 & -m1;
                    for (uint64_t m2 = m1 & (m1 - 1); m2 && !changed; m2 &= m2 - 1) {
                        uint64_t b2_ = m2 & -m2;
                        uint64_t nw2 = wm & ~(b1 | b2_), nb2 = bm & ~(b1 | b2_);
                        if (!(nw2 | nb2)) continue;
                        if (passedW(nw2, nb2, 0, 0) || passedB(nw2, nb2, 0, 0)) continue;
                        reset_if_big();
                        Value v = solve(nw2, nb2, 0, 0);
                        if (v.WL == v0.WL && v.WR == v0.WR) { wm = nw2; bm = nb2; changed = 1; }
                    }
                }
            }
        }
        char buf[1024], ob[80]; pos_str(buf, wm, bm);
        printf("%s\t%d\t%c\t%d\t%s\n", buf, __builtin_popcountll(wm) + __builtin_popcountll(bm), outcome_of(v0), nimber_of(v0), ostr(v0, 10, ob));
        fflush(stdout);
    }
    fclose(fp);
}

static int ROT_N0 = 0;
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
static int max_file(uint64_t m) { int mx = -1; for (; m; m &= m - 1) { int f = FILEOF(__builtin_ctzll(m)); if (f > mx) mx = f; } return mx; }
static int min_file(uint64_t m) { int mn = 99; for (; m; m &= m - 1) { int f = FILEOF(__builtin_ctzll(m)); if (f < mn) mn = f; } return mn; }

static int xsq_n; static uint64_t xsq_bit[128]; static int xsq_white[128];
static int XPMAX = 99, ASSUME_SINGLE = 1;
static long ext_cand = 0, ext_skip = 0; static int NEWONLY = 0, core_lo = 0, core_hi = 0, MAXPERFILE = 99;
static long ext_seq = 0;
#define CH_I CHUNK_I
#define CH_N CHUNK_N

static void ext_rec(uint64_t wm, uint64_t bm, int start, int left, const char *tag) {
    /* evaluate current (if it has been extended at least once handled by caller) */
    for (int i = start; i < xsq_n; i++) {
        uint64_t bit = xsq_bit[i];
        if ((wm | bm) & bit) continue;
        if (NEWONLY) { int ff = FILEOF(__builtin_ctzll(bit)); if (ff >= core_lo && ff <= core_hi) continue; }
        if (MAXPERFILE < 99) { int ff = FILEOF(__builtin_ctzll(bit)); if (__builtin_popcountll((wm | bm) & filemask[ff]) >= MAXPERFILE) continue; }
        uint64_t nw2 = xsq_white[i] ? wm | bit : wm, nb2 = xsq_white[i] ? bm : bm | bit;
        if (__builtin_popcountll(nw2) + __builtin_popcountll(nb2) > XPMAX) continue;
        /* chunking on the sequence number of candidate (deterministic order) */
        ext_seq++;
        if (CH_N > 1 && (ext_seq % CH_N) != CH_I) { if (left > 1) ext_rec(nw2, nb2, i + 1, left - 1, tag); continue; }
        if (valid_root(nw2, nb2) && hs_insert(nw2, nb2)) {
            if (hs_cnt > 12000000) hs_init(1u << 24);
            reset_if_big();
            visit(nw2, nb2, tag, 0);
            ext_cand++;
        } else ext_skip++;
        if (left > 1) ext_rec(nw2, nb2, i + 1, left - 1, tag);
    }
}

static void extend_mode(const char *seedfile, int K) {
    Root seeds[4096]; int ns = 0;
    FILE *fp = fopen(seedfile, "r"); if (!fp) { perror("seeds"); exit(1); }
    char line[2048];
    while (fgets(line, sizeof line, fp) && ns < 4096) {
        if (line[0] == '#' || strlen(line) < 5) continue;
        uint64_t wm, bm; parse_pos(line, &wm, &bm);
        seeds[ns++] = (Root){wm, bm, 0};
    }
    fclose(fp);
    xsq_n = 0;
    for (int f = 0; f < W; f++) {
        for (int r = 2; r <= 6; r++) { xsq_bit[xsq_n] = B(f, r); xsq_white[xsq_n++] = 1; }
        for (int r = 3; r <= 7; r++) { xsq_bit[xsq_n] = B(f, r); xsq_white[xsq_n++] = 0; }
    }
    tab_init(1u << 18);
    hs_init(1u << 24);
    printf("#extend width=%d wrap=%d K=%d seeds=%d pmax=%d chunk=%d/%d\n", W, WRAP, K, ns, XPMAX, CH_I, CH_N);
    for (int si = 0; si < ns; si++) {
        uint64_t sw = seeds[si].wm, sb = seeds[si].bm;
        int lo = min_file(sw | sb), hi = max_file(sw | sb);
        int span = hi - lo + 1;
        int nrot = (ROT_N0 > 0 && WRAP) ? ROT_N0 : 0;
        for (int off = 0; nrot ? off < nrot : off + span <= W; off++) {
            if (WRAP && !nrot && off > 0) break;  /* rings: rotations are equivalent */
            uint64_t w2, b2;
            if (nrot) { w2 = rotate_files(sw, off, ROT_N0); b2 = rotate_files(sb, off, ROT_N0); }
            else { w2 = shift_files(sw, off - lo); b2 = shift_files(sb, off - lo); }
            char tag[64]; sprintf(tag, "X%d.%d", si, off);
            if (nrot) { core_lo = 0; core_hi = ROT_N0 - 1; } else { core_lo = off; core_hi = off + span - 1; }
            long c0 = ext_cand;
            if (hs_insert(w2, b2) && valid_root(w2, b2)) visit(w2, b2, tag, 0);
            ext_rec(w2, b2, 0, K, tag);
            fprintf(stderr, "seed %d off %d: new candidates %ld (total evals %ld, states %llu)\n", si, off, ext_cand - c0, ev_count, (unsigned long long)tcount);
        }
    }
    printf("#extend done evals=%ld skipped=%ld budget_aborts=%ld\n", ev_count, ext_skip, budget_aborts);
    printf("#hist_nim");
    for (int q = 0; q < 66; q++) if (hist_n[q]) printf(" nim%d=%ld", q, hist_n[q]);
    printf("\n#hist_near"); for (int q = 0; q < 8; q++) printf(" n%d=%ld", q, hist_near[q]);
    printf("\n#hist_m");
    for (int q = 0; q < 66; q++) if (hist_m[q]) printf(" m%d=%ld", q, hist_m[q]);
    printf("\n");
}

/* ------------------------------------------------------------------ combine two cores */
static int solve_budget(uint64_t wm, uint64_t bm, Value *out) {
    g_calls = 0;
    if (setjmp(g_jb)) return 0;
    *out = solve(wm, bm, 0, 0);
    return 1;
}
static int solve_budget_fwd(uint64_t wm, uint64_t bm, Value *out) { return solve_budget(wm, bm, out); }
static uint64_t colour_rev(uint64_t m) { return flip_ranks(m); }
static void read_pos_file(const char *fn, Root *arr, int *n, int cap) {
    FILE *fp = fopen(fn, "r"); if (!fp) { perror(fn); exit(1); }
    char line[2048]; *n = 0;
    int savedW = W; W = 8;
    while (fgets(line, sizeof line, fp) && *n < cap) {
        if (line[0] == '#' || strlen(line) < 5) continue;
        uint64_t wm, bm; parse_pos(line, &wm, &bm);
        arr[(*n)++] = (Root){wm, bm, 0};
    }
    W = savedW;
    fclose(fp);
}
static void norm_left(uint64_t *w, uint64_t *b, int *span) {
    int lo = min_file(*w | *b), hi = max_file(*w | *b);
    *w = shift_files(*w, -lo); *b = shift_files(*b, -lo); *span = hi - lo + 1;
}
static void mirror_core(uint64_t *w, uint64_t *b, int span) {
    uint64_t ow = 0, ob = 0;
    for (uint64_t m = *w; m; m &= m - 1) { int s = __builtin_ctzll(m); ow |= B(span - 1 - FILEOF(s), RANKOF(s)); }
    for (uint64_t m = *b; m; m &= m - 1) { int s = __builtin_ctzll(m); ob |= B(span - 1 - FILEOF(s), RANKOF(s)); }
    *w = ow; *b = ob;
}
static int MAXP = 16; static uint64_t CBUDGET = 20000000;
static void combine_mode(const char *fa, const char *fb) {
    static Root A[512], Bc[512]; int na, nbn;
    read_pos_file(fa, A, &na, 512); read_pos_file(fb, Bc, &nbn, 512);
    tab_init(1u << 18); hs_init(1u << 22);
    printf("#combine width=%d A=%s(%d) B=%s(%d) maxp=%d budget=%llu\n", W, fa, na, fb, nbn, MAXP, (unsigned long long)CBUDGET);
    long evals = 0, aborted = 0, dev = 0, skipped = 0;
    long hist[66] = {0};
    for (int ia = 0; ia < na; ia++) for (int ib = 0; ib < nbn; ib++) {
        for (int ta = 0; ta < 4; ta++) for (int tb = 0; tb < 4; tb++) {
            uint64_t aw = A[ia].wm, ab = A[ia].bm, bw = Bc[ib].wm, bb = Bc[ib].bm; int sa, sb;
            norm_left(&aw, &ab, &sa); norm_left(&bw, &bb, &sb);
            if (ta & 1) mirror_core(&aw, &ab, sa);
            if (ta & 2) { uint64_t t = colour_rev(ab); ab = colour_rev(aw); aw = t; }
            if (tb & 1) mirror_core(&bw, &bb, sb);
            if (tb & 2) { uint64_t t = colour_rev(bb); bb = colour_rev(bw); bw = t; }
            /* nimbers of the parts */
            Value va, vb; int na_ = -1, nb_ = -1;
            if (solve_budget(aw, ab, &va)) na_ = nimber_of(va);
            if (solve_budget(bw, bb, &vb)) nb_ = nimber_of(vb);
            for (int ov = 0; ov <= 2; ov++) {
                int off = sa - ov;
                if (off < 0 || off + sb > W) continue;
                uint64_t w2 = aw | shift_files(bw, off), b2 = ab | shift_files(bb, off);
                if ((aw & shift_files(bb, off)) || (ab & shift_files(bw, off))) continue;
                if (aw & ab) continue;
                if (__builtin_popcountll(w2) + __builtin_popcountll(b2) > MAXP) { skipped++; continue; }
                if (!valid_root(w2, b2)) { skipped++; continue; }
                if (!hs_insert(w2, b2)) continue;
                if (hs_cnt > 3000000) hs_init(1u << 22);
                reset_if_big();
                Value v;
                if (!solve_budget(w2, b2, &v)) { aborted++; continue; }
                int nim = nimber_of(v); evals++;
                hist[nim < 0 ? 65 : nim]++;
                int expect = (na_ >= 0 && nb_ >= 0) ? (na_ ^ nb_) : -9;
                if (nim >= 3 || (nim >= 0 && nim != expect)) {
                    char buf[1024], ob[80]; pos_str(buf, w2, b2);
                    printf("COMB%d.%d.%d.%d.ov%d\t%s\t%d\t%c\tnim=%d\texpect=%d(%d^%d)\t%s\n", ia, ib, ta, tb, ov, buf,
                           __builtin_popcountll(w2) + __builtin_popcountll(b2), outcome_of(v), nim, expect, na_, nb_, ostr(v, 10, ob));
                    fflush(stdout); dev++;
                }
            }
        }
        fprintf(stderr, "A%d B%d done: evals=%ld aborted=%ld skipped=%ld dev=%ld\n", ia, ib, evals, aborted, skipped, dev);
    }
    printf("#combine done evals=%ld aborted=%ld skipped=%ld deviations=%ld\n#hist_nim", evals, aborted, skipped, dev);
    for (int q = 0; q < 66; q++) if (hist[q]) printf(" nim%d=%ld", q, hist[q]);
    printf("\n");
}

/* ------------------------------------------------------------------ annealing over positions with a nimber-aware score */
static int SCORE_MEX = 0; static uint64_t cur_wm, cur_bm;
static int score_of(Value v, int *nim_out, int *near_out) {
    if (SCORE_MEX) {
        MexInfo mi = mexinfo(cur_wm, cur_bm);
        int nim = nimber_of(v);
        int mm = mi.mexL < mi.mexR ? mi.mexL : mi.mexR;
        int sc = 20 * mm + __builtin_popcountll(mi.setL) + __builtin_popcountll(mi.setR);
        if (mi.winL || mi.winR) sc -= 40;
        if (nim >= 0 && nim < 8) sc += 30 + 10 * nim;
        int cnt = 0, at = -1;
        for (int h = 0; h < 8; h++) if (!(((v.WL >> h) & 1) && ((v.WR >> h) & 1))) { cnt++; at = h; }
        *nim_out = nim; *near_out = (cnt == 1) ? at : -1;
        if (sc < 0) sc = 0;
        return sc;
    }
    int D = 0, cnt = 0, at = -1;
    for (int h = 0; h < 8; h++) if (!(((v.WL >> h) & 1) && ((v.WR >> h) & 1))) { cnt++; at = h; }
    (void)D;
    int nim = nimber_of(v);
    *nim_out = nim; *near_out = (cnt == 1) ? at : -1;
    if (nim >= 0 && nim < 8) return 40 + 10 * nim;
    if (cnt == 1) return 25 + 5 * at;
    if (cnt == 2) return 12;
    if (cnt == 0) return 0;
    return 5;
}
static void anneal_mode(const char *seedfile, long iters, double temp, int pmin, int pmax, int nchains_per_seed) {
    Root seeds[1024]; int ns = 0;
    FILE *fp = fopen(seedfile, "r"); if (!fp) { perror("seeds"); exit(1); }
    char line[2048];
    while (fgets(line, sizeof line, fp) && ns < 1024) {
        if (line[0] == '#' || strlen(line) < 5) continue;
        uint64_t wm, bm; parse_pos(line, &wm, &bm);
        seeds[ns++] = (Root){wm, bm, 0};
    }
    fclose(fp);
    tab_init(1u << 18);
    hs_init(1u << 22);
    printf("#anneal width=%d wrap=%d single=%d iters=%ld temp=%.1f pmin=%d pmax=%d seeds=%d chains=%d\n", W, WRAP, SINGLE, iters, temp, pmin, pmax, ns, nchains_per_seed);
    long hist_nim[66] = {0}, hist_near[8] = {0};
    long total = 0;
    int bestscore_all = 0;
    for (int si = 0; si < ns; si++) for (int ch = 0; ch < nchains_per_seed; ch++) {
        uint64_t cw = seeds[si].wm, cb = seeds[si].bm;
        if (!valid_root(cw, cb)) continue;
        int nim, nr;
        Value v = solve(cw, cb, 0, 0);
        cur_wm = cw; cur_bm = cb;
        int cs = score_of(v, &nim, &nr);
        for (long it = 0; it < iters; it++) {
            uint64_t nw_ = cw, nb_ = cb;
            int n = __builtin_popcountll(cw) + __builtin_popcountll(cb);
            int kind = (int)(rnd() % 12);
            int white = (rnd() & 1);
            uint64_t *mine = white ? &nw_ : &nb_;
            int rlo = white ? 2 : 3, rhi = white ? 6 : 7;
            int cnt = __builtin_popcountll(*mine);
            if (kind < 6) {                  /* nudge a pawn by one step in some direction */
                if (!cnt) continue;
                int pick = (int)(rnd() % cnt); uint64_t m = *mine;
                while (pick--) m &= m - 1;
                int s = __builtin_ctzll(m); int f = FILEOF(s) + (int)(rnd() % 3) - 1, r = RANKOF(s) + (int)(rnd() % 3) - 1;
                if (WRAP) f = (f + W) % W;
                if (f < 0 || f >= W || r < rlo || r > rhi) continue;
                *mine &= ~(m & -m); *mine |= B(f, r);
            } else if (kind < 7) {           /* relocate anywhere */
                if (!cnt) continue;
                int pick = (int)(rnd() % cnt); uint64_t m = *mine;
                while (pick--) m &= m - 1;
                *mine &= ~(m & -m);
                int f = (int)(rnd() % W), r = rlo + (int)(rnd() % (rhi - rlo + 1));
                *mine |= B(f, r);
            } else if (kind < 9) {           /* add one pawn */
                if (n >= pmax) continue;
                int f = (int)(rnd() % W), r = rlo + (int)(rnd() % (rhi - rlo + 1));
                *mine |= B(f, r);
            } else if (kind < 10) {          /* add a W/B pair on one file */
                if (n + 2 > pmax) continue;
                int f = (int)(rnd() % W), r = 2 + (int)(rnd() % 4), gap = 1 + 2 * (int)(rnd() % 2);
                if (r + gap + 1 > 7) continue;
                nw_ |= B(f, r); nb_ |= B(f, r + gap + 1);
            } else {                          /* remove a pawn */
                if (n <= pmin || cnt <= 1) continue;
                int pick = (int)(rnd() % cnt); uint64_t m = *mine;
                while (pick--) m &= m - 1;
                *mine &= ~(m & -m);
            }
            if (nw_ == cw && nb_ == cb) continue;
            { int n2 = __builtin_popcountll(nw_) + __builtin_popcountll(nb_); if (n2 < pmin || n2 > pmax) continue; }
            if (!valid_root(nw_, nb_)) continue;
            reset_if_big();
            int newfresh = hs_insert(nw_, nb_);
            if (hs_cnt > 3000000) hs_init(1u << 22);
            v = solve(nw_, nb_, 0, 0);
            int nim2, nr2;
            cur_wm = nw_; cur_bm = nb_;
            int ns_ = score_of(v, &nim2, &nr2);
            total++;
            if (newfresh) {
                hist_nim[nim2 < 0 ? 65 : nim2]++;
                if (nr2 >= 0) hist_near[nr2]++;
                if (nim2 >= 4 || (nr2 >= 4)) {
                    char buf[1024], ob[80]; pos_str(buf, nw_, nb_);
                    printf("HIT\t%s\t%d\t%c\tnim=%d\tnear=%d\t%s\n", buf, __builtin_popcountll(nw_) + __builtin_popcountll(nb_), outcome_of(v), nim2, nr2, ostr(v, 10, ob));
                    fflush(stdout);
                }
                if (nim2 == 3 || nr2 == 3) { /* log first sightings of 3-level objects compactly */
                    char buf[1024]; pos_str(buf, nw_, nb_);
                    printf("L3\t%s\t%d\tnim=%d\tnear=%d\n", buf, __builtin_popcountll(nw_) + __builtin_popcountll(nb_), nim2, nr2);
                }
            }
            if (ns_ > bestscore_all) bestscore_all = ns_;
            double d = ns_ - cs;
            if (d >= 0 || (double)(rnd() % 1000000) / 1e6 < exp(d / temp)) { cw = nw_; cb = nb_; cs = ns_; }
        }
        fprintf(stderr, "seed %d chain %d done: evals=%ld states=%llu\n", si, ch, total, (unsigned long long)tcount);
    }
    printf("#anneal done evals=%ld bestscore=%d\n#hist_nim", total, bestscore_all);
    for (int q = 0; q < 66; q++) if (hist_nim[q]) printf(" nim%d=%ld", q, hist_nim[q]);
    printf("\n#hist_near"); for (int q = 0; q < 8; q++) printf(" n%d=%ld", q, hist_near[q]);
    printf("\n");
}

/* ------------------------------------------------------------------ duel boards: every file has exactly one W and one B pawn (W below B) */
static void duel_mode(int chunk_i, int chunk_n) {
    int opts_r[64], opts_s[64], no = 0;
    for (int r = 2; r <= 6; r++) for (int s = 3; s <= 7; s++) if (s > r) { opts_r[no] = r; opts_s[no] = s; no++; }
    uint64_t total = 1; for (int f = 0; f < W; f++) total *= (uint64_t)no;
    tab_init(1u << 18);
    long hist_nim[66] = {0}; long done = 0;
    printf("#duel width=%d wrap=%d options/file=%d configs=%llu chunk=%d/%d\n", W, WRAP, no, (unsigned long long)total, chunk_i, chunk_n);
    for (uint64_t idx = 0; idx < total; idx++) {
        if (chunk_n > 1 && (idx % chunk_n) != (uint64_t)chunk_i) continue;
        uint64_t x = idx, wm = 0, bm = 0; int dig[8];
        for (int f = 0; f < W; f++) { dig[f] = (int)(x % no); x /= no; wm |= B(f, opts_r[dig[f]]); bm |= B(f, opts_s[dig[f]]); }
        /* mirror symmetry (flat) : keep only the lexicographically smaller of dig and its reverse */
        if (!WRAP) { int rev = 0; for (int f = 0; f < W; f++) { int a = dig[f], b = dig[W - 1 - f]; if (a != b) { rev = (b < a) ? 1 : 0; break; } } if (rev) continue; }
        if (passedW(wm, bm, 0, 0) || passedB(wm, bm, 0, 0)) continue;
        reset_if_big();
        Value v = solve(wm, bm, 0, 0);
        int nim = nimber_of(v); hist_nim[nim < 0 ? 65 : nim]++; done++;
        int cnt = 0, at = -1;
        for (int h = 0; h < 8; h++) if (!(((v.WL >> h) & 1) && ((v.WR >> h) & 1))) { cnt++; at = h; }
        if (nim >= 2 || (cnt == 1 && at >= 3)) {
            char buf[1024], ob[80]; pos_str(buf, wm, bm);
            printf("%s\t%d\t%c\tnim=%d\tnear=%d\t%s\n", buf, 2 * W, outcome_of(v), nim, cnt == 1 ? at : -1, ostr(v, 10, ob)); fflush(stdout);
        }
    }
    printf("#duel done roots=%ld", done);
    for (int q = 0; q < 66; q++) if (hist_nim[q]) printf(" nim%d=%ld", q, hist_nim[q]);
    printf("\n");
}

static void children_mode(const char *fn) {
    FILE *fp = fopen(fn, "r"); if (!fp) { perror(fn); exit(1); }
    char line[2048]; tab_init(1u << 18);
    while (fgets(line, sizeof line, fp)) {
        if (line[0] == '#' || strlen(line) < 5) continue;
        line[strcspn(line, "\r\n")] = 0;
        uint64_t wm, bm; parse_pos(line, &wm, &bm);
        char buf[1024]; pos_str(buf, wm, bm);
        Value v = solve(wm, bm, 0, 0);
        printf("ROOT %s nim=%d out=%c\n", buf, nimber_of(v), outcome_of(v));
        for (int white = 1; white >= 0; white--) {
            St ch[256]; int n = root_children(wm, bm, white, ch);
            for (int i = 0; i < n; i++) {
                int code = child_code(ch[i], white);
                char b2[1024]; pos_str(b2, ch[i].wm, ch[i].bm);
                char ob[80] = "";
                if (code >= -1) { Value cv = solve(ch[i].wm, ch[i].bm, ch[i].ep3, ch[i].ep6); ostr(cv, 8, ob); }
                printf("  %s -> %s%s code=%d %s\n", white ? "W" : "B", b2, ch[i].ep3 || ch[i].ep6 ? " (ep)" : "", code, ob);
            }
        }
    }
    fclose(fp);
}

int main(int argc, char **argv) {
    int nw = -1, nb = -1, width = -1, setting = 2, count_only = 0;
    const char *evalfile = NULL;
    int search = 0, pmin = 6, pmax = 11, target = 3;
    long iters = 100000; double temp = 1.0;
    const char *extfile = NULL; int extK = 2; const char *predfile = NULL; const char *chfile = NULL; int duel = 0; const char *annfile = NULL; int annchains = 1; const char *combA = NULL, *combB = NULL; const char *minfile = NULL; int preddepth = 1, mexthr = 4;
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
        else if (!strcmp(argv[i], "--extend") && i + 1 < argc) extfile = argv[++i];
        else if (!strcmp(argv[i], "--pred") && i + 1 < argc) predfile = argv[++i];
        else if (!strcmp(argv[i], "--scan-mex")) SCAN_MEX = 1;
        else if (!strcmp(argv[i], "--score-mex")) SCORE_MEX = 1;
        else if (!strcmp(argv[i], "--children") && i + 1 < argc) chfile = argv[++i];
        else if (!strcmp(argv[i], "--duel")) duel = 1;
        else if (!strcmp(argv[i], "--reset-pct") && i + 1 < argc) RESET_PCT = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--evalbudget") && i + 1 < argc) g_budget = (uint64_t)atoll(argv[++i]);
        else if (!strcmp(argv[i], "--newonly")) NEWONLY = 1;
        else if (!strcmp(argv[i], "--maxperfile") && i + 1 < argc) MAXPERFILE = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--anneal") && i + 1 < argc) annfile = argv[++i];
        else if (!strcmp(argv[i], "--chains") && i + 1 < argc) annchains = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--combine") && i + 2 < argc) { combA = argv[++i]; combB = argv[++i]; }
        else if (!strcmp(argv[i], "--maxp") && i + 1 < argc) MAXP = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--budget") && i + 1 < argc) CBUDGET = (uint64_t)atoll(argv[++i]);
        else if (!strcmp(argv[i], "--rot") && i + 1 < argc) ROT_N0 = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--minimize") && i + 1 < argc) minfile = argv[++i];
        else if (!strcmp(argv[i], "--near") && i + 1 < argc) NEAR_REPORT = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--pdepth") && i + 1 < argc) preddepth = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--mexthr") && i + 1 < argc) mexthr = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--k") && i + 1 < argc) extK = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--xpmax") && i + 1 < argc) XPMAX = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--rep-nim") && i + 1 < argc) REPORT_NIM = atol(argv[++i]);
        else if (!strcmp(argv[i], "--rep-m") && i + 1 < argc) REPORT_M = atol(argv[++i]);
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
            Value v;
            if (g_budget) { if (!solve_budget_fwd(wm, bm, &v)) { printf("%s\t%d\t%d\tBUDGET\n", buf, W, n); fflush(stdout); reset_if_big(); continue; } }
            else v = solve(wm, bm, 0, 0);
            printf("%s\t%d\t%d\t%c\t%d\t%s\n", buf, W, n, outcome_of(v), nimber_of(v), ostr(v, 8, ob));
            fflush(stdout);
        }
        fclose(fp);
        return 0;
    }

    if (extfile) { extend_mode(extfile, extK); return 0; }
    if (predfile) { pred_mode(predfile, preddepth, mexthr); return 0; }
    if (chfile) { children_mode(chfile); return 0; }
    if (duel) { duel_mode(CHUNK_I, CHUNK_N); return 0; }
    if (annfile) { anneal_mode(annfile, iters, temp, pmin, pmax, annchains); return 0; }
    if (combA) { g_budget = CBUDGET; combine_mode(combA, combB); return 0; }
    if (minfile) { minimize_mode(minfile); return 0; }
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
        reset_if_big();
        Value v = solve(roots[i].wm, roots[i].bm, 0, 0);
        char o = outcome_of(v); int nim = nimber_of(v);
        hist_out[o == 'L' ? 0 : o == 'R' ? 1 : o == 'N' ? 2 : 3]++;
        hist_nim[nim < 0 ? KMAX : nim]++;
        if (nim >= 2) {
            pos_str(buf, roots[i].wm, roots[i].bm);
            printf("%s\t%d\t%d\t%c\t%d\n", buf, W, roots[i].n, o, nim);
            fflush(stdout);
        }
        if (SCAN_MEX) {
            MexInfo mi = mexinfo(roots[i].wm, roots[i].bm);
            int mm = (mi.winL || mi.winR) ? -1 : (mi.mexL < mi.mexR ? mi.mexL : mi.mexR);
            hist_mex2[mm < 0 ? 0 : (mm + 1 > 15 ? 15 : mm + 1)]++;
            int mx = mi.mexL > mi.mexR ? mi.mexL : mi.mexR;
            hist_mexmax[mx > 15 ? 15 : mx]++;
            if (mm >= 3 && nim != 3) {
                pos_str(buf, roots[i].wm, roots[i].bm);
                printf("MEX%d\t%s\t%d\t%c\tnim=%d\tmexLR=%d,%d\n", mm, buf, roots[i].n, o, nim, mi.mexL, mi.mexR); fflush(stdout);
            }
        }
        { int cnt = 0, at = -1;
          for (int h = 0; h < 8; h++) if (!(((v.WL >> h) & 1) && ((v.WR >> h) & 1))) { cnt++; at = h; }
          if (cnt == 1) hist_near[at]++;
          if (cnt == 1 && at >= 3 && nim < 0) {
            char ob2[80]; pos_str(buf, roots[i].wm, roots[i].bm);
            printf("NEAR%d\t%s\t%d\t%c\t%s\n", at, buf, roots[i].n, o, ostr(v, 10, ob2)); fflush(stdout); } }
    }
    printf("#summary roots=%d states=%llu L=%ld R=%ld N=%ld P=%ld", nroots, (unsigned long long)tcount,
           hist_out[0], hist_out[1], hist_out[2], hist_out[3]);
    for (int q = 0; q < KMAX; q++) if (hist_nim[q]) printf(" nim%d=%ld", q, hist_nim[q]);
    if (SCAN_MEX) { printf(" minmex:"); for (int q = 0; q < 16; q++) if (hist_mex2[q]) printf(" m%d=%ld", q - 1, hist_mex2[q]); printf(" maxmex:"); for (int q = 0; q < 16; q++) if (hist_mexmax[q]) printf(" M%d=%ld", q, hist_mexmax[q]); }
    printf(" near0=%ld near1=%ld near2=%ld near3=%ld near4=%ld near5=%ld near6=%ld near7=%ld", hist_near[0], hist_near[1], hist_near[2], hist_near[3], hist_near[4], hist_near[5], hist_near[6], hist_near[7]);
    printf(" cpu=%.1fs\n", (double)(clock() - t0) / CLOCKS_PER_SEC);
    return 0;
}
