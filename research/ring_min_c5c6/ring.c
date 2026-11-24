/* ring.c -- independent solver: is a "ring" of pawns on the cylinder C_n x 8 equal to *2 ?
 * Written from the rules in delegate/briefs/T34_ring_min_independent.md only.
 *
 * Game: pawns only; White = Left moves up, Black = Right moves down; normal play.
 * Board position S (pawn placement + e.p. flag).  Sum S + *h (nim heap).
 *   WL[h] = Left to move in S+*h wins ; WR[h] = Right to move in S+*h wins.
 * G = *k  <=>  S+*k is a second-player win  <=>  !WL[k] && !WR[k].
 *
 * Valuation after every BOARD move:
 *   exactly one side owns a passed pawn  -> that side wins outright (value +-BIG, BIG=256)
 *   both sides own a passed pawn         -> race rule (default "count")
 *   neither                              -> normal play continues
 * E.p. right = part of the board position (component-local): it persists until the next
 * board move (a move in the *h heap does not remove it).  OPT_LAPSE=1 gives the variant in
 * which any move, heap included, removes it.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXN 7
static int N = 4;
static int OPT_EP = 1;      /* en passant captures exist */
static int OPT_EPAWARE = 1; /* a pawn that can be taken e.p. is not passed */
static int OPT_RACE = 0;    /* 0 count, 1 mover wins, 2 opponent (non-mover) wins */
static int OPT_LAPSE = 0;   /* 1: heap move removes e.p. flag (and re-evaluates) */
#define HMAX 4              /* heaps *0..*3 */
static long long lapse_flagged = 0, lapse_term = 0;

typedef struct {
    uint8_t c[MAXN][10];    /* c[file][rank], rank 1..8 ; 0 empty, 1 White, 2 Black */
    int flag;               /* 0 none, else 1+file of the pawn that can be taken e.p. */
    int fcol;               /* colour of that pawn (1 W at rank 4, 2 B at rank 5) */
} Bd;

/* ---------- key encoding ---------- */
typedef unsigned __int128 u128;
static u128 enc(const Bd *b) {
    u128 k = 0;
    for (int f = 0; f < N; f++)
        for (int r = 2; r <= 7; r++)
            k |= (u128)b->c[f][r] << (2 * (f * 6 + r - 2));
    if (b->flag) k |= (u128)(b->flag | ((b->fcol == 2) << 3)) << (12 * N);
    return k;
}
static void dec(u128 k, Bd *b) {
    memset(b, 0, sizeof(*b));
    for (int f = 0; f < N; f++)
        for (int r = 2; r <= 7; r++)
            b->c[f][r] = (k >> (2 * (f * 6 + r - 2))) & 3;
    u128 fl = k >> (12 * N);
    if (fl) { b->flag = fl & 7; b->fcol = (fl & 8) ? 2 : 1; }
}

/* ---------- hash table (bounded, replaces entries when full) ---------- */
static u128 *HK; static uint8_t *HV; static uint64_t HCAP, HCNT;
#define EMPTYK ((u128)0 - 1)  /* all ones */
static uint64_t HMAXCAP = 0;
static void hinit(uint64_t cap) {
    HCAP = cap; HCNT = 0;
    HK = calloc(cap, sizeof(u128)); HV = calloc(cap, 1);
    if (!HK || !HV) { fprintf(stderr, "oom\n"); exit(1); }
    for (uint64_t i = 0; i < cap; i++) HK[i] = EMPTYK;
}
static inline uint64_t hh(u128 k) {
    uint64_t x = (uint64_t)k ^ (uint64_t)(k >> 64);
    x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ULL; x ^= x >> 33;
    return x;
}
static int hget(u128 k, uint8_t *v) {
    uint64_t i = hh(k) & (HCAP - 1);
    uint64_t start = i;
    do {
        if (HK[i] == EMPTYK) return 0;
        if (HK[i] == k) { *v = HV[i]; return 1; }
        i = (i + 1) & (HCAP - 1);
    } while (i != start);
    return 0;
}
static void hput(u128 k, uint8_t v) {
    uint64_t i = hh(k) & (HCAP - 1);
    uint64_t start = i;
    while (1) {
        if (HK[i] == EMPTYK || HK[i] == k) { HK[i] = k; HV[i] = v; if (HCNT < HCAP) HCNT++; return; }
        i = (i + 1) & (HCAP - 1);
        if (i == start) { /* table full: replace this slot */
            HK[i] = k; HV[i] = v; return;
        }
    }
}

