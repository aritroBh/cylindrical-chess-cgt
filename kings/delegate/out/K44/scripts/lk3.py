#!/usr/bin/env python3
"""K44 third implementation of the local king game LK (written for K44 from the definition in LOOPY section 8 item 3 and
the K20 summary; not from kg.cpp, lk.cpp or check_kg.py).

Definition used.
 Board: cyl:WxH (files wrap) or flat:WxH, files 0..W-1, ranks 1..H.  A configuration is a list of blocked pairs
 (f, r): white pawn on (f, r), black pawn on (f, r+1).  A node is (alive pawn set, white king, black king); kings stand
 on squares of the region, not on a pawn square, not adjacent to each other, a king is not attacked by an enemy pawn.
 A move is a king step to an adjacent square (not onto an own pawn, not adjacent to the enemy king, not attacked by an
 enemy pawn of the pawn set after the move); stepping onto an enemy pawn captures it.  After a capture, if some pawn is
 passed (no enemy pawn on its file or an adjacent file strictly ahead of it), the move ends the play: +  if only white
 pawns are passed, - if only black ones are passed.  A node whose mover has no move is a loss for the mover (empty option
 set).  Pawns never move.
Sums with a context K are the D-sum: a move to a terminal in either coordinate ends all play, a mover with no move in any
coordinate loses, infinite play is a draw.  outcome pair (White to move, Black to move) in {W,D,L} from White's side.
"""
import sys, itertools, collections

class LK:
    def __init__(self, W, H, wrap, pairs, region=None):
        self.W, self.H, self.wrap = W, H, wrap
        self.pairs = pairs
        self.pawns = []                       # (colour 0/1, f, r)
        for f, r in pairs:
            self.pawns.append((0, f, r)); self.pawns.append((1, f, r + 1))
        self.region = region                  # None or set of allowed files
        self.build()

    def nbf(self, f, d):
        g = f + d
        if self.wrap: return g % self.W
        return g if 0 <= g < self.W else None

    def adjacent(self, a, b):
        (fa, ra), (fb, rb) = a, b
        if abs(ra - rb) > 1: return False
        df = abs(fa - fb)
        if self.wrap: df = min(df, self.W - df)
        return df <= 1

    def passed(self, mask):
        res = [False, False]
        for i, (c, f, r) in enumerate(self.pawns):
            if not (mask >> i) & 1: continue
            ok = True
            for j, (c2, f2, r2) in enumerate(self.pawns):
                if not (mask >> j) & 1 or c2 == c: continue
                df = abs(f - f2)
                if self.wrap: df = min(df, self.W - df)
                if df <= 1 and ((r2 > r) if c == 0 else (r2 < r)): ok = False; break
            if ok: res[c] = True
        return res

    def attacked(self, mask, sq, by):
        f, r = sq
        for i, (c, pf, pr) in enumerate(self.pawns):
            if not (mask >> i) & 1 or c != by: continue
            tr = pr + (1 if c == 0 else -1)
            if tr != r: continue
            for d in (-1, 1):
                if self.nbf(pf, d) == f: return True
        return False

    def build(self):
        W, H = self.W, self.H
        n = len(self.pawns)
        full = (1 << n) - 1
        self.full = full
        sqs = [(f, r) for f in range(W) for r in range(1, H + 1) if self.region is None or f in self.region]
        self.sqs = sqs
        kadj = {}
        for s in sqs:
            lst = []
            for df in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    if df == 0 and dr == 0: continue
                    g = self.nbf(s[0], df)
                    if g is None: continue
                    t = (g, s[1] + dr)
                    if 1 <= t[1] <= H and t != s and (self.region is None or g in self.region) and t not in lst: lst.append(t)
            kadj[s] = lst
        self.kadj = kadj
        okm = {}
        for m in range(1 << n):
            p = self.passed(m); okm[m] = not (p[0] or p[1])
        self.okm = okm
        pawnsq = {}
        for m in range(1 << n):
            pawnsq[m] = {(f, r): (c, i) for i, (c, f, r) in enumerate(self.pawns) if (m >> i) & 1}
        self.pawnsq = pawnsq
        index = {}; nodes = []
        for m in range(1 << n):
            if not okm[m]: continue
            ps = pawnsq[m]
            for wk in sqs:
                if wk in ps or self.attacked(m, wk, 1): continue
                for bk in sqs:
                    if bk in ps or self.attacked(m, bk, 0) or self.adjacent(wk, bk) or wk == bk: continue
                    index[(m, wk, bk)] = len(nodes); nodes.append((m, wk, bk))
        self.nodes, self.index = nodes, index
        L = [[] for _ in nodes]; R = [[] for _ in nodes]
        for i, (m, wk, bk) in enumerate(nodes):
            ps = pawnsq[m]
            for c in (0, 1):
                me, op = (wk, bk) if c == 0 else (bk, wk)
                out = L[i] if c == 0 else R[i]
                for t in kadj[me]:
                    if self.adjacent(t, op) or t == op: continue
                    nm = m
                    if t in ps:
                        cc, pi = ps[t]
                        if cc == c: continue
                        nm = m & ~(1 << pi)
                    if self.attacked(nm, t, 1 - c): continue
                    if not okm[nm]:
                        p = self.passed(nm)
                        if p[0] and not p[1]: out.append('P')
                        elif p[1] and not p[0]: out.append('M')
                        else: raise RuntimeError('race')
                    else:
                        key = (nm, t, bk) if c == 0 else (nm, wk, t)
                        out.append(index[key])
        self.L, self.R = L, R

    def name(self, i):
        m, wk, bk = self.nodes[i]
        F = 'abcdefghijklmnopqrstuvwxyz'
        s = 'K%s%d k%s%d' % (F[wk[0]], wk[1], F[bk[0]], bk[1])
        for k, (c, f, r) in enumerate(self.pawns):
            if (m >> k) & 1: s += ' %s%s%d' % ('P' if c == 0 else 'p', F[f], r)
        return s

