/* c7check_persist.c: T43's research/c7_independent/c7check.c with ONE semantic change (search CHANGED):
 * an e.p. right persists across nim-heap moves (CGT sum semantics) instead of lapsing (chess semantics). */
#define _POSIX_C_SOURCE 200809L
#include <dirent.h>
#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

enum { MAX_FILES = 7, ROWS = 6, MAX_STATES_LOG2 = 22, EP_NONE = 63 };
typedef struct { uint64_t w, b; uint8_t turn, ep, heap, epo; } State;  /* epo: side that may capture e.p. */
typedef struct { uint64_t w, b; uint8_t turn, ep, heap, epo, value, used; } Entry;
typedef struct { uint16_t code, w, b; uint8_t count; } Pattern;

static Entry *tt;
static uint32_t tt_mask;
static uint64_t nodes, lookups, hits, replacements;
static int files_n;

static inline int bit(int f, int r) { return f * ROWS + r; }
static inline int has(uint64_t x, int sq) { return (int)((x >> sq) & 1u); }
static inline uint64_t rotl64(uint64_t x, unsigned n) { return (x << n) | (x >> (64 - n)); }
static uint64_t mix64(uint64_t x) {
    x ^= x >> 30; x *= UINT64_C(0xbf58476d1ce4e5b9);
    x ^= x >> 27; x *= UINT64_C(0x94d049bb133111eb);
    return x ^ (x >> 31);
}
static uint64_t state_hash(State s) {
    return mix64(s.w + UINT64_C(0x9e3779b97f4a7c15)) ^
           rotl64(mix64(s.b + UINT64_C(0x243f6a8885a308d3)), 17) ^
           ((uint64_t)s.turn << 3) ^ ((uint64_t)s.ep << 9) ^ ((uint64_t)s.heap << 19) ^ ((uint64_t)s.epo << 23);
}
static int state_equal(Entry *e, State s) {
    return e->used && e->w == s.w && e->b == s.b && e->turn == s.turn &&
           e->ep == s.ep && e->heap == s.heap && e->epo == s.epo;
}
static void tt_init(void) {
    size_t n = (size_t)1 << MAX_STATES_LOG2;
    tt = calloc(n, sizeof(*tt));
    if (!tt) { perror("calloc transposition table"); exit(2); }
    tt_mask = (uint32_t)n - 1;
}

static int side_has_passer(State s, int side, int *nearest) {
    uint64_t own = side ? s.b : s.w;
    uint64_t enemy = side ? s.w : s.b;
    int dir = side ? -1 : 1;
    int victim = EP_NONE;
    if (s.ep != EP_NONE) victim = (int)s.ep - (s.epo ? -1 : 1);
    *nearest = 99;
    for (int sq = 0; sq < files_n * ROWS; ++sq) {
        if (!has(own, sq)) continue;
        if (side != s.epo && sq == victim) continue;
        int f = sq / ROWS, r = sq % ROWS, blocked = 0;
        for (int df = -1; df <= 1 && !blocked; ++df) {
            int nf = (f + df + files_n) % files_n;
            for (int rr = r + dir; rr >= 0 && rr < ROWS; rr += dir) {
                if (has(enemy, bit(nf, rr))) { blocked = 1; break; }
            }
        }
        if (!blocked) {
            int d = side ? r + 1 : 6 - r;
            if (d < *nearest) *nearest = d;
        }
    }
    return *nearest != 99;
}

/* Returns -1 for a nonterminal board, otherwise the winning side (0=White). */
static int race_winner(State s, int mover) {
    int dw, db;
    int pw = side_has_passer(s, 0, &dw), pb = side_has_passer(s, 1, &db);
    if (pw && !pb) return 0;
    if (pb && !pw) return 1;
    if (pw && pb) {
        int other = 1 - mover;
        int d_other = other ? db : dw;
        int d_mover = mover ? db : dw;
        return d_other <= d_mover ? other : mover;
    }
    return -1;
}

static int can_win(State s);

