"""K32 implementation P (Python): own enumerator, own stopper test, K21's solver (dsum.py: solve, reserves) for the sums.
Usage: pyref.py N  -> enumerates ALL labeled graphs on N nodes (2^(2N^2), N <= 3), keeps stoppers, groups every node's reachable
subgraph into isomorphism classes (canonical = lexicographic minimum over relabelings fixing the root), evaluates each class once.
Writes classes to stdout as lines  'key | lam rho LS RS'  (stops in sixteenths, +inf/-inf), and the class counts per size to stderr.
Also usable as a module: evaluate(L, R, root) -> dict."""
import sys, itertools
from fractions import Fraction
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K21/scripts")
from dsum import Comp, solve, reserves

K = 5          # grid 1/32 (as in B); coarse = 1/16
INF, NINF = "+inf", "-inf"

def is_stopper(L, R):
    n = len(L)
    # state (i, m): m = 0 Left to move.  detect a cycle by repeated peeling of states with no live successor
    alive = {(i, m) for i in range(n) for m in (0, 1)}
    changed = True
    while changed:
        changed = False
        for (i, m) in list(alive):
            opts = L[i] if m == 0 else R[i]
            if not any((j, 1 - m) in alive for j in opts):
                alive.discard((i, m)); changed = True
    return not alive

def reach(L, R, root):
    seen = [root]; st = [root]
    while st:
        x = st.pop()
        for o in L[x] + R[x]:
            if o not in seen:
                seen.append(o); st.append(o)
    return seen

def canon(L, R, root):
    r = reach(L, R, root)
    others = [x for x in r if x != root]
    best = None
    for perm in itertools.permutations(others):
        order = [root] + list(perm)
        mp = {x: i for i, x in enumerate(order)}
        enc = tuple((tuple(sorted(mp[o] for o in L[x])), tuple(sorted(mp[o] for o in R[x]))) for x in order)
        if best is None or enc < best:
            best = enc
    return best

def numbers(M):
    vals = [Fraction(m, 1 << K) for m in range(-M * (1 << K), M * (1 << K) + 1)]
    idx = {v: i for i, v in enumerate(vals)}
    Lo, Ro = [], []
    for v in vals:
        if v == 0:
            Lo.append([]); Ro.append([])
        elif v.denominator == 1:
            if v > 0: Lo.append([idx[v - 1]]); Ro.append([])
            else: Lo.append([]); Ro.append([idx[v + 1]])
        else:
            h = Fraction(1, v.denominator)
            Lo.append([idx[v - h]]); Ro.append([idx[v + h]])
    return vals, idx, Comp(Lo, Ro, 0)

_num_cache = {}

def evaluate_key(key):
    """key = canonical encoding ((Lset, Rset), ...) root = 0.  Returns (lam, rho, LS, RS) at the root, sixteenths."""
    n = len(key)
    L = [list(a) for a, b in key]; R = [list(b) for a, b in key]
    comp = Comp(L, R, 0)
    Cmax = n + 2
    lam, rho = reserves(comp, 1, Cmax)
    M = n + 1
    if M not in _num_cache:
        _num_cache[M] = numbers(M)
    vals, idx, N = _num_cache[M]
    nodes = comp.reach()
    roots = [(y, i) for y in nodes for i in range(len(vals))]
    res = solve([comp, N], roots)
    def Lsec(y, x): return res[((y, idx[-x]), 1)] == "W"
    def Lfirst(y, x): return res[((y, idx[-x]), 0)] == "W"
    # D2
    def sup(f, y):
        top, bot = vals[-1], vals[0]
        if f(y, top): return INF
        if not f(y, bot): return NINF
        xm = max(x for x in vals if f(y, x))
        m = xm * (1 << K)          # integer, units of 1/32
        m = int(m)
        r = m if m % 2 == 0 else m + 1
        return r // 2
    LS2 = {y: sup(Lfirst, y) for y in nodes}; RS2 = {y: sup(Lsec, y) for y in nodes}
    # D1
    eq = {}
    for y in nodes:
        e = [x for x in vals if Lsec(y, x) and not Lfirst(y, x)]
        assert len(e) <= 1
        eq[y] = e[0] if e else None
    memo = {}
    def stop(side, y):
        k = (side, y)
        if k in memo: return memo[k]
        if eq[y] is not None:
            v = eq[y] * 16
            assert v.denominator == 1; v = int(v)
        elif side == 0:
            v = max([stop(1, j) for j in L[y]] or [NINF], key=lambda t: (-10**9 if t == NINF else 10**9 if t == INF else t))
        else:
            v = min([stop(0, j) for j in R[y]] or [INF], key=lambda t: (-10**9 if t == NINF else 10**9 if t == INF else t))
        memo[k] = v; return v
    out = {"lam": lam[0], "rho": rho[0], "LS": stop(0, 0), "RS": stop(1, 0), "LS2": LS2[0], "RS2": RS2[0]}
    return out

def fmt(v):
    return v if isinstance(v, str) else "%d/16" % v

def main():
    N = int(sys.argv[1])
    classes = {}
    cnt_graphs = 0
    for n in range(1, N + 1):
        pairs = list(itertools.product(range(1 << n), repeat=2))
        for combo in itertools.product(pairs, repeat=n):
            L = [[j for j in range(n) if a >> j & 1] for a, b in combo]
            R = [[j for j in range(n) if b >> j & 1] for a, b in combo]
            if not is_stopper(L, R): continue
            cnt_graphs += 1
            for root in range(n):
                k = canon(L, R, root)
                classes.setdefault(k, None)
    sizes = {}
    for k in classes: sizes[len(k)] = sizes.get(len(k), 0) + 1
    print("classes by number of reachable nodes:", dict(sorted(sizes.items())), file=sys.stderr)
    for k in sorted(classes, key=lambda k: (len(k), k)):
        r = evaluate_key(k)
        flag = "" if (r["LS"] == r["LS2"] and r["RS"] == r["RS2"]) else " !D1D2"
        print("%s | %s %s %s %s%s" % (k, r["lam"] if r["lam"] is not None else "inf", r["rho"] if r["rho"] is not None else "inf", fmt(r["LS"]), fmt(r["RS"]), flag))

if __name__ == "__main__":
    main()
