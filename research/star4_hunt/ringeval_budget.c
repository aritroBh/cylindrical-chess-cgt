/* ringeval.c -- single-position evaluator for king-less pawn rings (T41, research/ring_family).
 *
 * The solver core (solve/gen/child_mask, race and e.p. conventions) follows
 * research/star26_rings/frontier_split1_fixed2.c line by line, but the bit layout is different so that
 * widths up to 10 fit in 64 bits: square (file f, rank r) is bit (r-2)*STRIDE + f for r = 2..7.
 * (In a non-terminal position W pawns stand on ranks 2..6 and B pawns on ranks 3..7; a W pawn on 7 or a B pawn
 * on 2 is always passed, so rank 1 and rank 8 are never occupied.)
 *
 * Value representation (as in the scanner): for every k < 64, WL bit k = "Left wins G+*k moving first",
 * WR bit k = "Right wins G+*k moving first".  G = *q  iff  G+*q is a second-player win, i.e. both bits clear at q.
 *
 * Build:  cc -O2 -DSTRIDE=10 -o ringeval ringeval.c      (STRIDE=8 for widths <= 8, STRIDE=10 for widths <= 10)
 * Run:    echo "W: a2 a3 b2 / B: b7 c6 c7" | ./ringeval --width 3 [--race count|mover|opponent] [--ep on|off|aware]
 *                  [--max-entries N] [--moves]
 * Input lines: "W: a2 a3 b2 / B: b7 c6 c7" (anything after a TAB is ignored; lines starting with # are skipped).
 * Output per line: position TAB outcome(N/L/R/P) TAB nimber-or--1 TAB signature TAB states
 *   signature = outcome of G+*k for k=0..7 (N/L/R/P)
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <setjmp.h>
static jmp_buf g_jb; static uint64_t g_budget = 0, g_calls = 0;

#ifndef STRIDE
#define STRIDE 10
#endif
#define KMAX 64
#define FULL UINT64_MAX

static int W;          /* board width */
static int WRAP = 1;
static int RACE = 0;   /* 0 count, 1 mover, 2 opponent */
static int EPON = 1, AWARE = 1;
static int EPW = 1, EPB = 1;   /* e.p. rights created by White / Black double steps (experiments) */

static inline int SQ(int f, int r) { return (r - 2) * STRIDE + f; }
static inline uint64_t B(int f, int r) { return UINT64_C(1) << SQ(f, r); }
static inline int FILEOF(int s) { return s % STRIDE; }
static inline int RANKOF(int s) { return s / STRIDE + 2; }

static uint64_t frontW[64], frontB[64], filemask[16];

