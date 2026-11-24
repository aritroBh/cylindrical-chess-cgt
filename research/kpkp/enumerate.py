#!/usr/bin/env python3
"""Enumerate all legal KPKP and KPPK positions on flat and cylindrical 8x8 boards.

Optimized version - precompute attack tables.
"""

import sys

N = 8
FILES = "abcdefgh"


def name(s):
    return f"{FILES[s % N]}{s // N + 1}"


def build_tables(wrap):
    """Precompute king distance and pawn attacks."""
    # king distance table
    king_dist = [[0]*64 for _ in range(64)]
    for a in range(64):
        for b in range(64):
            df = abs(a % N - b % N)
            if wrap:
                df = min(df, N - df)
            king_dist[a][b] = max(df, abs(a // N - b // N))
    
    # pawn attacks: pawn_attacks[color][pawn_sq][target_sq] = bool
    pawn_attacks = [[[False]*64 for _ in range(64)] for _ in range(2)]
    for color in (0, 1):
        for p in range(64):
            f, r = p % N, p // N
            for df in (-1, 1):
                g = f + df
                if wrap:
                    g %= N
                elif not 0 <= g < N:
                    continue
                if color == 0:  # white attacks up
                    t = (r + 1) * N + g
                else:  # black attacks down
                    t = (r - 1) * N + g
                if 0 <= t < 64:
                    pawn_attacks[color][p][t] = True
    return king_dist, pawn_attacks


def is_in_check(wk, bk, wp_list, bp_list, king_dist, pawn_attacks, side_to_move):
    """Check if the given side's king is in check."""
    if side_to_move == 0:  # White king
        if king_dist[bk][wk] <= 1:
            return True
        for bp in bp_list:
            if pawn_attacks[1][bp][wk]:
                return True
    else:  # Black king
        if king_dist[wk][bk] <= 1:
            return True
        for wp in wp_list:
            if pawn_attacks[0][wp][bk]:
                return True
    return False


def enumerate_kpkp(wrap, king_dist, pawn_attacks):
    """Enumerate all legal KPKP positions (White K+P vs Black K+P)."""
    positions = []
    append = positions.append
    for wk in range(64):
        for bk in range(64):
            if bk == wk or king_dist[wk][bk] <= 1:
                continue
            for wp in range(8, 56):
                if wp == wk or wp == bk:
                    continue
                for bp in range(8, 56):
                    if bp == wk or bp == bk or bp == wp:
                        continue
                    # White to move
                    if not is_in_check(wk, bk, [wp], [bp], king_dist, pawn_attacks, 1):
                        append((wk, bk, wp, bp, 0))
                    # Black to move
                    if not is_in_check(wk, bk, [wp], [bp], king_dist, pawn_attacks, 0):
                        append((wk, bk, wp, bp, 1))
    return positions


def enumerate_kppk(wrap, king_dist, pawn_attacks):
    """Enumerate all legal KPPK positions (White K+P+P vs Black K+P)."""
    positions = []
    append = positions.append
    for wk in range(64):
        for bk in range(64):
            if bk == wk or king_dist[wk][bk] <= 1:
                continue
            for wp1 in range(8, 56):
                if wp1 == wk or wp1 == bk:
                    continue
                for wp2 in range(wp1 + 1, 56):
                    if wp2 == wk or wp2 == bk:
                        continue
                    for bp in range(8, 56):
                        if bp == wk or bp == bk or bp == wp1 or bp == wp2:
                            continue
                        # White to move
                        if not is_in_check(wk, bk, [wp1, wp2], [bp], king_dist, pawn_attacks, 1):
                            append((wk, bk, wp1, wp2, bp, 0))
                        # Black to move
                        if not is_in_check(wk, bk, [wp1, wp2], [bp], king_dist, pawn_attacks, 0):
                            append((wk, bk, wp1, wp2, bp, 1))
    return positions


def write_kpkp_input(positions, filename):
    """Write positions in kpsolve input format."""
    out_lines = []
    for wk, bk, wp, bp, stm in positions:
        s = 'w' if stm == 0 else 'b'
        out_lines.append(f"K{name(wk)} P{name(wp)} k{name(bk)} P{name(bp)} {s} -")
    with open(filename, 'w') as f:
        f.write('\n'.join(out_lines) + '\n')


def write_kppk_input(positions, filename):
    """Write positions in kpsolve input format."""
    out_lines = []
    for wk, bk, wp1, wp2, bp, stm in positions:
        s = 'w' if stm == 0 else 'b'
        out_lines.append(f"K{name(wk)} P{name(wp1)} P{name(wp2)} k{name(bk)} P{name(bp)} {s} -")
    with open(filename, 'w') as f:
        f.write('\n'.join(out_lines) + '\n')


if __name__ == "__main__":
    import os
    
    os.makedirs("research/kpkp", exist_ok=True)
    
    for wrap, board_name in [(0, "flat"), (1, "cyl")]:
        print(f"\n=== {board_name} 8x8 ===")
        king_dist, pawn_attacks = build_tables(wrap)
        
        # KPKP
        print("Enumerating KPKP...")
        kpkp_pos = enumerate_kpkp(wrap, king_dist, pawn_attacks)
        print(f"  {len(kpkp_pos)} legal positions")
        write_kpkp_input(kpkp_pos, f"research/kpkp/kpkp_{board_name}.in")
        
        # KPPK
        print("Enumerating KPPK...")
        kppk_pos = enumerate_kppk(wrap, king_dist, pawn_attacks)
        print(f"  {len(kppk_pos)} legal positions")
        write_kppk_input(kppk_pos, f"research/kpkp/kppk_{board_name}.in")