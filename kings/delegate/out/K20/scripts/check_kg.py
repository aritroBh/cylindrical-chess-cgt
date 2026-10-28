#!/usr/bin/env python3
"""Independent re-implementation (K20) of the local king-fight game and of the battery signature.
Written from the definition in REPORT.md section 1, not from kg.cpp.  Uses cylcgt.pawns.passed for the
passed-pawn test (project code, independent of kg.cpp).  Compares, for every legal root of the given
configurations, the full battery signature with the one printed by kg (roots file).

usage: check_kg.py <board e.g. cyl:6x6> <roots file written by kg --roots> <config e.g. "a2 c4">...
"""
import sys, itertools
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
from cylcgt.pawns import Board, Pos, passed

P, M = 'P', 'M'   # plus / minus terminals


def contexts():
    """name -> (list of (Lopts, Ropts)), root = node 0. Options: int node, 'P', 'M'."""
    C = {}
    C['0'] = [([], [])]
    C['*'] = [([1], [1]), ([], [])]
    for n in (1, 2, 3):
        C['+%d' % n] = [([i + 1] if i < n else [], []) for i in range(n + 1)]
        C['-%d' % n] = [([], [i + 1] if i < n else []) for i in range(n + 1)]
    C['1/2'] = [([1], [2]), ([], []), ([1], [])]
    C['-1/2'] = [([2], [1]), ([], []), ([], [1])]
    C['up'] = [([1], [2]), ([], []), ([1], [1])]
    C['down'] = [([2], [1]), ([], []), ([1], [1])]
    C['up*'] = [([1, 2], [1]), ([], []), ([1], [1])]
    C['down*'] = [([1], [1, 2]), ([], []), ([1], [1])]
    C['*2'] = [([1, 2], [1, 2]), ([], []), ([1], [1])]
    C['on'] = [([0], [])]
    C['off'] = [([], [0])]
    C['dud'] = [([0], [0])]
    C['over'] = [([1], [0]), ([], [])]
    C['under'] = [([0], [1]), ([], [])]
    C['tis'] = [([1], []), ([], [0])]
    C['tisn'] = [([], [1]), ([0], [])]
    C['{+|}'] = [([P], [])]
    C['{|-}'] = [([], [M])]
    C['{+|-}'] = [([P], [M])]
    C['{+|0}'] = [([P], [1]), ([], [])]
    C['{0|-}'] = [([1], [M]), ([], [])]
    C['{1|0}'] = [([1], [2]), ([2], []), ([], [])]
    C['{0|-1}'] = [([2], [1]), ([], [2]), ([], [])]
    C['{2|0}'] = [([1], [3]), ([2], []), ([3], []), ([], [])]
    C['{0|-2}'] = [([3], [1]), ([], [2]), ([], [3]), ([], [])]
    C['{+|on}'] = [([P], [1]), ([1], [])]
    C['{off|-}'] = [([1], [M]), ([], [1])]
    C['{on|off}'] = [([1], [2]), ([1], []), ([], [2])]
    return C


ORDER = ["0", "*", "+1", "-1", "+2", "-2", "+3", "-3", "1/2", "-1/2", "up", "down", "up*", "down*", "*2", "on", "off", "dud",
         "over", "under", "tis", "tisn", "{+|}", "{|-}", "{+|-}", "{+|0}", "{0|-}", "{1|0}", "{0|-1}", "{2|0}", "{0|-2}",
         "{+|on}", "{off|-}", "{on|off}"]


def build_game(board, W, H, wrap, pairs):
    """Return (nodes: list of (pawnset(frozenset of ('P'|'p',(f,r))), wk, bk)), L, R option lists."""
    B = Board(W, H, wrap, False)
    pawns = []
    for (f, r) in pairs:
        pawns.append(('P', (f, r)))
        pawns.append(('p', (f, r + 1)))

    def kn(sq):
        out = []
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == 0 and dr == 0:
                    continue
                g = B.nb(sq[0], df) if wrap else (sq[0] + df if 1 <= sq[0] + df <= W else None)
                # cylcgt Board uses 0-based files; we use 0-based files, 1-based ranks
                r = sq[1] + dr
                if g is None or not (1 <= r <= H):
                    continue
                if wrap:
                    g = g % W
                out.append((g, r))
        return out

    def kn0(sq):
        out = []
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == 0 and dr == 0:
                    continue
                g = sq[0] + df
                if wrap:
                    g %= W
                elif not (0 <= g < W):
                    continue
                r = sq[1] + dr
                if not (1 <= r <= H):
                    continue
                if (g, r) != sq:
                    out.append((g, r))
        return out

    adjc = {}
    squares = [(f, r) for f in range(W) for r in range(1, H + 1)]
    for s in squares:
        adjc[s] = set(kn0(s))

    def attacked(pset, sq, by):
        # is sq attacked by a pawn of colour `by` ('P' or 'p') in pset
        for c, (f, r) in pset:
            if c != by:
                continue
            rr = r + 1 if c == 'P' else r - 1
            for df in (-1, 1):
                g = f + df
                if wrap:
                    g %= W
                elif not (0 <= g < W):
                    continue
                if (g, rr) == sq:
                    return True
        return False

    def pawnsets_terminal(pset):
        w = frozenset(s for c, s in pset if c == 'P')
        b = frozenset(s for c, s in pset if c == 'p')
        pos = Pos(w, b, None)
        pw = passed(B, pos, 'W')
        pb = passed(B, pos, 'B')
        return pw, pb

    full = frozenset(pawns)
    subsets = []
    for k in range(len(pawns) + 1):
        for comb in itertools.combinations(pawns, k):
            subsets.append(frozenset(comb))
    # non-terminal subsets (no passer for anyone)
    okset = {}
    for ps in subsets:
        pw, pb = pawnsets_terminal(ps)
        okset[ps] = not (pw or pb)
    if not okset[full]:
        return None
    index = {}
    nodes = []
    for ps in subsets:
        if not okset[ps]:
            continue
        occ = {s for c, s in ps}
        for wk in squares:
            if wk in occ or attacked(ps, wk, 'p'):
                continue
            for bk in squares:
                if bk in occ or bk == wk or bk in adjc[wk] or attacked(ps, bk, 'P'):
                    continue
                index[(ps, wk, bk)] = len(nodes)
                nodes.append((ps, wk, bk))
    L = [[] for _ in nodes]
    R = [[] for _ in nodes]
    for i, (ps, wk, bk) in enumerate(nodes):
        for side in (0, 1):
            me, op = (wk, bk) if side == 0 else (bk, wk)
            mine, theirs = ('P', 'p') if side == 0 else ('p', 'P')
            for t in adjc[me]:
                if t == op or t in adjc[op]:
                    continue
                occ_own = {s for c, s in ps if c == mine}
                if t in occ_own:
                    continue
                nps = ps
                for c, s in ps:
                    if c == theirs and s == t:
                        nps = frozenset(x for x in ps if x != (c, s))
                if attacked(nps, t, theirs):
                    continue
                if not okset[nps]:
                    pw, pb = pawnsets_terminal(nps)
                    assert pw != pb, 'race'
                    term = P if pw else M
                    (L if side == 0 else R)[i].append(term)
                else:
                    key = (nps, t, bk) if side == 0 else (nps, wk, t)
                    (L if side == 0 else R)[i].append(index[key])
    return nodes, index, L, R


