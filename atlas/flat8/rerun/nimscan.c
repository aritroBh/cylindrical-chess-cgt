/* nimscan.c -- independent outcome / nimber census for pawn-only positions on
 * FLAT boards with 8 ranks and widths 1..4 (workstream A2-search rerun).
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
 * Build:  cc -O2 -o nimscan nimscan.c
 * Run:    ./nimscan > census.tsv      (all 9 settings, all classes in scope)
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

#define KMAX 16
#define FULL 0xFFFFu

static int W;          /* board width, 1..4 */
static int RACE;       /* 0 count, 1 mover, 2 opponent */
static int EPON;       /* e.p. allowed */
static int AWARE;      /* e.p.-capturable pawn does not count as passed */

/* square (f, r), f = 0..3, r = 1..8  ->  bit (r-1)*4 + f */
static inline int SQ(int f, int r) { return (r - 1) * 4 + f; }
static inline uint32_t B(int f, int r) { return 1u << SQ(f, r); }
static inline int FILEOF(int s) { return s & 3; }
static inline int RANKOF(int s) { return (s >> 2) + 1; }

static uint32_t frontW[32], frontB[32]; /* squares on files f-1..f+1 above / below */
static uint32_t filemask[4];

static void init_masks(void) {
    for (int f = 0; f < 4; f++) {
        filemask[f] = 0;
        for (int r = 1; r <= 8; r++) filemask[f] |= B(f, r);
    }
    for (int f = 0; f < 4; f++)
        for (int r = 1; r <= 8; r++) {
            uint32_t mw = 0, mb = 0;
            for (int g = f - 1; g <= f + 1; g++) {
                if (g < 0 || g >= W) continue;
                for (int s = 1; s <= 8; s++) {
                    if (s > r) mw |= B(g, s);
                    if (s < r) mb |= B(g, s);
                }
            }
            frontW[SQ(f, r)] = mw;
            frontB[SQ(f, r)] = mb;
        }
}

/* e.p. state: 0 = none, else 1 + target square.
 * target on rank 3: a white pawn just went x2-x4; Black may capture onto x3.
 * target on rank 6: a black pawn just went x7-x5; White may capture onto x6.
 * Only stored when a capturing pawn stands next to the double-stepped pawn. */
static inline int ep_target(int ep) { return ep - 1; }
static inline int ep_holder_white(int ep) { return RANKOF(ep - 1) == 6; }
static inline int ep_victim(int ep) {
    int t = ep - 1, f = FILEOF(t), r = RANKOF(t);
    return r == 3 ? SQ(f, 4) : SQ(f, 5);
}

/* is the pawn of colour `white` on square s takeable e.p. right now? */
static int ep_capturable(uint32_t wm, uint32_t bm, int ep, int white, int s) {
    if (!ep || ep_victim(ep) != s) return 0;
    if (white == ep_holder_white(ep)) return 0;
    int f = FILEOF(s), r = RANKOF(s);
    uint32_t theirs = white ? bm : wm;
    for (int g = f - 1; g <= f + 1; g += 2)
        if (g >= 0 && g < W && (theirs & B(g, r))) return 1;
    return 0;
}

static int passedW(uint32_t wm, uint32_t bm, int ep) {
    for (uint32_t m = wm; m; m &= m - 1) {
        int s = __builtin_ctz(m);
        if (!(bm & frontW[s])) {
            if (AWARE && ep_capturable(wm, bm, ep, 1, s)) continue;
            return 1;
        }
    }
    return 0;
}
static int passedB(uint32_t wm, uint32_t bm, int ep) {
    for (uint32_t m = bm; m; m &= m - 1) {
        int s = __builtin_ctz(m);
        if (!(wm & frontB[s])) {
            if (AWARE && ep_capturable(wm, bm, ep, 0, s)) continue;
            return 1;
        }
    }
    return 0;
}

