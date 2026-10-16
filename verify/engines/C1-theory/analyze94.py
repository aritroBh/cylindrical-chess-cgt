"""Theory-lens re-analysis of claim C1 (offline; reads the verifier's copy of results.json).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/engines/C1-theory/analyze94.py
"""
import collections, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "suite_copy"))
import build_suite as BS
rows = json.load(open(os.path.join(HERE, "suite_copy", "results.json")))
WINS, LOSSES = BS.WINS, BS.LOSSES
g = [r for r in rows if BS.tame(r["value"]["count"]) and not r["features"]["race_sensitive"] and r["treb"].startswith("A")]
print("n =", len(g))
print("tiers:", collections.Counter(r["tier"] for r in g))
print("treb:", collections.Counter(r["treb"] for r in g))
print("stm:", collections.Counter(r["stm"] for r in g))
print("distinct components (comp,stm):", len({(r["component"], r["stm"]) for r in g}))
print("tb root:", collections.Counter(r["tb_root"] for r in g))
# per-position informativeness of the pawn-set test
c = r = None
nontriv = 0; vac = 0; npawnmoves = 0; pawn_mismatch_draw = 0
pawn_cat = collections.Counter()
for r in g:
    pawn = set(r["san"]) - set(r["king_moves"])
    cnt = r["rules"]["count"]
    pw = set(cnt["pred_win"])
    tbw = set(r["tb_win"]) & pawn
    npawnmoves += len(pawn)
    if not pw and not tbw:
        vac += 1
    if pw and (pawn - pw):
        nontriv += 1
    for u in pawn:
        pred = "win" if u in pw else "loss"
        pawn_cat[(pred, r["tb_moves"][u])] += 1
print("positions where the pawn-set test is vacuous (both sets empty):", vac)
print("positions where CGT says some pawn moves win and some lose:", nontriv)
print("total pawn moves tested:", npawnmoves)
print("pawn moves (CGT prediction, TB result for mover):", dict(pawn_cat))
km = collections.Counter()
for r in g:
    for u in r["king_moves"]:
        km[r["tb_moves"][u]] += 1
print("king moves (pred loss) TB results:", dict(km))
print("\nroot disagreements:")
for r in g:
    cnt = r["rules"]["count"]
    if not cnt["root_agree"]:
        print(" ", r["id"], r["tier"], r["treb"], r["component"], r["value"]["count"], r["tb_root"], r["fen"])
        print("    moves:", {r["san"][u]: r["tb_moves"][u] for u in r["san"]})
print("\nfull-win-set disagreements:")
for r in g:
    cnt = r["rules"]["count"]
    if not cnt["win_set_agree"]:
        print(" ", r["id"], r["tier"], r["treb"], r["component"], r["value"]["count"], r["tb_root"],
              "pred", [r["san"][u] for u in cnt["pred_win"]], "tb", [r["san"][u] for u in r["tb_win"]])
print("\nvalues in group:", collections.Counter(r["value"]["count"] for r in g).most_common())
print("classes:", collections.Counter(r["features"]["class"] for r in g))
# pooled A+B
gab = [r for r in rows if BS.tame(r["value"]["count"]) and not r["features"]["race_sensitive"]]
for k in ("root_agree", "pawn_set_agree", "win_set_agree", "all_moves_agree"):
    print("pooled A+B tame race-insens", k, sum(r["rules"]["count"][k] for r in gab), "/", len(gab))
# TB-won subset of the 94
w = [r for r in g if r["tb_root"] in WINS]
print("TB-won subset:", len(w), "pawn-set agree", sum(r["rules"]["count"]["pawn_set_agree"] for r in w),
      "unique-solution", sum(len(r["tb_win"]) == 1 for r in w))
