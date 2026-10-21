"""Exhaustive nimber scan of all single components ("atoms") with <= P pawns,
plus all two-component sums, with the independent engine (cg.py + pg.py).

Atoms: flat strips of width 1..5 with every file occupied, and rings of 3..5
files (every file occupied); pawns on ranks 2..7; no passer for either side
at the start. One representative per symmetry orbit (flat: mirror; ring:
dihedral group). Every value in the cylinder/flat atlas with w+b <= 5 is an
atom value or a sum of two atom values (2+2 or 2+3 pawns), because a lone
pawn is passed and a cylinder position with an empty file cuts to a flat one.

Run (from this directory):
  ../../../.venv/bin/python scan.py --rule count --ep 1 --epaware 0 --split 1 --maxp 5 --out scan_count_ep1.json
"""
from __future__ import annotations

import argparse
import itertools
import json
import time

import cg
import pg

RANKS = range(2, 8)


def orbit_rep(kind, n, W, B):
    if kind == "C":
        maps = [[(s * f + k) % n for f in range(n)] for s in (1, -1) for k in range(n)]
    else:
        maps = [list(range(n)), [n - 1 - f for f in range(n)]]
    best = None
    for m in maps:
        img = (tuple(sorted((m[f], r) for f, r in W)), tuple(sorted((m[f], r) for f, r in B)))
        if best is None or img < best:
            best = img
    return best


def atoms(kind, n, p):
    sqs = [(f, r) for f in range(n) for r in RANKS]
    seen = set()
    for S in itertools.combinations(sqs, p):
        if len({f for f, _ in S}) != n:
            continue
        for cols in itertools.product((0, 1), repeat=p):
            W = tuple(sorted(s for s, c in zip(S, cols) if c == 0))
            B = tuple(sorted(s for s, c in zip(S, cols) if c == 1))
            if not W or not B:
                continue
            if pg.has_passer(kind, n, W, B, None, "W") or pg.has_passer(kind, n, W, B, None, "B"):
                continue
            rep = orbit_rep(kind, n, W, B)
            if rep in seen:
                continue
            seen.add(rep)
            yield rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule", default="count")
    ap.add_argument("--ep", type=int, default=1)
    ap.add_argument("--epaware", type=int, default=0)
    ap.add_argument("--split", type=int, default=1)
    ap.add_argument("--maxp", type=int, default=5)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    pg.RULE, pg.EP, pg.EPAWARE, pg.SPLIT = a.rule, bool(a.ep), bool(a.epaware), bool(a.split)
    pg.reset()
    t0 = time.time()
    rows = []          # (kind, n, p, W, B, gid)
    for kind, widths in (("F", range(1, 6)), ("C", range(3, 6))):
        for n in widths:
            for p in range(max(2, n), a.maxp + 1):
                t = time.time()
                c = 0
                for W, B in atoms(kind, n, p):
                    g = pg.root_value(kind, n, W, B)
                    rows.append((kind, n, p, W, B, g))
                    c += 1
                print(f"{kind}{n} p={p}: {c} atoms, {time.time()-t:.1f}s, nodes={len(pg._memo)}",
                      flush=True)
    # nimbers among atoms
    nim_atoms = []
    nim_count = {}
    mismatch = 0
    for kind, n, p, W, B, g in rows:
        k = cg.nimber_eq(g, 32)
        if k != cg.nimber_of(g, 32):
            mismatch += 1
        if k is not None:
            nim_count[k] = nim_count.get(k, 0) + 1
            if k >= 2:
                nim_atoms.append((kind, n, p, pg.fmt(W, B), k))
    # two-component sums (2+2 and 2+3 pawns), on distinct values
    vals = {}
    for kind, n, p, W, B, g in rows:
        if kind == "F":
            vals.setdefault(p, {}).setdefault(g, (n, pg.fmt(W, B)))
    pair_nims = []
    pair_checked = 0
    for p1, p2 in ((2, 2), (2, 3)):
        if p1 + p2 > a.maxp:
            continue
        for g1, w1 in vals.get(p1, {}).items():
            # negatives: also include colour-reversed atoms -> the orbit list above
            for g2, w2 in vals.get(p2, {}).items():
                s = cg.add(g1, g2)
                pair_checked += 1
                k = cg.nimber_eq(s, 32)
                if k != cg.nimber_of(s, 32):
                    mismatch += 1
                if k is not None and k >= 2:
                    pair_nims.append((p1, p2, w1, w2, k))
    # distinct values
    distinct = len({g for *_, g in rows})
    out = {
        "settings": vars(a),
        "atoms": len(rows),
        "atoms_by_class": {f"{k}{n}p{p}": sum(1 for r in rows if r[:3] == (k, n, p))
                           for k, n, p in sorted({r[:3] for r in rows})},
        "distinct_atom_values": distinct,
        "nimber_atom_counts": {str(k): v for k, v in sorted(nim_count.items())},
        "nimber_atoms_k_ge_2": nim_atoms,
        "pair_sums_checked": pair_checked,
        "pair_sums_nimber_k_ge_2": pair_nims,
        "id_vs_order_nimber_mismatches": mismatch,
        "seconds": round(time.time() - t0, 1),
        "nodes": len(pg._memo),
        "cg_nodes": len(cg._L),
    }
    with open(a.out, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    # also dump per-atom nimber index / outcome for cross-comparison
    with open(a.out.replace(".json", "_atoms.tsv"), "w") as fh:
        for kind, n, p, W, B, g in rows:
            k = cg.nimber_of(g, 32)
            fh.write(f"{kind}\t{n}\t{p}\t{pg.fmt(W, B)}\t{'' if k is None else k}\t{cg.outcome(g)}\n")
    print(json.dumps({k: v for k, v in out.items() if k != "atoms_by_class"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
