"""K62 referee: checks of Theorem 4.20 / Proposition 4.21 on families and on random exact groups.

Usage (from the repository root):
  .venv/bin/python kings/delegate/out/K62/verify/src/chk62.py families
  .venv/bin/python kings/delegate/out/K62/verify/src/chk62.py random SEED COUNT
  .venv/bin/python kings/delegate/out/K62/verify/src/chk62.py climb SEED ITERS MODE
"""
import random
import sys
import time

from ref62 import (Group, WHITE as Wh, BLACK as Bl, W_, D_, L_, exact, x_of, S_sets, PE, F0_set, aux_wins,
                   white_ep_promotes, sum_values, ladder, surv_under)
import fam62

INF = 10 ** 9


def analyse(G, reading='strict', m2=False, extra_n=2):
    ok, info = exact(G, reading, m2)
    if not ok:
        return None, info
    b = G.nb
    K = G.ns
    nmax = K + extra_n
    S = S_sets(G, nmax)
    F0 = F0_set(G)
    AW = aux_wins(G)
    viol = []
    for n in range(nmax):
        if not S[n + 1] <= S[n]:
            viol.append('S not decreasing at %d' % n)
    if S[K] != S[K + 1]:
        viol.append('S not stable at K')
    epP = white_ep_promotes(G)
    rows = []
    for r, m in info['bad']:
        x = x_of(G, r, m)
        Nstar = next((n for n in range(nmax + 1) if x not in S[n]), INF)
        aux = x in AW
        Z, P, E = PE(G, x, F0)
        X = P - E
        Sinf_b = set(g for g in range(b) if G.si(g, 0, Bl) in S[nmax])
        bnd = len(P - (E | Sinf_b))
        if aux != (Nstar == INF):
            viol.append('aux vs ladder at %s' % ((r, m),))
        if Nstar < INF and Nstar > bnd:
            viol.append('N* > |P\\(E u Sinf)| at %s: %d > %d' % ((r, m), Nstar, bnd))
        if bnd > len(X) or len(X) > b:
            viol.append('bound chain')
        if not epP and len(X) > b - 1:
            viol.append('|P\\E| = %d > b - 1 without e.p. promotion' % len(X))
        if (x in S[len(X)]) != aux:
            viol.append('x in S_|P\\E| vs aux at %s' % ((r, m),))
        vN = None
        if Nstar < INF:
            T = ladder(Nstar)
            vN = sum_values(G, T)[x * T.n]
        rows.append(dict(r=r, m=m, x=x, Nstar=Nstar, aux=aux, P=len(P), E=len(E), X=len(X), bnd=bnd, vN=vN))
    # Theorem 4.20(d): root test beside T_b (T_{b-1} without White e.p. promotions) iff Aux at every bad move
    allaux = all(row['aux'] for row in rows)
    for n in ([b] + ([b - 1] if not epP else [])):
        T = ladder(n)
        v = sum_values(G, T)
        rt = all(v[G.si(r, 0, Bl) * T.n] == W_ for r in (0, 1))
        if rt != allaux:
            viol.append('root test beside T_%d disagrees with Aux' % n)
    return dict(rows=rows, viol=viol, b=b, epP=epP, info=info), info


def fmt(v):
    return 'inf' if v == INF else str(v)


