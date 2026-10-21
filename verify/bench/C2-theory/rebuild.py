"""Independent rebuild of ChessSums library v1 and v2 with indep.py (no cylcgt, no bench imports).

For each of the candidate components (w = 1..4 files, all occupied, 2..4 pawns of both colours on
ranks 2..7, no passer at the root):
  * root value and every child value in the 12 settings (2 passed tests x 3 race rules x e.p. on/off);
  * filters 1-5 under the textbook test (-> v1) and under the e.p.-aware test alone;
  * "judged differently": does any position at which the textbook computation makes a passed-test
    judgement get a different judgement from the e.p.-aware test (audit mode)?
  * filter 5' analogue: at a textbook-terminal position of the tree, is the double-stepped pawn
    textbook-passed and capturable e.p.?
Output: rebuild_out.json (per candidate flags) + printed summary, compared with bench/data/components.jsonl.

Run: cd verify/bench/C2-theory && ../../../.venv/bin/python rebuild.py [--jobs N]
"""
from __future__ import annotations

import itertools
import json
import sys
import time
from collections import Counter
from multiprocessing import get_context
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import indep as I  # noqa: E402

HERE = Path(__file__).resolve().parent
LIB = HERE.parents[2] / "bench" / "data" / "components.jsonl"
RULES = ("count", "mover", "opponent")
EPS = (True, False)


def candidates():
    out = []
    for w in range(1, 5):
        sqs = [(f, r) for f in range(w) for r in range(2, 8)]
        for n in range(max(2, w), 5):
            for S in itertools.combinations(sqs, n):
                if len({f for f, _ in S}) != w:
                    continue
                for cols in itertools.product("WB", repeat=n):
                    if "W" not in cols or "B" not in cols:
                        continue
                    W = frozenset(s for s, c in zip(S, cols) if c == "W")
                    B = frozenset(s for s, c in zip(S, cols) if c == "B")
                    p = (W, B, None)
                    m = I.Model(w, True, False, "count")
                    if m.passed(p, "W", False) or m.passed(p, "B", False):
                        continue
                    out.append((w, p))
    return out


def has_big(g):
    seen, st = set(), [g]
    while st:
        x = st.pop()
        if x.id in seen:
            continue
        seen.add(x.id)
        if x.num is not None:
            if abs(x.num) >= I.BIG // 2:
                return True
            continue
        st.extend(x.L + x.R)
    return False


def tree_scan(w, p, aware):
    """(e.p. capture available at a non-terminal node, e.p.-passer at a terminal node) in the tree
    whose terminal nodes are those where the given test finds a passed pawn."""
    m = I.Model(w, True, aware, "count")
    seen, st = set(), [p]
    ep_internal = ep_leaf = False
    while st:
        q = st.pop()
        if q in seen:
            continue
        seen.add(q)
        if m.passed(q, "W", aware) or m.passed(q, "B", aware):
            if q[2] is not None and m.ep_capture_available(q):
                mover = "B" if q[2][1] == "W" else "W"
                if m.pawn_free(q, mover, q[2][0]):
                    ep_leaf = True
            continue
        if m.ep_capture_available(q):
            ep_internal = True
            continue
        for side in "WB":
            st.extend(m.moves(q, side))
    return ep_internal, ep_leaf, len(seen)


