"""Compute cylcgt values of the atoms from enum_atoms.py (verifier script).

  --root R   directory whose cylcgt/ is imported (main checkout = textbook passed
             test; the ep-aware-passed worktree = e.p.-aware test)
  --task flat:k:p | ring:n:p | sums     (sums = every 2-component flat sum with
             2+2 or 2+3 pawns, built from flat atoms with 2 and 3 pawns)

Race rule "count", e.p. on (Board(..., ep=True)).  Output: JSONL, one line per
position (or per sum) with the value id = sha1(exact key)[:16], using the same
key format as atlas/cylinder/atlas_run.py so ids are comparable.

  .venv/bin/python verify/cylatlas/C3-reproduce/values.py --root . --task ring:3:4 --out x.jsonl
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ap = argparse.ArgumentParser()
ap.add_argument("--root", required=True)
ap.add_argument("--task", required=True)
ap.add_argument("--shard", type=int, default=0)
ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--flag", default=None, help="force PASSED_RESPECTS_EP to 0/1 if the module has it")
ap.add_argument("--out", required=True)
a = ap.parse_args()
sys.path.insert(0, os.path.abspath(a.root))

from cylcgt import cgt, pawns  # noqa: E402
from enum_atoms import atoms  # noqa: E402

assert pawns.RACE_RULE == "count"
if a.flag is not None and hasattr(pawns, "PASSED_RESPECTS_EP"):
    pawns.PASSED_RESPECTS_EP = bool(int(a.flag))
    pawns._value.cache_clear()
BIG = pawns.BIG
_k = {}


def key(g):
    r = _k.get(g.id)
    if r is None:
        if g.num is not None:
            x = g.num
            r = str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
        elif g.nim is not None:
            r = f"*{g.nim}"
        else:
            r = "{" + ",".join(sorted(key(x) for x in g.L)) + "|" + ",".join(sorted(key(x) for x in g.R)) + "}"
        _k[g.id] = r
    return r


_b = {}


def big(g):
    r = _b.get(g.id)
    if r is None:
        r = (abs(g.num) >= BIG // 2) if g.num is not None else any(big(x) for x in g.L + g.R)
        _b[g.id] = r
    return r


def rec_of(g, **extra):
    k = key(g)
    s = cgt.show(g)
    return {**extra, "vid": hashlib.sha1(k.encode()).hexdigest()[:16], "big": big(g),
            "show": s if len(s) <= 300 else None}


def txt(W, B):
    F = "abcdefgh"
    return ("W: " + " ".join(f"{F[f]}{r}" for f, r in W) + " / B: " + " ".join(f"{F[f]}{r}" for f, r in B))


t0 = time.time()
meta = {"module": pawns.__file__, "PASSED_RESPECTS_EP": getattr(pawns, "PASSED_RESPECTS_EP", None),
        "race_rule": pawns.RACE_RULE, "task": a.task}
with open(a.out + ".tmp", "w") as fh:
    fh.write(json.dumps({"meta": meta}) + "\n")
    if a.task == "sums":
        comps = {2: [], 3: []}
        for p in (2, 3):
            for k in range(1, p + 1):
                b = pawns.Board(k, 8, False, True)
                for W, B in atoms(k, False, p):
                    g = pawns.value(b, pawns.Pos(frozenset(W), frozenset(B)))
                    comps[p].append((g, f"flat{k}:{txt(W, B)}"))
        # distinct values only
        d2 = {g.id: (g, t) for g, t in comps[2]}
        d3 = {g.id: (g, t) for g, t in comps[3]}
        done = set()
        for (g1, t1) in d2.values():
            for (g2, t2) in list(d2.values()) + list(d3.values()):
                s = cgt.add(g1, g2)
                if s.id in done:
                    continue
                done.add(s.id)
                fh.write(json.dumps(rec_of(s, pos=f"{t1} + {t2}"), ensure_ascii=False) + "\n")
    else:
        kind, n, p = a.task.split(":")
        n, p = int(n), int(p)
        wrap = kind == "ring"
        b = pawns.Board(n, 8, wrap, True)
        for i, (W, B) in enumerate(atoms(n, wrap, p)):
            if i % a.nshards != a.shard:
                continue
            g = pawns.value(b, pawns.Pos(frozenset(W), frozenset(B)))
            fh.write(json.dumps(rec_of(g, kind=kind, n=n, p=p, pos=txt(W, B)), ensure_ascii=False) + "\n")
    fh.write(json.dumps({"done": True, "secs": round(time.time() - t0, 1)}) + "\n")
os.replace(a.out + ".tmp", a.out)
print(a.task, a.shard, "done", round(time.time() - t0, 1), flush=True)
