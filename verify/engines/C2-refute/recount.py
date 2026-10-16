"""Independent recount of claim C2 (king moves in the trebuchet suite).

Does NOT import any worker code (engine/*). Reads the worker's raw Lichess
cache files (engine/suite/tbcache/**/*.json) read-only, classifies each cached
FEN structurally (trebuchet layout, queenside component), recomputes the CGT
group membership with the project's cylcgt (read-only), and counts the
tablebase result of every king move from the raw Lichess categories.

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python verify/engines/C2-refute/recount.py
"""
import collections
import glob
import json
import os
import sys

from cylcgt import cgt, pawns

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CACHE = os.path.join(ROOT, "engine", "suite", "tbcache")
FILES = "abcdefgh"
B4 = pawns.Board(4, 8, False, True)
ZERO = cgt.integer(0)
# category is for the side to move AFTER the move -> result for the mover
MOVER = {"loss": "win", "blessed-loss": "cursed-win", "draw": "draw", "cursed-win": "blessed-loss",
         "win": "loss"}


def parse(fen):
    board, stm = fen.split()[:2]
    pcs = {}
    for i, row in enumerate(board.split("/")):
        r = 8 - i
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                pcs[(f, r)] = ch
                f += 1
    return pcs, stm


def classify(pcs):
    """Return (layout, rank) if pcs = trebuchet + a-d component with e empty, else None."""
    wk = [s for s, p in pcs.items() if p == "K"][0]
    bk = [s for s, p in pcs.items() if p == "k"][0]
    gw = [s for s, p in pcs.items() if p == "P" and s[0] == 6]
    gb = [s for s, p in pcs.items() if p == "p" and s[0] == 6]
    others = [s for s, p in pcs.items() if p in "Pp" and s[0] != 6]
    if len(gw) != 1 or len(gb) != 1 or any(s[0] > 3 for s in others):
        return None
    r = gw[0][1]
    if gb[0][1] != r + 1:
        return None
    if wk == (5, r + 1) and bk == (7, r):
        return ("A", r)
    if wk == (7, r + 1) and bk == (5, r):
        return ("B", r)
    return None


def has_big(g, seen=None):
    seen = set() if seen is None else seen
    if g.id in seen:
        return False
    seen.add(g.id)
    if g.num is not None and abs(g.num) >= pawns.BIG // 2:
        return True
    return any(has_big(x, seen) for x in g.L + g.R)


def child_value(pos, mover, rule):
    if pawns.passed(B4, pos, "W") and pawns.passed(B4, pos, "B"):
        other = "B" if mover == "W" else "W"
        if rule == "mover":
            w = mover
        elif rule == "opponent":
            w = other
        else:
            w = other if pawns.promote_distance(B4, pos, other) <= pawns.promote_distance(B4, pos, mover) else mover
        return cgt.integer(pawns.BIG if w == "W" else -pawns.BIG)
    return pawns.value(B4, pos)


def win_set(pos, stm, rule):
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()
    out = []
    for ch in pawns.moves(B4, pos, stm):
        v = child_value(ch, stm, rule)
        out.append(cgt.le(ZERO, v) if stm == "W" else cgt.le(v, ZERO))
    return tuple(out)