/* ---------- rules ---------- */
static int is_passed(const Bd *b, int f, int r, int col) {
    if (OPT_EPAWARE && b->flag && col == b->fcol && f == b->flag - 1 && r == (col == 1 ? 4 : 5))
        return 0;                                  /* can be captured e.p. next move */
    if (col == 1) {
        for (int d = -1; d <= 1; d++) { int g = (f + d + N) % N; for (int q = r + 1; q <= 8; q++) if (b->c[g][q] == 2) return 0; }
    } else {
        for (int d = -1; d <= 1; d++) { int g = (f + d + N) % N; for (int q = 1; q < r; q++) if (b->c[g][q] == 1) return 0; }
    }
    return 1;
}
/* 0 = play on, 1 = White wins, 2 = Black wins ; mover = colour that has just moved */
static int term(const Bd *b, int mover) {
    int dW = 99, dB = 99;
    for (int f = 0; f < N; f++)
        for (int r = 1; r <= 8; r++) {
            int c = b->c[f][r];
            if (!c) continue;
            if (c == 1) { if (is_passed(b, f, r, 1)) { int d = (r == 2) ? 5 : 8 - r; if (d < dW) dW = d; } }
            else        { if (is_passed(b, f, r, 2)) { int d = (r == 7) ? 5 : r - 1; if (d < dB) dB = d; } }
        }
    if (dW == 99 && dB == 99) return 0;
    if (dB == 99) return 1;
    if (dW == 99) return 2;
    int nm = 3 - mover, dm = (mover == 1) ? dW : dB, dn = (mover == 1) ? dB : dW;
    if (OPT_RACE == 1) return mover;
    if (OPT_RACE == 2) return nm;
    return (dn <= dm) ? nm : mover;                /* count rule */
}
static int children(const Bd *b, int col, Bd *out) {
    int n = 0, dir = (col == 1) ? 1 : -1, start = (col == 1) ? 2 : 7, en = 3 - col;
    for (int f = 0; f < N; f++)
        for (int r = 1; r <= 8; r++) {
            if (b->c[f][r] != col) continue;
            int nr = r + dir;
            if (nr < 1 || nr > 8) continue;
            if (b->c[f][nr] == 0) {
                Bd t = *b; t.c[f][r] = 0; t.c[f][nr] = col; t.flag = 0; t.fcol = 0; out[n++] = t;
                if (r == start && b->c[f][r + 2 * dir] == 0) {
                    Bd u = *b; int lr = r + 2 * dir;
                    u.c[f][r] = 0; u.c[f][lr] = col; u.flag = 0; u.fcol = 0;
                    if (OPT_EP && (b->c[(f + 1) % N][lr] == en || b->c[(f + N - 1) % N][lr] == en)) { u.flag = f + 1; u.fcol = col; }
                    out[n++] = u;
                }
            }
            for (int d = -1; d <= 1; d += 2) {
                int g = (f + d + N) % N;
                if (b->c[g][nr] == en) { Bd t = *b; t.c[f][r] = 0; t.c[g][nr] = col; t.flag = 0; t.fcol = 0; out[n++] = t; }
            }
        }
    if (OPT_EP && b->flag && b->fcol == en) {
        int g = b->flag - 1, er = (en == 1) ? 4 : 5, tr = er + dir;
        for (int d = -1; d <= 1; d += 2) {
            int f = (g + d + N) % N;
            if (b->c[f][er] == col && b->c[g][tr] == 0) {
                Bd t = *b; t.c[f][er] = 0; t.c[g][er] = 0; t.c[g][tr] = col; t.flag = 0; t.fcol = 0; out[n++] = t;
            }
        }
    }
    return n;
}

