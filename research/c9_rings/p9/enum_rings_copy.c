/* enum_rings.c -- enumerate the "root rings" on the pawn cylinder C_n (8 ranks).
 *
 * Usage:  enum_rings N P NW NB [--chunk I K] [--count] [--general] [--check]
 *   N   number of files, 3..12 (the project's work is N = 8 and 9)
 *   P   total pawns, NW white + NB black, P = NW + NB, NW,NB >= 1
 *   --chunk I K   emit only chunk I of K (0 <= I < K).  The chunks partition the root set exactly.
 *                 A chunk is a set of search-tree prefixes (the first CDEPTH = 5 files, --chunk-depth D to
 *                 change; N-2 at most), dealt round robin in search order, so one chunk costs about 1/K of
 *                 the full enumeration and chunks have nearly equal sizes.  The partition depends on D.
 *   --count       do not print rings, print "rings <count>" on stdout at the end
 *   --locate FILE print "LOCATED prefix=<index> ring=..." on stderr for every enumerated ring that is in the
 *                 dihedral orbit of one of the (up to 64) rings in FILE; the chunk of a ring is index mod K
 *   --general     do not use the (provable) pre-filter white rank <= 6 / black rank >= 3 on the file
 *                 configurations; only for cross-checks, it gives the same set.
 *   --check       re-test every emitted ring from scratch with an independent passed-pawn test
 *                 (bitboard-free, rank-by-rank) and abort on a mismatch (slow, for validation only)
 *
 * Root ring (definition, identical to research/star26_rings/frontier_split1_fixed2.c enum_roots):
 *   - white pawns on ranks 2..7, black pawns on ranks 2..7 (ranks 1 and 8 are never occupied), no square
 *     holds two pawns, exactly NW white and NB black pawns;
 *   - every file carries at least one pawn (the ring is a ring and not a smaller cylinder);
 *   - no passed pawn for either side.  A white pawn on (f,r) is passed iff no black pawn stands on
 *     files f-1,f,f+1 (indices mod N) with rank > r; a black pawn on (f,r) is passed iff no white pawn
 *     stands on files f-1,f,f+1 with rank < r.  No e.p. right exists at the root, so the e.p.-aware
 *     refinement of "passed" does not apply;
 *   - up to the dihedral group of the cylinder: rotations f -> f+t and the reflection f -> -f
 *     (2N elements).  Colours are NOT exchanged.  One representative per orbit is printed
 *     (the one whose per-file code sequence is lexicographically smallest).
 *
 * Output: one ring per line, one token per file, "W4B7" = white pawn on rank 4 and black pawn on rank 7
 * of that file, "W23" = white pawns on ranks 2 and 3, "B6", "W2", ... (the rg token syntax).
 *
 * Method: a ring is a cyclic sequence of per-file configurations (set of white ranks, set of black
 * ranks).  Whether the pawns of file f are passed depends only on hiW[f] (highest white rank), loB[f]
 * (lowest black rank) and on hiB, loW of files f-1, f, f+1.  Depth-first search over the files; file f-1
 * is tested as soon as file f is placed, files N-1 and 0 are tested at the end.  Rotations are cut by
 * requiring file 0 to carry the smallest configuration code; the rest of the dihedral group is removed
 * by comparing the code sequence with its 2N images at the leaf.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXF 12
#define MAXCFG 800

typedef struct {
    uint8_t w, b;           /* bit (r-2) = pawn on rank r, ranks 2..7 */
    uint8_t cw, cb;         /* pawn counts */
    uint8_t hiW, loW, hiB, loB;   /* highest/lowest white rank (0 / 9 if none), same for black */
} Cfg;

static Cfg cfg[MAXCFG];
static int ncfg;
static int NF, NP, NW, NB;
static int GENERAL = 0, CHECK = 0, COUNT = 0;
static int CHUNK_I = 0, CHUNK_K = 1, CDEPTH = 5;   /* chunks are dealt over the prefixes of CDEPTH files */
static int *lists[16][16];      /* lists[rw][rb] = ids with cw<=rw, cb<=rb, ascending */
static int  listn[16][16];

