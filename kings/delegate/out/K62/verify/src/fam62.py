"""K62 referee: the investigator's constructions, rebuilt from the text of PROOF.md (not from its src/)."""
from ref62 import Group, WHITE as Wh, BLACK as Bl

F, T = False, True


def gamma2(k, R='', endP=False, a_c1_in_AB=False):
    """Gamma2(k, R): boards A=0, B=1, q=2, c_i = 3+i."""
    A, B, q = 0, 1, 2
    c = [3 + i for i in range(k + 1)]
    mv0, ep = {}, {}
    for r in (A, B):
        mv0[(r, Wh)] = [(q, F)]
    for ci in c:
        mv0[(ci, Wh)] = [(q, F)]
    mv0[(q, Wh)] = [(c[0], T)]
    ep[(c[0], Wh)] = ['P']
    mv0[(A, Bl)] = [(B, F), (c[0], F)]
    mv0[(B, Bl)] = [(A, F)]
    mv0[(q, Bl)] = [(c[0], T)]
    ep[(c[0], Bl)] = ['P']
    if endP:
        assert k == 0 and R == ''
        mv0[(c[0], Bl)] = ['P']
    elif R == '':
        for i in range(k):
            mv0[(c[i], Bl)] = [(c[i + 1], F)]
        mv0[(c[k], Bl)] = [(q, F)]
    else:
        assert k >= 1
        mv0[(c[0], Bl)] = [(A, F)]
        if R == 'A':
            mv0[(A, Bl)].append((c[1], F))
        else:
            mv0[(B, Bl)].append((c[1], F))
            if a_c1_in_AB:
                mv0[(A, Bl)].append((c[1], F))
        for i in range(1, k):
            mv0[(c[i], Bl)] = [(c[i + 1], F)]
        mv0[(c[k], Bl)] = [(q, F)]
    name = 'Gamma2(%d,%s)%s' % (k, R or '0', ' endP' if endP else '')
    return Group(3 + k + 1, mv0=mv0, ep=ep, name=name), (A, (c[0], F))


def gamma0(R):
    """Gamma(0, R), R in {'A', 'AB'}: as Gamma2(0, 0) with c_0 -> A, a bad double step to q, and an extra
    e.p. move of White at (q, White, right) to (q, 0, Black)."""
    A, B, q, c0 = 0, 1, 2, 3
    mv0, ep = {}, {}
    mv0[(A, Wh)] = [(q, F)]
    mv0[(B, Wh)] = [(q, F)]
    mv0[(c0, Wh)] = [(q, F)]
    mv0[(q, Wh)] = [(c0, T)]
    ep[(c0, Wh)] = ['P']
    ep[(q, Wh)] = [(q, F)]
    mv0[(A, Bl)] = [(B, F), (c0, F)]
    mv0[(B, Bl)] = [(A, F)]
    mv0[(q, Bl)] = [(c0, T)]
    ep[(c0, Bl)] = ['P']
    mv0[(c0, Bl)] = [(A, F)]
    if R == 'A':
        mv0[(A, Bl)].append((q, T))
    else:
        mv0[(B, Bl)].append((q, T))
    return Group(4, mv0=mv0, ep=ep, name='Gamma(0,%s)' % R), (A, (c0, F))


def pi(k, R='', endP=False):
    """Pi(k, R): boards A=0, B=1, q=2, p=3 (hot), c_i = 4+i."""
    A, B, q, p = 0, 1, 2, 3
    c = [4 + i for i in range(k + 1)]
    mv0 = {}
    for r in (A, B):
        mv0[(r, Wh)] = [(q, F)]
    for ci in c:
        mv0[(ci, Wh)] = [(q, F)]
    mv0[(q, Wh)] = [(p, F)]
    mv0[(p, Wh)] = ['P']
    mv0[(p, Bl)] = ['P']
    mv0[(A, Bl)] = [(B, F), (c[0], F)]
    mv0[(B, Bl)] = [(A, F)]
    mv0[(q, Bl)] = [(p, F)]
    if endP:
        assert k == 0 and R == ''
        mv0[(c[0], Bl)] = ['P']
    elif R == '':
        for i in range(k):
            mv0[(c[i], Bl)] = [(c[i + 1], F)]
        mv0[(c[k], Bl)] = [(q, F)]
    else:
        mv0[(c[0], Bl)] = [(A, F)]
        if R == 'A':
            mv0[(A, Bl)].append((c[1], F))
        else:
            mv0[(B, Bl)].append((c[1], F))
        for i in range(1, k):
            mv0[(c[i], Bl)] = [(c[i + 1], F)]
        mv0[(c[k], Bl)] = [(q, F)]
    name = 'Pi(%d,%s)%s' % (k, R or '0', ' endP' if endP else '')
    return Group(4 + k + 1, mv0=mv0, name=name), (A, (c[0], F))


