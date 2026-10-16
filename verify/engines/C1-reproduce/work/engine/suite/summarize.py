"""Print the summary tables quoted in engine/suite/README.md (offline).

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      PYTHONPATH=. .venv/bin/python engine/suite/summarize.py
"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_suite as BS  # noqa: E402

rows = json.load(open(BS.RESULTS))


def pct(a, b):
    return f"{a}/{b}" + (f" ({100*a/b:.0f}%)" if b else "")


def tame(r):
    return BS.tame(r["value"]["count"])


def rs(r):
    return r["features"]["race_sensitive"]


groups = {
    "tame (no +-BIG in canonical form), race-insensitive, A-trebuchets":
        [r for r in rows if tame(r) and not rs(r) and r["treb"].startswith("A")],
    "tame, race-insensitive, B-trebuchets": [r for r in rows if tame(r) and not rs(r) and r["treb"].startswith("B")],
    "BIG-valued, race-insensitive": [r for r in rows if not tame(r) and not rs(r)],
    "race-sensitive (CGT win set depends on RACE_RULE), A-trebuchets": [r for r in rows if rs(r) and r["treb"].startswith("A")],
    "race-sensitive, B-trebuchets": [r for r in rows if rs(r) and r["treb"].startswith("B")],
}
for name, grp in groups.items():
    n = len(grp)
    print(f"\n## {name}: {n} positions")
    for rule in ("count", "mover", "opponent"):
        x = [r["rules"][rule] for r in grp]
        print(f"  {rule:9s} root {pct(sum(a['root_agree'] for a in x), n):12s} "
              f"pawn-move win set {pct(sum(a['pawn_set_agree'] for a in x), n):12s} "
              f"full win set {pct(sum(a['win_set_agree'] for a in x), n):12s} "
              f"every move exact {pct(sum(a['all_moves_agree'] for a in x), n)}")
    print(f"  tablebase root: {dict(collections.Counter(r['tb_root'] for r in grp))}")
    print(f"  all king moves lose (as the model assumes): {pct(sum(r['king_moves_all_lose'] for r in grp), n)}")
    km = collections.Counter(v for r in grp for v in r["king_move_results"].values())
    print(f"  king-move results over all king moves: {dict(km)}")

print("\n## tame, race-insensitive positions by value class (count rule)")
by = collections.defaultdict(list)
for r in rows:
    if tame(r) and not rs(r):
        by[r["features"]["class"]].append(r)
for k, grp in sorted(by.items()):
    n = len(grp)
    c = [r["rules"]["count"] for r in grp]
    print(f"  {k:14s} n={n:3d} root {pct(sum(a['root_agree'] for a in c), n):12s} "
          f"pawn set {pct(sum(a['pawn_set_agree'] for a in c), n):12s} "
          f"full win set {pct(sum(a['win_set_agree'] for a in c), n)}")

print("\n## files")
for f in ("cgt_verified.epd", "cgt_disagree.epd"):
    p = os.path.join(HERE, f)
    n = sum(1 for line in open(p) if line.strip())
    print(f"  {f}: {n} positions")
v = [r for r in rows if r["tb_root"] in BS.WINS and r["rules"]["count"]["win_set_agree"]]
print("  verified by value class:", dict(collections.Counter(r["features"]["class"] for r in v)))
print("  verified with a unique solution:", sum(r["features"]["nsol"] == 1 for r in v),
      "; only-slow-winning-move:", sum(r["features"]["slow"] for r in v))
print("  max pawn-play length in verified positions:",
      dict(sorted(collections.Counter(r["features"]["maxlen"] for r in v).items())))
