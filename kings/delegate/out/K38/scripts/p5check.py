# p5check.py (K38) -- mechanical check of the hand proof in K38/PROOF.md for P5 = Kc4 Pb5 kb6 pc5 (White to move).
# Uses only the own move generator p5gen.py (written from kings/SPEC.md). Strategies are coded as stated in PROOF.md.
# Usage: python p5check.py cyl|flat
import sys
from p5gen import Board, parse, fmt, name, solve

kind = sys.argv[1]
MUT = sys.argv[2] if len(sys.argv) > 2 else ''  # mutation test: 'cutZL', 'noexcl', 'cutZR'
B = Board(7, 6, kind == 'cyl')
PF = 2  # the Black pawn's file (c)
X = parse('Kc4 Pb5 kb6 pc5 w -', B)
fails = []


def fail(msg):
    fails.append(msg)
    if len(fails) <= 20:
        print('FAIL', msg)


def rel(x, y, r):
    return B.sq(PF + x, r + y)


def is_corner(s):
    return (not B.cyl) and s[0] in (0, B.W - 1) and s[1] in (0, B.H - 1)

# ---------------- statement 0 ----------------
wm = sorted(name(c[0]) for k, c in B.moves(X) if k == 'K')
pm = [k for k, c in B.moves(X) if k != 'K']
print('White moves at X:', wm, 'pawn moves:', len(pm))
if wm != ['b3', 'c3', 'd3', 'd5'] or pm:
    fail('statement 0')
print('Black moves at X (b to move):', sorted(fmt(c) for k, c in B.moves(X[:5] + (1,)) if c))

# ---------------- the invariant S of Lemma D (Black to move) ----------------
ZL = {(x, y) for x in (1, 2) for y in range(-2 if MUT == 'cutZL' else -3, 1)}
ZR = {(x, y) for x in (-1, -2) for y in range(-2 if MUT == 'cutZR' else -3, 1)}


def zone(Z, r):
    return {rel(x, y, r) for (x, y) in Z if rel(x, y, r) is not None}


S = set()
per_r = {}
squares = [(f, r) for f in range(B.W) for r in range(B.H)]
for r in range(1, B.H - 1):  # pawn on rank r+1 = 2..5
    p = (PF, r)
    R = r + 1  # rank number
    cnt = 0
    for w in squares:
        for b in squares:
            pos = (w, b, frozenset(), frozenset([p]), None, 1)
            if not B.legal_position(pos):
                continue
            F, M, L, Rr = rel(0, -1, r), rel(0, -2, r), rel(-1, -2, r), rel(1, -2, r)
            ok = False
            if R >= 4:
                ok = (w == F) or (w == M) or (w == L and b not in zone(ZL, r)) or (w == Rr and b not in zone(ZR, r))
            elif R == 3:
                ok = (w == F) or (w == M and (MUT == 'noexcl' or b not in {rel(-1, 0, r), rel(1, 0, r)})) or \
                     (w == L and b == rel(-1, 0, r)) or (w == Rr and b == rel(1, 0, r))
            elif R == 2:
                ok = (w == rel(0, -1, r)) and b in {rel(-1, 1, r), rel(1, 1, r)}
            if ok:
                S.add(pos)
                cnt += 1
    per_r[R] = cnt
print('|S| =', len(S), 'per rank of the pawn:', per_r)


def rho(pos):
    """White's rule (White to move, Black pawn on file c). Returns the child or None."""
    w, b, wp, bp, ep, stm = pos
    (p,) = tuple(bp)
    r = p[1]
    legal = {c[0]: c for k, c in B.moves(pos) if k == 'K'}
    if p in legal:  # rule 1
        return legal[p], 1
    F, M, L, Rr = rel(0, -1, r), rel(0, -2, r), rel(-1, -2, r), rel(1, -2, r)
    if w == F:
        return legal.get(M), 2
    if w == M:
        if F in legal:
            return legal[F], 3
        if b[0] == (PF - 1) % B.W:
            return legal.get(L), 3
        if b[0] == (PF + 1) % B.W:
            return legal.get(Rr), 3
        return None, 3
    if w in (L, Rr):
        return legal.get(M) or legal.get(F), 4
    if w in (rel(-1, -1, r), rel(1, -1, r)):
        return legal.get(F), 5
    return None, 0


def check_S():
    pairs = caps = stal = inS = 0
    wtm = set()
    for pos in S:
        for k, c in B.moves(pos):
            pairs += 1
            if k == 'Q' or c is None:
                fail('Black promotes from ' + fmt(pos))
                continue
            wtm.add(c)
            ms = B.moves(c)
            if not ms:
                if B.in_check(c):
                    fail('White mated ' + fmt(c))
                else:
                    stal += 1
                continue
            ch, rule = rho(c)
            if ch is None:
                fail('rho undefined at ' + fmt(c))
                continue
            if not ch[3]:
                caps += 1
            elif ch in S:
                inS += 1
            else:
                fail('rho leaves S: %s -> %s (rule %d)' % (fmt(c), fmt(ch), rule))
    print('Lemma D: %d (S, Black move) pairs, %d White-to-move positions; captures %d, White stalemated %d, back in S %d'
          % (pairs, len(wtm), caps, stal, inS))
    return wtm


wtmS = check_S()

# ---------------- Part A: after each White move, ...Kxb5, then tau ----------------
def tau_moves(pos):
    return [c for k, c in B.moves(pos) if k == 'K']