static int try_pawn_move(State s, int from, int to, int ep_capture, int double_step) {
    int mover = s.turn, dir = mover ? -1 : 1;
    uint64_t from_bit = UINT64_C(1) << from, to_bit = UINT64_C(1) << to;
    State child = s;
    child.turn ^= 1;
    child.ep = EP_NONE;
    child.heap = s.heap;
    if (!mover) child.w = (child.w & ~from_bit) | to_bit;
    else child.b = (child.b & ~from_bit) | to_bit;
    if (ep_capture) {
        int victim = to - dir;
        uint64_t vb = UINT64_C(1) << victim;
        if (!mover) child.b &= ~vb; else child.w &= ~vb;
    } else if (mover) child.w &= ~to_bit;
    else child.b &= ~to_bit;
    if (double_step) {
        int f = to / ROWS, r = to % ROWS, capturable = 0;
        for (int df = -1; df <= 1; df += 2) {
            int nf = (f + df + files_n) % files_n;
            if (has(mover ? child.w : child.b, bit(nf, r))) capturable = 1;
        }
        if (capturable) { child.ep = (uint8_t)(to - dir); child.epo = (uint8_t)(1 - mover); }
    }
    int winner = race_winner(child, mover);
    if (winner >= 0) return winner == mover;
    return !can_win(child);
}

static int can_win(State s) {
    lookups++;
    uint32_t slot = (uint32_t)state_hash(s) & tt_mask;
    Entry *e = &tt[slot];
    if (state_equal(e, s)) { hits++; return e->value; }
    nodes++;
    uint64_t own = s.turn ? s.b : s.w;
    uint64_t enemy = s.turn ? s.w : s.b;
    int dir = s.turn ? -1 : 1;
    for (int from = 0; from < files_n * ROWS; ++from) {
        if (!has(own, from)) continue;
        int f = from / ROWS, r = from % ROWS, nr = r + dir;
        if (nr >= 0 && nr < ROWS) {
            int to = bit(f, nr);
            if (!has(s.w | s.b, to) && try_pawn_move(s, from, to, 0, 0)) goto win;
            if ((!s.turn && r == 0) || (s.turn && r == 5)) {
                int nr2 = r + 2 * dir, to2 = bit(f, nr2);
                if (!has(s.w | s.b, to) && !has(s.w | s.b, to2) &&
                    try_pawn_move(s, from, to2, 0, 1)) goto win;
            }
            for (int df = -1; df <= 1; df += 2) {
                int nf = (f + df + files_n) % files_n, cap = bit(nf, nr);
                if (has(enemy, cap) && try_pawn_move(s, from, cap, 0, 0)) goto win;
                if (s.ep != EP_NONE && s.epo == s.turn && cap == s.ep && try_pawn_move(s, from, cap, 1, 0)) goto win;
            }
        }
    }
    for (int h = 0; h < s.heap; ++h) {
        State child = s;
        child.turn ^= 1;
        child.heap = (uint8_t)h;
        /* CHANGED (orchestrator): the e.p. right persists across a move in the nim heap, as in the CGT sum
         * that the scanner and cylcgt compute; it lapses only at the next move inside the pawn position. */
        int winner = race_winner(child, s.turn);
        if (winner >= 0) {
            if (winner == s.turn) goto win;
            continue;
        }
        if (!can_win(child)) goto win;
    }
    e = &tt[slot];
    if (e->used) replacements++;
    e->w = s.w; e->b = s.b; e->turn = s.turn; e->ep = s.ep; e->heap = s.heap; e->epo = s.epo;
    e->value = 0; e->used = 1;
    return 0;
win:
    e = &tt[slot];
    if (e->used) replacements++;
    e->w = s.w; e->b = s.b; e->turn = s.turn; e->ep = s.ep; e->heap = s.heap; e->epo = s.epo;
    e->value = 1; e->used = 1;
    return 1;
}

static void tt_clear(void) {
    memset(tt, 0, ((size_t)tt_mask + 1) * sizeof(*tt));
    nodes = lookups = hits = replacements = 0;
}

static int read_pos(const char *str, int n, State *s) {
    memset(s, 0, sizeof(*s)); s->ep = EP_NONE; s->turn = 0;
    int side = 0, count = 0;
    const char *p = str;
    while (*p) {
        if (*p == '/') { side = 1; p++; continue; }
        if ((*p == 'W' || *p == 'B') && p[1] == ':') { side = (*p == 'B'); p += 2; continue; }
        if (*p >= 'a' && *p <= 'g' && p[1] >= '2' && p[1] <= '7') {
            int f = *p - 'a', r = p[1] - '2';
            if (f >= n) return 0;
            uint64_t b = UINT64_C(1) << bit(f, r);
            if ((s->w | s->b) & b) return 0;
            if (side) s->b |= b; else s->w |= b;
            count++; p += 2; continue;
        }
        p++;
    }
    if (!count) return 0;
    return 1;
}

