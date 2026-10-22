"""Check 2 of brief K4: pure sums of test games against known CGT facts (no chess)."""

from testgames import GAMES, plus, neg
from product import pure

# (description, [summands], expected (White starts, Black starts), reading)
FACTS = [
    ('1 + (-1)',            ['1', '-1'],            ('L', 'W'), 'second player wins'),
    ('* + *',               ['*', '*'],             ('L', 'W'), 'second player wins'),
    ('up + down',           ['up', 'down'],         ('L', 'W'), 'second player wins'),
    ('1/2 + 1/2 + (-1)',    ['1/2', '1/2', '-1'],   ('L', 'W'), 'second player wins'),
    ('on + (-2)',           ['on', '-2'],           ('W', 'W'), 'Left wins either way'),
    ('on + off',            ['on', 'off'],          ('D', 'D'), 'draw either way'),
    ('dud + 1',             ['dud', '1'],           ('D', 'D'), 'draw either way'),
    ('over + (-1/2)',       ['over', '-1/2'],       ('L', 'L'), 'Right wins either way'),
    ('over',                ['over'],               ('W', 'W'), 'Left wins either way'),
    ('up + *',              ['up', '*'],            ('W', 'L'), 'first player wins'),
]


def check2():
    """Returns (list of (description, expected, got, reading, ok))."""
    out = []
    for desc, parts, exp, reading in FACTS:
        g = plus(*[GAMES[p] for p in parts]) if len(parts) > 1 else GAMES[parts[0]]
        got = pure(g)
        out.append((desc, exp, got, reading, got == exp))
    return out


if __name__ == '__main__':
    res = check2()
    for desc, exp, got, reading, ok in res:
        print('%-4s %-22s expected %s got %s  (%s)' % ('PASS' if ok else 'FAIL', desc, exp, got, reading))
    print('%d/%d passed' % (sum(r[4] for r in res), len(res)))