static void init_masks(void) {
    for (int f = 0; f < W; f++) {
        filemask[f] = 0;
        for (int r = 2; r <= 7; r++) filemask[f] |= B(f, r);
    }
    for (int f = 0; f < W; f++)
        for (int r = 2; r <= 7; r++) {
            uint64_t mw = 0, mb = 0;
            for (int d = -1; d <= 1; d++) {
                int g = f + d;
                if (WRAP) g = (g + W) % W;
                else if (g < 0 || g >= W) continue;
                for (int s = 2; s <= 7; s++) {
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
            for (int q = r + 1; q <= 7; q++) if (occ & B(f, q)) front = 0;
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
            for (int q = 2; q < r; q++) if (occ & B(f, q)) front = 0;
            if (!front) continue;
            int d = r - 1 - (r == 7);
            if (d < best) best = d;
        }
    }
    return best;
}

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
    if (!tab_dummy) tab_dummy = calloc(1, sizeof(Entry));
}
static Entry *tab_find(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6) {
    uint64_t h = mix(wm ^ mix(bm) ^ mix(ep3) ^ mix(ep6)) & (tcap - 1);
    uint64_t start = h;
    while (tab[h].used && !(tab[h].wm == wm && tab[h].bm == bm && tab[h].ep3 == ep3 && tab[h].ep6 == ep6)) {
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

/* returns, as a bitmask over k, the set of k such that the mover wins (G'+*k')... see scanner */
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

/* Move enumeration shared by gen() and the --moves listing. cb == NULL: accumulate child_mask (as the scanner). */
typedef void (*movecb)(const char *desc, uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6, int white);
static movecb CB = NULL;

static uint64_t gen(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6, int white) {
    uint64_t acc = 0;
    uint64_t occ = wm | bm;
    uint64_t mine = white ? wm : bm, theirs = white ? bm : wm;
    int d = white ? 1 : -1, start = white ? 2 : 7;
    char desc[64];
    for (uint64_t m = mine; m && (CB || acc != FULL); m &= m - 1) {
        int s = __builtin_ctzll(m), f = FILEOF(s), r = RANKOF(s);
        int r1 = r + d;
        if (r1 < 2 || r1 > 7) continue;
        uint32_t epcomp = (ep3 | ep6) ? component_files(occ, f) : 0;
        uint64_t base_ep3 = clear_component_ep(ep3, epcomp);
        uint64_t base_ep6 = clear_component_ep(ep6, epcomp);
        uint64_t rest = mine & ~B(f, r);
        if (!(occ & B(f, r1))) {
            uint64_t nm = rest | B(f, r1);
            if (CB) { sprintf(desc, "%c%d-%c%d", 'a' + f, r, 'a' + f, r1);
                      if (white) CB(desc, nm, theirs, base_ep3, base_ep6, 1); else CB(desc, theirs, nm, base_ep3, base_ep6, 0); }
            else acc |= white ? child_mask(nm, theirs, base_ep3, base_ep6, 1)
                              : child_mask(theirs, nm, base_ep3, base_ep6, 0);
            int r2 = r + 2 * d;
            if (r == start && !(occ & B(f, r2))) {
                uint64_t nm2 = rest | B(f, r2), cep3 = base_ep3, cep6 = base_ep6;
                if (EPON && has_ep_capturer(theirs, f, r2)) {
                    if (white) { if (EPW) cep3 |= B(f, r1); } else { if (EPB) cep6 |= B(f, r1); }
                }
                if (CB) { sprintf(desc, "%c%d-%c%d", 'a' + f, r, 'a' + f, r2);
                          if (white) CB(desc, nm2, theirs, cep3, cep6, 1); else CB(desc, theirs, nm2, cep3, cep6, 0); }
                else acc |= white ? child_mask(nm2, theirs, cep3, cep6, 1)
                                  : child_mask(theirs, nm2, cep3, cep6, 0);
            }
        }
        for (int side = -1; side <= 1; side += 2) {
            int g = f + side;
            if (WRAP) g = (g + W) % W;
            else if (g < 0 || g >= W) continue;
            if (theirs & B(g, r1)) {
                uint64_t nm = rest | B(g, r1), nt = theirs & ~B(g, r1);
                if (CB) { sprintf(desc, "%c%dx%c%d", 'a' + f, r, 'a' + g, r1);
                          if (white) CB(desc, nm, nt, base_ep3, base_ep6, 1); else CB(desc, nt, nm, base_ep3, base_ep6, 0); }
                else acc |= white ? child_mask(nm, nt, base_ep3, base_ep6, 1)
                                  : child_mask(nt, nm, base_ep3, base_ep6, 0);
            } else if ((white && (ep6 & B(g, r1))) || (!white && (ep3 & B(g, r1)))) {
                int victim_r = white ? r1 - 1 : r1 + 1;
                uint64_t nm = rest | B(g, r1), nt = theirs & ~B(g, victim_r);
                if (CB) { sprintf(desc, "%c%dx%c%d e.p.", 'a' + f, r, 'a' + g, r1);
                          if (white) CB(desc, nm, nt, base_ep3, base_ep6, 1); else CB(desc, nt, nm, base_ep3, base_ep6, 0); }
                else acc |= white ? child_mask(nm, nt, base_ep3, base_ep6, 1)
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
    movecb saved = CB; CB = NULL;
    uint64_t AL = gen(wm, bm, ep3, ep6, 1), AR = gen(wm, bm, ep3, ep6, 0);
    CB = saved;
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


/* ------------------------------------------------------------ reduced game graph
 * A move is "immediately losing" if afterwards the mover has lost on the spot, and "poisoned" if the opponent then has
 * a move to a terminal win.  The reduced graph keeps only the other moves.  term_val: +1 mover wins at once, -1 mover
 * loses at once, 0 non-terminal (same rules as child_mask). */
static int term_val(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6, int white) {
    int pw = passedW(wm, bm, ep3, ep6), pb = passedB(wm, bm, ep3, ep6);
    if (pw && pb) {
        int winner_white;
        if (RACE == 1) winner_white = white;
        else if (RACE == 2) winner_white = !white;
        else {
            int dm = dist(wm, bm, ep3, ep6, white), dop = dist(wm, bm, ep3, ep6, !white);
            winner_white = (dop <= dm) ? !white : white;
        }
        return winner_white == white ? 1 : -1;
    }
    if (pw) return white ? 1 : -1;
    if (pb) return white ? -1 : 1;
    return 0;
}
static int POI_FOUND;
static int POI_SIDE;
static void poi_cb(const char *d, uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6, int white) {
    if (term_val(wm, bm, ep3, ep6, white) == 1) POI_FOUND = 1;
}
static int poisoned(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6, int mover_white) {
    movecb saved = CB; int sf = POI_FOUND;
    CB = poi_cb; POI_FOUND = 0;
    gen(wm, bm, ep3, ep6, !mover_white);
    int r = POI_FOUND;
    CB = saved; POI_FOUND = sf;
    return r;
}
/* visited set */
typedef struct { uint64_t wm, bm, ep3, ep6; uint8_t used; } VEnt;
static VEnt *vtab; static uint64_t vcap, vcount;
static FILE *RG_OUT = NULL;
static long RG_EDGES = 0, RG_POISONED = 0, RG_LOSING = 0, RG_TERMWIN = 0;
static uint64_t RG_CAP = 2000000; static int RG_OVERFLOW = 0;   /* --rg-cap N: stop exploring beyond N nodes */
static int vfind_insert(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6) { /* returns 1 if new */
    if (vcount * 2 >= vcap) {
        VEnt *old = vtab; uint64_t oc = vcap; vcap = oc ? oc * 2 : (1u << 16);
        vtab = calloc(vcap, sizeof(VEnt));
        for (uint64_t i = 0; i < oc; i++) if (old[i].used) {
            uint64_t h = mix(old[i].wm ^ mix(old[i].bm) ^ mix(old[i].ep3) ^ mix(old[i].ep6)) & (vcap - 1);
            while (vtab[h].used) h = (h + 1) & (vcap - 1);
            vtab[h] = old[i];
        }
        free(old);
    }
    uint64_t h = mix(wm ^ mix(bm) ^ mix(ep3) ^ mix(ep6)) & (vcap - 1);
    while (vtab[h].used) {
        if (vtab[h].wm == wm && vtab[h].bm == bm && vtab[h].ep3 == ep3 && vtab[h].ep6 == ep6) return 0;
        h = (h + 1) & (vcap - 1);
    }
    vtab[h] = (VEnt){wm, bm, ep3, ep6, 1}; vcount++;
    return 1;
}
static void pos_str(char *out, uint64_t wm, uint64_t bm);
static void pos_str_ep(char *out, uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6) {
    pos_str(out, wm, bm);
    char *p = out + strlen(out);
    if (ep3 | ep6) {
        p += sprintf(p, " ep");
        for (int f = 0; f < W; f++) { if (ep3 & B(f, 3)) p += sprintf(p, " %c3", 'a' + f); if (ep6 & B(f, 6)) p += sprintf(p, " %c6", 'a' + f); }
    }
}
static void visit(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6);
static uint64_t CUR_WM, CUR_BM, CUR_EP3, CUR_EP6;
typedef struct { uint64_t wm, bm, ep3, ep6; char desc[40]; int white; } PendingMove;
static PendingMove *pend; static int npend, cappend;
static void rg_cb(const char *d, uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6, int white) {
    int t = term_val(wm, bm, ep3, ep6, white);
    if (t < 0) { RG_LOSING++; return; }
    if (t > 0) { RG_TERMWIN++; if (RG_OUT) { char a[1024], b[1024]; pos_str_ep(a, CUR_WM, CUR_BM, CUR_EP3, CUR_EP6);
                 fprintf(RG_OUT, "%s\t%c\t%s\tTERMINAL-WIN\n", a, white ? 'W' : 'B', d); } return; }
    if (poisoned(wm, bm, ep3, ep6, white)) { RG_POISONED++; return; }
    if (npend == cappend) { cappend = cappend ? cappend * 2 : 64; pend = realloc(pend, cappend * sizeof(PendingMove)); }
    pend[npend++] = (PendingMove){wm, bm, ep3, ep6, {0}, white};
    snprintf(pend[npend - 1].desc, 40, "%s", d);
}
static void visit(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6) {
    if (vcount >= RG_CAP) { RG_OVERFLOW = 1; return; }
    if (!vfind_insert(wm, bm, ep3, ep6)) return;
    int base = npend;
    movecb saved = CB;
    uint64_t s_wm = CUR_WM, s_bm = CUR_BM, s_e3 = CUR_EP3, s_e6 = CUR_EP6;
    CUR_WM = wm; CUR_BM = bm; CUR_EP3 = ep3; CUR_EP6 = ep6;
    CB = rg_cb;
    gen(wm, bm, ep3, ep6, 1);
    gen(wm, bm, ep3, ep6, 0);
    CB = saved;
    int cnt = npend - base;
    PendingMove *mine = malloc(sizeof(PendingMove) * (cnt ? cnt : 1));
    memcpy(mine, pend + base, sizeof(PendingMove) * cnt);
    npend = base;
    CUR_WM = s_wm; CUR_BM = s_bm; CUR_EP3 = s_e3; CUR_EP6 = s_e6;
    for (int i = 0; i < cnt; i++) {
        RG_EDGES++;
        if (RG_OUT) { char a[1024], b[1024]; pos_str_ep(a, wm, bm, ep3, ep6); pos_str_ep(b, mine[i].wm, mine[i].bm, mine[i].ep3, mine[i].ep6);
                      fprintf(RG_OUT, "%s\t%c\t%s\t%s\n", a, mine[i].white ? 'W' : 'B', mine[i].desc, b); }
        visit(mine[i].wm, mine[i].bm, mine[i].ep3, mine[i].ep6);
    }
    free(mine);
}

/* ------------------------------------------------------------ io */
static void pos_str(char *out, uint64_t wm, uint64_t bm) {
    char *p = out;
    p += sprintf(p, "W:");
    for (int f = 0; f < W; f++) for (int r = 2; r <= 7; r++) if (wm & B(f, r)) p += sprintf(p, " %c%d", 'a' + f, r);
    p += sprintf(p, " / B:");
    for (int f = 0; f < W; f++) for (int r = 2; r <= 7; r++) if (bm & B(f, r)) p += sprintf(p, " %c%d", 'a' + f, r);
}

static char outcome_char(Value v, int k) {
    int l = (v.WL >> k) & 1, r = (v.WR >> k) & 1;
    return l && r ? 'N' : l ? 'L' : r ? 'R' : 'P';
}
static int nimber_of(Value v) {
    for (int q = 0; q < KMAX; q++) if (!((v.WL >> q) & 1) && !((v.WR >> q) & 1)) return q;
    return -1;
}
static void describe_value(char *out, Value v) {
    int nk = nimber_of(v);
    char sig[16];
    for (int k = 0; k < 8; k++) sig[k] = outcome_char(v, k);
    sig[8] = 0;
    sprintf(out, "%c\t%d\t%s", outcome_char(v, 0), nk, sig);
}

static void child_report(const char *desc, uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6, int white) {
    char buf[1024], d[128];
    int pw = passedW(wm, bm, ep3, ep6), pb = passedB(wm, bm, ep3, ep6);
    pos_str(buf, wm, bm);
    if (pw && pb) { printf("  %c %-10s -> race: %s\n", white ? 'L' : 'R', desc, buf); return; }
    if (pw || pb) { printf("  %c %-10s -> %s passer (%s)\n", white ? 'L' : 'R', desc, pw ? "W" : "B", buf); return; }
    Value v = solve(wm, bm, ep3, ep6);
    describe_value(d, v);
    for (char *c = d; *c; c++) if (*c == '\t') *c = ' ';
    printf("  %c %-10s -> %s   [%s]%s\n", white ? 'L' : 'R', desc, d, buf, (ep3 | ep6) ? " (ep)" : "");
}

static int parse_side(const char *s, uint64_t *mask) {
    *mask = 0;
    while (*s) {
        while (*s == ' ') s++;
        if (!*s) break;
        if (*s < 'a' || *s >= 'a' + W || s[1] < '2' || s[1] > '7') return 0;
        *mask |= B(*s - 'a', s[1] - '0');
        s += 2;
    }
    return 1;
}

int main(int argc, char **argv) {
    int moves = 0, reduced = 0, nosolve = 0; W = 8;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--width") && i + 1 < argc) W = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--flat")) WRAP = 0;
        else if (!strcmp(argv[i], "--rg-cap") && i + 1 < argc) RG_CAP = (uint64_t)atoll(argv[++i]);
        else if (!strcmp(argv[i], "--no-ep-white")) EPW = 0;
        else if (!strcmp(argv[i], "--no-ep-black")) EPB = 0;
        else if (!strcmp(argv[i], "--max-entries") && i + 1 < argc) TAB_CAP = (uint64_t)atoll(argv[++i]);
        else if (!strcmp(argv[i], "--moves")) moves = 1;
        else if (!strcmp(argv[i], "--no-solve")) nosolve = 1;
        else if (!strcmp(argv[i], "--reduced") && i + 1 < argc) { reduced = 1; const char *fn = argv[++i]; if (strcmp(fn, "-")) RG_OUT = fopen(fn, "w"); }
        else if (!strcmp(argv[i], "--race") && i + 1 < argc) { ++i; RACE = !strcmp(argv[i], "mover") ? 1 : !strcmp(argv[i], "opponent") ? 2 : 0; }
        else if (!strcmp(argv[i], "--ep") && i + 1 < argc) {
            ++i;
            if (!strcmp(argv[i], "off")) { EPON = 0; AWARE = 0; }
            else if (!strcmp(argv[i], "on")) { EPON = 1; AWARE = 0; }
            else { EPON = 1; AWARE = 1; }
        }
    }
    if (W < 1 || W > STRIDE || (6 * STRIDE) > 64) { fprintf(stderr, "bad width/stride\n"); return 2; }
    init_masks();
    tab_init(1u << 18);
    char line[4096], buf[1024], d[128];
    while (fgets(line, sizeof line, stdin)) {
        char *tab_ = strchr(line, '\t'); if (tab_) *tab_ = 0;
        char *nl = strchr(line, '\n'); if (nl) *nl = 0;
        if (!line[0] || line[0] == '#') continue;
        char *slash = strchr(line, '/');
        char *wc = strstr(line, "W:"), *bc = strstr(line, "B:");
        if (!slash || !wc || !bc) { fprintf(stderr, "bad line: %s\n", line); continue; }
        *slash = 0;
        uint64_t wm, bm;
        if (!parse_side(wc + 2, &wm) || !parse_side(bc + 2, &bm)) { fprintf(stderr, "bad squares: %s\n", line); continue; }
        if (wm & bm) { fprintf(stderr, "overlap: %s\n", line); continue; }
        pos_str(buf, wm, bm);
        clock_t c0 = clock();
        uint64_t t0 = tcount;
        int pw = passedW(wm, bm, 0, 0), pb = passedB(wm, bm, 0, 0);
        if (pw || pb) { printf("%s\t%s\n", buf, pw && pb ? "RACE-at-root" : pw ? "W-passed-at-root" : "B-passed-at-root"); continue; }
        if (nosolve) printf("%s\t(not solved)\n", buf);
        else {
            Value v = solve(wm, bm, 0, 0);
            describe_value(d, v);
            printf("%s\t%s\t%llu\t%.2fs\n", buf, d, (unsigned long long)(tcount - t0), (double)(clock() - c0) / CLOCKS_PER_SEC);
        }
        if (reduced) {
            vcount = 0; if (vtab) memset(vtab, 0, vcap * sizeof(VEnt));
            RG_EDGES = RG_POISONED = RG_LOSING = RG_TERMWIN = 0; RG_OVERFLOW = 0;
            visit(wm, bm, 0, 0);
            printf("  reduced graph: nodes=%llu edges=%ld deleted(poisoned)=%ld deleted(losing)=%ld terminal-win moves=%ld%s\n",
                   (unsigned long long)vcount, RG_EDGES, RG_POISONED, RG_LOSING, RG_TERMWIN, RG_OVERFLOW ? " OVERFLOW" : "");
        }
        if (moves) {
            CB = child_report;
            gen(wm, bm, 0, 0, 1);
            gen(wm, bm, 0, 0, 0);
            CB = NULL;
        }
        fflush(stdout);
    }
    return 0;
}
