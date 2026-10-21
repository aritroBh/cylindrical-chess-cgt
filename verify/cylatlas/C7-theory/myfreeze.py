"""C7-theory: independent re-implementation of the trebuchet freeze test
(does not import cylcgt or atlas/cylinder/freeze.py).

Pawn game on a flat strip of width w, 8 ranks: single and double steps, diagonal
captures, en passant (right lasts one move).  BFS over every configuration
reachable with either side moving in any order; expansion stops at a node where
some side has a passed pawn (textbook test: no enemy pawn ahead on own or
adjacent file), but those nodes are still checked.

Trebuchet on files f,g,h (pawn file g = 6): W P(g,r), B P(g,r+1), WK (g+s, r+1),
BK (g-s, r), s = +-1, r = 2..6.  Component placed on files a..e (offset o,
optional mirror).  A placement FAILS if at some reachable node a pawn stands on a
square the enemy king attacks, or attacks the enemy king's square.

Also reports, per placement, the smallest BFS depth of a failing node and whether
any failing node is non-terminal, so one can see how early the freeze breaks.

Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
     .venv/bin/python verify/cylatlas/C7-theory/myfreeze.py ["W: a2 c2 / B: b7 d7" ...]
"""
import sys
from collections import deque

F = "abcdefgh"


def parse(t):
    w, b = t.split("/")
    g = lambda s: frozenset((F.index(x[0]), int(x[1:])) for x in s.split(":")[1].split())
    return g(w), g(b)


def passed(W, B, side):
    mine, th = (W, B) if side == "W" else (B, W)
    for f, r in mine:
        if side == "W":
            if not any(abs(g - f) <= 1 and s > r for g, s in th):
                return True
        else:
            if not any(abs(g - f) <= 1 and s < r for g, s in th):
                return True
    return False


def gen(W, B, ep, side, w):
    mine, th = (W, B) if side == "W" else (B, W)
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else 7
    occ = W | B
    out = []
    for f, r in mine:
        rest = mine - {(f, r)}
        r1 = r + d
        if not 1 <= r1 <= 8:
            continue
        if (f, r1) not in occ:
            out.append((rest | {(f, r1)}, th, None))
            if r == start and (f, r + 2 * d) not in occ:
                out.append((rest | {(f, r + 2 * d)}, th, ((f, r1), (f, r + 2 * d), "B" if side == "W" else "W")))
        for g in (f - 1, f + 1):
            if not 0 <= g < w:
                continue
            if (g, r1) in th:
                out.append((rest | {(g, r1)}, th - {(g, r1)}, None))
            elif ep and ep[2] == side and ep[0] == (g, r1):
                out.append((rest | {(g, r1)}, th - {ep[1]}, None))
    res = []
    for m, t, e in out:
        res.append((frozenset(m), frozenset(t), e) if side == "W" else (frozenset(t), frozenset(m), e))
    return res


def reach(W, B, w):
    start = (W, B, None)
    depth = {start: 0}
    dq = deque([start])
    while dq:
        n = dq.popleft()
        Wn, Bn, ep = n
        if passed(Wn, Bn, "W") or passed(Wn, Bn, "B"):
            continue
        for side in "WB":
            for c in gen(Wn, Bn, ep, side, w):
                if c not in depth:
                    depth[c] = depth[n] + 1
                    dq.append(c)
    return depth


def katt(k, wrap):
    f, r = k
    s = set()
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df or dr:
                g = f + df
                if wrap:
                    g %= 8
                if 0 <= g < 8 and 1 <= r + dr <= 8:
                    s.add((g, r + dr))
    return s


def patt(p, col, wrap):
    f, r = p
    q = r + (1 if col == "W" else -1)
    s = set()
    for g in (f - 1, f + 1):
        if wrap:
            g %= 8
        if 0 <= g < 8:
            s.add((g, q))
    return s


def run(text, verbose=True):
    W, B = parse(text)
    lo = min(f for f, _ in W | B)
    W = frozenset((f - lo, r) for f, r in W)
    B = frozenset((f - lo, r) for f, r in B)
    w = max(f for f, _ in W | B) + 1
    nodes = reach(W, B, w)
    configs = {(a, b) for a, b, _ in nodes}
    res = {}
    for wrap in (False, True):
        ok = 0
        tot = 0
        details = []
        for o in range(0, 5 - w + 1):
            for mir in (False, True):
                for s in (1, -1):
                    for r in range(2, 7):
                        tot += 1
                        wk = ((6 + s) % 8, r + 1)
                        bk = ((6 - s) % 8, r)
                        wka, bka = katt(wk, wrap), katt(bk, wrap)
                        mp = (lambda c: o + (w - 1 - c)) if mir else (lambda c: o + c)
                        fail_d = None
                        nonterm = False
                        for (Wn, Bn, ep), dep in nodes.items():
                            bad = any(((mp(f), q) in wka) or (wk in patt((mp(f), q), "B", wrap)) for f, q in Bn) or \
                                  any(((mp(f), q) in bka) or (bk in patt((mp(f), q), "W", wrap)) for f, q in Wn)
                            if bad:
                                term = passed(Wn, Bn, "W") or passed(Wn, Bn, "B")
                                if not term:
                                    nonterm = True
                                if fail_d is None or dep < fail_d:
                                    fail_d = dep
                        if fail_d is None:
                            ok += 1
                        details.append((o, mir, s, r, fail_d, nonterm))
        res["cyl8" if wrap else "flat8"] = (ok, tot, details)
    if verbose:
        print(text, "width", w, "nodes(with ep tag)", len(nodes), "configs", len(configs))
        for k in ("flat8", "cyl8"):
            ok, tot, det = res[k]
            print(f"  {k}: pass {ok}/{tot}")
            if k == "cyl8":
                md = [d[4] for d in det if d[4] is not None]
                print("   min failing depth over placements:", sorted(set(md)) if md else None,
                      "; placements whose failures are all at terminal nodes:",
                      sum(1 for d in det if d[4] is not None and not d[5]))
    return res


if __name__ == "__main__":
    for t in (sys.argv[1:] or ["W: a2 c2 / B: b7 d7"]):
        run(t)