/* bit 2h : Left to move wins S+*h ; bit 2h+1 : Right to move wins S+*h */
static uint8_t solve(const Bd *b) {
    u128 k = enc(b); uint8_t v;
    if (hget(k, &v)) return v;
    int wl[HMAX] = {0}, wr[HMAX] = {0};
    Bd ch[96];
    for (int col = 1; col <= 2; col++) {
        int n = children(b, col, ch);
        for (int i = 0; i < n; i++) {
            int t = term(&ch[i], col);
            if (t) {
                if (t == col) for (int h = 0; h < HMAX; h++) { if (col == 1) wl[h] = 1; else wr[h] = 1; }
            } else {
                uint8_t cv = solve(&ch[i]);
                for (int h = 0; h < HMAX; h++) {
                    if (col == 1) { if (!((cv >> (2 * h + 1)) & 1)) wl[h] = 1; }
                    else          { if (!((cv >> (2 * h)) & 1)) wr[h] = 1; }
                }
            }
        }
    }
    /* heap moves */
    int lapse = OPT_LAPSE && b->flag;
    uint8_t nv[3] = {0, 0, 0}; int nterm[3] = {0, 0, 0}; /* index by mover colour: nterm[col] terminal result after heap move by col */
    if (lapse) {
        Bd nb = *b; nb.flag = 0; nb.fcol = 0;
        for (int col = 1; col <= 2; col++) nterm[col] = term(&nb, col);
        lapse_flagged++; if (nterm[1] || nterm[2]) lapse_term++;
        if (!nterm[1] || !nterm[2]) nv[0] = solve(&nb); /* nonterminal state's bits (nterm same for both unless race) */
    }
    for (int h = 1; h < HMAX; h++)
        for (int hp = 0; hp < h; hp++) {
            if (!lapse) {
                if (!wr[hp]) wl[h] = 1;
                if (!wl[hp]) wr[h] = 1;
            } else {
                /* Left moves heap h->hp, board loses its e.p. flag */
                if (nterm[1]) { if (nterm[1] == 1) wl[h] = 1; }
                else if (!((nv[0] >> (2 * hp + 1)) & 1)) wl[h] = 1;
                if (nterm[2]) { if (nterm[2] == 2) wr[h] = 1; }
                else if (!((nv[0] >> (2 * hp)) & 1)) wr[h] = 1;
            }
        }
    v = 0;
    for (int h = 0; h < HMAX; h++) v |= (wl[h] << (2 * h)) | (wr[h] << (2 * h + 1));
    hput(k, v);
    return v;
}

