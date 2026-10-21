#!/usr/bin/env python3
"""Generate all legal KPK positions on 8x8 board (flat or cylinder)."""

import itertools
import sys

FILES = 8
RANKS = 8
N = FILES * RANKS

def sq_name(f, r):
    return chr(ord('a') + f) + str(r + 1)

def sq_index(name):
    f = ord(name[0]) - ord('a')
    r = int(name[1:]) - 1
    return r * FILES + f

def square_from_index(idx):
    f = idx % FILES
    r = idx // FILES
    return f, r

def king_attacks(sq, wrap):
    """Squares attacked by a king on sq."""
    f, r = square_from_index(sq)
    attacks = []
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == 0 and dr == 0:
                continue
            nf = f + df
            nr = r + dr
            if not (0 <= nr < RANKS):
                continue
            if wrap:
                nf = nf % FILES
            elif not (0 <= nf < FILES):
                continue
            attacks.append(nr * FILES + nf)
    return attacks

def is_legal_kpk(wk, wp, bk, stm, wrap):
    """Check if a KPK position is legal."""
    # No overlapping pieces
    if len({wk, wp, bk}) != 3:
        return False
    
    # Kings not adjacent
    if bk in king_attacks(wk, wrap):
        return False
    
    # Pawn not on first or last rank
    wp_f, wp_r = square_from_index(wp)
    if wp_r == 0 or wp_r == RANKS - 1:
        return False
    
    # Side not to move not in check
    if stm == 'w':
        # Black just moved, so White king shouldn't be in check
        if wk in king_attacks(bk, wrap):
            return False
        # Also check if black pawn attacks... but there's no black pawn in KPK
    else:
        # White just moved, so Black king shouldn't be in check
        if bk in king_attacks(wk, wrap):
            return False
        # Check if white pawn attacks black king
        wp_f, wp_r = square_from_index(wp)
        bk_f, bk_r = square_from_index(bk)
        # White pawn attacks diagonally forward
        for df in (-1, 1):
            nf = wp_f + df
            if wrap:
                nf = nf % FILES
            elif not (0 <= nf < FILES):
                continue
            if nf == bk_f and wp_r + 1 == bk_r:
                return False
    
    return True

def generate_kpk_positions(wrap=True):
    """Generate all legal KPK positions."""
    positions = []
    
    for wk in range(N):
        for wp in range(N):
            if wk == wp:
                continue
            wp_f, wp_r = square_from_index(wp)
            if wp_r == 0 or wp_r == RANKS - 1:
                continue
            for bk in range(N):
                if bk in (wk, wp):
                    continue
                for stm in ('w', 'b'):
                    if is_legal_kpk(wk, wp, bk, stm, wrap):
                        wk_name = sq_name(*square_from_index(wk))
                        wp_name = sq_name(*square_from_index(wp))
                        bk_name = sq_name(*square_from_index(bk))
                        pos_str = f"K{wk_name} P{wp_name} k{bk_name} {stm} -"
                        positions.append(pos_str)
    
    return positions

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'flat':
        wrap = False
    else:
        wrap = True
    
    positions = generate_kpk_positions(wrap)
    print(f"Generated {len(positions)} legal KPK positions (wrap={wrap})", file=sys.stderr)
    
    for pos in positions:
        print(pos)

if __name__ == '__main__':
    main()