def families():
    out = []
    groups = []
    groups.append(fam62.gamma2(0, endP=True))
    for k in range(0, 5):
        groups.append(fam62.gamma2(k))
    for k in range(1, 5):
        groups.append(fam62.gamma2(k, 'A'))
        groups.append(fam62.gamma2(k, 'AB'))
    groups.append(fam62.gamma2(2, 'AB', a_c1_in_AB=True))
    groups.append(fam62.gamma0('A'))
    groups.append(fam62.gamma0('AB'))
    groups.append(fam62.pi(0, endP=True))
    for k in range(0, 5):
        groups.append(fam62.pi(k))
    for k in range(1, 5):
        groups.append(fam62.pi(k, 'A'))
        groups.append(fam62.pi(k, 'AB'))
    groups.append(fam62.pi_self(3))
    groups.append(fam62.pi_self(4))
    for N in range(1, 7):
        groups.append(fam62.lam(N))
    groups.append(fam62.three_literal())
    groups.append(fam62.delta4())
    nviol = 0
    for G, mm in groups:
        line = []
        for reading in ('strict', 'literal'):
            for m2 in (False, True):
                ok, info = exact(G, reading, m2)
                line.append('%s%s=%s' % (reading[0], '2' if m2 else '1', 'Y' if ok else 'n'))
        res, info = analyse(G, 'literal')
        if res is None:
            print('%-26s b=%2d NOT EXACT (literal): %s' % (G.name, G.nb, info['why']))
            continue
        nviol += len(res['viol'])
        su = surv_under(G)
        for row in res['rows']:
            tag = '*' if (row['r'], row['m']) == mm else ' '
            vN = {None: '-', W_: 'W', D_: 'D', L_: 'L'}[row['vN']]
            uv = {W_: 'W', D_: 'D', L_: 'L'}[su[row['x']]]
            print('%-26s b=%2d %s %s m=%s->%s N*=%s aux=%d |P|=%d |E|=%d |P\\E|=%d bnd=%d v(T_N*)=%s under=%s'
                  % (G.name, G.nb, ' '.join(line), tag, row['r'], row['m'], fmt(row['Nstar']), row['aux'],
                     row['P'], row['E'], row['X'], row['bnd'], vN, uv))
        for v in res['viol']:
            print('   VIOLATION', v)
    print('families: %d groups, %d violations' % (len(groups), nviol))


# ---------------------------------------------------------------- random exact groups
def rand_group(rng, b, nq, pchk, pdbl, pep, pprom, strict, m2, maxdeg=3, bias=False):
    A, B = 0, 1
    Q = list(range(2, 2 + nq))
    O = list(range(2 + nq, b))
    chk = [[False, False] for _ in range(b)]
    for g in O:
        chk[g] = [rng.random() < pchk, rng.random() < pchk]
    protected = set([A, B] + Q)

    def rmove(g, s, allow_prom):
        if allow_prom and rng.random() < pprom:
            return 'P'
        while True:
            g2 = rng.randrange(b)
            if m2 and g2 == g:
                continue
            return (g2, rng.random() < pdbl)

    mv0, ep = {}, {}
    for g in range(b):
        for s in (Wh, Bl):
            allow = not (strict and g in protected)
            lst = []
            for _ in range(rng.choice([1, 1, 2, 2, 3][:maxdeg + 2])):
                mv = rmove(g, s, allow)
                if m2 and mv in lst:
                    continue
                lst.append(mv)
            mv0[(g, s)] = lst
            if rng.random() < pep:
                e = rmove(g, s, allow and True)
                if not (m2 and e in lst):
                    ep[(g, s)] = [e]
    mv0[(A, Bl)] = [(B, False)] + [m for m in mv0[(A, Bl)] if m != (B, False)]
    mv0[(B, Bl)] = [(A, False)] + [m for m in mv0[(B, Bl)] if m != (A, False)]
    for r in (A, B):
        fz = (rng.choice(Q), rng.random() < pdbl)
        if fz not in mv0[(r, Wh)]:
            mv0[(r, Wh)].append(fz)
    if bias:
        # counter-like structure: White's moves off the roots mostly go to a q-board,
        # Black's moves there mostly walk among the other boards and the roots
        for g in O:
            if rng.random() < 0.7:
                mv0[(g, Wh)] = [(rng.choice(Q), False)] + mv0[(g, Wh)][:rng.randint(0, 1)]
            if rng.random() < 0.7:
                mv0[(g, Bl)] = [(rng.choice(O + [A, B] + Q), False)]
                if m2 and mv0[(g, Bl)][0][0] == g:
                    mv0[(g, Bl)] = [(A, False)]
    # repair
    for _ in range(30):
        G = Group(b, chk, mv0, ep)
        from ref62 import p_values
        P = p_values(G)

        def loses(m, s):
            if m == 'P':
                return False
            v = P[G.succ_state(m, s)]
            return v == (L_ if s == Wh else W_)

        changed = False
        for r, o in ((A, B), (B, A)):
            lst = mv0[(r, Bl)]
            new = [lst[0]] + [m for m in lst[1:] if loses(m, Bl)]
            if new != lst:
                mv0[(r, Bl)] = new
                changed = True
        fzs = []
        for r in (A, B):
            lst = mv0[(r, Wh)]
            new = [m for m in lst if m != 'P' and (loses(m, Wh) or m[0] in Q)]
            if new != lst:
                mv0[(r, Wh)] = new
                changed = True
            fzs += [m for m in new if not loses(m, Wh)]
        if not fzs:
            return None
        for q, dbl in set(fzs):
            # Black at (q, dbl): mv0 moves (and e.p. moves if dbl) must lose at once
            lst = mv0.get((q, Bl), [])
            new = [m for m in lst if loses(m, Bl)]
            if new != lst:
                mv0[(q, Bl)] = new
                changed = True
            if dbl:
                lst = ep.get((q, Bl), [])
                new = [m for m in lst if loses(m, Bl)]
                if new != lst:
                    ep[(q, Bl)] = new
                    changed = True
            lst = mv0.get((q, Wh), [])
            new = [m for m in lst if loses(m, Wh)]
            if new != lst:
                mv0[(q, Wh)] = new
                changed = True
        if not changed:
            return G
    return None


