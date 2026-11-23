#!/usr/bin/env python3
import sys
from collections import deque

RANKS = 8
W, B = 0, 1
INF = 10 ** 6


def other(c):
    return 1 - c


def bits(m):
    r = 1
    while m:
        if m & 1:
            yield r
        m >>= 1
        r += 1


def parse_file(tok):
    w = b = 0
    i = 0
    n = len(tok)
    while i < n:
        col = tok[i]
        i += 1
        j = i
        while j < n and tok[j].isdigit():
            j += 1
        for d in tok[i:j]:
            bit = 1 << (int(d) - 1)
            if col == 'W':
                w |= bit
            else:
                b |= bit
        i = j
    return (w, b)


def fam_M(n):
    assert n % 2 == 0 and n >= 10
    wall = []
    for f in range((n - 8)):
        if f % 2 == 0:
            wall.append('B4')
        else:
            wall.append('W2')
    tail = ['B6', 'W2', 'W3', 'B6', 'B7', 'W3', 'B7', 'W5']
    return wall + tail


def fam_O(n):
    assert n % 2 == 1 and n >= 11
    toks = ['B4']
    wall_len = n - 9
    for j in range(1, wall_len + 1):
        if j % 2 == 1:
            toks.append('B7')
        else:
            toks.append('W5')
    tail = ['B7', 'W3', 'B7', 'B6', 'W3', 'W2', 'B6', 'W2']
    return toks + tail


