#!/usr/bin/env python3
"""Analyze kpsolve output for KPKP positions."""
import sys

def analyze_output(filename, board_name):
    wins_w = draws_w = losses_w = 0
    wins_b = draws_b = losses_b = 0
    capped = 0
    total = 0
    
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Format: "K... | W W" or "K... | W D" etc.
            if '|' not in line:
                continue
            parts = line.split('|')
            pos_part = parts[0].strip()
            result_part = parts[1].strip()
            
            # Extract side to move from position
            stm = pos_part.split()[-2]  # second to last is 'w' or 'b'
            results = result_part.split()
            if len(results) >= 2:
                bound_a, bound_b = results[0], results[1]
                if bound_a != bound_b:
                    capped += 1
                # Use bound A (first result) for statistics
                res = bound_a
            else:
                res = results[0] if results else 'X'
            
            total += 1
            if stm == 'w':
                if res == 'W':
                    wins_w += 1
                elif res == 'D':
                    draws_w += 1
                elif res == 'L':
                    losses_w += 1
            else:
                if res == 'W':
                    wins_b += 1
                elif res == 'D':
                    draws_b += 1
                elif res == 'L':
                    losses_b += 1
    
    n_w = wins_w + draws_w + losses_w
    n_b = wins_b + draws_b + losses_b
    
    print(f"\n=== {board_name} ===")
    print(f"Total positions: {total}")
    print(f"  Capped promotions (bounds differ): {capped}")
    print(f"\nWhite to move ({n_w} positions):")
    print(f"  Wins: {wins_w} ({100*wins_w/n_w:.2f}%)")
    print(f"  Draws: {draws_w} ({100*draws_w/n_w:.2f}%)")
    print(f"  Losses: {losses_w} ({100*losses_w/n_w:.2f}%)")
    print(f"\nBlack to move ({n_b} positions):")
    print(f"  Wins: {wins_b} ({100*wins_b/n_b:.2f}%)")
    print(f"  Draws: {draws_b} ({100*draws_b/n_b:.2f}%)")
    print(f"  Losses: {losses_b} ({100*losses_b/n_b:.2f}%)")
    
    return {
        'total': total, 'capped': capped,
        'wins_w': wins_w, 'draws_w': draws_w, 'losses_w': losses_w,
        'wins_b': wins_b, 'draws_b': draws_b, 'losses_b': losses_b,
        'n_w': n_w, 'n_b': n_b
    }

if __name__ == "__main__":
    flat_stats = analyze_output("research/kpkp/kpkp_flat.out", "Flat 8x8")
    cyl_stats = analyze_output("research/kpkp/kpkp_cyl.out", "Cylinder 8x8")
    
    # Compare
    print("\n=== Comparison ===")
    print(f"Positions: flat={flat_stats['total']}, cyl={cyl_stats['total']}")
    
    # Find positions that differ
    # We need to match positions between the two outputs
    flat_results = {}
    with open("research/kpkp/kpkp_flat.out") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            if '|' not in line: continue
            pos, res = line.split('|', 1)
            flat_results[pos.strip()] = res.strip().split()[0]
    
    cyl_results = {}
    with open("research/kpkp/kpkp_cyl.out") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            if '|' not in line: continue
            pos, res = line.split('|', 1)
            cyl_results[pos.strip()] = res.strip().split()[0]
    
    # Compare common positions
    common = set(flat_results.keys()) & set(cyl_results.keys())
    flat_win_cyl_draw = 0
    flat_draw_cyl_win = 0
    flat_loss_cyl_draw = 0
    flat_draw_cyl_loss = 0
    flat_win_cyl_loss = 0
    flat_loss_cyl_win = 0
    
    for pos in common:
        fr = flat_results[pos]
        cr = cyl_results[pos]
        if fr != cr:
            if fr == 'W' and cr == 'D':
                flat_win_cyl_draw += 1
            elif fr == 'D' and cr == 'W':
                flat_draw_cyl_win += 1
            elif fr == 'L' and cr == 'D':
                flat_loss_cyl_draw += 1
            elif fr == 'D' and cr == 'L':
                flat_draw_cyl_loss += 1
            elif fr == 'W' and cr == 'L':
                flat_win_cyl_loss += 1
            elif fr == 'L' and cr == 'W':
                flat_loss_cyl_win += 1
    
    print(f"Common positions: {len(common)}")
    print(f"Flat win -> Cyl draw: {flat_win_cyl_draw}")
    print(f"Flat draw -> Cyl win: {flat_draw_cyl_win}")
    print(f"Flat loss -> Cyl draw: {flat_loss_cyl_draw}")
    print(f"Flat draw -> Cyl loss: {flat_draw_cyl_loss}")
    print(f"Flat win -> Cyl loss: {flat_win_cyl_loss}")
    print(f"Flat loss -> Cyl win: {flat_loss_cyl_win}")
    print(f"Total flipped: {flat_win_cyl_draw + flat_draw_cyl_win + flat_loss_cyl_draw + flat_draw_cyl_loss + flat_win_cyl_loss + flat_loss_cyl_win}")