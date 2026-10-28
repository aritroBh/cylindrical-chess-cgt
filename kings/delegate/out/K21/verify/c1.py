import sys, random, json, itertools, time
sys.path.insert(0,'.')
from ref import *
from tests1 import rnd_comp
from tests2 import dres
def run(seed, N, B):
    rng = random.Random(seed); st = dict(T_states=0, T_fail=0, T_fail_crit=0, T_crit_states=0, T_fail_inst=0, regime_viol=0, forced_states=0)
    ex = None
    for it in range(N):
        K = [rnd_comp(rng, 3, short=True) for _ in range(rng.choice((1, 2)))]
        S = rnd_comp(rng, 4, terms=False)
        if not S.is_stopper(): continue
        comps = K + [S]
        _, dS = dres(comps); _, dOn = dres(K + [ON()]); _, dOff = dres(K + [OFF()])
        crit = criterion(comps, B)
        Ys = list(itertools.product(*[c.reach() for c in K]))
        sts = [(tuple(('n', y) for y in Y + (s,)), m) for Y in Ys for s in S.reach() for m in (0, 1)]
        cs = cgt_solve(comps, B, sts)
        failed = False
        for Y in Ys:
            for s in S.reach():
                for m in (0, 1):
                    d = dS[(Y + (s,), m)]; k0 = Y + (0,)
                    PL = dOff[(k0, m)] == 'W'; PR = dOn[(k0, m)] == 'L'
                    tr = outcome(*cs[(tuple(('n', y) for y in Y + (s,)), m)])
                    if PL or PR:
                        st['forced_states'] += 1
                        if d != ('W' if PL else 'L'): st['regime_viol'] += 1
                    else:
                        st['T_states'] += 1
                        if crit: st['T_crit_states'] += 1
                        if tr != d:
                            st['T_fail'] += 1; failed = True
                            if crit: st['T_fail_crit'] += 1
                            if ex is None or (len(str(ex)) > len(str((K, S)))): ex = (K, S, Y, s, m, d, tr)
        st['T_fail_inst'] += failed
    return st, ex
if __name__ == '__main__':
    t = time.time(); st, ex = run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    print(json.dumps(st), "%.0fs" % (time.time() - t)); print(ex)
