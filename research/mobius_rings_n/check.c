// T77. Only ranks 2..7 can occur: on the last interior rank facing an
// edge, a pawn is already passed (and cannot be the double-step victim).
#include <assert.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

typedef unsigned __int128 Bits;
typedef struct { Bits army[2], down; int ep; } Pos; // ep: victim square or -1
typedef struct {
    Bits blockers, file_ahead, attacks, crossed, sources[2];
    int distance;
} Geometry;
static Geometry geo[132][2];
static int width;
static inline Bits bit(int sq) { return (Bits)1 << sq; }
static inline int first(Bits b) { uint64_t lo = (uint64_t)b; return lo ? __builtin_ctzll(lo) : 64 + __builtin_ctzll((uint64_t)(b >> 64)); }

static void setup(int n, int twist) {
    width = n;
    for (int f = 0; f < n; f++) for (int r = 0; r < 6; r++)
        for (int down = 0; down < 2; down++) {
            int s = 6*f+r, step = down ? -1 : 1;
            Geometry *g = &geo[s][down];
            int home = r == (down ? 5 : 0);
            g->distance = (down ? r+1 : 6-r) - home;
            for (int df = -1; df <= 1; df++) {
                int file = (f+df+n)%n;
                int flip = twist && (f+df < 0 || f+df >= n);
                for (int k = r+step; k >= 0 && k < 6; k += step) {
                    int dst = 6*file + (flip ? 5-k : k);
                    g->blockers |= bit(dst);
                    if (!df) g->file_ahead |= bit(dst);
                    if (df && k == r+step) {
                        g->attacks |= bit(dst);
                        if (flip) g->crossed |= bit(dst);
                        geo[dst][0].sources[down] |= bit(s);
                    }
                }
            }
        }
}

static Bits passers(Pos p, int side) {
    Bits found = 0, candidates = p.army[side];
    if (p.ep >= 0) candidates &= ~bit(p.ep);
    for (; candidates; candidates &= candidates-1) {
        int s = first(candidates), d = !!(p.down & bit(s));
        if (!(geo[s][d].blockers & p.army[1-side])) found |= bit(s);
    }
    return found;
}

static int distance(Pos p, Bits passed) {
    int best = 99;
    for (; passed; passed &= passed-1) {
        int s = first(passed), d = !!(p.down & bit(s));
        Geometry *g = &geo[s][d];
        if (!(g->file_ahead & (p.army[0] | p.army[1])) && g->distance < best)
            best = g->distance;
    }
    return best;
}

static int terminal(Pos p, int mover) {
    Bits a = passers(p, mover), b = passers(p, 1-mover);
    if (a && b) return distance(p, a) < distance(p, b) ? 1 : -1;
    return !!a - !!b;
}

// Return -1 on a terminal win, otherwise retain only nonterminal successors.
// A null buffer requests only the immediate-win test.
static int children(Pos p, int side, Pos *out) {
    int count = 0;
    Bits occ = p.army[0] | p.army[1];
    for (Bits a = p.army[side]; a; a &= a-1) {
        int s = first(a), d = !!(p.down & bit(s)), step = d ? -1 : 1;
        Geometry *g = &geo[s][d];
        Bits destinations = g->attacks & p.army[1-side], ep_target = 0;
        if (p.ep >= 0 && (p.army[1-side] & bit(p.ep))) {
            int skipped = p.ep + ((p.down & bit(p.ep)) ? 1 : -1);
            ep_target = g->attacks & bit(skipped);
            destinations |= ep_target;
        }
        // Only nonterminal positions reach this function.
        if (!(occ & bit(s+step))) {
            destinations |= bit(s+step);
            if (s%6 == (d ? 5 : 0) && !(occ & bit(s+2*step)))
                destinations |= bit(s+2*step);
        }
        for (; destinations; destinations &= destinations-1) {
            int t = first(destinations);
            Bits dst = bit(t), removed = dst == ep_target ? bit(p.ep) : dst;
            Pos q = p;
            q.army[side] ^= bit(s) | dst;
            q.army[1-side] &= ~removed;
            q.down &= ~(bit(s) | removed);
            if (d != !!(g->crossed & dst)) q.down |= dst;
            q.ep = -1;
            if (t == s+2*step) {
                Geometry *skipped = &geo[s+step][0];
                Bits capable = (skipped->sources[0] & ~q.down) |
                               (skipped->sources[1] & q.down);
                if (q.army[1-side] & capable) q.ep = t;
            }
            int result = terminal(q, side);
            if (result == 1) return -1;
            if (!result && out) out[count++] = q;
        }
    }
    return count;
}

