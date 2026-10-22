#!/usr/bin/env python3
"""KPK solver for 8x8 Möbius strip board.

Uses retrograde analysis (least fixed point) over all legal KPK positions.
Möbius geometry: files wrap with rank flip (r -> 7-r), ranks have boundaries.
Pawn crossing the file seam via capture flips its forward direction.
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

WHITE = 0
BLACK = 1

W = 8
H = 8
N = W * H  # 64

FILES = "abcdefgh"

def sq_name(f: int, r: int) -> str:
    return f"{FILES[f]}{r+1}"

def parse_sq(name: str) -> tuple[int, int]:
    return (FILES.index(name[0]), int(name[1:]) - 1)

def sq_index(f: int, r: int) -> int:
    return r * W + f

def file_of(sq: int) -> int:
    return sq % W

def rank_of(sq: int) -> int:
    return sq // W

# Möbius step function
def mobius_step(sq: int, df: int, dr: int) -> Optional[int]:
    """Step from sq by (df, dr) on Möbius board. Returns None if off board."""
    f = file_of(sq) + df
    r = rank_of(sq) + dr
    
    f_wrapped = False
    if f < 0 or f >= W:
        f = (f + W) % W
        f_wrapped = True
    
    if r < 0 or r >= H:
        return None
    
    # Möbius twist: crossing file seam flips rank
    if f_wrapped:
        r = (H - 1) - r  # 7 - r for 0-indexed
        if r < 0 or r >= H:
            return None
    
    return sq_index(f, r)

# Precompute king moves
KING_MOVES = [[] for _ in range(N)]
KING_MASK = [0] * N
for sq in range(N):
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == 0 and dr == 0:
                continue
            t = mobius_step(sq, df, dr)
            if t is not None and t != sq:
                KING_MOVES[sq].append(t)
    for t in KING_MOVES[sq]:
        KING_MASK[sq] |= 1 << t

# Precompute pawn capture targets
# White captures: (df, +1), Black captures: (df, -1)
PAWN_CAP_WHITE = [[] for _ in range(N)]
PAWN_CAP_BLACK = [[] for _ in range(N)]
PAWN_FROM_WHITE = [0] * N  # squares from which a white pawn attacks this square
PAWN_FROM_BLACK = [0] * N

for sq in range(N):
    f, r = file_of(sq), rank_of(sq)
    # White pawn on sq captures to (f±1, r+1) with wrap+flip
    for df in (-1, 1):
        t = mobius_step(sq, df, 1)
        if t is not None:
            PAWN_CAP_WHITE[sq].append(t)
            PAWN_FROM_WHITE[t] |= 1 << sq
    # Black pawn on sq captures to (f±1, r-1) with wrap+flip
    for df in (-1, 1):
        t = mobius_step(sq, df, -1)
        if t is not None:
            PAWN_CAP_BLACK[sq].append(t)
            PAWN_FROM_BLACK[t] |= 1 << sq

# Pawn forward steps (no capture)
# White: +1 rank (toward 7), Black: -1 rank (toward 0)
# No file wrap for forward steps
PAWN_FWD_WHITE = [None] * N
PAWN_FWD_BLACK = [None] * N
PAWN_DBL_WHITE = [None] * N
PAWN_DBL_BLACK = [None] * N

for sq in range(N):
    f, r = file_of(sq), rank_of(sq)
    # White single step
    if r + 1 < H:
        PAWN_FWD_WHITE[sq] = sq_index(f, r + 1)
    # White double step from rank 1 (rank 2 in 1-indexed)
    if r == 1 and r + 2 < H:
        PAWN_DBL_WHITE[sq] = sq_index(f, r + 2)
    # Black single step
    if r - 1 >= 0:
        PAWN_FWD_BLACK[sq] = sq_index(f, r - 1)
    # Black double step from rank 6 (rank 7 in 1-indexed)
    if r == 6 and r - 2 >= 0:
        PAWN_DBL_BLACK[sq] = sq_index(f, r - 2)


def is_adjacent(s1: int, s2: int) -> bool:
    """Kings adjacent on Möbius board."""
    return s2 in KING_MOVES[s1]


def is_attacked_by_pawn(sq: int, by_white: bool, pawn_bb: int) -> bool:
    """Is sq attacked by a pawn of given color?"""
    if by_white:
        return (pawn_bb & PAWN_FROM_WHITE[sq]) != 0
    else:
        return (pawn_bb & PAWN_FROM_BLACK[sq]) != 0


def is_in_check(wk: int, bk: int, wp: int, bp: int, side: int) -> bool:
    """Is the king of `side` in check?"""
    king_sq = wk if side == WHITE else bk
    # King attacks
    if (KING_MASK[wk if side == BLACK else bk] >> king_sq) & 1:
        return True
    # Pawn attacks
    if side == WHITE:
        return is_attacked_by_pawn(king_sq, True, bp)
    else:
        return is_attacked_by_pawn(king_sq, False, wp)


@dataclass(frozen=True)
class Position:
    wp: int      # white pawn bitboard (exactly 1 bit)
    bp: int      # black pawn bitboard (0 for KPK)
    wk: int      # white king square
    bk: int      # black king square
    stm: int     # side to move (0=White, 1=Black)
    ep: int      # en passant target square (-1 if none)
    pawn_dir: int  # +1 (toward rank 7) or -1 (toward rank 0) for the white pawn

    def key(self) -> tuple:
        return (self.wp, self.bp, self.wk, self.bk, self.stm, self.ep, self.pawn_dir)


def is_legal(pos: Position) -> bool:
    """Check if KPK position is legal on Möbius board."""
    # Exactly one white pawn, no black pawns
    if pos.bp != 0:
        return False
    if pos.wp == 0 or (pos.wp & (pos.wp - 1)) != 0:
        return False
    
    # Kings not adjacent
    if is_adjacent(pos.wk, pos.bk):
        return False
    
    # No piece overlap
    occ = pos.wp | (1 << pos.wk) | (1 << pos.bk)
    if occ.bit_count() != 3:
        return False
    
    # Pawn not on promotion rank
    pawn_sq = (pos.wp.bit_length() - 1)
    pawn_rank = rank_of(pawn_sq)
    if pos.pawn_dir == 1 and pawn_rank == H - 1:
        return False
    if pos.pawn_dir == -1 and pawn_rank == 0:
        return False
    
    # Side not to move not in check
    if is_in_check(pos.wk, pos.bk, pos.wp, 0, 1 - pos.stm):
        return False
    
    # En passant validity (simplified - only if ep target is valid)
    if pos.ep >= 0:
        # For KPK, ep can only exist if white just double-stepped
        # and black has a pawn to capture - but black has no pawns in KPK
        # So ep should always be -1 for KPK
        return False
    
    return True


def generate_moves(pos: Position) -> list[Position]:
    """Generate all legal moves from KPK position on Möbius board."""
    moves = []
    us = pos.stm
    them = 1 - us
    occ = pos.wp | (1 << pos.wk) | (1 << pos.bk)
    own_king = pos.wk if us == WHITE else pos.bk
    opp_king = pos.bk if us == WHITE else pos.wk
    pawn_sq = (pos.wp.bit_length() - 1)
    pawn_dir = pos.pawn_dir
    
    promo_rank = H - 1 if pawn_dir == 1 else 0
    start_rank = 1 if pawn_dir == 1 else H - 2
    
    # King moves
    for to in KING_MOVES[own_king]:
        if (occ >> to) & 1:
            continue
        if to == opp_king:
            continue
        if is_adjacent(to, opp_king):
            continue
        new_wk = to if us == WHITE else pos.wk
        new_bk = to if us == BLACK else pos.bk
        new_pos = Position(
            wp=pos.wp, bp=0,
            wk=new_wk, bk=new_bk,
            stm=them, ep=-1, pawn_dir=pawn_dir
        )
        # Check if own king would be in check
        if not is_in_check(new_wk, new_bk, new_pos.wp, 0, us):
            moves.append(new_pos)
    
    # Pawn moves (only if it's White's pawn and White to move, or if we generalize)
    # In KPK, only White has a pawn
    if us == WHITE:
        # Single step forward
        fwd = PAWN_FWD_WHITE[pawn_sq]
        if fwd is not None and not ((occ >> fwd) & 1):
            if rank_of(fwd) == promo_rank:
                # Promotion - check if promoted queen can be captured by black king
                # Queen on fwd square - can black king capture it?
                queen_capturable = False
                for k_move in KING_MOVES[pos.bk]:
                    if k_move == fwd:
                        queen_capturable = True
                        break
                if not queen_capturable:
                    moves.append(('PROMO_WIN', WIN))
                # If queen is capturable, pawn cannot move there (it's occupied by black king check above)
                # Actually, if black king is on fwd, the pawn can't move there anyway (occ check)
                # So queen_capturable only matters if black king is ADJACENT to fwd
            else:
                new_wp = (pos.wp & ~(1 << pawn_sq)) | (1 << fwd)
                new_pos = Position(
                    wp=new_wp, bp=0,
                    wk=pos.wk, bk=pos.bk,
                    stm=them, ep=-1, pawn_dir=pawn_dir
                )
                if not is_in_check(new_pos.wk, new_pos.bk, new_pos.wp, 0, us):
                    moves.append(new_pos)
            
            # Double step from starting rank
            dbl = PAWN_DBL_WHITE[pawn_sq]
            if dbl is not None and not ((occ >> dbl) & 1) and not ((occ >> fwd) & 1):
                if rank_of(dbl) == promo_rank:
                    # Double step promotes - check if queen capturable
                    queen_capturable = False
                    for k_move in KING_MOVES[pos.bk]:
                        if k_move == dbl:
                            queen_capturable = True
                            break
                    if not queen_capturable:
                        moves.append(('PROMO_WIN', WIN))
                else:
                    new_wp = (pos.wp & ~(1 << pawn_sq)) | (1 << dbl)
                    new_ep = -1
                    # Check for en passant (black has no pawns in KPK, so no ep)
                    new_pos = Position(
                        wp=new_wp, bp=0,
                        wk=pos.wk, bk=pos.bk,
                        stm=them, ep=new_ep, pawn_dir=pawn_dir
                    )
                    if not is_in_check(new_pos.wk, new_pos.bk, new_pos.wp, 0, us):
                        moves.append(new_pos)
        
        # Captures (diagonally forward)
        for cap_sq in PAWN_CAP_WHITE[pawn_sq]:
            # In KPK, black has no pawns, so no normal captures
            # But black king could be on the capture square
            if cap_sq == pos.bk:
                # Pawn captures king? Illegal in chess
                continue
            # No other pieces to capture in KPK
            pass
    
    # Black has no pawn moves in KPK
    
    return moves


def solve_kpk_mobius() -> dict[tuple, int]:
    """Solve all KPK positions on 8x8 Möbius board using retrograde analysis."""
    print("Generating all legal KPK positions on Möbius 8x8...", file=sys.stderr)
    
    all_positions = []
    pos_to_idx = {}
    
    squares = list(range(N))
    pawn_squares = [sq for sq in squares if 1 <= rank_of(sq) <= H - 2]  # ranks 1-6 (0-indexed)
    
    for wk in squares:
        for bk in squares:
            if wk == bk:
                continue
            if is_adjacent(wk, bk):
                continue
            for pawn_sq in pawn_squares:
                if pawn_sq == wk or pawn_sq == bk:
                    continue
                wp = 1 << pawn_sq
                for pawn_dir in (1, -1):
                    # Check pawn not on promotion rank for its direction
                    if pawn_dir == 1 and rank_of(pawn_sq) == H - 1:
                        continue
                    if pawn_dir == -1 and rank_of(pawn_sq) == 0:
                        continue
                    for stm in (WHITE, BLACK):
                        for ep in (-1,):  # No ep in KPK
                            pos = Position(wp=wp, bp=0, wk=wk, bk=bk, stm=stm, ep=ep, pawn_dir=pawn_dir)
                            if is_legal(pos):
                                idx = len(all_positions)
                                all_positions.append(pos)
                                pos_to_idx[pos.key()] = idx
    
    print(f"Generated {len(all_positions)} legal KPK positions", file=sys.stderr)
    
    # Build move graph
    moves_from = [[] for _ in all_positions]
    moves_to = [[] for _ in all_positions]
    terminal_value = [None] * len(all_positions)
    promo_wins = []
    
    for idx, pos in enumerate(all_positions):
        moves = generate_moves(pos)
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
                    # Move leads to illegal position
                    pass
    
    # Retrograde analysis
    result = [None] * len(all_positions)
    remaining_moves = [len(moves_from[i]) for i in range(len(all_positions))]
    queue = deque()
    
    # Initialize terminals: no legal moves
    for idx in range(len(all_positions)):
        if remaining_moves[idx] == 0:
            pos = all_positions[idx]
            if is_in_check(pos.wk, pos.bk, pos.wp, 0, pos.stm):
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
    
    return result_dict, all_positions


def analyze_results(result_dict: dict, all_positions: list):
    """Analyze KPK results."""
    wtm_total = 0
    wtm_wins = 0
    wtm_draws = 0
    wtm_losses = 0
    
    btm_total = 0
    btm_wins = 0
    btm_draws = 0
    btm_losses = 0
    
    # Mutual zugzwangs: positions where both sides to move lose (i.e., the side to move loses)
    # A mutual zugzwang is a position where whoever moves loses.
    # In our encoding: WTM position is LOSS for White (Black wins), BTM position is WIN for White (White wins).
    # So mutual zugzwang = (WTM=LOSS and BTM=WIN) for the same board position.
    
    # Group by board position (ignoring stm)
    by_board = {}
    for pos_key, val in result_dict.items():
        wp, bp, wk, bk, stm, ep, pawn_dir = pos_key
        board_key = (wp, bp, wk, bk, ep, pawn_dir)
        if board_key not in by_board:
            by_board[board_key] = {}
        by_board[board_key][stm] = val
    
    mutual_zugzwangs = 0
    mutual_zugzwang_positions = []
    wtm_draw_btm_win = 0  # WTM draws, BTM White wins (zugzwang for White)
    wtm_win_btm_draw = 0  # WTM White wins, BTM draws (zugzwang for Black)
    
    for board_key, outcomes in by_board.items():
        if WHITE in outcomes and BLACK in outcomes:
            wtm_val = outcomes[WHITE]
            btm_val = outcomes[BLACK]
            # Mutual zugzwang: WTM loses (LOSS for White = Black wins) AND BTM loses (WIN for White = White wins)
            # That means whoever moves loses.
            if wtm_val == LOSS and btm_val == WIN:
                mutual_zugzwangs += 1
                mutual_zugzwang_positions.append(board_key)
            # Zugzwang for White: WTM draws, BTM White wins
            elif wtm_val == DRAW and btm_val == WIN:
                wtm_draw_btm_win += 1
            # Zugzwang for Black: WTM White wins, BTM draws
            elif wtm_val == WIN and btm_val == DRAW:
                wtm_win_btm_draw += 1
    
    # Count stats
    for pos_key, val in result_dict.items():
        wp, bp, wk, bk, stm, ep, pawn_dir = pos_key
        if stm == WHITE:
            wtm_total += 1
            if val == WIN:
                wtm_wins += 1
            elif val == DRAW:
                wtm_draws += 1
            elif val == LOSS:
                wtm_losses += 1
        else:
            btm_total += 1
            if val == WIN:
                btm_wins += 1
            elif val == DRAW:
                btm_draws += 1
            elif val == LOSS:
                btm_losses += 1
    
    print(f"\n=== KPK on Möbius 8x8 ===")
    print(f"Total legal positions: {len(all_positions)}")
    print(f"White to move: {wtm_total}")
    print(f"  White wins: {wtm_wins} ({wtm_wins/wtm_total*100:.4f}%)")
    print(f"  Draws: {wtm_draws} ({wtm_draws/wtm_total*100:.4f}%)")
    print(f"  Black wins: {wtm_losses} ({wtm_losses/wtm_total*100:.4f}%)")
    print(f"Black to move: {btm_total}")
    print(f"  White wins: {btm_wins} ({btm_wins/btm_total*100:.4f}%)")
    print(f"  Draws: {btm_draws} ({btm_draws/btm_total*100:.4f}%)")
    print(f"  Black wins: {btm_losses} ({btm_losses/btm_total*100:.4f}%)")
    print(f"Mutual zugzwangs (whoever moves loses): {mutual_zugzwangs}")
    print(f"Zugzwangs for White (WTM draws, BTM White wins): {wtm_draw_btm_win}")
    print(f"Zugzwangs for Black (WTM White wins, BTM draws): {wtm_win_btm_draw}")
    
    # Check specific position: Ka6 Pa5 vs Ka8 (White to move)
    # a6 = file 0, rank 5 (0-indexed); a5 = file 0, rank 4; a8 = file 0, rank 7
    wk = sq_index(0, 5)  # a6
    pawn = sq_index(0, 4)  # a5
    bk = sq_index(0, 7)  # a8
    wp = 1 << pawn
    print(f"\nRook-pawn position Ka6 Pa5 vs Ka8:")
    found = False
    for pd in (1, -1):
        pos_wtm = Position(wp=wp, bp=0, wk=wk, bk=bk, stm=WHITE, ep=-1, pawn_dir=pd)
        pos_btm = Position(wp=wp, bp=0, wk=wk, bk=bk, stm=BLACK, ep=-1, pawn_dir=pd)
        if is_legal(pos_wtm):
            val_wtm = result_dict.get(pos_wtm.key())
            val_btm = result_dict.get(pos_btm.key())
            if val_wtm is not None:
                print(f"  pawn_dir={pd}: WTM={'WIN' if val_wtm == WIN else 'DRAW' if val_wtm == DRAW else 'LOSS'}, BTM={'WIN' if val_btm == WIN else 'DRAW' if val_btm == DRAW else 'LOSS'}")
                found = True
    if not found:
        print(f"  NOT FOUND (illegal or not in results)")
    
    return mutual_zugzwangs, mutual_zugzwang_positions


def main():
    result_dict, all_positions = solve_kpk_mobius()
    analyze_results(result_dict, all_positions)
    return 0


if __name__ == '__main__':
    sys.exit(main())