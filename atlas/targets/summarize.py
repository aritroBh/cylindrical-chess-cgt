#!/usr/bin/env python3
"""Compact target tables across scopes (flat board), from matrix_SCOPE.json.

For each target family: number of positions (records, up to mirror image) under the
adopted setting (count rule, e.p. on, e.p.-aware), under the textbook setting
(count, e.p. on, textbook), under at least one of the 15 settings, and identical
under all 15; smallest witness of each.

Usage (from the project root):
  PYTHONPATH=. .venv/bin/python atlas/targets/summarize.py   -> summary_targets.json / .out
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C  # noqa: E402

SCOPES = [("db", "w1-4, <=6 pawns"), ("w5", "w5 connected, 5-6 pawns"), ("n7", "w2-4, 7 pawns"),
          ("w5n7", "w5 connected, 7 pawns")]
A, T = "count/epon-aware", "count/epon-textbook"


SHIFT = re.compile(r"^-?\d+(/\d+)? \+ ")


def family(label):
    """Map a matrix label 'kind | value' to a report family."""
    kind, val = label.split(" | ", 1)
    shift = " (number-shifted)" if SHIFT.match(val) else ""
    core = SHIFT.sub("", val)
    if kind.startswith("*"):
        return f"nimber {val}"
    if kind.startswith("dyadic"):
        x = abs(Fraction(val))
        return f"dyadic, denominator {x.denominator}" + (" (|x| = 1/" + str(x.denominator) + ")" if x.numerator == 1 else " (other numerators)")
    if kind.startswith("up-second"):
        if "↑³" in core or "↓³" in core:
            return "up-third family" + shift
        return f"up-second: {core}" + shift
    m = re.match(r"^(tiny|miny)\((.*)\)$", core)
    sub = m.group(2) if m else core
    if kind.startswith("fractional"):
        return f"tiny/miny(x), x = {sub}" + shift
    if kind.startswith("tiny, non-number"):
        if sub == "{1 | 1*}":
            return "tiny/miny(1↑)" + shift
        if sub == "{1* | 1}":
            return "tiny/miny(1↓)" + shift
        if sub == "1*":
            return "tiny/miny(1*)" + shift
        return "tiny/miny(G), G another non-number" + shift
    return kind


def main():
    fam = defaultdict(lambda: {"A": set(), "T": set(), "any": set(), "robust": set()})
    for scope, _ in SCOPES:
        path = os.path.join(HERE, f"matrix_{scope}.json")
        if not os.path.exists(path):
            continue
        with open(path) as fh:
            m = json.load(fh)
        for label, by in m["by_label"].items():
            f = fam[family(label)]
            for s, ps in by.items():
                for p in ps:
                    f["any"].add((scope, p, label))
                    if s == A:
                        f["A"].add((scope, p, label))
                    if s == T:
                        f["T"].add((scope, p, label))
        for label, ps in m["robust_all15"].items():
            for p in ps:
                fam[family(label)]["robust"].add((scope, p, label))

    def smallest(xs):
        if not xs:
            return None
        sc, p, lab = min(xs, key=lambda t: (C.npawns(t[1]), len({q[0] for q in C.parse_pos(t[1])[0] + C.parse_pos(t[1])[1]}), t[1]))
        return f"{p} [{lab.split(' | ', 1)[1]}] ({sc})"

    def minw(xs):
        ws = [len({q[0] for q in C.parse_pos(p)[0] + C.parse_pos(p)[1]}) for _, p, _ in xs]
        return min(ws) if ws else None

    out, lines = {}, []
    lines.append(f"{'family':58s} {'adopted':>8s} {'textbk':>8s} {'any':>8s} {'all15':>8s} minw(A/T/any/15)  smallest (adopted / all15 / any)")
    for k in sorted(fam):
        f = fam[k]
        out[k] = {"adopted_count_epon_aware": len(f["A"]), "textbook_count_epon": len(f["T"]),
                  "any_of_15": len(f["any"]), "identical_all_15": len(f["robust"]),
                  "smallest_adopted": smallest(f["A"]), "smallest_all15": smallest(f["robust"]),
                  "smallest_any": smallest(f["any"]),
                  "min_width_adopted": minw(f["A"]), "min_width_textbook": minw(f["T"]),
                  "min_width_any": minw(f["any"]), "min_width_all15": minw(f["robust"]),
                  "width5_adopted_positions": sorted({p for sc, p, _ in f["A"] if sc in ("w5", "w5n7")}),
                  "width5_textbook_positions": sorted({p for sc, p, _ in f["T"] if sc in ("w5", "w5n7")})}
        mw = "/".join(str(out[k][x]) if out[k][x] else "-" for x in ("min_width_adopted", "min_width_textbook", "min_width_any", "min_width_all15"))
        lines.append(f"{k[:58]:58s} {len(f['A']):8d} {len(f['T']):8d} {len(f['any']):8d} {len(f['robust']):8d} {mw:>16s}  "
                     f"{out[k]['smallest_adopted']} / {out[k]['smallest_all15']} / {out[k]['smallest_any']}")
    with open(os.path.join(HERE, "summary_targets.json"), "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, "summary_targets.out"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
