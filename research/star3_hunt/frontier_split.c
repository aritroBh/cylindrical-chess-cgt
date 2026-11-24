/* frontier_split.c -- variant of frontier.c that runs a specific pawn split (nw, nb).
 * Build: cc -O2 -o frontier_split research/star2_frontier/frontier_split.c
 * Run:   ./frontier_split --flat --width 5 --nw 4 --nb 4 > out.tsv 2> out.log
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define KMAX 64
#define FULL UINT64_MAX

static int W;          /* board width, 1..8; width 9 has no <=8-pawn ring */
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

static void init_masks(void) {
    for (int f = 0; f < W; f++) {
        filemask[f] = 0;
        for (int r = 1; r <= 8; r++) filemask[f] |= B(f, r);
    }
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

static inline uint64_t mix(uint64_t x) {
    x += 0x9E3779B97F4A7C15ull;
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ull;
    x = (x ^ (x >> 27)) * 0x94D049BB133111EBull;
    return x ^ (x >> 31);
}
static void tab_init(uint64_t cap) {
    free(tab);
    tcap = cap; tcount = 0;
    tab = calloc(tcap, sizeof(Entry));
    if (!tab) { fprintf(stderr, "out of memory\n"); exit(1); }
}
static Entry *tab_find(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6) {
    uint64_t h = mix(wm ^ mix(bm) ^ mix(ep3) ^ mix(ep6)) & (tcap - 1);
    while (tab[h].used && !(tab[h].wm == wm && tab[h].bm == bm &&
                            tab[h].ep3 == ep3 && tab[h].ep6 == ep6)) h = (h + 1) & (tcap - 1);
    return &tab[h];
}
static void tab_grow(void) {
    Entry *old = tab; uint64_t oc = tcap;
    tab = calloc(oc * 2, sizeof(Entry)); tcap = oc * 2;
    if (!tab) { fprintf(stderr, "out of memory\n"); exit(1); }
    for (uint64_t i = 0; i < oc; i++) if (old[i].used)
        *tab_find(old[i].wm, old[i].bm, old[i].ep3, old[i].ep6) = old[i];
    free(old);
}

/* ------------------------------------------------------------------ search */
static Value solve(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6);

/* Occupied-file connected component containing g; ponytail: O(W^2), W <= 8. */
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
    if ((tcount + 1) * 2 > tcap) { tab_grow(); e = tab_find(wm, bm, ep3, ep6); }
    e->wm = wm; e->bm = bm; e->ep3 = ep3; e->ep6 = ep6; e->val = v; e->used = 1; tcount++;
    return v;
}

/* ------------------------------------------------------------------ roots */
typedef struct { uint64_t wm, bm; int n; } Root;
static Root *roots; static int nroots, rcap;

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

static int canonical_root(uint64_t wm, uint64_t bm) {
    uint64_t bestw = wm, bestb = bm;
    int variants = WRAP ? 2 * W : 1;
    for (int v = 0; v < variants; v++) {
        int refl = WRAP ? v / W : 1;
        int shift = WRAP ? v % W : 0;
        uint64_t tw = transform(wm, shift, refl), tb = transform(bm, shift, refl);
        if (tw < bestw || (tw == bestw && tb < bestb)) { bestw = tw; bestb = tb; }
    }
    return wm == bestw && bm == bestb;
}

static void add_root(uint64_t wm, uint64_t bm, int n) {
    if (!canonical_root(wm, bm)) return;
    if (nroots == rcap) {
        rcap = rcap ? rcap * 2 : 1024;
        roots = realloc(roots, (size_t)rcap * sizeof(Root));
        if (!roots) { fprintf(stderr, "root allocation failed\n"); exit(1); }
    }
    roots[nroots++] = (Root){wm, bm, n};
}

/* Enumerate no-passer roots. W-rank-7 and B-rank-2 pawns are necessarily
   passed because roots have no pawns on ranks 8 and 1, so omitting them is exact. */
