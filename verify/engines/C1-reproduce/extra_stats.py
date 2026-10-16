"""Extra breakdowns of the C1 group. Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/engines/C1-reproduce/extra_stats.py"""
import collections, json, sys
sys.path.insert(0, "engine/suite")
import build_suite as BS
rows = json.load(open("engine/suite/results.json"))
sel = {c["id"]: c for c in BS.all_selected()}
grp = [r for r in rows if BS.tame(r["value"]["count"]) and not r["features"]["race_sensitive"] and r["treb"].startswith("A")]
mult = collections.Counter(r["component"] for r in grp)
print("components appearing >1 time:", {k: v for k, v in mult.items() if v > 1})
win = [r for r in grp if r["tb_root"] == "win"]
pw = lambda r: set(r["rules"]["count"]["pred_win"])
pawn = lambda r: set(sel[r["id"]]["pawn_moves"])
print("TB-win positions:", len(win), "; with CGT pawn set == TB pawn set:", sum(pw(r) == set(r["tb_win"]) & pawn(r) for r in win))
print("  of which some pawn move is NOT winning (discriminating):", sum(0 < len(pw(r)) < len(pawn(r)) for r in win),
      "; all pawn moves win:", sum(len(pw(r)) == len(pawn(r)) for r in win))
print("empty-vs-empty pawn-set comparisons (TB loss or draw):", sum(not pw(r) and not (set(r["tb_win"]) & pawn(r)) for r in grp))
exact_pawn = sum(all((r["tb_moves"][u] == "win") == (u in pw(r)) and r["tb_moves"][u] in ("win", "loss") for u in pawn(r)) for r in grp)
print("positions where every PAWN move's TB result (win/loss, draw = mismatch) equals CGT:", exact_pawn, "/", len(grp))
print("pawn moves total:", sum(len(pawn(r)) for r in grp), "; king moves total:", sum(len(r["king_moves"]) for r in grp))
print("tiers x TB root:", collections.Counter((r["tier"], r["tb_root"]) for r in grp))
print("new_race_nodes>0 under count in group:")
cands = {(c["pos"], c["stm"]): c for c in json.load(open("engine/suite/candidates.json"))}
print(" ", sum(cands[(r["component"], r["stm"])]["rules"]["count"]["new_race_nodes"] > 0 for r in grp), "(order-dependent counter; lower bound)")
