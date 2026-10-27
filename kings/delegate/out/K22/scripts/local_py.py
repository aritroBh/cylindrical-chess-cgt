#!/usr/bin/env python3
"""Second, independent implementation of the local game of LOOPY.md Definition 2.6 (unbounded time).

Written from the definition, not from local.cpp: coordinates (file, rank), frozensets, forward exploration
of the reachable game graph from each root, then T = least n such that White (s-bar) forces a win
within n White moves, computed by rounds  W_n = {white states with a move to terminal-win or to a black
state all of whose moves lead into W_{n-1}}.

White = s-bar (moves up, king confined to F_Z, no pass).  Black = s (moves down, may pass when not in check).
First promotion ends the game.  White promotion wins (L1_P), or with safe=True only if the black king
cannot capture the new queen at once (L1).  Black promotion = failure for White.  Mate of Black (in check,
no legal move) = win for White.  White with no legal move = failure.  Infinite play = failure.

usage: local_py.py BOARD(flat|cyl) W H FZLO FZHI [safe]  < lines "Ka1 ka6 Pc2 pd3 b -"
prints per line: "<line> | no-win" or "<line> | WIN T=<n>"
"""
import sys

def make(kind, W, H, fzlo, fzhi, safe):
    wrap = (kind == 'cyl')

    def norm(f, r):
        if r < 0 or r >= H:
            return None
        if wrap:
            f %= W
        elif f < 0 or f >= W:
            return None
        return (f, r)

    def nbrs(sq):
        out = set()
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == 0 and dr == 0:
                    continue
                t = norm(sq[0] + df, sq[1] + dr)
                if t is not None and t != sq:
                    out.add(t)
        return out

    def pattacks(col, sq):          # squares attacked by a pawn of colour col (0 white, 1 black) on sq
        dr = 1 if col == 0 else -1
        out = set()
        for df in (-1, 1):
            t = norm(sq[0] + df, sq[1] + dr)
            if t is not None:
                out.add(t)
        return out

    def hit(col, sq, pawns):        # is sq attacked by some pawn of colour col among pawns
        return any(sq in pattacks(col, p) for p in pawns)

    last = {0: H - 1, 1: 0}
    start = {0: 1, 1: H - 2}
    dirr = {0: 1, 1: -1}

    def legal_state(s):
        wp, bp, wk, bk, stm, ep = s
        if wk == bk or wk in wp or wk in bp or bk in wp or bk in bp:
            return False
        if bk in nbrs(wk):
            return False
        if stm == 0 and hit(0, bk, wp):
            return False
        if stm == 1 and hit(1, wk, bp):
            return False
        return True

    def moves(s):
        """list of (kind, newstate) ; kind 'win' (white promotion that wins), 'fail' (terminal, no win), 'go'"""
        wp, bp, wk, bk, stm, ep = s
        res = []
        me = stm
        op = 1 - me
        mine = wp if me == 0 else bp
        theirs = bp if me == 0 else wp
        mk, ok = (wk, bk) if me == 0 else (bk, wk)
        allocc = set(wp) | set(bp) | {wk, bk}

        def build(nmine, ntheirs, nmk, nep):
            nwp, nbp = (nmine, ntheirs) if me == 0 else (ntheirs, nmine)
            nwk, nbk = (nmk, ok) if me == 0 else (ok, nmk)
            return (frozenset(nwp), frozenset(nbp), nwk, nbk, op, nep)

        # king moves
        for t in nbrs(mk):
            if t in mine or t == ok or t in nbrs(ok):
                continue
            if me == 0 and not (fzlo <= t[0] <= fzhi):
                continue
            nth = theirs - {t}
            if hit(op, t, nth):
                continue
            res.append(('go', build(mine, nth, t, None)))
        # pass
        if me == 1 and not hit(0, bk, wp):
            res.append(('go', (wp, bp, wk, bk, 0, None)))
        # pawn moves
        d = dirr[me]
        for p in mine:
            f, r = p
            cands = []   # (target, captured_square or None, new_ep)
            t1 = norm(f, r + d)
            if t1 is not None and t1 not in allocc:
                cands.append((t1, None, None))
                if r == start[me]:
                    t2 = norm(f, r + 2 * d)
                    if t2 is not None and t2 not in allocc:
                        nep = None
                        if t2[1] != last[me]:
                            for df in (-1, 1):
                                a = norm(f + df, t2[1])
                                if a is not None and a in theirs:
                                    nep = (t1, me)
                        cands.append((t2, None, nep))
            for tc in pattacks(me, p):
                if tc in theirs:
                    cands.append((tc, tc, None))
                elif ep is not None and ep[0] == tc and ep[1] == op:
                    victim = (tc[0], r)
                    if victim in theirs:
                        cands.append((tc, victim, None))
            for (t, cap, nep) in cands:
                nth = theirs - {cap} if cap is not None else theirs
                if hit(op, mk, nth):
                    continue
                nmine = (mine - {p})
                if t[1] == last[me]:
                    if me == 1:
                        res.append(('fail', None))
                    else:
                        kind = 'win'
                        if safe:
                            # can the black king capture the new queen on t?
                            if bk in nbrs(t) and not (t in nbrs(wk)) and not hit(0, t, nmine):
                                kind = 'fail'
                        res.append((kind, None))
                else:
                    res.append(('go', build(nmine | {t}, nth, mk, nep)))
        return res

    def solve(root):
        # explore
        graph = {}
        stack = [root]
        while stack:
            s = stack.pop()
            if s in graph:
                continue
            ms = moves(s)
            graph[s] = ms
            for k, ns in ms:
                if k == 'go' and ns not in graph:
                    stack.append(ns)
        # rounds
        won_prev = set()          # white-to-move states winning within n-1 white moves
        n = 0
        won_black_prev = set()
        # black-to-move state b is "good(n)" iff mate, or all moves lead to white states in W_n
        while True:
            n += 1
            Wn = set()
            # good black states given W_{n-1} (white states winning within n-1 moves)
            good = set()
            for s, ms in graph.items():
                if s[4] != 1:
                    continue
                if not ms:
                    good.add(s)            # black cannot move: only possible in check -> mate
                    continue
                ok = True
                for k, ns in ms:
                    if k != 'go' or ns not in won_prev:
                        ok = False
                        break
                if ok:
                    good.add(s)
            for s, ms in graph.items():
                if s[4] != 0:
                    continue
                for k, ns in ms:
                    if k == 'win' or (k == 'go' and ns in good):
                        Wn.add(s)
                        break
            if root[4] == 0 and root in Wn:
                return n
            if root[4] == 1:
                # a black-to-move root is won within n White moves iff it is mate or all its moves lead into W_n
                ms = graph[root]
                if (not ms) or all(k == 'go' and ns in Wn for k, ns in ms):
                    return n if ms else 0
            if Wn == won_prev:
                return None
            won_prev = Wn
            if n > 60:
                return None

    solve.moves = moves
    solve.hit = hit
    return solve


def parse(line, W, H):
    toks = line.split()
    stm = 1 if toks[-2] == 'b' else 0
    epstr = toks[-1]
    wp, bp = set(), set()
    wk = bk = None
    for t in toks[:-2]:
        f = ord(t[1]) - 97
        r = int(t[2:]) - 1
        c = t[0]
        if c == 'K': wk = (f, r)
        elif c == 'k': bk = (f, r)
        elif c == 'P': wp.add((f, r))
        elif c == 'p': bp.add((f, r))
    ep = None
    if epstr != '-':
        f = ord(epstr[0]) - 97
        r = int(epstr[1:]) - 1
        ep = ((f, r), 1 if stm == 0 else 0)
    return (frozenset(wp), frozenset(bp), wk, bk, stm, ep)


if __name__ == '__main__':
    kind, W, H, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    safe = len(sys.argv) > 6 and sys.argv[6] == 'safe'
    solve = make(kind, W, H, lo, hi, safe)
    for line in sys.stdin:
        line = line.split('|')[0].strip()
        if not line:
            continue
        s = parse(line, W, H)
        t = solve(s)
        print(line, '|', 'no-win' if t is None else 'WIN T=%d' % t)