# ---------------- contexts: a context is (L, R) option lists on nodes 0..k-1 with 'P','M' terminals
def battery():
    C = {}
    C['0'] = ([[]], [[]])
    C['*'] = ([[1], []], [[1], []])
    for n in (1, 2, 3):
        C['+%d' % n] = ([[i + 1] if i < n else [] for i in range(n + 1)], [[] for i in range(n + 1)])
        C['-%d' % n] = ([[] for i in range(n + 1)], [[i + 1] if i < n else [] for i in range(n + 1)])
    C['1/2'] = ([[1], [], [1]], [[2], [], []])
    C['-1/2'] = ([[2], [], []], [[1], [], [1]])
    C['up'] = ([[1], [], [1]], [[2], [], [1]])
    C['down'] = ([[2], [], [1]], [[1], [], [1]])
    C['up*'] = ([[1, 2], [], [1]], [[1], [], [1]])
    C['down*'] = ([[1], [], [1]], [[1, 2], [], [1]])
    C['*2'] = ([[1, 2], [], [1]], [[1, 2], [], [1]])
    C['on'] = ([[0]], [[]])
    C['off'] = ([[]], [[0]])
    C['dud'] = ([[0]], [[0]])
    C['over'] = ([[1], []], [[0], []])
    C['under'] = ([[0], []], [[1], []])
    C['tis'] = ([[1], []], [[], [0]])
    C['tisn'] = ([[], [0]], [[1], []])
    C['{+|}'] = ([['P']], [[]])
    C['{|-}'] = ([[]], [['M']])
    C['{+|-}'] = ([['P']], [['M']])
    C['{+|0}'] = ([['P'], []], [[1], []])
    C['{0|-}'] = ([[1], []], [['M'], []])
    C['{1|0}'] = ([[1], [2], []], [[2], [], []])
    C['{0|-1}'] = ([[2], [], []], [[1], [2], []])
    C['{2|0}'] = ([[1], [2], [3], []], [[3], [], [], []])
    C['{0|-2}'] = ([[3], [], [], []], [[1], [2], [3], []])
    C['{+|on}'] = ([['P'], [1]], [[1], []])
    C['{off|-}'] = ([[1], []], [['M'], [1]])
    C['{on|off}'] = ([[1], [1], []], [[2], [], [2]])
    return C

# ---------------- bisimulation quotient (strong, with terminals P/M as distinct sinks)
def quotient(L, R, starts=None):
    n = len(L)
    cls = [0] * n
    ncls = 1
    while True:
        sigs = {}
        new = [0] * n
        for x in range(n):
            s = (cls[x],
                 tuple(sorted({(t if isinstance(t, str) else cls[t]) if isinstance(t, str) else cls[t] for t in L[x]}, key=str)),
                 tuple(sorted({(t if isinstance(t, str) else cls[t]) if isinstance(t, str) else cls[t] for t in R[x]}, key=str)))
            new[x] = sigs.setdefault(s, len(sigs))
        if len(sigs) == ncls: cls = new; break
        ncls = len(sigs); cls = new
    QL = [None] * ncls; QR = [None] * ncls
    for x in range(n):
        c = cls[x]
        if QL[c] is None:
            QL[c] = sorted({t if isinstance(t, str) else cls[t] for t in L[x]}, key=str)
            QR[c] = sorted({t if isinstance(t, str) else cls[t] for t in R[x]}, key=str)
    return cls, QL, QR

