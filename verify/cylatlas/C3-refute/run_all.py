"""Independent recomputation of the C3 value sets (count rule, e.p. on, w+b <= 5).

  cd /Users/aritro/Downloads/Research/Chessendgames/verify/cylatlas/C3-refute && \
  nohup ../../../.venv/bin/python -I run_all.py > run_all.log 2>&1 &

Structure used (each fact is elementary and re-derived here, not taken from
the worker):
  * every root position without a passer has >= 2 pawns per component, so with
    <= 5 pawns a flat root is one full-span component (span <= 5) or a sum of a
    2-pawn component (span <= 2) and a 2- or 3-pawn component (span <= 3),
    needing s1 + s2 + 1 files;
  * an n-file cylinder root either occupies every file (a ring) or has an empty
    file, and is then literally the (n-1)-file flat strip cut there.
Output: results.json with per-atom value keys and witnesses.
"""
from __future__ import annotations

import itertools
import json
import sys
import time

sys.path.insert(0, ".")
import mycgt as C  # noqa: E402
import mypawns as P  # noqa: E402

FILES = "abcdefgh"
PR = range(2, 8)


def txt(W, B):
    return ("W: " + " ".join(f"{FILES[f]}{r}" for f, r in sorted(W)) + " / B: " +
            " ".join(f"{FILES[f]}{r}" for f, r in sorted(B)))


def roots(geom, s, p):
    """all (W, B) with p pawns on s files (ranks 2..7), every file occupied, no passer."""
    sqs = [(f, r) for f in range(s) for r in PR]
    for w in range(1, p):
        b = p - w
        for Wt in itertools.combinations(sqs, w):
            Ws = set(Wt)
            zone = [(f, r) for (f, r) in sqs if (f, r) not in Ws and
                    any((g == f or g in P.nbrs(geom, f)) and t < r for g, t in Wt)]
            for Bt in itertools.combinations(zone, b):
                ok = True
                for (f, r) in Wt:
                    nb = P.nbrs(geom, f)
                    if not any((g == f or g in nb) and t > r for g, t in Bt):
                        ok = False
                        break
                if not ok:
                    continue
                if len({f for f, _ in Wt} | {f for f, _ in Bt}) != s:
                    continue
                yield Wt, Bt


def main():
    res = {"atoms": {}, "sums": {}}
    nodes = {}  # (kind, s, p) -> {key: node}
    t0 = time.time()
    blocks = [("ring", 3, 3), ("ring", 3, 4), ("ring", 3, 5), ("ring", 4, 4), ("ring", 4, 5), ("ring", 5, 5)]
    blocks += [("flat", s, p) for p in range(2, 6) for s in range(1, 6) if s <= p]
    for kind, s, p in blocks:
        geom = ("ring", s) if kind == "ring" else ("flat",)
        d = {}
        canon = set()
        cnt = 0
        t1 = time.time()
        for W, B in roots(geom, s, p):
            cnt += 1
            if kind == "ring":
                canon.add(P._ring_norm(s, W, B, None))
            else:
                canon.add(P._flat_norm(W, B, None))
            # the root check: no passer (also guaranteed by roots())
            v, reach = P.start_value(geom, W, B)
            k = C.key(v)
            if k not in d:
                d[k] = {"wit": txt(W, B), "big": C.has_big(v), "reach": reach, "n": 1}
                nodes.setdefault((kind, s, p), {})[k] = v
            else:
                d[k]["n"] += 1
        res["atoms"][f"{kind}{s}_p{p}"] = {"positions_raw": cnt, "positions_canon": len(canon), "values": d}
        print(f"{kind} s={s} p={p}: raw={cnt} canon={len(canon)} values={len(d)} "
              f"memo={len(P.MEMO)} t={time.time()-t1:.1f}s total={time.time()-t0:.1f}s", flush=True)
        with open("results.json", "w") as fh:
            json.dump(res, fh)
    # sums: a 2-pawn flat component (span s1) + a 2- or 3-pawn flat component (span s2)
    t1 = time.time()
    sums = {}
    for s1 in (1, 2):
        A = res["atoms"].get(f"flat{s1}_p2", {}).get("values", {})
        for p2 in (2, 3):
            for s2 in range(1, p2 + 1):
                Bv = res["atoms"].get(f"flat{s2}_p{p2}", {}).get("values", {})
                for ka, da in A.items():
                    va = nodes[("flat", s1, 2)][ka]
                    for kb, db in Bv.items():
                        vb = nodes[("flat", s2, p2)][kb]
                        v = C.add(va, vb)
                        k = C.key(v)
                        width = s1 + s2 + 1
                        unsafe = (da["reach"][0] and db["reach"][1]) or (da["reach"][1] and db["reach"][0])
                        e = sums.get(k)
                        rec = {"width": width, "pawns": 2 + p2, "wit": da["wit"] + " + " + db["wit"],
                               "big": C.has_big(v), "unsafe_reach": bool(unsafe)}
                        if e is None:
                            sums[k] = {"min_width": width, "min_width_safe": None if unsafe else width,
                                       "big": rec["big"], "wit": rec["wit"], "pawns": rec["pawns"]}
                        else:
                            e["min_width"] = min(e["min_width"], width)
                            if not unsafe:
                                e["min_width_safe"] = width if e["min_width_safe"] is None else min(e["min_width_safe"], width)
    res["sums"] = sums
    print(f"sums: {len(sums)} distinct values t={time.time()-t1:.1f}s", flush=True)
    print(f"races scored: {P.STATS['race']}", flush=True)
    with open("results.json", "w") as fh:
        json.dump(res, fh)
    print("done", time.time() - t0, flush=True)


if __name__ == "__main__":
    main()
