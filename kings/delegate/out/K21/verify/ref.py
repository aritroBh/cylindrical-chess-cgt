"""Referee's own independent implementation (K21 verify).  Not derived from K21/scripts.
Component = (L, R) where L[n], R[n] are lists of options; an option is an int node or 'P' (White-win terminal) or 'M' (Black-win terminal).
Root is node 0.
"""
import random, itertools, sys
from collections import defaultdict, deque

class G:
    def __init__(s, L, R):
        s.L = [list(x) for x in L]; s.R = [list(x) for x in R]; s.n = len(L)
    def reach(s):
        seen = {0}; st = [0]
        while st:
            x = st.pop()
            for o in s.L[x] + s.R[x]:
                if isinstance(o, int) and o not in seen:
                    seen.add(o); st.append(o)
        return sorted(seen)
    def events(s):
        ev = set()
        for x in s.reach():
            for o in s.L[x] + s.R[x]:
                if o in ('P', 'M'): ev.add(o)
        return ev
    def is_stopper(s):
        # (node, mover) graph acyclic from reachable nodes
        succ = {}
        for x in s.reach():
            succ[(x, 0)] = [(o, 1) for o in s.L[x] if isinstance(o, int)]
            succ[(x, 1)] = [(o, 0) for o in s.R[x] if isinstance(o, int)]
        color = {}
        sys.setrecursionlimit(10000)
        def dfs(v):
            color[v] = 1
            for w in succ[v]:
                if color.get(w, 0) == 1: return False
                if color.get(w, 0) == 0 and not dfs(w): return False
            color[v] = 2
            return True
        return all(color.get(v, 0) != 0 or dfs(v) for v in succ)
    def __repr__(s):
        return "G(L=%r,R=%r)" % (s.L, s.R)

def solve(states0, succ):
    """succ(state) -> (list_of_next_states, term) where term is a set of terminal results among options: 'LW','RW'.
    Returns dict state -> (Lwin, Rwin) as booleans, over all states reachable from states0.
    state = (payload, mover) with mover 0 = Left, 1 = Right. Least fixed point (finite-forced wins)."""
    info = {}
    todo = list(states0)
    while todo:
        s = todo.pop()
        if s in info: continue
        nxt, term = succ(s)
        info[s] = (nxt, term)
        for t in nxt:
            if t not in info: todo.append(t)
    pred = defaultdict(list)
    for s, (nxt, term) in info.items():
        for t in nxt: pred[t].append(s)
    res = {}
    for sigma in (0, 1):   # sigma = 0: Left is the winner, 1: Right
        win = set()
        cnt = {}
        q = deque()
        for s, (nxt, term) in info.items():
            mover = s[1]
            if mover == sigma:
                if ('LW' if sigma == 0 else 'RW') in term:
                    win.add(s); q.append(s)
            else:
                # opponent to move: wins iff all options are sigma-wins; opponent terminal win blocks
                badt = 'RW' if sigma == 0 else 'LW'
                if badt in term:
                    cnt[s] = None  # can never be a sigma win
                else:
                    c = len(nxt)   # terminal options (sigma's own result, i.e. suicide) are automatically fine
                    cnt[s] = c
                    if c == 0:
                        win.add(s); q.append(s)
        while q:
            t = q.popleft()
            for s in pred[t]:
                if s in win: continue
                if s[1] == sigma:
                    win.add(s); q.append(s)
                else:
                    if cnt[s] is None: continue
                    cnt[s] -= 1   # NB: multiplicity: each option listed once in nxt (we dedupe)
                    if cnt[s] == 0:
                        win.add(s); q.append(s)
        res[sigma] = win
    return {s: (s in res[0], s in res[1]) for s in info}

def outcome(lw, rw):
    return 'W' if lw else ('L' if rw else 'D')

# ---------- D sum ----------
def d_succ(comps):
    def f(state):
        t, mv = state
        nxt = set(); term = set()
        for i, c in enumerate(comps):
            opts = (c.L if mv == 0 else c.R)[t[i]]
            for o in opts:
                if o == 'P': term.add('LW')
                elif o == 'M': term.add('RW')
                else: nxt.add((t[:i] + (o,) + t[i+1:], 1 - mv))
        return sorted(nxt), term
    return f

def d_results(comps, starts=None):
    root = tuple(0 for _ in comps)
    starts = starts or [(root, 0), (root, 1)]
    return solve(starts, d_succ(comps))

