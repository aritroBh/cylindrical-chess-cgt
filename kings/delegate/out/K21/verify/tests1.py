import sys, random, json, time
sys.path.insert(0,'.')
from ref import *

def rnd_comp(rng, maxn=4, short=False, pterm=0.25, popt=0.35, terms=True):
    n = rng.randint(1, maxn)
    L = []; R = []
    for x in range(n):
        l = []; r = []
        for side, out in ((0, l), (1, r)):
            cands = list(range(x+1, n)) if short else list(range(n))
            for y in cands:
                if rng.random() < popt: out.append(y)
            if terms:
                if rng.random() < pterm: out.append('P')
                if rng.random() < pterm: out.append('M')
        L.append(l); R.append(r)
    return G(L, R)

def bridge_test(seed, N, B, maxn=4, ncomp=(2,3)):
    rng = random.Random(seed)
    stats = dict(inst=0, dom=0, dom_eq=0, viol=0, crit=0, crit_dom_viol=0, nondom_neq=0, nondom_eq=0, loopy_dom=0)
    bad = []
    for it in range(N):
        k = rng.choice(ncomp)
        comps = [rnd_comp(rng, maxn, short=(rng.random() < 0.3)) for _ in range(k)]
        stats['inst'] += 1
        dom = dominance(comps, B)
        cr = criterion(comps, B)
        if cr and not dom:
            stats['crit_dom_viol'] += 1; bad.append(('crit-not-dom', comps, B))
        Ys = reach_tuples(comps)
        ds = d_results(comps, [(Y, m) for Y in Ys for m in (0, 1)])
        cs = cgt_solve(comps, B, [(tuple(('n', y) for y in Y), m) for Y in Ys for m in (0, 1)])
        eq = all(outcome(*ds[(Y, m)]) == outcome(*cs[(tuple(('n', y) for y in Y), m)]) for Y in Ys for m in (0, 1))
        if cr: stats['crit'] += 1
        if dom:
            stats['dom'] += 1
            if any(not c.is_stopper() or True for c in comps) and any(any(o in (c.L[x]+c.R[x]) for x in c.reach() for o in ('P','M')) for c in comps):
                pass
            if eq: stats['dom_eq'] += 1
            else: stats['viol'] += 1; bad.append(('dom-neq', comps, B))
        else:
            if eq: stats['nondom_eq'] += 1
            else: stats['nondom_neq'] += 1
    return stats, bad

if __name__ == '__main__':
    seed, N, B = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    t = time.time()
    st, bad = bridge_test(seed, N, B)
    print(json.dumps(st), "bad:", len(bad), "time %.0fs" % (time.time() - t))
    for b in bad[:3]: print(b)
