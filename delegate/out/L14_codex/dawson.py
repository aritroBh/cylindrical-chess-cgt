"""Dawson macro-moves from compulsory pawn captures, with xor on empty-file cuts."""
from functools import cache


def moves(p, side, ring):
    takes, pushes = [], []
    for f, col in enumerate(p):
        # A file is an integer bitmask. Lower 3 bits white, upper 3 black.
        for r in ((0,1) if side == 0 else (1,2)):
            here = 1 << (3*side+r)
            if not col & here:
                continue
            dest = r + (1 if side == 0 else -1)
            mover, victim = 1 << (3*side+dest), 1 << (3*(1-side)+dest)
            if not col & (mover|victim):
                q = list(p)
                q[f] ^= here|mover
                pushes.append(tuple(q))
            for j in (f-1,f+1):
                if not ring and not 0 <= j < len(p):
                    continue
                j %= len(p)
                if p[j] & victim:
                    q = list(p)
                    q[f] ^= here
                    q[j] ^= victim|mover
                    takes.append(tuple(q))
    return takes, pushes


@cache
def value(p, s, ring):
    # Empty files isolate strips. Ignore the inert middle file only if it has no moves.
    if 0 in p:
        if ring:
            i = p.index(0)
            return value(p[i+1:]+p[:i],s,False)
        i = p.index(0)
        return value(p[:i],s,False) ^ value(p[i+1:],s,False)
    forced, pushes = moves(p,s,ring)
    assert not forced
    options = set()
    for q in pushes:
        frontier = [(q,1-s)]
        outcomes = set()
        while frontier:
            x, t = frontier.pop()
            caps, _ = moves(x,t,ring)
            if caps:
                frontier.extend((z,1-t) for z in caps)
            else:
                assert t != s
                outcomes.add(value(x,t,ring))
        assert len(outcomes) == 1
        options.update(outcomes)
    return next(j for j in range(len(options)+1) if j not in options)


if __name__ == '__main__':
    row = []
    for n in range(3,21):
        a,b = (value((33,)*n,s,True) for s in (0,1))
        assert a == b
        row.append(a)
    # For the longer range independently apply the published strip recurrence.
    g = [0,1]
    for length in range(2,58):
        opts = {g[length-2]} | {g[i]^g[length-3-i] for i in range(length-2)}
        g.append(next(j for j in range(len(opts)+1) if j not in opts))
    wins = [n for n in range(3,61) if g[n-3] == 0]
    assert row == [int(n in wins) for n in range(3,21)]
    print('pawn macro Grundy, n=3..20',row)
    print('winning widths by strip recurrence through 60',wins)
