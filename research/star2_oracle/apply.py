"""T20 resume: put the exact kpsolve results for the decisive 8-man terminal sides
into the sandwich and report the bounds, the exclusion of *2 and 0, and the
sensitivity of each still-open decisive side.

kpsolve prints "<position> | A B", both from WHITE's point of view whoever is to
move (kings/SPEC.md, "Output format"; kpsolve.c wpov()), exact when A == B.
The raw terminal pairs in oracle_value are also White's view (rW, rB), so the
values are used as they stand.  (The first version of this script flipped the
sign for black-to-move lines; that was wrong and is fixed here.)

    PYTHONPATH=. .venv/bin/python research/star2_oracle/apply.py \
        research/star2_oracle/min_support_A.json research/star2_oracle/kp_A_8men.out \
        --tb research/star2_oracle/tb_A_8men.json --out research/star2_oracle/apply_A.json
    PYTHONPATH=. .venv/bin/python research/star2_oracle/apply.py \
        research/star2_oracle/min_support_B.json research/star2_oracle/kp_B_8men.out \
        --out research/star2_oracle/apply_B.json
"""
import argparse
import json
import sys
import time
from collections import Counter

from cylcgt import cgt
from cylcgt.pawns import Pos

from realchess.certify import termdb
from realchess.certify.oracle10 import raw_from_db, side_fens
from realchess.oracle_value import (TREATMENTS, Terminals, certificate, describe_bounds,
                                    excluded, sandwich)

WDL = {"W": 1, "D": 0, "L": -1}
LBL = {1: "W", 0: "D", -1: "L"}


def tokens(fen):
    board, stm, _castle, ep = fen.split()[:4]
    out = []
    for i, row in enumerate(board.split("/")):
        rank, f = 8 - i, 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
                continue
            out.append(f"{ch}{'abcdefgh'[f]}{rank}")
            f += 1
    return " ".join(out) + f" {stm} {ep}"


ap = argparse.ArgumentParser()
ap.add_argument("min_support")
ap.add_argument("kp", nargs="*")
ap.add_argument("--tb", default=None, help="realchess Searcher results (mover's view) to cross-check")
ap.add_argument("--out", default=None)
ap.add_argument("--treatments", nargs="*", default=list(TREATMENTS))
ap.add_argument("--sens-treatments", nargs="*", default=["free (only L/R fixed)", "switch, draw = Black win",
                                                     "switch, draw = White win", "switch, draw = 0"])
ap.add_argument("--deadline-min", type=float, default=30.0)
ap.add_argument("--sens-men", nargs="*", type=int, default=None,
                help="restrict the sensitivity pass to open sides of terminals with these men counts")
a = ap.parse_args()

d = json.load(open(a.min_support))
kp = {}
for path in a.kp:
    for line in open(path):
        if line.startswith("#") or "|" not in line:
            continue
        pos, res = line.split("|")[:2]
        ab = res.split()
        kp[pos.strip()] = (WDL.get(ab[0]), WDL.get(ab[1]))  # White's view, as printed

T = Terminals(Pos.parse(d["component"]))
byname = {str(t): t for t in T.terms}
needed = [byname[x["terminal"]] for x in d["needed_terminals"]]
db = termdb.load()
raw_none, _ = raw_from_db(T, db, "none", None)
raw_model, _ = raw_from_db(T, db, "model", d["race_rule_for_fill"])

# independent cross-check: realchess Searcher + Lichess tablebase, mover's view
tb = {}
if a.tb:
    for s in json.load(open(a.tb))["sides"]:
        if "interval" not in s:
            continue
        lo, hi = s["interval"]
        tb[(s["terminal"], s["side"])] = (lo, hi) if s["side"] == "W" else (-hi, -lo)  # -> White's view

targets = {"*2": cgt.nimber(2), "0": cgt.ZERO}
out = {"component": d["component"], "min_support_treatment": d["treatment"],
       "race_rule_for_fill": d["race_rule_for_fill"],
       "model_value": d["value_if_needed_sides_as_model"],
       "needed": len(needed), "kp_positions": len(kp),
       "needed_by_men": dict(sorted(Counter(T.men(t) for t in needed).items()))}

info = []
exact = checked2 = mismatch_model = mismatch_tb = 0
for t in needed:
    row = {"terminal": str(t), "men": T.men(t), "model": list(raw_model[t]), "sides": []}
    for i, s in enumerate("WB"):
        f = side_fens(T, t)[s]
        r = kp.get(tokens(f))
        ex = bool(r and r[0] == r[1])
        e = {"side_to_move": s, "fen": f, "kpsolve_white_view": list(r) if r else None, "exact": ex,
             "model": raw_model[t][i]}
        if ex:
            exact += 1
            if r[0] != raw_model[t][i]:
                mismatch_model += 1
        tv = tb.get((str(t), s))
        if tv is not None:
            e["searcher_tb_white_view"] = list(tv)
            if ex and tv[0] == tv[1]:
                if tv[0] == r[0]:
                    checked2 += 1
                else:
                    mismatch_tb += 1
        row["sides"].append(e)
    info.append(row)
