"""K60 referee: brute-force check of Theorems A, B (and A0, A1, A2, B2, B3) on abstract exact over groups.

Usage: python r60run.py SEED NGROUPS NRANDOM_T
Own code (r60lib.py). Prints counters and every violation found.
"""
import random
import sys
from collections import Counter
from r60lib import (zielonka_aux, Group, p_values, over_group, sum_solve, aux_solve, T_N, dsum, NAMED, random_dgame,
                    WHITE, BLACK)

OVER = over_group()


def exact_over(G, Pv):
    """Definition 4.8 (over orientation). Returns (ok, why, bad Black root moves [(root, target, kind)], q-states)."""
    def v(g, e, c):
        return Pv[G.sidx(g, e, c)]
    for r in (0, 1):
        if G.chk[r][0] or G.chk[r][1]:
            return False, 'root check', None, None
    bad, qs = [], set()
    for r in (0, 1):
        leg = G.legal(r, 0, BLACK)
        if (1 - r, 'n') not in leg:
            return False, 'no shuttle', None, None
        seen_shuttle = False
        for (t, k) in leg:
            if (t, k) == (1 - r, 'n') and not seen_shuttle:
                seen_shuttle = True
                continue
            if k == 'p' or v(t, 1 if k == 'd' else 0, WHITE) != 2:
                return False, 'black root move not losing', None, None
            bad.append((r, t, k))
        freezes = 0
        for (t, k) in G.legal(r, 0, WHITE):
            if k == 'p':
                return False, 'white promotion at root', None, None
            e = 1 if k == 'd' else 0
            if v(t, e, BLACK) == 0:
                continue
            freezes += 1
            q = t
            if G.chk[q][0] or G.chk[q][1]:
                return False, 'check at q', None, None
            for (qe, c) in ((e, BLACK), (0, WHITE)):
                lq = G.legal(q, qe, c)
                if not lq:
                    return False, 'no move at q', None, None
                for (t2, k2) in lq:
                    if k2 == 'p':
                        return False, 'promotion at q', None, None
                    want = 2 if c == BLACK else 0
                    if v(t2, 1 if k2 == 'd' else 0, 1 - c) != want:
                        return False, 'q move not losing', None, None
            qs.add((q, e))
        if freezes == 0:
            return False, 'no freeze', None, None
    return True, '', bad, sorted(qs)


def gen_group(rng, family):
    """Random group, then filtered to Definition 4.8. family 'rand' or 'adv' (adversarial: small dense gadgets
    with checks, double steps, e.p. moves and back edges)."""
    nq = rng.randint(1, 2)
    ng = {'rand': rng.randint(3, 8), 'adv': rng.randint(2, 6), 'tempo': rng.randint(3, 7)}[family]
    nb = 2 + nq + ng
    G = Group(nb)
    Q = list(range(2, 2 + nq))
    gad = list(range(2 + nq, nb))
    pc = {'rand': 0.25, 'adv': 0.4, 'tempo': 0.15}[family]
    for g in gad:
        r = rng.random()
        if r < pc / 2:
            G.chk[g][WHITE] = True
        elif r < pc:
            G.chk[g][BLACK] = True
    pp = {'rand': 0.15, 'adv': 0.25, 'tempo': 0.3}[family]
    mmax = 2 if family == 'tempo' else 3
    for g in gad:
        for c in (0, 1):
            for _ in range(rng.randint(0 if family != 'tempo' else 1, mmax)):
                r = rng.random()
                k = 'p' if r < pp else ('d' if r < pp + 0.15 else 'n')
                if rng.random() < (0.1 if family == 'rand' else 0.2):
                    t = rng.choice([0, 1] + Q)
                else:
                    t = rng.choice(gad)
                G.mv[g][c].append((t, k))
            if rng.random() < 0.25:
                G.ep[g][c].append((rng.choice(gad), 'p' if rng.random() < 0.3 else 'n'))
    # roots
    G.mv[0][BLACK].append((1, 'n'))
    G.mv[1][BLACK].append((0, 'n'))
    for r in (0, 1):
        q = rng.choice(Q)
        G.mv[r][WHITE].append((q, 'd' if rng.random() < 0.3 else 'n'))
        for _ in range(rng.randint(1, 3)):
            G.mv[r][BLACK].append((rng.choice(gad), 'd' if rng.random() < 0.3 else 'n'))
        for _ in range(rng.randint(0, 2)):
            G.mv[r][WHITE].append((rng.choice(gad), 'd' if rng.random() < 0.2 else 'n'))
    for q in Q:
        for c in (0, 1):
            for _ in range(rng.randint(1, 2)):
                G.mv[q][c].append((rng.choice(gad), 'd' if rng.random() < 0.2 else 'n'))
            if rng.random() < 0.2:
                G.ep[q][c].append((rng.choice(gad), 'n'))
    # filter: drop root/q moves with the wrong P value, twice (back edges can change values)
    for _ in range(3):
        Pv = p_values(G)
        def v(g, e, c):
            return Pv[G.sidx(g, e, c)]
        for r in (0, 1):
            G.mv[r][BLACK] = [(t, k) for (t, k) in G.mv[r][BLACK]
                              if (t, k) == (1 - r, 'n') or (not G.chk[t][BLACK] and v(t, k == 'd', WHITE) == 2)]
            G.mv[r][WHITE] = [(t, k) for (t, k) in G.mv[r][WHITE]
                              if t in Q or (not G.chk[t][WHITE] and v(t, k == 'd', BLACK) == 0)]
        for q in Q:
            for c in (0, 1):
                want = 2 if c == BLACK else 0
                G.mv[q][c] = [(t, k) for (t, k) in G.mv[q][c]
                              if not G.chk[t][c] and v(t, k == 'd', 1 - c) == want]
                G.ep[q][c] = [(t, k) for (t, k) in G.ep[q][c]
                              if not G.chk[t][c] and v(t, 0, 1 - c) == want]
    Pv = p_values(G)
    ok, why, bad, qs = exact_over(G, Pv)
    if not ok or not bad:
        return None
    return G, bad, qs


