import sys, random, json, time, itertools
sys.path.insert(0,'.')
from ref import *
from tests1 import rnd_comp

def dres(comps, ts=None):
    Ys = reach_tuples(comps)
    ds = d_results(comps, [(Y, m) for Y in Ys for m in (0, 1)])
    return Ys, {k: outcome(*v) for k, v in ds.items()}

def sandwich(seed, N):
    rng = random.Random(seed); viol = 0; states = 0; nontriv = 0; suic = 0
    for it in range(N):
        K = [rnd_comp(rng, 3, short=(rng.random() < .4)) for _ in range(rng.choice((1, 2)))]
        kind = rng.choice(['named', 'quiet', 'suicide', 'stopper'])
        if kind == 'named': S = rng.choice([ON(), OFF(), DUD(), OVER(), UNDER()])
        else:
            S = rnd_comp(rng, 4, terms=False)
            if kind == 'suicide':
                n = S.n
                for x in range(n):
                    if rng.random() < .4: S.L[x].append('M')
                    if rng.random() < .4: S.R[x].append('P')
                suic += 1
            if kind == 'stopper' and not S.is_stopper(): continue
        assert all('P' not in S.L[x] and 'M' not in S.R[x] for x in range(S.n))
        Ys, dS = dres(K + [S]); _, dOn = dres(K + [ON()]); _, dOff = dres(K + [OFF()]); _, dDud = dres(K + [DUD()])
        for Y in itertools.product(*[c.reach() for c in K]):
            for s in S.reach():
                for m in (0, 1):
                    t = Y + (s,); t0 = Y + (0,)
                    a, on, off, dud = dS[(t, m)], dOn[(t0, m)], dOff[(t0, m)], dDud[(t0, m)]
                    states += 1
                    ok = True
                    Wm = lambda r: r == 'W'; Lm = lambda r: r == 'L'
                    if Wm(off) and not Wm(a): ok = False
                    if Wm(a) and not Wm(on): ok = False
                    if Lm(on) and not Lm(a): ok = False
                    if Lm(a) and not Lm(off): ok = False
                    if Wm(off) != Wm(dud): ok = False
                    if Lm(on) != Lm(dud): ok = False
                    if not ok:
                        viol += 1; print("VIOL", K, S, Y, s, m, a, on, off, dud)
                    if (Wm(on) and not Wm(off)) or (Lm(off) and not Lm(on)): nontriv += 1
    return dict(instances=N, states=states, viol=viol, nontrivial=nontriv, suicide_instances=suic)

def pure(seed, N, B):
    rng = random.Random(seed); n = 0; cnt = dict(viol=0, on_right_in_PL=0, off_right_in_PR=0, total=0, on_wrong=0)
    for it in range(N):
        K = [rnd_comp(rng, 4, short=True) for _ in range(rng.choice((1, 2)))]
        Ys = reach_tuples(K)
        _, dOn = dres(K + [ON()]); _, dOff = dres(K + [OFF()]); _, dDud = dres(K + [DUD()])
        for nm, X in (('on', ON()), ('off', OFF()), ('dud', DUD())):
            cs = cgt_solve(K + [X], B, [(tuple(('n', y) for y in Y) + (('n', 0),), m) for Y in Ys for m in (0, 1)])
            for Y in Ys:
                for m in (0, 1):
                    t = tuple(('n', y) for y in Y) + (('n', 0),)
                    tr = outcome(*cs[(t, m)])
                    exp = {'on': 'W', 'off': 'L', 'dud': 'D'}[nm]
                    if tr != exp: cnt['viol'] += 1
                    D = {'on': dOn, 'off': dOff, 'dud': dDud}[nm][(Y + (0,), m)]
                    PL = dOff[(Y + (0,), m)] == 'W'; PR = dOn[(Y + (0,), m)] == 'L'
                    cnt['total'] += 1
                    right = (tr == D)
                    claim = {'on': not PR, 'off': not PL, 'dud': not (PL or PR)}[nm]
                    if right != claim: cnt['viol'] += 1
                    if nm == 'on' and right and PL: cnt['on_right_in_PL'] += 1
                    if nm == 'off' and right and PR: cnt['off_right_in_PR'] += 1
    return cnt

def stopper_nodraw(seed, N):
    rng = random.Random(seed); st = dict(inst=0, draws=0, nonstopper_inst=0, nonstopper_draw_inst=0)
    for it in range(N):
        S = rnd_comp(rng, 4)
        K = [rnd_comp(rng, 3, short=True) for _ in range(rng.choice((1, 2)))]
        _, d = dres(K + [S])
        has_draw = any(v == 'D' for v in d.values())
        if S.is_stopper():
            st['inst'] += 1
            if has_draw: st['draws'] += 1
        else:
            st['nonstopper_inst'] += 1
            if has_draw: st['nonstopper_draw_inst'] += 1
    return st