def solve_product(L, R, KL, KR):
    """Naive least-fixed-point iteration. Returns outcomes for K root 0: dict x -> (outW, outB), 0=W 1=D 2=L."""
    n, m = len(L), len(KL)
    G = (L, R)
    K = (KL, KR)

    def wins(player):
        term = P if player == 0 else M
        win = [[[False, False] for _ in range(m)] for _ in range(n)]   # win[x][k][side to move]
        changed = True
        while changed:
            changed = False
            for x in range(n):
                for k in range(m):
                    for s in (0, 1):
                        if win[x][k][s]:
                            continue
                        opts = []   # list of statuses: True if option is a win for `player`
                        for t in G[s][x]:
                            if t == P or t == M:
                                opts.append(t == term)
                            else:
                                opts.append(win[t][k][1 - s])
                        for t in K[s][k]:
                            if t == P or t == M:
                                opts.append(t == term)
                            else:
                                opts.append(win[x][t][1 - s])
                        if s == player:
                            v = any(opts)
                        else:
                            v = all(opts)    # empty -> True: opponent has no move, loses
                        if v:
                            win[x][k][s] = True
                            changed = True
        return win

    w0, w1 = wins(0), wins(1)
    res = []
    for x in range(n):
        r = []
        for s in (0, 1):
            r.append(0 if w0[x][0][s] else (2 if w1[x][0][s] else 1))
        res.append(tuple(r))
    return res


def rootname(nodes_i):
    ps, wk, bk = nodes_i
    FILES = 'abcdefgh'
    nm = lambda s: FILES[s[0]] + str(s[1])
    toks = {'K' + nm(wk), 'k' + nm(bk)}
    for c, s in ps:
        toks.add(c + nm(s))
    return frozenset(toks)


def main():
    board = sys.argv[1]
    rootsfile = sys.argv[2]
    configs = sys.argv[3:]
    wrap = board.startswith('cyl')
    W, H = [int(x) for x in board.split(':')[1].split('x')]
    # load kg signatures
    ref = {}
    for line in open(rootsfile):
        cn, pos, rest = line.rstrip('\n').split('|', 2)
        nm, sh, sig = rest.rsplit('|', 2)
        ref[(cn.strip(), frozenset(pos.split()))] = sig
    C = contexts()
    bad = 0
    tot = 0
    for cfg in configs:
        pairs = []
        for tok in ([] if cfg == "none" else cfg.split()):
            pairs.append((ord(tok[0]) - 97, int(tok[1:])))
        nodes, index, L, R = build_game(board, W, H, wrap, pairs)
        sigs = [[] for _ in nodes]
        for name in ORDER:
            nd = C[name]
            KL = [x[0] for x in nd]
            KR = [x[1] for x in nd]
            res = solve_product(L, R, KL, KR)
            for i, (a, b) in enumerate(res):
                sigs[i].append(str(a) + str(b))
        cnt = 0
        for i, nd_i in enumerate(nodes):
            key = (cfg, rootname(nd_i))
            if key not in ref:
                print('MISSING in kg output', cfg, sorted(key[1]))
                bad += 1
                continue
            mine = ''.join(sigs[i])
            tot += 1
            cnt += 1
            if mine != ref[key]:
                bad += 1
                if bad <= 10:
                    print('MISMATCH', cfg, sorted(key[1]), '\n  py', mine, '\n  kg', ref[key])
        print('config', cfg, 'nodes', len(nodes), 'compared', cnt, 'running mismatches', bad, flush=True)
    print('TOTAL compared', tot, 'mismatches', bad)


main()
