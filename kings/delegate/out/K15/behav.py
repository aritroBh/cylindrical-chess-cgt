#!/usr/bin/env python3
"""K15: behavioural test of a king group against abstract tempo contexts (D-model, exact).

For a group (all pieces of the group, real legal moves of both sides, no passes, promotion = decisive win for the
promoter) and every context (a, b, c) = (a private White tempo moves, b private Black tempo moves, c shared single
moves), the outcome of  Z (+) (a,b,c)  is computed (normal play: a side with no move loses; infinite play = draw)
for both sides to move, and compared with  X_D (+) (a,b,c)  for X in dud, over, under, on, off, zero.
usage: behav.py W H flat(0|1) a_max b_max c_max "<group position>" ["<group position>" ...]
"""
import sys, itertools
W, H = int(sys.argv[1]), int(sys.argv[2]); FLAT = sys.argv[3] == "1"
AM, BM_, CM = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
FILES = "abcdefgh"
ALLSQ = [(f, r) for r in range(H) for f in range(W)]

def nbrs(s):
    f, r = s; out = []
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == 0 and dr == 0: continue
            q = r + dr
            if 0 <= q < H and (not FLAT or 0 <= f + df < W): out.append(((f + df) % W, q))
    return out
NB = {s: tuple(dict.fromkeys(nbrs(s))) for s in ALLSQ}
def adjacent(a, b): return b in NB[a]
def pawn_attacks(color, s):
    f, r = s; q = r + (1 if color == 0 else -1)
    if not (0 <= q < H): return ()
    return tuple(((f + d) % W, q) for d in (-1, 1) if not FLAT or 0 <= f + d < W)
def attacked_by(color, pawns, s):
    return any(s in pawn_attacks(color, p) for p in pawns)

def gen_moves(wk, bk, wp, bp, stm, ep):
    me = stm; ks, ko = (wk, bk) if me == 0 else (bk, wk)
    myp, opp = (wp, bp) if me == 0 else (bp, wp); oc = 1 - me; res = []
    for t in NB[ks]:
        if t in myp or t == ko or adjacent(t, ko): continue
        opp2 = opp - {t} if t in opp else opp
        if attacked_by(oc, opp2, t): continue
        nwp, nbp = (wp, opp2) if me == 0 else (opp2, bp); nwk, nbk = (t, bk) if me == 0 else (wk, t)
        res.append((nwk, nbk, nwp, nbp, None))
    d = 1 if me == 0 else -1; start = 1 if me == 0 else H - 2; last = H - 1 if me == 0 else 0
    occ = set(wp) | set(bp)
    for p in myp:
        f, r = p; r1 = r + d; t = (f, r1)
        if t != wk and t != bk and t not in occ and not attacked_by(oc, opp, ks):
            if r1 == last: res.append("WIN")
            else:
                nm = (myp - {p}) | {t}; nwp, nbp = (nm, opp) if me == 0 else (opp, nm)
                res.append((wk, bk, nwp, nbp, None))
                if r == start:
                    t2 = (f, r + 2 * d)
                    if t2 != wk and t2 != bk and t2 not in occ:
                        nm2 = (myp - {p}) | {t2}; nwp, nbp = (nm2, opp) if me == 0 else (opp, nm2)
                        res.append((wk, bk, nwp, nbp, (t, t2)))
        for t in pawn_attacks(me, p):
            if t in opp:
                opp2 = opp - {t}
                if attacked_by(oc, opp2, ks): continue
                nm = (myp - {p}) | {t}; nwp, nbp = (nm, opp2) if me == 0 else (opp2, nm)
                res.append((wk, bk, nwp, nbp, None))
    if ep is not None:
        T, C = ep
        for p in myp:
            if p[1] == C[1] and T in pawn_attacks(me, p):
                opp2 = opp - {C}
                if attacked_by(oc, opp2, ks): continue
                nm = (myp - {p}) | {T}; nwp, nbp = (nm, opp2) if me == 0 else (opp2, nm)
                res.append((wk, bk, nwp, nbp, None))
    return res

def parse(pos):
    wk = bk = None; wp = set(); bp = set()
    for t in pos.split():
        if len(t) < 3 or t[0] not in "KkPp": continue
        s = (FILES.index(t[1]), int(t[2:]) - 1)
        if t[0] == "K": wk = s
        elif t[0] == "k": bk = s
        elif t[0] == "P": wp.add(s)
        else: bp.add(s)
    return wk, bk, frozenset(wp), frozenset(bp)

# ---- abstract reservoirs X_D ----
ZSTR = {"dud": {"w": (["w"], ["w"])}, "on": {"w": (["w"], [])}, "off": {"w": ([], ["w"])},
        "over": {"w": (["0"], ["w"]), "0": ([], [])}, "under": {"w": (["w"], ["0"]), "0": ([], [])}, "zero": {"w": ([], [])}}

