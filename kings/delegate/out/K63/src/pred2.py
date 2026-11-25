"""K63 question 3, second implementation of the D-sum prediction (written separately from gen_ctx63.py: own move
generator on 64-bit masks, own state space, retrograde analysis with move counters instead of repeated sweeps).
For each context line of in/ctx_<tag>.pred (the context is read from the bracket), computes
  r(over_D (+) X) and r(X) for White and Black to move (White's view)
and prints the lines that disagree with the .pred file, then a tally.
Rules: X = context pawns on flat 8x8, pawn moves only, double steps from rank 2 (White) / rank 7 (Black), e.p.
(only right after a double step, by the side to move, lost after any move of that side, in X or in over), promotion is
a terminal win for the promoter, no move = loss.  over_D: at omega Black may pass (omega -> omega) and White may move
omega -> 0_D; 0_D has no move.
usage: python3 pred2.py <tag>"""
import sys
from collections import deque

W = 8


def sq(name):
    return (int(name[1]) - 1) * W + (ord(name[0]) - 97)


def gen(wp, bp, ep, side):
    """yields ('T', winner) or ('N', wp, bp, ep); side 0 White, 1 Black"""
    me, op = (wp, bp) if side == 0 else (bp, wp)
    occ = wp | bp
    step = W if side == 0 else -W
    for s in range(64):
        if not (me >> s) & 1:
            continue
        f, r = s % W, s // W
        t = s + step
        lastrank = 7 if side == 0 else 0

        def emit(to, capmask, newep):
            if to // W == lastrank:
                return ('T', side)
            nme = (me & ~(1 << s)) | (1 << to)
            nop = op & ~capmask
            return ('N', nme, nop, newep) if side == 0 else ('N', nop, nme, newep)
        if not (occ >> t) & 1:
            yield emit(t, 0, -1)
            if r == (1 if side == 0 else 6) and not (occ >> (t + step)) & 1:
                yield emit(t + step, 0, t)
        for df in (-1, 1):
            if not 0 <= f + df < W:
                continue
            c = t + df
            if (op >> c) & 1:
                yield emit(c, 1 << c, -1)
            elif c == ep:
                yield emit(c, 1 << (c - step), -1)


def solve(ws, bs):
    wp = sum(1 << sq(x) for x in ws); bp = sum(1 << sq(x) for x in bs)
    # state: (o, wp, bp, ep, side); o = 0 omega, 1 zero.  Terminal outcomes as strings.
    succ, pred, index = {}, {}, {}
    starts = [(o, wp, bp, -1, s) for o in (0, 1) for s in (0, 1)]
    todo = deque(starts)
    for st in starts:
        index[st] = True
    while todo:
        st = todo.popleft()
        o, a, b, ep, side = st
        out = []
        for m in gen(a, b, ep, side):
            if m[0] == 'T':
                out.append('WIN' if m[1] == side else 'LOSS')
            else:
                out.append((o, m[1], m[2], m[3], 1 - side))
        if o == 0:
            out.append((1, a, b, -1, 1) if side == 0 else (0, a, b, -1, 0))
        succ[st] = out
        for nx in out:
            if isinstance(nx, str):
                continue
            pred.setdefault(nx, []).append(st)
            if nx not in index:
                index[nx] = True; todo.append(nx)
    val = {}   # 'win' / 'lose' for the side to move
    cnt = {}
    q = deque()
    for st, out in succ.items():
        if not out or all(x == 'LOSS' for x in out):
            val[st] = 'lose'; q.append(st)
        elif any(x == 'WIN' for x in out):
            val[st] = 'win'; q.append(st)
        else:
            cnt[st] = sum(1 for x in out if x != 'LOSS')
    while q:
        st = q.popleft()
        for p in pred.get(st, []):
            if p in val:
                continue
            if val[st] == 'lose':
                val[p] = 'win'; q.append(p)
            else:
                cnt[p] -= 1
                if cnt[p] == 0:
                    val[p] = 'lose'; q.append(p)
    res = {}
    for o, lab in ((0, 'omega'), (1, 'zero')):
        for s, c in ((0, 'w'), (1, 'b')):
            v = val.get((o, wp, bp, -1, s))
            res[(lab, c)] = 'D' if v is None else ('W' if (v == 'win') == (s == 0) else 'L')
    return res


if __name__ == '__main__':
    tag = sys.argv[1]
    n = bad = 0
    for line in open('in/ctx_%s.pred' % tag):
        name, rest = line.split(' [', 1)
        ctx, rest = rest.split('] ', 1)
        t = rest.split()
        want = {('omega', 'w'): t[2], ('omega', 'b'): t[4], ('zero', 'w'): t[7], ('zero', 'b'): t[9]}
        toks = ctx.split() if ctx != 'empty' else []
        got = solve([x[1:] for x in toks if x[0] == 'P'], [x[1:] for x in toks if x[0] == 'p'])
        n += 1
        if got != want:
            bad += 1
            print('DIFF', name, ctx, 'pred', want, 'pred2', got)
    print('%d contexts, %d differ between gen_ctx63 and pred2' % (n, bad))
