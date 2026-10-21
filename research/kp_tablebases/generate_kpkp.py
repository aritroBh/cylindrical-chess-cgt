#!/usr/bin/env python3
"""Generate all legal KPKP positions on 8x8 board (flat or cylinder)."""

import itertools
import sys

FILES = 8
RANKS = 8
N = FILES * RANKS

def sq_name(f, r):
    return chr(ord('a') + f) + str(r + 1)

def square_from_index(idx):
    f = idx % FILES
    r = idx // FILES
    return f, r

def king_attacks(sq, wrap):
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

def pawn_attacks(sq, color, wrap):
    """Squares attacked by a pawn of given color."""
    f, r = square_from_index(sq)
    attacks = []
    if color == 'w':
        dr = 1
    else:
        dr = -1
    for df in (-1, 1):
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

def is_legal_kpkp(wk, wp1, wp2, bk, bp, stm, wrap):
    """Check if a KPKP position is legal."""
    pieces = [wk, wp1, wp2, bk, bp]
    if len(set(pieces)) != 5:
        return False
    
    # Kings not adjacent
    if bk in king_attacks(wk, wrap):
        return False
    
    # Pawns not on first or last rank
    for wp in [wp1, wp2]:
        wp_f, wp_r = square_from_index(wp)
        if wp_r == 0 or wp_r == RANKS - 1:
            return False
    bp_f, bp_r = square_from_index(bp)
    if bp_r == 0 or bp_r == RANKS - 1:
        return False
    
    # Side not to move not in check
    if stm == 'w':
        # Black just moved, so White king shouldn't be in check
        if wk in king_attacks(bk, wrap):
            return False
        # Check if black pawn attacks white king
        if wk in pawn_attacks(bp, 'b', wrap):
            return False
    else:
        # White just moved, so Black king shouldn't be in check
        if bk in king_attacks(wk, wrap):
            return False
        # Check if white pawns attack black king
        if bk in pawn_attacks(wp1, 'w', wrap) or bk in pawn_attacks(wp2, 'w', wrap):
            return False
    
    # Pawns on same file: if they're adjacent, they block each other
    # This is legal but we need to handle it
    # Actually, pawns can be on same file as long as not on same square
    
    return True

def generate_kpkp_positions(wrap=True):
    """Generate all legal KPKP positions."""
    positions = []
    count = 0
    
    # To reduce symmetry, we can order white pawns
    for wk in range(N):
        for wp1 in range(N):
            if wp1 == wk:
                continue
            wp1_f, wp1_r = square_from_index(wp1)
            if wp1_r == 0 or wp1_r == RANKS - 1:
                continue
            for wp2 in range(wp1 + 1, N):  # Order to avoid duplicates
                if wp2 == wk:
                    continue
                wp2_f, wp2_r = square_from_index(wp2)
                if wp2_r == 0 or wp2_r == RANKS - 1:
                    continue
                for bk in range(N):
                    if bk in (wk, wp1, wp2):
                        continue
                    for bp in range(N):
                        if bp in (wk, wp1, wp2, bk):
                            continue
                        bp_f, bp_r = square_from_index(bp)
                        if bp_r == 0 or bp_r == RANKS - 1:
                            continue
                        for stm in ('w', 'b'):
                            if is_legal_kpkp(wk, wp1, wp2, bk, bp, stm, wrap):
                                wk_name = sq_name(*square_from_index(wk))
                                wp1_name = sq_name(*square_from_index(wp1))
                                wp2_name = sq_name(*square_from_index(wp2))
                                bk_name = sq_name(*square_from_index(bk))
                                bp_name = sq_name(*square_from_index(bp))
                                pos_str = f"K{wk_name} P{wp1_name} P{wp2_name} k{bk_name} p{bp_name} {stm} -"
                                positions.append(pos_str)
                                count += 1
                                if count % 100000 == 0:
                                    print(f"Generated {count} positions...", file=sys.stderr)
    
    print(f"Generated {count} legal KPKP positions (wrap={wrap})", file=sys.stderr)
    return positions

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'flat':
        wrap = False
    else:
        wrap = True
    
    positions = generate_kpkp_positions(wrap)
    
    for pos in positions:
        print(pos)

if __name__ == '__main__':
    main()