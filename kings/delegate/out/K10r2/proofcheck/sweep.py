import sys, os, random, itertools, collections, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chk import *


def all_ep_options(B, wp, bp, wk, bk, stm):
    """list of ep target squares that are consistent for (pawns, stm)"""
    occ = set(wp) | set(bp) | {wk, bk}
    out = []
    mover = other(stm)
    if mover == 'w':
        for (f, r) in wp:
            if r == 4 and (f, 3) not in occ and (f, 2) not in occ:
                out.append((f, 3))
    else:
        rr = B.H - 3
        for (f, r) in bp:
            if r == rr and (f, B.H - 2) not in occ and (f, B.H - 1) not in occ:
                out.append((f, B.H - 2))
    return out


def features(B, y, beta, p, res):
    om = other(beta)
    f, r = p
    rp = rho(B, beta, p)
    bps = y.wp if beta == 'w' else y.bp
    ops = y.bp if beta == 'w' else y.wp
    okg = y.bk if beta == 'w' else y.wk
    adj = B.adjfiles(f)
    F = set()
    F.add('s=omega' if y.stm == om else 's=beta')
    F.add('beta=' + ('White' if beta == 'w' else 'Black'))
    if any(q != p and q[0] in adj and rho(B, beta, q) == rp + 1 for q in bps):
        F.add('H4_at_bound(other beta pawn at rho(p)+1 on adjacent file)')
    if any(q[0] == f and rho(B, beta, q) < rp for q in bps):
        F.add('beta_pawn_behind_p_on_p_file')
        for q in bps:
            if q[0] == f and rho(B, beta, q) < rp:
                if any((g, q[1] + (1 if om == 'w' else -1) * 0) in ops for g in ()):
                    pass
    # omega pawn attacking a beta pawn (possible capture) classification
    dm = 1 if om == 'w' else -1
    for q in bps:
        if q == p:
            continue
        # omega pawn positioned to capture q: at (g, q.r - dm) with g adjacent to q.file
        att = [o for o in ops if o[1] == q[1] - dm and o[0] in B.adjfiles(q[0])]
        if att:
            if q[0] == f and rho(B, beta, q) < rp:
                F.add('capture_of_beta_pawn_behind_p_on_p_file_available')
            if q[0] in adj:
                F.add('capture_of_beta_pawn_on_adjacent_file_available')
                if any(o[0] not in ({f} | set(adj)) for o in att):
                    F.add('omega_pawn_enters_strip_by_capture_from_two_files_away')
    if y.ep is not None:
        v = ep_victim(B, y)
        if y.stm == om and v != p and v in bps:
            F.add('ep_right_for_omega_against_another_beta_pawn')
            if any(o[1] == v[1] and o[0] in B.adjfiles(v[0]) for o in ops):
                F.add('ep_capturable_by_omega_pawn_now')
                if v[0] in adj:
                    F.add('ep_victim_on_adjacent_file')
        if y.stm == beta:
            F.add('ep_right_for_beta')
    # p attacks omega king
    if attacked_by_pawns(B, y, beta, okg) and any(
            okg == (g, r + (1 if beta == 'w' else -1)) for g in adj):
        F.add('p_gives_check_to_omega_king')
    if y.stm == om and attacked_by_pawns(B, y, beta, okg):
        F.add('omega_in_check_at_y(any beta pawn)')
    # race: omega has a passer (no beta pawn ahead of it in its strip)
    for o in ops:
        st = {o[0]} | set(B.adjfiles(o[0]))
        # ahead for omega = smaller rho
        if not any(q[0] in st and rho(B, beta, q) < rho(B, beta, o) for q in bps):
            F.add('omega_has_a_passer(race)')
            break
    if res['mu'] == res['e'] + 1:
        F.add('H5_tight(mu=e+1)')
    if y.wk[0] != 0 or y.bk[0] != 0:
        F.add('kings_not_both_on_a_file')
    else:
        F.add('kings_both_on_a_file')
    return F


class Tally:
    def __init__(self):
        self.pos_tested = 0       # (position, s) queried in kpsolve
        self.pos_generated = 0
        self.inst_cert = 0
        self.violations = []
        self.feat = collections.Counter()
        self.xs = []              # positions kp rejected as illegal while checker said legal
        self.both = []            # positions where both colours certified
        self.perboard = collections.Counter()


