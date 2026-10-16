"""Extra adversarial checks on the C1 group (uses indep.py; the BIG test imports cylcgt, non-decisive).
    cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/engines/C1-refute/extra.py
"""
import collections, sys
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/verify/engines/C1-refute")
import indep
out = indep.main()
def rs(o):
    s = {r: frozenset(u for u, w in o["preds"][r].items() if w) for r in o["preds"]}
    return len(set(s.values())) > 1
grp = [o for o in out if "W" not in o["value"] and not rs(o) and o["treb"].startswith("A")]
rows = {r["id"]: r for r in __import__("json").load(open(indep.ROOT + "/engine/suite/results.json"))}
comps = collections.Counter(rows[o["id"]]["component"] for o in grp)
print("positions", len(grp), "distinct components", len(comps), "repeated:", {k: v for k, v in comps.items() if v > 1})
# root category consistent with the move categories?
bad = []
for o in out:
    best = "win" if any(c == "win" for c in o["tbm"].values()) else "draw" if any(c == "draw" for c in o["tbm"].values()) else "loss"
    if best != o["tb_root"]:
        bad.append(o["id"])
print("root/move category inconsistencies (all 275):", bad)
# pawn moves the model calls losses that the tablebase calls draws
for o in grp:
    pd = [u for u in o["pawn_moves"] if not o["preds"]["count"][u] and o["tbm"][u] == "draw"]
    if pd:
        print("  pawn move predicted LOSS, TB DRAW:", o["id"], o["fen"], pd, "tb_root", o["tb_root"], "value", o["value"])
# values present in group
print("value strings:", dict(collections.Counter(o["value"] for o in grp)))
# tameness: canonical form must not change when BIG changes (uses cylcgt, NOT decisive)
from cylcgt import pawns, cgt
pawns.RACE_RULE = "count"
cgt.BIG_DISPLAY = None
def val(comp, big):
    pawns.BIG = big
    pawns._value.cache_clear()
    return cgt.show(pawns.value(pawns.Board(4, 8, False, True), pawns.Pos.parse(comp.split(" (ep")[0])))
changed = []
for c in comps:
    if "(ep" in c:
        continue
    a, b = val(c, 256), val(c, 1000)
    if a != b:
        changed.append((c, a, b))
print("components whose canonical form depends on BIG (should be none if tame):", changed)
print("ep-variant components in group:", [c for c in comps if "(ep" in c])