# ---------- CGT translation ----------
# coordinate values: ('n', node) for original nodes; ('P', k) integer +k; ('M', k) integer -k
def c_succ(comps, B):
    def f(state):
        t, mv = state
        nxt = set()
        for i, c in enumerate(comps):
            v = t[i]
            if v[0] == 'n':
                opts = (c.L if mv == 0 else c.R)[v[1]]
                for o in opts:
                    if o == 'P': nv = ('P', B)
                    elif o == 'M': nv = ('M', B)
                    else: nv = ('n', o)
                    nxt.add((t[:i] + (nv,) + t[i+1:], 1 - mv))
            elif v[0] == 'P':
                if mv == 0 and v[1] >= 1:
                    nxt.add((t[:i] + (('P', v[1]-1),) + t[i+1:], 1 - mv))
            else:
                if mv == 1 and v[1] >= 1:
                    nxt.add((t[:i] + (('M', v[1]-1),) + t[i+1:], 1 - mv))
        return sorted(nxt), set()
    return f

def cgt_solve(comps, B, starts):
    return solve(starts, c_succ(comps, B))

def cgt_results(comps, B):
    root = tuple(('n', 0) for _ in comps)
    return cgt_solve(comps, B, [(root, 0), (root, 1)])

def reach_tuples(comps):
    return list(itertools.product(*[c.reach() for c in comps]))

# ---------- dominance ----------
def dominance(comps, B, return_witness=False):
    ev = []
    for Y in reach_tuples(comps):
        for j, c in enumerate(comps):
            for sg in ('P', 'M'):
                if any(sg in (c.L[Y[j]] + c.R[Y[j]]) for _ in [0]):
                    ev.append((Y, j, sg))
    starts = []
    for Y, j, sg in ev:
        t = tuple(('n', y) for y in Y)
        t = t[:j] + ((sg, B),) + t[j+1:]
        starts += [(t, 0), (t, 1)]
    if not starts: return True
    res = cgt_solve(comps, B, starts)
    for s in starts:
        lw, rw = res[s]
        # which sign?
        j = [i for i, v in enumerate(s[0]) if v[0] in ('P', 'M') and v[1] == B]
    # redo with sign knowledge
    k = 0
    for Y, j, sg in ev:
        for mv in (0, 1):
            lw, rw = res[starts[k]]; k += 1
            if sg == 'P' and not lw: return False
            if sg == 'M' and not rw: return False
    return True

# ---------- reserves ----------
def lam_rho(c, B, node, cap):
    """lambda_B(node), rho_B(node) for single component c (list [c]); inf = None"""
    lam = rho = None
    for C in range(cap + 1):
        s = ((('n', node), ('P', C)), 1)
        if cgt_solve([c, G([[]], [[]])], B, [((( 'n', node), ('P', C)), 1)]).get(s)[0] if False else False:
            pass
    return lam, rho

def reserves(c, B, cap=None):
    """returns dict node -> (lam, rho) with None = infinity. components in a 2-tuple: (c, token-component) where the token comp
    is an integer chain realised as the pair of coordinate 'P'/'M' values (we use a dummy 1-node component)."""
    dummy = G([[]], [[]])
    n = len(c.reach())
    cap = cap if cap is not None else 3 * (n + 1) + B + 4
    out = {}
    comps = [c, dummy]
    for x in c.reach():
        lam = rho = None
        sts = []
        for C in range(cap + 1):
            sts.append(((('n', x), ('P', C)), 1))   # Right moves first, Left tokens
            sts.append(((('n', x), ('M', C)), 0))   # Left moves first, Right tokens
        res = cgt_solve(comps, B, sts)
        for C in range(cap + 1):
            if lam is None and res[((('n', x), ('P', C)), 1)][0]: lam = C
            if rho is None and res[((('n', x), ('M', C)), 0)][1]: rho = C
        out[x] = (lam, rho)
    return out

def big_lam_rho(c, B, cap=None):
    r = reserves(c, B, cap)
    lams = [v[0] for v in r.values()]; rhos = [v[1] for v in r.values()]
    L = None if any(v is None for v in lams) else max(lams)
    P = None if any(v is None for v in rhos) else max(rhos)
    return L, P, r

def criterion(comps, B, cache=None):
    info = [big_lam_rho(c, B) for c in comps]
    for j, c in enumerate(comps):
        ev = c.events()
        for sg in ev:
            tot = 0; ok = True
            for i in range(len(comps)):
                if i == j: continue
                v = info[i][0] if sg == 'P' else info[i][1]
                if v is None: ok = False; break
                tot += v
            if not ok or tot > B - 1: return False
    return True

# ---------- named games ----------
def ON():  return G([[0]], [[]])
def OFF(): return G([[]], [[0]])
def DUD(): return G([[0]], [[0]])
def OVER(): return G([[1], []], [[0], []])   # over = {0 | over}: node0: L->node1(=0), R->node0
def UNDER(): return G([[0], []], [[1], []])
