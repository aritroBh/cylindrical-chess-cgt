#!/usr/bin/env python3
"""Mini-solver for king-and-pawn endgames on small boards.

Implements SPEC.md rules for kings + up to 2 pawns per side on boards up to 5x5.
Promotion wins unless the new queen can be captured at once.
Uses retrograde analysis (least fixed point).
"""

import sys
import itertools
from collections import deque
from dataclasses import dataclass
from typing import Optional

# Result values from White's POV
WIN = 1      # White wins
LOSS = -1    # Black wins
DRAW = 0     # Draw
ILLEGAL = 2  # Illegal position

# Piece encoding
WHITE = 0
BLACK = 1

@dataclass(frozen=True)
class Position:
    """Immutable position representation."""
    wp: int      # bitboard of white pawns
    bp: int      # bitboard of black pawns
    wk: int      # white king square
    bk: int      # black king square
    stm: int     # side to move (0=White, 1=Black)
    ep: int      # en passant target square (-1 if none)
    # No officers in this mini-solver (max 2 pawns each, promotion ends game)
    
    def key(self) -> tuple:
        return (self.wp, self.bp, self.wk, self.bk, self.stm, self.ep)

def square(file: int, rank: int, W: int) -> int:
    return rank * W + file

def file_of(sq: int, W: int) -> int:
    return sq % W

def rank_of(sq: int, W: int) -> int:
    return sq // W

def is_adjacent(s1: int, s2: int, W: int, wrap: bool) -> bool:
    df = abs(file_of(s1, W) - file_of(s2, W))
    if wrap:
        df = min(df, W - df)
    dr = abs(rank_of(s1, W) - rank_of(s2, W))
    return max(df, dr) <= 1

def king_moves(sq: int, W: int, H: int, wrap: bool) -> list[int]:
    moves = []
    f, r = file_of(sq, W), rank_of(sq, W)
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == 0 and dr == 0:
                continue
            nf, nr = f + df, r + dr
            if nr < 0 or nr >= H:
                continue
            if wrap:
                nf = (nf % W + W) % W
            elif nf < 0 or nf >= W:
                continue
            moves.append(square(nf, nr, W))
    return moves

def pawn_attacks(sq: int, color: int, W: int, H: int, wrap: bool) -> list[int]:
    """Squares attacked by a pawn of given color on sq."""
    attacks = []
    f, r = file_of(sq, W), rank_of(sq, W)
    dir = 1 if color == WHITE else -1
    for df in (-1, 1):
        nf, nr = f + df, r + dir
        if nr < 0 or nr >= H:
            continue
        if wrap:
            nf = (nf % W + W) % W
        elif nf < 0 or nf >= W:
            continue
        attacks.append(square(nf, nr, W))
    return attacks

def pawn_can_double_step(sq: int, color: int, W: int, H: int, occ: int) -> Optional[int]:
    """Return target square if pawn can double step, else None."""
    f, r = file_of(sq, W), rank_of(sq, W)
    if color == WHITE:
        if r != 1:  # rank 2 (0-indexed)
            return None
        step1 = square(f, r + 1, W)
        step2 = square(f, r + 2, W)
        if step2 // W >= H:  # would promote
            return None
        if (occ >> step1) & 1 or (occ >> step2) & 1:
            return None
        return step2
    else:
        if r != H - 2:  # rank H-1
            return None
        step1 = square(f, r - 1, W)
        step2 = square(f, r - 2, W)
        if step2 // W < 0:  # would promote
            return None
        if (occ >> step1) & 1 or (occ >> step2) & 1:
            return None
        return step2

def is_legal(pos: Position, W: int, H: int, wrap: bool) -> bool:
    """Check if position is legal."""
    # Kings not adjacent
    if is_adjacent(pos.wk, pos.bk, W, wrap):
        return False
    # No piece overlap
    occ = pos.wp | pos.bp | (1 << pos.wk) | (1 << pos.bk)
    if pos.wp & pos.bp:
        return False
    if (occ >> pos.wk) & 1 != 1 or (occ >> pos.bk) & 1 != 1:
        return False
    # Pawns not on first/last rank
    for sq in range(W * H):
        if (pos.wp >> sq) & 1:
            if rank_of(sq, W) == 0 or rank_of(sq, W) == H - 1:
                return False
        if (pos.bp >> sq) & 1:
            if rank_of(sq, W) == 0 or rank_of(sq, W) == H - 1:
                return False
    # Side not to move not in check
    if is_in_check(pos, W, H, wrap, not pos.stm):
        return False
    # En passant target validity
    if pos.ep >= 0:
        mover = not pos.stm
        skipped = pos.ep
        landed = skipped + (W if mover == WHITE else -W)
        origin = skipped - (W if mover == WHITE else -W)
        if rank_of(skipped, W) != (2 if mover == WHITE else H - 3):
            return False
        opp_pawns = pos.bp if mover == WHITE else pos.wp
        if not ((opp_pawns >> landed) & 1):
            return False
        if (occ >> skipped) & 1 or (occ >> origin) & 1:
            return False
    return True

