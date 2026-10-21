#!/usr/bin/env python3
"""Fast KPKP position generator using bitboards."""

import sys

FILES = 8
RANKS = 8
N = FILES * RANKS

# Precompute king attacks
KING_ATTACKS_FLAT = [[] for _ in range(N)]
KING_ATTACKS_CYL = [[] for _ in range(N)]
PAWN_ATTACKS_W = [[], []]  # [flat, cyl]
PAWN_ATTACKS_B = [[], []]

def sq_name(f, r):
    return chr(ord('a') + f) + str(r + 1)

def square_from_index(idx):
    return idx % FILES, idx // FILES

def precompute():
    for sq in range(N):
        f, r = square_from_index(sq)
        # King attacks flat
        attacks = []
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == 0 and dr == 0:
                    continue
                nf, nr = f + df, r + dr
                if 0 <= nf < FILES and 0 <= nr < RANKS:
                    attacks.append(nr * FILES + nf)
        KING_ATTACKS_FLAT[sq] = attacks
        
        # King attacks cylinder
        attacks = []
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == 0 and dr == 0:
                    continue
                nf, nr = (f + df) % FILES, r + dr
                if 0 <= nr < RANKS:
                    attacks.append(nr * FILES + nf)
        KING_ATTACKS_CYL[sq] = attacks
        
        # Pawn attacks white
        for wrap in (0, 1):
            attacks = []
            for df in (-1, 1):
                nf = (f + df) % FILES if wrap else f + df
                nr = r + 1
                if 0 <= nf < FILES and 0 <= nr < RANKS:
                    attacks.append(nr * FILES + nf)
            PAWN_ATTACKS_W[wrap].append(attacks)
            
            # Pawn attacks black
            attacks = []
            for df in (-1, 1):
                nf = (f + df) % FILES if wrap else f + df
                nr = r - 1
                if 0 <= nf < FILES and 0 <= nr < RANKS:
                    attacks.append(nr * FILES + nf)
            PAWN_ATTACKS_B[wrap].append(attacks)

precompute()

def generate_kpkp_fast(wrap=True, output_file=None):
    """Generate KPKP positions efficiently."""
    king_attacks = KING_ATTACKS_CYL if wrap else KING_ATTACKS_FLAT
    pawn_att_w = PAWN_ATTACKS_W[1 if wrap else 0]
    pawn_att_b = PAWN_ATTACKS_B[1 if wrap else 0]
    
    # Valid pawn squares (not on rank 1 or 8)
    valid_pawn_squares = [sq for sq in range(N) if 1 <= sq // FILES <= 6]
    
    count = 0
    out = open(output_file, 'w') if output_file else sys.stdout
    
    for wk in range(N):
        wk_attacks = king_attacks[wk]
        for wp1 in valid_pawn_squares:
            if wp1 == wk:
                continue
            for wp2 in valid_pawn_squares:
                if wp2 <= wp1 or wp2 == wk:
                    continue
                # White pawn attacks
                wp1_att = pawn_att_w[wp1]
                wp2_att = pawn_att_w[wp2]
                white_pawn_attacks = set(wp1_att) | set(wp2_att)
                
                for bk in range(N):
                    if bk in (wk, wp1, wp2):
                        continue
                    if bk in wk_attacks:  # Kings adjacent
                        continue
                    if bk in white_pawn_attacks:  # Black king in check from white pawn
                        continue
                    
                    bk_attacks = king_attacks[bk]
                    if wk in bk_attacks:  # Kings adjacent (redundant check)
                        continue
                    
                    for bp in valid_pawn_squares:
                        if bp in (wk, wp1, wp2, bk):
                            continue
                        if bp in bk_attacks:  # Black pawn attacks white king? No, black pawn attacks down
                            pass
                        # Check black pawn attacks white king
                        if wk in pawn_att_b[bp]:
                            continue
                        
                        # Both sides to move
                        for stm in ('w', 'b'):
                            if stm == 'w':
                                # Black just moved, white king not in check
                                if wk in bk_attacks:
                                    continue
                                if wk in pawn_att_b[bp]:
                                    continue
                            else:
                                # White just moved, black king not in check
                                if bk in wk_attacks:
                                    continue
                                if bk in white_pawn_attacks:
                                    continue
                            
                            wk_name = sq_name(*square_from_index(wk))
                            wp1_name = sq_name(*square_from_index(wp1))
                            wp2_name = sq_name(*square_from_index(wp2))
                            bk_name = sq_name(*square_from_index(bk))
                            bp_name = sq_name(*square_from_index(bp))
                            out.write(f"K{wk_name} P{wp1_name} P{wp2_name} k{bk_name} p{bp_name} {stm} -\n")
                            count += 1
                            
                            if count % 1000000 == 0:
                                print(f"Generated {count} positions...", file=sys.stderr)
    
    if output_file:
        out.close()
    
    print(f"Total: {count} legal KPKP positions (wrap={wrap})", file=sys.stderr)
    return count

if __name__ == '__main__':
    wrap = not (len(sys.argv) > 1 and sys.argv[1] == 'flat')
    output = sys.argv[2] if len(sys.argv) > 2 else None
    generate_kpkp_fast(wrap, output)