static uint64_t nrings = 0, nprefix = 0, nlabelled = 0;
static int seq[MAXF];
static uint64_t curprefix = 0;                 /* index of the CDEPTH-file prefix being expanded */
static int nloc = 0, locseq[64][MAXF];         /* --locate FILE: canonical code sequences to look for */
static const char *LOCFILE = NULL;

static void build_cfgs(void) {
    ncfg = 0;
    for (int w = 0; w < 64; w++)
        for (int b = 0; b < 64; b++) {
            if (w & b) continue;                 /* same square */
            if (!w && !b) continue;              /* every file carries a pawn */
            Cfg c; memset(&c, 0, sizeof c);
            c.w = (uint8_t)w; c.b = (uint8_t)b;
            c.loW = 9; c.loB = 9;
            for (int r = 2; r <= 7; r++) {
                if (w >> (r - 2) & 1) { c.cw++; if (r > c.hiW) c.hiW = (uint8_t)r; if (r < c.loW) c.loW = (uint8_t)r; }
                if (b >> (r - 2) & 1) { c.cb++; if (r > c.hiB) c.hiB = (uint8_t)r; if (r < c.loB) c.loB = (uint8_t)r; }
            }
            if (!GENERAL) {
                /* a white pawn on rank 7 can never be blocked (no black pawn on rank 8), a black pawn on
                 * rank 2 likewise: such a file never occurs in a root ring. */
                if (c.cw && c.hiW > 6) continue;
                if (c.cb && c.loB < 3) continue;
            }
            if (c.cw > NW || c.cb > NB) continue;
            if (ncfg >= MAXCFG) { fprintf(stderr, "too many configs\n"); exit(2); }
            cfg[ncfg++] = c;
        }
    for (int rw = 0; rw <= NW; rw++)
        for (int rb = 0; rb <= NB; rb++) {
            lists[rw][rb] = malloc(sizeof(int) * (size_t)(ncfg + 1));
            int n = 0;
            for (int i = 0; i < ncfg; i++) if (cfg[i].cw <= rw && cfg[i].cb <= rb) lists[rw][rb][n++] = i;
            listn[rw][rb] = n;
        }
}

/* file x (with neighbours a, c) has no passed pawn */
static inline int file_ok(const Cfg *a, const Cfg *x, const Cfg *c) {
    int MB = a->hiB; if (x->hiB > MB) MB = x->hiB; if (c->hiB > MB) MB = c->hiB;
    int mW = a->loW; if (x->loW < mW) mW = x->loW; if (c->loW < mW) mW = c->loW;
    if (x->cw && x->hiW >= MB) return 0;      /* top white pawn not blocked by a higher black pawn nearby */
    if (x->cb && x->loB <= mW) return 0;      /* lowest black pawn not blocked by a lower white pawn nearby */
    return 1;
}

/* canonical: seq is lexicographically <= all of its 2N images */
static int canonical(void) {
    int n = NF;
    for (int t = 0; t < n; t++) {
        if (t) {                                  /* rotation by t */
            for (int i = 0; i < n; i++) {
                int x = seq[(i + t) % n];
                if (x < seq[i]) return 0;
                if (x > seq[i]) break;
            }
        }
        for (int i = 0; i < n; i++) {             /* reflection, then rotation: image[i] = seq[(t - i) mod n] */
            int x = seq[((t - i) % n + n) % n];
            if (x < seq[i]) return 0;
            if (x > seq[i]) break;
        }
    }
    return 1;
}

/* independent passed-pawn test straight from the definition on the expanded board (for --check) */
static int check_ring(void) {
    int n = NF, nw = 0, nb = 0;
    uint8_t Wb[MAXF][9], Bb[MAXF][9];
    memset(Wb, 0, sizeof Wb); memset(Bb, 0, sizeof Bb);
    for (int f = 0; f < n; f++) {
        const Cfg *c = &cfg[seq[f]];
        int any = 0;
        for (int r = 2; r <= 7; r++) {
            if (c->w >> (r - 2) & 1) { Wb[f][r] = 1; nw++; any = 1; }
            if (c->b >> (r - 2) & 1) { if (Wb[f][r]) return 0; Bb[f][r] = 1; nb++; any = 1; }
        }
        if (!any) return 0;
    }
    if (nw != NW || nb != NB) return 0;
    for (int f = 0; f < n; f++)
        for (int r = 1; r <= 8; r++) {
            if (Wb[f][r]) {
                int blocked = 0;
                for (int d = -1; d <= 1; d++) for (int q = r + 1; q <= 8; q++) if (Bb[(f + d + n) % n][q]) blocked = 1;
                if (!blocked) return 0;
            }
            if (Bb[f][r]) {
                int blocked = 0;
                for (int d = -1; d <= 1; d++) for (int q = 1; q < r; q++) if (Wb[(f + d + n) % n][q]) blocked = 1;
                if (!blocked) return 0;
            }
        }
    return 1;
}


