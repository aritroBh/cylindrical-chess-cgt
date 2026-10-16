"""Full traversal of the 7.3 {c,d} game tree with the independent rules in indep_tiny.py:
count nodes, race nodes, double-step availability, e.p. captures; identify the exact c3-c4 option.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/diagrams/N1-reproduce/indep_tree_stats.py
"""
import sys
sys.path.insert(0, "verify/diagrams/N1-reproduce")
import indep_tiny as T

root = "W: c1 c3 d3 / B: c2 d4 d5 d6"
for wrap in (False, True):
    for ep in (True, False):
        T.CFG.update(wrap=wrap, ep=ep, race="count"); T.reset()
        seen, stack, terms = set(), [T.pawnnode(T.parse(root))], {}
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            if x[0] == "n":
                terms[x[1]] = terms.get(x[1], 0) + 1
                continue
            L, R = T.opts(x)
            stack.extend(L + R)
        pawn_nodes = sum(1 for x in seen if x[0] == "p")
        print(f"wrap={wrap} ep={ep}: pawn nodes {pawn_nodes}, terminal values {sorted(terms)}, "
              f"race nodes {len(T.STATS['races'])}, double-step-available nodes {len(T.STATS['doubles'])}, "
              f"e.p. captures {len(T.STATS['ep_caps'])}")
        for s in sorted(T.STATS["doubles"]):
            print("    double step available in:", s)
# exact value of the c3-c4 option: compare against {0 | -k*} and {0 | -k} for integers k
T.CFG.update(wrap=False, ep=True, race="count"); T.reset()
c4 = T.pawnnode(T.parse("W: c1 c4 d3 / B: c2 d4 d5 d6"))
hits = [k for k in range(0, 300) if T.eq(c4, T.G([T.ZERO], [T.G([T.N(-k)], [T.N(-k)])]))]
print("c3-c4 option equals {0 | -k*} for k in", hits)
rx = T.pawnnode(T.parse("W: c1 d3 / B: c2 c4 d4 d6"))
print("after c3-c4 dxc4: equals -k* for k in", [k for k in range(0, 300) if T.eq(rx, T.G([T.N(-k)], [T.N(-k)]))],
      "; equals -k for k in", [k for k in range(0, 300) if T.eq(rx, T.N(-k))])
