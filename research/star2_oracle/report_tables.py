"""T20 resume: print the tables used in REPORT.md from apply_A.json / apply_B.json.

    PYTHONPATH=. .venv/bin/python research/star2_oracle/report_tables.py
"""
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
LBL = {1: "W", 0: "D", -1: "L"}


def pov(r):
    return "-" if r is None else "".join(LBL[x] for x in r)


for X in "AB":
    d = json.load(open(os.path.join(HERE, f"apply_{X}.json")))
    # the draw = 0 pass of apply_X.json stopped at its 30-minute deadline before the 9-man
    # sides; apply_X_draw0_9man.json covers them (same code, --sens-men 9).
    extra = os.path.join(HERE, f"apply_{X}_draw0_9man.json")
    if os.path.exists(extra):
        e = json.load(open(extra))
        have = {(r["terminal"], r["side_to_move"]): r for r in d["sensitivity"]}
        for r in e["sensitivity"]:
            have[(r["terminal"], r["side_to_move"])]["trials"].update(r["trials"])
        d["sensitivity_treatments_done"] = ["free (only L/R fixed)", "switch, draw = Black win",
                                            "switch, draw = White win", "switch, draw = 0 (merged, complete)"]
    print(f"\n######## {X}: {d['component']}")
    print("needed by men:", d["needed_by_men"], " exact sides:", d["sides_exact"],
          " disagree with model:", d["sides_exact_disagree_with_model"],
          " also by searcher+TB:", d["sides_exact_also_by_searcher_tb"],
          " searcher disagree:", d["sides_exact_searcher_tb_disagree"])
    print("open sides:", d["sides_open"], d["open_by_men"], " open terminals:", d["open_terminals_by_men"])
    print("\nsolved 8-man decisive terminals (White's view, W/D/L; model; searcher+TB):")
    for r in d["needed_detail"]:
        if r["men"] != 8:
            continue
        for s in r["sides"]:
            print(f"  {r['terminal']:<28} {s['side_to_move']} to move  kp={pov(s['kpsolve_white_view'])}  "
                  f"tb={pov(s.get('searcher_tb_white_view'))}  model={LBL[s['model']]}  {s['fen']}")
    print("\nbounds per treatment:")
    ref = None
    for name, b in d["bounds"].items():
        key = (b["G_lo"], b["G_hi"])
        ref = ref or key
        print(f"  {name:<28} same-as-first={key == ref} pinned={b['pinned']} outcome_lo={b['outcome_G_lo']} "
              f"outcome_hi={b['outcome_G_hi']} excl*2={b['excludes *2']} excl0={b['excludes 0']} "
              f"cond={b['conditional_open_sides_at_model']['G_lo']}/{b['conditional_open_sides_at_model']['pinned']} "
              f"before_same={(b['before_any_8man_result']['G_lo'], b['before_any_8man_result']['G_hi']) == key} "
              f"cert*2={b['certificate_not_target_*2']} cert0={b['certificate_not_target_0']}")
    b0 = next(iter(d["bounds"].values()))
    print("  G_lo =", b0["G_lo"])
    print("  G_hi =", b0["G_hi"])
    print("\nsensitivity treatments done:", d["sensitivity_treatments_done"])
    # single open side deviating from the model, others at model
    summary = defaultdict(Counter)
    breakers = defaultdict(list)
    for r in d["sensitivity"]:
        for tr, res in r["trials"].items():
            for v, x in res.items():
                if LBL[r["model"]] == v:
                    assert x["pinned"] and x["value"] == "*2", (r["terminal"], tr, v, x)
                    continue
                kind = ("excludes *2" if x["excludes_*2"] else
                        ("pinned to *2 (no change)" if x["pinned"] and x["value"] == "*2" else
                         "unpinned, *2 not excluded"))
                summary[tr][kind] += 1
                if x["excludes_*2"]:
                    breakers[tr].append((r["terminal"], r["men"], r["side_to_move"], LBL[r["model"]], v,
                                         x["value"] if x["pinned"] else f"{x['G_lo'][:30]}..{x['G_hi'][:30]}"))
    for tr, c in summary.items():
        print(f"  deviations from the model, {tr}: {dict(c)}")
    for tr, lst in breakers.items():
        print(f"  single deviations that exclude *2 under '{tr}': {len(lst)}")
        for x in lst:
            print("     ", x)
    # sides that can break *2 under any treatment
    any_break = defaultdict(set)
    for tr, lst in breakers.items():
        for x in lst:
            any_break[(x[0], x[1], x[2])].add((tr, x[4]))
    print(f"  distinct open sides whose single deviation excludes *2 under some treatment: {len(any_break)}")
    men = Counter(k[1] for k in any_break)
    print("   by men:", dict(men))
