#!/usr/bin/env python3
"""Validate the C engine (pcgt) against a cylcgt value database.

For every record of the database, compare pcgt's option-sorted show string and
outcome with the record (the record's value is cylcgt.show with option lists
sorted, i.e. norm_show; raw strings are normalised here as well).

Usage (from the project root):
  .venv/bin/python atlas/targets/check_db.py DB.jsonl[.gz] PCGT_OUTPUT.tsv
"""
from __future__ import annotations

import gzip
import json
import sys


def norm_show(s: str) -> str:
    """cgt.show with every option list sorted, recursively (as atlas/flat8/rerun)."""
    s = s.strip()
    if not s.startswith("{"):
        return s
    body = s[1:-1]
    depth, parts, cur, side = 0, [[], []], [], 0
    i = 0
    while i < len(body):
        c = body[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        if depth == 0 and body.startswith(" | ", i):
            parts[side].append("".join(cur)); cur = []; side = 1; i += 3; continue
        if depth == 0 and body.startswith(", ", i):
            parts[side].append("".join(cur)); cur = []; i += 2; continue
        cur.append(c)
        i += 1
    parts[side].append("".join(cur))
    L = sorted(norm_show(x) for x in parts[0] if x.strip())
    R = sorted(norm_show(x) for x in parts[1] if x.strip())
    return "{" + ", ".join(L) + " | " + ", ".join(R) + "}"


def read_pcgt(path):
    pos, vals = {}, {}
    with open(path) as fh:
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if p[0] == "#V":
                vals[int(p[1])] = (p[4], p[5])
            else:
                pos[(p[0], int(p[1]), int(p[2]))] = (int(p[6]), p[7])
    return pos, vals


def opener(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path)


def main():
    db, out = sys.argv[1], sys.argv[2]
    pos, vals = read_pcgt(out)
    n = bad_show = bad_out = missing = 0
    examples = []
    with opener(db) as fh:
        for line in fh:
            r = json.loads(line)
            n += 1
            k = (r["position"], r["width"], 0)
            if k not in pos:
                missing += 1
                continue
            gid, oc = pos[k]
            s = vals[gid][0]
            if norm_show(r["value"]) != s:
                bad_show += 1
                if len(examples) < 5:
                    examples.append((r["position"], r["width"], r["value"][:80], s[:80]))
            if r["outcome"] != oc:
                bad_out += 1
    print(f"db {db}: {n} records; missing {missing}; show mismatches {bad_show}; outcome mismatches {bad_out}")
    for e in examples:
        print("  ", e)


if __name__ == "__main__":
    main()