def main():
    recs = []
    for p in glob.glob(os.path.join(CACHE, "*", "*.json")):
        recs.append(json.load(open(p)))
    print("cached records:", len(recs))
    rows = []
    for rec in recs:
        pcs, stm = parse(rec["fen"])
        lay = classify(pcs)
        if lay is None:
            continue
        assert rec["status"] == 200
        d = rec["data"]
        w = frozenset(s for s, p in pcs.items() if p == "P" and s[0] <= 3)
        b = frozenset(s for s, p in pcs.items() if p == "p" and s[0] <= 3)
        pos = pawns.Pos(w, b, None)
        pawns.RACE_RULE = "count"
        pawns._value.cache_clear()
        v = pawns.value(B4, pos)
        tame = not has_big(v)
        rs = len({win_set(pos, stm.upper(), r) for r in ("count", "mover", "opponent")}) > 1
        ksq = [s for s, p in pcs.items() if p == ("K" if stm == "w" else "k")][0]
        kname = FILES[ksq[0]] + str(ksq[1])
        km = {m["uci"]: MOVER.get(m["category"], "?" + str(m["category"])) for m in d["moves"]
              if m["uci"][:2] == kname}
        pm = {m["uci"]: MOVER.get(m["category"], "?" + str(m["category"])) for m in d["moves"]
              if m["uci"][:2] != kname}
        # pawn moves in the chess position must be the component's pawn moves
        assert len(pm) == len(pawns.moves(B4, pos, "W" if stm == "w" else "B")) or any(
            m["uci"][3] in "18" for m in d["moves"]), rec["fen"]
        pawns.RACE_RULE = "count"
        pawns._value.cache_clear()
        rows.append(dict(fen=rec["fen"], lay=lay, stm=stm, tame=tame, rs=rs, value=cgt.show(v),
                         root=d["category"], km=km, pm=pm))
    print("suite positions found structurally:", len(rows))
    cats = collections.Counter(m["category"] for rec in recs if rec.get("data") for m in rec["data"]["moves"])
    print("all move categories in cache:", dict(cats))
    groups = {
        "tame, race-insensitive, A": lambda r: r["tame"] and not r["rs"] and r["lay"][0] == "A",
        "tame, race-insensitive, B": lambda r: r["tame"] and not r["rs"] and r["lay"][0] == "B",
        "tame, race-insensitive, B, White to move": lambda r: r["tame"] and not r["rs"] and r["lay"][0] == "B" and r["stm"] == "w",
        "tame, race-insensitive, B, Black to move": lambda r: r["tame"] and not r["rs"] and r["lay"][0] == "B" and r["stm"] == "b",
        "BIG, race-insensitive": lambda r: not r["tame"] and not r["rs"],
        "race-sensitive A": lambda r: r["rs"] and r["lay"][0] == "A",
        "race-sensitive B": lambda r: r["rs"] and r["lay"][0] == "B",
        "ALL": lambda r: True,
    }
    out = {}
    for name, f in groups.items():
        g = [r for r in rows if f(r)]
        kc = collections.Counter(x for r in g for x in r["km"].values())
        npos_nonlose = sum(any(x != "loss" for x in r["km"].values()) for r in g)
        roots = collections.Counter(r["root"] for r in g)
        # king-move results split by tablebase root
        by_root = collections.defaultdict(collections.Counter)
        for r in g:
            for x in r["km"].values():
                by_root[r["root"]][x] += 1
        print(f"\n{name}: {len(g)} positions; roots {dict(roots)}")
        print(f"   king moves {sum(kc.values())}: {dict(kc)}; positions with a non-losing king move: {npos_nonlose}")
        print(f"   king-move results by TB root: { {k: dict(v) for k, v in by_root.items()} }")
        out[name] = dict(n=len(g), kc=dict(kc), nonlose_pos=npos_nonlose)
    # list A-group positions with non-losing king moves
    print("\nA-group (tame, race-insensitive) positions with non-losing king moves:")
    for r in rows:
        if r["tame"] and not r["rs"] and r["lay"][0] == "A" and any(x != "loss" for x in r["km"].values()):
            print("  ", r["lay"], r["fen"], r["value"], "root", r["root"],
                  {k: v for k, v in r["km"].items() if v != "loss"})
    print("\nB-group (tame, race-insensitive) positions with non-losing king moves:")
    for r in rows:
        if r["tame"] and not r["rs"] and r["lay"][0] == "B" and any(x != "loss" for x in r["km"].values()):
            print("  ", r["lay"], r["stm"], r["fen"], r["value"], "root", r["root"],
                  {k: v for k, v in r["km"].items() if v != "loss"})
    json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "recount_rows.json"), "w"),
              indent=1, default=str)


if __name__ == "__main__":
    main()