def solve_generic(nodes_opts, init_nodes):
    """nodes_opts: dict node -> (list_of_options_for_stm0, list_for_stm1); an option is a node or 'WIN'/'LOSE' (decisive
    win for White / Black).  States are (node, stm); a player with no option loses.  Returns dict state -> 0/1/2
    (draw / mover wins / mover loses)."""
    pass

def contexts():
    return [(a, b, c) for a in range(AM + 1) for b in range(BM_ + 1) for c in range(CM + 1)]

def solve_sum(nodes, opts):
    """nodes: list of node ids; opts[node] = (white_options, black_options) lists of node ids or 'WIN' (decisive win for the mover).
    returns val[(node, ctx, stm)] from the mover's point of view."""
    ctxs = contexts(); cid = {c: i for i, c in enumerate(ctxs)}
    # state index: (stm, ci, ni)
    n = len(nodes); nid = {x: i for i, x in enumerate(nodes)}
    def sidx(stm, ci, ni): return (stm * len(ctxs) + ci) * n + ni
    S = 2 * len(ctxs) * n
    succ = [None] * S; win = [False] * S
    for stm in (0, 1):
        for ci, (a, b, c) in enumerate(ctxs):
            for ni, x in enumerate(nodes):
                s = sidx(stm, ci, ni); lst = []; w = False
                for o in opts[x][stm]:
                    if o == "WIN": w = True
                    else: lst.append(sidx(1 - stm, ci, nid[o]))
                mine = a if stm == 0 else b
                if mine > 0:
                    na, nb = (a - 1, b) if stm == 0 else (a, b - 1)
                    lst.append(sidx(1 - stm, cid[(na, nb, c)], nid[x]))
                if c > 0: lst.append(sidx(1 - stm, cid[(a, b, c - 1)], nid[x]))
                succ[s] = lst; win[s] = w
    preds = [[] for _ in range(S)]; cnt = [0] * S
    for s in range(S):
        cnt[s] = len(succ[s])
        for t in succ[s]: preds[t].append(s)
    val = [0] * S; q = []
    for s in range(S):
        if win[s]: val[s] = 1; q.append(s)
        elif cnt[s] == 0: val[s] = 2; q.append(s)
    qi = 0
    while qi < len(q):
        v = q[qi]; qi += 1
        for u in preds[v]:
            if val[u]: continue
            if val[v] == 2: val[u] = 1; q.append(u)
            else:
                cnt[u] -= 1
                if cnt[u] == 0: val[u] = 2; q.append(u)
    return ctxs, nid, n, val

def build_group(root):
    wk, bk, wp, bp = root
    start = (wk, bk, wp, bp, None)
    nodes = {}; order = []
    stack = [start]
    # a node is (wk,bk,wp,bp,ep); ep belongs to the side to move after the double step; plain nodes have ep None.
    def opts_of(node):
        wk, bk, wp, bp, ep = node
        res = []
        for stm in (0, 1):
            # an ep right is only usable by the side that did not double-step: we store ep with the node and record the
            # side that may use it: ep right created by White's double step is usable by Black (stm 1).
            lst = []
            for m in gen_moves(wk, bk, wp, bp, stm, ep if stm_ok(node, stm) else None):
                lst.append(m if m == "WIN" else norm(m, stm))
            res.append(lst)
        return res
    def stm_ok(node, stm):
        return node[4] is not None and node[4][2] == stm  # placeholder, replaced below
    return None

# ep handling: store ep as (T, C, side_that_may_capture)
def gen_for(node, stm):
    wk, bk, wp, bp, ep = node
    e = (ep[0], ep[1]) if (ep is not None and ep[2] == stm) else None
    out = []
    for m in gen_moves(wk, bk, wp, bp, stm, e):
        if m == "WIN": out.append("WIN"); continue
        nwk, nbk, nwp, nbp, nep = m
        out.append((nwk, nbk, nwp, nbp, (nep[0], nep[1], 1 - stm) if nep else None))
    return out

def group_graph(root):
    wk, bk, wp, bp = root
    start = (wk, bk, wp, bp, None)
    opts = {}; stack = [start]
    while stack:
        nd = stack.pop()
        if nd in opts: continue
        o = (gen_for(nd, 0), gen_for(nd, 1)); opts[nd] = o
        for lst in o:
            for m in lst:
                if m != "WIN" and m not in opts: stack.append(m)
    return start, opts

def with_plain_variants(opts):
    """context moves clear an ep right: handled in solve_sum by mapping node -> plain node of the same position.
    To keep solve_sum generic we add, for every ep node, nothing; instead we transform: an ep node's context moves lead to the plain node."""
    return opts

def outcome_table(start, opts):
    nodes = list(opts.keys())
    # plain node map for ep nodes (context move expires the right)
    # emulate by adding, for ep nodes, a pseudo option via contexts: handled by remapping inside solve_sum2
    return nodes