static int nimber_signature(State root, int *p0, int *p1, int *p2) {
    int *ps[3] = {p0, p1, p2};
    const int order[] = {2, 0, 1};
    for (int i = 0; i < 3; ++i) {
        int h = order[i];
        int w = can_win((State){root.w, root.b, 0, EP_NONE, (uint8_t)h});
        int b = can_win((State){root.w, root.b, 1, EP_NONE, (uint8_t)h});
        *ps[h] = !w && !b;
    }
    return *p2 && !*p0 && !*p1;
}

static int is_star2_fast(State root) {
    for (int turn = 0; turn < 2; ++turn)
        if (can_win((State){root.w, root.b, (uint8_t)turn, EP_NONE, 2})) return 0;
    for (int turn = 0; turn < 2; ++turn)
        if (can_win((State){root.w, root.b, (uint8_t)turn, EP_NONE, 0})) return 0;
    for (int turn = 0; turn < 2; ++turn)
        if (can_win((State){root.w, root.b, (uint8_t)turn, EP_NONE, 1})) return 0;
    return 1;
}

static void print_position(FILE *out, State s, int n) {
    fprintf(out, "W:");
    for (int f = 0; f < n; ++f) for (int r = 0; r < ROWS; ++r)
        if (has(s.w, bit(f, r))) fprintf(out, " %c%d", 'a' + f, r + 2);
    fprintf(out, " / B:");
    for (int f = 0; f < n; ++f) for (int r = 0; r < ROWS; ++r)
        if (has(s.b, bit(f, r))) fprintf(out, " %c%d", 'a' + f, r + 2);
}

static int mode_pos(int argc, char **argv) {
    if (argc < 4) return 2;
    files_n = atoi(argv[2]);
    if (files_n < 3 || files_n > MAX_FILES) return 2;
    State s;
    if (!read_pos(argv[3], files_n, &s)) { fprintf(stderr, "bad position\n"); return 2; }
    int dw, db;
    if (side_has_passer(s, 0, &dw) || side_has_passer(s, 1, &db)) {
        fprintf(stderr, "root has a passed pawn; this task's root domain excludes it\n"); return 2;
    }
    tt_init();
    int p0, p1, p2, star2 = nimber_signature(s, &p0, &p1, &p2);
    printf("P(G+*0)=%d P(G+*1)=%d P(G+*2)=%d star2=%d\n", p0, p1, p2, star2);
    printf("nodes=%" PRIu64 " lookups=%" PRIu64 " hits=%" PRIu64 " replacements=%" PRIu64 "\n", nodes, lookups, hits, replacements);
    return 0;
}

static int c3_walk(uint64_t w, uint64_t b, int next_sq, int left, int files, uint64_t *tested, uint64_t *stars) {
    if (!left) {
        int occupied[7] = {0}, sides[2] = {0};
        for (int f = 0; f < files; ++f) for (int r = 0; r < ROWS; ++r) {
            int sq = bit(f, r); if (has(w | b, sq)) occupied[f] = 1;
            if (has(w, sq)) sides[0] = 1; if (has(b, sq)) sides[1] = 1;
        }
        for (int f = 0; f < files; ++f) if (!occupied[f]) return 0;
        if (!sides[0] || !sides[1]) return 0;
        State s = {w, b, 0, EP_NONE, 0}; int dw, db;
        if (side_has_passer(s, 0, &dw) || side_has_passer(s, 1, &db)) return 0;
        (*tested)++;
        int p0, p1, p2;
        if (nimber_signature(s, &p0, &p1, &p2)) {
            (*stars)++;
            print_position(stdout, s, files);
            printf("\tP0=%d P1=%d P2=%d\n", p0, p1, p2);
        }
        return 0;
    }
    int remaining = files * ROWS - next_sq;
    if (remaining < left) return 0;
    for (int sq = next_sq; sq < files * ROWS; ++sq) {
        uint64_t m = UINT64_C(1) << sq;
        c3_walk(w | m, b, sq + 1, left - 1, files, tested, stars);
        c3_walk(w, b | m, sq + 1, left - 1, files, tested, stars);
    }
    return 0;
}

