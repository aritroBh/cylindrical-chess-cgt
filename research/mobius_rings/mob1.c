/* mob1.c -- C1: whole-board pawn game on the n-file flat board / cylinder / Moebius strip (8 ranks).
 * State: per file, per colour, per direction a rank bitmask (chart = files 0..N-1; crossing the seam by a capture
 * flips the rank r -> 9-r and the pawn's direction flag).  Memo on (position, h, side), win(p,h,side).
 *   solve [--kind 0|1|2] [--H 3]        stdin: positions (tokens per file, W/B default direction, w/b reversed) -> signature
 *   scan N P [--chunk i k] [--out f]    enumerate Moebius root rings (mring.h) and solve each (kind 2)
 * Rules: see REPORT.md.  Race rule "count", e.p. on, a pawn that can still be taken e.p. is not passed.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <pthread.h>
#include "mring.h"
#define MAXN 8
#define MAXMV 160
typedef struct { uint8_t m[2][2][MAXN]; int8_t epf; uint8_t epr, epk, eph; uint8_t pad[4]; } Pos;
static int N, KIND = 2;   /* 0 flat, 1 cylinder, 2 Moebius */
static inline int nbL(int f) { return f > 0 ? f - 1 : (KIND ? N - 1 : -1); }
static inline int nbR(int f) { return f < N - 1 ? f + 1 : (KIND ? 0 : -1); }
static inline uint8_t eview(const Pos *p, int ec, int f, int g) {
    uint8_t e = p->m[ec][0][g] | p->m[ec][1][g];
    if (KIND == 2 && (f - g == N - 1 || g - f == N - 1)) e = MREV[e];
    return e; }
static inline int blocked(const Pos *p, int c, int f, int r, int di) {
    int ec = 1 - c; uint8_t U = p->m[ec][0][f] | p->m[ec][1][f];
    int l = nbL(f), rt = nbR(f);
    if (l >= 0) U |= eview(p, ec, f, l);
    if (rt >= 0) U |= eview(p, ec, f, rt);
    return di == 0 ? (U >> r) != 0 : (U & ((1u << (r - 1)) - 1)) != 0; }
static inline int epprot(const Pos *p, int c, int f, int r) { return p->epf == f && p->epr == r && p->eph == 1 - c; }
static int has_passed(const Pos *p, int c) {
    for (int f = 0; f < N; f++) for (int di = 0; di < 2; di++) {
        unsigned mk = p->m[c][di][f];
        for (int r = 1; r <= 8; r++) if (mk >> (r - 1) & 1) if (!blocked(p, c, f, r, di) && !epprot(p, c, f, r)) return 1; }
    return 0; }
static int pdist(const Pos *p, int c) {
    int best = 1000000;
    for (int f = 0; f < N; f++) {
        unsigned occ = p->m[0][0][f] | p->m[0][1][f] | p->m[1][0][f] | p->m[1][1][f];
        for (int di = 0; di < 2; di++) {
            unsigned mk = p->m[c][di][f];
            for (int r = 1; r <= 8; r++) if (mk >> (r - 1) & 1) {
                if (blocked(p, c, f, r, di) || epprot(p, c, f, r)) continue;
                if (di == 0 ? (occ >> r) != 0 : (occ & ((1u << (r - 1)) - 1)) != 0) continue;
                int d = di == 0 ? 8 - r - (r == 2) : r - 1 - (r == 7);
                if (d < best) best = d; } } }
    return best; }
/* +1: mover wins at once, -1: mover loses at once, 0: continues */
static int cls(const Pos *c, int mover) {
    int wp = has_passed(c, 0), bp = has_passed(c, 1);
    if (!wp && !bp) return 0;
    if (wp && bp) { int o = 1 - mover; int winner = pdist(c, o) <= pdist(c, mover) ? o : mover; return winner == mover ? 1 : -1; }
    return (wp ? 0 : 1) == mover ? 1 : -1; }
