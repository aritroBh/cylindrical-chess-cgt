"""growlib.py -- ring representation, canonical form, passed-pawn test and the local-growth moves.

A ring is a tuple of files; a file is (W, B) with W, B sorted tuples of ranks (2..7).
Token text matches rg's input: "W4B7 B6 W2" ('-' for an empty file).
"""
import itertools

RANKS = range(2, 8)
MAXFILES = 16


def parse_token(tok):
    w, b, mode = [], [], None
    if tok == '-':
        return ((), ())
    for ch in tok:
        if ch == 'W':
            mode = 'w'
        elif ch == 'B':
            mode = 'b'
        else:
            (w if mode == 'w' else b).append(int(ch))
    return (tuple(sorted(w)), tuple(sorted(b)))


def parse(s):
    return tuple(parse_token(t) for t in s.split())


def fmt_file(f):
    w, b = f
    if not w and not b:
        return '-'
    return ('W' + ''.join(map(str, w)) if w else '') + ('B' + ''.join(map(str, b)) if b else '')


def fmt(r):
    return ' '.join(fmt_file(f) for f in r)


def npawns(r):
    return sum(len(w) + len(b) for w, b in r)


def is_ring(r):
    return all(w or b for w, b in r)


def has_passed(r, side):
    n = len(r)
    for f in range(n):
        mine = r[f][side]
        if not mine:
            continue
        a, c = (f - 1) % n, (f + 1) % n
        if side == 0:
            hi = max([x for g in (a, f, c) for x in r[g][1]], default=0)
            for rk in mine:
                if not hi > rk:
                    return True
        else:
            lo = min([x for g in (a, f, c) for x in r[g][0]], default=99)
            for rk in mine:
                if not lo < rk:
                    return True
    return False


def any_passed(r):
    return has_passed(r, 0) or has_passed(r, 1)


# ---- symmetry: file rotation, file reflection, colour reversal (swap W/B, rank r -> 9-r) ----
def colour_flip(r):
    return tuple((tuple(sorted(9 - x for x in b)), tuple(sorted(9 - x for x in w))) for w, b in r)


def variants(r):
    n = len(r)
    out = []
    for base in (r, colour_flip(r)):
        for refl in (base, base[::-1]):
            for k in range(n):
                out.append(refl[k:] + refl[:k])
    return out


def canon(r):
    return min(variants(r))


# ---- moves ----
def _put(r, f, color, rank):
    """return ring with a pawn added, or None if the square is occupied"""
    w, b = r[f]
    if rank in w or rank in b:
        return None
    if color == 0:
        nf = (tuple(sorted(w + (rank,))), b)
    else:
        nf = (w, tuple(sorted(b + (rank,))))
    return r[:f] + (nf,) + r[f + 1:]


def add1(r):
    out = []
    for f in range(len(r)):
        for color in (0, 1):
            for rank in RANKS:
                q = _put(r, f, color, rank)
                if q is not None:
                    out.append(q)
    return out


def pair_same(r, gap):
    out = []
    for f in range(len(r)):
        for rk in RANKS:
            if rk + gap > 7:
                continue
            q = _put(r, f, 0, rk)
            if q is None:
                continue
            q = _put(q, f, 1, rk + gap)
            if q is not None:
                out.append(q)
    return out


def pair_adj(r, gap=2):
    out = []
    n = len(r)
    for f in range(n):
        g = (f + 1) % n
        for rk in RANKS:
            if rk + gap > 7:
                continue
            for cw, cb in ((0, 1), (1, 0)):          # white on f / black on g  and the reverse
                q = _put(r, f, cw, rk if cw == 0 else rk + gap)
                if q is None:
                    continue
                q = _put(q, g, cb, rk + gap if cb == 1 else rk)
                if q is not None:
                    out.append(q)
    return out


def remove1(r):
    out = []
    for f in range(len(r)):
        w, b = r[f]
        for i in range(len(w)):
            out.append(r[:f] + ((w[:i] + w[i + 1:], b),) + r[f + 1:])
        for i in range(len(b)):
            out.append(r[:f] + ((w, b[:i] + b[i + 1:]),) + r[f + 1:])
    return out


def _single_files():
    return [((x,), ()) for x in RANKS] + [((), (x,)) for x in RANKS]


def _pair_files():
    out = []
    for x in RANKS:
        for y in RANKS:
            if x != y:
                out.append(((x,), (y,)))          # W x + B y on one file
    for x, y in itertools.combinations(RANKS, 2):
        out.append(((x, y), ()))                  # doubled white
        out.append(((), (x, y)))                  # doubled black
    return out


SINGLES = _single_files()
PAIRFILES_WB = [((x,), (y,)) for x in RANKS for y in RANKS if x != y]
PAIRFILES_DBL = [((x, y), ()) for x, y in itertools.combinations(RANKS, 2)] + \
                [((), (x, y)) for x, y in itertools.combinations(RANKS, 2)]


def insert1(r, kinds=('single', 'wb', 'dbl')):
    """insert ONE new file (1 pawn, or 2 pawns) in each of the n gaps"""
    out = []
    files = []
    if 'single' in kinds:
        files += SINGLES
    if 'wb' in kinds:
        files += PAIRFILES_WB
    if 'dbl' in kinds:
        files += PAIRFILES_DBL
    for k in range(len(r)):
        for nf in files:
            out.append(r[:k] + (nf,) + r[k:])
    return out


def insert2(r):
    """insert TWO adjacent new files, one pawn each (two pawns in all) in each of the n gaps"""
    out = []
    for k in range(len(r)):
        for a in SINGLES:
            for b in SINGLES:
                out.append(r[:k] + (a, b) + r[k:])
    return out


# move classes, in priority order (cheap and most local first)
MOVE_CLASSES = [
    ('add1', add1),
    ('pair_same2', lambda r: pair_same(r, 2)),
    ('pair_adj2', lambda r: pair_adj(r, 2)),
    ('remove1', remove1),
    ('ins1_single', lambda r: insert1(r, ('single',))),
    ('ins1_wb', lambda r: insert1(r, ('wb',))),
    ('ins2_single', insert2),
    ('ins1_dbl', lambda r: insert1(r, ('dbl',))),
    ('pair_same3', lambda r: pair_same(r, 3)),     # extension: the same-file pairs of the seeds are W r / B r+3
]


def neighbours(r, classes=None):
    """yield (class_name, ring) for every move; rings with a passed pawn, > MAXFILES files or empty are dropped"""
    for name, fn in MOVE_CLASSES:
        if classes is not None and name not in classes:
            continue
        for q in fn(r):
            if len(q) > MAXFILES or npawns(q) == 0:
                continue
            if any_passed(q):
                continue
            yield name, q


def Q(n):
    assert n >= 8 and n % 2 == 0
    k = (n - 8) // 2
    return "W4 B7 " + "B4 W2 " * k + "W3B6 W3 W2B5 B5 W2 B4"
