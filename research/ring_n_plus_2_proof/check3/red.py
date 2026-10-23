# copy of research/ring_family_proof/verify/red.py (T50 verifier's independent engine, written from the rules, not from rg.c) with the family P added; see ../run_check3.sh
import sys
from collections import deque
from eng import *

def build(pos0, cap=200000):
    """reduced game graph. node = (pos, ep). returns dict node->(info) with edges."""
    ids = {(pos0, None): 0}
    order = [(pos0, None)]
    info = {}
    q = deque([(pos0, None)])
    while q:
        nd = q.popleft()
        pos, ep = nd
        rec = {}
        for side in 'WB':
            cl = classify_moves(pos, ep, side)
            T = sorted({(np_, ne) for k, np_, ne in cl if k == 'T'}, key=repr)
            K = sorted({(np_, ne) for k, np_, ne in cl if k == 'K'}, key=repr)
            rec[side] = (T, K, sum(1 for k, _, _ in cl if k in 'LP'))
            for c in K:
                if c not in ids:
                    ids[c] = len(ids); order.append(c); q.append(c)
                    if len(ids) > cap: raise RuntimeError('cap')
        info[nd] = rec
    return ids, order, info

def solve_graph(ids, order, info, hs=(0,1,2,3)):
    memo = {}
    def win(nd, h, mover):
        key = (nd, h, mover)
        if key in memo: return memo[key]
        T, K, _ = info[nd][mover]
        res = bool(T)
        if not res:
            y = other(mover)
            for c in K:
                if not win(c, h, y): res = True; break
        if not res:
            for h2 in range(h):
                if not win(nd, h2, other(mover)): res = True; break
        memo[key] = res
        return res
    sig = ''
    s0 = order[0]
    for h in hs:
        a = win(s0, h, 'W'); b = win(s0, h, 'B')
        sig += {(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(a, b)]
    return sig

def stats(ids, order, info, pos0):
    n = len(pos0)
    nT = sum(len(info[nd][s][0]) for nd in order for s in 'WB')
    nK = sum(len(info[nd][s][1]) for nd in order for s in 'WB')
    flags = sum(1 for nd in order if nd[1] is not None)
    diff_files = set()
    for pos, ep in order:
        for f in range(n):
            if pos[f] != pos0[f]: diff_files.add(f)
    return dict(nodes=len(order), K_edges=nK, T_edges=nT, flagged=flags, touched=sorted(diff_files))

if __name__ == '__main__':
    kind = sys.argv[1]
    for n in map(int, sys.argv[2:]):
        pos0 = ring(kind, n)
        ids, order, info = build(pos0)
        st = stats(ids, order, info, pos0)
        print(kind, n, st['nodes'], 'K-edges', st['K_edges'], 'T-edges', st['T_edges'], 'flagged', st['flagged'],
              'touched', st['touched'], 'sig', solve_graph(ids, order, info), flush=True)
