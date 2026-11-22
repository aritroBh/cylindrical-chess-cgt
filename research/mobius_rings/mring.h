/* mring.h -- enumeration of Moebius ROOT rings (default directions, ranks 2..7, a pawn on every file,
 * no passed pawn), up to the group {id, mirror, kappa, mirror*kappa} (see REPORT.md).
 * A ring is a sequence of per-file configurations (white rank set, black rank set), bit (r-1) = rank r.
 * Passed test on the strip (twist): the neighbour across the seam (file n-1 seen from file 0, and file 0 seen
 * from file n-1) is read with ranks flipped r -> 9-r.
 * Pre-filter (provable): white ranks 2..6, black ranks 3..7 (a white pawn on rank 7 is blocked only by an enemy
 * pawn on rank 8, or on rank 1 across the seam; no root pawn stands on rank 1 or 8; same for black on rank 2).
 */
#ifndef MRING_H
#define MRING_H
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef struct { uint8_t w, b, cw, cb, hiW, loW, hiB, loB; } MCfg;
static MCfg mcfg[512]; static int mncfg; static int mkap[512];
static uint8_t MREV[256];
static void mr_init(void) {
    for (int i = 0; i < 256; i++) { int r = 0; for (int k = 0; k < 8; k++) if (i >> k & 1) r |= 1 << (7 - k); MREV[i] = r; }
    mncfg = 0;
    for (int w = 0; w < 256; w++) { if (w & ~0x3E) continue;            /* ranks 2..6: bits 1..5 */
        for (int b = 0; b < 256; b++) { if (b & ~0x7C) continue;        /* ranks 3..7: bits 2..6 */
            if ((w & b) || !(w | b)) continue;
            MCfg c; memset(&c, 0, sizeof c); c.w = w; c.b = b; c.loW = 9; c.loB = 9;
            for (int r = 1; r <= 8; r++) {
                if (w >> (r - 1) & 1) { c.cw++; if (r > c.hiW) c.hiW = r; if (r < c.loW) c.loW = r; }
                if (b >> (r - 1) & 1) { c.cb++; if (r > c.hiB) c.hiB = r; if (r < c.loB) c.loB = r; } }
            mcfg[mncfg++] = c; } }
    for (int i = 0; i < mncfg; i++) { int w = MREV[mcfg[i].b], b = MREV[mcfg[i].w]; mkap[i] = -1;
        for (int j = 0; j < mncfg; j++) if (mcfg[j].w == w && mcfg[j].b == b) mkap[i] = j; }
}
typedef void (*ring_cb)(const uint8_t *w, const uint8_t *b, void *ctx);
static int MN, MP, MCI, MCK, MCD; static long mprefix; static int mseq[16]; static ring_cb MCB; static void *MCTX;
static long mcount;
static int m_white_ok(int f) {
    const MCfg *c = &mcfg[mseq[f]]; if (!c->cw) return 1;
    const MCfg *L = &mcfg[mseq[(f + MN - 1) % MN]], *R = &mcfg[mseq[(f + 1) % MN]];
    int mb = c->hiB, v;
    v = f == 0 ? 9 - L->loB : L->hiB; if (v > mb) mb = v;
    v = f == MN - 1 ? 9 - R->loB : R->hiB; if (v > mb) mb = v;
    return c->hiW < mb;
}
static int m_black_ok(int f) {
    const MCfg *c = &mcfg[mseq[f]]; if (!c->cb) return 1;
    const MCfg *L = &mcfg[mseq[(f + MN - 1) % MN]], *R = &mcfg[mseq[(f + 1) % MN]];
    int mw = c->loW, v;
    v = f == 0 ? 9 - L->hiW : L->loW; if (v < mw) mw = v;
    v = f == MN - 1 ? 9 - R->hiW : R->loW; if (v < mw) mw = v;
    return c->loB > mw;
}
static int m_canon(void) {
    for (int im = 1; im < 4; im++) {
        int cmp = 0;
        for (int f = 0; f < MN && !cmp; f++) {
            int g = (im & 1) ? mseq[MN - 1 - f] : mseq[f];
            if (im & 2) g = mkap[g];
            if (g < mseq[f]) cmp = -1; else if (g > mseq[f]) cmp = 1; }
        if (cmp < 0) return 0; }
    return 1;
}
static void m_rec(int f, int used) {
    if (f == MN) {
        if (used != MP) return;
        if (!m_white_ok(MN - 1) || !m_black_ok(MN - 1) || !m_white_ok(0) || !m_black_ok(0)) return;
        if (!m_canon()) return;
        uint8_t w[16], b[16]; for (int i = 0; i < MN; i++) { w[i] = mcfg[mseq[i]].w; b[i] = mcfg[mseq[i]].b; }
        mcount++; MCB(w, b, MCTX); return; }
    int remf = MN - f - 1;
    for (int i = 0; i < mncfg; i++) {
        int pc = mcfg[i].cw + mcfg[i].cb;
        if (used + pc + remf > MP) continue;
        if (f == MN - 1 && used + pc != MP) continue;
        mseq[f] = i;
        if (f >= 2 && (!m_white_ok(f - 1) || !m_black_ok(f - 1))) continue;
        if (f == MCD - 1) { long idx = mprefix++; if (idx % MCK != MCI) continue; }
        m_rec(f + 1, used + pc);
    }
}
static long mr_enum(int n, int P, int ci, int ck, ring_cb cb, void *ctx) {
    MN = n; MP = P; MCI = ci; MCK = ck; MCB = cb; MCTX = ctx; MCD = n - 1 < 4 ? n - 1 : 4; mprefix = 0; mcount = 0;
    m_rec(0, 0); return mcount;
}
static void mr_format(char *out, const uint8_t *w, const uint8_t *b, int n) {
    char *o = out;
    for (int f = 0; f < n; f++) {
        if (f) *o++ = ' ';
        if (w[f]) { *o++ = 'W'; for (int r = 1; r <= 8; r++) if (w[f] >> (r - 1) & 1) *o++ = '0' + r; }
        if (b[f]) { *o++ = 'B'; for (int r = 1; r <= 8; r++) if (b[f] >> (r - 1) & 1) *o++ = '0' + r; }
        if (!w[f] && !b[f]) *o++ = '-'; }
    *o = 0;
}
#endif