static int cfg_of(int w, int b) { for (int i = 0; i < ncfg; i++) if (cfg[i].w == w && cfg[i].b == b) return i; return -1; }

/* lexicographically smallest of the 2N images of s (in place into out) */
static void min_image(const int *s, int *out) {
    int n = NF, best[MAXF], cur[MAXF], have = 0;
    for (int t = 0; t < n; t++)
        for (int refl = 0; refl < 2; refl++) {
            for (int i = 0; i < n; i++) cur[i] = refl ? s[((t - i) % n + n) % n] : s[(i + t) % n];
            if (!have || memcmp(cur, best, sizeof(int) * (size_t)n) < 0) { memcpy(best, cur, sizeof(int) * (size_t)n); have = 1; }
        }
    /* memcmp on ints is not numeric order; redo with a numeric compare */
    int bb[MAXF], hv = 0;
    for (int t = 0; t < n; t++)
        for (int refl = 0; refl < 2; refl++) {
            for (int i = 0; i < n; i++) cur[i] = refl ? s[((t - i) % n + n) % n] : s[(i + t) % n];
            int less = !hv;
            if (hv) for (int i = 0; i < n; i++) { if (cur[i] != bb[i]) { less = cur[i] < bb[i]; break; } }
            if (less) { memcpy(bb, cur, sizeof(int) * (size_t)n); hv = 1; }
        }
    memcpy(out, bb, sizeof(int) * (size_t)n);
}

static void load_locate(const char *fn) {
    FILE *fp = fopen(fn, "r");
    if (!fp) { fprintf(stderr, "cannot open %s\n", fn); exit(2); }
    char line[512];
    while (fgets(line, sizeof line, fp) && nloc < 64) {
        int s[MAXF], f = 0, ok = 1;
        char *tok = strtok(line, " \t\r\n");
        while (tok && f < MAXF) {
            int w = 0, b = 0, mode = 0;
            for (char *c = tok; *c; c++) {
                if (*c == 'W') mode = 1; else if (*c == 'B') mode = 2;
                else if (*c >= '2' && *c <= '7') { if (mode == 1) w |= 1 << (*c - '2'); else if (mode == 2) b |= 1 << (*c - '2'); }
            }
            s[f] = cfg_of(w, b);
            if (s[f] < 0) ok = 0;
            f++; tok = strtok(NULL, " \t\r\n");
        }
        if (f != NF || !ok) { fprintf(stderr, "locate: skipping line (not a ring of this N, or not a root-file config): %s", line); continue; }
        min_image(s, locseq[nloc]);
        nloc++;
    }
    fclose(fp);
}

static int is_located(void) {
    for (int k = 0; k < nloc; k++) if (!memcmp(locseq[k], seq, sizeof(int) * (size_t)NF)) return 1;
    return 0;
}

static void emit(void) {
    char line[MAXF * 20], *p = line;
    for (int f = 0; f < NF; f++) {
        const Cfg *c = &cfg[seq[f]];
        if (f) *p++ = ' ';
        if (c->w) { *p++ = 'W'; for (int r = 2; r <= 7; r++) if (c->w >> (r - 2) & 1) *p++ = (char)('0' + r); }
        if (c->b) { *p++ = 'B'; for (int r = 2; r <= 7; r++) if (c->b >> (r - 2) & 1) *p++ = (char)('0' + r); }
    }
    *p++ = '\n'; *p = 0;
    fputs(line, stdout);
}

