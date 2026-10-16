"""Fresh (no stored predictions) recomputation of the "72 race-sensitive A4 positions"
root-outcome agreement in claim C3.

CGT side: cylcgt.pawns directly (cache cleared before each rule), component on the
4-file flat board with e.p. on; king moves predicted to lose, so the predicted root
result is "White to move wins the component" (G not <= 0) else loss.
TB side: cached Lichess replies read directly from disk (no network).
Race-sensitivity is recomputed: winning pawn-move sets differ between rules.

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python verify/engines/C3-reproduce/fresh_root72.py
"""
import collections
import glob
import json
import os

from cylcgt import cgt, pawns

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
B4 = pawns.Board(4, 8, False, True)
RULES = ("count", "opponent", "mover")

sel = json.load(open(os.path.join(ROOT, "engine/suite/selection.json")))
sel += json.load(open(os.path.join(ROOT, "engine/suite/selection_ext.json")))
cache = {}
for d in ("engine/suite/tbcache", "realchess/cache"):
    for p in glob.glob(os.path.join(ROOT, d, "*", "*.json")):
        rec = json.load(open(p))
        cache[" ".join(rec["fen"].split()[:4])] = rec


def comp_from_fen(fen):
    board, stm, _c, ep = fen.split()[:4]
    w, b = set(), set()
    for i, row in enumerate(board.split("/")):
        r, f = 8 - i, 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
                continue
            if f <= 3 and ch == "P":
                w.add((f, r))
            if f <= 3 and ch == "p":
                b.add((f, r))
            f += 1
    epx = None
    if ep != "-":
        t = (ord(ep[0]) - 97, int(ep[1]))
        epx = (t, (t[0], t[1] - 1), "W") if stm == "w" else (t, (t[0], t[1] + 1), "B")
    return pawns.Pos(frozenset(w), frozenset(b), epx), stm


def winset(pos, side):
    out = set()
    for ch in pawns.moves(B4, pos, side):
        v = pawns._child(B4, ch, side)
        if (cgt.le(cgt.ZERO, v) if side == "W" else cgt.le(v, cgt.ZERO)):
            out.add(ch)
    return frozenset(out)


res = {}
for rule in RULES:
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()
    for c in sel:
        pos, stm = comp_from_fen(c["fen"])
        side = "W" if stm == "w" else "B"
        v = pawns.value(B4, pos)
        stm_wins = (not cgt.le(v, cgt.ZERO)) if side == "W" else (not cgt.le(cgt.ZERO, v))
        ws = winset(pos, side)
        assert stm_wins == bool(ws)
        res.setdefault(c["id"], {})[rule] = (stm_wins, ws, cgt.show(v))
pawns.RACE_RULE = "count"
pawns._value.cache_clear()

stored = {r["id"]: r for r in json.load(open(os.path.join(ROOT, "engine/suite/results.json")))}
groups = collections.defaultdict(list)
mismatch_stored = 0
for c in sel:
    r = res[c["id"]]
    rs = len({r[ru][1] for ru in RULES}) > 1
    tbroot = cache[" ".join(c["fen"].split()[:4])]["data"]["category"]
    tbres = "win" if tbroot in ("win", "cursed-win") else "loss" if tbroot in ("loss", "blessed-loss") else tbroot
    agree = {ru: ("win" if r[ru][0] else "loss") == tbres for ru in RULES}
    for ru in RULES:
        if agree[ru] != stored[c["id"]]["rules"][ru]["root_agree"] or r[ru][2] != c["value"][ru]:
            mismatch_stored += 1
    if rs:
        groups[(c["treb"][0], c["treb"], c["tier"])].append((c["id"], agree, tbres))

print("mismatches vs stored results.json/selection values:", mismatch_stored)
for k in sorted(groups):
    g = groups[k]
    print(k, len(g), {ru: sum(a[ru] for _, a, _ in g) for ru in RULES},
          "tb roots:", dict(collections.Counter(t for *_, t in g)))
a = [x for k, g in groups.items() if k[0] == "A" for x in g]
print("ALL race-sensitive A-trebuchet:", len(a), {ru: sum(x[1][ru] for x in a) for ru in RULES})
