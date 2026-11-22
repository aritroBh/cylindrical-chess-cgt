/* mob2.c -- C2: independent solver of the same game, different encoding and recursion from mob1.c.
 *   * Geometry: the strip is handled as its double cover, a straight cylinder with 2N files, on which every pawn has a
 *     twin lift (file+N, rank 9-r, direction -D).  All geometry (capture targets, "ahead", seam) is done on cover
 *     coordinates; the stored state is the cell array of the chart files 0..N-1 only (twin lifts are implied).
 *     Cell codes: 1 white up, 2 white down, 3 black up, 4 black down (D = direction in the cover).
 *   * Recursion: one memo entry per position holds the outcome bits of BOTH movers for ALL heaps h = 0..3 (8 bits);
 *     moves into positions where the opponent has an immediate winning move are skipped (they lose for every h).
 *   * e.p.: always recorded after a double step; a pawn is protected only if the holder can really capture it now.
 * Modes as mob1:  solve [--kind K], scan N P [--chunk i k] [--out f].
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <pthread.h>
#include "mring.h"
#define MAXN 8
#define MAXMV 160
typedef struct { uint8_t cell[MAXN][8]; int8_t epf; uint8_t epr, eph, pad; } P2;
static int N, KIND = 2, HH = 3;
static inline int colof(int cd) { return (cd - 1) >> 1; }
static inline int dirof(int cd) { return ((cd - 1) & 1) ? -1 : 1; }
static inline int mkcode(int c, int D) { return 1 + 2 * c + (D < 0); }
static inline int flipdir(int cd) { return ((cd - 1) ^ 1) + 1; }
static inline int clen(void) { return KIND == 2 ? 2 * N : N; }
static int code_at(const P2 *p, int F, int R) {
    if (R < 1 || R > 8) return 0;
    if (KIND == 0) { if (F < 0 || F >= N) return 0; return p->cell[F][R - 1]; }
    int L = clen(); F %= L; if (F < 0) F += L;
    if (F < N) return p->cell[F][R - 1];
    int c = p->cell[F - N][8 - R]; return c ? flipdir(c) : 0; }
/* chart coordinates of the lift at cover coordinates (F,R,D) */
static void norm(int F, int R, int D, int *f, int *r, int *Dn) {
    if (KIND == 0) { *f = F; *r = R; *Dn = D; return; }
    int L = clen(); F %= L; if (F < 0) F += L;
    if (F < N) { *f = F; *r = R; *Dn = D; } else { *f = F - N; *r = 9 - R; *Dn = -D; } }
static int same_cover(int F1, int R1, int F2, int R2) {
    if (R1 != R2) return 0;
    if (KIND == 0) return F1 == F2;
    int L = clen(); return (((F1 - F2) % L) + L) % L == 0; }
static int is_blocked(const P2 *p, int c, int F, int R, int D) {
    for (int dF = -1; dF <= 1; dF++) for (int RR = R + D; RR >= 1 && RR <= 8; RR += D) { int cd = code_at(p, F + dF, RR); if (cd && colof(cd) != c) return 1; }
    return 0; }
/* can the holder really take the stepper e.p. now? */
static int ep_capturable(const P2 *p) {
    int cd = p->cell[p->epf][p->epr - 1]; int Ds = dirof(cd); int sk = p->epr - Ds;
    for (int f = 0; f < N; f++) for (int r = 1; r <= 8; r++) {
        int q = p->cell[f][r - 1]; if (!q || colof(q) != p->eph) continue; int D = dirof(q);
        for (int dF = -1; dF <= 1; dF += 2) {
            int TF = f + dF, TR = r + D;
            if (same_cover(TF, TR, p->epf, sk)) return 1;
            if (KIND == 2 && same_cover(TF, TR, p->epf + N, 9 - sk)) return 1; } }
    return 0; }
