"""K62 constructions (abstract exact over groups). See PROOF.md for the hand proofs.

Notation: boards are named; Black = 1, White = 0; a move is 'P' or (board, double_step).
"""
from k62lib import Group, W, B


def _mk(names):
    G = Group(len(names), list(names))
    return G, {n: i for i, n in enumerate(names)}


def ep_path(k, via_A=True, via_B=True, end='q'):
    """E.p. family Gamma(k, via_A, via_B): boards A, B, q, c0..ck (b = k + 4), no checks.
    Path of Black after the bad move m = A -> c0: c0 -> c1 -> ... -> ck [-> A [-> B]] -> (q, White, right)
    by a double step. end='P': ck with Black to move promotes instead (only with via_A = via_B = False).
    White promotes only by the e.p. move at (c0, White, right); Black only by the e.p. move at (c0, Black, right)
    (and, for end='P', at ck)."""
    names = ['A', 'B', 'q'] + ['c%d' % i for i in range(k + 1)]
    G, I = _mk(names)
    A, Bb, q = I['A'], I['B'], I['q']
    c = [I['c%d' % i] for i in range(k + 1)]
    # roots
    G.mv[A][B] = [(Bb, False), (c[0], False)]
    G.mv[Bb][B] = [(A, False)]
    G.mv[A][W] = [(q, False)]
    G.mv[Bb][W] = [(q, False)]
    # q: Black's only move: double step to c0 (White then promotes e.p.); White's only move: double step to c0
    G.mv[q][B] = [(c[0], True)]
    G.mv[q][W] = [(c[0], True)]
    G.ep[q][W] = [(q, False)]          # at (q, White, right): an e.p. move back to the zugzwang q
    G.ep[c[0]][W] = ['P']
    G.ep[c[0]][B] = ['P']
    for i in range(k + 1):
        G.mv[c[i]][W] = [(q, False)]
    for i in range(k):
        G.mv[c[i]][B] = [(c[i + 1], False)]
    if end == 'P':
        assert not via_A and not via_B
        G.mv[c[k]][B] = ['P']
    elif via_A:
        G.mv[c[k]][B] = [(A, False)]
        if via_B:
            G.mv[Bb][B].append((q, True))      # bad move of B: double step to q
        else:
            G.mv[A][B].append((q, True))       # bad move of A: double step to q
    else:
        G.mv[c[k]][B] = [(q, True)]
    return G


def plain_path(k, detour='', end='q'):
    """Plain family Pi(k, detour): boards A, B, q, p, c0..ck (b = k + 5), no checks, no e.p.
    p is hot: whoever moves at p promotes. Path after m = A -> c0:
      detour ''   : c0 -> c1 -> ... -> ck -> (q, White)
      detour 'A'  : c0 -> A -(bad move A -> c1)-> c1 -> ... -> ck -> (q, White)          (k >= 1)
      detour 'AB' : c0 -> A -(shuttle)-> B -(bad move B -> c1)-> c1 -> ... -> ck -> (q, White)   (k >= 1)
    end='P': ck with Black to move promotes instead of moving to q."""
    names = ['A', 'B', 'q', 'p'] + ['c%d' % i for i in range(k + 1)]
    G, I = _mk(names)
    A, Bb, q, p = I['A'], I['B'], I['q'], I['p']
    c = [I['c%d' % i] for i in range(k + 1)]
    G.mv[A][B] = [(Bb, False), (c[0], False)]
    G.mv[Bb][B] = [(A, False)]
    G.mv[A][W] = [(q, False)]
    G.mv[Bb][W] = [(q, False)]
    G.mv[q][B] = [(p, False)]
    G.mv[q][W] = [(p, False)]
    G.mv[p][W] = ['P']
    G.mv[p][B] = ['P']
    for i in range(k + 1):
        G.mv[c[i]][W] = [(q, False)]
    seq = list(range(k + 1))
    if detour:
        assert k >= 1
        G.mv[c[0]][B] = [(A, False)]
        if detour == 'A':
            G.mv[A][B].append((c[1], False))
        else:
            G.mv[Bb][B].append((c[1], False))
        seq = list(range(1, k + 1))
    for a, bb in zip(seq, seq[1:]):
        G.mv[c[a]][B] = [(c[bb], False)]
    G.mv[c[k]][B] = ['P'] if end == 'P' else [(q, False)]
    if end == 'P' and k == 0:
        G.ep[c[0]][B] = []      # Black promotes at c0 anyway
    return G


def lam(N):
    """Lambda_N (question 2): boards A, B, q, p, e, c1..cN (N + 5 boards), no checks, no e.p.
    White: roots -> q; q -> e; ci -> q; e -> p; p promotes.
    Black: shuttle; A -> c1 (the bad move); q -> p; ci -> c(i+1); cN -> e; e promotes; p -> e."""
    names = ['A', 'B', 'q', 'p', 'e'] + ['c%d' % i for i in range(1, N + 1)]
    G, I = _mk(names)
    A, Bb, q, p, e = I['A'], I['B'], I['q'], I['p'], I['e']
    c = [None] + [I['c%d' % i] for i in range(1, N + 1)]
    G.mv[A][B] = [(Bb, False), (c[1], False)]
    G.mv[Bb][B] = [(A, False)]
    G.mv[A][W] = [(q, False)]
    G.mv[Bb][W] = [(q, False)]
    G.mv[q][B] = [(p, False)]
    G.mv[q][W] = [(e, False)]
    G.mv[e][W] = [(p, False)]
    G.mv[e][B] = ['P']
    G.mv[p][W] = ['P']
    G.mv[p][B] = [(e, False)]
    for i in range(1, N + 1):
        G.mv[c[i]][W] = [(q, False)]
        G.mv[c[i]][B] = [(c[i + 1], False)] if i < N else [(e, False)]
    return G


