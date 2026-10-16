"""Independent recomputation of claim C1 (theory-lens verifier).

Does NOT use build_suite.compare / summarize / candidates.json / cylcgt.
 * component outcome: crosscheck/minimax.py (Codex's independent pawn minimax, 'count'-like race rule)
 * tablebase: raw Lichess JSON from the verifier's copy of engine/suite/tbcache (offline)
 * group membership (tame, race-insensitive, A-trebuchet) is taken from results.json ids only.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/engines/C1-theory/independent94.py
"""
import collections, glob, hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
from crosscheck import minimax as M

rows = json.load(open(os.path.join(HERE, "suite_copy", "results.json")))
def tame(v): return "W" not in v
grp = [r for r in rows if tame(r["value"]["count"]) and not r["features"]["race_sensitive"] and r["treb"].startswith("A")]

# raw cache index: normalised fen -> data
cache = {}
for p in glob.glob(os.path.join(HERE, "suite_copy", "tbcache", "*", "*.json")):
    rec = json.load(open(p))
    k = rec.get("fen") or rec.get("key")
    cache[p] = rec
byfen = {}
for rec in cache.values():
    for k in ("fen", "key", "fen_key"):
        if k in rec:
            byfen[" ".join(rec[k].split()[:4])] = rec
            break

B = M.Board(4, 8, False, True)
FILES = "abcdefgh"

def parse(fen):
    board, stm, _, ep = fen.split()[:4]
    w, b = set(), set()
    for i, row in enumerate(board.split("/")):
        rank = 8 - i; f = 0
        for ch in row:
            if ch.isdigit(): f += int(ch); continue
            if f < 4 and ch == "P": w.add((f, rank))
            if f < 4 and ch == "p": b.add((f, rank))
            f += 1
    side = "W" if stm == "w" else "B"
    epx = None
    if ep != "-":
        t = (FILES.index(ep[0]), int(ep[1]))
        epx = (t, (t[0], t[1] - 1), "W") if side == "W" else (t, (t[0], t[1] + 1), "B")
    return frozenset(w), frozenset(b), epx, side

def apply(w, b, epx, side, uci):
    fr = (FILES.index(uci[0]), int(uci[1])); to = (FILES.index(uci[2]), int(uci[3]))
    mine, theirs = (set(w), set(b)) if side == "W" else (set(b), set(w))
    assert fr in mine, uci
    mine.discard(fr); mine.add(to)
    theirs.discard(to)
    if epx and to == epx[0] and fr[0] != to[0]:
        theirs.discard(epx[1])
    newep = None
    if abs(to[1] - fr[1]) == 2:
        mid = (fr[0], (fr[1] + to[1]) // 2)
        newep = (mid, to, "B" if side == "W" else "W")
    W, Bk = (mine, theirs) if side == "W" else (theirs, mine)
    return M.Position(frozenset(W), frozenset(Bk), newep)

def mover_wins(child, mover):
    r = M._winner_after_move(B, child, mover)
    if r is None:
        r = M.winner(B, child, "B" if mover == "W" else "W")
    return r == mover

MOVER = {"loss": "win", "win": "loss", "draw": "draw", "cursed-win": "loss*", "blessed-loss": "win*"}
stats = collections.Counter(); pawncat = collections.Counter()
for r in grp:
    fen = r["fen"]; key = " ".join(fen.split()[:4])
    rec = byfen.get(key)
    if rec is None:
        stats["missing_tb"] += 1; continue
    d = rec["data"]
    w, b, epx, side = parse(fen)
    pos = M.Position(w, b, epx)
    nchild = len(M.legal_moves(B, pos, side))
    tbm = {m["uci"]: MOVER[m["category"]] for m in d["moves"]}
    pawn = {u for u in tbm if (FILES.index(u[0]), int(u[1])) in (w if side == "W" else b)}
    assert len(pawn) == nchild, (fen, pawn, nchild)
    predw = {u for u in pawn if mover_wins(apply(w, b, epx, side, u), side)}
    tbw = {u for u, c in tbm.items() if c == "win"}
    root_pred = "win" if predw else "loss"
    stats["n"] += 1
    stats["root_agree"] += root_pred == d["category"]
    stats["pawnset_agree"] += predw == (tbw & pawn)
    stats["fullset_agree"] += predw == tbw
    stats["pawn_moves_exact"] += all((u in predw) == (tbm[u] == "win") and tbm[u] in ("win", "loss") for u in pawn)
    stats["tb_root_" + d["category"]] += 1
    for u in pawn:
        pawncat[("win" if u in predw else "loss", tbm[u])] += 1
print(dict(stats))
print("pawn moves (minimax prediction, TB):", dict(pawncat))