/* ---------- roots ---------- */
static int root_ok(const Bd *b) {       /* every file occupied, both colours, nobody passed */
    int hasW = 0, hasB = 0;
    for (int f = 0; f < N; f++) {
        int occ = 0;
        for (int r = 1; r <= 8; r++) { if (b->c[f][r]) occ = 1; if (b->c[f][r] == 1) hasW = 1; if (b->c[f][r] == 2) hasB = 1; }
        if (!occ) return 0;
    }
    if (!hasW || !hasB) return 0;
    return term(b, 1) == 0;
}
static void transform(const Bd *b, int rot, int refl, Bd *o) {
    memset(o, 0, sizeof(*o));
    for (int f = 0; f < N; f++) {
        int g = refl ? ((N - f) % N) : f;
        g = (g + rot) % N;
        for (int r = 0; r < 10; r++) o->c[g][r] = b->c[f][r];
    }
}
static void fmt(const Bd *b, char *s) {
    char *p = s; int first;
    p += sprintf(p, "W:"); first = 1;
    for (int f = 0; f < N; f++) for (int r = 1; r <= 8; r++) if (b->c[f][r] == 1) { p += sprintf(p, " %c%d", 'a' + f, r); first = 0; }
    p += sprintf(p, " / B:");
    for (int f = 0; f < N; f++) for (int r = 1; r <= 8; r++) if (b->c[f][r] == 2) { p += sprintf(p, " %c%d", 'a' + f, r); }
    (void)first;
}
static void mirror(const Bd *b, Bd *o) { /* swap colours and flip ranks */
    memset(o, 0, sizeof(*o));
    for (int f = 0; f < N; f++) for (int r = 1; r <= 8; r++) if (b->c[f][r]) o->c[f][9 - r] = 3 - b->c[f][r];
}
static int parse(const char *s, Bd *b) {
    memset(b, 0, sizeof(*b));
    int col = 0; const char *p = s;
    while (*p) {
        if (*p == 'W') { col = 1; p++; }
        else if (*p == 'B') { col = 2; p++; }
        else if (*p >= 'a' && *p < 'a' + N && p[1] >= '1' && p[1] <= '8') { b->c[*p - 'a'][p[1] - '0'] = col; p += 2; }
        else p++;
    }
    return 1;
}

static int MAXP = 7;
static int OPT_EXACT = 0;
static Bd cur;
static int fileCnt[7];
static long long raw[16], cls[16], rawk[16][HMAX + 1], clsk[16][HMAX + 1], mism[16];
static FILE *LIST = NULL, *ALLF = NULL;
static int LISTK = 2;

static void process(void) {
    int np = 0;
    for (int f = 0; f < N; f++) for (int r = 1; r <= 8; r++) if (cur.c[f][r]) np++;
    raw[np]++;
    u128 k0 = enc(&cur);
    Bd t; int orb = 0; u128 seen[2 * MAXN];
    for (int rot = 0; rot < N; rot++) for (int refl = 0; refl < 2; refl++) {
        transform(&cur, rot, refl, &t);
        u128 k = enc(&t);
        if (k < k0) return;                    /* not canonical */
        int dup = 0; for (int i = 0; i < orb; i++) if (seen[i] == k) dup = 1;
        if (!dup) seen[orb++] = k;
    }
    cls[np]++;
    uint8_t v = solve(&cur);
    int cl = HMAX;   /* index for "none of *0..*3" */
    for (int h = 0; h < HMAX; h++) if (!((v >> (2 * h)) & 1) && !((v >> (2 * h + 1)) & 1)) cl = h;
    clsk[np][cl]++; rawk[np][cl] += orb;
    /* colour/rank mirror consistency */
    Bd m; mirror(&cur, &m); uint8_t mv = solve(&m);
    for (int h = 0; h < HMAX; h++)
        if (((v >> (2 * h)) & 1) != ((mv >> (2 * h + 1)) & 1) || ((v >> (2 * h + 1)) & 1) != ((mv >> (2 * h)) & 1)) { mism[np]++; break; }
    if (LIST && cl == LISTK) { char s[200]; fmt(&cur, s); fprintf(LIST, "%d\t%d\t%s\n", np, orb, s); }
    if (ALLF) { char s[200]; fmt(&cur, s); fprintf(ALLF, "%d\t%u\t%s\n", np, (unsigned)v, s); }
}
static void rec(int s, int np) {
    if (s == 6 * N) {
        int allocc = 1;
        for (int i = 0; i < N; i++) if (fileCnt[i] == 0) allocc = 0;
        if (allocc && np >= N && root_ok(&cur) && (!OPT_EXACT || np == MAXP)) process();
        return;
    }
    int f = s / 6, r = s % 6 + 2;
    int rem = 6 * N - s;
    if (np > MAXP) return;
    if (np + rem < N) return;
    if (s % 6 == 0 && f > 0 && fileCnt[f-1] == 0) return;
    int unocc = 0;
    for (int i = f; i < N; i++) if (fileCnt[i] == 0) unocc++;
    if (unocc > rem) return;

    /* empty */
    rec(s + 1, np);
    if (np >= MAXP) return;
    if (r <= 6) {
        cur.c[f][r] = 1; fileCnt[f]++;
        rec(s + 1, np + 1);
        cur.c[f][r] = 0; fileCnt[f]--;
    }
    if (np >= MAXP) return;
    if (r >= 3) {
        cur.c[f][r] = 2; fileCnt[f]++;
        rec(s + 1, np + 1);
        cur.c[f][r] = 0; fileCnt[f]--;
    }
}

