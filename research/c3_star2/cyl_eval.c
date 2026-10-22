/* frontier.c -- extension of atlas/flat8/rerun/nimscan.c for T8.
 * Flat boards have widths 1..5; cylindrical rings have widths 5..8.
 *
 * Written from the rules, not from cylcgt: it shares no code with cylcgt/,
 * crosscheck/ or ../indep_scan.py. It reproduces cylcgt's *model* (normal play,
 * a one-sided passed pawn ends the game, races settled by a race rule, the e.p.
 * right of a component kept until someone moves in that component), and decides
 * G = *k by testing whether G + *k is a second-player win, for k = 0..15.
 *
 * For each state s it computes two 16-bit masks:
 *   WL bit k = Left (White) moving first wins G(s) + *k,
 *   WR bit k = Right (Black) moving first wins G(s) + *k.
 * Then G(s) = *k  iff  neither bit k is set.  Outcome of G(s) is read off k = 0.
 *
 * Settings: race rule (count | mover | opponent), e.p. on/off, and the passed
 * test (textbook | aware: a pawn that can still be taken e.p. is not passed).
 *
 * Build:  cc -O2 -o frontier research/star2_frontier/frontier.c
 * Run:    ./frontier --width-min 1 --width-max 4 --min 2 --max 6 > census.tsv
 *
 * Mode --test FILE: lines "position<TAB>width<TAB>DAG" where DAG lists nodes "i,j|k,l"
 *   separated by ";" (node 0 = root) of an explicit game H; prints EQUAL per setting
 *   when G + H is a second-player win (use H = -T to test G = T). Test mode adds the
 *   race rules allWhite / allBlack (every race won by one side): by monotonicity in
 *   leaf values, G = T under both means G = T for every assignment of race results.
 *
 * Output: one line per canonical root:
 *   position \t width \t npawns \t <outcome,nim> for each setting
 * nim = -1 when G is not *k for any k <= 15.
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

/* Fixed stride 8 keeps every square of a width-1..8 board in one uint64_t. */
static inline int SQ(int f, int r) { return (r - 1) * 8 + f; }
static inline uint64_t B(int f, int r) { return UINT64_C(1) << SQ(f, r); }
static inline int FILEOF(int s) { return s & 7; }
static inline int RANKOF(int s) { return (s >> 3) + 1; }

static uint64_t frontW[64], frontB[64]; /* squares on files f-1..f+1 above / below */
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

