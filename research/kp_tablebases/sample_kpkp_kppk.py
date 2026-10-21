#!/usr/bin/env python3
"""Sample KPKP/KPPK positions and solve them."""

import subprocess
import random
import sys
import os

FILES = 8
RANKS = 8
N = FILES * RANKS

def sq_name(f, r):
    return chr(ord('a') + f) + str(r + 1)

def square_from_index(idx):
    return idx % FILES, idx // FILES

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
    f, r = square_from_index(sq)
    attacks = []
    dr = 1 if color == 'w' else -1
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

def random_kpkp_position(wrap=True):
    """Generate a random legal KPKP position."""
    valid_pawn_squares = [sq for sq in range(N) if 1 <= sq // FILES <= 6]
    
    while True:
        wk = random.randrange(N)
        wp1 = random.choice(valid_pawn_squares)
        if wp1 == wk: continue
        wp2 = random.choice(valid_pawn_squares)
        if wp2 in (wk, wp1): continue
        bk = random.randrange(N)
        if bk in (wk, wp1, wp2): continue
        bp = random.choice(valid_pawn_squares)
        if bp in (wk, wp1, wp2, bk): continue
        stm = random.choice(['w', 'b'])
        
        # Check legality
        if bk in king_attacks(wk, wrap): continue
        if wk in king_attacks(bk, wrap): continue
        
        wp1_att = pawn_attacks(wp1, 'w', wrap)
        wp2_att = pawn_attacks(wp2, 'w', wrap)
        white_pawn_att = set(wp1_att) | set(wp2_att)
        if bk in white_pawn_att: continue
        
        bp_att = pawn_attacks(bp, 'b', wrap)
        if wk in bp_att: continue
        
        if stm == 'w':
            if wk in king_attacks(bk, wrap): continue
            if wk in bp_att: continue
        else:
            if bk in king_attacks(wk, wrap): continue
            if bk in white_pawn_att: continue
        
        wk_name = sq_name(*square_from_index(wk))
        wp1_name = sq_name(*square_from_index(wp1))
        wp2_name = sq_name(*square_from_index(wp2))
        bk_name = sq_name(*square_from_index(bk))
        bp_name = sq_name(*square_from_index(bp))
        return f"K{wk_name} P{wp1_name} P{wp2_name} k{bk_name} p{bp_name} {stm} -"

def random_kppk_position(wrap=True):
    """Generate a random legal KPPK position."""
    valid_pawn_squares = [sq for sq in range(N) if 1 <= sq // FILES <= 6]
    
    while True:
        wk = random.randrange(N)
        wp1 = random.choice(valid_pawn_squares)
        if wp1 == wk: continue
        wp2 = random.choice(valid_pawn_squares)
        if wp2 in (wk, wp1): continue
        bk = random.randrange(N)
        if bk in (wk, wp1, wp2): continue
        bp1 = random.choice(valid_pawn_squares)
        if bp1 in (wk, wp1, wp2, bk): continue
        bp2 = random.choice(valid_pawn_squares)
        if bp2 in (wk, wp1, wp2, bk, bp1): continue
        stm = random.choice(['w', 'b'])
        
        # Check legality
        if bk in king_attacks(wk, wrap): continue
        if wk in king_attacks(bk, wrap): continue
        
        wp1_att = pawn_attacks(wp1, 'w', wrap)
        wp2_att = pawn_attacks(wp2, 'w', wrap)
        white_pawn_att = set(wp1_att) | set(wp2_att)
        if bk in white_pawn_att: continue
        
        bp1_att = pawn_attacks(bp1, 'b', wrap)
        bp2_att = pawn_attacks(bp2, 'b', wrap)
        black_pawn_att = set(bp1_att) | set(bp2_att)
        if wk in black_pawn_att: continue
        
        if stm == 'w':
            if wk in king_attacks(bk, wrap): continue
            if wk in black_pawn_att: continue
        else:
            if bk in king_attacks(wk, wrap): continue
            if bk in white_pawn_att: continue
        
        wk_name = sq_name(*square_from_index(wk))
        wp1_name = sq_name(*square_from_index(wp1))
        wp2_name = sq_name(*square_from_index(wp2))
        bk_name = sq_name(*square_from_index(bk))
        bp1_name = sq_name(*square_from_index(bp1))
        bp2_name = sq_name(*square_from_index(bp2))
        return f"K{wk_name} P{wp1_name} P{wp2_name} k{bk_name} p{bp1_name} p{bp2_name} {stm} -"

def solve_positions(positions, board_type):
    """Solve a list of positions using kpsolve."""
    input_data = '\n'.join(positions) + '\n'
    
    cmd = [
        '/Users/aritro/Downloads/Research/Chessendgames/kings/kpsolve',
        '--board', board_type,
        '--ep', 'on',
        '--promote', 'QRBN',
        '--cap', '2'  # KPKP/KPPK may need cap=2 for promotions
    ]
    
    result = subprocess.run(cmd, input=input_data, capture_output=True, text=True, timeout=300)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return None
    
    return result.stdout

def parse_results(output):
    """Parse kpsolve output."""
    results = []
    for line in output.strip().split('\n'):
        if '|' not in line:
            continue
        pos_part, res_part = line.split('|', 1)
        pos_part = pos_part.strip()
        res_parts = res_part.strip().split()
        if len(res_parts) >= 2:
            results.append((pos_part, res_parts[0], res_parts[1]))
    return results

def main():
    random.seed(42)  # Reproducible
    
    # Sample sizes
    kpkp_sample = 50000
    kppk_sample = 50000
    
    print(f"Generating {kpkp_sample} random KPKP positions (cylinder)...")
    kpkp_cyl_positions = [random_kpkp_position(wrap=True) for _ in range(kpkp_sample)]
    
    print(f"Generating {kpkp_sample} random KPKP positions (flat)...")
    kpkp_flat_positions = [random_kpkp_position(wrap=False) for _ in range(kpkp_sample)]
    
    print(f"Generating {kppk_sample} random KPPK positions (cylinder)...")
    kppk_cyl_positions = [random_kppk_position(wrap=True) for _ in range(kppk_sample)]
    
    print(f"Generating {kppk_sample} random KPPK positions (flat)...")
    kppk_flat_positions = [random_kppk_position(wrap=False) for _ in range(kppk_sample)]
    
    # Solve in batches
    batch_size = 5000
    
    def solve_and_save(positions, board_type, output_file):
        print(f"\nSolving {len(positions)} positions on {board_type}...")
        with open(output_file, 'w') as f:
            for i in range(0, len(positions), batch_size):
                batch = positions[i:i+batch_size]
                print(f"  Batch {i//batch_size + 1}/{(len(positions)-1)//batch_size + 1}...", file=sys.stderr)
                result = solve_positions(batch, board_type)
                if result is None:
                    print(f"  Failed!", file=sys.stderr)
                    return False
                f.write(result)
        print(f"  Saved to {output_file}", file=sys.stderr)
        return True
    
    # KPKP Cylinder
    solve_and_save(kpkp_cyl_positions, 'cyl:8x8', 'research/kp_tablebases/kpkp_cylinder_sample.txt')
    
    # KPKP Flat
    solve_and_save(kpkp_flat_positions, 'flat:8x8', 'research/kp_tablebases/kpkp_flat_sample.txt')
    
    # KPPK Cylinder
    solve_and_save(kppk_cyl_positions, 'cyl:8x8', 'research/kp_tablebases/kppk_cylinder_sample.txt')
    
    # KPPK Flat
    solve_and_save(kppk_flat_positions, 'flat:8x8', 'research/kp_tablebases/kppk_flat_sample.txt')
    
    print("\nAll sampling done!")

if __name__ == '__main__':
    main()