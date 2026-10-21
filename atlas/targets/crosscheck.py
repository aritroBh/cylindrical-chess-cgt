#!/usr/bin/env python3
"""Second-implementation check of the target values (widths <= 4, flat).

For every target hit in targets_SCOPE.json (both reference settings), the claimed
value T is written as an explicit game DAG of -T, and the A2 worker's independent
C solver atlas/flat8/rerun/nimscan (read-only; it shares no code with cylcgt or
pcgt, and models the WHOLE board rather than a sum of components) decides
G + (-T) = 0 under 15 settings (count / mover / opponent / all races to White /
all races to Black, each with e.p. on + textbook, e.p. off, e.p. on + aware).
Its EQUAL / differ vector is compared with pcgt's (value under the setting ==
the hit's value).

Usage (from the project root):
  PYTHONPATH=. .venv/bin/python atlas/targets/crosscheck.py db
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C  # noqa: E402

NIMSCAN = os.path.join(C.ROOT, "atlas", "flat8", "rerun", "nimscan")
# nimscan --test column order
NAMES = {"count": "count", "mover": "mover", "opponent": "opponent", "white": "allWhite", "black": "allBlack"}


def dag_of(g):
    idx, order = {}, []

    def visit(x):
        if x.id in idx:
            return
        idx[x.id] = len(order)
        order.append(x)
        for y in x.L + x.R:
            visit(y)
    visit(g)
    return [([idx[y.id] for y in x.L], [idx[y.id] for y in x.R]) for x in order]


def col_name(s):
    r, ep, aw = s
    return f"{NAMES[r]}/{'epon' if ep else 'epoff'}{'/aware' if aw else ''}"


def main():
    scope = sys.argv[1]
    with open(os.path.join(HERE, f"targets_{scope}.json")) as fh:
        tj = json.load(fh)
    with C.opener(os.path.join(C.WORK, f"classes_{scope}.json")) as fh:
        classes = json.load(fh)
    show2key = {}
    for v in classes.values():
        show2key.setdefault(v["show"], v["key"])
    tests = []
    for ref, groups in tj["targets"].items():
        for grp in groups:
            for e in grp["positions"]:
                if e["width"] > 4:
                    continue
                T = C.parse_key(show2key[e["value"]])
                tests.append((ref, grp["label"], e, T))
    seen = set()
    uniq = []
    for t in tests:
        k = (t[2]["position"], t[2]["width"], t[2]["value"])
        if k not in seen:
            seen.add(k)
            uniq.append(t)
    path = os.path.join(C.WORK, f"crosscheck_{scope}_input.tsv")
    with open(path, "w") as fh:
        for ref, label, e, T in uniq:
            dag = dag_of(C.cgt.neg(T))
            if len(dag) > 256 or any(len(L) > 16 or len(R) > 16 for L, R in dag):
                continue
            fh.write(f"{e['position']}\t{e['width']}\t" + ";".join(",".join(map(str, L)) + "|" + ",".join(map(str, R))
                                                          for L, R in dag) + "\n")
    out = subprocess.run([NIMSCAN, "--test", path], capture_output=True, text=True, check=True).stdout.strip().split("\n")
    header = out[0].split("\t")[2:]
    rows = {}
    for line in out[1:]:
        p = line.split("\t")
        rows.setdefault((p[0], int(p[1])), []).append(dict(zip(header, (x == "EQUAL" for x in p[2:]))))
    agree = total = 0
    bad = []
    counters = {}
    res = []
    for ref, label, e, T in uniq:
        key = (e["position"], e["width"])
        cvec = rows[key].pop(0)
        mine = {col_name(s): (e["values_by_setting"][C.sname(s)] == e["value"]) for s in C.SETTINGS}
        ok = all(cvec[k] == mine[k] for k in mine)
        total += 1
        agree += ok
        if not ok:
            bad.append((e["position"], e["value"], {k: (cvec[k], mine[k]) for k in mine if cvec[k] != mine[k]}))
        res.append({"position": e["position"], "width": e["width"], "value": e["value"], "label": label,
                    "nimscan_equal": cvec, "pcgt_equal": mine, "agree": ok})
    with open(os.path.join(HERE, f"crosscheck_{scope}.json"), "w") as fh:
        json.dump({"tests": res, "agree": agree, "total": total, "settings_compared": 15}, fh, indent=1,
                  ensure_ascii=False)
    print(f"{scope}: {total} (position, value) pairs x 15 settings; full-vector agreement nimscan vs pcgt: "
          f"{agree}/{total}")
    for b in bad[:10]:
        print("  DISAGREE", b)


if __name__ == "__main__":
    main()