static int mode_small(void) {
    files_n = 3; tt_init();
    uint64_t total_tested = 0, stars = 0;
    for (int k = 3; k <= 5; ++k) c3_walk(0, 0, 0, k, 3, &total_tested, &stars);
    printf("C3 roots with 3..5 pawns, all files, both sides, no root passer: tested=%" PRIu64 " star2=%" PRIu64 "\n", total_tested, stars);
    return 0;
}

static Pattern pats[232];
static int npat;
static uint8_t *triple_ok;
static uint16_t seq[7];
static uint64_t enum_raw, enum_classes, enum_star2, enum_tests;
static int enum_chunk, enum_chunks, enum_count_only;
static void build_patterns(void) {
    npat = 0;
    for (uint16_t code = 1; code < 4096; ++code) {
        uint16_t w = code & 63u, b = (code >> 6) & 63u;
        if (w & b) continue;
        int count = __builtin_popcount((unsigned)w) + __builtin_popcount((unsigned)b);
        if (count < 1 || count > 3) continue;
        pats[npat++] = (Pattern){code, w, b, (uint8_t)count};
    }
    triple_ok = malloc((size_t)npat * npat * npat);
    if (!triple_ok) { perror("malloc triple table"); exit(2); }
    for (int l = 0; l < npat; ++l) for (int c = 0; c < npat; ++c) for (int r = 0; r < npat; ++r) {
        uint16_t black = pats[l].b | pats[c].b | pats[r].b;
        uint16_t white = pats[l].w | pats[c].w | pats[r].w;
        int ok = 1;
        for (int x = 0; x < ROWS && ok; ++x) {
            if ((pats[c].w >> x) & 1u) {
                uint16_t ahead = (uint16_t)(black & (uint16_t)(63u ^ ((1u << (x + 1)) - 1u)));
                if (!ahead) ok = 0;
            }
            if ((pats[c].b >> x) & 1u) {
                uint16_t ahead = (uint16_t)(white & (uint16_t)((1u << x) - 1u));
                if (!ahead) ok = 0;
            }
        }
        triple_ok[((size_t)l * npat + c) * npat + r] = (uint8_t)ok;
    }
}

static int is_canonical(void) {
    for (int shift = 0; shift < 7; ++shift) for (int d = -1; d <= 1; d += 2) {
        int less = 0;
        for (int j = 0; j < 7; ++j) {
            int k = (shift + d * j) % 7; if (k < 0) k += 7;
            uint16_t a = pats[seq[k]].code, b = pats[seq[j]].code;
            if (a < b) { less = 1; break; }
            if (a > b) break;
        }
        if (less) return 0;
    }
    return 1;
}

static void enum_leaf(void) {
    if (!triple_ok[((size_t)seq[5] * npat + seq[6]) * npat + seq[0]]) return;
    if (!triple_ok[((size_t)seq[6] * npat + seq[0]) * npat + seq[1]]) return;
    enum_raw++;
    if (!is_canonical()) return;
    enum_classes++;
    if (enum_count_only) return;
    State s = {0, 0, 0, EP_NONE, 0};
    for (int f = 0; f < 7; ++f) {
        for (int r = 0; r < ROWS; ++r) {
            if ((pats[seq[f]].w >> r) & 1u) s.w |= UINT64_C(1) << bit(f, r);
            if ((pats[seq[f]].b >> r) & 1u) s.b |= UINT64_C(1) << bit(f, r);
        }
    }
    enum_tests++;
    if (is_star2_fast(s)) {
        enum_star2++;
        int p0, p1, p2;
        nimber_signature(s, &p0, &p1, &p2);
        print_position(stdout, s, 7);
        printf("\tP0=%d P1=%d P2=%d\n", p0, p1, p2);
        fflush(stdout);
    }
}

static void enum_rec(int col, int pawns) {
    int rem = 7 - col;
    if (pawns + rem > 9 || pawns + 3 * rem < 9) return;
    if (col == 7) { if (pawns == 9) enum_leaf(); return; }
    for (int p = 0; p < npat; ++p) {
        if (col == 1 && (((int)seq[0] * npat + p) % enum_chunks) != enum_chunk) continue;
        if (col > 0 && pats[p].code < pats[seq[0]].code) continue;
        int next = pawns + pats[p].count;
        if (next + (6 - col) > 9 || next + 3 * (6 - col) < 9) continue;
        seq[col] = (uint16_t)p;
        if (col >= 2 && !triple_ok[((size_t)seq[col - 2] * npat + seq[col - 1]) * npat + seq[col]]) continue;
        enum_rec(col + 1, next);
    }
}

