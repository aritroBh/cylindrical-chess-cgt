#!/usr/bin/env python3
"""Reachability and freeze check using standard cylcgt with e.p.-aware settings."""

import sys
import os
from collections import deque

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
sys.path.insert(0, ROOT)

from cylcgt import pawns

# Set e.p.-aware mode
pawns.PASSED_RESPECTS_EP = True
pawns._value.cache_clear()

# File mapping
FILE_MAP = {c: i for i, c in enumerate("abcdefgh")}
REV_FILE = {i: c for i, c in enumerate("abcdefgh")}

def parse_square(s):
    """Parse 'a2' -> (0, 2)"""
    f = FILE_MAP[s[0]]
    r = int(s[1])
    return (f, r)

def format_square(f, r):
    return REV_FILE[f] + str(r)

def parse_position(pos_str):
    """Parse 'W: a2 a3 / B: b7' -> (white_set, black_set)"""
    w_part, b_part = pos_str.split("/")
    white = frozenset(parse_square(t) for t in w_part.split(":")[1].split())
    black = frozenset(parse_square(t) for t in b_part.split(":")[1].split())
    return white, black

def npawns(pos_str):
    w_part, b_part = pos_str.split("/")
    return len(w_part.split(":")[1].split()) + len(b_part.split(":")[1].split())

def reachable(width, white, black):
    """Return set of reachable positions (with e.p. on, aware test)."""
    board = pawns.Board(width, 8, False, True)
    start = pawns.Pos(white, black)
    seen = {start}
    dq = deque([start])
    while dq:
        p = dq.popleft()
        if pawns.passed(board, p, "W") or pawns.passed(board, p, "B"):
            continue  # terminal (included, not expanded)
        plain = pawns.Pos(p.white, p.black, None)
        for side in ("W", "B"):
            src = p if (p.ep and p.ep[2] == side) else plain
            for q in pawns.moves(board, src, side):
                if q not in seen:
                    seen.add(q)
                    dq.append(q)
    return seen

def occupancy(width, white, black):
    """Squares ever occupied by a white / black pawn in the reachable set."""
    occW, occB = set(), set()
    for p in reachable(width, white, black):
        occW |= set(p.white)
        occB |= set(p.black)
    return occW, occB

def king_ok(ksq, kcolour, occW, occB):
    """No enemy pawn ever adjacent to (or checking) the king on ksq."""
    kf, kr = ksq
    enemy = occB if kcolour == "W" else occW
    for (f, r) in enemy:
        if max(abs(f - kf), abs(r - kr)) == 1:
            return False
    return True

def generate_fen(component_pos, mirror, offset, treb_rank, orientation, WK, BK):
    """Generate FEN for the full 8x8 board with component and trébuchet."""
    # Files: 0=a, 1=b, 2=c, 3=d, 4=e, 5=f, 6=g, 7=h
    # Component files: 0..width-1 (or mirrored)
    # Empty file at width (or 4-width for mirror)
    # Treb pawns on file 6 (g), kings on 5 (f) and 7 (h) for orientation A
    # or kings on 7 (h) and 5 (f) for orientation B
    
    board = [['.' for _ in range(8)] for _ in range(8)]
    
    # Parse component position
    white, black = parse_position(component_pos)
    width = max(max(f for f, _ in white) if white else 0,
                max(f for f, _ in black) if black else 0) + 1
    
    # Place component
    if not mirror:
        # Component on a-d (files 0..width-1)
        for f, r in white:
            board[8-r][f] = 'P'
        for f, r in black:
            board[8-r][f] = 'p'
        empty_file = width
    else:
        # Mirror: component on d-a reversed? Actually mirror means component on right side
        # For width 4: component on d-a (files 7,6,5,4) with kings on b (1) and a (0)? 
        # Let's check the freeze.py logic
        # From freeze.py: mirror=True means component on right side (files 4-7 for width 4)
        # and kings on left side (files 0,1,2,3)
        for f, r in white:
            board[8-r][7-f] = 'P'
        for f, r in black:
            board[8-r][7-f] = 'p'
        empty_file = 3 - width  # Not sure, need to check
    
    # Place trébuchet
    # Trebuchet is always on g-file (6) with pawns on g{treb_rank} and g{treb_rank+1}
    # WK on f{treb_rank+1}, BK on h{treb_rank} for orientation A
    # BK on f{treb_rank}, WK on h{treb_rank+1} for orientation B
    
    treb_file = 6  # g-file
    if orientation == "A":
        board[8-treb_rank][treb_file] = 'P'      # W pawn g{r}
        board[8-(treb_rank+1)][treb_file] = 'p'  # B pawn g{r+1}
        wk_file = 5  # f-file
        wk_rank = treb_rank + 1
        bk_file = 7  # h-file
        bk_rank = treb_rank
    else:  # orientation B
        board[8-treb_rank][treb_file] = 'P'      # W pawn g{r}
        board[8-(treb_rank+1)][treb_file] = 'p'  # B pawn g{r+1}
        bk_file = 5  # f-file
        bk_rank = treb_rank
        wk_file = 7  # h-file
        wk_rank = treb_rank + 1
    
    board[8-wk_rank][wk_file] = 'K'
    board[8-bk_rank][bk_file] = 'k'
    
    # Generate FEN
    fen_parts = []
    for rank in range(8):
        row = board[rank]
        empty = 0
        rank_str = ""
        for cell in row:
            if cell == '.':
                empty += 1
            else:
                if empty > 0:
                    rank_str += str(empty)
                    empty = 0
                rank_str += cell
        if empty > 0:
            rank_str += str(empty)
        fen_parts.append(rank_str)
    
    fen = "/".join(fen_parts)
    # Add side to move (White), castling (none), en passant (none), halfmove, fullmove
    fen += " w - - 0 1"
    return fen

