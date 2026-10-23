"""Independent checker of (H1)-(H5) of Proposition 2.11 of kings/theory/LOOPY.md.
Own move generator; mu_omega by iterative-deepening search over G_omega.
Squares are (file, rank), file 0-based, rank 1..H.  Colours 'w', 'b'."""
import subprocess, sys, os, random, itertools, collections

S = os.path.dirname(os.path.abspath(__file__))
KP = os.path.join(S, 'kp')
FILES = 'abcdefghij'
MAXRSS = 0


def other(c):
    return 'b' if c == 'w' else 'w'


class Bd:
    def __init__(self, W, H, wrap=True):
        self.W, self.H, self.wrap = W, H, wrap

    def nf(self, f, df):
        g = f + df
        if self.wrap:
            return g % self.W
        return g if 0 <= g < self.W else None

    def fd(self, f, g):
        d = abs(f - g)
        return min(d, self.W - d) if self.wrap else d

    def kdist(self, a, b):
        return max(self.fd(a[0], b[0]), abs(a[1] - b[1]))

    def adjfiles(self, f):
        return [g for g in (self.nf(f, -1), self.nf(f, 1)) if g is not None]

    def name(self, s):
        return FILES[s[0]] + str(s[1])


class Pos:
    __slots__ = ('wk', 'bk', 'wp', 'bp', 'stm', 'ep')

    def __init__(self, wk, bk, wp, bp, stm, ep=None):
        self.wk, self.bk, self.wp, self.bp, self.stm, self.ep = wk, bk, frozenset(wp), frozenset(bp), stm, ep

    def key(self):
        return (self.wk, self.bk, tuple(sorted(self.wp)), tuple(sorted(self.bp)), self.stm, self.ep)

    def text(self, B):
        t = ['K' + B.name(self.wk), 'k' + B.name(self.bk)]
        t += ['P' + B.name(s) for s in sorted(self.wp)]
        t += ['p' + B.name(s) for s in sorted(self.bp)]
        t += [self.stm, B.name(self.ep) if self.ep else '-']
        return ' '.join(t)


def parse(B, line):
    wp, bp, wk, bk, stm, ep = [], [], None, None, None, None
    toks = line.split()
    i = 0
    while i < len(toks):
        t = toks[i]
        if t in ('w', 'b') and stm is None:
            stm = t
            e = toks[i + 1]
            ep = None if e == '-' else (FILES.index(e[0]), int(e[1:]))
            break
        sq = (FILES.index(t[1]), int(t[2:]))
        c = t[0]
        if c == 'K': wk = sq
        elif c == 'k': bk = sq
        elif c == 'P': wp.append(sq)
        elif c == 'p': bp.append(sq)
        i += 1
    return Pos(wk, bk, wp, bp, stm, ep)


def rho(B, beta, sq):
    return sq[1] if beta == 'w' else B.H + 1 - sq[1]


def ep_victim(B, y):
    """square of the pawn that just double-stepped, or None"""
    if y.ep is None:
        return None
    f, r = y.ep
    mover = other(y.stm)
    return (f, r + 1) if mover == 'w' else (f, r - 1)


def attacked_by_pawns(B, y, color, sq):
    """is sq attacked by a pawn of `color`?"""
    f, r = sq
    pw = y.wp if color == 'w' else y.bp
    rr = r - 1 if color == 'w' else r + 1
    return any((g, rr) in pw for g in B.adjfiles(f))


def legal(B, y):
    allp = list(y.wp) + list(y.bp)
    if len(set(allp)) != len(allp):
        return False
    for s in allp:
        if not (2 <= s[1] <= B.H - 1):
            return False
    pcs = allp + [y.wk, y.bk]
    if len(set(pcs)) != len(pcs):
        return False
    if B.kdist(y.wk, y.bk) < 2:
        return False
    # side not to move must not be in check
    nm = other(y.stm)
    ks = y.wk if nm == 'w' else y.bk
    if attacked_by_pawns(B, y, y.stm, ks):
        return False
    if y.ep is not None:
        f, r = y.ep
        mover = other(y.stm)
        if mover == 'w':
            if r != 3: return False
            landed, origin = (f, 4), (f, 2)
            mp = y.wp
        else:
            if r != B.H - 2: return False
            landed, origin = (f, B.H - 3), (f, B.H - 1)
            mp = y.bp
        if landed not in mp: return False
        occ = set(pcs)
        if (f, r) in occ or origin in occ: return False
    return True


def promo_dist(B, rp):
    return B.H - rp - (1 if rp == 2 else 0)