def M(c, who):
    memo = {}
    def f(x):
        if x in memo: return memo[x]
        best = 0
        for o in c.L[x]:
            v = (1 if who == 0 else 0) + (0 if not isinstance(o, int) else f(o))
            best = max(best, v)
        for o in c.R[x]:
            v = (1 if who == 1 else 0) + (0 if not isinstance(o, int) else f(o))
            best = max(best, v)
        memo[x] = best; return best
    return f(0)

def thm111b(seed, N):
    rng = random.Random(seed); cnt = dict(safe=0, with_events=0, crit_fail=0, dom_fail=0, eq_fail=0)
    for it in range(N):
        comps = [rnd_comp(rng, 4, short=True) for _ in range(rng.choice((2, 3)))]
        ev = [c.events() for c in comps]
        if any('P' in ev[i] and 'M' in ev[j] for i in range(len(comps)) for j in range(len(comps)) if i != j): continue
        cnt['safe'] += 1
        B = max(sum(M(c, 0) for c in comps), sum(M(c, 1) for c in comps)) + 1
        if any(ev): cnt['with_events'] += 1
        if not criterion(comps, B): cnt['crit_fail'] += 1
        if not dominance(comps, B): cnt['dom_fail'] += 1
        Ys = reach_tuples(comps)
        ds = d_results(comps, [(Y, m) for Y in Ys for m in (0, 1)])
        cs = cgt_solve(comps, B, [(tuple(('n', y) for y in Y), m) for Y in Ys for m in (0, 1)])
        if any(outcome(*ds[(Y, m)]) != outcome(*cs[(tuple(('n', y) for y in Y), m)]) for Y in Ys for m in (0, 1)): cnt['eq_fail'] += 1
    return cnt

def lam_tuple(comps, B, node_tuple, cap, who):
    cs = comps + [G([[]], [[]])]
    sts = []
    for C in range(cap + 1):
        t = tuple(('n', x) for x in node_tuple)
        if who == 0: sts.append((t + (('P', C),), 1))
        else: sts.append((t + (('M', C),), 0))
    res = cgt_solve(cs, B, sts)
    for C in range(cap + 1):
        r = res[sts[C]]
        if (who == 0 and r[0]) or (who == 1 and r[1]): return C
    return None

def subadd(seed, N, B):
    rng = random.Random(seed); chk = 0; viol = 0
    for it in range(N):
        a = rnd_comp(rng, 3); b = rnd_comp(rng, 3)
        cap = 20
        for who in (0, 1):
            la = lam_tuple([a], B, (0,), cap, who); lb = lam_tuple([b], B, (0,), cap, who)
            lab = lam_tuple([a, b], B, (0, 0), 2 * cap, who)
            chk += 1
            if la is not None and lb is not None:
                if lab is None or lab > la + lb: viol += 1; print("SUBADD VIOL", a, b, who, la, lb, lab)
    return dict(checks=chk, viol=viol)

def onestopper(seed, N):
    rng = random.Random(seed); cnt = dict(inst=0, events=0, crit_fail=0, eq_fail=0, skipped_inf=0)
    for it in range(N):
        S = rnd_comp(rng, 4, terms=False) if rng.random() < .8 else rng.choice([OVER(), UNDER()])
        K = [rnd_comp(rng, 3, short=True) for _ in range(rng.choice((1, 2)))]
        evs = [c.events() for c in K]
        if any('P' in evs[i] and 'M' in evs[j] for i in range(len(K)) for j in range(len(K)) if i != j): continue
        Lam, Rho, _ = big_lam_rho(S, 1)
        if Lam is None or Rho is None: cnt['skipped_inf'] += 1; continue
        B = 1 + max(Lam, Rho) + max(sum(M(c, 0) for c in K), sum(M(c, 1) for c in K))
        comps = [S] + K
        cnt['inst'] += 1
        if any(evs): cnt['events'] += 1
        if not criterion(comps, B): cnt['crit_fail'] += 1
        Ys = reach_tuples(comps)
        ds = d_results(comps, [(Y, m) for Y in Ys for m in (0, 1)])
        cs = cgt_solve(comps, B, [(tuple(('n', y) for y in Y), m) for Y in Ys for m in (0, 1)])
        if any(outcome(*ds[(Y, m)]) != outcome(*cs[(tuple(('n', y) for y in Y), m)]) for Y in Ys for m in (0, 1)): cnt['eq_fail'] += 1
    return cnt

if __name__ == '__main__':
    which = sys.argv[1]; args = [int(a) for a in sys.argv[2:]]
    t = time.time()
    print(which, args, json.dumps(globals()[which](*args)), "time %.0fs" % (time.time() - t))