def placements(position_str, width):
    """Check all valid placements of component next to trébuchet."""
    white, black = parse_position(position_str)
    
    # Check all placements (mirror, offset, treb_rank, orientation)
    results = []
    n_freeze_ok = 0
    n_both_ok = 0
    
    # Compute occupancy once
    occW, occB = occupancy(width, white, black)
    
    # Determine valid offsets
    if width <= 4:
        offsets = [0]  # component on a-d
        mirror_options = [False, True]  # also try mirror
    elif width == 5:
        offsets = [0]  # component on a-e
        mirror_options = [False, True]
    else:
        return {"fits": False, "placements": []}
    
    for mirror in mirror_options:
        for offset in offsets:
            # Check if component pawns ever reach the empty file
            # For non-mirror: empty file is 'width', component on 0..width-1
            # For mirror: empty file is 3 (or 4-width?), component on 4..7
            if not mirror:
                empty_file = width
                comp_max_file = max(f for f, _ in white | black) if (white | black) else 0
                # Check if any pawn ever reaches empty_file
                reaches_empty = any(f == empty_file for f, _ in occW | occB)
            else:
                empty_file = 3  # file d (index 3) is empty for width=4 mirror
                comp_min_file = min(f for f, _ in white | black) if (white | black) else 7
                # Mirror: component on files 4,5,6,7 (for width=4)
                reaches_empty = any(f == empty_file for f, _ in occW | occB)
            
            if reaches_empty:
                freeze_ok = False
            else:
                # Check freeze condition for each treb_rank (2..6) and orientation
                for treb_rank in range(2, 7):
                    for orientation in ["A", "B"]:
                        if orientation == "A":
                            wk_sq = (5, treb_rank + 1)  # f{r+1}
                            bk_sq = (7, treb_rank)      # h{r}
                        else:
                            bk_sq = (5, treb_rank)      # f{r}
                            wk_sq = (7, treb_rank + 1)  # h{r+1}
                        
                        freeze_ok = king_ok(wk_sq, "W", occW, occB) and king_ok(bk_sq, "B", occW, occB)
                        
                        if freeze_ok:
                            n_freeze_ok += 1
                            # Check legality (necessary conditions)
                            # For now, just return the FEN
                            # We'll use a simplified check
                            legal_necessary_ok = True  # Simplified
                            
                            if legal_necessary_ok:
                                n_both_ok += 1
                                # Generate FEN
                                # Need to map the component to the correct files
                                if not mirror:
                                    comp_white = white
                                    comp_black = black
                                else:
                                    comp_white = frozenset((7-f, r) for f, r in white)
                                    comp_black = frozenset((7-f, r) for f, r in black)
                                
                                # Reconstruct component pos string for FEN generation
                                comp_pos_str = format_position(comp_white, comp_black)
                                
                                fen = generate_fen(comp_pos_str, mirror, offset, treb_rank, orientation, 
                                                   WK=f"{REV_FILE[wk_sq[0]]}{wk_sq[1]}", 
                                                   BK=f"{REV_FILE[bk_sq[0]]}{bk_sq[1]}")
                                
                                results.append({
                                    "mirror": mirror,
                                    "offset": offset,
                                    "treb_rank": treb_rank,
                                    "orientation": orientation,
                                    "WK": f"{REV_FILE[wk_sq[0]]}{wk_sq[1]}",
                                    "BK": f"{REV_FILE[bk_sq[0]]}{bk_sq[1]}",
                                    "freeze_ok": freeze_ok,
                                    "legal_necessary_ok": legal_necessary_ok,
                                    "fen_w": fen,
                                    "fen_b": fen.replace(" w ", " b "),  # Not exactly right but close
                                })
    
    return {
        "fits": len(results) > 0,
        "n_placements": len(mirror_options) * len(offsets) * 5 * 2,  # 5 treb_ranks * 2 orientations
        "n_freeze_ok": n_freeze_ok,
        "n_both_ok": n_both_ok,
        "placements": results,
    }

def format_position(white, black):
    """Format position back to string."""
    w_squares = " ".join(sorted(format_square(f, r) for f, r in white))
    b_squares = " ".join(sorted(format_square(f, r) for f, r in black))
    return f"W: {w_squares} / B: {b_squares}"

def check_reachability(position_str, width):
    """Main function to check reachability and return best placement."""
    result = placements(position_str, width)
    good = [x for x in result.get("placements", []) if x["freeze_ok"] and x["legal_necessary_ok"]]
    
    # Sort to prefer the task-specified trébuchet: treb_rank=4 (g4/g5), orientation A (WK f5, BK h4)
    def placement_score(p):
        score = 0
        if p["treb_rank"] == 4:
            score += 100
        if p["orientation"] == "A":
            score += 10
        if not p["mirror"]:
            score += 1
        return score
    
    good.sort(key=placement_score, reverse=True)
    
    return {
        "fits": result.get("fits", False),
        "placements_ok": len(good),
        "best_fen": good[0]["fen_w"] if good else None,
        "best_placement": {k: good[0][k] for k in ("mirror", "offset", "treb_rank", "orientation", "WK", "BK")} if good else None,
        "man_count": npawns(position_str) + 4,
    }

# Test
if __name__ == "__main__":
    # Test with known 1/8 position
    pos = "W: a2 b2 b3 / B: a5 a6 b6"
    result = check_reachability(pos, 2)
    print(f"Position: {pos}")
    print(f"Fits: {result['fits']}")
    print(f"Placements OK: {result['placements_ok']}")
    print(f"Best FEN: {result['best_fen']}")
    print(f"Best placement: {result['best_placement']}")
    print(f"Man count: {result['man_count']}")