static int mode_enum(int argc, char **argv) {
    if (argc < 4) return 2;
    enum_chunk = atoi(argv[2]); enum_chunks = atoi(argv[3]);
    enum_count_only = argc > 4 && !strcmp(argv[4], "--count-only");
    if (enum_chunks < 1 || enum_chunk < 0 || enum_chunk >= enum_chunks) return 2;
    files_n = 7; build_patterns();
    if (!enum_count_only) tt_init();
    enum_rec(0, 0);
    printf("chunk=%d/%d raw_nopasser=%" PRIu64 " canonical_classes=%" PRIu64 " solved=%" PRIu64 " star2=%" PRIu64 "\n",
           enum_chunk, enum_chunks, enum_raw, enum_classes, enum_tests, enum_star2);
    if (!enum_count_only) printf("nodes=%" PRIu64 " lookups=%" PRIu64 " hits=%" PRIu64 " replacements=%" PRIu64 "\n", nodes, lookups, hits, replacements);
    return 0;
}

static int mode_hits(const char *dir) {
    files_n = 7; tt_init();
    DIR *d = opendir(dir);
    if (!d) { perror(dir); return 2; }
    struct dirent *de;
    uint64_t lines = 0, stars = 0, bad = 0;
    while ((de = readdir(d))) {
        size_t len = strlen(de->d_name);
        if (len < 9 || strcmp(de->d_name + len - 9, ".hits.tsv")) continue;
        char path[4096]; snprintf(path, sizeof(path), "%s/%s", dir, de->d_name);
        FILE *fp = fopen(path, "r"); if (!fp) continue;
        char *line = NULL; size_t cap = 0; ssize_t got;
        while ((got = getline(&line, &cap, fp)) >= 0) {
            char *tab = strchr(line, '\t');
            if (tab) *tab = '\0';
            line[strcspn(line, "\r\n")] = '\0';
            if (!*line) continue;
            State s;
            if (!read_pos(line, 7, &s)) { bad++; continue; }
            int dw, db;
            if (side_has_passer(s, 0, &dw) || side_has_passer(s, 1, &db)) { bad++; continue; }
            int p0, p1, p2, yes = nimber_signature(s, &p0, &p1, &p2);
            printf("%s\tP0=%d P1=%d P2=%d star2=%d\n", line, p0, p1, p2, yes);
            lines++; stars += yes;
        }
        free(line); fclose(fp);
    }
    closedir(d);
    printf("claimed_lines=%" PRIu64 " star2=%" PRIu64 " invalid_or_root_passer=%" PRIu64 "\n", lines, stars, bad);
    printf("nodes=%" PRIu64 " lookups=%" PRIu64 " hits=%" PRIu64 " replacements=%" PRIu64 "\n", nodes, lookups, hits, replacements);
    return 0;
}

static int mode_self(void) {
    const char *pos[] = {
        "W: a2 a3 b2 / B: b7 c6 c7",
        "W: a4 b2 c2 / B: b6 c5 d6 d7"
    };
    const int widths[] = {3, 4};
    tt_init();
    for (int i = 0; i < 2; ++i) {
        tt_clear();
        files_n = widths[i]; State s;
        if (!read_pos(pos[i], files_n, &s)) return 1;
        int p0, p1, p2;
        if (!nimber_signature(s, &p0, &p1, &p2)) {
            fprintf(stderr, "known star2 cross-check failed: %s\n", pos[i]); return 1;
        }
    }
    printf("known C3 and C4 *2 positions: pass\n");
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s --self | --pos FILES 'W: ... / B: ...' | --small-c3 | --hits DIR | --enum CHUNK CHUNKS [--count-only]\n", argv[0]);
        return 2;
    }
    if (!strcmp(argv[1], "--self")) return mode_self();
    if (!strcmp(argv[1], "--pos")) return mode_pos(argc, argv);
    if (!strcmp(argv[1], "--small-c3")) return mode_small();
    if (!strcmp(argv[1], "--hits") && argc >= 3) return mode_hits(argv[2]);
    if (!strcmp(argv[1], "--enum")) return mode_enum(argc, argv);
    fprintf(stderr, "unknown mode\n"); return 2;
}