A_w, A_b = set(), set()
for k, c in B.moves(X):
    xs = [cc for kk, cc in B.moves(c) if kk == 'K' and cc[1] == (1, 4)]
    if len(xs) != 1:
        fail('Kxb5 not legal after ' + fmt(c))
        continue
    stack = [xs[0]]
    while stack:
        p = stack.pop()
        if p in A_w:
            continue
        A_w.add(p)
        if p[2]:
            fail('White has a pawn in tau ' + fmt(p))
        for kk, cc in B.moves(p):
            if cc is None:
                fail('White promotes?')
                continue
            if cc in A_b:
                continue
            A_b.add(cc)
            if B.in_check(cc):
                fail('Black in check ' + fmt(cc))
            tm = tau_moves(cc)
            if not tm:
                fail('tau has no move at ' + fmt(cc))
            stack.extend(tm)
print('Part A (tau): %d White-to-move, %d Black-to-move positions' % (len(A_w), len(A_b)))

# ---------------- Part C: Kd5 c3 and Black pushes every move ----------------
kd5 = [c for k, c in B.moves(X) if c[0] == (3, 4)][0]
c3 = [c for k, c in B.moves(kd5) if k == 'P' and (2, 2) in c[3]]
if len(c3) != 1:
    fail('no double step after Kd5')
lines = 0
front = c3
for step in range(3):
    nxt = []
    for p in front:
        for kk, cc in B.moves(p):
            if cc is None:
                fail('White promotes in C')
                continue
            lines += 1
            if B.in_check(cc):
                fail('Black in check in C ' + fmt(cc))
            push = [(k3, c3_) for k3, c3_ in B.moves(cc) if k3 in ('P', 'Q')]
            if not push:
                fail('no push in C ' + fmt(cc))
            elif step < 1:
                nxt.extend(c3_ for k3, c3_ in push if k3 == 'P' and c3_[1] == (1, 5) and c3_[3] and
                           tuple(c3_[3])[0][0] == PF)
            else:
                if not any(k3 == 'Q' for k3, c3_ in push):
                    fail('no promotion at the end of C ' + fmt(cc))
    front = nxt
    if step == 1:
        break
print('Part C: Black promotes with c3, c2, c1 in every line; %d White-to-move states checked' % lines)

# ---------------- Part B: sigma after Kb3, Kc3, Kd3 ----------------
def sigma(pos):
    """White to move. Returns the White reply, or 'free' handling, per PROOF.md section 4."""
    w, b, wp, bp, ep, stm = pos
    legal = {c[0]: c for k, c in B.moves(pos) if k == 'K'}
    if not bp:  # Black has no pawn: free mode, any king move
        return ('free', next(iter(legal.values()))) if legal else ('free', None)
    if not wp:  # the pawn b5 was taken: Lemma D
        ch, rule = rho(pos)
        return ('rho', ch)
    (q,) = tuple(bp)
    if q != (PF, 4):  # pawn has stepped next to the king
        return ('cap', legal.get(q))
    # pawn still on c5, White pawn b5: Black's king left b6 (to a5) or is back on b6 after Kc4
    if w == (PF, 3):  # Kc4 stands: Black played a king move away from b6
        return ('cap', legal.get(q))
    return ('Kc4', legal.get((PF, 3)))


B_w = {}
for sortie in ('Kb3', 'Kc3', 'Kd3'):
    sq_ = (ord(sortie[1]) - 97, int(sortie[2]) - 1)
    start = [c for k, c in B.moves(X) if c[0] == sq_][0]
    seen_w, seen_b, stack, free = set(), set(), [start], 0
    while stack:
        p = stack.pop()  # Black to move
        if p in seen_b:
            continue
        seen_b.add(p)
        if p == X[:5] + (1,):
            fail('?')
        for kk, cc in B.moves(p):
            if cc is None:
                fail('Black promotes in sigma from ' + fmt(p))
                continue
            if cc == X:  # back to X: White repeats the sortie
                stack.append(start)
                continue
            seen_w.add(cc)
            if not B.moves(cc):
                if B.in_check(cc):
                    fail('White mated ' + fmt(cc))
                continue
            mode, ch = sigma(cc)
            if ch is None:
                fail('sigma undefined (%s) at %s' % (mode, fmt(cc)))
                continue
            if mode == 'free':
                free += 1
            if mode == 'rho' and ch[3] and ch not in S:
                fail('sigma/rho leaves S at ' + fmt(cc))
            stack.append(ch)
    B_w[sortie] = (len(seen_w), free)
print('Part B (sigma):', {k: '%d White-to-move, %d free mode' % v for k, v in B_w.items()})

# ---------------- values from the own solver (P, EPW, EPB) ----------------
vals = {m: solve(B, [X, X[:5] + (1,)], m) for m in ('P', 'EPW', 'EPB')}
print('own solver: %d positions reachable from X (both sides to move)' % len(vals['P']))
for m in ('P', 'EPW', 'EPB'):
    v = vals[m]
    print('  %s: X w = %s, X b = %s, sorties (b to move):' % (m, v[X], v[X[:5] + (1,)]),
          {name(c[0]): v[c] for k, c in B.moves(X)})
bad = [p for p in S | wtmS if p in vals['P'] and vals['P'][p] == 'L']
print('positions of S or their White-to-move successors that the own P solver calls L:', len(bad))
notreached = [p for p in S if p not in vals['P']]
print('positions of S not reachable from X:', len(notreached))
with open('../logs/own_positions_%s%s.txt' % (kind, MUT and '_' + MUT), 'w') as fh:
    for p in sorted(vals['P'], key=fmt):
        fh.write('%s | %s %s %s\n' % (fmt(p), vals['P'][p], vals['EPW'][p], vals['EPB'][p]))
print('FAILURES:', len(fails))
