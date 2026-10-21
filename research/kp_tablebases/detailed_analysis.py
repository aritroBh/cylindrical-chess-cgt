#!/usr/bin/env python3
"""Detailed analysis of KPK cylinder vs flat results."""

import sys
import re
from collections import Counter, defaultdict

def parse_result_file(filename):
    results = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '|' not in line:
                continue
            pos_part, res_part = line.split('|', 1)
            pos_part = pos_part.strip()
            res_parts = res_part.strip().split()
            if len(res_parts) >= 2:
                results.append((pos_part, res_parts[0], res_parts[1]))
    return results

def parse_position(pos_str):
    match = re.match(r'K([a-h][1-8])\s+P([a-h][1-8])\s+k([a-h][1-8])\s+([wb])\s+-', pos_str)
    if not match:
        return None
    wk, wp, bk, stm = match.groups()
    return wk, wp, bk, stm

def square_to_coords(sq):
    return ord(sq[0]) - ord('a'), int(sq[1]) - 1

def analyze_cylinder_kpk():
    """Deep analysis of cylinder KPK."""
    cyl_results = parse_result_file('research/kp_tablebases/kpk_cylinder_results2.txt')
    flat_results = parse_result_file('research/kp_tablebases/kpk_flat_results2.txt')
    
    # Build dicts
    cyl_dict = {}
    for pos, a, b in cyl_results:
        if a == b:
            parsed = parse_position(pos)
            if parsed:
                cyl_dict[parsed] = a
    
    flat_dict = {}
    for pos, a, b in flat_results:
        if a == b:
            parsed = parse_position(pos)
            if parsed:
                flat_dict[parsed] = a
    
    print("=== CYLINDER KPK DETAILED ANALYSIS ===\n")
    
    # 1. Share of positions won with White to move
    wtm_cyl = [(k, v) for k, v in cyl_dict.items() if k[3] == 'w']
    wtm_total = len(wtm_cyl)
    wtm_wins = sum(1 for _, v in wtm_cyl if v == 'W')
    wtm_draws = sum(1 for _, v in wtm_cyl if v == 'D')
    print(f"1. SHARE WON WITH WHITE TO MOVE (CYLINDER)")
    print(f"   Total WTM positions: {wtm_total}")
    print(f"   White wins: {wtm_wins} ({wtm_wins/wtm_total*100:.2f}%)")
    print(f"   Draws: {wtm_draws} ({wtm_draws/wtm_total*100:.2f}%)")
    print()
    
    # 2. Classic flat draws that become wins on cylinder
    print("2. CLASSIC FLAT DRAWS THAT BECOME WINS ON CYLINDER")
    classic_draws_to_wins = []
    for key, cyl_val in cyl_dict.items():
        if key in flat_dict:
            flat_val = flat_dict[key]
            if flat_val == 'D' and cyl_val == 'W':
                classic_draws_to_wins.append((key, cyl_val, flat_val))
    
    print(f"   Count: {len(classic_draws_to_wins)}")
    # Group by pawn file
    by_file = defaultdict(int)
    for (wk, wp, bk, stm), _, _ in classic_draws_to_wins:
        wp_f, _ = square_to_coords(wp)
        by_file[wp_f] += 1
    print("   By pawn file:")
    for f in range(8):
        if by_file[f]:
            print(f"     File {chr(ord('a')+f)}: {by_file[f]}")
    
    # Show key examples
    print("   Key examples:")
    for (wk, wp, bk, stm), _, _ in classic_draws_to_wins[:20]:
        print(f"     WK {wk} WP {wp} BK {bk} {stm}: cyl=W, flat=D")
    print()
    
    # 3. Classic flat wins that become draws on cylinder
    print("3. CLASSIC FLAT WINS THAT BECOME DRAWS ON CYLINDER")
    wins_to_draws = []
    for key, cyl_val in cyl_dict.items():
        if key in flat_dict:
            flat_val = flat_dict[key]
            if flat_val == 'W' and cyl_val == 'D':
                wins_to_draws.append((key, cyl_val, flat_val))
    
    print(f"   Count: {len(wins_to_draws)}")
    by_file = defaultdict(int)
    for (wk, wp, bk, stm), _, _ in wins_to_draws:
        wp_f, _ = square_to_coords(wp)
        by_file[wp_f] += 1
    print("   By pawn file:")
    for f in range(8):
        if by_file[f]:
            print(f"     File {chr(ord('a')+f)}: {by_file[f]}")
    
    print("   Key examples:")
    for (wk, wp, bk, stm), _, _ in wins_to_draws[:20]:
        print(f"     WK {wk} WP {wp} BK {bk} {stm}: cyl=D, flat=W")
    print()
    
    # 4. Cylinder "square rule"
    print("4. CYLINDER SQUARE RULE ANALYSIS")
    # The square rule: pawn promotes if king can't reach promotion square in time
    # On cylinder, the promotion square is the same file, but king can approach from either side
    square_rule_correct = 0
    square_rule_total = 0
    square_rule_failures = []
    
    for (wk, wp, bk, stm), val in cyl_dict.items():
        if stm != 'w':  # Only analyze White to move for square rule
            continue
        wp_f, wp_r = square_to_coords(wp)
        wk_f, wk_r = square_to_coords(wk)
        bk_f, bk_r = square_from_index = square_to_coords(bk)
        
        # Distance from white king to promotion (rank 8)
        # White pawn promotes at rank 8, needs (8 - wp_r) steps
        pawn_steps_to_promote = 8 - wp_r
        if wp_r == 2:  # Can double step
            pawn_steps_to_promote = 7 - wp_r  # Actually from rank 2, double step to 4, then 4 more = 5 steps to promote? Let me recalculate
            # From rank 2: move to 3 (1), to 4 (2), to 5 (3), to 6 (4), to 7 (5), promote on 8 (6) = 6 moves
            # Double step: 2->4 (1), 4->5 (2), 5->6 (3), 6->7 (4), promote (5) = 5 moves
            # So minimum is 5 moves from rank 2
            pawn_steps_to_promote = 5
        else:
            pawn_steps_to_promote = 8 - wp_r  # From rank r, need 8-r moves (including promotion move)
        
        # Black king distance to promotion square (wp_f, 8)
        # On cylinder, king moves in Chebyshev distance with wrap
        def cyl_king_dist(f1, r1, f2, r2):
            df = min((f1 - f2) % 8, (f2 - f1) % 8)
            dr = abs(r1 - r2)
            return max(df, dr)
        
        bk_to_prom = cyl_king_dist(bk_f, bk_r, wp_f, 7)  # Rank 8 is index 7
        
        # Square rule: if Black king can reach promotion square before or same time as pawn promotes, it's a draw
        # Pawn moves first (White to move), so pawn gets pawn_steps_to_promote moves
        # Black king gets pawn_steps_to_promote - 1 moves (since White moves first)
        # Actually, if pawn promotes on move N, Black has made N-1 moves
        square_rule_draw = (bk_to_prom <= pawn_steps_to_promote - 1)
        square_rule_win = not square_rule_draw
        
        actual_win = (val == 'W')
        square_rule_total += 1
        if square_rule_win == actual_win:
            square_rule_correct += 1
        else:
            square_rule_failures.append(((wk, wp, bk, stm), val, square_rule_win))
    
    print(f"   Square rule accuracy: {square_rule_correct}/{square_rule_total} = {square_rule_correct/square_rule_total*100:.1f}%")
    print(f"   Failures: {len(square_rule_failures)}")
    if square_rule_failures:
        print("   Example failures:")
        for (wk, wp, bk, stm), actual, predicted in square_rule_failures[:10]:
            print(f"     WK {wk} WP {wp} BK {bk}: actual={'W' if actual=='W' else 'D'}, predicted={'W' if predicted else 'D'}")
    print()
    
    # 5. Key squares analysis
    print("5. KEY SQUARES ANALYSIS")
    # On cylinder, key squares for a pawn are the three squares in front of it
    # (file-1, rank+1), (file, rank+1), (file+1, rank+1) with wrap
    
    key_square_stats = {'on_key_win': 0, 'on_key_total': 0, 'off_key_win': 0, 'off_key_total': 0}
    
    for (wk, wp, bk, stm), val in cyl_dict.items():
        if stm != 'w':
            continue
        wp_f, wp_r = square_to_coords(wp)
        wk_f, wk_r = square_to_coords(wk)
        
        # Key squares
        key_squares = [
            ((wp_f - 1) % 8, wp_r + 1),
            (wp_f, wp_r + 1),
            ((wp_f + 1) % 8, wp_r + 1)
        ]
        # Filter to valid ranks
        key_squares = [(f, r) for f, r in key_squares if r < 8]
        
        on_key = (wk_f, wk_r) in key_squares
        
        if on_key:
            key_square_stats['on_key_total'] += 1
            if val == 'W':
                key_square_stats['on_key_win'] += 1
        else:
            key_square_stats['off_key_total'] += 1
            if val == 'W':
                key_square_stats['off_key_win'] += 1
    
    print(f"   King on key squares: {key_square_stats['on_key_win']}/{key_square_stats['on_key_total']} wins ({key_square_stats['on_key_win']/key_square_stats['on_key_total']*100:.1f}%)")
    print(f"   King off key squares: {key_square_stats['off_key_win']}/{key_square_stats['off_key_total']} wins ({key_square_stats['off_key_win']/key_square_stats['off_key_total']*100:.1f}%)")
    print()
    
    # 6. Mutual zugzwangs
    print("6. MUTUAL ZUGZWANGS")
    # In KPK, mutual zugzwang = position where side to move loses
    # Since Black can never win in KPK, this means:
    # White to move draws, Black to move draws? No, that's just a draw.
    # True mutual zugzwang in CGT: first player loses.
    # In KPK: White to move -> Black wins (impossible), Black to move -> White wins (normal)
    # So no true mutual zugzwangs in pure KPK.
    # But we can look for positions where White to move draws but Black to move wins for White
    # These are "zugzwang" positions for White.
    
    zugzwangs = []
    for key in cyl_dict:
        wk, wp, bk, _ = key
        wtm_key = (wk, wp, bk, 'w')
        btm_key = (wk, wp, bk, 'b')
        if wtm_key in cyl_dict and btm_key in cyl_dict:
            wtm_val = cyl_dict[wtm_key]
            btm_val = cyl_dict[btm_key]
            # White to move draws, Black to move White wins
            if wtm_val == 'D' and btm_val == 'W':
                zugzwangs.append((wk, wp, bk))
    
    print(f"   Zugzwang positions (WTM draws, BTM White wins): {len(zugzwangs)}")
    for wk, wp, bk in zugzwangs[:20]:
        print(f"     WK {wk} WP {wp} BK {bk}")
    print()
    
    # 7. Pawn file breakdown
    print("7. OUTCOMES BY PAWN FILE (CYLINDER, WHITE TO MOVE)")
    file_stats = defaultdict(lambda: {'W': 0, 'D': 0, 'L': 0, 'X': 0, 'total': 0})
    for (wk, wp, bk, stm), val in cyl_dict.items():
        if stm != 'w':
            continue
        wp_f, _ = square_to_coords(wp)
        file_stats[wp_f]['total'] += 1
        file_stats[wp_f][val] += 1
    
    for f in range(8):
        s = file_stats[f]
        if s['total'] > 0:
            print(f"   File {chr(ord('a')+f)}: {s['total']} positions, W: {s['W']} ({s['W']/s['total']*100:.1f}%), D: {s['D']} ({s['D']/s['total']*100:.1f}%)")
    print()
    
    # 8. Pawn rank breakdown
    print("8. OUTCOMES BY PAWN RANK (CYLINDER, WHITE TO MOVE)")
    rank_stats = defaultdict(lambda: {'W': 0, 'D': 0, 'L': 0, 'X': 0, 'total': 0})
    for (wk, wp, bk, stm), val in cyl_dict.items():
        if stm != 'w':
            continue
        _, wp_r = square_to_coords(wp)
        rank_stats[wp_r]['total'] += 1
        rank_stats[wp_r][val] += 1
    
    for r in range(1, 7):
        s = rank_stats[r]
        if s['total'] > 0:
            print(f"   Rank {r+1}: {s['total']} positions, W: {s['W']} ({s['W']/s['total']*100:.1f}%), D: {s['D']} ({s['D']/s['total']*100:.1f}%)")
    print()
    
    # 9. Cylinder-specific wins (rook pawns)
    print("9. ROOK PAWN ANALYSIS (FILES a AND h)")
    rook_pawn_wins = 0
    rook_pawn_total = 0
    for (wk, wp, bk, stm), val in cyl_dict.items():
        if stm != 'w':
            continue
        wp_f, _ = square_to_coords(wp)
        if wp_f == 0 or wp_f == 7:
            rook_pawn_total += 1
            if val == 'W':
                rook_pawn_wins += 1
    
    print(f"   Rook pawn (a/h) WTM: {rook_pawn_wins}/{rook_pawn_total} wins ({rook_pawn_wins/rook_pawn_total*100:.1f}%)")
    
    # Compare with flat
    flat_rook_wins = 0
    flat_rook_total = 0
    for (wk, wp, bk, stm), val in flat_dict.items():
        if stm != 'w':
            continue
        wp_f, _ = square_to_coords(wp)
        if wp_f == 0 or wp_f == 7:
            flat_rook_total += 1
            if val == 'W':
                flat_rook_wins += 1
    
    print(f"   Flat rook pawn WTM: {flat_rook_wins}/{flat_rook_total} wins ({flat_rook_wins/flat_rook_total*100:.1f}%)")
    print()
    
    return cyl_dict, flat_dict, classic_draws_to_wins, wins_to_draws, zugzwangs

if __name__ == '__main__':
    analyze_cylinder_kpk()