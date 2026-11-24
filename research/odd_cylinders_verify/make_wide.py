#!/usr/bin/env python3
"""Build a 128-bit variant of kings/kpsolve.c that supports up to 10 files.

The stock solver (kings/kpsolve.c) uses uint64_t bitboards, which is enough for
the 8x8 board (64 squares) but not for a 9- or 10-file cylinder.  This script
applies a mechanical widening to a *copy* of the stock source; the stock file
is never touched.

Two things have to be widened:
  * the bitboards and the square-indexed tables (64 -> 128 entries),
  * the ray tables: on a W-file cylinder a horizontal ray has W-1 squares, so
    the per-ray arrays must hold 16, not 8.  (Keeping the stock size of 8
    would overflow the buffer for W >= 10; the copy below uses 16 so that it
    is safe for every W <= 10.)

The hashing code needs explicit casts back to uint64_t, because the stock
expression `k->wp * 0x9E37...` would be evaluated in 128-bit arithmetic.

Usage:  python3 make_wide.py ../.. kings/kpsolve.c > kpsolve_wide.c
"""

import re
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else '../../kings/kpsolve.c'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'kpsolve_wide.c'

text = open(SRC).read()

REPL = [
    # --- bitboard type -------------------------------------------------
    ('#define BIT(s) (1ULL << (s))',
     'typedef unsigned __int128 u128;\n#define BIT(s) ((u128)1 << (s))'),
    # --- square-indexed tables ----------------------------------------
    ('static int kingN[64], kingL[64][8], knightN[64], knightL[64][8];',
     'static int kingN[128], kingL[128][8], knightN[128], knightL[128][8];'),
    ('static uint64_t kingBB[64], knightBB[64];',
     'static u128 kingBB[128], knightBB[128];'),
    ('static uint64_t pawnAtt[2][64]; /* squares from which a pawn of colour c attacks s */',
     'static u128 pawnAtt[2][128]; /* squares from which a pawn of colour c attacks s */'),
    ('static int capN[2][64], capL[2][64][2];',
     'static int capN[2][128], capL[2][128][2];'),
    ('static int rayN[64][8], rayL[64][8][8];',
     'static int rayN[128][8], rayL[128][8][16];'),
    ('static int8_t rayIdx[64][8][64];',
     'static int8_t rayIdx[128][8][128];'),
    ('static uint64_t rayBefore[64][8][8];',
     'static u128 rayBefore[128][8][16];'),
    # --- positions and keys -------------------------------------------
    ('  uint64_t wp, bp;\n  int wk, bk, no, stm, ep;',
     '  u128 wp, bp;\n  int wk, bk, no, stm, ep;'),
    ('  uint64_t wp, bp;\n  int no;',
     '  u128 wp, bp;\n  int no;'),
    ('static uint64_t occupancy(const Pos *p) {\n  uint64_t o',
     'static u128 occupancy(const Pos *p) {\n  u128 o'),
    ('static int man_attacks(int type, int from, int target, uint64_t occ) {',
     'static int man_attacks(int type, int from, int target, u128 occ) {'),
    ('      uint64_t before = 0;', '      u128 before = 0;'),
    ('  uint64_t occ = occupancy(p);', '  u128 occ = occupancy(p);'),
    ('  uint64_t seen = p->wp | p->bp;', '  u128 seen = p->wp | p->bp;'),
    ('  uint64_t *pp = victim == BLACK ? &q->bp : &q->wp;',
     '  u128 *pp = victim == BLACK ? &q->bp : &q->wp;'),
    ('  uint64_t ownP = us == BLACK ? p->bp : p->wp, oppP = us == BLACK ? p->wp : p->bp;',
     '  u128 ownP = us == BLACK ? p->bp : p->wp, oppP = us == BLACK ? p->wp : p->bp;'),
    ('  uint64_t ownO = 0, oppO = 0;', '  u128 ownO = 0, oppO = 0;'),
    ('  uint64_t occ = p->wp | p->bp | ownO | oppO | BIT(ok) | BIT(ek);',
     '  u128 occ = p->wp | p->bp | ownO | oppO | BIT(ok) | BIT(ek);'),
    ('  uint64_t ownAll = ownP | ownO | BIT(ok);',
     '  u128 ownAll = ownP | ownO | BIT(ok);'),
    ('    uint64_t dest = 0;', '    u128 dest = 0;'),
    # --- hashing: force 64-bit arithmetic ------------------------------
    ('  uint64_t h = k->wp * 0x9E3779B97F4A7C15ULL ^ (k->bp + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL;',
     '  uint64_t h = (uint64_t)k->wp * 0x9E3779B97F4A7C15ULL\n'
     '             ^ ((uint64_t)k->bp + 0x632BE59BD9B4E019ULL) * 0xC2B2AE3D27D4EB4FULL;'),
    # --- allow 9 and 10 files -----------------------------------------
    ('if (!boardSet || W < 2 || W > 8 || H < 4 || H > 8',
     'if (!boardSet || W < 2 || W > 10 || H < 4 || H > 8'),
]

for old, new in REPL:
    if old not in text:
        raise SystemExit('pattern not found:\n%s' % old)
    if text.count(old) != 1 and 'uint64_t h = k->wp' not in old:
        raise SystemExit('pattern not unique (%d):\n%s' % (text.count(old), old))
    text = text.replace(old, new)

assert 'uint64_t wp, bp' not in text
assert text.count('static int8_t rayIdx[128][8][128];') == 1
open(OUT, 'w').write(text)
print('wrote %s' % OUT)
