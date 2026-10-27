"""diff_rules.py -- differential test of oddeng.py (this directory) against
  E = verify_compute/myeng.py   (moves, passed pawns, verdict),
  C = check3/eng.py             (moves, passed pawns, status),
  P = cylcgt/pawns.py           (RULES ONLY: moves, passed, promote_distance; no game-value / cgt code is touched),
on positions reached by random walks (arbitrary legal moves of either colour, terminal or not) from the starts of R_n, Qo_n
(n = 9, 11, 13, 15) and from random pawn scatterings on small cylinders, with e.p. flags (raw flags for the pawns.py comparison).
Any difference is printed; the last line is the verdict.   Usage: python diff_rules.py [seed] [walks]
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'verify_compute'))
sys.path.insert(0, os.path.join(HERE, '..', 'check3'))
sys.path.insert(0, ROOT)
import oddeng as O          # noqa: E402
import myeng as E           # noqa: E402
import eng as C             # noqa: E402
from cylcgt import pawns as P   # noqa: E402

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
walks = int(sys.argv[2]) if len(sys.argv) > 2 else 400
rnd = random.Random(seed)
bad = {'moves_E': 0, 'moves_C': 0, 'moves_P': 0, 'passed_E': 0, 'passed_C': 0, 'passed_P': 0, 'verdict_E': 0,
       'verdict_C': 0, 'verdict_P': 0, 'dist_E': 0, 'dist_P': 0}
cnt = {'positions': 0, 'moves': 0, 'flagged': 0, 'caps_live_flag': 0, 'both_passed': 0, 'one_passed': 0}


def pawnspos(pos, flag):
    """oddeng (pos, raw flag) -> cylcgt Pos."""
    w = frozenset((f, r) for f, s in enumerate(pos) for r in range(1, 9) if (s >> (r - 1)) & 1)
    b = frozenset((f, r) for f, s in enumerate(pos) for r in range(1, 9) if (s >> (8 + r - 1)) & 1)
    ep = None
    if flag is not None:
        f, c = flag
        r2 = 4 if c == 0 else 5
        r1 = 3 if c == 0 else 6
        ep = ((f, r1), (f, r2), 'B' if c == 0 else 'W')
    return P.Pos(w, b, ep)


def from_pawnspos(pp, n):
    lst = [0] * n
    for f, r in pp.white:
        lst[f] |= 1 << (r - 1)
    for f, r in pp.black:
        lst[f] |= 1 << (8 + r - 1)
    flag = None
    if pp.ep is not None:
        (f, _), (_, r2), capside = pp.ep
        flag = (f, 0 if capside == 'B' else 1)
    return tuple(lst), flag


def canon(pos, flag):
    """drop an inert flag (no enemy pawn beside the stepper)."""
    if flag is None:
        return None
    f, c = flag
    n = len(pos)
    r2 = 4 if c == 0 else 5
    se = 8 * (1 - c)
    return flag if ((pos[f - 1] | pos[(f + 1) % n]) >> (se + r2 - 1)) & 1 else None


def check_position(pos, flag):
    """pos: oddeng tuple, flag: canonical flag.  Compare everything."""
    n = len(pos)
    cnt['positions'] += 1
    if flag is not None:
        cnt['flagged'] += 1
    pairs = O.to_pairs(pos)
    Eflag = flag                                   # myeng: (file, colour int)
    Cflag = None if flag is None else (flag[0], 'WB'[flag[1]])
    Ppos = pawnspos(pos, flag)
    board = P.Board(n, 8, True, True)
    for c in (0, 1):
        # passed pawns
        mine = sorted(O.passed(pos, flag, c))
        e_ = sorted(E.passed_pawns(pairs, Eflag, c))
        c_ = sorted(C.passed_ranks(pairs, Cflag, 'WB'[c]))
        if mine != e_:
            bad['passed_E'] += 1
            print('PASSED differs from E', pos, flag, c, mine, e_)
        if mine != c_:
            bad['passed_C'] += 1
            print('PASSED differs from C', pos, flag, c, mine, c_)
        if bool(mine) != P.passed(board, Ppos, 'WB'[c]):
            bad['passed_P'] += 1
            print('PASSED differs from pawns.py', pos, flag, c, mine)
        # promotion distance (only meaningful if passed)
        dm = O.promo_dist(pos, flag, c)
        de = E.promo_dist(pairs, Eflag, c)
        dp = P.promote_distance(board, Ppos, 'WB'[c])
        if dm != de:
            bad['dist_E'] += 1
            print('DIST differs from E', pos, flag, c, dm, de)
        if dm != dp:
            bad['dist_P'] += 1
            print('DIST differs from pawns.py', pos, flag, c, dm, dp)
        # moves
        mv = O.gen(pos, flag, c)
        cnt['moves'] += len(mv)
        mv_pairs = {(O.to_pairs(p), f_) for p, f_ in mv}
        ev = set(E.gen_moves(pairs, Eflag, c))
        cv = set(C.moves(pairs, Cflag, 'WB'[c]))
        cv_norm = {(p, None if f_ is None else (f_[0], 0 if f_[1] == 'W' else 1)) for p, f_ in cv}
        if mv_pairs != ev:
            bad['moves_E'] += 1
            print('MOVES differ from E', pos, flag, c, len(mv_pairs), len(ev))
        if mv_pairs != cv_norm:
            bad['moves_C'] += 1
            print('MOVES differ from C', pos, flag, c, len(mv_pairs), len(cv_norm))
        # pawns.py: raw flags
        mv_raw = O.gen(pos, flag, c, raw=True)
        pm = {(frozenset(x.white), frozenset(x.black), x.ep) for x in P.moves(board, Ppos, 'WB'[c])}
        mm = {(pawnspos(p, f_).white, pawnspos(p, f_).black, pawnspos(p, f_).ep) for p, f_ in mv_raw}
        if pm != mm:
            bad['moves_P'] += 1
            print('MOVES differ from pawns.py', pos, flag, c, len(pm), len(mm))
        # verdict after c moved INTO this position (pos, flag): all engines
        vm = O.verdict(pos, flag, c)
        ve = E.verdict(pairs, Eflag, c)
        vc = C.status(pairs, Cflag, 'WB'[c])
        # pawns.py verdict reconstruction (same logic as pawns._child under RACE_RULE count)
        wpp, bpp = P.passed(board, Ppos, 'W'), P.passed(board, Ppos, 'B')
        if wpp and bpp:
            opp = 'B' if c == 0 else 'W'
            win = opp if P.promote_distance(board, Ppos, opp) <= P.promote_distance(board, Ppos, 'WB'[c]) else 'WB'[c]
            vp = 0 if win == 'W' else 1
            cnt['both_passed'] += 1
        elif wpp:
            vp = 0
            cnt['one_passed'] += 1
        elif bpp:
            vp = 1
            cnt['one_passed'] += 1
        else:
            vp = None
        if vm != ve:
            bad['verdict_E'] += 1
            print('VERDICT differs from E', pos, flag, c, vm, ve)
        if vm != (None if vc is None else 'WB'.index(vc)):
            bad['verdict_C'] += 1
            print('VERDICT differs from C', pos, flag, c, vm, vc)
        if vm != vp:
            bad['verdict_P'] += 1
            print('VERDICT differs from pawns.py', pos, flag, c, vm, vp)
        # e.p. captures actually generated
        if flag is not None and flag[1] != c:
            for p, f_ in mv:
                if npawns_diff(pos, p) == -1:
                    cnt['caps_live_flag'] += 1


def npawns_diff(a, b):
    return O.npawns(b) - O.npawns(a)


def random_scatter(n):
    lst = [0] * n
    for _ in range(rnd.randint(n, 2 * n)):
        f = rnd.randrange(n)
        c = rnd.randrange(2)
        r = rnd.randint(2, 7) if rnd.random() < 0.8 else (2 if c == 0 else 7)
        if lst[f] >> (8 * c) & 255 and rnd.random() < 0.6:
            continue
        if ((lst[f] | (lst[f] >> 8)) >> (r - 1)) & 1:       # a square holds at most one pawn
            continue
        lst[f] |= 1 << (8 * c + r - 1)
    return tuple(lst)


def main():
    starts = [O.start(fam, n) for fam in ('R', 'Qo') for n in (9, 11, 13, 15)]
    for w in range(walks):
        if w % 3 == 2:
            n = rnd.choice([5, 6, 7, 8, 9])
            pos, flag = random_scatter(n), None
        else:
            pos, flag = rnd.choice(starts), None
        c = rnd.randrange(2)
        for ply in range(rnd.randint(2, 45)):
            check_position(pos, flag)
            mv = O.gen(pos, flag, c)
            if not mv:
                c = 1 - c
                mv = O.gen(pos, flag, c)
                if not mv:
                    break
            # prefer double steps / captures a third of the time so that e.p. positions occur
            pos, flag = rnd.choice(mv)
            c = 1 - c
    print('positions', cnt['positions'], 'moves', cnt['moves'], 'flagged', cnt['flagged'], 'captures while a flag is live',
          cnt['caps_live_flag'], 'one-passer verdicts', cnt['one_passed'], 'race verdicts', cnt['both_passed'])
    print('differences', bad)
    print('DIFFERENTIAL TEST', 'PASSED' if not any(bad.values()) else 'FAILED')


if __name__ == '__main__':
    main()