int main(int argc, char **argv) {
    const char *listfile = NULL, *allfile = NULL; int mode_pos = 0; char posbuf[512] = "";
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-n")) N = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-p")) MAXP = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--noep")) OPT_EP = 0;
        else if (!strcmp(argv[i], "--textbook")) OPT_EPAWARE = 0;
        else if (!strcmp(argv[i], "--race")) OPT_RACE = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--lapse")) OPT_LAPSE = 1;
        else if (!strcmp(argv[i], "--list")) listfile = argv[++i];
        else if (!strcmp(argv[i], "--listk")) LISTK = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--all")) allfile = argv[++i];
        else if (!strcmp(argv[i], "--exact")) OPT_EXACT = 1;
        else if (!strcmp(argv[i], "-H")) HMAXCAP = (uint64_t)1 << atoi(argv[++i]);
        else if (!strcmp(argv[i], "--pos")) { mode_pos = 1; strncpy(posbuf, argv[++i], 511); }
    }
    if (!HMAXCAP) HMAXCAP = (uint64_t)1 << 22;
    if (N == 6 && MAXP == 9) HMAXCAP = (uint64_t)1 << 26;  /* 1 GB; keeps load factor low enough for fast probe */
    hinit(HMAXCAP);
    clock_t t0 = clock();
    if (mode_pos) {
        Bd b; parse(posbuf, &b);
        char s[200]; fmt(&b, s);
        int ok = root_ok(&b); uint8_t v = solve(&b);
        printf("%s  root_ok=%d  bits=0x%02x  ", s, ok, v);
        for (int h = 0; h < HMAX; h++) printf(" h%d:L%d,R%d", h, (v >> (2 * h)) & 1, (v >> (2 * h + 1)) & 1);
        printf("\n"); return 0;
    }
    if (listfile) LIST = fopen(listfile, "w");
    if (allfile) ALLF = fopen(allfile, "w");
    memset(&cur, 0, sizeof(cur));
    memset(fileCnt, 0, sizeof(fileCnt));
    rec(0, 0);
    if (LIST) fclose(LIST);
    if (ALLF) fclose(ALLF);
    printf("N=%d maxpawns=%d EP=%d EPAWARE=%d RACE=%d LAPSE=%d\n", N, MAXP, OPT_EP, OPT_EPAWARE, OPT_RACE, OPT_LAPSE);
    printf("pawns | rings(raw) rings(classes) | classes by value: 0 *1 *2 *3 other | raw by value: 0 *1 *2 *3 other | mirror-mismatch\n");
    for (int np = 1; np <= MAXP; np++) {
        if (!raw[np]) continue;
        printf("%5d | %10lld %10lld | ", np, raw[np], cls[np]);
        for (int h = 0; h <= HMAX; h++) printf("%lld ", clsk[np][h]);
        printf("| ");
        for (int h = 0; h <= HMAX; h++) printf("%lld ", rawk[np][h]);
        printf("| %lld\n", mism[np]);
    }
    if (OPT_LAPSE) printf("lapse: flagged states=%lld, of which the flag-less board is terminal=%lld\n", lapse_flagged, lapse_term);
    printf("states=%llu table_cap=%llu cpu=%.1fs\n", (unsigned long long)HCNT, (unsigned long long)HCAP, (double)(clock() - t0) / CLOCKS_PER_SEC);
    return 0;
}
