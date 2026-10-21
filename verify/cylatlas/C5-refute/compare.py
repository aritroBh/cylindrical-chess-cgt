"""Compare the worker's atlas (values.jsonl, count rule / e.p. on) with the
independent scan on nimber-valued single components.

Every worker row with ncomp == 1 is mapped to an atom (ring if ring == 1,
otherwise the occupied files cut out as a flat strip) and reduced to the
same orbit representative scan.py uses. Rows with ncomp == 2 are checked for
nimber strings.

Run: ../../../.venv/bin/python compare.py ../../../atlas/cylinder/values.jsonl scan5_count_ep1_aw0_split1_atoms.tsv ../../../atlas/cylinder/value_index.jsonl
"""
import json
import sys

import pg
from scan import orbit_rep


def atom_of(board, n, W, B):
    files = sorted({f for f, _ in W} | {f for f, _ in B})
    if board == "cyl" and len(files) == n:
        return ("C", n) + orbit_rep("C", n, W, B)
    occ = set(files)
    if board == "cyl":
        e = next(f for f in range(n) if f not in occ)
        order = [(e + 1 + i) % n for i in range(n - 1)]
    else:
        order = list(range(n))
    run = [f for f in order if f in occ]
    # single component => occupied files are consecutive in `order`
    idx = [order.index(f) for f in run]
    assert idx == list(range(idx[0], idx[0] + len(idx))), (board, n, W, B)
    fmap = {f: i for i, f in enumerate(run)}
    W2 = tuple(sorted((fmap[f], r) for f, r in W))
    B2 = tuple(sorted((fmap[f], r) for f, r in B))
    w = len(run)
    return ("F", w) + orbit_rep("F", w, W2, B2)


def main(values_path, atoms_tsv, index_path):
    vidx = {}
    for line in open(index_path):
        d = json.loads(line)
        vidx[d["vid"]] = (d["show"], d["out"])
    mine = {}
    for line in open(atoms_tsv):
        kind, n, p, pos, k, outc = line.rstrip("\n").split("\t")
        W, B = pg.parse(pos)
        mine[(kind, int(n)) + orbit_rep(kind, int(n), W, B)] = (k, outc)
    theirs = {}
    conflicts = 0
    multi_nim = {}
    rows = 0
    for line in open(values_path):
        d = json.loads(line)
        rows += 1
        W, B = pg.parse(d["pos"])
        v, outc = vidx[d["vid"]]
        if d["ncomp"] != 1:
            if v.startswith("*") or v == "0":
                multi_nim[v] = multi_nim.get(v, 0) + 1
            continue
        key = atom_of(d["board"], d["n"], W, B)
        v = (v, outc)
        if key in theirs and theirs[key] != v:
            conflicts += 1
        theirs[key] = v
    def nim(v):
        v = v[0]
        if v == "0":
            return "0"
        if v == "*":
            return "1"
        if v.startswith("*") and v[1:].isdigit():
            return v[1:]
        return ""
    missing_in_mine = [k for k in theirs if k not in mine]
    missing_in_theirs = [k for k in mine if k not in theirs]
    disagree = []
    for k, v in theirs.items():
        if k in mine and nim(v) != mine[k][0]:
            disagree.append((k, v, mine[k]))
    print(f"worker rows read: {rows}")
    print(f"worker distinct atoms (ncomp=1): {len(theirs)}; inconsistent duplicates: {conflicts}")
    print(f"my atoms: {len(mine)}; atoms only in worker: {len(missing_in_mine)}; only in mine: {len(missing_in_theirs)}")
    print(f"nimber-status disagreements (0/*/*k vs other): {len(disagree)}")
    odis = [(k, v, mine[k]) for k, v in theirs.items() if k in mine and v[1] != mine[k][1]]
    print(f"outcome-class disagreements: {len(odis)}")
    for x in odis[:10]:
        print("   ", x)
    for x in disagree[:20]:
        print("   ", x)
    for x in missing_in_mine[:5]:
        print("   only-worker", x)
    for x in missing_in_theirs[:5]:
        print("   only-mine", x)
    print("worker multi-component rows with nimber value strings:", multi_nim)
    from collections import Counter
    print("worker atom nimber strings:", Counter(nim(v) for v in theirs.values() if nim(v)))
    print("my atom nimber indices:", Counter(m[0] for m in mine.values() if m[0]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