static int passed_at(const P2 *p, int f, int r) {   /* chart pawn at (f,r) is a passed pawn (not e.p.-protected) */
    int cd = p->cell[f][r - 1]; int c = colof(cd), D = dirof(cd);
    if (is_blocked(p, c, f, r, D)) return 0;
    if (p->epf == f && p->epr == r && p->eph != c && ep_capturable(p)) return 0;
    return 1; }
static int any_passed(const P2 *p, int c) {
    for (int f = 0; f < N; f++) for (int r = 1; r <= 8; r++) { int cd = p->cell[f][r - 1]; if (cd && colof(cd) == c && passed_at(p, f, r)) return 1; }
    return 0; }
static int dist_of(const P2 *p, int c) {
    int best = 1000000;
    for (int f = 0; f < N; f++) for (int r = 1; r <= 8; r++) {
        int cd = p->cell[f][r - 1]; if (!cd || colof(cd) != c || !passed_at(p, f, r)) continue;
        int D = dirof(cd), front = 1;
        for (int RR = r + D; RR >= 1 && RR <= 8; RR += D) if (p->cell[f][RR - 1]) front = 0;
        if (!front) continue;
        int d = D > 0 ? 8 - r - (r == 2) : r - 1 - (r == 7);
        if (d < best) best = d; }
    return best; }
static int cls(const P2 *c, int mover) {
    int wp = any_passed(c, 0), bp = any_passed(c, 1);
    if (!wp && !bp) return 0;
    if (wp && bp) { int o = 1 - mover; int w = dist_of(c, o) <= dist_of(c, mover) ? o : mover; return w == mover ? 1 : -1; }
    return (wp ? 0 : 1) == mover ? 1 : -1; }
static void setcell(P2 *q, int f, int r, int cd) { q->cell[f][r - 1] = cd; }
static int gen(const P2 *p, int c, P2 *out) {
    int k = 0;
    for (int f = 0; f < N; f++) for (int r = 1; r <= 8; r++) {
        int cd = p->cell[f][r - 1]; if (!cd || colof(cd) != c) continue;
        int D = dirof(cd), R1 = r + D; if (R1 < 1 || R1 > 8) continue;
        if (!p->cell[f][R1 - 1]) {
            P2 q = *p; q.epf = -1; q.epr = q.eph = 0; setcell(&q, f, r, 0); setcell(&q, f, R1, cd); out[k++] = q;
            int R2 = r + 2 * D, home = D > 0 ? 2 : 7;
            if (r == home && !p->cell[f][R2 - 1]) {
                P2 q2 = *p; q2.epf = f; q2.epr = R2; q2.eph = 1 - c; setcell(&q2, f, r, 0); setcell(&q2, f, R2, cd); out[k++] = q2; } }
        for (int dF = -1; dF <= 1; dF += 2) {
            int TF = f + dF, TR = r + D; int tc = code_at(p, TF, TR);
            int isep = 0;
            if (!tc && p->epf >= 0 && p->eph == c) {
                int cs = p->cell[p->epf][p->epr - 1]; int sk = p->epr - dirof(cs);
                if (same_cover(TF, TR, p->epf, sk) || (KIND == 2 && same_cover(TF, TR, p->epf + N, 9 - sk))) isep = 1; }
            if (!((tc && colof(tc) != c) || isep)) continue;
            if (KIND == 0 && (TF < 0 || TF >= N)) continue;
            P2 q = *p; q.epf = -1; q.epr = q.eph = 0; setcell(&q, f, r, 0);
            int vf, vr, vD;
            if (isep) { setcell(&q, p->epf, p->epr, 0); }
            else { norm(TF, TR, D, &vf, &vr, &vD); setcell(&q, vf, vr, 0); }
            norm(TF, TR, D, &vf, &vr, &vD); setcell(&q, vf, vr, mkcode(c, vD)); out[k++] = q; } }
    return k; }
