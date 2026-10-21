#!/usr/bin/env python3
"""Validate KPK results against Lichess tablebase (online)."""

import subprocess
import random
import sys
import os
import time

sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')

from realchess.probe import Prober

def kpsolve_to_fen(pos_str):
    """Convert kpsolve position format to FEN."""
    import re
    match = re.match(r'K([a-h][1-8])\s+P([a-h][1-8])\s+k([a-h][1-8])\s+([wb])\s+-', pos_str)
    if not match:
        return None
    wk, wp, bk, stm = match.groups()
    
    board = [['.' for _ in range(8)] for _ in range(8)]
    def place(piece, square, color):
        f = ord(square[0]) - ord('a')
        r = 8 - int(square[1])
        board[r][f] = piece.upper() if color == 'w' else piece.lower()
    
    place('K', wk, 'w')
    place('P', wp, 'w')
    place('K', bk, 'b')
    
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

def validate_positions_online(positions, num_samples=20):
    """Validate random positions against Lichess (online)."""
    prober = Prober(cap=num_samples, ledger='research/kp_tablebases/val_ledger.jsonl', offline=False, verbose=True)
    
    print(f"Validating {min(num_samples, len(positions))} random positions against Lichess (online)...")
    
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
    
    flat_positions = list(flat_results.keys())
    samples = random.sample(flat_positions, min(num_samples, len(flat_positions)))
    
    matches = 0
    mismatches = 0
    errors = 0
    
    for i, pos in enumerate(samples):
        fen = kpsolve_to_fen(pos)
        if not fen:
            continue
        
        print(f"\n[{i+1}/{len(samples)}] Probing: {pos}")
        print(f"  FEN: {fen}")
        
        try:
            rec = prober.probe(fen)
            category = rec.get('data', {}).get('category')
            if category:
                lichess_result = category
                kpsolve_result = flat_results[pos]
                
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
                    print(f"  MATCH: kpsolve={kpsolve_cat}, lichess={lichess_result}")
                else:
                    mismatches += 1
                    print(f"  MISMATCH: kpsolve={kpsolve_cat}, lichess={lichess_result}")
            else:
                print(f"  No category in response: {rec}")
                errors += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            errors += 1
        
        # Rate limiting is handled by prober
    
    print(f"\nResults: {matches} matches, {mismatches} mismatches, {errors} errors")
    return matches, mismatches

def main():
    with open('research/kp_tablebases/kpk_flat_results2.txt') as f:
        positions = [line.strip() for line in f if '|' in line]
    
    validate_positions_online(positions, 20)

if __name__ == '__main__':
    main()