def hand_groups():
    out = {}
    # K60's G1 (PROOF.md section 5): A B q qb qw x x2 y z y2 = 0..9
    G = Group(10)
    A, B, q, qb, qw, x, x2, y, z, y2 = range(10)
    for (a, b) in ((A, q), (B, q), (q, qw), (x, y), (y, y2)):
        G.mv[a][WHITE].append((b, 'n'))
    for a in (qb, x2, z):
        G.mv[a][WHITE].append((0, 'p'))
    for (a, b) in ((A, B), (A, x), (B, A), (B, x), (q, qb), (x, x2), (y, z)):
        G.mv[a][BLACK].append((b, 'n'))
    for a in (qw, y2):
        G.mv[a][BLACK].append((0, 'p'))
    out['G1'] = G
    # K60's G2 (Prop. A2): A B q qb qw x w w2 = 0..7
    G = Group(8)
    A, B, q, qb, qw, x, w, w2 = range(8)
    for (a, b) in ((A, q), (B, q), (q, qw), (x, w)):
        G.mv[a][WHITE].append((b, 'n'))
    for a in (qb, w, w2):
        G.mv[a][WHITE].append((0, 'p'))
    for (a, b) in ((A, B), (A, x), (B, A), (q, qb), (w, w2)):
        G.mv[a][BLACK].append((b, 'n'))
    for a in (qw, x):
        G.mv[a][BLACK].append((0, 'p'))
    out['G2'] = G
    # K58's witness: r0 r1 q x p = 0..4
    G = Group(5)
    for (a, b) in ((0, 2), (1, 2), (2, 3), (3, 2)):
        G.mv[a][WHITE].append((b, 'n'))
    G.mv[4][WHITE].append((0, 'p'))
    for (a, b) in ((0, 1), (0, 3), (1, 0), (1, 3), (2, 4)):
        G.mv[a][BLACK].append((b, 'n'))
    for a in (3, 4):
        G.mv[a][BLACK].append((0, 'p'))
    out['K58'] = G
    # R1: a check/e.p. probe built by hand: Black's bad move is a double step that gives check; White must answer
    # on the board (cannot pass in Aux), its only answer is the e.p. capture.
    G = Group(9)
    A, B, q, qb, qw, x, y, z, y2 = range(9)
    G.mv[A][WHITE].append((q, 'n')); G.mv[B][WHITE].append((q, 'n'))
    G.mv[q][WHITE].append((qw, 'n')); G.mv[qb][WHITE].append((0, 'p'))
    G.mv[A][BLACK] += [(B, 'n'), (x, 'd')]; G.mv[B][BLACK].append((A, 'n'))
    G.mv[q][BLACK].append((qb, 'n')); G.mv[qw][BLACK].append((0, 'p'))
    G.chk[x][WHITE] = True
    G.ep[x][WHITE].append((y, 'n'))           # only with the right
    G.mv[y][BLACK].append((z, 'n')); G.mv[z][WHITE].append((0, 'p'))
    G.mv[y][BLACK].append((y2, 'n')); G.mv[y2][WHITE].append((0, 'p'))
    out['R1'] = G
    return out


