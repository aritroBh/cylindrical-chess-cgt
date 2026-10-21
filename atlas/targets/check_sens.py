#!/usr/bin/env python3
"""Validate pcgt under the other race rules and with e.p. off, against the
cylinder atlas's sensitivity runs (atlas/cylinder/parts_sens.tar.gz: cylcgt,
textbook test; "atoms" = every file occupied; flat widths 1-4 and cylinder
widths 3-4 with <= 4 pawns, cylinder widths 3-5 with 5 pawns; count / mover /
opponent x e.p. on / off). Exact canonical keys are compared.

Usage (from the project root):
  mkdir -p atlas/targets/work/sens && (cd atlas/targets/work/sens && tar xzf ../../../cylinder/parts_sens.tar.gz)
  .venv/bin/python atlas/targets/check_sens.py
"""
from __future__ import annotations

import glob
import json
import os
import subprocess
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SENS = os.path.join(HERE, "work", "sens", "parts_sens")


def main():
    keys = {}
    for p in glob.glob(os.path.join(SENS, "*.vals")):
        with open(p) as fh:
            for line in fh:
                r = json.loads(line)
                keys[r["vid"]] = r["key"]
    by = defaultdict(list)
    for p in glob.glob(os.path.join(SENS, "*.jsonl")):
        with open(p) as fh:
            for line in fh:
                r = json.loads(line)
                by[(r["rule"], r["ep"])].append((r["n"], r["wrap"], r["pos"], keys[r["vid"]]))
    total = bad = 0
    for (rule, ep), rows in sorted(by.items()):
        rows.sort()
        inp = "".join(f"{p}\t{n}\t{w}\n" for n, w, p, _ in rows)
        out = subprocess.run([os.path.join(HERE, "pcgt"), "--race", rule, "--ep", str(ep)], input=inp,
                             capture_output=True, text=True, check=True).stdout
        mine, vals = {}, {}
        for line in out.splitlines():
            q = line.split("\t")
            if q[0] == "#V":
                vals[int(q[1])] = q[5]
            else:
                mine[(q[0], int(q[1]), int(q[2]))] = int(q[6])
        nb = 0
        for n, w, p, k in rows:
            if vals[mine[(p, n, w)]] != k:
                nb += 1
                if nb <= 3:
                    print("   mismatch", rule, ep, n, w, p, k[:60], vals[mine[(p, n, w)]][:60])
        total += len(rows)
        bad += nb
        print(f"{rule:8s} ep={ep}: {len(rows)} positions, {nb} exact-key mismatches")
    print(f"TOTAL {total} positions, {bad} mismatches")


if __name__ == "__main__":
    main()
