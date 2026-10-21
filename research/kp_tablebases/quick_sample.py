#!/usr/bin/env python3
"""Quick sample of KPKP/KPPK positions."""

import subprocess
import random
import sys

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
            if df == 0 and dr == 0: continue
            nf, nr = f + df, r + dr
            if not (0 <= nr < RANKS): continue
            if wrap: nf = nf % FILES
            elif not (0 <= nf < FILES): continue
            attacks.append(nr * FILES + nf)
    return attacks

def pawn_attacks(sq, color, wrap):
    f, r = square_from_index(sq)
    attacks = []
    dr = 1 if color == 'w' else -1
    for df in (-1, 1):
        nf, nr = f + df, r + dr
        if not (0 <= nr < RANKS): continue
        if wrap: nf = nf % FILES
        elif not (0 <= nf < FILES): continue
        attacks.append(nr * FILES + nf)
    return attacks

valid_pawn_squares = [sq for sq in range(N) if 1 <= sq // FILES <= 6]

def random_kpkp(wrap):
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
        
        if bk in king_attacks(wk, wrap): continue
        wp_att = set(pawn_attacks(wp1, 'w', wrap)) | set(pawn_attacks(wp2, 'w', wrap))
        if bk in wp_att: continue
        bp_att = set(pawn_attacks(bp, 'b', wrap))
        if wk in bp_att: continue
        if stm == 'w':
            if wk in king_attacks(bk, wrap): continue
            if wk in bp_att: continue
        else:
            if bk in king_attacks(wk, wrap): continue
            if bk in wp_att: continue
        
        return f"K{sq_name(*square_from_index(wk))} P{sq_name(*square_from_index(wp1))} P{sq_name(*square_from_index(wp2))} k{sq_name(*square_from_index(bk))} p{sq_name(*square_from_index(bp))} {stm} -"

def random_kppk(wrap):
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
        
        if bk in king_attacks(wk, wrap): continue
        wp_att = set(pawn_attacks(wp1, 'w', wrap)) | set(pawn_attacks(wp2, 'w', wrap))
        if bk in wp_att: continue
        bp_att = set(pawn_attacks(bp1, 'b', wrap)) | set(pawn_attacks(bp2, 'b', wrap))
        if wk in bp_att: continue
        if stm == 'w':
            if wk in king_attacks(bk, wrap): continue
            if wk in bp_att: continue
        else:
            if bk in king_attacks(wk, wrap): continue
            if bk in wp_att: continue
        
        return f"K{sq_name(*square_from_index(wk))} P{sq_name(*square_from_index(wp1))} P{sq_name(*square_from_index(wp2))} k{sq_name(*square_from_index(bk))} p{sq_name(*square_from_index(bp1))} p{sq_name(*square_from_index(bp2))} {stm} -"

def solve_batch(positions, board_type, cap=2):
    input_data = '\n'.join(positions) + '\n'
    cmd = ['/Users/aritro/Downloads/Research/Chessendgames/kings/kpsolve', '--board', board_type, '--ep', 'on', '--promote', 'QRBN', '--cap', str(cap)]
    result = subprocess.run(cmd, input=input_data, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return None
    return result.stdout

def analyze_sample(name, positions, board_type):
    print(f"\n=== {name} on {board_type} ===")
    batch_size = 2000
    all_results = []
    
    for i in range(0, len(positions), batch_size):
        batch = positions[i:i+batch_size]
        result = solve_batch(batch, board_type)
        if result is None:
            return
        all_results.extend(result.strip().split('\n'))
        if i % 10000 == 0:
            print(f"  Progress: {min(i+batch_size, len(positions))}/{len(positions)}", file=sys.stderr)
    
    # Parse and analyze
    wins_w = wins_b = draws = bounds_diff = illegal = 0
    for line in all_results:
        if '|' not in line: continue
        pos_part, res_part = line.split('|', 1)
        res_parts = res_part.strip().split()
        if len(res_parts) >= 2:
            a, b = res_parts[0], res_parts[1]
            if a == 'X' or b == 'X':
                illegal += 1
            elif a == b:
                if a == 'W': wins_w += 1
                elif a == 'L': wins_b += 1
                else: draws += 1
            else:
                bounds_diff += 1
    
    total = len(all_results)
    print(f"  Total: {total}")
    print(f"  White wins: {wins_w} ({wins_w/total*100:.1f}%)")
    print(f"  Black wins: {wins_b} ({wins_b/total*100:.1f}%)")
    print(f"  Draws: {draws} ({draws/total*100:.1f}%)")
    print(f"  Bounds differ: {bounds_diff}")
    print(f"  Illegal: {illegal}")
    return all_results

def main():
    random.seed(42)
    sample_size = 5000  # Smaller sample for speed
    
    print(f"Generating {sample_size} random positions each...")
    
    kpkp_cyl = [random_kpkp(True) for _ in range(sample_size)]
    kpkp_flat = [random_kpkp(False) for _ in range(sample_size)]
    kppk_cyl = [random_kppk(True) for _ in range(sample_size)]
    kppk_flat = [random_kppk(False) for _ in range(sample_size)]
    
    print("Generated. Now solving...")
    
    analyze_sample("KPKP", kpkp_cyl, 'cyl:8x8')
    analyze_sample("KPKP", kpkp_flat, 'flat:8x8')
    analyze_sample("KPPK", kppk_cyl, 'cyl:8x8')
    analyze_sample("KPPK", kppk_flat, 'flat:8x8')

if __name__ == '__main__':
    main()