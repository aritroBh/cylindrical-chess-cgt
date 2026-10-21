#!/usr/bin/env python3
"""Analyze KPK tablebase results."""

import sys
import re
from collections import Counter

def parse_result_file(filename):
    """Parse kpsolve result file."""
    results = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Format: "K... P... k... w - | A B"
            if '|' not in line:
                continue
            pos_part, res_part = line.split('|', 1)
            pos_part = pos_part.strip()
            res_parts = res_part.strip().split()
            if len(res_parts) >= 2:
                a, b = res_parts[0], res_parts[1]
                results.append((pos_part, a, b))
    return results

def parse_position(pos_str):
    """Parse position string into components."""
    # Format: "K<wk> P<wp> k<bk> <stm> -"
    match = re.match(r'K([a-h][1-8])\s+P([a-h][1-8])\s+k([a-h][1-8])\s+([wb])\s+-', pos_str)
    if not match:
        return None
    wk, wp, bk, stm = match.groups()
    return wk, wp, bk, stm

def square_to_coords(sq):
    f = ord(sq[0]) - ord('a')
    r = int(sq[1]) - 1
    return f, r

def analyze_results(results, name):
    """Analyze KPK results."""
    total = len(results)
    exact = sum(1 for _, a, b in results if a == b)
    wins_w = sum(1 for _, a, b in results if a == b == 'W')
    wins_b = sum(1 for _, a, b in results if a == b == 'L')
    draws = sum(1 for _, a, b in results if a == b == 'D')
    bounds_diff = sum(1 for _, a, b in results if a != b)
    illegal = sum(1 for _, a, b in results if a == 'X' or b == 'X')
    
    print(f"\n=== {name} ===")
    print(f"Total positions: {total}")
    print(f"Exact results: {exact} ({exact/total*100:.1f}%)")
    print(f"  White wins: {wins_w} ({wins_w/total*100:.1f}%)")
    print(f"  Black wins: {wins_b} ({wins_b/total*100:.1f}%)")
    print(f"  Draws: {draws} ({draws/total*100:.1f}%)")
    print(f"Bounds differ: {bounds_diff}")
    print(f"Illegal: {illegal}")
    
    # By side to move
    wtm_wins = sum(1 for pos, a, b in results if a == b == 'W' and parse_position(pos)[3] == 'w')
    wtm_draws = sum(1 for pos, a, b in results if a == b == 'D' and parse_position(pos)[3] == 'w')
    wtm_losses = sum(1 for pos, a, b in results if a == b == 'L' and parse_position(pos)[3] == 'w')
    btm_wins = sum(1 for pos, a, b in results if a == b == 'W' and parse_position(pos)[3] == 'b')
    btm_draws = sum(1 for pos, a, b in results if a == b == 'D' and parse_position(pos)[3] == 'b')
    btm_losses = sum(1 for pos, a, b in results if a == b == 'L' and parse_position(pos)[3] == 'b')
    
    wtm_total = wtm_wins + wtm_draws + wtm_losses
    btm_total = btm_wins + btm_draws + btm_losses
    
    print(f"\nWhite to move ({wtm_total}):")
    print(f"  Wins: {wtm_wins} ({wtm_wins/wtm_total*100:.1f}%)")
    print(f"  Draws: {wtm_draws} ({wtm_draws/wtm_total*100:.1f}%)")
    print(f"  Losses: {wtm_losses} ({wtm_losses/wtm_total*100:.1f}%)")
    
    print(f"\nBlack to move ({btm_total}):")
    print(f"  Wins: {btm_wins} ({btm_wins/btm_total*100:.1f}%)")
    print(f"  Draws: {btm_draws} ({btm_draws/btm_total*100:.1f}%)")
    print(f"  Losses: {btm_losses} ({btm_losses/btm_total*100:.1f}%)")
    
    return results

