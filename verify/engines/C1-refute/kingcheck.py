"""Independent check that the tablebase move list = all legal moves (pawn moves + king moves).
    cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/engines/C1-refute/kingcheck.py
"""
import sys
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/verify/engines/C1-refute")
import indep
def attacked_by(board, sq, colour):  # colour 'w' or 'b' attacks sq (kings and pawns only)
    f, r = sq
    for (g, s), p in board.items():
        if colour == "w" and p == "P" and s + 1 == r and abs(g - f) == 1: return True
        if colour == "b" and p == "p" and s - 1 == r and abs(g - f) == 1: return True
        if p == ("K" if colour == "w" else "k") and max(abs(g - f), abs(s - r)) == 1: return True
    return False
out = indep.main()
bad = 0
for o in out:
    board, stm, ep = indep.parse_fen(o["fen"])
    me = "K" if stm == "w" else "k"
    ks = [s for s, p in board.items() if p == me][0]
    opp = "b" if stm == "w" else "w"
    legal = set()
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == dr == 0: continue
            t = (ks[0] + df, ks[1] + dr)
            if not (0 <= t[0] < 8 and 1 <= t[1] <= 8): continue
            p = board.get(t)
            if p is not None and (p.isupper() == (stm == "w")): continue
            b2 = dict(board); del b2[ks]; b2[t] = me
            if attacked_by(b2, t, opp): continue
            legal.add(indep.sqn(*ks) + indep.sqn(*t))
    # side to move not in check at root (pawn moves then all legal: no sliders, no pins)
    assert not attacked_by(board, ks, opp), o["fen"]
    if legal != set(o["king_moves"]):
        bad += 1; print("MISMATCH", o["id"], o["fen"], legal ^ set(o["king_moves"]))
print("positions", len(out), "king-move-set mismatches", bad)