def mu_search(B, y, beta, p, cap):
    """least number of omega moves in G_omega(y;p) after which an omega pawn is on its last rank
    (promoting move included), if <= cap, else cap+1 (meaning > cap)."""
    om = other(beta)
    opw = frozenset(y.wp if om == 'w' else y.bp)
    bpw = frozenset((y.bp if om == 'w' else y.wp)) - {p}
    kings = frozenset((y.wk, y.bk))
    d = 1 if om == 'w' else -1
    start = 2 if om == 'w' else B.H - 1
    last = B.H if om == 'w' else 1
    ept = epv = None
    if y.ep is not None and y.stm == om:
        ept = y.ep
        epv = ep_victim(B, y)
        if epv == p:
            ept = None   # p deleted; nothing to capture (cannot happen under H1)

    def succ(opw, bpw, first):
        occ = opw | bpw | kings
        out = []
        for (f, r) in opw:
            r1 = r + d
            if not (1 <= r1 <= B.H):
                continue
            rest = opw - {(f, r)}
            if (f, r1) not in occ:
                out.append((r1 == last, rest | {(f, r1)}, bpw))
                r2 = r + 2 * d
                if r == start and 1 <= r2 <= B.H and (f, r2) not in occ:
                    out.append((r2 == last, rest | {(f, r2)}, bpw))
            for g in B.adjfiles(f):
                t = (g, r1)
                if t in bpw:
                    out.append((r1 == last, rest | {t}, bpw - {t}))
                elif first and ept is not None and t == ept and epv in bpw:
                    out.append((False, rest | {t}, bpw - {epv}))
        return out

    def exists(opw, bpw, L, first):
        for promo, o2, b2 in succ(opw, bpw, first):
            if promo:
                return True
            if L > 1 and exists(o2, b2, L - 1, False):
                return True
        return False

    for L in range(1, cap + 1):
        if exists(opw, bpw, L, True):
            return L
    return cap + 1


def hyps(B, y, beta, p, full=False, mucap=None):
    """dict with h1..h5 booleans (h5 None if not evaluated), plus e, d, mu (mu = cap+1 means > cap)."""
    om = other(beta)
    s = y.stm
    f, r = p
    rp = rho(B, beta, p)
    bp_set = y.wp if beta == 'w' else y.bp
    op_set = y.bp if beta == 'w' else y.wp
    bkg = y.wk if beta == 'w' else y.bk      # beta's king
    okg = y.bk if beta == 'w' else y.wk      # omega's king
    res = {'h1': None, 'h2': None, 'h3': None, 'h4': None, 'h5': None}
    d = promo_dist(B, rp)
    e = d if s == om else d - 1
    res['d'], res['e'] = d, e
    # H1: passed (e.p. aware) and clear path
    strip = {f} | set(B.adjfiles(f))
    ok1 = all(not (q[0] in strip and rho(B, beta, q) > rp) for q in op_set)
    if ok1 and y.ep is not None and s == om and ep_victim(B, y) == p:
        if any((g, r) in op_set for g in B.adjfiles(f)):
            ok1 = False
    if ok1:
        rng = range(r + 1, B.H + 1) if beta == 'w' else range(r - 1, 0, -1)
        for rr in rng:
            sq = (f, rr)
            if sq in y.wp or sq in y.bp or sq == y.wk or sq == y.bk:
                ok1 = False
                break
    res['h1'] = ok1
    # H4
    res['h4'] = all(not (q != p and q[0] in B.adjfiles(f) and rho(B, beta, q) > rp + 1) for q in bp_set)
    # H2
    badf = set(B.adjfiles(bkg[0]))
    res['h2'] = not any(q[0] in badf for q in list(y.wp) + list(y.bp))
    # H3
    ok3 = False
    allpf = {q[0] for q in list(y.wp) + list(y.bp)}
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == 0 and dr == 0:
                continue
            g = B.nf(okg[0], df)
            rr = okg[1] + dr
            if g is None or not (1 <= rr <= B.H):
                continue
            t = (g, rr)
            if B.kdist(t, bkg) < 2:
                continue
            tf = {g} | set(B.adjfiles(g))
            if tf & allpf:
                continue
            ok3 = True
    res['h3'] = ok3
    # H5
    if (res['h1'] and res['h4'] and res['h2'] and res['h3']) or full:
        cap = max(mucap if mucap is not None else e + 1, 1)
        mu = mu_search(B, y, beta, p, cap)
        res['mu'] = mu
        res['h5'] = mu >= e + 1
    else:
        res['mu'] = None
        res['h5'] = None
    return res


def certified(res):
    return all(res[k] is True for k in ('h1', 'h2', 'h3', 'h4', 'h5'))


def instances(B, y):
    out = []
    for beta in ('w', 'b'):
        for p in (y.wp if beta == 'w' else y.bp):
            res = hyps(B, y, beta, p)
            if certified(res):
                out.append((beta, p, res))
    return out


def run_kp(B, lines, threads=2, extra=()):
    inp = '\n'.join(lines) + '\n'
    cmd = ['/usr/bin/time', '-l', 'nice', '-n', '10', KP, '--board', ('cyl' if B.wrap else 'flat') + ':%dx%d' % (B.W, B.H), '--frozen',
           '--threads', str(threads)] + list(extra)
    pr = subprocess.run(cmd, input=inp, capture_output=True, text=True)
    out = {}
    global MAXRSS
    for ln in pr.stderr.splitlines():
        if 'maximum resident set size' in ln:
            MAXRSS = max(MAXRSS, int(ln.split()[0]))
    for ln in pr.stdout.splitlines():
        if ' | ' in ln:
            a, b = ln.rsplit(' | ', 1)
            out[a] = b.split()
    return out, pr.stderr.strip()