def is_attacked(pos: Position, sq: int, by: int, W: int, H: int, wrap: bool) -> bool:
    """Is square attacked by given color?"""
    # King attacks
    king_sq = pos.bk if by == BLACK else pos.wk
    if is_adjacent(king_sq, sq, W, wrap):
        return True
    # Pawn attacks
    pawns = pos.bp if by == BLACK else pos.wp
    for p_sq in range(W * H):
        if (pawns >> p_sq) & 1:
            if sq in pawn_attacks(p_sq, by, W, H, wrap):
                return True
    return False

def is_in_check(pos: Position, W: int, H: int, wrap: bool, side: int) -> bool:
    king_sq = pos.wk if side == WHITE else pos.bk
    return is_attacked(pos, king_sq, not side, W, H, wrap)

def generate_moves(pos: Position, W: int, H: int, wrap: bool, ep_on: bool) -> list[Position]:
    """Generate all legal moves from position."""
    moves = []
    us = pos.stm
    them = 1 - us
    occ = pos.wp | pos.bp | (1 << pos.wk) | (1 << pos.bk)
    own_pawns = pos.wp if us == WHITE else pos.bp
    opp_pawns = pos.bp if us == WHITE else pos.wp
    own_king = pos.wk if us == WHITE else pos.bk
    opp_king = pos.bk if us == WHITE else pos.wk
    dir = 1 if us == WHITE else -1
    start_rank = 1 if us == WHITE else H - 2
    promo_rank = H - 1 if us == WHITE else 0
    
    # King moves
    for to in king_moves(own_king, W, H, wrap):
        if (occ >> to) & 1:
            continue
        if to == opp_king:
            continue
        if is_adjacent(to, opp_king, W, wrap):
            continue
        new_pos = Position(
            wp=pos.wp, bp=pos.bp,
            wk=to if us == WHITE else pos.wk,
            bk=to if us == BLACK else pos.bk,
            stm=them, ep=-1
        )
        if not is_in_check(new_pos, W, H, wrap, us):
            moves.append(new_pos)
    
    # Pawn moves
    for from_sq in range(W * H):
        if not ((own_pawns >> from_sq) & 1):
            continue
        f, r = file_of(from_sq, W), rank_of(from_sq, W)
        
        # Single step
        to_sq = square(f, r + dir, W)
        if 0 <= r + dir < H and not ((occ >> to_sq) & 1):
            if r + dir == promo_rank:
                # Promotion - check if queen can be captured at once
                promo_pos = Position(
                    wp=pos.wp & ~(1 << from_sq) if us == WHITE else pos.wp,
                    bp=pos.bp & ~(1 << from_sq) if us == BLACK else pos.bp,
                    wk=pos.wk, bk=pos.bk,
                    stm=them, ep=-1
                )
                # Queen on to_sq - can opponent capture it?
                # Opponent king
                if is_adjacent(opp_king, to_sq, W, wrap):
                    # Capture is legal if it doesn't put own king in check
                    cap_pos = Position(
                        wp=promo_pos.wp, bp=promo_pos.bp,
                        wk=promo_pos.wk, bk=promo_pos.bk,
                        stm=us, ep=-1
                    )
                    # After capture, side to move is us, check if in check
                    if not is_in_check(cap_pos, W, H, wrap, us):
                        continue  # Queen can be captured, not an immediate win
                # Opponent pawns
                can_capture = False
                for p_sq in range(W * H):
                    if (opp_pawns >> p_sq) & 1:
                        if to_sq in pawn_attacks(p_sq, them, W, H, wrap):
                            # Check if capture is legal
                            cap_pos = Position(
                                wp=promo_pos.wp, bp=promo_pos.bp,
                                wk=promo_pos.wk, bk=promo_pos.bk,
                                stm=us, ep=-1
                            )
                            if not is_in_check(cap_pos, W, H, wrap, us):
                                can_capture = True
                                break
                if can_capture:
                    continue  # Queen can be captured
                # Immediate win for promoter
                # We encode this as a terminal WIN for White if White promoted, LOSS if Black promoted
                # For retrograde, we'll handle this specially
                win_val = WIN if us == WHITE else LOSS
                # Create a special terminal position marker
                moves.append(('PROMO_WIN', win_val))
            else:
                new_wp = pos.wp
                new_bp = pos.bp
                if us == WHITE:
                    new_wp = (pos.wp & ~(1 << from_sq)) | (1 << to_sq)
                else:
                    new_bp = (pos.bp & ~(1 << from_sq)) | (1 << to_sq)
                new_pos = Position(
                    wp=new_wp, bp=new_bp,
                    wk=pos.wk, bk=pos.bk,
                    stm=them, ep=-1
                )
                if not is_in_check(new_pos, W, H, wrap, us):
                    moves.append(new_pos)
        
        # Double step
        double_to = pawn_can_double_step(from_sq, us, W, H, occ)
        if double_to is not None:
            if double_to // W == promo_rank:
                # Double step promotes on 4-rank board - no e.p.
                promo_pos = Position(
                    wp=pos.wp & ~(1 << from_sq) if us == WHITE else pos.wp,
                    bp=pos.bp & ~(1 << from_sq) if us == BLACK else pos.bp,
                    wk=pos.wk, bk=pos.bk,
                    stm=them, ep=-1
                )
                # Check if queen can be captured
                can_capture = False
                if is_adjacent(opp_king, double_to, W, wrap):
                    cap_pos = Position(wp=promo_pos.wp, bp=promo_pos.bp, wk=promo_pos.wk, bk=promo_pos.bk, stm=us, ep=-1)
                    if not is_in_check(cap_pos, W, H, wrap, us):
                        can_capture = True
                if not can_capture:
                    for p_sq in range(W * H):
                        if (opp_pawns >> p_sq) & 1:
                            if double_to in pawn_attacks(p_sq, them, W, H, wrap):
                                cap_pos = Position(wp=promo_pos.wp, bp=promo_pos.bp, wk=promo_pos.wk, bk=promo_pos.bk, stm=us, ep=-1)
                                if not is_in_check(cap_pos, W, H, wrap, us):
                                    can_capture = True
                                    break
                if not can_capture:
                    win_val = WIN if us == WHITE else LOSS
                    moves.append(('PROMO_WIN', win_val))
            else:
                new_wp = pos.wp
                new_bp = pos.bp
                if us == WHITE:
                    new_wp = (pos.wp & ~(1 << from_sq)) | (1 << double_to)
                else:
                    new_bp = (pos.bp & ~(1 << from_sq)) | (1 << double_to)
                new_ep = -1
                if ep_on:
                    # Check if opponent pawn can capture en passant
                    ep_target = double_to - dir * W
                    for df in (-1, 1):
                        cap_sq = square(f + df, r + dir, W)
                        if wrap:
                            cap_sq = square((f + df) % W, r + dir, W)
                        if 0 <= cap_sq < W * H and ((opp_pawns >> cap_sq) & 1):
                            new_ep = ep_target
                            break
                new_pos = Position(
                    wp=new_wp, bp=new_bp,
                    wk=pos.wk, bk=pos.bk,
                    stm=them, ep=new_ep
                )
                if not is_in_check(new_pos, W, H, wrap, us):
                    moves.append(new_pos)
        
        # Captures (including en passant)
        for df in (-1, 1):
            nf = f + df
            if wrap:
                nf = (nf % W + W) % W
            elif nf < 0 or nf >= W:
                continue
            nr = r + dir
            if nr < 0 or nr >= H:
                continue
            cap_sq = square(nf, nr, W)
            
            # Normal capture
            if (opp_pawns >> cap_sq) & 1:
                new_wp = pos.wp
                new_bp = pos.bp
                if us == WHITE:
                    new_wp = (pos.wp & ~(1 << from_sq)) | (1 << cap_sq)
                    new_bp = pos.bp & ~(1 << cap_sq)
                else:
                    new_bp = (pos.bp & ~(1 << from_sq)) | (1 << cap_sq)
                    new_wp = pos.wp & ~(1 << cap_sq)
                if nr == promo_rank:
                    # Promotion by capture - check if queen can be captured
                    promo_pos = Position(wp=new_wp, bp=new_bp, wk=pos.wk, bk=pos.bk, stm=them, ep=-1)
                    can_capture = False
                    if is_adjacent(opp_king, cap_sq, W, wrap):
                        cap_pos = Position(wp=promo_pos.wp, bp=promo_pos.bp, wk=promo_pos.wk, bk=promo_pos.bk, stm=us, ep=-1)
                        if not is_in_check(cap_pos, W, H, wrap, us):
                            can_capture = True
                    if not can_capture:
                        for p_sq in range(W * H):
                            if ( (pos.bp if us == WHITE else pos.wp) >> p_sq ) & 1:
                                # Wait, we already removed the captured pawn
                                pass
                    if not can_capture:
                        win_val = WIN if us == WHITE else LOSS
                        moves.append(('PROMO_WIN', win_val))
                else:
                    new_pos = Position(wp=new_wp, bp=new_bp, wk=pos.wk, bk=pos.bk, stm=them, ep=-1)
                    if not is_in_check(new_pos, W, H, wrap, us):
                        moves.append(new_pos)
            
            # En passant capture
            elif ep_on and cap_sq == pos.ep:
                # Captured pawn is on skipped square
                captured_sq = cap_sq - dir * W
                new_wp = pos.wp
                new_bp = pos.bp
                if us == WHITE:
                    new_wp = (pos.wp & ~(1 << from_sq)) | (1 << cap_sq)
                    new_bp = pos.bp & ~(1 << captured_sq)
                else:
                    new_bp = (pos.bp & ~(1 << from_sq)) | (1 << cap_sq)
                    new_wp = pos.wp & ~(1 << captured_sq)
                new_pos = Position(wp=new_wp, bp=new_bp, wk=pos.wk, bk=pos.bk, stm=them, ep=-1)
                if not is_in_check(new_pos, W, H, wrap, us):
                    moves.append(new_pos)
    
    return moves

