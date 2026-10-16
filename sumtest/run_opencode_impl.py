"""Part 3 harness: run an external JSON-lines solver on test (a) and a 500-position sample of (b).

The external solver must follow the interface in sumtest/opencode_spec.md:
  python3 solver.py  < problems.jsonl  > answers.jsonl

  PYTHONPATH=. .venv/bin/python -m sumtest.run_opencode_impl [--impl sumtest/opencode_impl/solver.py]

Compares each answer with this directory's brute-force solver (both e.p. passer conventions)
and with cylcgt's stored predictions (sumtest/data/cylcgt__*.json.gz, from compare_cylcgt).
The harness itself was validated with --impl sumtest/jsonl_adapter.py (our own solver behind
the same interface).
"""
import argparse
import gzip
import json
import os
import random
import subprocess
import sys
from collections import Counter

from sumtest.enum_positions import BOARDS, OUT, positions
from sumtest.sumsolver import REF_NAMES

SPEC_KEYS = {"0": "0", "*": "*", "*2": "*2", "*3": "*3", "up": "up", "down": "down", "up*": "up*",
             "dup*": "double-up*", "1/2": "1/2", "-1/2": "-1/2", "1": "1", "-1": "-1",
             "{1|0}": "{1|0}", "+-1": "+-1", "tiny1": "tiny(1)"}
HERE = os.path.dirname(os.path.abspath(__file__))


def problems(n_sample=500, seed=2026):
    out = []
    pid = 0
    for rule in ("count", "mover", "opponent"):
        for ep in (True, False):
            out.append({"id": pid, "files": 4, "wrap": False, "ep": ep, "race_rule": rule,
                        "white": ["a2", "c2"], "black": ["b7", "d7"], "_board": "flat4", "_test": "a"})
            pid += 1
    pool = []
    for b, (f, w) in BOARDS.items():
        geo, pos = positions(f, w)
        pool += [(b, geo.show(W, B)) for W, B in pos]
    rng = random.Random(seed)
    for b, text in rng.sample(pool, n_sample):
        f, w = BOARDS[b]
        wp, bp = [p.split(":")[1].split() for p in text.split("/")]
        for rule in ("count", "mover", "opponent"):
            for ep in (True, False):
                out.append({"id": pid, "files": f, "wrap": w, "ep": ep, "race_rule": rule,
                            "white": wp, "black": bp, "_board": b, "_test": "b", "_text": text})
                pid += 1
    return out


def load(path):
    with gzip.open(path, "rt") as fh:
        return json.load(fh)["outcomes"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--impl", default=os.path.join(HERE, "opencode_impl", "solver.py"))
    ap.add_argument("--timeout", type=int, default=1500)
    a = ap.parse_args()
    probs = problems()
    feed = "\n".join(json.dumps({k: v for k, v in p.items() if not k.startswith("_")}) for p in probs) + "\n"
    impl = os.path.abspath(a.impl)
    r = subprocess.run([sys.executable, "-I", impl], input=feed, capture_output=True, text=True,
                       timeout=a.timeout, cwd=os.path.dirname(impl))
    if r.returncode != 0:
        print("external solver failed:", r.stderr[-2000:])
        sys.exit(1)
    ans = {}
    for line in r.stdout.splitlines():
        line = line.strip()
        if line:
            d = json.loads(line)
            ans[d["id"]] = d["outcomes"]
    cache = {}

    def ref(kind, board, rule, ep):
        if kind == "cylcgt":
            k = f"cylcgt__{board}__{rule}__{'ep' if ep else 'noep'}.json.gz"
        else:
            epv = kind if ep else "off"
            k = f"mine__{board}__{rule}__{epv}__whole.json.gz"
        if k not in cache:
            cache[k] = load(os.path.join(OUT, k))
        return cache[k]

    stats = Counter()
    shown = Counter()
    for p in probs:
        got = ans.get(p["id"])
        if got is None:
            stats[(p["_test"], "missing")] += 1
            continue
        vec = "".join(got.get(SPEC_KEYS[n], "?") for n in REF_NAMES)
        text = p.get("_text") or "W: a2 c2 / B: b7 d7"
        for kind in ("cylcgt", "plain", "aware"):
            want = ref(kind, p["_board"], p["race_rule"], p["ep"])[text]
            ok = vec == want
            stats[(p["_test"], "ep" if p["ep"] else "noep", kind, ok)] += 1
            if not ok and shown[(kind, p["ep"])] < 3:
                shown[(kind, p["ep"])] += 1
                print(f"differs from {kind}: {p['_board']} {p['race_rule']} ep={p['ep']} {text}\n"
                      f"   external: {vec}\n   {kind:8s}: {want}")
        if p["_test"] == "a":
            print(f"test (a) {p['race_rule']:8s} ep={p['ep']!s:5s}: G={got.get('0')} G+*={got.get('*')} "
                  f"G+*2={got.get('*2')} G+*3={got.get('*3')}  full {vec}")
    for k in sorted(stats, key=str):
        print(k, stats[k])


if __name__ == "__main__":
    main()