static void dfs(int f, int rw, int rb) {
    int left = NF - f - 1;                         /* files still to place after f */
    const int *L = lists[rw][rb];
    int n = listn[rw][rb];
    int c0 = f ? seq[0] : 0;
    for (int k = 0; k < n; k++) {
        int id = L[k];
        if (id < c0) continue;
        const Cfg *c = &cfg[id];
        int nrw = rw - c->cw, nrb = rb - c->cb;
        if (nrw + nrb < left) continue;            /* every remaining file needs a pawn */
        if (f == NF - 1 && (nrw || nrb)) continue; /* all pawns placed */
        seq[f] = id;
        if (f >= 2 && !file_ok(&cfg[seq[f - 2]], &cfg[seq[f - 1]], c)) continue;
        if (f == CDEPTH - 1) {                     /* chunking: deal the CDEPTH-file prefixes round robin */
            uint64_t pi = nprefix++;
            curprefix = pi;
            if (CHUNK_K > 1 && (int)(pi % (uint64_t)CHUNK_K) != CHUNK_I) continue;
        }
        if (f == NF - 1) {
            if (!file_ok(&cfg[seq[NF - 2]], c, &cfg[seq[0]])) continue;
            if (!file_ok(&cfg[seq[NF - 1]], &cfg[seq[0]], &cfg[seq[1]])) continue;
            nlabelled++;
            if (!canonical()) continue;
            if (CHECK && !check_ring()) { fprintf(stderr, "CHECK FAILED\n"); exit(4); }
            if (nloc && is_located()) {
                fprintf(stderr, "LOCATED prefix=%llu ring=", (unsigned long long)curprefix);
                for (int f2 = 0; f2 < NF; f2++) { const Cfg *c = &cfg[seq[f2]]; if (f2) fputc(' ', stderr);
                    if (c->w) { fputc('W', stderr); for (int r = 2; r <= 7; r++) if (c->w >> (r - 2) & 1) fputc('0' + r, stderr); }
                    if (c->b) { fputc('B', stderr); for (int r = 2; r <= 7; r++) if (c->b >> (r - 2) & 1) fputc('0' + r, stderr); } }
                fputc('\n', stderr);
            }
            nrings++;
            if (!COUNT) emit();
        } else dfs(f + 1, nrw, nrb);
    }
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: enum_rings N P NW NB [--chunk I K] [--count] [--general] [--check]\n"); return 1; }
    NF = atoi(argv[1]); NP = atoi(argv[2]); NW = atoi(argv[3]); NB = atoi(argv[4]);
    for (int i = 5; i < argc; i++) {
        if (!strcmp(argv[i], "--chunk") && i + 2 < argc) { CHUNK_I = atoi(argv[++i]); CHUNK_K = atoi(argv[++i]); }
        else if (!strcmp(argv[i], "--chunk-depth") && i + 1 < argc) CDEPTH = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--locate") && i + 1 < argc) LOCFILE = argv[++i];
        else if (!strcmp(argv[i], "--count")) COUNT = 1;
        else if (!strcmp(argv[i], "--general")) GENERAL = 1;
        else if (!strcmp(argv[i], "--check")) CHECK = 1;
        else { fprintf(stderr, "unknown argument %s\n", argv[i]); return 1; }
    }
    if (NF < 4 || NF > MAXF || NW < 1 || NB < 1 || NW + NB != NP || NP < NF || NW > 15 || NB > 15
        || CHUNK_K < 1 || CHUNK_I < 0 || CHUNK_I >= CHUNK_K) {
        fprintf(stderr, "bad arguments (need 4<=N<=%d, P=NW+NB>=N, 0<=I<K)\n", MAXF); return 1;
    }
    if (CDEPTH > NF - 2) CDEPTH = NF - 2;
    if (CDEPTH < 3) CDEPTH = 3;
    setvbuf(stdout, NULL, _IOFBF, 1 << 16);
    build_cfgs();
    if (LOCFILE) load_locate(LOCFILE);
    dfs(0, NW, NB);
    fflush(stdout);
    fprintf(stderr, "enum_rings N=%d P=%d split=%d+%d chunk=%d/%d configs=%d prefixes_seen=%llu labelled_leaves=%llu rings=%llu\n",
            NF, NP, NW, NB, CHUNK_I, CHUNK_K, ncfg, (unsigned long long)nprefix, (unsigned long long)nlabelled,
            (unsigned long long)nrings);
    if (COUNT) printf("rings %llu\n", (unsigned long long)nrings);
    return 0;
}
