"""C1 adversarial checks (offline). Reads the worker's results/selection/cache; writes nothing outside stdout.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/engines/C1-reproduce/check_c1.py
"""
import collections, json, os, sys
sys.path.insert(0, "engine/suite")
import build_suite as BS
import tb
from realchess import movegen as MG

rows = json.load(open("engine/suite/results.json"))
sel = {c["id"]: c for c in BS.all_selected()}
grp = [r for r in rows if BS.tame(r["value"]["count"]) and not r["features"]["race_sensitive"] and r["treb"].startswith("A")]
print("group size", len(grp))
print("stm:", collections.Counter(r["stm"] for r in grp))
print("treb:", collections.Counter(r["treb"] for r in grp))
print("tier:", collections.Counter(r["tier"] for r in grp))
print("distinct components:", len({(r["component"], r["stm"]) for r in grp}))
print("tb root:", collections.Counter(r["tb_root"] for r in grp))
print("values identical across rules:", all(len(set(r["value"].values())) == 1 for r in grp))
print("unresolved moves:", sum(len(r["tb_unresolved"]) for r in grp))
print("TB move categories:", collections.Counter(v for r in grp for v in r["tb_moves"].values()))

# 1. Lichess perspective consistency over every cached response used
bad = 0
for r in rows:
    rec = tb.lookup(r["fen"], allow_network=False)
    d = rec["data"]
    assert rec["fen"] == MG.normal_fen(r["fen"]), r["id"]
    cats = [m["category"] for m in d["moves"]]
    root = d["category"]
    exp = "win" if any(c in ("loss", "blessed-loss") for c in cats) else ("draw" if any(c == "draw" for c in cats) else "loss")
    rootn = {"cursed-win": "win", "blessed-loss": "loss"}.get(root, root)
    if exp != rootn:
        bad += 1; print("perspective inconsistency", r["id"], root, cats)
    # independent recount from raw data
    tbw = sorted(m["uci"] for m in d["moves"] if m["category"] in ("loss", "blessed-loss"))
    assert tbw == r["tb_win"], r["id"]
print("root/move perspective inconsistencies over", len(rows), "responses:", bad)

# 2. independent recount of the four C1 numbers from raw TB data + candidates (not results.json flags)
cands = {(c["pos"], c["stm"]): c for c in json.load(open("engine/suite/candidates.json"))}
n_root = n_pawn = n_full = n_exact = 0
miss_root, miss_full = [], []
nontriv_pawn = 0
for r in grp:
    c = sel[r["id"]]
    rec = tb.lookup(r["fen"], allow_network=False)["data"]
    cat = {m["uci"]: m["category"] for m in rec["moves"]}
    cand = cands[(r["component"], r["stm"])]
    pawn = {m[0] for m in cand["rules"]["count"]["moves"]}
    predw = {m[0] for m in cand["rules"]["count"]["moves"] if m[4]}
    tbw = {u for u, k in cat.items() if k in ("loss", "blessed-loss")}
    root = rec["category"]
    pr = "win" if predw else "loss"
    n_root += (pr == root)
    if pr != root: miss_root.append((r["id"], r["fen"], root, pr, {u: cat[u] for u in pawn}))
    n_pawn += (predw == (tbw & pawn))
    if predw: nontriv_pawn += (predw == (tbw & pawn))
    n_full += (predw == tbw)
    if predw != tbw: miss_full.append((r["id"], r["fen"], sorted(predw), sorted(tbw)))
print(f"recount: root {n_root}/{len(grp)}, pawn set {n_pawn}/{len(grp)} (non-empty predicted sets agreeing: {nontriv_pawn}), full set {n_full}/{len(grp)}")
for m in miss_root: print(" root miss:", m)
for m in miss_full: print(" full-set miss:", m)
# draws among pawn moves that CGT calls losses
dr = [(r["id"], u, r["tb_moves"][u]) for r in grp for u in sel[r["id"]]["pawn_moves"] if r["tb_moves"][u] == "draw"]
print("pawn moves that TB rates draw (CGT: loss):", len(dr), dr[:20])
lw = [(r["id"], u) for r in grp for u in sel[r["id"]]["pawn_moves"] if r["tb_moves"][u] in ("loss","blessed-loss") and u in r["rules"]["count"]["pred_win"]]
print("CGT-winning pawn moves that TB rates loss:", lw)
print("values that differ across rules:")
for r in grp:
    if len(set(r["value"].values())) > 1:
        print(" ", r["id"], r["treb"], r["component"], r["value"])
print("root-miss king-move results:")
for i in ("cgt052", "cgt055"):
    r = next(x for x in grp if x["id"] == i)
    print(" ", i, r["component"], r["value"]["count"], r["king_move_results"], {u: r["tb_moves"][u] for u in sel[i]["pawn_moves"]})