def work(item):
    w, p = item
    res = {}
    mism = 0
    for aware in (False, True):
        for rule in RULES:
            for ep in EPS:
                m, root, kids = I.root_and_children(w, p, ep, aware, rule, audit=True)
                mism += len(m.mismatch)
                res[(aware, rule, ep)] = (root, tuple(k[2] for k in kids))
    out = {"w": w, "pos": I.ptext(p), "mismatch_nodes": mism}
    for aware in (False, True):
        ks = [(aware, r, e) for r in RULES for e in EPS]
        vals = [res[k] for k in ks]
        roots = [v[0] for v in vals]
        ok = all(r is not None for r in roots) and all(r is roots[0] for r in roots)
        ok = ok and not has_big(roots[0])
        ok = ok and all(all(c is not None for c in v[1]) and all(a is b for a, b in zip(v[1], vals[0][1])) for v in vals)
        ep_int, ep_leaf, n = tree_scan(w, p, aware)
        out["f1-4 " + ("aware" if aware else "textbook")] = ok
        out["f5 hit " + ("aware" if aware else "textbook")] = ep_int
        if not aware:
            out["f5' hit (textbook tree)"] = ep_leaf
            out["tree size"] = n
    allv = [res[k] for k in res]
    out["identical in 12 settings"] = all(v[0] is not None and v[0] is allv[0][0] and len(v[1]) == len(allv[0][1])
                                          and all(a is b and a is not None for a, b in zip(v[1], allv[0][1])) for v in allv)
    out["test changes some value"] = any(res[(False, r, e)][0] is not res[(True, r, e)][0] or
                                         any(a is not b for a, b in zip(res[(False, r, e)][1], res[(True, r, e)][1]))
                                         for r in RULES for e in EPS)
    out["test changes root value"] = any(res[(False, r, e)][0] is not res[(True, r, e)][0] for r in RULES for e in EPS)
    r0 = res[(False, "count", True)][0]
    out["outcome textbook count ep"] = None if r0 is None else I.outcome(r0)
    return out


def main():
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 4
    t0 = time.time()
    cands = candidates()
    print("candidates", len(cands), flush=True)
    with get_context("fork").Pool(jobs) as pool:
        rows = list(pool.imap(work, cands, chunksize=10))
    lib = {(json.loads(x)["width"], json.loads(x)["position"]): json.loads(x) for x in LIB.read_text().splitlines()}
    v1 = [r for r in rows if r["f1-4 textbook"] and not r["f5 hit textbook"]]
    aw = [r for r in rows if r["f1-4 aware"] and not r["f5 hit aware"]]
    v2_f5p = [r for r in v1 if not r["f5' hit (textbook tree)"]]
    v2_exact = [r for r in v1 if r["mismatch_nodes"] == 0]
    key = lambda r: (r["w"], r["pos"])
    S = lambda rs: {key(r) for r in rs}
    summ = {
        "candidates": len(cands),
        "v1 (filters 1-5, textbook)": len(v1),
        "filters 1-5, e.p.-aware alone": len(aw),
        "intersection": len(S(v1) & S(aw)),
        "aware-only": len(S(aw) - S(v1)),
        "v1 minus filter-5' analogue": len(v2_f5p),
        "v1 minus components with a judged-differently node": len(v2_exact),
        "filter-5' analogue == judged-differently on v1": S(v2_f5p) == S(v2_exact),
        "removed": len(v1) - len(v2_f5p),
        "removed with some value change between tests": sum(1 for r in v1 if r["f5' hit (textbook tree)"] and r["test changes some value"]),
        "removed with root value change": sum(1 for r in v1 if r["f5' hit (textbook tree)"] and r["test changes root value"]),
        "removed with no value change": sum(1 for r in v1 if r["f5' hit (textbook tree)"] and not r["test changes some value"]),
        "v1 components that change but filter 5' misses": sum(1 for r in v1 if not r["f5' hit (textbook tree)"] and r["test changes some value"]),
        "library size": len(lib),
        "library == independent v2": set(lib) == S(v2_f5p),
        "library minus independent v2": sorted(set(lib) - S(v2_f5p))[:20],
        "independent v2 minus library": sorted(S(v2_f5p) - set(lib))[:20],
        "independent v2: identical in 12 settings": sum(r["identical in 12 settings"] for r in v2_f5p),
        "independent v2: judged-differently nodes (sum)": sum(r["mismatch_nodes"] for r in v2_f5p),
        "library outcome agreement": sum(1 for r in v2_f5p if key(r) in lib and lib[key(r)]["outcome"] == r["outcome textbook count ep"]),
        "max tree size (v2)": max(r["tree size"] for r in v2_f5p),
        "seconds": round(time.time() - t0, 1),
    }
    for k, v in summ.items():
        print(f"{k}: {v}")
    (HERE / "rebuild_out.json").write_text(json.dumps({"summary": summ, "rows": rows}, indent=0) + "\n")


if __name__ == "__main__":
    main()
