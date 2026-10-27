"""K19: own full-board solver of the promotion model P (Definition 1.5): kings move normally; the first
promotion ends the game and wins for the promoter (whatever happens to the new piece); checkmate loses for the
mover, stalemate draws, infinite play draws (least fixed point). Reachable-state retrograde analysis."""
from collections import deque
from k19engine import *

W_, L_, D_ = 'W', 'L', 'D'


def solve_p(B, roots, ep_on=True, max_states=3_000_000):
    idx = {}
    nodes = []
    succ = []
    term = []        # None, 'W' (promotion available), 'L' (mated), 'D' (stalemate)
    stack = []

    def get(pos):
        i = idx.get(pos)
        if i is None:
            i = len(nodes)
            idx[pos] = i
            nodes.append(pos)
            stack.append(i)
            if i > max_states:
                raise RuntimeError('too many states')
        return i

    for r in roots:
        get(r)
    while stack:
        i = stack.pop()
        pos = nodes[i]
        while len(succ) <= i:
            succ.append(None)
            term.append(None)
        mv = legal_moves(B, pos, ep_on)
        if any(m.kind == 'p' for m in mv):
            term[i] = 'W'
            succ[i] = []
            continue
        if not mv:
            term[i] = 'L' if in_check(B, pos) else 'D'
            succ[i] = []
            continue
        succ[i] = list({get(m.pos) for m in mv})
    n = len(nodes)
    pred = [[] for _ in range(n)]
    for i in range(n):
        for j in succ[i]:
            pred[j].append(i)
    val = [None] * n          # 'W','L' resolved; None = draw
    cnt = [len(succ[i]) for i in range(n)]
    work = deque()
    for i in range(n):
        if term[i] == 'W':
            val[i] = 'W'
            work.append(i)
        elif term[i] == 'L':
            val[i] = 'L'
            work.append(i)
    while work:
        j = work.popleft()
        for i in pred[j]:
            if val[i] is not None or term[i] is not None:
                continue
            if val[j] == 'L':
                val[i] = 'W'
                work.append(i)
            else:
                cnt[i] -= 1
                if cnt[i] == 0:
                    val[i] = 'L'
                    work.append(i)
    res = {}
    for r in roots:
        v = val[idx[r]]
        res[r] = v if v else 'D'
    return res, n


def white_pov(pos, v):
    """Result from White's point of view given the value for the side to move."""
    if v == 'D':
        return 'D'
    stm = pos[5]
    if stm == 0:
        return v
    return 'L' if v == 'W' else 'W'
