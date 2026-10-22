"""Verifier A, check 2: known CGT facts, solved with the pure product code."""
import vgames as gm
import vproduct as pr

N = gm.named
S = lambda *gs: _sum(gs)


def _sum(gs):
    g = gs[0]
    for h in gs[1:]:
        g = gm.add(g, h)
    return g


def half():
    return N('1/2')


FACTS = [
    ('1 + (-1): second player wins', _sum([N('1'), N('-1')]), ('L', 'W')),
    ('* + *: second player wins', _sum([N('*'), N('*')]), ('L', 'W')),
    ('up + down: second player wins', _sum([N('up'), N('down')]), ('L', 'W')),
    ('1/2 + 1/2 + (-1): second player wins', _sum([N('1/2'), N('1/2'), N('-1')]), ('L', 'W')),
    ('on + (-2): Left wins either way', _sum([N('on'), N('-2')]), ('W', 'W')),
    ('on + off: draw either way', _sum([N('on'), N('off')]), ('D', 'D')),
    ('dud + 1: draw either way', _sum([N('dud'), N('1')]), ('D', 'D')),
    ('over + (-1/2): Right wins either way', _sum([N('over'), N('-1/2')]), ('L', 'L')),
    ('over: Left wins either way', N('over'), ('W', 'W')),
    ('up + *: first player wins', _sum([N('up'), N('*')]), ('W', 'L')),
]


def run():
    ok = True
    for name, g, want in FACTS:
        got = pr.solve_pure(g)
        good = got == want
        ok &= good
        print('%-42s got (W-starts,B-starts)=%s want=%s %s' % (name, got, want, 'PASS' if good else 'FAIL'))
    return ok


if __name__ == '__main__':
    import sys
    sys.exit(0 if run() else 1)
