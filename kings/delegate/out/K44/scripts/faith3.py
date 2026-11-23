import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lk3 import LK, parse_cfg
def faithful(g):
    n = len(g.pawns); full = g.full
    reach = {full}; st = [full]
    while st:
        m = st.pop()
        if not g.okm[m]: continue
        for i in range(n):
            if (m >> i) & 1:
                m2 = m & ~(1 << i)
                if m2 not in reach: reach.add(m2); st.append(m2)
    for m in reach:
        if not g.okm[m]: continue
        for i, (c, f, r) in enumerate(g.pawns):
            if not (m >> i) & 1: continue
            dr = 1 if c == 0 else -1
            if (f, r + dr) not in g.pawnsq[m]: return False
            for d in (-1, 1):
                gf = g.nbf(f, d)
                if gf is None: continue
                o = g.pawnsq[m].get((gf, r + dr))
                if o and o[0] != c: return False
    return True
if __name__ == '__main__':
    board, cfg = sys.argv[1], sys.argv[2]
    W, H = [int(v) for v in board.split(':')[1].split('x')]
    g = LK(W, H, True, parse_cfg(cfg))
    print(board, cfg, 'faithful', faithful(g))