def three_board_literal():
    """3 boards A, B, q with e.p. promotions at states (board, side, right) that (O0)-(O4) do not name.
    Valid only under the literal reading of (O1)-(O4) (they constrain the named states only)."""
    G, I = _mk(['A', 'B', 'q'])
    A, Bb, q = I['A'], I['B'], I['q']
    G.mv[A][B] = [(Bb, False), (Bb, True)]   # shuttle; bad move: double step to B
    G.mv[Bb][B] = [(A, False), (q, True)]    # shuttle; bad move: double step to q
    G.mv[A][W] = [(q, False)]
    G.mv[Bb][W] = [(q, False)]
    G.mv[q][B] = [(A, True)]                 # -> (A, White, right): White promotes e.p.
    G.mv[q][W] = [(q, True)]                 # -> (q, Black, right): Black promotes e.p.
    G.ep[A][W] = ['P']
    G.ep[q][B] = ['P']
    G.ep[q][W] = [(q, False)]
    return G


def ep_path2(k, roots='', end='q'):
    """E.p. family without moves to the same board (reading M2). Boards A, B, q, c0..ck (b = k + 4), no checks.
    Path after the bad move m = A -> c0: c0 [-> A [-> B]] -> c1 -> ... -> ck -> (q, White) (single step).
    roots 'A': c0 -> A, bad move A -> c1; roots 'AB': c0 -> A, shuttle, bad move B -> c1 (k >= 1 for both).
    Promotions only by e.p. moves at c0: (c0, White, right) and (c0, Black, right), after q -> c0 double steps."""
    names = ['A', 'B', 'q'] + ['c%d' % i for i in range(k + 1)]
    G, I = _mk(names)
    A, Bb, q = I['A'], I['B'], I['q']
    c = [I['c%d' % i] for i in range(k + 1)]
    G.mv[A][B] = [(Bb, False), (c[0], False)]
    G.mv[Bb][B] = [(A, False)]
    G.mv[A][W] = [(q, False)]
    G.mv[Bb][W] = [(q, False)]
    G.mv[q][B] = [(c[0], True)]
    G.mv[q][W] = [(c[0], True)]
    G.ep[c[0]][W] = ['P']
    G.ep[c[0]][B] = ['P']
    for i in range(k + 1):
        G.mv[c[i]][W] = [(q, False)]
    seq = list(range(k + 1))
    if roots:
        assert k >= 1
        G.mv[c[0]][B] = [(A, False)]
        if roots == 'A':
            G.mv[A][B].append((c[1], False))
        else:
            G.mv[Bb][B].append((c[1], False))
        seq = list(range(1, k + 1))
    for a, bb in zip(seq, seq[1:]):
        G.mv[c[a]][B] = [(c[bb], False)]
    G.mv[c[k]][B] = ['P'] if end == 'P' else [(q, False)]
    if end == 'P' and k == 0:
        G.ep[c[0]][B] = []      # Black promotes at c0 anyway
    return G


def plain_self(which):
    """Plain group on 5 boards A, B, q, p, y with a Black move from a root to the same root (reading M1 only).
    which = 3: B has the bad moves B -> B and B -> y; N* = 3 at x = (B, White).
       which = 4: A has the bad move A -> A, B has the bad move B -> y; N* = 4 at x = (A, White)."""
    G, I = _mk(['A', 'B', 'q', 'p', 'y'])
    A, Bb, q, p, y = I['A'], I['B'], I['q'], I['p'], I['y']
    G.mv[A][B] = [(Bb, False)]
    G.mv[Bb][B] = [(A, False), (y, False)]
    if which == 3:
        G.mv[Bb][B].append((Bb, False))
    else:
        G.mv[A][B].append((A, False))
    G.mv[A][W] = [(q, False)]
    G.mv[Bb][W] = [(q, False)]
    G.mv[q][B] = [(p, False)]
    G.mv[q][W] = [(p, False)]
    G.mv[p][W] = ['P']
    G.mv[p][B] = ['P']
    G.mv[y][W] = [(q, False)]
    G.mv[y][B] = [(q, False)]
    return G


def self_moves(G):
    """Moves from a board to the same board (excluded in reading M2), and duplicate successors."""
    out = []
    for g in range(G.nb):
        for s in (W, B):
            seen = set()
            for f in (0, 1):
                for m in G.legal(g, f, s):
                    if m != 'P' and m[0] == g:
                        out.append((G.names[g], s, f, m))
            ms = [m for m in G.mv[g][s] + G.ep[g][s]]
            for m in ms:
                key = m if m == 'P' else (m[0], bool(m[1]))
                if key in seen:
                    out.append(('dup', G.names[g], s, m))
                seen.add(key)
    return out