static inline int shiftsq(int f, int r, int df, int dr, int *g, int *r2, int *cr) {
    int gg = f + df, c = 0;
    if (gg < 0 || gg >= N) { if (KIND == 0) return 0; gg = (gg + N) % N; c = 1; }
    int rr = r + dr; if (c && KIND == 2) rr = 9 - rr;
    if (rr < 1 || rr > 8) return 0;
    *g = gg; *r2 = rr; *cr = c; return 1; }
static inline void rem(Pos *q, int c, int f, int r) { q->m[c][0][f] &= ~(1u << (r - 1)); q->m[c][1][f] &= ~(1u << (r - 1)); }
static inline void put(Pos *q, int c, int di, int f, int r) { q->m[c][di][f] |= 1u << (r - 1); }
static inline int occ_at(const Pos *p, int f, int r) { return ((p->m[0][0][f] | p->m[0][1][f] | p->m[1][0][f] | p->m[1][1][f]) >> (r - 1)) & 1; }
static inline int occ_col(const Pos *p, int c, int f, int r) { return ((p->m[c][0][f] | p->m[c][1][f]) >> (r - 1)) & 1; }
/* can an enemy pawn of colour ec capture onto the empty square (f, rk) ? */
static int can_take_onto(const Pos *p, int ec, int f, int rk) {
    for (int g = 0; g < N; g++) for (int di = 0; di < 2; di++) {
        unsigned mk = p->m[ec][di][g]; int e = di ? -1 : 1;
        for (int s = 1; s <= 8; s++) if (mk >> (s - 1) & 1)
            for (int df = -1; df <= 1; df += 2) { int a, b, cr; if (shiftsq(g, s, df, e, &a, &b, &cr) && a == f && b == rk) return 1; } }
    return 0; }
static uint8_t gcap[MAXMV];
static int gen(const Pos *p, int c, Pos *out) {
    int k = 0; int ec = 1 - c;
    for (int f = 0; f < N; f++) for (int di = 0; di < 2; di++) {
        unsigned mk = p->m[c][di][f]; int d = di ? -1 : 1, start = di ? 7 : 2;
        for (int r = 1; r <= 8; r++) if (mk >> (r - 1) & 1) {
            int r1 = r + d; if (r1 < 1 || r1 > 8) continue;
            if (!occ_at(p, f, r1)) {
                Pos q = *p; q.epf = -1; q.epr = q.epk = q.eph = 0; rem(&q, c, f, r); put(&q, c, di, f, r1); gcap[k] = 0; out[k++] = q;
                int r2 = r + 2 * d;
                if (r == start && !occ_at(p, f, r2)) {
                    Pos q2 = *p; q2.epf = -1; q2.epr = q2.epk = q2.eph = 0; rem(&q2, c, f, r); put(&q2, c, di, f, r2);
                    if (can_take_onto(&q2, ec, f, r1)) { q2.epf = f; q2.epr = r2; q2.epk = r1; q2.eph = ec; }
                    gcap[k] = 0; out[k++] = q2; } }
            for (int df = -1; df <= 1; df += 2) {
                int g, rr, cr; if (!shiftsq(f, r, df, d, &g, &rr, &cr)) continue;
                int ndi = di ^ (cr && KIND == 2);
                if (occ_col(p, ec, g, rr)) {
                    Pos q = *p; q.epf = -1; q.epr = q.epk = q.eph = 0; rem(&q, c, f, r); rem(&q, ec, g, rr); put(&q, c, ndi, g, rr); gcap[k] = 1; out[k++] = q; }
                else if (p->epf >= 0 && p->eph == c && g == p->epf && rr == p->epk) {
                    Pos q = *p; q.epf = -1; q.epr = q.epk = q.eph = 0; int sr = p->epr;
                    rem(&q, c, f, r); rem(&q, ec, g, sr); put(&q, c, ndi, g, rr); gcap[k] = 1; out[k++] = q; } } } }
    return k; }