def find_classic_draws(results):
    """Find classic KPK draws (rook pawn, wrong corner, etc.)"""
    classic_draws = []
    for pos, a, b in results:
        if a != b:
            continue
        parsed = parse_position(pos)
        if not parsed:
            continue
        wk, wp, bk, stm = parsed
        wp_f, wp_r = square_to_coords(wp)
        wk_f, wk_r = square_to_coords(wk)
        bk_f, bk_r = square_to_coords(bk)
        
        # Classic rook pawn draw: pawn on a/h file, defending king in front
        is_rook_pawn = wp_f == 0 or wp_f == 7
        if is_rook_pawn and a == 'D':
            classic_draws.append((pos, a, b, 'rook_pawn'))
        
        # Key square rule: White wins if king reaches key squares
        # Key squares for pawn on rank r: (file±1, r+1), (file, r+1) on flat
        # We'll analyze this separately
        
    return classic_draws

def cylinder_key_squares(wp_f, wp_r):
    """Key squares on cylinder for a pawn at (wp_f, wp_r)."""
    # On cylinder, key squares are the three squares in front of the pawn
    # plus the squares diagonally ahead (which wrap)
    key = []
    # Square directly in front
    if wp_r + 1 < 8:
        key.append((wp_f, wp_r + 1))
    # Diagonals (wrap around)
    if wp_r + 1 < 8:
        key.append(((wp_f - 1) % 8, wp_r + 1))
        key.append(((wp_f + 1) % 8, wp_r + 1))
    return key

def analyze_key_squares(results):
    """Analyze key square rule on cylinder."""
    key_square_wins = 0
    key_square_total = 0
    non_key_wins = 0
    non_key_total = 0
    
    for pos, a, b in results:
        if a != b:
            continue
        parsed = parse_position(pos)
        if not parsed:
            continue
        wk, wp, bk, stm = parsed
        if stm != 'w':
            continue  # Only analyze White to move
        
        wp_f, wp_r = square_to_coords(wp)
        wk_f, wk_r = square_to_coords(wk)
        
        key_sqs = cylinder_key_squares(wp_f, wp_r)
        wk_on_key = (wk_f, wk_r) in key_sqs
        
        if wk_on_key:
            key_square_total += 1
            if a == 'W':
                key_square_wins += 1
        else:
            non_key_total += 1
            if a == 'W':
                non_key_wins += 1
    
    print(f"\nKey Square Analysis (White to move):")
    print(f"  King on key squares: {key_square_wins}/{key_square_total} wins ({key_square_wins/key_square_total*100:.1f}%)" if key_square_total else "  King on key squares: 0/0")
    print(f"  King NOT on key squares: {non_key_wins}/{non_key_total} wins ({non_key_wins/non_key_total*100:.1f}%)" if non_key_total else "  King NOT on key squares: 0/0")

def find_mutual_zugzwangs(results):
    """Find mutual zugzwangs: positions where side to move loses."""
    mz = []
    for pos, a, b in results:
        if a != b:
            continue
        parsed = parse_position(pos)
        if not parsed:
            continue
        wk, wp, bk, stm = parsed
        
        # Mutual zugzwang: both sides to move lose (i.e., P-position)
        # White to move loses (Black wins) AND Black to move loses (White wins)
        # We need to find pairs of positions that differ only in stm
        pass
    
    # Build dict by position without stm
    pos_dict = {}
    for pos, a, b in results:
        if a != b:
            continue
        parsed = parse_position(pos)
        if not parsed:
            continue
        wk, wp, bk, stm = parsed
        key = (wk, wp, bk)
        if key not in pos_dict:
            pos_dict[key] = {}
        pos_dict[key][stm] = a  # from White's perspective
    
    mutual_zugzwangs = []
    for key, outcomes in pos_dict.items():
        if 'w' in outcomes and 'b' in outcomes:
            # White to move: outcome from White's perspective
            # Black to move: outcome from White's perspective
            # Mutual zugzwang: White to move -> Black wins (L), Black to move -> White wins (W)
            if outcomes['w'] == 'L' and outcomes['b'] == 'W':
                mutual_zugzwangs.append(key)
    
    print(f"\nMutual Zugzwangs: {len(mutual_zugzwangs)}")
    for i, (wk, wp, bk) in enumerate(mutual_zugzwangs[:10]):
        print(f"  {i+1}. WK {wk} WP {wp} BK {bk}")
    if len(mutual_zugzwangs) > 10:
        print(f"  ... and {len(mutual_zugzwangs) - 10} more")
    
    return mutual_zugzwangs