def solve_board(W: int, H: int, wrap: bool, ep_on: bool) -> dict[tuple, int]:
    """Solve all positions on a WxH board using retrograde analysis."""
    # Generate all legal positions
    all_positions = []
    pos_to_idx = {}
    
    squares = list(range(W * H))
    pawn_squares = [sq for sq in squares if 1 <= rank_of(sq, W) <= H - 2]
    
    # Max 2 pawns per side
    for wp_count in range(3):
        for bp_count in range(3):
            if wp_count + bp_count > 4:  # limit total pawns
                continue
            for wp_sqs in itertools.combinations(pawn_squares, wp_count):
                wp_bb = sum(1 << sq for sq in wp_sqs)
                for bp_sqs in itertools.combinations([sq for sq in pawn_squares if sq not in wp_sqs], bp_count):
                    bp_bb = sum(1 << sq for sq in bp_sqs)
                    pawn_occ = wp_bb | bp_bb
                    free_squares = [sq for sq in squares if not (pawn_occ >> sq) & 1]
                    for wk, bk in itertools.permutations(free_squares, 2):
                        if is_adjacent(wk, bk, W, wrap):
                            continue
                        occ = pawn_occ | (1 << wk) | (1 << bk)
                        for stm in (WHITE, BLACK):
                            for ep in [-1] + pawn_squares:
                                pos = Position(wp=wp_bb, bp=bp_bb, wk=wk, bk=bk, stm=stm, ep=ep)
                                if is_legal(pos, W, H, wrap):
                                    idx = len(all_positions)
                                    all_positions.append(pos)
                                    pos_to_idx[pos.key()] = idx
    
    print(f"Generated {len(all_positions)} legal positions")
    
    # Build move graph
    moves_from = [[] for _ in all_positions]
    moves_to = [[] for _ in all_positions]
    terminal_value = [None] * len(all_positions)  # WIN/LOSS/DRAW for terminals
    promo_wins = []  # list of (idx, win_val) for promo wins
    
    for idx, pos in enumerate(all_positions):
        moves = generate_moves(pos, W, H, wrap, ep_on)
        for move in moves:
            if isinstance(move, tuple) and move[0] == 'PROMO_WIN':
                promo_wins.append((idx, move[1]))
            else:
                key = move.key()
                if key in pos_to_idx:
                    target_idx = pos_to_idx[key]
                    moves_from[idx].append(target_idx)
                    moves_to[target_idx].append(idx)
                else:
                    # Move leads to illegal position (shouldn't happen if generate_moves is correct)
                    pass
    
    # Retrograde analysis
    # Result: WIN (1), LOSS (-1), DRAW (0), UNKNOWN (None)
    result = [None] * len(all_positions)
    remaining_moves = [len(moves_from[i]) for i in range(len(all_positions))]
    
    queue = deque()
    
    # Initialize terminals
    for idx in range(len(all_positions)):
        if remaining_moves[idx] == 0:
            # No legal moves
            if is_in_check(all_positions[idx], W, H, wrap, all_positions[idx].stm):
                result[idx] = LOSS  # Checkmate = loss for side to move
            else:
                result[idx] = DRAW  # Stalemate = draw
            queue.append(idx)
    
    # Promotion wins
    for idx, win_val in promo_wins:
        if result[idx] is None:
            result[idx] = win_val
            queue.append(idx)
    
    # Propagate
    while queue:
        idx = queue.popleft()
        val = result[idx]
        for pred in moves_to[idx]:
            if result[pred] is not None:
                continue
            pred_pos = all_positions[pred]
            if pred_pos.stm == WHITE:
                # White to move
                if val == WIN:
                    result[pred] = WIN
                    queue.append(pred)
                else:
                    remaining_moves[pred] -= 1
                    if remaining_moves[pred] == 0:
                        result[pred] = LOSS
                        queue.append(pred)
            else:
                # Black to move
                if val == LOSS:
                    result[pred] = LOSS
                    queue.append(pred)
                else:
                    remaining_moves[pred] -= 1
                    if remaining_moves[pred] == 0:
                        result[pred] = WIN
                        queue.append(pred)
    
    # Remaining are draws
    for idx in range(len(all_positions)):
        if result[idx] is None:
            result[idx] = DRAW
    
    # Build result dict
    result_dict = {}
    for idx, pos in enumerate(all_positions):
        result_dict[pos.key()] = result[idx]
    
    return result_dict