def fam_T(n):
    assert n % 2 == 0 and n >= 12
    wall = []
    for _ in range((n - 10) // 2):
        wall += ['B4', 'W2']
    tail = ['B5', 'W2', 'W6B7', 'W3', 'B7', 'B6', 'W3', 'W2', 'B6', 'W2']
    return wall + tail


def fam_S(n):
    assert n % 2 == 1 and n >= 13
    toks = ['B4', 'B6', 'W3']
    wall = []
    for _ in range((n - 11) // 2):
        wall += ['W2', 'B4']
    toks += wall
    tail = ['W6B7', 'W3', 'B7', 'B6', 'W3', 'W2', 'B6', 'W2']
    return toks + tail


def make_pos(tokens):
    return tuple(parse_file(t) for t in tokens)


def npawns(pos):
    return sum(bin(w).count('1') + bin(b).count('1') for w, b in pos)


def ep_protected(pos, ep, c, f, r):
    if ep is None:
        return False
    ef, stepper = ep
    if stepper != c or ef != f:
        return False
    if r != (4 if c == W else 5):
        return False
    n = len(pos)
    enemy_bit = 1 << (r - 1)
    left = pos[(f - 1) % n][1 - c]
    right = pos[(f + 1) % n][1 - c]
    return bool((left | right) & enemy_bit)


def passed_pawns(pos, ep, c):
    n = len(pos)
    e = 1 - c
    res = []
    for f in range(n):
        mine = pos[f][c]
        if not mine:
            continue
        foe_mask = pos[f][e] | pos[(f - 1) % n][e] | pos[(f + 1) % n][e]
        for r in bits(mine):
            if c == W:
                ahead = foe_mask >> r
            else:
                ahead = foe_mask & ((1 << (r - 1)) - 1)
            if ahead:
                continue
            if ep_protected(pos, ep, c, f, r):
                continue
            res.append((f, r))
    return res


def promo_dist(pos, ep, c):
    best = INF
    for f, r in passed_pawns(pos, ep, c):
        occ = pos[f][0] | pos[f][1]
        if c == W:
            if occ >> r:
                continue
            d = RANKS - r - (1 if r == 2 else 0)
        else:
            if occ & ((1 << (r - 1)) - 1):
                continue
            d = r - 1 - (1 if r == RANKS - 1 else 0)
        if d < best:
            best = d
    return best


def verdict(pos, ep, mover):
    wp = passed_pawns(pos, ep, W)
    bp = passed_pawns(pos, ep, B)
    if wp and bp:
        opp = other(mover)
        if promo_dist(pos, ep, opp) <= promo_dist(pos, ep, mover):
            return opp
        return mover
    if wp:
        return W
    if bp:
        return B
    return None


def gen_moves(pos, ep, c):
    n = len(pos)
    e = other(c)
    step = 1 if c == W else -1
    home = 2 if c == W else 7
    out = {}
    for f in range(n):
        mine = pos[f][c]
        if not mine:
            continue
        occ = pos[f][0] | pos[f][1]
        for r in bits(mine):
            r1 = r + step
            if r1 < 1 or r1 > RANKS:
                continue
            frm = 1 << (r - 1)
            to1 = 1 << (r1 - 1)
            if not (occ & to1):
                lst = [list(x) for x in pos]
                pr = list(lst[f])
                pr[c] = (mine & ~frm) | to1
                lst[f] = tuple(pr)
                lst = tuple(tuple(x) for x in lst)
                out[(lst, None)] = 1
                r2 = r + 2 * step
                if r == home and 1 <= r2 <= RANKS and not (occ & (1 << (r2 - 1))):
                    to2 = 1 << (r2 - 1)
                    lst = [list(x) for x in pos]
                    pr = list(lst[f])
                    pr[c] = (mine & ~frm) | to2
                    lst[f] = tuple(pr)
                    lst = tuple(tuple(x) for x in lst)
                    beside = (pos[(f - 1) % n][e] | pos[(f + 1) % n][e]) & to2
                    newep = (f, c) if beside else None
                    out[(lst, newep)] = 1
            for g in ((f - 1) % n, (f + 1) % n):
                if pos[g][e] & to1:
                    lst = [list(x) for x in pos]
                    prf = list(lst[f])
                    prf[c] = mine & ~frm
                    lst[f] = tuple(prf)
                    prg = list(lst[g])
                    prg[c] |= to1
                    prg[e] &= ~to1
                    lst[g] = tuple(prg)
                    lst = tuple(tuple(x) for x in lst)
                    out[(lst, None)] = 1
                elif ep is not None and ep[1] == e and ep[0] == g and r1 == (3 if e == W else 6):
                    lst = [list(x) for x in pos]
                    prf = list(lst[f])
                    prf[c] = mine & ~frm
                    lst[f] = tuple(prf)
                    prg = list(lst[g])
                    prg[c] |= to1
                    prg[e] &= ~frm
                    lst[g] = tuple(prg)
                    lst = tuple(tuple(x) for x in lst)
                    out[(lst, None)] = 1
    return list(out)


class Full:
    def __init__(self, ep_mode='keep'):
        assert ep_mode in ('keep', 'expire')
        self.mode = ep_mode
        self.memo = {}
        self.nodes = 0

    def wins(self, pos, ep, h, mover):
        key = (pos, ep, h, mover)
        v = self.memo.get(key)
        if v is not None:
            return v
        self.nodes += 1
        e = other(mover)
        res = False
        later = []
        for np_, ne in gen_moves(pos, ep, mover):
            v2 = verdict(np_, ne, mover)
            if v2 == mover:
                res = True
                break
            if v2 is None:
                later.append((np_, ne))
        if not res:
            for np_, ne in later:
                if not self.wins(np_, ne, h, e):
                    res = True
                    break
        if not res and h:
            keep = ep if self.mode == 'keep' else None
            for h2 in range(h):
                if not self.wins(pos, keep, h2, e):
                    res = True
                    break
        self.memo[key] = res
        return res

    def signature(self, pos, hs):
        sig = ''
        for h in hs:
            a = self.wins(pos, None, h, W)
            b = self.wins(pos, None, h, B)
            sig += {(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(a, b)]
        return sig


def classify(pos, ep, c):
    e = other(c)
    res = []
    for np_, ne in gen_moves(pos, ep, c):
        v = verdict(np_, ne, c)
        if v == c:
            k = 'T'
        elif v == e:
            k = 'L'
        else:
            k = 'K'
            for np2, ne2 in gen_moves(np_, ne, e):
                if verdict(np2, ne2, e) == e:
                    k = 'P'
                    break
        res.append((k, np_, ne))
    return res


class Graph:
    def __init__(self, pos0):
        self.start = (pos0, None)
        self.info = {}
        self.order = [self.start]
        seen = {self.start}
        q = deque([self.start])
        while q:
            nd = q.popleft()
            pos, ep = nd
            rec = {}
            for c in (W, B):
                cl = classify(pos, ep, c)
                T = frozenset((p, e) for k, p, e in cl if k == 'T')
                K = frozenset((p, e) for k, p, e in cl if k == 'K')
                nL = sum(1 for k, _, _ in cl if k == 'L')
                nP = sum(1 for k, _, _ in cl if k == 'P')
                rec[c] = (T, K, nL, nP)
                for ch in sorted(K, key=repr):
                    if ch not in seen:
                        seen.add(ch)
                        self.order.append(ch)
                        q.append(ch)
            self.info[nd] = rec

    def stats(self):
        n = len(self.start[0])
        nK = sum(len(self.info[nd][c][1]) for nd in self.order for c in (W, B))
        nT = sum(len(self.info[nd][c][0]) for nd in self.order for c in (W, B))
        flagged = sum(1 for nd in self.order if nd[1] is not None)
        p0 = self.start[0]
        zone = sorted({f for (p, _) in self.order for f in range(n) if p[f] != p0[f]})
        return dict(nodes=len(self.order), K=nK, T=nT, flagged=flagged, zone=zone)


def run_smallest():
    cases = [('M', fam_M, 10, range(4)),
             ('O', fam_O, 11, range(4)),
             ('T', fam_T, 12, range(5)),
             ('S', fam_S, 13, range(5))]
    for name, fam, n, hs in cases:
        pos = make_pos(fam(n))
        assert npawns(pos) == (n if name in ('M', 'O') else n + 1), (name, n, npawns(pos))
        for mode in ('keep', 'expire'):
            f = Full(mode)
            sig = f.signature(pos, hs)
            print(f'{name}_{n} mode={mode} sig={sig} states={f.nodes}', flush=True)


def run_graph(n_family, n):
    fammap = {'M': fam_M, 'O': fam_O, 'T': fam_T, 'S': fam_S}
    pos = make_pos(fammap[n_family](n))
    g = Graph(pos)
    st = g.stats()
    print(f'{n_family}_{n}: {st}', flush=True)
    return st


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'graph':
        run_graph(sys.argv[2], int(sys.argv[3]))
    else:
        run_smallest()


def run_extra():
    cases = [('M', fam_M, 8, range(4)),
             ('O', fam_O, 9, range(4)),
             ('T', fam_T, 10, range(5)),
             ('S', fam_S, 11, range(5))]
    for name, fam, n, hs in cases:
        try:
            pos = make_pos(fam(n))
        except AssertionError as e:
            print(f'{name}_{n} invalid: {e}', flush=True)
            continue
        f = Full('keep')
        sig = f.signature(pos, hs)
        print(f'{name}_{n} (below claimed smallest) sig={sig} states={f.nodes}', flush=True)

if __name__ == '__main__' and False:
    pass
