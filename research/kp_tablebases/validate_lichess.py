#!/usr/bin/env python3
"""Validate KPK results against Lichess tablebase."""

import subprocess
import random
import sys
import os

# Add realchess to path
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')

from realchess.probe import Prober

def kpsolve_to_fen(pos_str):
    """Convert kpsolve position format to FEN."""
    # Parse: "K<wk> P<wp> k<bk> <stm> -"
    import re
    match = re.match(r'K([a-h][1-8])\s+P([a-h][1-8])\s+k([a-h][1-8])\s+([wb])\s+-', pos_str)
    if not match:
        return None
    wk, wp, bk, stm = match.groups()
    
    # Build board
    board = [['.' for _ in range(8)] for _ in range(8)]
    # White pieces uppercase, Black lowercase
    # Rank 8 is index 0, rank 1 is index 7
    def place(piece, square, color):
        f = ord(square[0]) - ord('a')
        r = 8 - int(square[1])
        board[r][f] = piece.upper() if color == 'w' else piece.lower()
    
    place('K', wk, 'w')
    place('P', wp, 'w')
    place('K', bk, 'b')
    
    # Convert to FEN
    fen_rows = []
    for row in board:
        empty = 0
        fen_row = ''
        for cell in row:
            if cell == '.':
                empty += 1
            else:
                if empty > 0:
                    fen_row += str(empty)
                    empty = 0
                fen_row += cell
        if empty > 0:
            fen_row += str(empty)
        fen_rows.append(fen_row)
    
    fen = '/'.join(fen_rows) + f' {stm} - - 0 1'
    return fen

def validate_positions(positions, num_samples=20):
    """Validate random positions against Lichess."""
    prober = Prober(cap=200, offline=True)  # Offline mode first
    
    print(f"Validating {min(num_samples, len(positions))} random positions against Lichess cache...")
    
    # Load cylinder results for comparison
    cyl_results = {}
    with open('research/kp_tablebases/kpk_cylinder_results2.txt') as f:
        for line in f:
            line = line.strip()
            if '|' in line:
                pos_part, res_part = line.split('|', 1)
                pos_part = pos_part.strip()
                res_parts = res_part.strip().split()
                if len(res_parts) >= 2 and res_parts[0] == res_parts[1]:
                    cyl_results[pos_part] = res_parts[0]
    
    flat_results = {}
    with open('research/kp_tablebases/kpk_flat_results2.txt') as f:
        for line in f:
            line = line.strip()
            if '|' in line:
                pos_part, res_part = line.split('|', 1)
                pos_part = pos_part.strip()
                res_parts = res_part.strip().split()
                if len(res_parts) >= 2 and res_parts[0] == res_parts[1]:
                    flat_results[pos_part] = res_parts[0]
    
    # Pick random positions from flat results (since Lichess is flat board)
    flat_positions = list(flat_results.keys())
    samples = random.sample(flat_positions, min(num_samples, len(flat_positions)))
    
    matches = 0
    mismatches = 0
    not_cached = 0
    
    for pos in samples:
        fen = kpsolve_to_fen(pos)
        if not fen:
            continue
        
        # Check Lichess cache
        try:
            rec = prober.cached(fen)
            if rec is None:
                not_cached += 1
                # Try online (but respect rate limit)
                # For now, just note it's not cached
                continue
            
            category = rec.get('data', {}).get('category')
            if category:
                lichess_result = category  # 'win', 'loss', 'draw'
                kpsolve_result = flat_results[pos]
                
                # Map kpsolve result to Lichess category
                # kpsolve: 'W' = White wins, 'L' = Black wins, 'D' = draw
                # Lichess: 'win' = side to move wins, 'loss' = side to move loses, 'draw' = draw
                stm = pos.split()[-2]
                if stm == 'w':
                    if kpsolve_result == 'W':
                        kpsolve_cat = 'win'
                    elif kpsolve_result == 'L':
                        kpsolve_cat = 'loss'
                    else:
                        kpsolve_cat = 'draw'
                else:
                    if kpsolve_result == 'L':
                        kpsolve_cat = 'win'
                    elif kpsolve_result == 'W':
                        kpsolve_cat = 'loss'
                    else:
                        kpsolve_cat = 'draw'
                
                if kpsolve_cat == lichess_result:
                    matches += 1
                    print(f"  MATCH: {pos} -> kpsolve={kpsolve_cat}, lichess={lichess_result}")
                else:
                    mismatches += 1
                    print(f"  MISMATCH: {pos} -> kpsolve={kpsolve_cat}, lichess={lichess_result} (FEN: {fen})")
            else:
                print(f"  NO CATEGORY: {pos}")
                not_cached += 1
        except Exception as e:
            print(f"  ERROR: {pos} -> {e}")
            not_cached += 1
    
    print(f"\nResults: {matches} matches, {mismatches} mismatches, {not_cached} not in cache")
    return matches, mismatches

def main():
    # Load some positions
    with open('research/kp_tablebases/kpk_flat_results2.txt') as f:
        positions = [line.strip() for line in f if '|' in line]
    
    validate_positions(positions, 20)

if __name__ == '__main__':
    main()