def pi_self(n):
    """Pi_self(3) / Pi_self(4): boards A=0, B=1, q=2, p=3 (hot), y=4."""
    A, B, q, p, y = 0, 1, 2, 3, 4
    mv0 = {(A, Wh): [(q, F)], (B, Wh): [(q, F)], (y, Wh): [(q, F)], (q, Wh): [(p, F)], (p, Wh): ['P'],
           (A, Bl): [(B, F)], (B, Bl): [(A, F), (y, F)], (q, Bl): [(p, F)], (y, Bl): [(q, F)], (p, Bl): ['P']}
    if n == 3:
        mv0[(B, Bl)].append((B, F))
        m = (B, (B, F))
    else:
        mv0[(A, Bl)].append((A, F))
        m = (A, (A, F))
    return Group(5, mv0=mv0, name='Pi_self(%d)' % n), m


def lam(N):
    """Lambda_N: boards A=0, B=1, q=2, p=3, e=4, c_i = 4+i (i = 1..N)."""
    A, B, q, p, e = 0, 1, 2, 3, 4
    c = {i: 4 + i for i in range(1, N + 1)}
    mv0 = {(A, Wh): [(q, F)], (B, Wh): [(q, F)], (q, Wh): [(e, F)], (e, Wh): [(p, F)], (p, Wh): ['P'],
           (A, Bl): [(B, F), (c[1], F)], (B, Bl): [(A, F)], (q, Bl): [(p, F)], (e, Bl): ['P'], (p, Bl): [(e, F)]}
    for i in range(1, N + 1):
        mv0[(c[i], Wh)] = [(q, F)]
        mv0[(c[i], Bl)] = [(c[i + 1], F)] if i < N else [(e, F)]
    return Group(N + 5, mv0=mv0, name='Lambda_%d' % N), (A, (c[1], F))


def three_literal():
    """PROOF.md 2.5.4: boards A=0, B=1, q=2."""
    A, B, q = 0, 1, 2
    mv0 = {(A, Bl): [(B, F), (B, T)], (B, Bl): [(A, F), (q, T)], (q, Bl): [(A, T)],
           (A, Wh): [(q, F)], (B, Wh): [(q, F)], (q, Wh): [(q, T)]}
    ep = {(A, Wh): ['P'], (q, Bl): ['P'], (q, Wh): [(q, F)]}
    return Group(3, mv0=mv0, ep=ep, name='three_literal'), (A, (B, T))


def delta4():
    """Referee's example (not in PROOF.md): 4 boards A=0, B=1, q=2, g=3, no checks, every move changes the board.
    Black: A -> B; B -> A, B => A (bad, double step to a root), B -> g (bad); q => g; g -> q; e.p. promotion at (g, Black, right).
    White: A -> q, B -> q (freezes); q => g; g -> q; e.p. promotion at (g, White, right).
    Route after m = B => A: A, B, g, q, so N* = 4 = b."""
    A, B, q, g = 0, 1, 2, 3
    mv0 = {(A, Bl): [(B, F)], (B, Bl): [(A, F), (A, T), (g, F)], (q, Bl): [(g, T)], (g, Bl): [(q, F)],
           (A, Wh): [(q, F)], (B, Wh): [(q, F)], (q, Wh): [(g, T)], (g, Wh): [(q, F)]}
    ep = {(g, Bl): ['P'], (g, Wh): ['P']}
    return Group(4, mv0=mv0, ep=ep, name='Delta4'), (B, (A, T))