typedef struct { Pos pos; unsigned known, won; } Entry;
static Entry *memo;
#define SLOTS (1u << 20)
static Entry *lookup(Pos p) {
    uint64_t h = ((uint64_t)p.army[0] ^ (uint64_t)(p.army[0] >> 64)*UINT64_C(0x94d049bb133111eb))*UINT64_C(0x9e3779b97f4a7c15)
               + ((uint64_t)p.army[1] ^ (uint64_t)(p.army[1] >> 64)*UINT64_C(0x94d049bb133111eb))*UINT64_C(0xd6e8feb86659fd93)
               + ((uint64_t)p.down ^ (uint64_t)(p.down >> 64)*UINT64_C(0x94d049bb133111eb))*UINT64_C(0xa0761d6478bd642f) + p.ep;
    h ^= h >> 31;
    h *= UINT64_C(0xbf58476d1ce4e5b9);
    return &memo[h >> (64-20)];
}
static int same(Pos a, Pos b) {
    return a.army[0] == b.army[0] && a.army[1] == b.army[1]
           && a.down == b.down && a.ep == b.ep;
}
static int wins(Pos p, int side, int heap) {
    Entry *e = lookup(p);
    unsigned flag = 1u << (4*side+heap);
    if ((e->known & flag) && same(e->pos, p)) return !!(e->won & flag);
    Pos moves[4*132];
    int k = children(p, side, moves), win = k < 0;
    if (win) flag = 15u << (4*side);
    for (int h = 0; !win && h < heap; h++) win = !wins(p, 1-side, h);
    for (int i = 0; !win && i < k; i++) win = !wins(moves[i], 1-side, heap);
    // ponytail: direct-mapped exact keys; eviction costs time only.
    if (!same(e->pos, p)) *e = (Entry){.pos=p};
    e->known |= flag;
    if (win) e->won |= flag;
    return win;
}
static char outcome(Pos p, int heap) {
    return "PLRN"[wins(p, 0, heap) + 2*wins(p, 1, heap)];
}

static uint64_t raw, orbits, hits[2][2]; // hits[heap-2][raw,mirror]
static Bits mirror(Bits b) {
    Bits m = 0;
    for (int f = 0; f < width; f++) { m = (m << 6) | (b & 63); b >>= 6; }
    return m;
}
static void record(Pos p) {
    raw++;  // Count every root independently of any symmetry decisions.
    Bits w = mirror(p.army[0]), b = mirror(p.army[1]);
    if (w < p.army[0] || (w == p.army[0] && b < p.army[1])) return;
    orbits++;
    if (children(p, 0, NULL) < 0 || children(p, 1, NULL) < 0) return;
    if (outcome(p, 0) != 'N' || outcome(p, 1) != 'N') return;
    char a = outcome(p, 2), c = outcome(p, 3);
    int which = a == 'P' && c == 'N' ? 0 : a == 'N' && c == 'P' ? 1 : -1;
    if (which >= 0) {
        hits[which][0] += 1 + (w != p.army[0] || b != p.army[1]);
        hits[which][1]++;
    }
}

// A file can be checked as soon as both its neighbours have been filled.
static int blocked_file(Pos p, int f) {
    Bits file = (Bits)63 << (6*f);
    for (int side = 0; side < 2; side++)
        for (Bits a = p.army[side] & file; a; a &= a-1)
            if (!(geo[first(a)][side].blockers & p.army[1-side])) return 0;
    return 1;
}
static void enumerate(Pos p, int f, int start, int left) {
    for (int r = start; r < 6; r++) for (int side = 0; side < 2; side++) {
        Pos q = p;
        q.army[side] |= bit(6*f+r);
        if (side) q.down |= bit(6*f+r);
        if (left > width-f) enumerate(q, f, r+1, left-1);
        if (f >= 2 && !blocked_file(q, f-1)) continue;
        if (f+1 < width && left > 1) enumerate(q, f+1, 0, left-1);
        if (f+1 == width && left == 1 && blocked_file(q, 0) && blocked_file(q, f))
            record(q);
    }
}

static void fail(const char *msg) { fprintf(stderr, "%s\n", msg); exit(2); }
static void solve_lines(void) {
    char line[2048];
    while (fgets(line, sizeof line, stdin)) {
        Pos p = {.ep=-1};
        char *tok = strtok(line, " \n\t\r");
        for (int f = 0; f < width; f++, tok = strtok(NULL, " \n\t\r")) {
            if (!tok) fail("too few files");
            if (!strcmp(tok, "-")) continue;
            int side = -1;
            for (char *c = tok; *c; c++) {
                if (*c == 'W' || *c == 'B') {
                    if (c[1] < '2' || c[1] > '7') fail("expected pawn rank");
                    side = *c == 'B'; continue;
                }
                if (side < 0 || *c < '2' || *c > '7') fail("invalid token");
                Bits b = bit(6*f+*c-'2');
                if (b & (p.army[0] | p.army[1])) fail("square occupied twice");
                p.army[side] |= b;
            }
        }
        if (tok) fail("too many files");
        p.down = p.army[1];
        if (passers(p, 0) || passers(p, 1)) fail("root has a passer");
        for (int h = 0; h < 4; h++) putchar(outcome(p, h));
        puts("");
    }
}
int main(int argc, char **argv) {
    alarm(8*3600);
    if (argc < 4 || argc > 5) fail("check cylinder|mobius width solve|enum [pawns]");
    int twist = !strcmp(argv[1], "mobius");
    if (!twist && strcmp(argv[1], "cylinder")) fail("unknown topology");
    int n = atoi(argv[2]);
    if (n < 3 || n > 21) fail("width must be 3..21");
    setup(n, twist);
    memo = calloc(SLOTS, sizeof *memo);
    if (!memo) fail("cannot allocate cache");
    if (argc == 4 && !strcmp(argv[3], "solve")) solve_lines();
    else if (argc == 5 && !strcmp(argv[3], "enum")) {
        int k = atoi(argv[4]);
        if (k < n || k > n*6) fail("invalid pawn count");
        enumerate((Pos){.ep=-1}, 0, 0, k);
        printf("%d %d %"PRIu64" %"PRIu64" %"PRIu64" %"PRIu64" %"PRIu64" %"PRIu64"\n",
               n,k,raw,orbits,hits[0][0],hits[0][1],hits[1][0],hits[1][1]);
    } else fail("invalid mode");
    return 0;
}