static int imm_win(const P2 *p, int side) {
    P2 ch[MAXMV]; int k = gen(p, side, ch);
    for (int j = 0; j < k; j++) if (cls(&ch[j], side) == 1) return 1;
    return 0; }
typedef struct { P2 p; uint8_t res; uint32_t gen; } Ent;
static Ent *tab; static size_t tcap, tcount; static uint32_t curgen = 1; static int overflow; static long nodes;
static inline uint64_t hp(const P2 *p) {
    const uint8_t *b = (const uint8_t *)p; uint64_t x = 1469598103934665603ULL;
    for (size_t i = 0; i < sizeof(P2); i++) { x ^= b[i]; x *= 1099511628211ULL; } x ^= x >> 29; return x; }
/* bits 0..3: Left (white) to move wins in P+*h; bits 4..7: Right to move wins */
static uint8_t both(const P2 *p) {
    if (overflow) return 0;
    size_t i = hp(p) & (tcap - 1);
    while (tab[i].gen == curgen) { if (!memcmp(&tab[i].p, p, sizeof(P2))) return tab[i].res; i = (i + 1) & (tcap - 1); }
    nodes++;
    unsigned opt[2] = {0, 0};
    for (int side = 0; side < 2; side++) {
        P2 ch[MAXMV]; int k = gen(p, side, ch);
        for (int j = 0; j < k && opt[side] != 15; j++) {
            int cl = cls(&ch[j], side);
            if (cl == 1) { opt[side] = 15; break; }
            if (cl < 0) continue;
            if (imm_win(&ch[j], 1 - side)) continue;
            unsigned rc = both(&ch[j]);
            opt[side] |= ~(rc >> (4 * (1 - side))) & 15; } }
    unsigned w[2] = {0, 0};
    for (int h = 0; h < 4; h++) for (int side = 0; side < 2; side++) {
        int win = (opt[side] >> h) & 1;
        for (int h2 = 0; h2 < h && !win; h2++) if (!((w[1 - side] >> h2) & 1)) win = 1;
        if (win) w[side] |= 1u << h; }
    /* side 0 uses w[1] at lower h only; computed above in the same h pass order (w[1][h2<h] already final) */
    uint8_t res = w[0] | (w[1] << 4);
    if (overflow) return 0;
    i = hp(p) & (tcap - 1);
    while (tab[i].gen == curgen) i = (i + 1) & (tcap - 1);
    tab[i].p = *p; tab[i].res = res; tab[i].gen = curgen;
    if (++tcount * 10 > tcap * 7) overflow = 1;
    return res; }
static void table_new(size_t cap) { free(tab); tcap = cap; tab = calloc(tcap, sizeof(Ent)); curgen = 1; tcount = 0; }
static const char LET[4] = {'N', 'L', 'R', 'P'};
static int solve_pos(const P2 *p) {
    int wp = any_passed(p, 0), bp = any_passed(p, 1);
    if (wp && bp) return -1;
    if (wp || bp) { int code = wp ? 1 : 2, s = 0; for (int h = 0; h <= HH; h++) s |= code << (2 * h); return s; }
    for (int fresh = 0;; fresh = 1) {
        overflow = 0; if (fresh) { tcount = 0; curgen++; }
        unsigned r = both(p);
        if (!overflow) { int s = 0; for (int h = 0; h <= HH; h++) { int l = (r >> h) & 1, rr = (r >> (4 + h)) & 1; s |= (l && rr ? 0 : l ? 1 : rr ? 2 : 3) << (2 * h); } return s; }
        if (fresh) table_new(tcap * 2); } }
