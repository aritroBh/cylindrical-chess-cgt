"""Print the tables used in REPORT.md (reads values.jsonl and value_index.jsonl).

  cd /Users/aritro/Downloads/Research/Chessendgames/atlas/cylinder && \
  ../../.venv/bin/python tables.py > logs/tables.txt
"""
import json
import re
from collections import Counter, defaultdict
from fractions import Fraction

idx = {}
for line in open("value_index.jsonl"):
    d = json.loads(line)
    idx[d["vid"]] = d


def lab(v):
    d = idx[v]
    return d.get("detail") or d["show"]


def span(pos, n, wrap):
    files = {"abcdefgh".index(t[0]) for t in re.findall(r"[a-h]\d", pos)}
    if not wrap:
        return max(files) - min(files) + 1
    return min(max((f - s) % n for f in files) + 1 for s in files)


best = defaultdict(dict)   # (board, n) -> vid -> (simplicity, rec)
count = defaultdict(Counter)
for line in open("values.jsonl"):
    r = json.loads(line)
    if r["board"] == "flat" and r["n"] < 3:
        continue
    if r["w"] + r["b"] > 5:
        continue
    key = (r["board"], r["n"])
    wrap = r["board"] == "cyl"
    simp = (r["w"] + r["b"], span(r["pos"], r["n"], wrap), r["ncomp"], r["pos"])
    d = best[key]
    if r["vid"] not in d or simp < d[r["vid"]][0]:
        d[r["vid"]] = (simp, r)
    count[key][r["vid"]] += 1

widths = range(3, 9)
print("## T1 per width (w+b <= 5)")
print("| n | cyl positions | flat positions | cyl values | flat values | cyl-only (non-W / W) | flat-only (non-W / W) |")
for n in widths:
    C, F = best[("cyl", n)], best[("flat", n)]
    co = set(C) - set(F)
    fo = set(F) - set(C)
    nw = lambda S: sum(1 for v in S if not idx[v]["big"])
    print(f"| {n} | {sum(count[('cyl', n)].values())} | {sum(count[('flat', n)].values())} | {len(C)} | {len(F)} | "
          f"{nw(co)} / {len(co) - nw(co)} | {nw(fo)} / {len(fo) - nw(fo)} |")

F8 = set(best[("flat", 8)])
allC = set().union(*(set(best[("cyl", n)]) for n in widths))
allF = set().union(*(set(best[("flat", n)]) for n in widths))
print(f"\nflat8 == union of flat widths: {F8 == allF}; cyl8 == flat8: {set(best[('cyl', 8)]) == F8}")
glob = allC - allF
print(f"\n## T3 values on some cylinder (n<=8) but on no flat strip (n<=8), w+b<=5: {len(glob)} "
      f"({sum(1 for v in glob if not idx[v]['big'])} without W)")
print("| value | class | temp | smallest n | simplest witness |")
for v in sorted(glob, key=lambda v: (idx[v]["big"], min(n for n in widths if v in best[("cyl", n)]))):
    if idx[v]["big"]:
        continue
    n0 = min(n for n in widths if v in best[("cyl", n)])
    rec = best[("cyl", n0)][v][1]
    print(f"| {lab(v)} | {idx[v]['cls']} | {idx[v].get('temp')} | {n0} | {rec['pos']} |")
globf = allF - allC
print(f"\nvalues on some flat strip but on no cylinder (n<=8): {len(globf)}")

for n in (3, 4):
    C, F = best[("cyl", n)], best[("flat", n)]
    for name, A, B, wrap in (("cylinder-only", C, F, True), ("flat-only", F, C, False)):
        xs = [v for v in set(A) - set(B) if not idx[v]["big"]]
        xs.sort(key=lambda v: A[v][0])
        print(f"\n## T2 n={n} {name} (non-W): {len(xs)}")
        print("| value | class | temp | pawns | witness | comps |")
        for v in xs:
            rec = A[v][1]
            print(f"| {lab(v)} | {idx[v]['cls']} | {idx[v].get('temp')} | {rec['w']}+{rec['b']} | {rec['pos']} | {rec['ncomp']} |")

print("\n## T4 special classes (union of widths 3..8), simplest witness")
for board in ("cyl", "flat"):
    for cls in ("nimber", "number+nimber", "ups", "tiny", "dyadic", "switch"):
        vs = {}
        for n in widths:
            for v, (simp, rec) in best[(board, n)].items():
                if idx[v]["cls"] == cls and (v not in vs or simp < vs[v][0]):
                    vs[v] = (simp, rec, n)
        print(f"\n### {board} {cls}: {len(vs)}")
        for v, (simp, rec, n) in sorted(vs.items(), key=lambda kv: kv[1][0]):
            print(f"  {lab(v):14s} temp={idx[v].get('temp')} n={n} {rec['pos']} comps={rec['ncomp']} ring={rec['ring']}")

print("\n## T5 max temperature per width (w+b <= 5)")
print("| board n | max temp (no W) | value | witness | max temp (with W) |")
for board in ("cyl", "flat"):
    for n in widths:
        B = best[(board, n)]
        t0 = [(Fraction(idx[v]["temp"]), v) for v in B if idx[v].get("temp") is not None and not idx[v]["big"]]
        t1 = [(Fraction(idx[v]["temp"]), v) for v in B if idx[v].get("temp") is not None and idx[v]["big"]]
        a = max(t0)
        b = max(t1)
        print(f"| {board}{n} | {a[0]} | {idx[a[1]]['show']} | {B[a[1]][1]['pos']} | {b[0]} ({B[b[1]][1]['pos']}) |")
    # rings only
for n in (3, 4, 5):
    B = {v: x for v, x in best[("cyl", n)].items() if x[1]["ring"]}
    t0 = [(Fraction(idx[v]["temp"]), v) for v in B if idx[v].get("temp") is not None and not idx[v]["big"]]
    if t0:
        a = max(t0)
        print(f"| ring C{n} | {a[0]} | {idx[a[1]]['show']} | {B[a[1]][1]['pos']} | |")