/* moves needed to promote for the best individually-passed front pawn */
static int dist(uint32_t wm, uint32_t bm, int ep, int white) {
    int best = 1000000;
    uint32_t occ = wm | bm;
    if (white) {
        for (uint32_t m = wm; m; m &= m - 1) {
            int s = __builtin_ctz(m), f = FILEOF(s), r = RANKOF(s);
            if (bm & frontW[s]) continue;
            if (AWARE && ep_capturable(wm, bm, ep, 1, s)) continue;
            int front = 1;
            for (int q = r + 1; q <= 8; q++) if (occ & B(f, q)) front = 0;
            if (!front) continue;
            int d = 8 - r - (r == 2);
            if (d < best) best = d;
        }
    } else {
        for (uint32_t m = bm; m; m &= m - 1) {
            int s = __builtin_ctz(m), f = FILEOF(s), r = RANKOF(s);
            if (wm & frontB[s]) continue;
            if (AWARE && ep_capturable(wm, bm, ep, 0, s)) continue;
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
typedef struct { uint64_t key; uint32_t val; uint8_t ep, used; } Entry;
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
static Entry *tab_find(uint64_t key, int ep) {
    uint64_t h = mix(key ^ ((uint64_t)ep << 58)) & (tcap - 1);
    while (tab[h].used && !(tab[h].key == key && tab[h].ep == ep)) h = (h + 1) & (tcap - 1);
    return &tab[h];
}
static void tab_grow(void) {
    Entry *old = tab; uint64_t oc = tcap;
    tab = calloc(oc * 2, sizeof(Entry)); tcap = oc * 2;
    if (!tab) { fprintf(stderr, "out of memory\n"); exit(1); }
    for (uint64_t i = 0; i < oc; i++) if (old[i].used) *tab_find(old[i].key, old[i].ep) = old[i];
    free(old);
}

/* ------------------------------------------------------------------ search */
static uint32_t solve(uint32_t wm, uint32_t bm, int ep);

/* files of the maximal run of occupied files that contains file g */
static uint32_t component_files(uint32_t occ, int g) {
    int lo = g, hi = g;
    while (lo - 1 >= 0 && (occ & filemask[lo - 1])) lo--;
    while (hi + 1 < W && (occ & filemask[hi + 1])) hi++;
    uint32_t m = 0;
    for (int f = lo; f <= hi; f++) m |= 1u << f;
    return m;
}

/* evaluate one child reached by `white`'s move; returns the 16-bit mask of k for
 * which the mover, having made this move, wins G(child) + *k with the opponent
 * to move. */
static uint32_t child_mask(uint32_t wm, uint32_t bm, int ep, int white) {
    int pw = passedW(wm, bm, ep), pb = passedB(wm, bm, ep);
    if (pw && pb) {
        int winner_white;
        if (RACE == 1) winner_white = white;
        else if (RACE == 2) winner_white = !white;
        else {
            int dm = dist(wm, bm, ep, white), dop = dist(wm, bm, ep, !white);
            winner_white = (dop <= dm) ? !white : white;
        }
        return (winner_white == white) ? FULL : 0;
    }
    if (pw) return white ? FULL : 0;
    if (pb) return white ? 0 : FULL;
    uint32_t v = solve(wm, bm, ep);
    uint32_t opp_wins = white ? (v >> 16) : (v & FULL); /* opponent to move */
    return (~opp_wins) & FULL;
}

static uint32_t gen(uint32_t wm, uint32_t bm, int ep, int white) {
    /* OR over the mover's moves of child_mask */
    uint32_t acc = 0;
    uint32_t occ = wm | bm;
    uint32_t epcomp = ep ? component_files(occ, FILEOF(ep_target(ep))) : 0;
    uint32_t mine = white ? wm : bm, theirs = white ? bm : wm;
    int d = white ? 1 : -1, start = white ? 2 : 7;
    for (uint32_t m = mine; m && acc != FULL; m &= m - 1) {
        int s = __builtin_ctz(m), f = FILEOF(s), r = RANKOF(s);
        int r1 = r + d;
        if (r1 < 1 || r1 > 8) continue;
        /* e.p. right after this move: kept if the move is in another component */
        int keep = ep && !(epcomp & (1u << f));
        int base_ep = keep ? ep : 0;
        uint32_t rest = mine & ~(1u << s);
        if (!(occ & B(f, r1))) {
            uint32_t nm = rest | B(f, r1);
            acc |= white ? child_mask(nm, theirs, base_ep, 1) : child_mask(theirs, nm, base_ep, 0);
            int r2 = r + 2 * d;
            if (r == start && !(occ & B(f, r2))) {
                uint32_t nm2 = rest | B(f, r2);
                int nep = 0;
                if (EPON) {
                    for (int g = f - 1; g <= f + 1; g += 2)
                        if (g >= 0 && g < W && (theirs & B(g, r2))) nep = 1 + SQ(f, r1);
                }
                if (nep && keep) { fprintf(stderr, "two live e.p. rights: unsupported\n"); exit(2); }
                int cep = nep ? nep : base_ep;
                acc |= white ? child_mask(nm2, theirs, cep, 1) : child_mask(theirs, nm2, cep, 0);
            }
        }
        for (int g = f - 1; g <= f + 1; g += 2) {
            if (g < 0 || g >= W) continue;
            int t = SQ(g, r1);
            if (theirs & (1u << t)) {
                uint32_t nm = rest | (1u << t), nt = theirs & ~(1u << t);
                acc |= white ? child_mask(nm, nt, base_ep, 1) : child_mask(nt, nm, base_ep, 0);
            } else if (ep && ep_holder_white(ep) == white && ep_target(ep) == t) {
                uint32_t nm = rest | (1u << t), nt = theirs & ~(1u << ep_victim(ep));
                acc |= white ? child_mask(nm, nt, 0, 1) : child_mask(nt, nm, 0, 0);
            }
        }
    }
    return acc;
}

static uint32_t solve(uint32_t wm, uint32_t bm, int ep) {
    uint64_t key = (uint64_t)wm | ((uint64_t)bm << 32);
    Entry *e = tab_find(key, ep);
    if (e->used) return e->val;
    uint32_t AL = gen(wm, bm, ep, 1), AR = gen(wm, bm, ep, 0);
    uint32_t WL = 0, WR = 0;
    int lose_L_seen = 0, lose_R_seen = 0; /* some j < k where mover-first loses */
    for (int k = 0; k < KMAX; k++) {
        int wl = ((AL >> k) & 1) || lose_R_seen; /* Left moves heap to j where Right-first loses */
        int wr = ((AR >> k) & 1) || lose_L_seen;
        if (wl) WL |= 1u << k;
        if (wr) WR |= 1u << k;
        if (!wr) lose_R_seen = 1;
        if (!wl) lose_L_seen = 1;
    }
    uint32_t v = WL | (WR << 16);
    if ((tcount + 1) * 2 > tcap) { tab_grow(); e = tab_find(key, ep); }
    e->key = key; e->ep = (uint8_t)ep; e->val = v; e->used = 1; tcount++;
    return v;
}

/* ------------------------------------------------------------- G + H tests
 * H is an explicit short game given as a DAG (node 0 = root). For a root
 * position G and H = -T, G + H is a second-player win iff G = T.            */
#define HMAX 256
static int HN, HLn[HMAX], HRn[HMAX], HL[HMAX][16], HR[HMAX][16];

typedef struct { uint64_t key; uint32_t ep_h; uint8_t val, used; } Entry2;
static Entry2 *tab2; static uint64_t t2cap, t2count;
static Entry2 *tab2_find(uint64_t key, uint32_t eh) {
    uint64_t h = mix(key ^ ((uint64_t)eh << 40)) & (t2cap - 1);
    while (tab2[h].used && !(tab2[h].key == key && tab2[h].ep_h == eh)) h = (h + 1) & (t2cap - 1);
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
    for (uint64_t i = 0; i < oc; i++) if (old[i].used) *tab2_find(old[i].key, old[i].ep_h) = old[i];
    free(old);
}

static int solve2(uint32_t wm, uint32_t bm, int ep, int h); /* bit0 WL, bit1 WR */

/* mover `white` has just moved to (wm,bm,ep); H at node h; does the mover win? */
static int child_win2(uint32_t wm, uint32_t bm, int ep, int white, int h) {
    int pw = passedW(wm, bm, ep), pb = passedB(wm, bm, ep);
    if (pw && pb) {
        int winner_white;
        if (RACE == 1) winner_white = white;
        else if (RACE == 2) winner_white = !white;
        else if (RACE == 3) winner_white = 1;      /* every race won by White */
        else if (RACE == 4) winner_white = 0;      /* every race won by Black */
        else {
            int dm = dist(wm, bm, ep, white), dop = dist(wm, bm, ep, !white);
            winner_white = (dop <= dm) ? !white : white;
        }
        return winner_white == white;
    }
    if (pw) return white;
    if (pb) return !white;
    int v = solve2(wm, bm, ep, h);
    return white ? !((v >> 1) & 1) : !(v & 1);
}

static int gen2(uint32_t wm, uint32_t bm, int ep, int white, int h) {
    uint32_t occ = wm | bm;
    uint32_t epcomp = ep ? component_files(occ, FILEOF(ep_target(ep))) : 0;
    uint32_t mine = white ? wm : bm, theirs = white ? bm : wm;
    int d = white ? 1 : -1, start = white ? 2 : 7;
    for (uint32_t m = mine; m; m &= m - 1) {
        int s = __builtin_ctz(m), f = FILEOF(s), r = RANKOF(s);
        int r1 = r + d;
        if (r1 < 1 || r1 > 8) continue;
        int keep = ep && !(epcomp & (1u << f));
        int base_ep = keep ? ep : 0;
        uint32_t rest = mine & ~(1u << s);
        if (!(occ & B(f, r1))) {
            uint32_t nm = rest | B(f, r1);
            if (white ? child_win2(nm, theirs, base_ep, 1, h) : child_win2(theirs, nm, base_ep, 0, h)) return 1;
            int r2 = r + 2 * d;
            if (r == start && !(occ & B(f, r2))) {
                uint32_t nm2 = rest | B(f, r2);
                int nep = 0;
                if (EPON)
                    for (int g = f - 1; g <= f + 1; g += 2)
                        if (g >= 0 && g < W && (theirs & B(g, r2))) nep = 1 + SQ(f, r1);
                if (nep && keep) { fprintf(stderr, "two live e.p. rights: unsupported\n"); exit(2); }
                int cep = nep ? nep : base_ep;
                if (white ? child_win2(nm2, theirs, cep, 1, h) : child_win2(theirs, nm2, cep, 0, h)) return 1;
            }
        }
        for (int g = f - 1; g <= f + 1; g += 2) {
            if (g < 0 || g >= W) continue;
            int t = SQ(g, r1);
            if (theirs & (1u << t)) {
                uint32_t nm = rest | (1u << t), nt = theirs & ~(1u << t);
                if (white ? child_win2(nm, nt, base_ep, 1, h) : child_win2(nt, nm, base_ep, 0, h)) return 1;
            } else if (ep && ep_holder_white(ep) == white && ep_target(ep) == t) {
                uint32_t nm = rest | (1u << t), nt = theirs & ~(1u << ep_victim(ep));
                if (white ? child_win2(nm, nt, 0, 1, h) : child_win2(nt, nm, 0, 0, h)) return 1;
            }
        }
    }
    return 0;
}

static int solve2(uint32_t wm, uint32_t bm, int ep, int h) {
    uint64_t key = (uint64_t)wm | ((uint64_t)bm << 32);
    uint32_t eh = (uint32_t)ep | ((uint32_t)h << 8);
    Entry2 *e = tab2_find(key, eh);
    if (e->used) return e->val;
    int wl = gen2(wm, bm, ep, 1, h);
    for (int i = 0; !wl && i < HLn[h]; i++) if (!((solve2(wm, bm, ep, HL[h][i]) >> 1) & 1)) wl = 1;
    int wr = gen2(wm, bm, ep, 0, h);
    for (int i = 0; !wr && i < HRn[h]; i++) if (!(solve2(wm, bm, ep, HR[h][i]) & 1)) wr = 1;
    int v = wl | (wr << 1);
    if ((t2count + 1) * 2 > t2cap) { tab2_grow(); e = tab2_find(key, eh); }
    e->key = key; e->ep_h = eh; e->val = (uint8_t)v; e->used = 1; t2count++;
    return v;
}

static uint32_t parse_sq_list(const char *s) {
    uint32_t m = 0;
    while (*s) {
        while (*s == ' ') s++;
        if (*s >= 'a' && *s <= 'd' && s[1] >= '1' && s[1] <= '8') { m |= B(s[0] - 'a', s[1] - '0'); s += 2; }
        else break;
    }
    return m;
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
        W = atoi(wid); init_masks();
        char *wpart = strstr(pos, "W:"), *bpart = strstr(pos, "B:");
        char *slash = strchr(pos, '/'); *slash = 0;
        uint32_t wm = parse_sq_list(wpart + 2), bm = parse_sq_list(bpart + 2);
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
            int v = solve2(wm, bm, 0, 0);
            printf("\t%s", v == 0 ? "EQUAL" : "differ");
        }
        printf("\n");
    }
    fclose(fp);
    return 0;
}

/* ------------------------------------------------------------------ roots */
typedef struct { uint32_t wm, bm; int w; } Root;
static Root *roots; static int nroots, rcap;

static uint32_t mirror(uint32_t m) {
    uint32_t o = 0;
    for (; m; m &= m - 1) {
        int s = __builtin_ctz(m);
        o |= B(W - 1 - FILEOF(s), RANKOF(s));
    }
    return o;
}

static void add_root(uint32_t wm, uint32_t bm) {
    if (nroots == rcap) { rcap = rcap ? rcap * 2 : 1024; roots = realloc(roots, rcap * sizeof(Root)); }
    roots[nroots].wm = wm; roots[nroots].bm = bm; roots[nroots].w = W; nroots++;
}

/* enumerate subsets of size k of cand[0..n) */
static void enum_roots(int nw, int nb) {
    int wc[32], bc[32], nwc = 0, nbc = 0;
    for (int f = 0; f < W; f++) {
        for (int r = 2; r <= 6; r++) wc[nwc++] = SQ(f, r);
        for (int r = 3; r <= 7; r++) bc[nbc++] = SQ(f, r);
    }
    int iw[8], ib[8];
    for (int i = 0; i < nw; i++) iw[i] = i;
    while (1) {
        uint32_t wm = 0;
        for (int i = 0; i < nw; i++) wm |= 1u << wc[iw[i]];
        for (int i = 0; i < nb; i++) ib[i] = i;
        while (1) {
            uint32_t bm = 0;
            for (int i = 0; i < nb; i++) bm |= 1u << bc[ib[i]];
            if (!(wm & bm)) {
                uint32_t occ = wm | bm;
                if ((occ & filemask[0]) && (occ & filemask[W - 1]) && !passedW(wm, bm, 0) && !passedB(wm, bm, 0)) {
                    uint32_t mw = mirror(wm), mb = mirror(bm);
                    uint64_t a = ((uint64_t)wm << 32) | bm, b = ((uint64_t)mw << 32) | mb;
                    if (a <= b) add_root(wm, bm);
                }
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

static void pos_str(char *out, uint32_t wm, uint32_t bm) {
    char *p = out;
    p += sprintf(p, "W:");
    for (int f = 0; f < 4; f++) for (int r = 1; r <= 8; r++) if (wm & B(f, r)) p += sprintf(p, " %c%d", 'a' + f, r);
    p += sprintf(p, " / B:");
    for (int f = 0; f < 4; f++) for (int r = 1; r <= 8; r++) if (bm & B(f, r)) p += sprintf(p, " %c%d", 'a' + f, r);
}

int main(int argc, char **argv) {
    int maxtot = 6, six_w4 = 1;
    for (int i = 1; i < argc; i++)
        if (!strcmp(argv[i], "--test") && i + 1 < argc) return run_tests(argv[i + 1]);
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--no-six-w4")) six_w4 = 0;
        if (!strcmp(argv[i], "--max") && i + 1 < argc) maxtot = atoi(argv[++i]);
    }
    /* settings: race x (ep off | ep on textbook | ep on aware) */
    const char *rname[3] = {"count", "mover", "opponent"};
    int nset = 9;
    int s_race[9], s_ep[9], s_aware[9];
    for (int r = 0, k = 0; r < 3; r++) {
        s_race[k] = r; s_ep[k] = 1; s_aware[k] = 0; k++;
        s_race[k] = r; s_ep[k] = 0; s_aware[k] = 0; k++;
        s_race[k] = r; s_ep[k] = 1; s_aware[k] = 1; k++;
    }
    printf("#position\twidth\tnpawns");
    for (int k = 0; k < nset; k++) printf("\t%s/%s%s", rname[s_race[k]], s_ep[k] ? "epon" : "epoff", s_aware[k] ? "/aware" : "");
    printf("\n");
    char buf[128];
    for (W = 1; W <= 4; W++) {
        init_masks();
        nroots = 0;
        for (int n = 2; n <= maxtot; n++) {
            if (n == 6 && W == 4 && !six_w4) continue;
            for (int nw = 1; nw < n; nw++) enum_roots(nw, n - nw);
        }
        char *res = malloc((size_t)nroots * nset * 2);
        int *nim = malloc((size_t)nroots * nset * sizeof(int));
        for (int k = 0; k < nset; k++) {
            RACE = s_race[k]; EPON = s_ep[k]; AWARE = s_aware[k];
            clock_t c0 = clock();
            tab_init(1u << 20);
            for (int i = 0; i < nroots; i++) {
                uint32_t v = solve(roots[i].wm, roots[i].bm, 0);
                uint32_t WL = v & FULL, WR = v >> 16;
                int l = WL & 1, r = WR & 1;
                res[i * nset + k] = l && r ? 'N' : l ? 'L' : r ? 'R' : 'P';
                int nk = -1;
                for (int q = 0; q < KMAX; q++) if (!((WL >> q) & 1) && !((WR >> q) & 1)) { nk = q; break; }
                nim[i * nset + k] = nk;
            }
            fprintf(stderr, "W=%d setting %d (%s ep=%d aware=%d): %d roots, %llu states, %.1fs\n", W, k,
                    rname[RACE], EPON, AWARE, nroots, (unsigned long long)tcount, (double)(clock() - c0) / CLOCKS_PER_SEC);
        }
        for (int i = 0; i < nroots; i++) {
            pos_str(buf, roots[i].wm, roots[i].bm);
            printf("%s\t%d\t%d", buf, W, __builtin_popcount(roots[i].wm | roots[i].bm));
            for (int k = 0; k < nset; k++) printf("\t%c,%d", res[i * nset + k], nim[i * nset + k]);
            printf("\n");
        }
        free(res); free(nim);
    }
    return 0;
}