# ---------------- D-sum solver
def dsum(GL, GR, KL, KR):
    """returns res[x][k] = (outcome White to move, outcome Black to move), 0 = W, 1 = D, 2 = L (White's view)."""
    n, m = len(GL), len(KL)
    opts = ((GL, KL), (GR, KR))   # mover 0 uses L, mover 1 uses R
    # predecessor lists
    predG = [[[] for _ in range(n)] for _ in (0, 1)]
    predK = [[[] for _ in range(m)] for _ in (0, 1)]
    for s in (0, 1):
        for x in range(n):
            for t in opts[s][0][x]:
                if not isinstance(t, str): predG[s][t].append(x)
        for k in range(m):
            for t in opts[s][1][k]:
                if not isinstance(t, str): predK[s][t].append(k)
    wins = []
    for p in (0, 1):
        term = 'P' if p == 0 else 'M'
        won = [[[False, False] for _ in range(m)] for _ in range(n)]
        cnt = [[[0, 0] for _ in range(m)] for _ in range(n)]
        q = collections.deque()
        for x in range(n):
            for k in range(m):
                for s in (0, 1):
                    og, ok = opts[s][0][x], opts[s][1][k]
                    ntw = sum(1 for t in og if t == term) + sum(1 for t in ok if t == term)
                    nop = len(og) + len(ok)
                    if s == p:
                        if ntw > 0: won[x][k][s] = True; q.append((x, k, s))
                    else:
                        cnt[x][k][s] = nop - ntw
                        if cnt[x][k][s] == 0: won[x][k][s] = True; q.append((x, k, s))
        while q:
            x, k, sp = q.popleft()
            s = 1 - sp
            for x0 in predG[s][x]:
                if won[x0][k][s]: continue
                if s == p: won[x0][k][s] = True; q.append((x0, k, s))
                else:
                    cnt[x0][k][s] -= 1
                    if cnt[x0][k][s] == 0: won[x0][k][s] = True; q.append((x0, k, s))
            for k0 in predK[s][k]:
                if won[x][k0][s]: continue
                if s == p: won[x][k0][s] = True; q.append((x, k0, s))
                else:
                    cnt[x][k0][s] -= 1
                    if cnt[x][k0][s] == 0: won[x][k0][s] = True; q.append((x, k0, s))
        wins.append(won)
    res = [[None] * m for _ in range(n)]
    for x in range(n):
        for k in range(m):
            res[x][k] = tuple(0 if wins[0][x][k][s] else (2 if wins[1][x][k][s] else 1) for s in (0, 1))
    return res

def signatures(QL, QR, names=None):
    C = battery()
    names = names or list(C)
    sig = [''] * len(QL)
    for nm in names:
        KL, KR = C[nm]
        r = dsum(QL, QR, KL, KR)
        for x in range(len(QL)):
            sig[x] += '%d%d' % r[x][0]
    return names, sig

def refsigs():
    C = battery(); names = list(C)
    out = {}
    for nm in names:
        GL, GR = C[nm]
        s = ''
        for nm2 in names:
            KL, KR = C[nm2]
            r = dsum(GL, GR, KL, KR); s += '%d%d' % r[0][0]
        out.setdefault(s, []).append(nm)
    return names, out

def parse_cfg(s):
    return [(ord(t[0]) - 97, int(t[1:])) for t in s.split()]

if __name__ == '__main__':
    import time
    board, cfg = sys.argv[1], sys.argv[2]
    region = None
    if len(sys.argv) > 3 and sys.argv[3] != 'all':
        a, b = sys.argv[3].split('-'); region = set(range(int(a), int(b) + 1))
    wrap = board.startswith('cyl'); W, H = [int(v) for v in board.split(':')[1].split('x')]
    t0 = time.time()
    g = LK(W, H, wrap, parse_cfg(cfg), region)
    print('built', len(g.nodes), 'nodes in %.1fs' % (time.time() - t0), flush=True)
    full = g.full
    cls, QL, QR = quotient(g.L, g.R)
    print('quotient classes', len(QL), 'in %.1fs' % (time.time() - t0), flush=True)
    names, sig = signatures(QL, QR)
    rn, refs = refsigs()
    cnt = collections.Counter(); ex = {}
    for i, (m, wk, bk) in enumerate(g.nodes):
        if m != full: continue
        s = sig[cls[i]]
        nm = '='.join(refs[s]) if s in refs else 'UNMATCHED'
        cnt[nm] += 1; ex.setdefault(nm, []).append(g.name(i))
    for nm, c in sorted(cnt.items(), key=lambda t: -t[1]): print('%-14s %7d  %s' % (nm, c, '; '.join(ex[nm][:2])))
    print('distinct unmatched signatures', len({sig[cls[i]] for i, (m, wk, bk) in enumerate(g.nodes) if m == full and sig[cls[i]] not in refs}))
