#!/usr/bin/env python3
"""classify.py BOARD 'pos' BETA(W|B) PSQ : why does the strategy 'beta pushes p every move' fail?
Returns the shortest failing line found by exhaustive search over omega's replies (own move generator, pyp.py)."""
import sys
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/scripts')
import pyp


def sqname(B, s):
    f, r = B.fr(s)
    return chr(97 + f) + str(r + 1)


def strategy_fail(B, st, beta, psq, maxdepth=12):
    """Return (kind, line) of a shortest omega line defeating the strategy, or None if the strategy wins."""
    om = 1 - beta
    memo = {}

    def rec(st, p, depth):
        key = (st, p)
        if key in memo:
            return memo[key]
        memo[key] = None  # cycle guard (cycles never win for beta)
        res = None
        if depth > maxdepth:
            memo[key] = ("too_long", [])
            return memo[key]
        if st[4] == beta:
            mv = pyp.moves(B, st)
            rp = (p // B.W + 1) if beta == 0 else (B.H - p // B.W)
            want = p + (1 if beta == 0 else -1) * B.W * (2 if rp == 2 else 1)  # the strategy: double step first from rho = 2
            pushes = [(k, ns) for k, ns in mv if _is_push(B, st, ns, beta, p) and (_own(ns, beta) - _own(st, beta)) == {want}]
            if not pushes:
                res = ("beta_cannot_push", [])
            else:
                k, ns = pushes[0]
                if k == "promo":
                    res = None  # beta wins
                else:
                    np_ = _new_p(B, st, ns, beta, p)
                    r = rec(ns, np_, depth + 1)
                    if r:
                        res = (r[0], [("B:" + sqname(B, p) + sqname(B, np_))] + r[1])
        else:
            mv = pyp.moves(B, st)
            if not mv:
                res = ("omega_stalemated" if not pyp.in_check(B, st, om) else None, [])
                if res[0] is None:
                    res = None
            else:
                best = None
                for k, ns in mv:
                    if k == "promo":
                        cand = ("omega_promotes", [_mv_text(B, st, ns)])
                    else:
                        if p not in (ns[2] if beta == 0 else ns[3]):
                            cand = ("p_captured", [_mv_text(B, st, ns)])
                        else:
                            r = rec(ns, p, depth + 1)
                            cand = (r[0], [_mv_text(B, st, ns)] + r[1]) if r else None
                    if cand and (best is None or len(cand[1]) < len(best[1])):
                        best = cand
                res = best
        memo[key] = res
        return res

    return rec(st, psq, 0)


def _mv_text(B, st, ns):
    wk, bk, wp, bp, stm, ep = st
    if stm == 0:
        if ns[0] != wk: return "K" + sqname(B, wk) + sqname(B, ns[0])
        a = wp - ns[2]; b = ns[2] - wp
    else:
        if ns[1] != bk: return "k" + sqname(B, bk) + sqname(B, ns[1])
        a = bp - ns[3]; b = ns[3] - bp
    return ("P" if stm == 0 else "p") + sqname(B, next(iter(a))) + sqname(B, next(iter(b)))


def _own(st, c):
    return st[2] if c == 0 else st[3]


def _is_push(B, st, ns, beta, p):
    """ns reached by pushing the pawn p straight ahead (single or double step)"""
    a = _own(st, beta) - _own(ns, beta)
    b = _own(ns, beta) - _own(st, beta)
    if len(a) != 1 or len(b) != 1 or p not in a:
        return False
    if _own(st, 1 - beta) != _own(ns, 1 - beta):
        return False
    t = next(iter(b))
    return t % B.W == p % B.W


def _new_p(B, st, ns, beta, p):
    return next(iter(_own(ns, beta) - _own(st, beta)))


def classify(spec, line, beta, psq_name):
    B = pyp.Board(spec)
    st = pyp.parse(B, line)
    psq = B.sq(ord(psq_name[0]) - 97, int(psq_name[1:]) - 1)
    om = 1 - beta
    if st[4] == om and not pyp.moves(B, st):
        return ("omega_stalemated_at_y" if not pyp.in_check(B, st, om) else "omega_mated_at_y", [])
    r = strategy_fail(B, st, beta, psq)
    return r if r else ("strategy_wins", [])


if __name__ == "__main__":
    spec, line, beta, p = sys.argv[1:5]
    print(classify(spec, line, 0 if beta == 'W' else 1, p))