def solve_group_sum(start, opts):
    nodes = list(opts.keys()); nid = {x: i for i, x in enumerate(nodes)}
    ctxs = contexts(); cid = {c: i for i, c in enumerate(ctxs)}; n = len(nodes)
    def sidx(stm, ci, ni): return (stm * len(ctxs) + ci) * n + ni
    S = 2 * len(ctxs) * n
    succ = [None] * S; win = [False] * S
    for stm in (0, 1):
        for ci, (a, b, c) in enumerate(ctxs):
            for ni, x in enumerate(nodes):
                s = sidx(stm, ci, ni); lst = []; w = False
                for o in opts[x][stm]:
                    if o == "WIN": w = True
                    else: lst.append(sidx(1 - stm, ci, nid[o]))
                plain = (x[0], x[1], x[2], x[3], None)
                pn = nid[plain] if plain in nid else None
                mine = a if stm == 0 else b
                if mine > 0 and pn is not None:
                    na, nb = (a - 1, b) if stm == 0 else (a, b - 1)
                    lst.append(sidx(1 - stm, cid[(na, nb, c)], pn))
                if c > 0 and pn is not None: lst.append(sidx(1 - stm, cid[(a, b, c - 1)], pn))
                succ[s] = lst; win[s] = w
    preds = [[] for _ in range(S)]; cnt = [0] * S
    for s in range(S):
        cnt[s] = len(succ[s])
        for t in succ[s]: preds[t].append(s)
    val = [0] * S; q = []
    for s in range(S):
        if win[s]: val[s] = 1; q.append(s)
        elif cnt[s] == 0: val[s] = 2; q.append(s)
    qi = 0
    while qi < len(q):
        v = q[qi]; qi += 1
        for u in preds[v]:
            if val[u]: continue
            if val[v] == 2: val[u] = 1; q.append(u)
            else:
                cnt[u] -= 1
                if cnt[u] == 0: val[u] = 2; q.append(u)
    res = {}
    r = nid[start]
    for ci, c in enumerate(ctxs):
        for stm in (0, 1):
            v = val[sidx(stm, ci, r)]
            res[(c, stm)] = "D" if v == 0 else ("W" if (v == 1) == (stm == 0) else "L")
    return res

def solve_abstract(zname):
    Z = ZSTR[zname]; states = list(Z.keys()); ctxs = contexts(); cid = {c: i for i, c in enumerate(ctxs)}
    n = len(states); nid = {s: i for i, s in enumerate(states)}
    def sidx(stm, ci, ni): return (stm * len(ctxs) + ci) * n + ni
    S = 2 * len(ctxs) * n; succ = [None] * S
    for stm in (0, 1):
        for ci, (a, b, c) in enumerate(ctxs):
            for ni, x in enumerate(states):
                lst = [sidx(1 - stm, ci, nid[o]) for o in Z[x][stm]]
                mine = a if stm == 0 else b
                if mine > 0:
                    na, nb = (a - 1, b) if stm == 0 else (a, b - 1)
                    lst.append(sidx(1 - stm, cid[(na, nb, c)], ni))
                if c > 0: lst.append(sidx(1 - stm, cid[(a, b, c - 1)], ni))
                succ[sidx(stm, ci, ni)] = lst
    preds = [[] for _ in range(S)]; cnt = [len(x) for x in succ]
    for s in range(S):
        for t in succ[s]: preds[t].append(s)
    val = [0] * S; q = [s for s in range(S) if cnt[s] == 0]
    for s in q: val[s] = 2
    qi = 0
    while qi < len(q):
        v = q[qi]; qi += 1
        for u in preds[v]:
            if val[u]: continue
            if val[v] == 2: val[u] = 1; q.append(u)
            else:
                cnt[u] -= 1
                if cnt[u] == 0: val[u] = 2; q.append(u)
    res = {}
    for ci, c in enumerate(ctxs):
        for stm in (0, 1):
            v = val[sidx(stm, ci, 0)]
            res[(c, stm)] = "D" if v == 0 else ("W" if (v == 1) == (stm == 0) else "L")
    return res

if __name__ == "__main__":
    ABS = {x: solve_abstract(x) for x in ZSTR}
    for pos in sys.argv[7:]:
        root = parse(pos); start, opts = group_graph(root)
        res = solve_group_sum(start, opts)
        line = [pos, f"nodes={len(opts)}"]
        for x in ZSTR:
            bad = [k for k in res if res[k] != ABS[x][k]]
            line.append(f"{x}:{'EQ' if not bad else str(len(bad)) + 'diff'}")
        print("  ".join(line), flush=True)
        if "-v" in sys.argv[0:0]: pass
        # show first few differences from dud
        bad = [(k, res[k], ABS['dud'][k]) for k in res if res[k] != ABS['dud'][k]]
        for k, a, b in bad[:6]: print("    ctx(a,b,c)=%s stm=%s group=%s dud=%s" % (k[0], "wb"[k[1]], a, b))
