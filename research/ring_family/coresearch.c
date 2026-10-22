/* coresearch.c -- exhaustive search over c-file cores (npc pawns) + alternating single-pawn chain of length L.
 * ring = chain (files 0..L-1) followed by core files (L..L+c-1); chain element i: W r (even i) / B r+2 (odd i) if start=W,
 * else the other way round.  Reports every ring whose value is *2 (default setting).
 * Build: cc -O2 -DSTRIDE=10 -o coresearch coresearch.c
 * Run:   ./coresearch --c 4 --npc 7 --r 3 --start W --L 4 [--maxpf 3]
 */
#define main ringeval_main
#include "ringeval.c"
#undef main

typedef struct { int nw, nb; int wr[3], br[3]; } Cont;
static Cont conts[400]; static int ncont;

static void gen_conts(int maxpf) {
    ncont = 0;
    for (int wm = 0; wm < 32; wm++) for (int bm = 0; bm < 32; bm++) {
        int nw = __builtin_popcount(wm), nb = __builtin_popcount(bm);
        if (nw + nb < 1 || nw + nb > maxpf) continue;
        /* W ranks 2..6 -> bit i = rank i+2 ; B ranks 3..7 -> bit i = rank i+3 */
        Cont c = {0};
        int ok = 1;
        for (int i = 0; i < 5; i++) if (wm >> i & 1) c.wr[c.nw++] = i + 2;
        for (int i = 0; i < 5; i++) if (bm >> i & 1) c.br[c.nb++] = i + 3;
        for (int a = 0; a < c.nw; a++) for (int b = 0; b < c.nb; b++) if (c.wr[a] == c.br[b]) ok = 0;
        if (!ok) continue;
        conts[ncont++] = c;
    }
}

static int NC, NPC, MAXPF = 3, R = 3, L = 4, START_W = 1;
static int idx[8];
static long tested = 0, hits = 0;

static void try_ring(void) {
    uint64_t wm = 0, bm = 0;
    for (int i = 0; i < L; i++) {
        int isW = ((i % 2) == 0) == START_W;
        if (isW) wm |= B(i, R); else bm |= B(i, R + 2);
    }
    for (int j = 0; j < NC; j++) {
        Cont *c = &conts[idx[j]];
        for (int a = 0; a < c->nw; a++) wm |= B(L + j, c->wr[a]);
        for (int a = 0; a < c->nb; a++) bm |= B(L + j, c->br[a]);
    }
    tested++;
    if (passedW(wm, bm, 0, 0) || passedB(wm, bm, 0, 0)) return;
    Value v = solve(wm, bm, 0, 0);
    if (nimber_of(v) == 2 && outcome_char(v, 0) == 'N') {
        char buf[1024]; pos_str(buf, wm, bm);
        printf("%s\n", buf); fflush(stdout); hits++;
    }
}
static void rec(int j, int left) {
    if (j == NC) { if (left == 0) try_ring(); return; }
    for (int i = 0; i < ncont; i++) {
        int p = conts[i].nw + conts[i].nb;
        if (p > left - (NC - j - 1)) continue;
        idx[j] = i;
        rec(j + 1, left - p);
    }
}

int main(int argc, char **argv) {
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--c")) NC = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--npc")) NPC = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--r")) R = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--L")) L = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--maxpf")) MAXPF = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--start")) START_W = argv[++i][0] == 'W';
        else if (!strcmp(argv[i], "--max-entries")) TAB_CAP = (uint64_t)atoll(argv[++i]);
    }
    W = NC + L;
    init_masks(); tab_init(1u << 18);
    gen_conts(MAXPF);
    fprintf(stderr, "contents %d, ring width %d\n", ncont, W);
    rec(0, NPC);
    fprintf(stderr, "tested %ld hits %ld states %llu\n", tested, hits, (unsigned long long)tcount);
    return 0;
}