MODELS = {'plain': (0.0, 0.0, 0.0), 'checks': (0.35, 0.0, 0.0), 'ep': (0.0, 0.35, 0.4), 'checks+ep': (0.35, 0.35, 0.4)}


def random_run(seed, count):
    rng = random.Random(seed)
    t0 = time.time()
    stats = dict(groups=0, bad=0, fail=0, viol=0, tries=0, withchk=0, withep=0, dbl_bad=0, epP=0)
    hist = {}
    slack = {}
    per = {}
    while stats['groups'] < count:
        stats['tries'] += 1
        model = rng.choice(list(MODELS))
        pchk, pdbl, pep = MODELS[model]
        b = rng.randint(4, 9)
        nq = 1 if b < 6 else rng.choice([1, 2])
        strict = rng.random() < 0.5
        m2 = rng.random() < 0.5
        bias = rng.random() < 0.5
        G = rand_group(rng, b, nq, pchk, pdbl, pep, rng.choice([0.15, 0.25, 0.4]), strict, m2, bias=bias)
        if G is None:
            continue
        reading = 'strict' if strict else 'literal'
        res, info = analyse(G, reading, m2)
        if res is None:
            continue
        stats['groups'] += 1
        per[(model, reading, m2)] = per.get((model, reading, m2), 0) + 1
        if any(c[0] or c[1] for c in G.chk):
            stats['withchk'] += 1
        if any(G.ep_only(g, s) for g in range(G.nb) for s in (0, 1)):
            stats['withep'] += 1
        stats['epP'] += res['epP']
        for row in res['rows']:
            stats['bad'] += 1
            if row['m'][1]:
                stats['dbl_bad'] += 1
            if row['Nstar'] < INF:
                stats['fail'] += 1
                hist[row['Nstar']] = hist.get(row['Nstar'], 0) + 1
                key = (row['Nstar'], row['bnd'], row['X'], G.nb)
                slack[key] = slack.get(key, 0) + 1
        if res['viol']:
            stats['viol'] += len(res['viol'])
            print('VIOLATION', G.name, G.nb, res['viol'], G.mv, G.chk)
    print('seed %d: %s' % (seed, stats))
    print('  N* histogram (failing bad moves):', dict(sorted(hist.items())))
    print('  (N*, |P\\(E u Sinf)|, |P\\E|, b) counts:', dict(sorted(slack.items())))
    print('  per (model, reading, M2):', dict(sorted(per.items())))
    print('  time %.1f s' % (time.time() - t0))


