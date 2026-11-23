#!/usr/bin/env python3
"""Promotion-free contexts. usage: ctx.py W H FILES(e.g. 4,5,6) MAXW MAXB OUT
A context G is a set of pawns on the context files (ranks 2..H-1). It is promotion-free if no sequence of legal
pawn moves of G alone (both colours, any order, captures and e.p. captures included) promotes. Its pawn game is
normal play (a side with no pawn move loses), White or Black to move, e.p. included. Writes, for every
promotion-free G whose pawn game is a loss for White to move (zero or negative class), a line
'<id> <class> <tokens>' (class Z: Black to move loses too; N: Black to move wins)."""
import sys, itertools, functools
W, H = int(sys.argv[1]), int(sys.argv[2]); FILES = [int(x) for x in sys.argv[3].split(",")]
MAXW, MAXB, OUT = int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
def nb(f, d): return (f + d) % W   # cylinder
def name(s): return "abcdefghi"[s[0]] + str(s[1] + 1)
def moves(ws, bs, color, ep):
    """yield (ws', bs', ep', promotes) for pawn moves of colour; ep = e.p. target usable by this colour or None"""
    own, en = (ws, bs) if color == "w" else (bs, ws); dr = 1 if color == "w" else -1
    last = H - 1 if color == "w" else 0; start = 1 if color == "w" else H - 2
    occ = ws | bs
    for (f, r) in own:
        t = (f, r + dr)
        if t not in occ:
            yield (own - {(f, r)}) | {t}, en, t if False else None, t[1] == last
            if r == start:
                t2 = (f, r + 2 * dr)
                if t2 not in occ:
                    epn = t if any((nb(f, d), r + 2 * dr) in en for d in (-1, 1)) else None
                    yield (own - {(f, r)}) | {t2}, en, epn, t2[1] == last
        for d in (-1, 1):
            c = (nb(f, d), r + dr)
            if c in en:
                yield (own - {(f, r)}) | {c}, en - {c}, None, c[1] == last
            elif ep is not None and c == ep:
                yield (own - {(f, r)}) | {c}, en - {(c[0], r)}, None, False
def tow(color, own2, en2): return (own2, en2) if color == "w" else (en2, own2)
def promfree(ws, bs):
    seen = set(); stack = [(ws, bs, None, None)]   # ep, colour allowed to use it
    while stack:
        st = stack.pop()
        if st in seen: continue
        seen.add(st)
        w, b, ep, epc = st
        for color in "wb":
            for own2, en2, epn, pr in moves(w, b, color, ep if epc == color else None):
                if pr: return False
                w2, b2 = tow(color, own2, en2)
                stack.append((w2, b2, epn, ("b" if color == "w" else "w") if epn else None))
    return True
@functools.lru_cache(maxsize=None)
def wins(ws, bs, color, ep):
    """normal play: does the side to move win?"""
    for own2, en2, epn, pr in moves(ws, bs, color, ep):
        assert not pr
        w2, b2 = tow(color, own2, en2)
        if not wins(w2, b2, "b" if color == "w" else "w", epn): return True
    return False
sqs = [(f, r) for f in FILES for r in range(1, H - 1)]
n = 0; cnt = {}
with open(OUT, "w") as out:
    for a in range(MAXW + 1):
        for ws in itertools.combinations(sqs, a):
            for b in range(MAXB + 1):
                for bs in itertools.combinations(sqs, b):
                    if set(ws) & set(bs) or (a + b == 0): continue
                    W_, B_ = frozenset(ws), frozenset(bs)
                    if not promfree(W_, B_): cnt["race"] = cnt.get("race", 0) + 1; continue
                    ww = wins(W_, B_, "w", None); bw = wins(W_, B_, "b", None)
                    cls = {(False, False): "Z", (False, True): "N", (True, True): "F", (True, False): "P"}[(ww, bw)]
                    cnt[cls] = cnt.get(cls, 0) + 1
                    if not ww:
                        n += 1
                        out.write(f"c{n}:{cls} " + " ".join(["P" + name(s) for s in sorted(ws)] + ["p" + name(s) for s in sorted(bs)]) + "\n")
print(cnt, "written", n)
