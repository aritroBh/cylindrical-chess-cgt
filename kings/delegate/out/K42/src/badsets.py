#!/usr/bin/env python3
"""bad squares for the certificate test of Proposition 8.1 / 8.1' with s = White.
usage: badsets.py W H CTXFILE OUT_P3 OUT_P3W
G-closure: from G (White to move, a loss for White in the pawn game), all White pawn moves, then every winning
Black reply.  X = squares holding a context pawn in a position of the closure (White-to-move positions and the
positions right after a White move); E = squares passed over by a double step made in that play; A = squares
attacked by a Black context pawn in those positions.  P3 bad set: X and its king-neighbourhood (Proposition 8.1);
P3W bad set: X, E and A (Proposition 8.1')."""
import sys, functools
sys.path.insert(0, __import__("os").path.dirname(__file__))
W, H = int(sys.argv[1]), int(sys.argv[2])
import importlib.util
def nb(f, d): return (f + d) % W
def name(s): return "abcdefghi"[s[0]] + str(s[1] + 1)
def sq(t): return ("abcdefghi".index(t[0]), int(t[1:]) - 1)
def moves(ws, bs, color, ep):
    own, en = (ws, bs) if color == "w" else (bs, ws); dr = 1 if color == "w" else -1
    last = H - 1 if color == "w" else 0; start = 1 if color == "w" else H - 2
    occ = ws | bs
    for (f, r) in own:
        t = (f, r + dr)
        if t not in occ:
            yield (own - {(f, r)}) | {t}, en, None, t[1] == last, None
            if r == start:
                t2 = (f, r + 2 * dr)
                if t2 not in occ:
                    epn = t if any((nb(f, d), r + 2 * dr) in en for d in (-1, 1)) else None
                    yield (own - {(f, r)}) | {t2}, en, epn, t2[1] == last, t
        for d in (-1, 1):
            c = (nb(f, d), r + dr)
            if c in en: yield (own - {(f, r)}) | {c}, en - {c}, None, c[1] == last, None
            elif ep is not None and c == ep: yield (own - {(f, r)}) | {c}, en - {(c[0], r)}, None, False, None
def tow(color, own2, en2): return (own2, en2) if color == "w" else (en2, own2)
@functools.lru_cache(maxsize=None)
def wins(ws, bs, color, ep):
    for own2, en2, epn, pr, _ in moves(ws, bs, color, ep):
        assert not pr
        w2, b2 = tow(color, own2, en2)
        if not wins(w2, b2, "b" if color == "w" else "w", epn): return True
    return False
def attB(bs): return {(nb(f, d), r - 1) for (f, r) in bs for d in (-1, 1)}
o3 = open(sys.argv[4], "w"); o3w = open(sys.argv[5], "w")
for line in open(sys.argv[3]):
    t = line.split(); cid = t[0]
    ws = frozenset(sq(x[1:]) for x in t[1:] if x[0] == "P"); bs = frozenset(sq(x[1:]) for x in t[1:] if x[0] == "p")
    assert not wins(ws, bs, "w", None)
    X, E, A = set(), set(), set(); seen = set(); stack = [(ws, bs, None)]
    while stack:
        st = stack.pop()
        if st in seen: continue
        seen.add(st); w, b, ep = st
        X |= w | b; A |= attB(b)
        for own2, en2, epn, pr, passed in moves(w, b, "w", ep):
            w2, b2 = tow("w", own2, en2)
            if passed: E.add(passed)
            X |= w2 | b2; A |= attB(b2)
            for o3_, e3_, epn3, pr3, passed3 in moves(w2, b2, "b", epn):
                b3, w3 = o3_, e3_
                if not wins(w3, b3, "w", epn3):
                    if passed3: E.add(passed3)
                    stack.append((w3, b3, epn3))
    N = {((f + df) % W, r + dr) for (f, r) in X for df in (-1, 0, 1) for dr in (-1, 0, 1) if 0 <= r + dr < H}
    o3.write(cid + " " + " ".join(sorted(name(s) for s in X | N)) + "\n")
    B = {s for s in X | E | A if 0 <= s[1] < H}
    o3w.write(cid + " " + " ".join(sorted(name(s) for s in B)) + "\n")