# ---------------------------------------------------------------- hill climbing
def mutate(rng, G, b, strict, m2, pdbl, pep_ok, chk_ok):
    mv0 = {k: list(G.mv[(k[0], 0, k[1])]) for k in [(g, s) for g in range(b) for s in (0, 1)]}
    ep = {(g, s): list(G.ep_only(g, s)) for g in range(b) for s in (0, 1)}
    chk = [list(c) for c in G.chk]
    protected = {0, 1, 2}
    g = rng.randrange(b)
    s = rng.randrange(2)
    kind = rng.random()
    target = ep if (pep_ok and rng.random() < 0.25) else mv0
    lst = target[(g, s)]
    if kind < 0.45 and lst:
        i = rng.randrange(len(lst))
        if target is mv0 and g in (0, 1) and s == Bl and i == 0:
            return None
        lst.pop(i)
    elif kind < 0.9:
        if rng.random() < 0.15 and not (strict and g in protected):
            mv = 'P'
        else:
            g2 = rng.randrange(b)
            if m2 and g2 == g:
                return None
            mv = (g2, pep_ok and rng.random() < pdbl)
        if m2 and mv in lst:
            return None
        lst.append(mv)
    elif chk_ok and g not in protected:
        chk[g][s] = not chk[g][s]
    return Group(b, chk, mv0, ep, filter_check=True)


def climb(seed, iters, mode):
    """mode: 'lit3' (literal, 3 boards, e.p.), 'm2ep4' (strict, M2, 4 boards, e.p.),
    'm2chk5' (strict, M2, 5 boards, checks, no e.p.), 'gen6' (strict, M1, 6 boards, checks + e.p.)."""
    rng = random.Random(seed)
    cfg = {'lit3': (3, 'literal', False, True, False), 'm2ep4': (4, 'strict', True, True, True),
           'm2chk5': (5, 'strict', True, False, True), 'gen6': (6, 'strict', False, True, True),
           'lit4': (4, 'literal', False, True, True), 'lit3m2': (3, 'literal', True, True, False),
           'm2bep4': (4, 'strict', 'board', True, True), 'm2bep5': (5, 'strict', 'board', True, True)}[mode]
    b, reading, m2, ep_ok, chk_ok = cfg
    best_overall = -1
    found = {}
    t0 = time.time()
    restarts = 0
    while time.time() - t0 < iters:
        restarts += 1
        G = None
        for _ in range(2000):
            pchk = 0.3 if chk_ok else 0.0
            pdbl, pep = (0.35, 0.5) if ep_ok else (0.0, 0.0)
            # literal: allow promotions anywhere; strict: not at protected boards (q-board = board 2)
            G = rand_group(rng, b, 1, pchk, pdbl, pep, 0.25, reading == 'strict', m2)
            if G is not None and exact(G, reading, m2)[0]:
                break
            G = None
        if G is None:
            continue

        def score(G):
            res, _ = analyse(G, reading, m2, extra_n=1)
            if res is None:
                return -1, None
            if res['viol']:
                print('VIOLATION', res['viol'], G.mv, G.chk)
            fin = [r['Nstar'] for r in res['rows'] if r['Nstar'] < INF]
            return (max(fin) if fin else 0), res

        cur, _ = score(G)
        for _ in range(300):
            H = mutate(rng, G, b, reading == 'strict', m2, 0.35, ep_ok, chk_ok)
            if H is None:
                continue
            sc, res = score(H)
            if sc >= cur and sc >= 0:
                G, cur = H, sc
                if sc not in found:
                    found[sc] = (dict((k, v) for k, v in G.mv.items() if v), [c for c in G.chk])
                    print('  mode %s: N* = %d reached (restart %d, %.0f s)' % (mode, sc, restarts, time.time() - t0))
        best_overall = max(best_overall, cur)
    print('climb %s seed %d: restarts %d, best N* %d, %.0f s' % (mode, seed, restarts, best_overall, time.time() - t0))
    for sc in sorted(found):
        if sc >= 3:
            print('  example with N* = %d: mv=%s chk=%s' % (sc, found[sc][0], found[sc][1]))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'families':
        families()
    elif cmd == 'random':
        random_run(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == 'climb':
        climb(int(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
