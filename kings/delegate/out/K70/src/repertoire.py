"""Discover a sufficient move repertoire by removing families of Black or White moves."""

from zones import *
from ctypes import CDLL, c_int, c_uint64
from pathlib import Path
from collections import defaultdict
from itertools import groupby
import subprocess, sys, tempfile

here = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(dir=here) as directory:
    shared = Path(directory) / "reach.so"
    subprocess.run(
        [
            "c++",
            "-std=c++17",
            "-O2",
            "-shared",
            "-fPIC",
            str(here / "reach.cpp"),
            "-o",
            str(shared),
        ],
        check=True,
    )
    lib = CDLL(str(shared))
lib.node.argtypes = [c_int, c_uint64, c_uint64, c_uint64]
lib.edge.argtypes = [c_int, c_int, c_uint64, c_int]
lib.zone.restype = c_uint64
lib.reset_graph()
roots = [diag(0, 41, w, 49, 42) for w in (10, 18, 26)]
targets = [geom(d)[0] & ~(bit(sq("b4")) if d[2] == 26 else 0) for d in roots]
hold = "--draw" in sys.argv
if hold:
    from defence import geom, edges, fortress

    roots = [diag(0, sq("b4"), sq("c5"), 49, 42)]
    targets = [bit(41)]
ds = roots.copy()
ids = {d: i for i, d in enumerate(ds)}
action = {}
es = []
for i, d in enumerate(ds):
    row = []
    legal = 0
    for m, h, mask_, king in () if hold and d[3] == d[4] == X else edges(d):
        z = -1
        if h is not None:
            if h not in ids:
                ids[h] = len(ds)
                ds.append(h)
            z = ids[h]
        row.append((m, z, mask_, king))
        legal |= dilation(mask_) if king else mask_
    es.append(row)
    zone, check, fixedcheck = geom(d)
    base = (
        zone
        if hold and d[3] == d[4] == X
        else (zone & ~legal if hold and d[0] and not fixedcheck else 0)
    )
    if hold:
        base |= fortress(d)
    assert lib.node(d[0], zone, zone if hold else zone & (legal | check), base) == i
for i, row in enumerate(es):
    for m, z, a, king in row:
        ident = lib.edge(i, z, a, king)
        if ident:
            action[ident] = (i, m, z, a)


def weight(d):
    t, j, w, b, c, e = d
    return (
        (0 if w == X else 8 - w // 8)
        + (0 if b == X else b // 8)
        + (0 if c == X else c // 8),
        e != X,
    )


order = sorted(range(len(ds)), key=lambda i: weight(ds[i]))
lib.set_order((c_int * len(order))(*order), len(order))


def works():
    lib.run(hold)
    return all(lib.zone(i) & a == a for i, a in enumerate(targets))


def read_policy(path):
    keep = set()
    for line in path.read_text().splitlines():
        *l, m = line.split()
        keep.add((tuple(map(int, l)), m))
    return {a for a, (i, m, z, ma) in action.items() if (ds[i], m) in keep}


def prune():
    live = set(action)

    def drop(batch):
        batch = live.intersection(batch)
        if not batch:
            return True
        for a in batch:
            lib.toggle(a, 0)
        if works():
            live.difference_update(batch)
            return True
        for a in batch:
            lib.toggle(a, 1)
        return False

    def descend(els):
        if drop(x for g in els for x in g):
            return
        if len(els) > 1:
            mid = len(els) // 2
            descend(els[:mid])
            descend(els[mid:])

    def groups(key):
        g = defaultdict(list)
        for a in sorted(live):
            i, m, z, ma = action[a]
            t, j, w, b, c, e = ds[i]
            g[key(j, w, b, c, e, m)].append(a)
        return g

    def apply(key, sort):
        g = groups(key)
        ks = sorted(g, key=sort, reverse=True)
        descend([g[k] for k in ks])
        print("stage", len(live), flush=True)

    # First prune whole corridors, then pawn structures, king squares and actions.
    apply(lambda j, w, b, c, e, m: j % 8, lambda f: abs(f - 1.6))
    apply(
        lambda j, w, b, c, e, m: (b, c),
        lambda pair: (
            sum(p == X for p in pair),
            sum(1 for p in pair if p != X and p % 8 != 1),
            min(pair),
        ),
    )
    apply(
        lambda j, w, b, c, e, m: (j, b, c),
        lambda key: (
            abs(key[0] % 8 - 1.6),
            abs((key[0] // 8) - min((p // 8 for p in key[1:] if p < X), default=0)),
        ),
    )
    apply(lambda j, w, b, c, e, m: (j, b, c, m), lambda key: (key[-1][0] == "K", key))
    apply(
        lambda j, w, b, c, e, m: (j, w, b, c, e, m),
        lambda key: (key[-1][0] == "K", key),
    )
    assert works()
    assert live == read_policy(here / ("draw-policy.txt" if hold else "policy.txt"))
    print("Reproduced the saved move repertoire.")


if __name__ == "__main__":
    print("diagrams", len(ds), "actions", len(action), flush=True)
    assert works()
    prune()
