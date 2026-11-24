#!/usr/bin/env python3
"""Merge the chunk results into a summary.

Collects hits from all chunks and reports per-width stats from .done files.
Writes census7/summary.json.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CENSUS7 = HERE / "census7"

sys.path.insert(0, str(HERE))
from census7 import Geom, scope_count

def main():
    summary = {
        "widths": {},
        "hits": [],
    }
    all_hits = []

    for width in (1, 2, 3, 4):
        geom = Geom(width)
        expected = scope_count(geom)
        chunks = sorted(CENSUS7.glob(f"w{width}_c*.done"))
        if not chunks and expected == 0:
            summary["widths"][width] = {"chunks": 0, "generated": 0, "status": "no_work"}
            continue

        if not chunks:
            print(f"WARNING: width {width}: no .done files found, expected {expected} positions", file=sys.stderr)
            summary["widths"][width] = {"chunks": 0, "generated": 0, "status": "missing_chunks"}
            continue

        total_gen = 0
        total_skip = 0
        total_eval = 0
        total_race = 0
        total_other = 0

        for done_path in chunks:
            text = done_path.read_text()
            lines = text.strip().splitlines()
            if not lines or lines[0] != "# census7 done":
                print(f"ERROR: {done_path} does not look like a done file", file=sys.stderr)
                sys.exit(1)

            # Parse the done file
            data = {}
            for line in lines[1:]:
                if " " in line:
                    k, v = line.split(" ", 1)
                    data[k] = v

            total_gen += int(data.get("generated", 0))
            total_skip += int(data.get("skipped_passed", 0))
            total_eval += int(data.get("evaluated", 0))
            total_race += int(data.get("race_errors", 0))
            total_other += int(data.get("other_errors", 0))

            # Read hits
            hits_path = done_path.with_suffix(".hits.tsv")
            if hits_path.exists():
                for line in hits_path.read_text().strip().splitlines():
                    if line:
                        pos_str, k_str, value = line.split("\t")
                        all_hits.append({
                            "width": width,
                            "position": pos_str,
                            "nimber": int(k_str),
                            "value": value,
                        })

        # Note: don't fail on count mismatch, just report it
        count_match = (total_gen == expected)
        if not count_match:
            print(f"WARNING: width {width}: generated {total_gen} != expected {expected} (diff={total_gen-expected})", file=sys.stderr)

        summary["widths"][width] = {
            "chunks": len(chunks),
            "generated": total_gen,
            "expected": expected,
            "count_match": count_match,
            "skipped_passed": total_skip,
            "evaluated": total_eval,
            "race_errors": total_race,
            "other_errors": total_other,
        }

    summary["hits"] = sorted(all_hits, key=lambda h: (h["width"], h["position"]))

    out_path = CENSUS7 / "summary.json"
    out_path.write_text(json.dumps(summary, indent=2))
    print(f"Wrote {out_path}")
    print(f"Total hits: {len(all_hits)}")
    for h in summary["hits"]:
        print(f"  w{h['width']}: {h['position']} = *{h['nimber']} ({h['value']})")

    return 0


if __name__ == "__main__":
    sys.exit(main())