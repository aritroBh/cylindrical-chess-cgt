"""Steps 2 and 3 of bench/conventions.py (checks E1 and E3), using its own
functions, but with the 12-setting evaluation restricted to the 518 v1
components instead of all 5,290 candidates (the full run did not fit the time
budget at load ~180). argv: <ep-wt root> <v1_positions.txt>"""
import sys, os, json, time
sys.path.insert(0, os.path.abspath(sys.argv[1]))
from cylcgt import pawns
from cylcgt.pawns import Pos
import bench.conventions as K
import bench.components as C
from collections import Counter
print("cylcgt:", pawns.__file__, "flag:", pawns.PASSED_RESPECTS_EP)
t0 = time.time()
v1 = [(int(a), Pos.parse(b)) for a, b in (l.rstrip("\n").split("|") for l in open(sys.argv[2]) if l.strip())]
# sanity: ptext(Pos.parse(text)) round-trips
assert all(C.ptext(p) == l.rstrip("\n").split("|")[1] for (w, p), l in zip(v1, open(sys.argv[2])))
ev = K.evaluate(v1)
print(f"evaluated {len(v1)} x {len(ev)} settings [{time.time()-t0:.0f}s]", flush=True)
lib = [json.loads(x) for x in (K.DATA / "components.jsonl").read_text().splitlines()]
idx = {(w, p): i for i, (w, p) in enumerate(v1)}
# --- E1 (step 2)
bad = []
for c in lib:
    i = idx[(c["width"], Pos.parse(c["position"]))]
    vals = [ev[s][i] for s in K.SETTINGS]
    if not all(v == vals[0] for v in vals) or vals[0][0] is None or any(x is None for x in vals[0][1]):
        bad.append(c["comp_id"])
    assert K.f(vals[0][0]) == c["value_ascii"], c["comp_id"]
    assert [K.f(x) for x in vals[0][1]] == [m["value"] for m in c["moves"]], c["comp_id"]
print(f"E1: library {len(lib)} components; differing in some setting: {len(bad)} {bad[:5]}")
# how many child values were compared
print("   children compared:", sum(len(ev[K.SETTINGS[0]][idx[(c['width'], Pos.parse(c['position']))]][1]) for c in lib))
# --- E3 (step 3), same code as conventions.main
keep_tb = [i for i, (w, p) in enumerate(v1) if K.passes_filters(i, ev, "textbook", w, p, False)]
print("v1 components passing textbook filters 1-5 (should be all 518):", len(keep_tb))
cur = {(c["width"], c["position"]) for c in lib}
combos, nchg, nroot = Counter(), 0, 0
for i in keep_tb:
    w, p = v1[i]
    tb, aw = ev[("textbook", "count", True)][i], ev[("e.p.-aware", "count", True)][i]
    differs = any(ev[("textbook", r, e)][i] != ev[("e.p.-aware", r, e)][i] for r in C.RULES for e in C.EPS)
    f5p = C.ep_relevant(w, p, at_terminals=True)
    exact = K.judged_differently(w, p)
    K.set_test(True)
    ep_aw = K.ep_reachable_current_test(w, p)
    in_cur = (w, C.ptext(p)) in cur
    combos[(f5p, exact, ep_aw, differs, in_cur)] += 1
    nchg += differs; nroot += differs and (tb[0] is not aw[0])
    assert in_cur == (not f5p) and not (differs and not f5p) and (exact or not (differs or ep_aw))
print(f"E3: v1 changed {nchg}, root changed {nroot}")
print("   (filter5', judged differently, ep capture playable in aware tree, values differ, kept now): count")
for k, v in sorted(combos.items()):
    print("  ", k, v)
print(f"done [{time.time()-t0:.0f}s]")
