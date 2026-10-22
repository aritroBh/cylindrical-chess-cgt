#!/usr/bin/env python3
"""Aggregate gapped/*.out (cmp_gapped_nim.py outputs): per (width, pawns) and in total."""
import re, glob, collections
tot = collections.defaultdict(lambda: collections.Counter())
for f in sorted(glob.glob("gapped/*.out")):
    m = re.match(r"gapped/w(\d+)p(\d+)_(\d+)_(\d+)\.out", f); w, p = int(m.group(1)), int(m.group(2))
    t = tot[(w, p)]
    txt = open(f).read()
    if "gapped rows=" not in txt: t["INCOMPLETE_FILES"] += 1; continue
    t["rows"] += int(re.search(r"gapped rows=(\d+)", txt).group(1))
    for sc, sm, n in re.findall(r"scanner=\s*(-?\d+) sum_model=\s*(-?\d+)\s+rows=(\d+)", txt): t[(int(sc), int(sm))] += int(n)
    mm = re.search(r"mismatching rows: (\d+); explained by \+BIG/-BIG in different parts: (\d+); NOT explained: (\d+)", txt)
    t["mismatch"] += int(mm.group(1)); t["explained"] += int(mm.group(2)); t["unexplained"] += int(mm.group(3))
print(" w p      gapped_rows  scanner*2 | sum-model*2 | scanner(0,*1) agree | mismatches (explained/unexplained) | files incomplete")
for (w, p), t in sorted(tot.items()):
    sc2 = sum(v for k, v in t.items() if isinstance(k, tuple) and k[0] == 2)
    sm2 = sum(v for k, v in t.items() if isinstance(k, tuple) and k[1] == 2)
    agree01 = t[(0, 0)] + t[(1, 1)]; sc01 = sum(v for k, v in t.items() if isinstance(k, tuple) and k[0] in (0, 1))
    print(f"{w:2d} {p:2d} {t['rows']:16d} {sc2:9d} | {sm2:11d} | {agree01:9d}/{sc01:<9d} | {t['mismatch']:8d} ({t['explained']}/{t['unexplained']}) | {t['INCOMPLETE_FILES']}")
T = collections.Counter()
for t in tot.values(): T.update(t)
print("TOTAL gapped rows", T["rows"], " unexplained mismatches", T["unexplained"], " sum-model *2 rows", sum(v for k, v in T.items() if isinstance(k, tuple) and k[1] == 2),
      " scanner *2 rows", sum(v for k, v in T.items() if isinstance(k, tuple) and k[0] == 2))