def run_batch(B, items, T, label):
    """items: dict text -> list of (beta, p, features)"""
    if not items:
        return
    lines = list(items.keys())
    out, err = run_kp(B, lines)
    for ln in lines:
        r = out.get(ln)
        T.pos_tested += 1
        if r is None or r[0] == 'X':
            T.xs.append((label, ln, r))
            continue
        for beta, p, F in items[ln]:
            T.inst_cert += 1
            win = (r[0] == 'W') if beta == 'w' else (r[0] == 'L')
            ok2 = (r[1] == 'W') if beta == 'w' else (r[1] == 'L')
            for ft in F:
                T.feat[ft] += 1
            if not (win and ok2):
                T.violations.append((label, ln, beta, B.name(p), r))
        if len({b for b, _, _ in items[ln]}) > 1:
            T.both.append((label, ln))


def process(B, gen, T, label, batch=30000, dedupe=True, maxpos=None):
    seen = set()
    items = {}
    n = 0
    t0 = time.time()
    for y in gen:
        k = y.key()
        if dedupe:
            if k in seen:
                continue
            seen.add(k)
        if not legal(B, y):
            continue
        T.pos_generated += 1
        inst = instances(B, y)
        if inst:
            txt = y.text(B)
            items[txt] = [(b, p, features(B, y, b, p, res)) for b, p, res in inst]
            if len(items) >= batch:
                run_batch(B, items, T, label)
                items = {}
        n += 1
        if maxpos and n >= maxpos:
            break
    run_batch(B, items, T, label)
    T.perboard[label] = (T.pos_generated, T.pos_tested, T.inst_cert)
    return time.time() - t0


# ------------ generators ------------

def kingpairs_afile(B, free_rank=True):
    out = []
    for a in range(1, B.H + 1):
        for b in range(1, B.H + 1):
            if abs(a - b) >= 2:
                out.append(((0, a), (0, b)))
    return out


def gen_exhaustive(B, files, maxper, kings, eps=True, ranks=None):
    ranks = ranks or list(range(2, B.H))
    sqs = [(f, r) for f in files for r in ranks]
    n = len(sqs)
    # enumerate assignments with <= maxper pawns per side
    def rec(i, w, b):
        if i == n:
            yield tuple(w), tuple(b)
            return
        yield from rec(i + 1, w, b)
        if len(w) < maxper:
            w.append(sqs[i]); yield from rec(i + 1, w, b); w.pop()
        if len(b) < maxper:
            b.append(sqs[i]); yield from rec(i + 1, w, b); b.pop()
    for w, b in rec(0, [], []):
        if not w and not b:
            continue
        for wk, bk in kings:
            for stm in ('w', 'b'):
                yield Pos(wk, bk, w, b, stm, None)
                if eps:
                    for e in all_ep_options(B, w, b, wk, bk, stm):
                        yield Pos(wk, bk, w, b, stm, e)


def rand_king_pair(B, rnd):
    while True:
        a = (rnd.randrange(B.W), rnd.randint(1, B.H))
        b = (rnd.randrange(B.W), rnd.randint(1, B.H))
        if B.kdist(a, b) >= 2:
            return a, b


def sq_from_rho(B, beta, f, rh):
    return (f % B.W, rh if beta == 'w' else B.H + 1 - rh)


