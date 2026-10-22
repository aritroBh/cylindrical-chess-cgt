#!/usr/bin/env python3
"""Colour-reversal consistency of the scans: swapping colours and flipping ranks maps a root of split (nw,nb) to one of (nb,nw) and
exchanges L<->R, keeps N,P and the nimber (a nimber is its own negative).  Compare the outcome x nimber histograms of the twin splits."""
import re, glob, collections
H = {}
for f in glob.glob("scan/*.summary"):
    m = re.match(r"scan/w(\d+)p(\d+)_(\d+)_(\d+)\.summary", f); key = tuple(map(int, m.groups()))
    h = collections.Counter()
    for l in open(f):
        mm = re.match(r"outcome=(\w) nimber=(-?\d+) count=(\d+)", l)
        if mm: h[(mm.group(1), int(mm.group(2)))] += int(mm.group(3))
    H[key] = h
swap = {"L": "R", "R": "L", "N": "N", "P": "P"}
bad = n = 0
for (w, p, a, b), h in H.items():
    if a > b: continue
    t = H[(w, p, b, a)]
    h2 = collections.Counter({(swap[o], k): c for (o, k), c in t.items()})
    n += 1
    if a == b:
        # the (a,a) split maps to itself: compare after the swap too
        pass
    if h != h2: bad += 1; print("TWIN MISMATCH", (w, p, a, b))
print(f"twin split pairs compared: {n}, mismatching: {bad}")
