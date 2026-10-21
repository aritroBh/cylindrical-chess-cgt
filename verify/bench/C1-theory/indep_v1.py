"""Independent comparison over the rebuilt v1 list (positions from v1_settings.json):
for each v1 component and each of the 6 (race rule, e.p.) settings, compare the
textbook and e.p.-aware games (root and every child) with the independent solver.
Also classify e.p. captures available in the e.p.-aware tree (e.p. on, count rule):
'urgent' = the pawn that may be taken is textbook-passed (it would be passed if not
taken at once), 'quiet' = it is not.
Run: .venv/bin/python -I verify/bench/C1-theory/indep_v1.py
"""
import sys, json
from collections import Counter
D = "/Users/aritro/Downloads/Research/Chessendgames/verify/bench/C1-theory"
sys.path.insert(0, D)
from indep import *

def main():
    data = json.load(open(f"{D}/v1_settings.json"))
    v1 = data["v1"]
    changed, root_by, any_by = [], Counter(), Counter()
    ep_class = {}
    for c in v1:
        pos = parse(c["position"]); w = c["width"]
        diff_settings, root_settings = [], []
        for race in ("count", "mover", "opponent"):
            for ep in (True, False):
                tb, aw = Rules(w, ep, False, race), Rules(w, ep, True, race)
                r_tb, r_aw = tb.value(pos), aw.value(pos)
                k_tb, k_aw = tb.children(pos), aw.children(pos)
                assert [x[1] for x in k_tb] == [x[1] for x in k_aw]
                rd = not eq(r_tb, r_aw)
                kd = any(not eq(a[2], b[2]) for a, b in zip(k_tb, k_aw))
                tag = f"{race},{'on' if ep else 'off'}"
                if rd: root_by[tag] += 1; root_settings.append(tag)
                if rd or kd: any_by[tag] += 1; diff_settings.append(tag)
        if diff_settings:
            # classify e.p. captures in the e.p.-aware tree (count rule, e.p. on)
            R = Rules(w, True, True, "count")
            seen, stack, cls = set(), [pos], Counter()
            while stack:
                q = stack.pop()
                if q in seen: continue
                seen.add(q)
                if R.passed(q, "W") or R.passed(q, "B"): continue
                W, B, ep = q
                if ep:
                    side = ep[2]
                    with_ep = set(R.moves(q, side)); without = set(R.moves((W, B, None), side))
                    if with_ep != without:
                        mover = "W" if side == "B" else "B"
                        theirs = B if mover == "W" else W
                        cls["urgent" if R.pawn_passed_tb(theirs, mover, ep[1]) else "quiet"] += 1
                # expand as cylcgt does: e.p. right kept only for the side holding it
                for s in "WB":
                    src = q if (not ep or ep[2] == s) else (W, B, None)
                    for c2 in R.moves(src, s):
                        if R.passed(c2, "W") and R.passed(c2, "B"): continue
                        stack.append(c2)
            changed.append({"id": c["id"], "position": c["position"], "textbook": c["value"],
                            "differs": diff_settings, "root_differs": root_settings, "ep_captures_aware_tree": dict(cls)})
            for k in cls: ep_class[k] = ep_class.get(k, 0) + 1
    half = [c for c in v1 if c["value"] in ("1/2", "-1/2", "1/2*", "-1/2*")]
    ch_ids = {c["id"] for c in changed}
    out = {"v1": len(v1), "changed (any setting, root or child)": len(changed),
           "changed by setting": dict(any_by), "root changed by setting": dict(root_by),
           "root changed in some setting": sum(1 for c in changed if c["root_differs"]),
           "+-1/2(*) in v1": len(half), "+-1/2(*) among changed": sum(1 for c in half if c["id"] in ch_ids),
           "changed components with an urgent / quiet e.p. capture in the aware tree": ep_class,
           "changed ids": sorted(ch_ids)}
    json.dump({"summary": out, "changed": changed}, open(f"{D}/indep_v1.json", "w"), indent=1)
    return out
print(json.dumps(run(main), indent=1))
