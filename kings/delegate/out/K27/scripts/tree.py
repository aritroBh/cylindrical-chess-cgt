"""tree.py -- extract small forced-win proof trees from pm.py.
usage: tree.py <position line> [maxplies]   (position: side to move wins; prints the tree)"""
import sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm
from functools import lru_cache
sys.setrecursionlimit(100000)

def wnode(p, n):
    """smallest tree (size, line) in which side to move wins within n plies; None if impossible"""
    return _w(p, n)

@lru_cache(maxsize=None)
def _w(p, n):
    if not pm.win(p, n): return None
    best = None
    for lab, q in pm.moves(p):
        if q == 'PROMO':
            return (1, [(lab + ' (promotes: wins)', None)])
    if n < 3: return None
    for lab, q in pm.moves(p):
        r = _l(q, n - 1)
        if r is not None:
            sz = 1 + r[0]
            if best is None or sz < best[0]:
                best = (sz, [(lab, r)])
    return best

@lru_cache(maxsize=None)
def _l(p, n):
    """tree in which side to move at p loses within n plies"""
    ms = pm.moves(p)
    if not ms:
        if pm.in_check(p, p[5]): return (1, 'MATE')
        return None
    if n < 2: return None
    tot = 1
    ch = []
    for lab, q in ms:
        if q == 'PROMO': return None
        r = _w(q, n - 1)
        if r is None: return None
        tot += r[0]
        ch.append((lab, q, r))
    return (tot, ch)

def pr(p, n, indent=0, out=None, mover=None):
    """print tree: p is a position where the side to move wins within n plies"""
    out = out if out is not None else []
    sp = '  ' * indent
    r = _w(p, n)
    if r is None:
        out.append(sp + '??? no win within %d' % n); return out
    lab, rr = r[1][0]
    if rr is None:
        out.append(sp + ('W:' if p[5]==0 else 'B:') + ' ' + lab); return out
    out.append(sp + ('W:' if p[5]==0 else 'B:') + ' ' + lab + '   [' + pm.show(pm.dict_move(p, lab) if hasattr(pm,'dict_move') else p) + ']' if False else sp + ('W:' if p[5]==0 else 'B:') + ' ' + lab)
    q = [qq for l, qq in pm.moves(p) if l == lab][0]
    if rr == 'MATE':
        out.append(sp + '  mate'); return out
    for l2, q2, r2 in rr[1]:
        out.append(sp + '  ' + ('b' if q[5]==1 else 'w') + ' ' + l2 + '  -> ' + pm.show(q2))
        pr(q2, n - 2, indent + 2, out)
    return out

if __name__ == '__main__':
    p = pm.parse(sys.argv[1])
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 21
    # minimal n
    for m in range(1, n + 1, 2):
        if pm.win(p, m): break
    r = _w(p, m)
    print('win within', m, 'plies; tree size', r[0])
    print('\n'.join(pr(p, m)))
