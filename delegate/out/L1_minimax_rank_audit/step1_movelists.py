"""Step 1: compare minimax.legal_moves (original, fixed) with cylcgt.pawns.moves on boards with ranks != 8."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "crosscheck_fixed")); sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
import minimax_orig as mo, minimax_fixed as mf
from cylcgt import pawns

def engine_moves(files, ranks, wrap, ep, text, side):
    b = pawns.Board(files, ranks, wrap, ep); p = pawns.Pos.parse(text)
    return {(x.white, x.black) for x in pawns.moves(b, p, side)}

def mm_moves(m, files, ranks, wrap, ep, text, side):
    b = m.Board(files, ranks, wrap, ep); p = m.parse_position(text)
    return {(x.white, x.black) for x in m.legal_moves(b, p, side)}

def fmt(S):
    return sorted("W:" + " ".join(f"{'abcdefgh'[f]}{r}" for f, r in sorted(w)) + " B:" + " ".join(f"{'abcdefgh'[f]}{r}" for f, r in sorted(k)) for w, k in S)

cases = [
 (3, 7, False, True, "W: a2 / B: c6", "B"),   # Black pawn on rank 6 = ranks-1 of a 7-rank board
 (3, 7, False, True, "W: a2 / B: c6", "W"),
 (3, 6, False, True, "W: a2 / B: c5", "B"),
 (3, 5, False, True, "W: a2 / B: c4", "B"),
 (3, 7, False, True, "W: a2 / B: c7", "B"),   # rank 7 = top rank of 7-rank board: Black pawn on its last... illegal-ish, shows bogus double step
 (8, 8, True, True, "W: a2 / B: c7", "B"),    # control: 8 ranks
]
for files, ranks, wrap, ep, text, side in cases:
    E = engine_moves(files, ranks, wrap, ep, text, side)
    O = mm_moves(mo, files, ranks, wrap, ep, text, side)
    F = mm_moves(mf, files, ranks, wrap, ep, text, side)
    print(f"--- {files}x{ranks} {'cyl' if wrap else 'flat'} ep={ep} {text} side={side}")
    print("  engine :", fmt(E))
    print("  orig   :", fmt(O), "| equals engine:", O == E)
    print("  fixed  :", fmt(F), "| equals engine:", F == E)
    if O != E:
        print("  orig missing:", fmt(E - O), " orig extra:", fmt(O - E))