/* ---- memo ---- */
typedef struct { Pos p; uint8_t h, side; int8_t res; uint32_t gen; } Ent;
static Ent *tab; static size_t tcap, tcount; static uint32_t curgen = 1; static int overflow; static long nodes, nodetot;
static inline uint64_t hpos(const Pos *p, int h, int side) {
    const uint64_t *w = (const uint64_t *)p; uint64_t x = 0x9E3779B97F4A7C15ULL ^ (h * 4 + side);
    for (int i = 0; i < (int)(sizeof(Pos) / 8); i++) { x ^= w[i]; x *= 0xff51afd7ed558ccdULL; x ^= x >> 32; }
    return x; }
static int win(const Pos *p, int h, int side) {
    if (overflow) return 0;
    size_t i = hpos(p, h, side) & (tcap - 1);
    while (tab[i].gen == curgen) { if (tab[i].h == h && tab[i].side == side && !memcmp(&tab[i].p, p, sizeof(Pos))) return tab[i].res; i = (i + 1) & (tcap - 1); }
    nodes++;
    Pos ch[MAXMV]; int k = gen(p, side, ch); int cl[MAXMV]; uint8_t cp[MAXMV]; int result = 0;
    memcpy(cp, gcap, k);
    for (int j = 0; j < k; j++) { cl[j] = cls(&ch[j], side); if (cl[j] == 1) { result = 1; break; } }
    for (int pass = 0; pass < 2 && !result; pass++)
        for (int j = 0; j < k && !result; j++) if (cl[j] == 0 && cp[j] == (pass == 0) && !win(&ch[j], h, 1 - side)) result = 1;
    for (int h2 = 0; h2 < h && !result; h2++) if (!win(p, h2, 1 - side)) result = 1;
    if (overflow) return 0;
    i = hpos(p, h, side) & (tcap - 1);
    while (tab[i].gen == curgen) i = (i + 1) & (tcap - 1);
    tab[i].p = *p; tab[i].h = h; tab[i].side = side; tab[i].res = result; tab[i].gen = curgen;
    if (++tcount * 10 > tcap * 7) overflow = 1;
    return result; }
static void table_new(size_t cap) { free(tab); tcap = cap; tab = calloc(tcap, sizeof(Ent)); curgen = 1; tcount = 0; }
/* signature code: bit pair per h: N=0 L=1 R=2 P=3 */
static const char LET[4] = {'N', 'L', 'R', 'P'};
static int solve_pos(const Pos *p, int H) {
    int wp = has_passed(p, 0), bp = has_passed(p, 1);
    if (wp && bp) return -1;
    if (wp || bp) { int code = wp ? 1 : 2, s = 0; for (int h = 0; h <= H; h++) s |= code << (2 * h); return s; }
    for (int fresh = 0;; fresh = 1) {
        overflow = 0; if (fresh) { tcount = 0; curgen++; if (curgen == 0xffffffff) { memset(tab, 0, tcap * sizeof(Ent)); curgen = 1; } }
        int s = 0;
        for (int h = 0; h <= H; h++) { int l = win(p, h, 0), r = win(p, h, 1); s |= (l && r ? 0 : l ? 1 : r ? 2 : 3) << (2 * h); }
        if (!overflow) return s;
        if (fresh) table_new(tcap * 2); } }
static void sigstr(int s, int H, char *o) { for (int h = 0; h <= H; h++) o[h] = LET[(s >> (2 * h)) & 3]; o[H + 1] = 0; }
static int parse(const char *s, Pos *p) {
    memset(p, 0, sizeof *p); p->epf = -1; int f = 0; char buf[1024]; strncpy(buf, s, 1023); buf[1023] = 0;
    char *sv, *t = strtok_r(buf, " \t\r\n", &sv);
    while (t) {
        if (f >= MAXN) return -1;
        if (strcmp(t, "-")) { int c = -1, di = 0;
            for (char *q = t; *q; q++) {
                if (*q == 'W') { c = 0; di = 0; } else if (*q == 'w') { c = 0; di = 1; } else if (*q == 'B') { c = 1; di = 1; } else if (*q == 'b') { c = 1; di = 0; }
                else if (*q >= '1' && *q <= '8' && c >= 0) p->m[c][di][f] |= 1u << (*q - '1'); else return -1; } }
        f++; t = strtok_r(NULL, " \t\r\n", &sv); }
    N = f; return f; }
