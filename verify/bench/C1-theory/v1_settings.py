"""C1-theory verifier: rebuild library v1 (textbook filters 1-5, filter 5' off)
and evaluate each v1 component in all 12 settings with the e.p.-aware cylcgt.
Run:
 cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
   .venv/bin/python verify/bench/C1-theory/v1_settings.py <ep-wt root>
"""
import sys, json, time
from collections import Counter
sys.path.insert(0, sys.argv[1])
sys.path.insert(1, "/Users/aritro/Downloads/Research/Chessendgames")
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
assert hasattr(pawns, "PASSED_RESPECTS_EP"), pawns.__file__
from bench import components as C, cgtfmt

t0 = time.time()
orig = C.ep_relevant
C.ep_relevant = lambda w, p, at_terminals=False: False if at_terminals else orig(w, p)
try:
    v1, st = C.build(verbose=False)
finally:
    C.ep_relevant = orig
print("v1 size", len(v1), "build s", round(time.time() - t0), flush=True)
vals = Counter(r["value_ascii"] for r in v1)
kinds = Counter(r["kind"] for r in v1)
print("v1 kinds", dict(kinds))
print("v1 values", dict(sorted(vals.items(), key=lambda kv: -kv[1])))
nonint_numbers = [(r["position"], r["value_ascii"]) for r in v1 if r["kind"] == "number"]
print("v1 kind=number:", Counter(v for _, v in nonint_numbers))

def evalall(w, p):
    out = {}
    for aware in (False, True):
        pawns.PASSED_RESPECTS_EP = aware
        for rule in C.RULES:
            pawns.RACE_RULE = rule
            pawns._value.cache_clear()
            for ep in C.EPS:
                b = Board(w, C.RANKS, False, ep)
                try:
                    g = pawns.value(b, p)
                except pawns.RaceError:
                    g = None
                kv = []
                for side, _, c in C._children(w, p, ep):
                    try:
                        kv.append(pawns._child(b, c, side))
                    except pawns.RaceError:
                        kv.append(None)
                out[(aware, rule, ep)] = (g, tuple(kv))
    return out

# group by setting to use the cache efficiently
recs = [(r["width"], r["_pos"], r) for r in v1]
res = {i: {} for i in range(len(recs))}
for aware in (False, True):
    pawns.PASSED_RESPECTS_EP = aware
    for rule in C.RULES:
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        for ep in C.EPS:
            for i, (w, p, r) in enumerate(recs):
                b = Board(w, C.RANKS, False, ep)
                try:
                    g = pawns.value(b, p)
                except pawns.RaceError:
                    g = None
                kv = []
                for side, _, c in C._children(w, p, ep):
                    try:
                        kv.append(pawns._child(b, c, side))
                    except pawns.RaceError:
                        kv.append(None)
                res[i][(aware, rule, ep)] = (g, tuple(kv))
    print("aware", aware, "done", round(time.time() - t0), flush=True)
pawns.PASSED_RESPECTS_EP = False; pawns.RACE_RULE = "count"; pawns._value.cache_clear()

f = lambda g: "race" if g is None else cgtfmt.fmt(g, ascii=True)
differs_any = []
root_by_setting = Counter()
root_any = []
child_only = []
epoff_diff = 0
differs_by_setting = Counter()
per = []
for i, (w, p, r) in enumerate(recs):
    d = res[i]
    ds = [(rule, ep) for rule in C.RULES for ep in C.EPS if d[(False, rule, ep)] != d[(True, rule, ep)]]
    for rule, ep in ds:
        differs_by_setting[(rule, ep)] += 1
        if not ep:
            epoff_diff += 1
    rd = [(rule, ep) for rule in C.RULES for ep in C.EPS if d[(False, rule, ep)][0] is not d[(True, rule, ep)][0]]
    for s in rd:
        root_by_setting[s] += 1
    if ds:
        differs_any.append(i)
        per.append({"position": r["position"], "width": w, "textbook_value": r["value_ascii"],
                    "differs_settings": [f"{a},{'on' if b else 'off'}" for a, b in ds],
                    "root_differs_settings": [f"{a},{'on' if b else 'off'}" for a, b in rd],
                    "aware_root": {f"{a},{'on' if b else 'off'}": f(d[(True, a, b)][0]) for a in C.RULES for b in C.EPS}})
    if rd:
        root_any.append(i)
half = [r for r in v1 if r["value_ascii"] in ("1/2", "-1/2", "1/2*", "-1/2*")]
half_in = sum(1 for r in half if any(per_r["position"] == r["position"] for per_r in per))
summary = {
    "v1 size": len(v1),
    "differs in some setting (root or child)": len(differs_any),
    "differs by setting": {f"{a},{'on' if b else 'off'}": n for (a, b), n in differs_by_setting.items()},
    "root differs by setting": {f"{a},{'on' if b else 'off'}": n for (a, b), n in root_by_setting.items()},
    "root differs in some setting": len(root_any),
    "e.p.-off setting differences (any)": epoff_diff,
    "v1 components valued +-1/2 or +-1/2*": len(half),
    "... of which change": half_in,
    "v1 kind counts": dict(kinds),
    "seconds": round(time.time() - t0),
}
print(json.dumps(summary, indent=1))
out = "/Users/aritro/Downloads/Research/Chessendgames/verify/bench/C1-theory/v1_settings.json"
json.dump({"summary": summary, "changed": per, "v1_values": dict(vals),
           "v1": [{"id": f"C{i:04d}", "width": r["width"], "position": r["position"], "value": r["value_ascii"], "kind": r["kind"]} for i, r in enumerate(v1)]},
          open(out, "w"), indent=1)