def compare_cylinder_flat(cyl_results, flat_results):
    """Compare cylinder vs flat results."""
    # Build dicts for easy lookup
    cyl_dict = {}
    for pos, a, b in cyl_results:
        if a == b:
            parsed = parse_position(pos)
            if parsed:
                wk, wp, bk, stm = parsed
                cyl_dict[(wk, wp, bk, stm)] = a
    
    flat_dict = {}
    for pos, a, b in flat_results:
        if a == b:
            parsed = parse_position(pos)
            if parsed:
                wk, wp, bk, stm = parsed
                flat_dict[(wk, wp, bk, stm)] = a
    
    # Compare
    diffs = []
    for key, cyl_val in cyl_dict.items():
        if key in flat_dict:
            flat_val = flat_dict[key]
            if cyl_val != flat_val:
                diffs.append((key, cyl_val, flat_val))
    
    print(f"\n=== Cylinder vs Flat Differences ===")
    print(f"Total compared: {len(set(cyl_dict.keys()) & set(flat_dict.keys()))}")
    print(f"Differences: {len(diffs)}")
    
    # Categorize differences
    cyl_win_flat_draw = sum(1 for _, c, f in diffs if c == 'W' and f == 'D')
    cyl_draw_flat_win = sum(1 for _, c, f in diffs if c == 'D' and f == 'W')
    cyl_win_flat_loss = sum(1 for _, c, f in diffs if c == 'W' and f == 'L')
    cyl_loss_flat_win = sum(1 for _, c, f in diffs if c == 'L' and f == 'W')
    cyl_draw_flat_loss = sum(1 for _, c, f in diffs if c == 'D' and f == 'L')
    cyl_loss_flat_draw = sum(1 for _, c, f in diffs if c == 'L' and f == 'D')
    
    print(f"  Cylinder win, Flat draw: {cyl_win_flat_draw}")
    print(f"  Cylinder draw, Flat win: {cyl_draw_flat_win}")
    print(f"  Cylinder win, Flat loss: {cyl_win_flat_loss}")
    print(f"  Cylinder loss, Flat win: {cyl_loss_flat_win}")
    print(f"  Cylinder draw, Flat loss: {cyl_draw_flat_loss}")
    print(f"  Cylinder loss, Flat draw: {cyl_loss_flat_draw}")
    
    # Show examples of classic flat draws that become wins on cylinder
    print("\nClassic flat draws that become wins on cylinder (examples):")
    count = 0
    for key, cyl_val, flat_val in diffs:
        if flat_val == 'D' and cyl_val == 'W':
            wk, wp, bk, stm = key
            print(f"  WK {wk} WP {wp} BK {bk} {stm}: cyl={cyl_val}, flat={flat_val}")
            count += 1
            if count >= 10:
                break
    
    print("\nClassic flat wins that become draws on cylinder (examples):")
    count = 0
    for key, cyl_val, flat_val in diffs:
        if flat_val == 'W' and cyl_val == 'D':
            wk, wp, bk, stm = key
            print(f"  WK {wk} WP {wp} BK {bk} {stm}: cyl={cyl_val}, flat={flat_val}")
            count += 1
            if count >= 10:
                break
    
    return diffs

def square_rule_analysis(results):
    """Analyze the square rule on cylinder."""
    # Square rule: pawn promotes if king can't reach the promotion square in time
    # On cylinder, the promotion square wraps, so we need to check both directions
    pass

def main():
    cyl_file = sys.argv[1] if len(sys.argv) > 1 else 'research/kp_tablebases/kpk_cylinder_results2.txt'
    flat_file = sys.argv[2] if len(sys.argv) > 2 else 'research/kp_tablebases/kpk_flat_results2.txt'
    
    print("Loading cylinder results...")
    cyl_results = parse_result_file(cyl_file)
    print(f"Loaded {len(cyl_results)} cylinder positions")
    
    print("Loading flat results...")
    flat_results = parse_result_file(flat_file)
    print(f"Loaded {len(flat_results)} flat positions")
    
    analyze_results(cyl_results, "Cylinder 8x8 KPK")
    analyze_results(flat_results, "Flat 8x8 KPK")
    
    analyze_key_squares(cyl_results)
    
    find_mutual_zugzwangs(cyl_results)
    
    compare_cylinder_flat(cyl_results, flat_results)

if __name__ == '__main__':
    main()