def parse_position(line: str, W: int, H: int) -> Optional[Position]:
    """Parse a position line in SPEC.md format."""
    tokens = line.strip().split()
    if not tokens or tokens[0].startswith('#'):
        return None
    
    wp = bp = 0
    wk = bk = -1
    stm = -1
    ep = -1
    ep_seen = False
    
    for tok in tokens:
        if tok in ('w', 'b'):
            stm = 0 if tok == 'w' else 1
            continue
        if stm >= 0 and not ep_seen:
            ep_seen = True
            if tok != '-':
                f = ord(tok[0]) - ord('a')
                r = int(tok[1:]) - 1
                ep = square(f, r, W)
            continue
        
        c = tok[0]
        color = WHITE if c.isupper() else BLACK
        f = ord(tok[1].lower()) - ord('a')
        r = int(tok[2:]) - 1
        sq = square(f, r, W)
        
        piece = c.upper()
        if piece == 'K':
            if color == WHITE:
                wk = sq
            else:
                bk = sq
        elif piece == 'P':
            if color == WHITE:
                wp |= 1 << sq
            else:
                bp |= 1 << sq
    
    if wk < 0 or bk < 0 or stm < 0:
        return None
    
    return Position(wp=wp, bp=bp, wk=wk, bk=bk, stm=stm, ep=ep)

