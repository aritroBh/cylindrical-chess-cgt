"""K21: aggregate logs/*.json into summary.json"""
import json, glob, os, collections
here = os.path.dirname(os.path.abspath(__file__)); logs = os.path.join(here, "..", "logs")
S = {}
def load(pat): return [json.load(open(f)) for f in sorted(glob.glob(os.path.join(logs, pat)))]
# bridge
tab = collections.Counter(); N = 0; viol = 0
for d in load("bridge_*.json"):
    N += d["N"]; viol += d["n_violations"]
    for k, v in d["table"].items(): tab[k] += v
S["bridge"] = {"instances": N, "violations(dominance-not-equal or criterion-not-dominance)": viol, "table": dict(sorted(tab.items()))}
# sandwich
agg = collections.Counter()
for d in load("sandwich_*.json"):
    for k in ("inst", "states", "viol", "dud_eq_viol", "nontrivial_S_between", "states_suicide_S", "viol_suicide_S"): agg[k] += d[k]
S["sandwich"] = dict(agg)
agg = collections.Counter()
for d in load("stopper_*.json"):
    for k in d:
        if k not in ("exp", "N", "seed"): agg[k] += d[k]
S["stopper"] = dict(agg)
agg = collections.Counter(); ex = []
for d in load("regime_*.json"):
    for k, v in d["stats"].items(): agg[k] += v
    ex += d["C1_examples"][:1]
S["regime"] = dict(sorted(agg.items()))
for key in ("subadd", "thm34", "over46"):
    a = collections.Counter()
    for d in load(key + "_*.json"):
        for k in ("checked", "violations", "cases_W_second"):
            if k in d: a[k] += d[k]
    S[key] = dict(a)
a = collections.Counter()
for d in load("thm111b_*.json"):
    for k in ("N", "pairwise_safe_instances", "with_events", "criterion_fail", "dominance_fail", "D_neq_CGT"): a[k] += d[k]
S["thm111b"] = dict(a)
a = collections.Counter()
for d in load("pure_*.json"):
    for k in ("checked", "violations"): a[k] += d[k]
S["pure_reservoirs"] = dict(a)
a = collections.Counter()
for d in load("onestopper_*.json"):
    for k in ("N", "instances", "with_events", "skipped_infinite_reserve", "criterion_fail", "D_neq_CGT"): a[k] += d[k]
S["one_finite_stopper_plus_safe_short"] = dict(a)
S["crosscheck"] = load("crosscheck_*.json")
S["chess_P_model"] = {"set24": "21 of 24 agree (18 Z_on contexts: 15 agree; 6 Z_off contexts: 6 agree); see logs/chess_P_compare.txt",
                      "random80": "64 of 80 agree; see logs/chess_rand_compare.txt", "direction": "logs/chess_direction.txt",
                      "all98_Zon": "79 agree, 13 differ in White's favour, 5 draws where D predicts a decision, 1 worse for White (race)"}
json.dump(S, open(os.path.join(here, "..", "summary.json"), "w"), indent=1)
print(json.dumps(S, indent=1))