static void enum_roots(int nw, int nb, int n) {
    int wc[64], bc[64], nwc = 0, nbc = 0;
    for (int f = 0; f < W; f++) {
        for (int r = 2; r <= 6; r++) wc[nwc++] = SQ(f, r);
        for (int r = 3; r <= 7; r++) bc[nbc++] = SQ(f, r);
    }
    if (nw > nwc || nb > nbc) return;
    int iw[8], ib[8];
    for (int i = 0; i < nw; i++) iw[i] = i;
    while (1) {
        uint64_t wm = 0;
        for (int i = 0; i < nw; i++) wm |= B(wc[iw[i]] % 8, (wc[iw[i]] / 8) + 1);
        for (int i = 0; i < nb; i++) ib[i] = i;
        while (1) {
            uint64_t bm = 0;
            for (int i = 0; i < nb; i++) bm |= B(bc[ib[i]] % 8, (bc[ib[i]] / 8) + 1);
            if (!(wm & bm)) {
                uint64_t occ = wm | bm;
                int edge_ok = 1;
                for (int f = 0; f < W; f++)
                    if ((WRAP || f == 0 || f == W - 1) && !(occ & filemask[f])) edge_ok = 0;
                if (edge_ok && !passedW(wm, bm, 0, 0) && !passedB(wm, bm, 0, 0)) add_root(wm, bm, n);
            }
            int i = nb - 1;
            while (i >= 0 && ib[i] == nbc - nb + i) i--;
            if (i < 0) break;
            ib[i]++;
            for (int j = i + 1; j < nb; j++) ib[j] = ib[j - 1] + 1;
        }
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

static int choose_samples(int per_n, int minp, int maxp, unsigned char *selected) {
    if (per_n <= 0) { memset(selected, 1, (size_t)nroots); return nroots; }
    int count_selected = 0;
    for (int n = minp; n <= maxp; n++) {
        int count = 0;
        for (int i = 0; i < nroots; i++) if (roots[i].n == n) count++;
        int take = count < per_n ? count : per_n, ordinal = 0;
        for (int i = 0; i < nroots; i++) if (roots[i].n == n) {
            if ((int64_t)ordinal * take / count != (int64_t)(ordinal + 1) * take / count) {
                selected[i] = 1; count_selected++;
            }
            ordinal++;
        }
    }
    return count_selected;
}

int main(int argc, char **argv) {
    int minp = 2, maxp = 6, wmin = 1, wmax = 4, pilot = 0;
    int split_nw = -1, split_nb = -1, width = -1;
    for (int i = 1; i < argc; i++)
        if (!strcmp(argv[i], "--test") && i + 1 < argc) { fprintf(stderr, "--test not supported in split mode\n"); return 1; }
        else if (!strcmp(argv[i], "--eval") && i + 1 < argc) { fprintf(stderr, "--eval not supported in split mode\n"); return 1; }
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--max") && i + 1 < argc) maxp = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--min") && i + 1 < argc) minp = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--width-min") && i + 1 < argc) wmin = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--width-max") && i + 1 < argc) wmax = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--width") && i + 1 < argc) width = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--nw") && i + 1 < argc) split_nw = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--nb") && i + 1 < argc) split_nb = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--pilot") && i + 1 < argc) pilot = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--cylinder")) WRAP = 1;
        else if (!strcmp(argv[i], "--flat")) WRAP = 0;
    }
    if (width >= 0) { wmin = wmax = width; }
    if (wmin < 1 || wmax < wmin || wmax > 8 || minp < 2 || maxp < minp || maxp > 10 || pilot < 0) {
        fprintf(stderr, "invalid range (width 1..8, pawns 2..10, pilot >= 0)\n"); return 2;
    }
    if (split_nw < 1 || split_nb < 1 || split_nw + split_nb != maxp) {
        fprintf(stderr, "must specify --nw and --nb such that nw+nb=maxp (and maxp=minp)\n"); return 2;
    }
    /* settings: race x (ep off | ep on textbook | ep on aware) */
    const char *rname[3] = {"count", "mover", "opponent"};
    int nset = 9, s_race[9], s_ep[9], s_aware[9];
    for (int r = 0, k = 0; r < 3; r++) {
        s_race[k] = r; s_ep[k] = 1; s_aware[k++] = 0;
        s_race[k] = r; s_ep[k] = 0; s_aware[k++] = 0;
        s_race[k] = r; s_ep[k] = 1; s_aware[k++] = 1;
    }
    printf("#position\twidth\tnpawns");
    for (int k = 0; k < nset; k++) printf("\t%s/%s%s", rname[s_race[k]], s_ep[k] ? "epon" : "epoff", s_aware[k] ? "/aware" : "");
    printf("\n");
    char buf[1024];
    for (int w = wmin; w <= wmax; w++) {
        W = w; nroots = 0;
        init_masks();
        clock_t enum0 = clock();
        enum_roots(split_nw, split_nb, split_nw + split_nb);
        double enum_secs = (double)(clock() - enum0) / CLOCKS_PER_SEC;
        fprintf(stderr, "W=%d flat split=%d+%d roots_ready=%d enumeration_cpu=%.3fs\n", W, split_nw, split_nb, nroots, enum_secs);
        unsigned char *selected = calloc((size_t)(nroots ? nroots : 1), 1);
        int nselected = choose_samples(pilot, minp, maxp, selected);
        char *res = calloc((size_t)(nroots ? nroots : 1) * nset, 1);
        int *nim = calloc((size_t)(nroots ? nroots : 1) * nset, sizeof(int));
        if (!selected || !res || !nim) { fprintf(stderr, "result allocation failed\n"); return 1; }
        for (int k = 0; k < nset; k++) {
            RACE = s_race[k]; EPON = s_ep[k]; AWARE = s_aware[k];
            clock_t c0 = clock(); tab_init(1u << 18);
            for (int i = 0; i < nroots; i++) if (selected[i]) {
                Value v = solve(roots[i].wm, roots[i].bm, 0, 0);
                uint64_t WL = v.WL, WR = v.WR;
                res[i * nset + k] = (WL & 1) && (WR & 1) ? 'N' : (WL & 1) ? 'L' : (WR & 1) ? 'R' : 'P';
                int nk = -1;
                for (int q = 0; q < KMAX; q++) if (!((WL >> q) & 1) && !((WR >> q) & 1)) { nk = q; break; }
                nim[i * nset + k] = nk;
            }
            double secs = (double)(clock() - c0) / CLOCKS_PER_SEC;
            double total_est = nroots;
            double projected = nselected ? secs * total_est / nselected : 0;
            fprintf(stderr, "W=%d flat setting=%d (%s ep=%d aware=%d): roots=%d sampled=%d states=%llu cpu=%.3fs projected=%.3fs\n",
                    W, k, rname[RACE], EPON, AWARE, nroots, nselected,
                    (unsigned long long)tcount, secs, projected);
        }
        for (int i = 0; i < nroots; i++) if (selected[i]) {
            pos_str(buf, roots[i].wm, roots[i].bm);
            printf("%s\t%d\t%d", buf, W, roots[i].n);
            for (int k = 0; k < nset; k++) printf("\t%c,%d", res[i * nset + k], nim[i * nset + k]);
            printf("\n");
        }
        free(selected); free(res); free(nim);
    }
    return 0;
}