static void sigstr(int s, char *o) { for (int h = 0; h <= HH; h++) o[h] = LET[(s >> (2 * h)) & 3]; o[HH + 1] = 0; }
static int parse(const char *s, P2 *p) {
    memset(p, 0, sizeof *p); p->epf = -1; int f = 0; char buf[1024]; strncpy(buf, s, 1023); buf[1023] = 0;
    char *sv, *t = strtok_r(buf, " \t\r\n", &sv);
    while (t) {
        if (f >= MAXN) return -1;
        if (strcmp(t, "-")) { int cd = 0;
            for (char *q = t; *q; q++) {
                if (*q == 'W') cd = 1; else if (*q == 'w') cd = 2; else if (*q == 'b') cd = 3; else if (*q == 'B') cd = 4;
                else if (*q >= '1' && *q <= '8' && cd) p->cell[f][*q - '1'] = cd; else return -1; } }
        f++; t = strtok_r(NULL, " \t\r\n", &sv); }
    N = f; return f; }
static FILE *outbin; static long hist[256], nring, unresolved;
static void ring_cb_fn(const uint8_t *w, const uint8_t *b, void *ctx) {
    (void)ctx; P2 p; memset(&p, 0, sizeof p); p.epf = -1;
    for (int f = 0; f < N; f++) for (int r = 1; r <= 8; r++) { if (w[f] >> (r - 1) & 1) p.cell[f][r - 1] = 1; if (b[f] >> (r - 1) & 1) p.cell[f][r - 1] = 4; }
    int s = solve_pos(&p); nring++;
    if (s < 0) { unresolved++; s = 255; }
    hist[s]++; if (outbin) fputc(s, outbin);
    if (s == 255) return;
    char sg[8]; sigstr(s, sg);
    if (!strcmp(sg, "NNPN") || !strcmp(sg, "NNNP")) { char t[256]; mr_format(t, w, b, N); printf("HIT %s %s\n", sg, t); fflush(stdout); } }
static int g_argc; static char **g_argv;
static void *real_main(void *a) {
    (void)a; int argc = g_argc; char **argv = g_argv; mr_init();
    size_t cap = 1u << 21; const char *mode = argv[1];
    if (getenv("TBITS")) cap = (size_t)1 << atoi(getenv("TBITS"));
    table_new(cap);
    if (!strcmp(mode, "solve")) {
        for (int i = 2; i < argc; i++) { if (!strcmp(argv[i], "--kind")) KIND = atoi(argv[++i]); else if (!strcmp(argv[i], "--H")) HH = atoi(argv[++i]); }
        char line[4096];
        while (fgets(line, sizeof line, stdin)) {
            if (line[0] == '#' || line[0] == '\n') continue;
            P2 p; if (parse(line, &p) < 0) { puts("ERR"); continue; }
            int s = solve_pos(&p); if (s < 0) puts("RACE"); else { char sg[8]; sigstr(s, sg); puts(sg); } }
    } else if (!strcmp(mode, "scan")) {
        int n = atoi(argv[2]), P = atoi(argv[3]), ci = 0, ck = 1; const char *out = NULL; KIND = 2; N = n;
        for (int i = 4; i < argc; i++) { if (!strcmp(argv[i], "--chunk")) { ci = atoi(argv[i + 1]); ck = atoi(argv[i + 2]); i += 2; } else if (!strcmp(argv[i], "--out")) out = argv[++i]; }
        if (out) outbin = fopen(out, "wb");
        mr_enum(n, P, ci, ck, ring_cb_fn, NULL);
        if (outbin) fclose(outbin);
        for (int s = 0; s < 256; s++) if (hist[s]) { if (s == 255) printf("HIST UNRESOLVED %ld\n", hist[s]); else { char sg[8]; sigstr(s, sg); printf("HIST %s %ld\n", sg, hist[s]); } }
        printf("RINGS %ld\n", nring); }
    return NULL; }
int main(int argc, char **argv) {
    g_argc = argc; g_argv = argv; pthread_attr_t at; pthread_attr_init(&at); pthread_attr_setstacksize(&at, (size_t)1 << 29);
    pthread_t t; pthread_create(&t, &at, real_main, NULL); pthread_join(t, NULL); return 0; }
