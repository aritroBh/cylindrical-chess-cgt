"""Independent check of the CGT(count) predicted winning pawn moves with crosscheck/minimax.py (Codex's solver).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/engines/C1-reproduce/crosscheck_cands.py
"""
import json, sys
from crosscheck import minimax as M
sys.path.insert(0, "engine/suite")
import build_suite as BS

B = M.Board(4, 8, False, True)
FILES = "abcdefgh"
def sq(s): return (FILES.index(s[0]), int(s[1:]))
def uci_child(pos, side, uci):
    # apply a uci pawn move to Position
    a, b = sq(uci[:2]), sq(uci[2:4])
    mine = set(pos.white if side == "W" else pos.black); theirs = set(pos.black if side == "W" else pos.white)
    mine.remove(a); mine.add(b)
    ep = None
    if b in theirs: theirs.remove(b)
    elif a[0] != b[0]:  # e.p.
        cap = (b[0], a[1]); assert cap in theirs and pos.ep and pos.ep[0] == b, (uci, pos); theirs.remove(cap)
    if abs(b[1] - a[1]) == 2 and B.ep:
        ep = ((a[0], (a[1] + b[1]) // 2), b, "B" if side == "W" else "W")
    w, k = (mine, theirs) if side == "W" else (theirs, mine)
    return M.Position(frozenset(w), frozenset(k), ep)

cands = json.load(open("engine/suite/candidates.json"))
rows = {r["id"]: r for r in json.load(open("engine/suite/results.json"))}
grp_keys = {(r["component"], r["stm"]) for r in rows.values()
            if BS.tame(r["value"]["count"]) and not r["features"]["race_sensitive"] and r["treb"].startswith("A")}
mism = 0; n = 0; ng = 0
for c in cands:
    pos = M.Position(frozenset(sq(s) for s in c["white"]), frozenset(sq(s) for s in c["black"]),
                     None if not c["ep"] else ((sq(c["ep"])), (sq(c["ep"])[0], sq(c["ep"])[1] + (-1 if c["stm"] == "W" else 1)), c["stm"]))
    side = c["stm"]; other = "B" if side == "W" else "W"
    mv = c["rules"]["count"]["moves"]
    # move set equality
    kids = set(M.legal_moves(B, pos, side))
    mine = {}
    for m in mv:
        ch = uci_child(pos, side, m[0])
        assert ch in kids, (c["pos"], m[0])
        res = M._winner_after_move(B, ch, side)
        if res is None: res = M.winner(B, ch, other)
        mine[m[0]] = (res == side)
    assert len(kids) == len(mv), (c["pos"], len(kids), len(mv))
    cg = {m[0]: m[4] for m in mv}
    n += 1
    key = (c["pos"], side)
    if key in grp_keys: ng += 1
    if mine != cg:
        mism += 1
        print("MISMATCH", c["pos"], side, cg, mine, "IN C1 GROUP" if key in grp_keys else "")
print(f"records {n}, per-move winning-set mismatches CGT(count) vs crosscheck minimax: {mism}; C1-group components checked: {ng}")