/* is the pawn of colour `white` on square s takeable e.p. right now? */
static int ep_capturable(uint64_t ep3, uint64_t ep6, int white, int s) {
    /* ep3: White just doubled; Black may take White's pawn on rank 4.
       ep6: Black just doubled; White may take Black's pawn on rank 5. */
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

/* moves needed to promote for the best individually-passed front pawn */
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

/* evaluate one child reached by `white`'s move; returns the 16-bit mask of k for
 * which the mover, having made this move, wins G(child) + *k with the opponent
 * to move. */
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
    uint64_t opp_wins = white ? v.WR : v.WL; /* opponent to move */
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
    /* OR over the mover's moves of child_mask */
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
    int lose_L_seen = 0, lose_R_seen = 0; /* some j < k where mover-first loses */
    for (int k = 0; k < KMAX; k++) {
        int wl = ((AL >> k) & 1) || lose_R_seen; /* Left moves heap to j where Right-first loses */
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

/* ------------------------------------------------------------- G + H tests
 * H is an explicit short game given as a DAG (node 0 = root). For a root
 * position G and H = -T, G + H is a second-player win iff G = T.            */
#define HMAX 256
static int HN, HLn[HMAX], HRn[HMAX], HL[HMAX][16], HR[HMAX][16];

typedef struct { uint64_t wm, bm, ep3, ep6; uint32_t h; uint8_t val, used; } Entry2;
static Entry2 *tab2; static uint64_t t2cap, t2count;
static Entry2 *tab2_find(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6, int hpos) {
    uint64_t h = mix(wm ^ mix(bm) ^ mix(ep3) ^ mix(ep6) ^ ((uint64_t)hpos << 40)) & (t2cap - 1);
    while (tab2[h].used && !(tab2[h].wm == wm && tab2[h].bm == bm &&
                             tab2[h].ep3 == ep3 && tab2[h].ep6 == ep6 && tab2[h].h == (uint32_t)hpos))
        h = (h + 1) & (t2cap - 1);
    return &tab2[h];
}
static void tab2_init(uint64_t cap) {
    free(tab2); t2cap = cap; t2count = 0; tab2 = calloc(t2cap, sizeof(Entry2));
    if (!tab2) { fprintf(stderr, "out of memory\n"); exit(1); }
}
static void tab2_grow(void) {
    Entry2 *old = tab2; uint64_t oc = t2cap;
    t2cap = oc * 2; tab2 = calloc(t2cap, sizeof(Entry2));
    if (!tab2) { fprintf(stderr, "out of memory\n"); exit(1); }
    for (uint64_t i = 0; i < oc; i++) if (old[i].used)
        *tab2_find(old[i].wm, old[i].bm, old[i].ep3, old[i].ep6, old[i].h) = old[i];
    free(old);
}

static int solve2(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6, int h); /* bit0 WL, bit1 WR */

/* mover `white` has just moved to (wm,bm,ep); H at node h; does the mover win? */
static int child_win2(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6, int white, int h) {
    int pw = passedW(wm, bm, ep3, ep6), pb = passedB(wm, bm, ep3, ep6);
    if (pw && pb) {
        int winner_white;
        if (RACE == 1) winner_white = white;
        else if (RACE == 2) winner_white = !white;
        else if (RACE == 3) winner_white = 1;      /* every race won by White */
        else if (RACE == 4) winner_white = 0;      /* every race won by Black */
        else {
            int dm = dist(wm, bm, ep3, ep6, white), dop = dist(wm, bm, ep3, ep6, !white);
            winner_white = (dop <= dm) ? !white : white;
        }
        return winner_white == white;
    }
    if (pw) return white;
    if (pb) return !white;
    int v = solve2(wm, bm, ep3, ep6, h);
    return white ? !((v >> 1) & 1) : !(v & 1);
}

static int gen2(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6, int white, int h) {
    uint64_t occ = wm | bm;
    uint64_t mine = white ? wm : bm, theirs = white ? bm : wm;
    int d = white ? 1 : -1, start = white ? 2 : 7;
    for (uint64_t m = mine; m; m &= m - 1) {
        int s = __builtin_ctzll(m), f = FILEOF(s), r = RANKOF(s);
        int r1 = r + d;
        if (r1 < 1 || r1 > 8) continue;
        uint32_t epcomp = (ep3 | ep6) ? component_files(occ, f) : 0;
        uint64_t base_ep3 = clear_component_ep(ep3, epcomp), base_ep6 = clear_component_ep(ep6, epcomp);
        uint64_t rest = mine & ~B(f, r);
        if (!(occ & B(f, r1))) {
            uint64_t nm = rest | B(f, r1);
            if (white ? child_win2(nm, theirs, base_ep3, base_ep6, 1, h)
                      : child_win2(theirs, nm, base_ep3, base_ep6, 0, h)) return 1;
            int r2 = r + 2 * d;
            if (r == start && !(occ & B(f, r2))) {
                uint64_t nm2 = rest | B(f, r2), cep3 = base_ep3, cep6 = base_ep6;
                if (EPON && has_ep_capturer(theirs, f, r2)) {
                    if (white) cep3 |= B(f, r1); else cep6 |= B(f, r1);
                }
                if (white ? child_win2(nm2, theirs, cep3, cep6, 1, h)
                          : child_win2(theirs, nm2, cep3, cep6, 0, h)) return 1;
            }
        }
        for (int side = -1; side <= 1; side += 2) {
            int g = f + side;
            if (WRAP) g = (g + W) % W;
            else if (g < 0 || g >= W) continue;
            if (theirs & B(g, r1)) {
                uint64_t nm = rest | B(g, r1), nt = theirs & ~B(g, r1);
                if (white ? child_win2(nm, nt, base_ep3, base_ep6, 1, h)
                          : child_win2(nt, nm, base_ep3, base_ep6, 0, h)) return 1;
            } else if ((white && (ep6 & B(g, r1))) || (!white && (ep3 & B(g, r1)))) {
                int victim_r = white ? r1 - 1 : r1 + 1;
                uint64_t nm = rest | B(g, r1), nt = theirs & ~B(g, victim_r);
                if (white ? child_win2(nm, nt, base_ep3, base_ep6, 1, h)
                          : child_win2(nt, nm, base_ep3, base_ep6, 0, h)) return 1;
            }
        }
    }
    return 0;
}

static int solve2(uint64_t wm, uint64_t bm, uint64_t ep3, uint64_t ep6, int h) {
    Entry2 *e = tab2_find(wm, bm, ep3, ep6, h);
    if (e->used) return e->val;
    int wl = gen2(wm, bm, ep3, ep6, 1, h);
    for (int i = 0; !wl && i < HLn[h]; i++) if (!((solve2(wm, bm, ep3, ep6, HL[h][i]) >> 1) & 1)) wl = 1;
    int wr = gen2(wm, bm, ep3, ep6, 0, h);
    for (int i = 0; !wr && i < HRn[h]; i++) if (!(solve2(wm, bm, ep3, ep6, HR[h][i]) & 1)) wr = 1;
    int v = wl | (wr << 1);
    if ((t2count + 1) * 2 > t2cap) { tab2_grow(); e = tab2_find(wm, bm, ep3, ep6, h); }
    e->wm = wm; e->bm = bm; e->ep3 = ep3; e->ep6 = ep6; e->h = (uint32_t)h;
    e->val = (uint8_t)v; e->used = 1; t2count++;
    return v;
}

static uint64_t parse_sq_list(const char *s) {
    uint64_t m = 0;
    while (*s) {
        while (*s == ' ') s++;
        if (*s >= 'a' && *s <= 'h' && s[1] >= '1' && s[1] <= '8') { m |= B(s[0] - 'a', s[1] - '0'); s += 2; }
        else break;
    }
    return m;
}

static int EVAL_CYL;  /* T33 copy: 1 = cylinder adjacency in --eval */

/* Evaluate a short explicit root list with the same 9-setting nimber masks. */
static int run_eval(const char *path) {
    FILE *fp = fopen(path, "r");
    if (!fp) { perror(path); return 1; }
    const char *rname[3] = {"count", "mover", "opponent"};
    int s_race[9], s_ep[9], s_aware[9];
    for (int r = 0, k = 0; r < 3; r++) {
        s_race[k] = r; s_ep[k] = 1; s_aware[k++] = 0;
        s_race[k] = r; s_ep[k] = 0; s_aware[k++] = 0;
        s_race[k] = r; s_ep[k] = 1; s_aware[k++] = 1;
    }
    printf("#position\twidth\tnpawns");
    for (int k = 0; k < 9; k++) printf("\t%s/%s%s", rname[s_race[k]], s_ep[k] ? "epon" : "epoff", s_aware[k] ? "/aware" : "");
    printf("\n");
    static char line[1 << 16];
    while (fgets(line, sizeof line, fp)) {
        if (line[0] == '#' || line[0] == '\n') continue;
        line[strcspn(line, "\n")] = 0;
        char *pos = strtok(line, "\t"), *wid = strtok(NULL, "\t");
        if (!pos || !wid) continue;
        char posbuf[256]; strncpy(posbuf, pos, sizeof posbuf - 1); posbuf[sizeof posbuf - 1] = 0;
        char *wpart = strstr(pos, "W:"), *bpart = strstr(pos, "B:"), *slash = strchr(pos, '/');
        if (!wpart || !bpart || !slash) { fprintf(stderr, "bad root line\n"); fclose(fp); return 2; }
        *slash = 0;
        W = atoi(wid); WRAP = EVAL_CYL;
        if (W < 1 || W > 8) { fprintf(stderr, "eval width must be 1..8\n"); fclose(fp); return 2; }
        init_masks();
        uint64_t wm = parse_sq_list(wpart + 2), bm = parse_sq_list(bpart + 2);
        printf("%s\t%d\t%d", posbuf, W, __builtin_popcountll(wm | bm));
        for (int k = 0; k < 9; k++) {
            RACE = s_race[k]; EPON = s_ep[k]; AWARE = s_aware[k]; tab_init(1u << 18);
            Value v = solve(wm, bm, 0, 0);
            int nim = -1;
            for (int q = 0; q < KMAX; q++) if (!((v.WL >> q) & 1) && !((v.WR >> q) & 1)) { nim = q; break; }
            int l = v.WL & 1, r = v.WR & 1;
            printf("\t%c,%d", l && r ? 'N' : l ? 'L' : r ? 'R' : 'P', nim);
        }
        printf("\n");
    }
    fclose(fp);
    return 0;
}

/* input lines: position \t width \t node;node;...   node = "i,j|k,l" */
static int run_tests(const char *path) {
    FILE *fp = fopen(path, "r");
    if (!fp) { perror(path); return 1; }
    const char *rname[5] = {"count", "mover", "opponent", "allWhite", "allBlack"};
    int s_race[15], s_ep[15], s_aware[15];
    for (int r = 0, k = 0; r < 5; r++) {
        s_race[k] = r; s_ep[k] = 1; s_aware[k] = 0; k++;
        s_race[k] = r; s_ep[k] = 0; s_aware[k] = 0; k++;
        s_race[k] = r; s_ep[k] = 1; s_aware[k] = 1; k++;
    }
    printf("#position\twidth");
    for (int k = 0; k < 15; k++) printf("\t%s/%s%s", rname[s_race[k]], s_ep[k] ? "epon" : "epoff", s_aware[k] ? "/aware" : "");
    printf("\n");
    static char line[1 << 16];
    while (fgets(line, sizeof line, fp)) {
        if (line[0] == '#' || line[0] == '\n') continue;
        line[strcspn(line, "\n")] = 0;
        char *pos = strtok(line, "\t"), *wid = strtok(NULL, "\t"), *dag = strtok(NULL, "\t");
        if (!pos || !wid || !dag) continue;
        char posbuf[128]; strncpy(posbuf, pos, 127); posbuf[127] = 0;
        W = atoi(wid); WRAP = 0; init_masks();
        char *wpart = strstr(pos, "W:"), *bpart = strstr(pos, "B:");
        char *slash = strchr(pos, '/'); *slash = 0;
        uint64_t wm = parse_sq_list(wpart + 2), bm = parse_sq_list(bpart + 2);
        /* parse DAG */
        HN = 0;
        char *save = NULL;
        for (char *node = strtok_r(dag, ";", &save); node; node = strtok_r(NULL, ";", &save)) {
            char *bar = strchr(node, '|'); *bar = 0;
            HLn[HN] = HRn[HN] = 0;
            for (char *p = node; *p;) { HL[HN][HLn[HN]++] = (int)strtol(p, &p, 10); if (*p == ',') p++; }
            for (char *p = bar + 1; *p;) { HR[HN][HRn[HN]++] = (int)strtol(p, &p, 10); if (*p == ',') p++; }
            HN++;
        }
        printf("%s\t%d", posbuf, W);
        for (int k = 0; k < 15; k++) {
            RACE = s_race[k]; EPON = s_ep[k]; AWARE = s_aware[k];
            tab2_init(1u << 16);
            int v = solve2(wm, bm, 0, 0, 0);
            printf("\t%s", v == 0 ? "EQUAL" : "differ");
        }
        printf("\n");
    }
    fclose(fp);
    return 0;
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

typedef struct { uint8_t wr, br, nw, nb; } LocalPattern;
static LocalPattern local[324];
static int nlocal;
static uint64_t suffix[9][9][9];
static long double estimated_roots;
typedef struct { uint64_t wm, bm; int n; uint8_t used; } SeenRoot;
static SeenRoot seen[1 << 15];

static uint64_t rand64(void) {
    return ((uint64_t)(unsigned)rand() << 32) ^ (uint64_t)(unsigned)rand();
}

static void make_local_patterns(void) {
    nlocal = 0;
    for (int r2 = 0; r2 <= 1; r2++) for (int mid = 0; mid < 81; mid++) for (int r7 = 0; r7 <= 1; r7++) {
        int code = mid, nw = r2, nb = r7;
        uint8_t wr = r2 ? (1u << 2) : 0, br = r7 ? (1u << 7) : 0;
        for (int r = 3; r <= 6; r++) {
            int side = code % 3; code /= 3;
            if (side == 1) { wr |= (uint8_t)(1u << r); nw++; }
            if (side == 2) { br |= (uint8_t)(1u << r); nb++; }
        }
        if (nw + nb) local[nlocal++] = (LocalPattern){wr, br, nw, nb};
    }
}

static void make_suffix_counts(int width) {
    memset(suffix, 0, sizeof suffix);
    suffix[width][0][0] = 1;
    for (int f = width - 1; f >= 0; f--)
        for (int w = 0; w <= 8; w++) for (int b = 0; b <= 8; b++)
            for (int i = 0; i < nlocal; i++) {
                LocalPattern p = local[i];
                if (p.nw <= w && p.nb <= b)
                    suffix[f][w][b] += suffix[f + 1][w - p.nw][b - p.nb];
            }
}

static void sample_ring_position(int width, int nw, int nb, uint64_t *wm, uint64_t *bm) {
    int rw = nw, rb = nb;
    *wm = *bm = 0;
    for (int f = 0; f < width; f++) {
        uint64_t total = suffix[f][rw][rb], pick = rand64() % total;
        int selected = 0;
        for (int i = 0; i < nlocal; i++) {
            LocalPattern p = local[i];
            if (p.nw > rw || p.nb > rb) continue;
            uint64_t ways = suffix[f + 1][rw - p.nw][rb - p.nb];
            if (pick < ways) {
                for (int r = 2; r <= 7; r++) {
                    if (p.wr & (1u << r)) *wm |= B(f, r);
                    if (p.br & (1u << r)) *bm |= B(f, r);
                }
                rw -= p.nw; rb -= p.nb; selected = 1; break;
            }
            pick -= ways;
        }
        if (!selected) { fprintf(stderr, "ring sampler invariant failed\n"); exit(2); }
    }
}

static int remember_sample(uint64_t wm, uint64_t bm, int n, int cap_per_stratum, int *stratum_count) {
    uint64_t h = mix(wm ^ mix(bm) ^ (uint64_t)n) & ((1u << 15) - 1);
    while (seen[h].used && !(seen[h].wm == wm && seen[h].bm == bm && seen[h].n == n))
        h = (h + 1) & ((1u << 15) - 1);
    if (seen[h].used || *stratum_count >= cap_per_stratum) return 0;
    seen[h] = (SeenRoot){wm, bm, n, 1};
    add_root(wm, bm, n); (*stratum_count)++;
    return 1;
}

/* Uniform Monte Carlo over exact ring roots; DP gives the population size. */
static void pilot_ring(int width, int minp, int maxp, int trials) {
    make_local_patterns(); make_suffix_counts(width); memset(seen, 0, sizeof seen);
    estimated_roots = 0;
    srand(20261021u + (unsigned)width * 1009u);
    for (int n = minp; n <= maxp; n++) {
        if (n < width) continue;
        for (int nw = 1; nw < n; nw++) {
            int nb = n - nw;
            uint64_t population = suffix[0][nw][nb];
            if (!population) continue;
            int hits = 0, sampled = 0;
            for (int t = 0; t < trials; t++) {
                uint64_t wm, bm;
                sample_ring_position(width, nw, nb, &wm, &bm);
                if (!passedW(wm, bm, 0, 0) && !passedB(wm, bm, 0, 0) && canonical_root(wm, bm)) {
                    hits++;
                    remember_sample(wm, bm, n, 500, &sampled);
                }
            }
            long double estimate = (long double)population * hits / trials;
            estimated_roots += estimate;
            fprintf(stderr, "ring pilot C%d n=%d split=%d+%d population=%llu trials=%d hits=%d estimate=%.1Lf sample=%d\n",
                    width, n, nw, nb, (unsigned long long)population, trials, hits, estimate, sampled);
        }
    }
    fprintf(stderr, "ring pilot C%d estimated canonical no-passer roots=%.1Lf; timing sample=%d\n", width, estimated_roots, nroots);
}

static int file_has_passer(uint64_t mine, uint64_t theirs, int f, int white) {
    for (uint64_t m = mine & filemask[f]; m; m &= m - 1) {
        int s = __builtin_ctzll(m);
        if (!(theirs & (white ? frontW[s] : frontB[s]))) return 1;
    }
    return 0;
}

static void ring_dfs(int f, uint64_t wm, uint64_t bm, int nw, int nb, int target) {
    int remain = W - f;
    if (nw + nb + remain > target || nw + nb > target) return;
    if (f == W) {
        if (nw && nb && nw + nb == target && !passedW(wm, bm, 0, 0) && !passedB(wm, bm, 0, 0))
            add_root(wm, bm, target);
        return;
    }
    for (int i = 0; i < nlocal; i++) {
        LocalPattern p = local[i];
        if (nw + nb + p.nw + p.nb + (remain - 1) > target) continue;
        uint64_t fw = 0, fb = 0;
        for (int r = 2; r <= 7; r++) {
            if (p.wr & (1u << r)) fw |= B(f, r);
            if (p.br & (1u << r)) fb |= B(f, r);
        }
        uint64_t nwm = wm | fw, nbm = bm | fb;
        int center = f - 1;
        if (center >= 1 && center < W - 1 &&
            (file_has_passer(nwm, nbm, center, 1) || file_has_passer(nbm, nwm, center, 0))) continue;
        ring_dfs(f + 1, nwm, nbm, nw + p.nw, nb + p.nb, target);
    }
}

static void enumerate_ring_exact(int minp, int maxp) {
    make_local_patterns();
    for (int n = minp > W ? minp : W; n <= maxp; n++) ring_dfs(0, 0, 0, 0, 0, n);
}

/* T33 copy: --cylinder switches the eval mode to cylinder adjacency */

int main(int argc, char **argv) {
    for (int i = 1; i < argc; i++) if (!strcmp(argv[i], "--cylinder")) EVAL_CYL = 1;
    int minp = 2, maxp = 6, wmin = 1, wmax = 4, pilot = 0, pilot_raw = 0;
    for (int i = 1; i < argc; i++)
        if (!strcmp(argv[i], "--test") && i + 1 < argc) return run_tests(argv[i + 1]);
        else if (!strcmp(argv[i], "--eval") && i + 1 < argc) return run_eval(argv[i + 1]);
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--max") && i + 1 < argc) maxp = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--min") && i + 1 < argc) minp = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--width-min") && i + 1 < argc) wmin = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--width-max") && i + 1 < argc) wmax = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--pilot") && i + 1 < argc) pilot = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--pilot-raw") && i + 1 < argc) pilot_raw = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--cylinder")) WRAP = 1;
        else if (!strcmp(argv[i], "--flat")) WRAP = 0;
    }
    if (wmin < 1 || wmax < wmin || wmax > 9 || minp < 2 || maxp < minp || maxp > 8 || pilot < 0 || pilot_raw < 0) {
        fprintf(stderr, "invalid range (width 1..9, pawns 2..8, pilot >= 0)\n"); return 2;
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
    for (int width = wmin; width <= wmax; width++) {
        if (WRAP && width == 9) {
            fprintf(stderr, "width=9: skipped; a ring needs at least 9 pawns, max=%d\n", maxp);
            continue;
        }
        W = width; nroots = 0;
        init_masks();
        clock_t enum0 = clock();
        if (WRAP && pilot_raw) pilot_ring(W, minp, maxp, pilot_raw);
        else if (WRAP) enumerate_ring_exact(minp, maxp);
        else for (int n = minp; n <= maxp; n++)
            for (int nw = 1; nw < n; nw++) enum_roots(nw, n - nw, n);
        double enum_secs = (double)(clock() - enum0) / CLOCKS_PER_SEC;
        fprintf(stderr, "W=%d %s roots_ready=%d enumeration_cpu=%.3fs%s\n", W, WRAP ? "cylinder" : "flat",
                nroots, enum_secs, (WRAP && pilot_raw) ? " (Monte Carlo pilot)" : "");
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
            double total_est = (WRAP && pilot_raw) ? (double)estimated_roots : nroots;
            double projected = nselected ? secs * total_est / nselected : 0;
            fprintf(stderr, "W=%d %s setting=%d (%s ep=%d aware=%d): roots=%d sampled=%d states=%llu cpu=%.3fs projected=%.3fs\n",
                    W, WRAP ? "cylinder" : "flat", k, rname[RACE], EPON, AWARE, nroots, nselected,
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
