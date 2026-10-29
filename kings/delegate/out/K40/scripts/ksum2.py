"""K40 second implementation of x (+) T (K+P v K in P, plus a terminal-free test game), for the cross-check.

Different method from kpsum.c: explicit move lists, predecessor lists and counting retrograde analysis
(a queue), White-win and White-loss sets propagated separately.  Own move generator, written from the
rules in kpsum.c's header (P: a promotion wins for White at once; Kxp is a draw terminal (K v K is dud);
a T-move is illegal while in check; a side with no move: Black in check = mated = White wins; otherwise
stalemate = draw, or a loss for the side to move with --normal).

Usage: python ksum2.py W H TESTSPEC [--normal] [--pv POS]  -> prints "pos | r ..." lines like kpsum.
TESTSPEC: ints:K (chain -K..K), or one of on off dud over under star up down pm1.
"""
import sys
from collections import deque

W, H, spec = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
NORMAL = '--normal' in sys.argv
N = W * H


def sqn(s):
    return chr(97 + s % W) + str(s // W + 1)


def at(f, r):
    return None if r < 0 or r >= H else r * W + f % W


KING = []
for s in range(N):
    f, r = s % W, s // W
    nb = {at(f + a, r + b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)}
    nb.discard(None); nb.discard(s)
    KING.append(nb)
PAWNATT = [{at(s % W - 1, s // W + 1), at(s % W + 1, s // W + 1)} - {None} for s in range(N)]

# ---- test game graph: list of (left options, right options), and named roots
tl, tr, roots = [], [], []


def node():
    tl.append([]); tr.append([]); return len(tl) - 1


if spec.startswith('ints:'):
    K = int(spec[5:]); z = node(); pos = {0: z}; neg = {0: z}
    for i in range(1, K + 1):
        a = node(); tl[a].append(pos[i - 1]); pos[i] = a
        b = node(); tr[b].append(neg[i - 1]); neg[i] = b
    roots = [(str(-i), neg[i]) for i in range(K, 0, -1)] + [('0', z)] + [(str(i), pos[i]) for i in range(1, K + 1)]
else:
    a = node()
    if spec == 'on': tl[a].append(a)
    elif spec == 'off': tr[a].append(a)
    elif spec == 'dud': tl[a].append(a); tr[a].append(a)
    elif spec == 'over': z = node(); tl[a].append(z); tr[a].append(a)
    elif spec == 'under': z = node(); tl[a].append(a); tr[a].append(z)
    elif spec == 'star': z = node(); tl[a].append(z); tr[a].append(z)
    elif spec == 'up': z = node(); st = node(); tl[st].append(z); tr[st].append(z); tl[a].append(z); tr[a].append(st)
    elif spec == 'down': z = node(); st = node(); tl[st].append(z); tr[st].append(z); tl[a].append(st); tr[a].append(z)
    elif spec == 'pm1':
        z = node(); o = node(); m = node(); tl[o].append(z); tr[m].append(z); tl[a].append(o); tr[a].append(m)
    else: raise SystemExit('bad spec')
    roots = [(spec, a)]
NT = len(tl)


def legal(s, wk, bk, p):
    if len({wk, bk, p}) < 3 or not (1 <= p // W <= H - 2) or bk in KING[wk]:
        return False
    return not (s == 0 and bk in PAWNATT[p])


def moves(state):
    """list of successors; 'W' = White wins at once, 'D' = draw terminal"""
    t, s, wk, bk, p = state
    out = []
    if s == 0:
        for d in KING[wk]:
            if d != p and d != bk and d not in KING[bk]:
                out.append((t, 1, d, bk, p))
        p1 = p + W
        if p1 != wk and p1 != bk:
            out.append('W' if p1 // W == H - 1 else (t, 1, wk, bk, p1))
            if p // W == 1:
                p2 = p1 + W
                if p2 != wk and p2 != bk:
                    out.append('W' if p2 // W == H - 1 else (t, 1, wk, bk, p2))
        for u in tl[t]:
            out.append((u, 1, wk, bk, p))
    else:
        for d in KING[bk]:
            if d != wk and d not in KING[wk] and d not in PAWNATT[p]:
                out.append('D' if d == p else (t, 0, wk, d, p))
        if bk not in PAWNATT[p]:
            for u in tr[t]:
                out.append((u, 0, wk, bk, p))
    return out


states = [(t, s, wk, bk, p) for t in range(NT) for s in (0, 1) for wk in range(N) for bk in range(N)
          for p in range(N) if legal(s, wk, bk, p)]
res, cnt, pred, dep = {}, {}, {}, {}
q = deque()
for st in states:
    mv = moves(st)
    cnt[st] = len(mv)
    for m in mv:
        if isinstance(m, tuple):
            pred.setdefault(m, []).append(st)
    s = st[1]
    if not mv:
        if s == 1 and st[3] in PAWNATT[st[4]]:
            res[st] = 'W'
        elif NORMAL:
            res[st] = 'L' if s == 0 else 'W'
        if st in res: q.append(st); dep[st] = 0
    elif s == 0 and 'W' in mv:
        res[st] = 'W'; q.append(st); dep[st] = 1
    elif s == 1:
        # Black terminal options: 'D' (Kxp) can never be a White win, so it is never counted down
        cnt[st] = sum(1 for m in mv if isinstance(m, tuple)) + (10 ** 6 if 'D' in mv else 0)
    else:
        cnt[st] = sum(1 for m in mv if isinstance(m, tuple)) + (10 ** 6 if 'W' in mv else 0)
# counters: for s=1, cnt = options not yet known W (White needs all); for s=0, cnt = options not yet L
while q:
    st = q.popleft(); r = res[st]
    for pr in pred.get(st, ()):
        if pr in res:
            continue
        s = pr[1]
        if r == 'W':
            if s == 0:
                res[pr] = 'W'; q.append(pr); dep[pr] = dep[st] + 1
            else:
                cnt[pr] -= 1
                if cnt[pr] == 0: res[pr] = 'W'; q.append(pr); dep[pr] = dep[st] + 1
        else:  # r == 'L'
            if s == 1:
                res[pr] = 'L'; q.append(pr); dep[pr] = dep[st] + 1
            else:
                cnt[pr] -= 1
                if cnt[pr] == 0: res[pr] = 'L'; q.append(pr); dep[pr] = dep[st] + 1

if '--pv' in sys.argv:
    # principal variation of a White win: White takes a fastest win, Black a slowest loss
    i = sys.argv.index('--pv'); wk, bk, p, sm, troot = sys.argv[i + 1:i + 6]
    idx = {sqn(x): x for x in range(N)}
    st = (dict(roots)[troot], 'wb'.index(sm), idx[wk], idx[bk], idx[p])
    tname = {v: k for k, v in roots}
    while True:
        r = res.get(st, 'D'); t, s, a, b, c = st
        print('wb'[s], 'K' + sqn(a), 'k' + sqn(b), 'P' + sqn(c), 'T=' + tname.get(t, str(t)), r, dep.get(st, ''))
        mv = moves(st)
        if r != 'W' or not mv: break
        if s == 0:
            if 'W' in mv: print('promotes'); break
            st = min((m for m in mv if isinstance(m, tuple) and res.get(m) == 'W'), key=lambda m: dep[m])
        else:
            st = max((m for m in mv if isinstance(m, tuple)), key=lambda m: dep[m])
    sys.exit()

print('# roots: ' + ' '.join(n for n, _ in roots))
for s in (0, 1):
    for wk in range(N):
        for bk in range(N):
            for p in range(N):
                if legal(s, wk, bk, p):
                    print(f'{sqn(wk)} {sqn(bk)} {sqn(p)} {"wb"[s]} |', ' '.join(res.get((t, s, wk, bk, p), 'D') for _, t in roots))
