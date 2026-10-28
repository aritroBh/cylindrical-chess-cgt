import sys, itertools, json, time, random
sys.path.insert(0,'.')
from ref import *
def subsets(xs):
    for r in range(len(xs)+1):
        for c in itertools.combinations(xs, r): yield list(c)
def all1():
    out = []
    for l in subsets([0,'P','M']):
        for r in subsets([0,'P','M']):
            out.append(G([l],[r]))
    return out
def check(comps, B, st):
    dom = dominance(comps, B); cr = criterion(comps, B)
    Ys = reach_tuples(comps)
    ds = d_results(comps, [(Y, m) for Y in Ys for m in (0, 1)])
    cs = cgt_solve(comps, B, [(tuple(('n', y) for y in Y), m) for Y in Ys for m in (0, 1)])
    eq = all(outcome(*ds[(Y, m)]) == outcome(*cs[(tuple(('n', y) for y in Y), m)]) for Y in Ys for m in (0, 1))
    hasev = any(c.events() for c in comps)
    st['n'] += 1
    if cr and not dom: st['crit_not_dom'] += 1; print("CRIT-NOT-DOM", comps, B)
    if dom and not eq: st['dom_not_eq'] += 1; print("DOM-NOT-EQ", comps, B)
    if dom and hasev: st['dom_ev'] += 1
    if cr and hasev: st['crit_ev'] += 1
    if dom and not cr: st['dom_nocrit'] += 1
    if not dom and eq: st['nondom_eq'] += 1
    return
if __name__ == '__main__':
    mode = sys.argv[1]; B = int(sys.argv[2])
    st = dict(n=0, crit_not_dom=0, dom_not_eq=0, dom_ev=0, crit_ev=0, dom_nocrit=0, nondom_eq=0)
    A = all1(); t = time.time()
    if mode == 'pairs':
        for a, b in itertools.combinations_with_replacement(A, 2): check([a, b], B, st)
    elif mode == 'triples':
        for a, b, c in itertools.combinations_with_replacement(A, 3): check([a, b, c], B, st)
    elif mode == 'p2':   # 1-node x random 2-node
        rng = random.Random(int(sys.argv[3]))
        opts = [0,1,'P','M']
        for it in range(int(sys.argv[4])):
            L = [[o for o in opts if rng.random()<.35] for _ in range(2)]; R = [[o for o in opts if rng.random()<.35] for _ in range(2)]
            g2 = G(L, R); a = rng.choice(A)
            check([a, g2], B, st)
    print(mode, B, json.dumps(st), "%.0fs" % (time.time()-t))
