"""K62 question 1: ladder length. Usage (from the repository root):
  .venv/bin/python kings/delegate/out/K62/src/k62q1.py families
  .venv/bin/python kings/delegate/out/K62/src/k62q1.py random SEED COUNT
  .venv/bin/python kings/delegate/out/K62/src/k62q1.py search MODEL BOARDS SEED COUNT   (MODEL: plain | checks | ep)
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k62lib import (Group, W, B, exactness, x_of, aux_win, bound_data, value_G_T, ladder)  # noqa: E402
from k62families import ep_path, ep_path2, plain_path, plain_self, lam, three_board_literal, self_moves  # noqa: E402


def analyse(G, cap=None):
    """For every bad move: (bad, aux, N*, |P|, |P\\E|, |P\\(E u Sinf)|, value beside T_{N*})."""
    ok, info = exactness(G)
    if not ok:
        return None, info
    aux = aux_win(G)
    rows = []
    for bad in info['bad']:
        x = x_of(bad)
        bd = bound_data(G, x, cap)
        P, E, Si = set(bd['P']), set(bd['E']), set(bd['Sinf'])
        ns = bd['nstar']
        fail_val = None
        if ns is not None:
            fail_val = value_G_T(G, ladder(ns))[((x[0], x[1]), 0, W)]
        rows.append(dict(bad=bad, x=x, aux=(x in aux), nstar=ns, P=len(P), PE=len(P - E),
                         PES=len(P - E - Si), fail_val=fail_val, chain=bd['chain'], Sn=bd['Sn'], Z=bd['Z']))
    return rows, info


def families():
    out = []
    print('# Q1 families: model, construction, boards b, bad move, Aux, N*, |P|, |P-E|, |P-(E+Sinf)|, value at T_N*')
    cases = []
    cases.append(('ep', 'Gamma end=P (N*=1)', ep_path(0, False, False, 'P')))
    for k in range(0, 6):
        cases.append(('ep', 'Gamma(k=%d)' % k, ep_path(k, False, False)))
        cases.append(('ep', 'Gamma(k=%d,A)' % k, ep_path(k, True, False)))
        cases.append(('ep', 'Gamma(k=%d,AB)' % k, ep_path(k, True, True)))
    cases.append(('plain', 'Pi end=P (N*=1)', plain_path(0, '', 'P')))
    for k in range(0, 6):
        cases.append(('plain', 'Pi(k=%d)' % k, plain_path(k, '')))
        if k >= 1:
            cases.append(('plain', 'Pi(k=%d,A)' % k, plain_path(k, 'A')))
            cases.append(('plain', 'Pi(k=%d,AB)' % k, plain_path(k, 'AB')))
    cases.append(('ep', 'Gamma2 end=P (N*=1)', ep_path2(0, '', 'P')))
    for k in range(0, 6):
        cases.append(('ep', 'Gamma2(k=%d)' % k, ep_path2(k, '')))
        if k >= 1:
            cases.append(('ep', 'Gamma2(k=%d,A)' % k, ep_path2(k, 'A')))
            cases.append(('ep', 'Gamma2(k=%d,AB)' % k, ep_path2(k, 'AB')))
    cases.append(('plain', 'Pi_self(3)', plain_self(3)))
    cases.append(('plain', 'Pi_self(4)', plain_self(4)))
    for N in range(1, 7):
        cases.append(('plain', 'Lambda_%d' % N, lam(N)))
    cases.append(('ep-literal', '3-board literal reading', three_board_literal()))
    viol = 0
    for model, name, G in cases:
        rows, info = analyse(G)
        if rows is None:
            print(model, name, 'NOT EXACT', info)
            viol += 1
            continue
        for r in rows:
            bname = '%s:%s' % (G.names[r['bad'][0]], r['bad'][1])
            print('%-10s %-22s b=%2d bad=%-12s aux=%-5s N*=%-4s |P|=%2d |P-E|=%2d |P-(E+Sinf)|=%2d val=%-2s self=%s' % (
                model, name, G.nb, bname, r['aux'], r['nstar'], r['P'], r['PE'], r['PES'], r['fail_val'],
                'yes' if self_moves(G) else 'no'))
            viol += check_row(G, r)
    print('violations of Theorem 4.20 / consistency:', viol)


def check_row(G, r):
    """Checks: Aux <=> N* finite (within cap >= K); N* <= |P-(E+Sinf)| <= |P-E| <= b;
    no e.p. promotion => |P-E| <= b-1; stabilisation of the chain."""
    v = 0
    if r['aux'] != (r['nstar'] is None):
        print('  VIOLATION aux vs ladders'); v += 1
    if r['nstar'] is not None:
        if not r['nstar'] <= r['PES'] <= r['PE'] <= G.nb:
            print('  VIOLATION bound'); v += 1
        if not G.has_ep_promotion() and not r['nstar'] <= G.nb - 1:
            print('  VIOLATION b-1 bound'); v += 1
    # chain: once R_n = R_{n+1}, S_n on Z constant afterwards
    ch, Sn, Z = r['chain'], r['Sn'], r['Z']
    for n in range(len(ch) - 1):
        if ch[n] == ch[n + 1]:
            for m in range(n + 1, len(Sn)):
                if any(Sn[m][z] != Sn[n + 1][z] for z in Z):
                    print('  VIOLATION chain stabilisation'); v += 1
                    break
            break
    # x in S_{|P-E|} <=> Aux
    pe = r['PE']
    if pe < len(Sn) and Sn[pe][r['x']] != r['aux']:
        print('  VIOLATION T_{|P-E|} test'); v += 1
    return v


def random_group(rng, b, model):
    """Random group on b boards: 0 = A, 1 = B, 2 = q; model plain / checks / ep / full."""
    G = Group(b, ['A', 'B', 'q'] + ['g%d' % i for i in range(3, b)])
    pc = 0.25 if model in ('checks', 'full') else 0.0
    pe = 0.3 if model in ('ep', 'full') else 0.0
    for g in range(3, b):
        if rng.random() < pc:
            G.chk[g][rng.randrange(2)] = True
    for g in range(b):
        for s in (W, B):
            ms = []
            for _ in range(rng.choice((0, 1, 1, 2, 2, 3))):
                if g >= 3 and rng.random() < 0.25:
                    ms.append('P')
                else:
                    ms.append((rng.randrange(b), rng.random() < pe))
            G.mv[g][s] = list(dict.fromkeys(ms))
            if pe and rng.random() < pe:
                ex = []
                for _ in range(rng.choice((1, 1, 2))):
                    ex.append('P' if (g >= 3 and rng.random() < 0.3) else (rng.randrange(b), rng.random() < pe))
                G.ep[g][s] = [m for m in dict.fromkeys(ex) if m not in G.mv[g][s]]
    for r, o in ((0, 1), (1, 0)):
        G.mv[r][B] = [(o, False)] + [m for m in G.mv[r][B] if m != 'P' and m != (o, False)]
        G.mv[r][W] = [(2, rng.random() < pe)] + [m for m in G.mv[r][W] if m != 'P']
    for s in (W, B):
        G.mv[2][s] = [m for m in G.mv[2][s] if m != 'P']
    if b >= 4 and rng.random() < 0.7:
        # bias towards exactness: board 3 hot (whoever moves there may promote), q moves to it
        for s in (W, B):
            if not G.chk[3][s] and not G.chk[3][1 - s]:
                G.mv[3][s] = ['P'] + [m for m in G.mv[3][s] if m != 'P']
            G.mv[2][s] = [(3, False)] + [m for m in G.mv[2][s] if m != (3, False)]
    return G


def random_run(seed, count):
    rng = random.Random(seed)
    stats = dict(groups=0, bad=0, fail=0, viol=0, hist={})
    tries = 0
    while stats['groups'] < count:
        tries += 1
        model = rng.choice(('plain', 'checks', 'ep', 'full'))
        b = rng.randint(4, 8)
        G = random_group(rng, b, model)
        rows, info = analyse(G, cap=4 * b + 2)
        if rows is None:
            continue
        stats['groups'] += 1
        for r in rows:
            stats['bad'] += 1
            if r['nstar'] is not None:
                stats['fail'] += 1
                key = (r['nstar'], r['PES'])
                stats['hist'][key] = stats['hist'].get(key, 0) + 1
            stats['viol'] += check_row(G, r)
    print('seed', seed, 'tries', tries, 'exact groups', stats['groups'], 'bad moves', stats['bad'],
          'with (C) failing', stats['fail'], 'violations', stats['viol'])
    print('histogram (N*, |P-(E+Sinf)|): count', sorted(stats['hist'].items()))


def search(model, b, seed, count):
    """Random search for an exact group on b boards maximising N* of a bad move."""
    rng = random.Random(seed)
    best = -1
    exact = fails = 0
    hist = {}
    for _ in range(count):
        G = random_group(rng, b, model)
        rows, info = analyse(G, cap=4 * b + 2)
        if rows is None:
            continue
        exact += 1
        for r in rows:
            if r['nstar'] is not None:
                fails += 1
                hist[r['nstar']] = hist.get(r['nstar'], 0) + 1
                if r['nstar'] > best:
                    best = r['nstar']
    print('model', model, 'b', b, 'seed', seed, 'samples', count, 'exact', exact, 'bad moves failing (C)', fails,
          'N* histogram', sorted(hist.items()), 'max N*', best)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'families':
        families()
    elif cmd == 'random':
        random_run(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == 'search':
        search(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
