"""For the cylinder placements of W a2 c2 / B b7 d7 whose freeze failures are all at
terminal (passed-pawn) nodes, classify each failing terminal node:
  who has a passer (W / B / race), offending pawn colour, whether the offending pawn is
  itself a passer, and whether it is capturable (on a square the enemy king attacks) and
  undefended by its own pawns.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/cylatlas/C7-theory/terminal_classify.py"""
import sys, os
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import myfreeze as M
F = "abcdefgh"
W0, B0 = M.parse("W: a2 c2 / B: b7 d7")
w = 4
nodes = M.reach(W0, B0, w)
def pawn_passed(p, mine, th, side):
    f, r = p
    if side == "W":
        return not any(abs(g - f) <= 1 and s > r for g, s in th)
    return not any(abs(g - f) <= 1 and s < r for g, s in th)
tot = Counter()
for o in (0, 1):
    for mir in (False, True):
        for s in (1, -1):
            for r in range(2, 7):
                wk = ((6 + s) % 8, r + 1); bk = ((6 - s) % 8, r)
                wka, bka = M.katt(wk, True), M.katt(bk, True)
                mp = (lambda c, o=o: o + (w - 1 - c)) if mir else (lambda c, o=o: o + c)
                fails = []
                nonterm = False
                for (Wn, Bn, ep), dep in nodes.items():
                    Wm = {(mp(f), q) for f, q in Wn}; Bm = {(mp(f), q) for f, q in Bn}
                    off = []
                    for p in Bm:
                        if p in wka or wk in M.patt(p, "B", True):
                            off.append(("B", p))
                    for p in Wm:
                        if p in bka or bk in M.patt(p, "W", True):
                            off.append(("W", p))
                    if not off:
                        continue
                    wp, bp = M.passed(Wn, Bn, "W"), M.passed(Wn, Bn, "B")
                    if not (wp or bp):
                        nonterm = True
                        break
                    who = "race" if (wp and bp) else ("W" if wp else "B")
                    for col, p in off:
                        mine, th = (Wm, Bm) if col == "W" else (Bm, Wm)
                        isp = pawn_passed(p, mine, th, col)
                        ka = wka if col == "B" else bka
                        d = -1 if col == "W" else 1  # a defender stands one rank behind
                        defended = any(((p[0] + df) % 8, p[1] - (1 if col == "W" else -1)) in mine for df in (-1, 1))
                        capt = p in ka and not defended
                        fails.append((who, col, isp, capt))
                if nonterm or not fails:
                    continue
                c = Counter(fails)
                tot.update(c)
                print(f"o={o} mir={mir!s:5} WK {F[wk[0]]}{wk[1]} BK {F[bk[0]]}{bk[1]}: {len(fails)} offending (node,pawn) pairs;",
                      " ".join(f"[passer={a} pawn={b} pawn_is_passer={x} capturable_undefended={y}]x{n}" for (a, b, x, y), n in sorted(c.items())))
print("TOTAL over terminal-only placements:", dict(tot))
