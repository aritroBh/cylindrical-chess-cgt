"""Cross-check ring lists against the C7 scan (research/star26_rings/c7): is each ring's scanner chunk finished, and is it a hit?"""
import sys, os, itertools, math, glob
sys.path.insert(0, "research/ring_family")
from ringlib import *
SC = "research/star26_rings/c7"
def to_masks(ring):
    wm = bm = 0
    for f, (a, b) in enumerate(ring):
        for r in a: wm |= 1 << ((r - 1) * 8 + f)
        for r in b: bm |= 1 << ((r - 1) * 8 + f)
    return wm, bm
def transform(m, shift, refl, W):
    out = 0
    for s in range(64):
        if m >> s & 1:
            f, r = s & 7, (s >> 3) + 1
            if refl: f = W - 1 - f
            f = (f + shift) % W
            out |= 1 << ((r - 1) * 8 + f)
    return out
def scanner_canon(wm, bm, W):
    best = (wm, bm)
    for v in range(2 * W):
        refl, shift = v // W, v % W
        t = (transform(wm, shift, refl, W), transform(bm, shift, refl, W))
        if t < best: best = t
    return best
def chunk_of(wm, nw, W, N):
    wc = [(f, r) for f in range(W) for r in range(2, 7)]
    pos = {(f, r): i for i, (f, r) in enumerate(wc)}
    idx = sorted(pos[((s & 7), (s >> 3) + 1)] for s in range(64) if wm >> s & 1)
    n = len(wc)
    # rank of the combination idx among combinations of nw out of n (lexicographic)
    rank = 0; prev = -1
    for j, c in enumerate(idx):
        for x in range(prev + 1, c):
            rank += math.comb(n - x - 1, nw - j - 1)
        prev = c
    total = math.comb(n, nw)
    for i in range(N):
        lo = i * total // N; hi = (i + 1) * total // N
        if lo <= rank < hi: return i
def info(ring):
    W = len(ring)
    variants = [ring, colour_reverse(ring)]
    out = []
    for v in variants:
        wm, bm = to_masks(v)
        nw, nb = bin(wm).count("1"), bin(bm).count("1")
        if nw > nb: continue
        cw, cb = scanner_canon(wm, bm, W)
        N = 1024 if (nw, nb) in ((5, 5), (4, 6)) else 256 if (nw, nb) == (3, 7) else 64 if (nw, nb) == (2, 8) else 16
        i = chunk_of(cw, nw, W, N)
        d = f"{SC}/p10_{nw}_{nb}"
        done = os.path.exists(f"{d}/c{i}of{N}.summary.txt")
        hit = False
        if done:
            hits = open(f"{d}/c{i}of{N}.hits.tsv").read()
            from ringlib import to_text
            pos = None
            # render scanner canonical in text form
            ws = [f"{chr(97+(s&7))}{(s>>3)+1}" for s in range(64) if cw >> s & 1]
            bs = [f"{chr(97+(s&7))}{(s>>3)+1}" for s in range(64) if cb >> s & 1]
            key = "W: " + " ".join(sorted(ws, key=lambda t: (t[0], int(t[1:])))) + " / B: " + " ".join(sorted(bs, key=lambda t: (t[0], int(t[1:]))))
            hit = any(l.startswith(key + "\t") for l in hits.split("\n"))
        out.append((nw, nb, i, N, done, hit))
    return out
if __name__ == "__main__":
    for line in sys.stdin:
        c = line.strip()
        if not c: continue
        print(c, "->", info(from_cstr(c)))
