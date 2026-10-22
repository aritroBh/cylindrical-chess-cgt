"""Independent second implementation of the product solver (naive Kleene iteration).

Shares only the chess move generator with product.py.  Successors are rebuilt from
solver.moves()/in_check() directly (no CSR, no predecessor lists, no counters), and the least fixed
point is found by sweeping until nothing changes:
    mover wins  if some successor is a win for him;   mover loses if all successors lose
    (including the case of no successor at all);       everything else stays a draw.
"""

from kings.ref.solve import make_solver


def naive_results(solver, starts, T):
    """starts: list of chess positions.  Returns {(pos, side-to-move-at-start): 'W'|'D'|'L'} for
    (pos, T.start)."""
    succ = {}
    todo = [(p, T.start) for p in starts]
    seen = set(todo)
    while todo:
        st = todo.pop()
        pos, t = st
        s = pos[0]
        _, quiet, exits = solver.moves(pos, full=True)
        out = [(q, t) for q in quiet] + [(q, t) for _, q in exits]
        if not solver.in_check(pos):
            fp = (1 - s,) + pos[1:]
            out += [(fp, t2) for t2 in T.opts(s)[t]]
        succ[st] = out
        for o in out:
            if o not in seen:
                seen.add(o)
                todo.append(o)
    win = {}                                  # state -> True if mover wins, False if mover loses
    changed = True
    while changed:
        changed = False
        for st, out in succ.items():
            if st in win:
                continue
            if any(win.get(o) is False for o in out):
                win[st] = True
                changed = True
            elif all(win.get(o) is True for o in out):      # also true for out == []
                win[st] = False
                changed = True
    res = {}
    for st in succ:
        if st[1] != T.start:
            continue
        w = win.get(st)
        if w is None:
            res[st[0]] = 'D'
        else:
            mover_white = st[0][0] == 0
            res[st[0]] = 'W' if w == mover_white else 'L'
    return res