def battery(rng, nrand):
    Ts = [(k, v) for k, v in NAMED.items()]
    names = list(NAMED)
    for _ in range(12):
        a, b = rng.sample(names, 2)
        Ts.append((a + '+' + b, dsum(NAMED[a], NAMED[b])))
    for i in range(nrand):
        Ts.append(('rnd%d' % i, random_dgame(rng, maxpos=rng.choice([2, 3, 4, 5, 6]))))
    return Ts


def main():
    seed, ngroups, nrand = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    TB = battery(rng, nrand)
    TNlist = [0, 1, 2, 3, 4, 6]
    ocache = {}

    def oval(name, T):
        if name not in ocache:
            ocache[name] = sum_solve(OVER, T)
        return ocache[name]

    cnt = Counter()
    viol = []
    groups = [(k, G, 'hand') for k, G in hand_groups().items()]
    tries = 0
    while len(groups) < ngroups + 4:
        tries += 1
        fam = ('rand', 'adv', 'tempo')[tries % 3]
        r = gen_group(rng, fam)
        if r is not None:
            groups.append(('%s%d' % (fam, tries), r[0], fam))
    cnt['generation_tries'] = tries
    for (gname, G, fam) in groups:
        Pv = p_values(G)
        ok, why, bad, qs = exact_over(G, Pv)
        if not ok:
            if fam == 'hand':
                print('hand group', gname, 'NOT exact:', why)
            continue
        cnt['exact_' + fam] += 1
        if any(G.chk[g][0] or G.chk[g][1] for g in range(G.nb)):
            cnt['groups_with_check'] += 1
        if any(k == 'd' for g in range(G.nb) for c in (0, 1) for (_, k) in G.mv[g][c]):
            cnt['groups_with_double_step'] += 1
        if any(G.ep[g][c] for g in range(G.nb) for c in (0, 1)):
            cnt['groups_with_ep_moves'] += 1
        K = 4 * G.nb
        # per bad move: Aux, (B1), Aux with draws, T_N
        info = []
        for (r, x, k) in bad:
            e = 1 if k == 'd' else 0
            aux, it = aux_solve(G, x, e)
            if zielonka_aux(G, x, e) != aux:
                viol.append((gname, 'Buchi solvers disagree', x))
            cnt['buchi_cross_checked'] += 1
            v1, i1 = sum_solve(G, NAMED['m1'])
            b1 = v1[i1(x, e, 0, WHITE)] == 2
            vu, iu = sum_solve(G, NAMED['under'])
            auxD = vu[iu(x, e, 0, WHITE)] != 0
            tn = {}
            for N in TNlist + [K]:
                vt, it_ = sum_solve(G, T_N(N))
                tn[N] = vt[it_(x, e, 0, WHITE)] == 2
            info.append(dict(r=r, x=x, e=e, aux=aux, b1=b1, auxD=auxD, tn=tn, C=True, Cnotn=True, CD=True,
                             CW=True, failT=None))
            cnt['bad_moves'] += 1
            cnt['aux_win' if aux else 'aux_loss'] += 1
            if aux and not b1:
                cnt['aux_win_without_B1'] += 1
            if G.chk[x][WHITE]:
                cnt['bad_moves_giving_check'] += 1
            if e:
                cnt['bad_moves_double_step'] += 1
            if b1 and not aux:
                viol.append((gname, 'B1 but Aux lost', x))
            if aux != tn[K]:
                viol.append((gname, 'Aux != T_K', x, aux, tn[K]))
            if aux and not all(tn.values()):
                viol.append((gname, 'Aux won but some T_N not W', x, tn))
        # root test of Corollary B3
        vK, iK = sum_solve(G, T_N(K))
        b3 = all(vK[iK(r, 0, 0, BLACK)] == 2 for r in (0, 1))
        resO_all = True
        for (tname, T) in TB + [('T_%d' % N, T_N(N)) for N in TNlist + [K]]:
            val, idx = sum_solve(G, T)
            ov, oidx = oval(tname if not tname.startswith('T_') else tname, T)
            nt = len(T[0])
            resO = True
            for r in (0, 1):
                for c in (0, 1):
                    for t in range(nt):
                        a, b = val[idx(r, 0, t, c)], ov[oidx(0, 0, t, c)]
                        cnt['results'] += 1
                        if a != b:
                            resO = False
                        if a > b:
                            viol.append((gname, 'A0(ii) root better for White than omega', tname, r, c, t))
            for (q, e) in qs:
                for (qe, c) in ((e, BLACK), (0, BLACK), (0, WHITE)):
                    for t in range(nt):
                        cnt['results'] += 1
                        if val[idx(q, qe, t, c)] != ov[oidx(1, 0, t, c)]:
                            viol.append((gname, 'A0(i) q differs from 0_D', tname, q, qe, c, t))
            for t in range(nt):
                if ov[oidx(0, 0, t, BLACK)] > ov[oidx(0, 0, t, WHITE)]:
                    viol.append(('over', 'A1 fails', tname, t))
            Cat = True
            for d in info:
                for t in range(nt):
                    a = val[idx(d['x'], d['e'], t, WHITE)]
                    b = ov[oidx(0, 0, t, BLACK)]
                    if a < b:
                        Cat = False
                        d['C'] = False
                        if not tname.startswith('T_'):
                            d['Cnotn'] = False
                        if d['failT'] is None:
                            d['failT'] = tname
                    if b >= 1 and a < 1:
                        d['CD'] = False
                    if a < ov[oidx(0, 0, t, WHITE)]:
                        d['CW'] = False
            if resO != Cat:
                viol.append((gname, 'Theorem A per T fails', tname, resO, Cat))
            resO_all &= resO
        nob1 = any(not d['b1'] for d in info)
        if resO_all:
            cnt['groups_results_of_omega_on_battery'] += 1
            if nob1:
                cnt['groups_omega_without_B1'] += 1
            if any(not d['CW'] for d in info):
                cnt['groups_omega_but_CW_fails'] += 1
        else:
            cnt['groups_differ_from_omega'] += 1
        if b3 != resO_all:
            viol.append((gname, 'Corollary B3 test disagrees with battery', b3, resO_all))
        for d in info:
            if d['aux'] and not d['C']:
                viol.append((gname, 'Aux won but (C) fails on battery', d['x'], d['failT']))
            if not d['aux']:
                if d['C']:
                    viol.append((gname, 'Aux lost but (C) holds on whole battery incl. T_N', d['x']))
                if d['Cnotn']:
                    cnt['aux_loss_not_separated_without_TN'] += 1
                    if cnt['aux_loss_not_separated_without_TN'] <= 3:
                        print('EXAMPLE aux loss separated only by T_N:', gname, 'x', d['x'], 'e', d['e'],
                              'TN', d['tn'], 'mv', G.mv, 'ep', G.ep, 'chk', G.chk)
                else:
                    cnt['aux_loss_separated_by_non_TN'] += 1
            if d['auxD'] != d['CD']:
                viol.append((gname, 'Aux-with-draws != D-half of (C) on battery', d['x'], d['auxD'], d['CD']))
        if fam == 'hand':
            print('hand', gname, 'bad', [(d['r'], d['x'], d['e']) for d in info], 'aux', [d['aux'] for d in info],
                  'B1', [d['b1'] for d in info], 'CW', [d['CW'] for d in info], 'omega', resO_all,
                  'TN', [d['tn'] for d in info])
    print('seed', seed, 'battery size', len(TB) + len(TNlist) + 1)
    for k in sorted(cnt):
        print('%-45s %d' % (k, cnt[k]))
    print('violations', len(viol))
    for v in viol[:50]:
        print('VIOL', v)


if __name__ == '__main__':
    main()