/* ---- scan ---- */
static FILE *outbin; static long hist[256], nring; static int HH = 3; static long unresolved;
static void ring_cb_fn(const uint8_t *w, const uint8_t *b, void *ctx) {
    (void)ctx; Pos p; memset(&p, 0, sizeof p); p.epf = -1;
    for (int f = 0; f < N; f++) { p.m[0][0][f] = w[f]; p.m[1][1][f] = b[f]; }
    int s = solve_pos(&p, HH); nring++;
    if (s < 0) { unresolved++; s = 255; }
    hist[s]++; if (outbin) fputc(s, outbin);
    char sg[8]; sigstr(s & 255, HH, sg);
    if (s == 255) return;
    if (!strcmp(sg, "NNPN") || !strcmp(sg, "NNNP")) { char t[256]; mr_format(t, w, b, N); printf("HIT %s %s\n", sg, t); fflush(stdout); } }
static int g_argc; static char **g_argv;
static void *real_main(void *a) {
    (void)a; int argc = g_argc; char **argv = g_argv;
    mr_init(); for (int i = 0; i < 256; i++) { MREV[i] = MREV[i]; }
    size_t cap = 1u << 22; const char *mode = argv[1];
    if (getenv("TBITS")) cap = (size_t)1 << atoi(getenv("TBITS"));
    table_new(cap);
    if (!strcmp(mode, "solve")) {
        for (int i = 2; i < argc; i++) { if (!strcmp(argv[i], "--kind")) KIND = atoi(argv[++i]); else if (!strcmp(argv[i], "--H")) HH = atoi(argv[++i]); }
        char line[4096];
        while (fgets(line, sizeof line, stdin)) {
            if (line[0] == '#' || line[0] == '\n') continue;
            Pos p; if (parse(line, &p) < 0) { puts("ERR"); continue; }
            nodes = 0; int s = solve_pos(&p, HH); nodetot += nodes;
            if (s < 0) puts("RACE"); else { char sg[8]; sigstr(s, HH, sg); puts(sg); } }
        fprintf(stderr, "nodes %ld\n", nodetot);
    } else if (!strcmp(mode, "scan")) {
        int n = atoi(argv[2]), P = atoi(argv[3]), ci = 0, ck = 1; const char *out = NULL; KIND = 2; N = n;
        for (int i = 4; i < argc; i++) { if (!strcmp(argv[i], "--chunk")) { ci = atoi(argv[i + 1]); ck = atoi(argv[i + 2]); i += 2; } else if (!strcmp(argv[i], "--out")) out = argv[++i]; }
        if (out) outbin = fopen(out, "wb");
        mr_enum(n, P, ci, ck, ring_cb_fn, NULL);
        if (outbin) fclose(outbin);
        for (int s = 0; s < 256; s++) if (hist[s]) { if (s == 255) printf("HIST UNRESOLVED %ld\n", hist[s]); else { char sg[8]; sigstr(s, HH, sg); printf("HIST %s %ld\n", sg, hist[s]); } }
        printf("RINGS %ld\n", nring); }
    return NULL; }
int main(int argc, char **argv) {
    g_argc = argc; g_argv = argv; pthread_attr_t at; pthread_attr_init(&at); pthread_attr_setstacksize(&at, (size_t)1 << 29);
    pthread_t t; pthread_create(&t, &at, real_main, NULL); pthread_join(t, NULL); return 0; }
