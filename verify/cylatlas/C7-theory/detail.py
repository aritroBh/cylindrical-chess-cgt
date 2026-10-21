"""List per-placement freeze results on the 8-file cylinder for W a2 c2 / B b7 d7,
with the first failing node, and whether all failures are at terminal (passer) nodes.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/cylatlas/C7-theory/detail.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import myfreeze as M
F = "abcdefgh"
t = sys.argv[1] if len(sys.argv) > 1 else "W: a2 c2 / B: b7 d7"
res = M.run(t, verbose=False)
for o, mir, s, r, d, nonterm in res["cyl8"][2]:
    wk = (F[(6 + s) % 8], r + 1); bk = (F[(6 - s) % 8], r)
    tag = "PASS" if d is None else ("fails only at terminal nodes" if not nonterm else "fails at a non-terminal node")
    print(f"o={o} mirror={mir!s:5} WK {wk[0]}{wk[1]} BK {bk[0]}{bk[1]}  first-fail-depth={d}  {tag}")
