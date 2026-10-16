"""Recount the '22 of 52' taxonomy (no script in engine/ computes it).

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      .venv/bin/python verify/engines/C2-reproduce/taxonomy_c2.py
"""
import collections
import json
import re

ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
rows = {r["id"]: r for r in json.load(open(f"{ROOT}/engine/suite/results.json"))}
ids = [re.search(r'id "([^"]+)"', l).group(1) for l in open(f"{ROOT}/engine/suite/cgt_disagree.epd") if l.strip()]
print("disagree EPD positions:", len(ids))

WINS = {"win", "cursed-win"}
cnt = collections.Counter()
lists = collections.defaultdict(list)
for i in ids:
    r = rows[i]
    km = set(r["king_moves"])
    pw = set(r["rules"]["count"]["pred_win"])
    tw = set(r["tb_win"])
    tbroot = "win" if r["tb_root"] in WINS else r["tb_root"]
    predroot = "win" if pw else "loss"
    extra, missing = tw - pw, pw - tw
    k = []
    if extra and extra <= km and not missing:
        k.append("only-extra-king-wins(any root)")
        if pw:
            k.append("only-extra-king-wins(root agrees)")
    if predroot != tbroot:
        k.append("root-differs")
    if missing:
        k.append("pred-pawn-win-not-win")
    if extra - km:
        k.append("extra-pawn-wins")
    if extra & km:
        k.append("any-extra-king-win")
    # strict: win set differs only by extra king wins AND every pawn move's result is as predicted
    pawn_exact = all((r["tb_moves"][u] in WINS) == (u in pw) and r["tb_moves"][u] in WINS | {"loss", "blessed-loss"}
                     for u in r["tb_moves"] if u not in km)
    if "only-extra-king-wins(root agrees)" in k and pawn_exact:
        k.append("only-extra-king-wins+pawn-moves-exact")
    for x in k:
        cnt[x] += 1
        lists[x].append(i)
for x, n in sorted(cnt.items()):
    print(f"  {x:42s} {n}")

# how many positions where CGT predicts a win but TB is a LOSS are excluded from the disagree EPD?
excl = [r["id"] for r in rows.values() if r["tb_root"] in {"loss", "blessed-loss"} and r["rules"]["count"]["pred_win"]]
print("rows with CGT(count) win but TB loss (not in cgt_disagree.epd):", len(excl), excl)
allbad = [r["id"] for r in rows.values()
          if not (r["tb_root"] in WINS and r["rules"]["count"]["win_set_agree"])
          and not (r["tb_root"] in {"loss", "blessed-loss"} and r["rules"]["count"]["win_set_agree"])]
print("all rows disagreeing with CGT(count) on the win set or root:", len(allbad))
# where do the 22 come from, by group
grp = collections.Counter()
for i in lists["only-extra-king-wins(any root)"]:
    r = rows[i]
    g = ("tame" if "W" not in r["value"]["count"] else "big") + ("-rs" if r["features"]["race_sensitive"] else "") + "-" + r["treb"]
    grp[g] += 1
print("only-extra-king-win positions by group:", dict(grp))
