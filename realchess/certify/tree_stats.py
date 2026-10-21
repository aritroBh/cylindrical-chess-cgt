"""Model-tree statistics and race sensitivity of an a-d component embedded
next to the g-file trebuchet (WK f5, Pg4 / BK h4, Pg5).

For the loaded cylcgt (textbook in the main checkout; e.p.-aware when run from
the ep-aware worktree, see run_both below) this reports
  * internal nodes and terminals of the CGT game tree (realchess.component),
    and the number of men of every terminal and internal node once embedded
    (component pawns + 4 trebuchet men);
  * race terminals (both sides passed) and their men;
  * the value of the component when every race terminal is scored by each
    rule, and by the rule that gives the reference value (e.g. *2);
  * race sensitivity: for the reference rule, every race terminal t whose
    re-scoring alone (to the other side's win, mover-specific) changes the value;
  * whether ANY scoring of the race terminals (each entry (t, mover) free in
    {+BIG, -BIG}) can give *2, by the monotone sandwich
        all races -BIG <= G <= all races +BIG
    and, if the sandwich does not decide, a greedy minimal set of race entries
    that pins *2 when fixed at the reference rule.

One-sided terminals stay at the model's +-BIG throughout: this is a MODEL
analysis, not a real-chess one.

    PYTHONPATH=. .venv/bin/python -m realchess.certify.tree_stats --component "W: a3 b3 c2 / B: b5 b7 c6" \
        --ref-rule opponent --out realchess/certify/results/<tag>_tree_textbook.json
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
EPAWARE_DEFAULT = ("/private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/"
                   "57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt")


def analyse(component: str, ref_rule: str, ep_on: bool = True, flips: bool = True):
    from cylcgt import cgt, pawns
    from cylcgt.pawns import Board, Pos
    from realchess import component as C

    board = Board(4, 8, False, ep_on)
    comp = Pos.parse(component)
    internal, terms, edges = C.enumerate_tree(board, comp)
    men = lambda p: 4 + len(p.white) + len(p.black)
    races = {t for t in terms if pawns.passed(board, t, "W") and pawns.passed(board, t, "B")}
    movers = {}
    for (p, side), kids in edges.items():
        for q in kids:
            if q in terms:
                movers.setdefault(q, set()).add(side)
    BIG = pawns.BIG
    GB, GNB = cgt.integer(BIG), cgt.integer(-BIG)

    def val(score):  # score(t, mover) -> +1/-1
        return C.value_with(board, comp, lambda q, m: GB if score(q, m) > 0 else GNB)

    def rule_score(rule):
        return lambda q, m: C.model_terminal_value(board, q, m, rule)

    out = {"component": component, "cylcgt_file": pawns.__file__,
           "passed_test": "e.p.-aware" if getattr(pawns, "PASSED_RESPECTS_EP", False) else "textbook",
           "ep": ep_on, "internal_nodes": len(internal), "terminals": len(terms),
           "internal_by_men": dict(sorted(Counter(men(p) for p in internal).items())),
           "terminals_by_men": dict(sorted(Counter(men(t) for t in terms).items())),
           "race_terminals": len(races),
           "race_terminals_by_men": dict(sorted(Counter(men(t) for t in races).items())),
           "race_entries": sum(len(movers[t]) for t in races)}
    vals = {}
    for rule in ("count", "mover", "opponent"):
        g = val(rule_score(rule))
        vals[rule] = g
        out[f"value_{rule}"] = cgt.show(g)
    # cross-check against cylcgt's own value
    for rule in ("count", "mover", "opponent"):
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        out[f"cylcgt_value_{rule}_matches"] = pawns.value(board, comp) is vals[rule]
    pawns.RACE_RULE = "count"
    pawns._value.cache_clear()
    ref = vals[ref_rule]
    out["reference_rule"] = ref_rule
    out["reference_value"] = cgt.show(ref)
    star2 = cgt.nimber(2)
    base = rule_score(ref_rule)
    # race entries where count and the reference rule disagree
    entries = sorted(((t, m) for t in races for m in movers[t]), key=lambda e: (men(e[0]), str(e[0]), e[1]))
    out["race_entries_ref_vs_count_disagree"] = sum(
        1 for t, m in entries if base(t, m) != rule_score("count")(t, m))
    # single flips
    crit = []
    for t, m in (entries if flips else []):
        flip = lambda q, mm, t=t, m=m: (-base(q, mm) if (q == t and mm == m) else base(q, mm))
        g = val(flip)
        if g is not ref:
            crit.append({"terminal": str(t), "entered_by": m, "men": men(t),
                         "ref_winner": "W" if base(t, m) > 0 else "B",
                         "count_winner": "W" if rule_score("count")(t, m) > 0 else "B",
                         "value_if_flipped": cgt.show(g)})
    out["single_flip_critical_race_entries"] = crit
    # sandwich over all race entries
    lo = val(lambda q, m: -1 if q in races else base(q, m))
    hi = val(lambda q, m: +1 if q in races else base(q, m))
    out["all_races_free_bounds"] = [cgt.show(lo), cgt.show(hi)]
    out["all_races_free_excludes_star2"] = (not cgt.le(lo, star2)) or (not cgt.le(star2, hi))
    # greedy minimal set of race entries that, fixed at the reference rule,
    # pin the value to ref while all other race entries are free
    if flips:
        fixed = set(entries)
        for e in sorted(entries, key=lambda e: (-men(e[0]), str(e[0]), e[1])):
            fixed.discard(e)
            lo = val(lambda q, m: base(q, m) if (q, m) in fixed or q not in races else -1)
            hi = val(lambda q, m: base(q, m) if (q, m) in fixed or q not in races else +1)
            if not (lo is ref and hi is ref):
                fixed.add(e)
        out["pinning_race_set_size"] = len(fixed)
        out["pinning_race_set"] = [{"terminal": str(t), "entered_by": m, "men": men(t),
                                    "ref_winner": "W" if base(t, m) > 0 else "B",
                                    "count_winner": "W" if rule_score("count")(t, m) > 0 else "B"}
                                   for t, m in sorted(fixed, key=lambda e: (men(e[0]), str(e[0]), e[1]))]
    return out


def run_both(component, ref_rule, ep_path=None, flips=True):
    ep_path = ep_path or os.environ.get("REALCHESS_EPAWARE_PATH", EPAWARE_DEFAULT)
    res = {}
    for name, root in (("textbook", ROOT), ("ep_aware", ep_path)):
        env = dict(os.environ, PYTHONPATH=root + os.pathsep + ROOT)
        cmd = [sys.executable, "-m", "realchess.certify.tree_stats", "--inner", "--component", component,
               "--ref-rule", ref_rule] + ([] if flips else ["--no-flips"])
        r = subprocess.run(cmd, env=env, cwd=root, capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(r.stderr[-3000:])
        out = json.loads(r.stdout.strip().splitlines()[-1])
        want = os.path.realpath(os.path.join(root, "cylcgt"))
        assert os.path.realpath(out["cylcgt_file"]).startswith(want), out["cylcgt_file"]
        res[name] = out
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", required=True)
    ap.add_argument("--ref-rule", default="opponent")
    ap.add_argument("--inner", action="store_true")
    ap.add_argument("--no-flips", action="store_true", help="skip the single-flip and pinning-set passes")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.inner:
        print(json.dumps(analyse(a.component, a.ref_rule, flips=not a.no_flips)))
        return
    res = run_both(a.component, a.ref_rule, flips=not a.no_flips)
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(res, fh, indent=1)
    for name, o in res.items():
        brief = {k: v for k, v in o.items() if k not in ("single_flip_critical_race_entries", "pinning_race_set")}
        brief["single_flip_critical"] = len(o.get("single_flip_critical_race_entries", []))
        print(name, json.dumps(brief, indent=1))


if __name__ == "__main__":
    main()
