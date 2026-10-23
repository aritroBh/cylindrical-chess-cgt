# Random adversarial tests of Lemma 2 (a),(b) and Lemma 3 (insertion) on arbitrary positions with a pattern arc.
import sys, random
from eng import *
from pump import expected, ins, insn, cls

def menu(rng):
    c = rng.random()
    W = lambda *rs: sum(1 << (r - 1) for r in rs)
    if c < 0.10: return (0, 0)
    if c < 0.35:
        r = rng.randint(2, 7); return (W(r), 0)
    if c < 0.60:
        r = rng.randint(2, 7); return (0, W(r))
    if c < 0.75:
        a = rng.randint(2, 7); b = rng.randint(2, 7)
        return (W(a), W(b)) if a != b else (W(a), 0)
    if c < 0.85:
        a, b = sorted(rng.sample(range(2, 8), 2)); return (W(a, b), 0)
    if c < 0.93:
        a, b = sorted(rng.sample(range(2, 8), 2)); return (0, W(a, b))
    a, b, d = sorted(rng.sample(range(2, 8), 3))
    return (W(a, b), W(d)) if rng.random() < .5 else (W(a), W(b, d))

def make(rng, kind, n, c, nmut, radius, near_boundary=True, lohi=None):
    pos = [expected(kind, j) for j in range(n)]
    lo_, hi_ = lohi if lohi else (c - 4, c + 5)   # protected arc
    cand = [j for j in range(n) if not (lo_ <= j <= hi_)]
    # bias towards the boundary files
    near = [j for j in cand if lo_ - 3 <= j <= hi_ + 3]
    for _ in range(nmut):
        j = rng.choice(near) if (near and near_boundary and rng.random() < 0.7) else rng.choice(cand)
        pos[j] = menu(rng)
    return tuple(pos)

def test_l3(kind, trials, seed, radius_shrink=0, mutate_rule=False):
    rng = random.Random(seed)
    n_ok = n_skip = n_bad = 0
    ex = None
    for t in range(trials):
        n = rng.randint(16, 22)
        c = rng.randint(5, n - 7)           # arc c-4..c+5 inside 0..n-1
        pos = make(rng, kind, n, c, rng.randint(1, 4), 5)
        if passed_ranks(pos, None, 'W') or passed_ranks(pos, None, 'B'):
            n_skip += 1; continue
        # shrink the pattern radius: damage the arc (test sensitivity) : replace file c-4 and c+5 etc by junk
        if radius_shrink:
            lst = list(pos)
            for j in ([c - 4 + i for i in range(radius_shrink)] + [c + 5 - i for i in range(radius_shrink)]):
                if rng.random() < 0.8: lst[j] = menu(rng)
            pos = tuple(lst)
            if passed_ranks(pos, None, 'W') or passed_ranks(pos, None, 'B'):
                n_skip += 1; continue
        ph = ins(pos, c)
        if passed_ranks(ph, None, 'W') or passed_ranks(ph, None, 'B'):
            n_bad += 1; ex = ex or ('phat passed', kind, pos, c); continue
        a = cls(pos, None); b = cls(ph, None)
        good = True
        for s in 'WB':
            if a[s][0] != b[s][0] or {insn((q, qe), c) for q, qe in a[s][1]} != set(b[s][1]): good = False
        n_ok += good; n_bad += (not good)
        if not good and ex is None: ex = ('mismatch', kind, pos, c)
    return n_ok, n_skip, n_bad, ex

def test_l2(kind, trials, seed):
    rng = random.Random(seed)
    cnt_a = bad_a = cnt_b = bad_b = 0
    ex = None
    for t in range(trials):
        n = rng.randint(12, 20)
        j0 = rng.randint(3, n - 4)
        w = rng.choice((1, 2, 3))
        pos = make(rng, kind, n, j0, rng.randint(1, 5), 5, lohi=(j0 - w, j0 + w))
        ep = None
        # random flag (protecting the non-mover): pick a mover Z and a stepped pawn of Y beside an enemy pawn
        Z = rng.choice('WB'); Y = other(Z)
        if rng.random() < 0.4:
            f = rng.randrange(n)
            r2 = 4 if Y == 'W' else 5; r1 = 3 if Y == 'W' else 6; r0 = 2 if Y == 'W' else 7
            m = (1 << (r0 - 1)) | (1 << (r1 - 1)) | (1 << (r2 - 1))
            a = list(pos[f]); a[0] &= ~m; a[1] &= ~m; a[0 if Y == 'W' else 1] |= 1 << (r2 - 1)
            lst = list(pos); lst[f] = tuple(a)
            g = (f + rng.choice((-1, 1))) % n
            e = 1 if Y == 'W' else 0
            b_ = list(lst[g]); b_[0] &= ~(1 << (r2 - 1)); b_[1] &= ~(1 << (r2 - 1)); b_[e] |= 1 << (r2 - 1); lst[g] = tuple(b_)
            pos = tuple(lst); ep = (f, Y)
        if passed_ranks(pos, ep, 'W') or passed_ranks(pos, ep, 'B'): continue
        # wall pawns q of Z with pattern files j-1,j,j+1
        for j in range(n):
            if not all(pos[(j + d) % n] == expected(kind, (j + d) % n) and 0 <= j + d < n for d in (-1, 0, 1)): continue
            own = pos[j][0 if Z == 'W' else 1]
            if bin(own).count('1') != 1 or (pos[j][1 if Z == 'W' else 0]): continue
            # the file must have Z's pawn at its pattern position
            # all moves of this pawn only: filter moves of the whole position to those that change file j's Z-mask
            kidx = 0 if Z == 'W' else 1
            mv = [(np_, ne) for np_, ne in moves(pos, ep, Z) if np_[j][kidx] != pos[j][kidx]]
            for np_, ne in mv:
                cnt_a += 1
                if passed_ranks(np_, ne, Z):
                    bad_a += 1; ex = ex or ('a', kind, pos, ep, j, Z)
            # (b): no flag, files j-1..j+3 or j-3..j+1 pattern
            if ep is None:
                okR = all(0 <= j + d < n and pos[j + d] == expected(kind, j + d) for d in (-1, 0, 1, 2, 3))
                okL = all(0 <= j + d < n and pos[j + d] == expected(kind, j + d) for d in (-3, -2, -1, 0, 1))
                if okR or okL:
                    for np_, ne in mv:
                        st = status(np_, ne, Z)
                        if st == Z: kind_ = 'T'
                        elif st == Y: kind_ = 'L'
                        else:
                            kind_ = 'K'
                            for np2, ne2 in moves(np_, ne, Y):
                                if status(np2, ne2, Y) == Y: kind_ = 'P'; break
                        cnt_b += 1
                        if kind_ in 'TK':
                            bad_b += 1; ex = ex or ('b', kind, pos, ep, j, Z, kind_)
    return cnt_a, bad_a, cnt_b, bad_b, ex

if __name__ == '__main__':
    what = sys.argv[1]; kind = sys.argv[2]; trials = int(sys.argv[3]); seed = int(sys.argv[4])
    if what == 'l3':
        sh = int(sys.argv[5]) if len(sys.argv) > 5 else 0
        print('L3', kind, 'trials', trials, 'shrink', sh, test_l3(kind, trials, seed, sh))
    else:
        print('L2', kind, trials, test_l2(kind, trials, seed))
