"""Descriptive statistics of the ChessSums data quoted in bench/README.md.

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.stats
"""
from __future__ import annotations

import json
import statistics
from collections import Counter
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"


def load(name):
    return [json.loads(x) for x in (DATA / name).read_text().splitlines() if x.strip()]


def main():
    comps = load("components.jsonl")
    vc = Counter(c["value"] for c in comps)
    print(f"components: {len(comps)}, distinct values {len(vc)}")
    print("values:", ", ".join(f"{v} x{n}" for v, n in sorted(vc.items(), key=lambda kv: (-kv[1], kv[0]))))
    print("by width:", dict(sorted(Counter(c["width"] for c in comps).items())))
    print("hold-out tags:", dict(Counter(str(c["heldout"]) for c in comps)))
    orbit_tag = {c["orbit"]: c["heldout"] for c in comps}
    print(f"orbits: {len(orbit_tag)}, by tag {dict(Counter(str(t) for t in orbit_tag.values()))}")
    train_vals = {c["value"] for c in comps if c["heldout"] is None}
    print("held-out values that no training component has:",
          sorted({c["value"] for c in comps if c["heldout"]} - train_vals))
    for sp in ("train", "val", "test", "test_heldout"):
        rows = load(f"{sp}.jsonl")
        r8 = [r for r in rows if r["fits8"]]
        lens = sorted(len(r["value"]) for r in rows)
        share = [len(r["winning_moves"][s]) / len(r["legal_moves"][s]) for r in rows for s in "WB"
                 if r["winning_moves"][s]]
        n_rows = [r for r in rows if r["outcome"] == "N"]
        files = [r["board"]["files"] for r in rows]
        print(f"{sp}: {len(rows)} rows; 8-file {len(r8)} with outcomes {dict(sorted(Counter(r['outcome'] for r in r8).items()))}"
              f" and k {dict(sorted(Counter(r['k'] for r in r8).items()))}; files {min(files)}-{max(files)}; "
              f"value length median {lens[len(lens) // 2]}, p90 {lens[int(0.9 * len(lens))]}, max {lens[-1]}; "
              f"median winning share of legal moves {statistics.median(share):.3g}; "
              f"random legal move wins in N rows {statistics.mean(len(r['winning_moves'][s]) / len(r['legal_moves'][s]) for r in n_rows for s in 'WB'):.3f}; "
              f"kinds {dict(sorted(Counter(r['kind'] for r in rows).items()))}")
        if sp == "test_heldout":
            k1 = {r["components"][0]["comp_id"] for r in rows if r["k"] == 1}
            print(f"  k=1 rows use {len(k1)} distinct held-out components")


if __name__ == "__main__":
    main()