def result_char(val: int) -> str:
    if val == WIN:
        return 'W'
    elif val == LOSS:
        return 'L'
    elif val == DRAW:
        return 'D'
    else:
        return 'X'

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--board', required=True, help='e.g., cyl:4x5 or flat:5x5')
    parser.add_argument('--ep', default='on', choices=['on', 'off'])
    parser.add_argument('--promote', default='Q', help='ignored, always Q')
    parser.add_argument('--cap', default='1', help='ignored')
    parser.add_argument('--moves', action='store_true', help='show move values')
    args = parser.parse_args()
    
    kind, size = args.board.split(':')
    W, H = map(int, size.split('x'))
    wrap = kind == 'cyl'
    ep_on = args.ep == 'on'
    
    if W > 5 or H > 5:
        print(f"Board {W}x{H} too large for mini-solver (max 5x5)", file=sys.stderr)
        return 1
    
    print(f"Solving {kind}:{W}x{H}...", file=sys.stderr)
    results = solve_board(W, H, wrap, ep_on)
    print(f"Solved {len(results)} positions", file=sys.stderr)
    
    # Read input positions and output results
    for line in sys.stdin:
        line = line.strip()
        if not line or line.startswith('#'):
            print(line)
            continue
        pos = parse_position(line, W, H)
        if pos is None:
            print(f"{line} | X X")
            continue
        val = results.get(pos.key())
        if val is None:
            print(f"{line} | X X")
        else:
            print(f"{line} | {result_char(val)} {result_char(val)}")

if __name__ == '__main__':
    sys.exit(main())