out["needed_detail"] = info
out["sides_exact"] = exact
out["sides_exact_disagree_with_model"] = mismatch_model
out["sides_exact_also_by_searcher_tb"] = checked2
out["sides_exact_searcher_tb_disagree"] = mismatch_tb
solved_men = sorted({T.men(t) for t in needed if all(kp.get(tokens(side_fens(T, t)[s])) for s in "WB")})
out["men_solved"] = solved_men

# exact kpsolve sides fixed, every other terminal (and every other side) free
applied = dict(raw_none)
for t in needed:
    vals = []
    for s in "WB":
        r = kp.get(tokens(side_fens(T, t)[s]))
        vals.append(r[0] if (r and r[0] == r[1]) else None)
    applied[t] = tuple(vals)
open_sides = [(t, i) for t in needed for i in (0, 1) if applied[t][i] is None]
out["sides_open"] = len(open_sides)
out["open_by_men"] = dict(sorted(Counter(T.men(t) for t, _ in open_sides).items()))
out["open_terminals_by_men"] = dict(sorted(Counter(T.men(t) for t in needed
                                                    if any(applied[t][i] is None for i in (0, 1))).items()))
out["open_sides_list"] = [{"terminal": str(t), "men": T.men(t), "side_to_move": "WB"[i],
                           "fen": side_fens(T, t)["WB"[i]], "model": raw_model[t][i]}
                          for t, i in open_sides]

# conditional: open decisive sides at the model assignment
cond = dict(applied)
for t in needed:
    cond[t] = tuple(raw_model[t][i] if applied[t][i] is None else applied[t][i] for i in (0, 1))

out["bounds"] = {}
for name in a.treatments:
    kind, dr = TREATMENTS[name]
    g_lo, g_hi = sandwich(T, applied, kind, dr)
    b = describe_bounds(g_lo, g_hi, targets)
    c_lo, c_hi = sandwich(T, cond, kind, dr)
    b["conditional_open_sides_at_model"] = {"G_lo": cgt.show(c_lo), "G_hi": cgt.show(c_hi),
                                           "pinned": c_lo is c_hi}
    n_lo, n_hi = sandwich(T, raw_none, kind, dr)
    b["before_any_8man_result"] = {"G_lo": cgt.show(n_lo), "G_hi": cgt.show(n_hi)}
    b["certificate_not_target_*2"] = {dr2: certificate(T, applied, cgt.nimber(2), dr, dr2)
                                      for dr2 in ("left", "right")}
    b["certificate_not_target_0"] = {dr2: certificate(T, applied, cgt.ZERO, dr, dr2)
                                     for dr2 in ("left", "right")}
    out["bounds"][name] = b

def dump():
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(out, fh, indent=1)


# bounds first, so a long sensitivity pass cannot lose them
dump()

# sensitivity: each still-open decisive side alone at W/D/L, every other open
# decisive side at the model assignment (the exact sides stay fixed).
# One treatment at a time, results written after each; --deadline-min stops the pass.
sens = [{"terminal": str(t), "men": T.men(t), "side_to_move": "WB"[i], "model": raw_model[t][i],
         "fen": side_fens(T, t)["WB"[i]], "trials": {}}
        for t, i in open_sides if a.sens_men is None or T.men(t) in a.sens_men]
sens_sides = [(t, i) for t, i in open_sides if a.sens_men is None or T.men(t) in a.sens_men]
out["sensitivity"] = sens
out["sensitivity_treatments_done"] = []
t_start = time.time()
for name in a.sens_treatments:
    kind, dr = TREATMENTS[name]
    if time.time() - t_start > 60 * a.deadline_min:
        print("deadline: skipping sensitivity for", name, flush=True)
        continue
    partial = False
    for (t, i), row in zip(sens_sides, sens):
        if time.time() - t_start > 60 * a.deadline_min:
            partial = True
            break
        res = {}
        for v in (1, 0, -1):
            trial = dict(cond)
            trial[t] = tuple(v if j == i else cond[t][j] for j in range(2))
            lo, hi = sandwich(T, trial, kind, dr)
            ex = excluded(lo, hi, cgt.nimber(2))
            res[LBL[v]] = {"G_lo": cgt.show(lo), "G_hi": cgt.show(hi), "pinned": lo is hi,
                           "value": cgt.show(lo) if lo is hi else None,
                           "excludes_*2": ex["by_lower_bound"] or ex["by_upper_bound"]}
        row["trials"][name] = res
    out["sensitivity_treatments_done"].append(name + (" (PARTIAL: deadline)" if partial else ""))
    dump()
    print("sensitivity done:", name, round(time.time() - t_start), "s", flush=True)

if a.out:
    print("wrote", a.out)
print(json.dumps({k: v for k, v in out.items()
                  if k not in ("needed_detail", "sensitivity", "open_sides_list", "bounds")}, indent=1))
for name, b in out["bounds"].items():
    print(f"--- {name}: pinned={b['pinned']} excludes*2={b['excludes *2']} excludes0={b['excludes 0']} "
          f"cond(open at model) pinned={b['conditional_open_sides_at_model']['pinned']} "
          f"= {b['conditional_open_sides_at_model']['G_lo'][:40]}")
    print("    G_lo =", b["G_lo"][:100])
    print("    G_hi =", b["G_hi"][:100])