def gen_scene(B, rnd, parked=False, free=True):
    """a random scene built around a beta pawn p, with roles that make the proof tight"""
    beta = rnd.choice('wb')
    om = other(beta)
    f = rnd.randrange(B.W)
    rp = rnd.randint(2, B.H - 1)
    p = sq_from_rho(B, beta, f, rp)
    bps = {p}
    ops = set()

    def add(color, sq):
        if not (2 <= sq[1] <= B.H - 1):
            return False
        if sq in bps or sq in ops:
            return False
        (bps if color == beta else ops).add(sq)
        return True

    roles = rnd.sample(['h4', 'behind', 'enter', 'ep', 'race', 'rand', 'rand', 'rand', 'near', 'ompawn'],
                       rnd.randint(1, 4))
    for ro in roles:
        if ro == 'h4':
            g = f + rnd.choice((-1, 1))
            q = sq_from_rho(B, beta, g, rp + rnd.choice((-1, 0, 1, 1, 2)))
            if add(beta, q):
                # omega pawn ready to capture q from either side
                o = sq_from_rho(B, beta, g + rnd.choice((-1, 1)), rho(B, beta, q) + 1)
                if rnd.random() < 0.7:
                    add(om, o)
        elif ro == 'behind':
            if rp > 2:
                q = sq_from_rho(B, beta, f, rnd.randint(2, rp - 1))
                if add(beta, q) and rnd.random() < 0.8:
                    o = sq_from_rho(B, beta, f + rnd.choice((-1, 1)), rho(B, beta, q) + 1)
                    add(om, o)
        elif ro == 'enter':
            g = f + rnd.choice((-1, 1))
            q = sq_from_rho(B, beta, g, rnd.randint(2, rp + 2))
            if add(beta, q):
                o = sq_from_rho(B, beta, g + (g - f), rho(B, beta, q) + 1)
                add(om, o)
        elif ro == 'ep':
            # a beta pawn just double-stepped (rho 4), omega pawn beside it
            g = f + rnd.choice((-2, -1, 1, 2, 3, -3))
            q = sq_from_rho(B, beta, g, 4)
            if add(beta, q):
                if rnd.random() < 0.9:
                    add(om, sq_from_rho(B, beta, g + rnd.choice((-1, 1)), 4))
        elif ro == 'race':
            g = f + rnd.choice((2, 3, -2, -3, 4))
            add(om, sq_from_rho(B, beta, g, rnd.randint(3, B.H - 1)))
        elif ro == 'near':
            # omega pawn near the strip, behind or level with p
            g = f + rnd.choice((-1, 0, 1, -2, 2))
            add(om, sq_from_rho(B, beta, g, rnd.randint(2, B.H - 1)))
        elif ro == 'ompawn':
            g = f + rnd.choice((-1, 1))
            add(om, sq_from_rho(B, beta, g, rnd.randint(2, min(rp + 1, B.H - 1))))
        else:
            g = f + rnd.randint(-3, 3)
            add(rnd.choice('wb'), (g % B.W, rnd.randint(2, B.H - 1)))
    # kings
    mode = rnd.random()
    pkings = None
    if parked or mode < 0.35:
        pairs = kingpairs_afile(B)
        wk, bk = rnd.choice(pairs)
        if rnd.random() < 0.5:
            fa = rnd.randrange(B.W)
            wk, bk = (fa, wk[1]), (fa, bk[1])
    elif mode < 0.55:
        # omega king near p (checks, diagonal-ahead squares)
        okf = f + rnd.choice((-1, 1, 0, 2, -2))
        okr = rho(B, beta, p) + rnd.choice((1, 1, 0, 2, -1))
        okr = sq_from_rho(B, beta, okf, okr)
        ok = (okr[0], min(max(okr[1], 1), B.H))
        for _ in range(100):
            bk_ = (rnd.randrange(B.W), rnd.randint(1, B.H))
            if B.kdist(ok, bk_) >= 2:
                break
        wk, bk = (bk_, ok) if beta == 'w' else (ok, bk_)
        # wk/bk naming: wk=white king, bk=black king
        if beta == 'w':
            wk, bk = bk_, ok
        else:
            wk, bk = ok, bk_
    else:
        wk, bk = rand_king_pair(B, rnd)
    wp = bps if beta == 'w' else ops
    bp = ops if beta == 'w' else bps
    stm = rnd.choice('wb')
    ep = None
    opts = all_ep_options(B, wp, bp, wk, bk, stm)
    if opts and rnd.random() < 0.8:
        ep = rnd.choice(opts)
    return Pos(wk, bk, wp, bp, stm, ep)


def gen_random_scenes(B, n, seed, parked=False):
    rnd = random.Random(seed)
    for _ in range(n):
        yield gen_scene(B, rnd, parked=parked)


def gen_uniform(B, n, seed, files=None, maxper=3, parked=False):
    """uniform random pawns on given files, <= maxper per side, kings free or on a-file"""
    rnd = random.Random(seed)
    files = files or list(range(B.W))
    for _ in range(n):
        nw, nb = rnd.randint(0, maxper), rnd.randint(0, maxper)
        if nw + nb == 0:
            continue
        sqs = [(f, r) for f in files for r in range(2, B.H)]
        pick = rnd.sample(sqs, min(nw + nb, len(sqs)))
        w, b = pick[:nw], pick[nw:nw + nb]
        if parked:
            wk, bk = rnd.choice(kingpairs_afile(B))
        else:
            wk, bk = rand_king_pair(B, rnd)
        stm = rnd.choice('wb')
        ep = None
        opts = all_ep_options(B, w, b, wk, bk, stm)
        if opts and rnd.random() < 0.7:
            ep = rnd.choice(opts)
        yield Pos(wk, bk, w, b, stm, ep)
