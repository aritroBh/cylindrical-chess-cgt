"""Independent verifier-written outcome solver: pawn position G (flat or cylinder, 8 ranks)
plus a nim heap *h.  No import of cylcgt, crosscheck or sumtest.

G = *2  <=>  G + *2 is a P-position (second player wins).
G = 0   <=>  G is a P-position.

Conventions: White = Left, normal play.  After a move in G, if exactly one side has a
passed pawn, that side wins the whole sum outright (BIG).  If both, race rule:
  count: opponent of mover moves first, fewer moves wins, ties to opponent; home-rank pawn
         gets the double step.   mover: mover wins.   opponent: mover loses.
e.p.: double step gives the opponent an e.p. right.  scope 'local' = survives moves in the
nim heap; 'global' = cleared by any move.  passer test 'plain' (static) or 'aware' (a pawn that
may be captured e.p. by the opponent's next move is not yet passed).
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)
NR = 8


def make_solver(F, wrap, ep_on, passer, scope, rule):
    def nbrs(f):
        out = set()
        for g in (f - 1, f + 1):
            if wrap:
                g %= F
            if 0 <= g < F and g != f:
                out.add(g)
        return out

    def is_passed(pawn, side, enemy):
        f, r = pawn
        span = {f} | nbrs(f)
        if side == "W":
            return not any(g in span and s > r for g, s in enemy)
        return not any(g in span and s < r for g, s in enemy)

    def passers(W, B, ep, side):
        mine, theirs = (W, B) if side == "W" else (B, W)
        ps = [p for p in mine if is_passed(p, side, theirs)]
        if passer == "aware" and ep is not None:
            skipped, landed, capturer = ep
            # the pawn that just double-stepped belongs to the non-capturer
            if capturer != side:
                # is a capture actually available?
                cap_side_pawns = theirs
                dr = -1 if capturer == "B" else 1
                can = any((g, skipped[1] - dr) in cap_side_pawns for g in nbrs(skipped[0]))
                if can:
                    ps = [p for p in ps if p != landed]
        return ps

    def steps(ps, side):
        best = 99
        for f, r in ps:
            if side == "W":
                n = NR - r - (1 if r == 2 else 0)
            else:
                n = r - 1 - (1 if r == NR - 1 else 0)
            best = min(best, n)
        return best

    def resolve(W, B, ep, mover):
        wp = passers(W, B, ep, "W")
        bp = passers(W, B, ep, "B")
        if not wp and not bp:
            return None
        if wp and not bp:
            return "W"
        if bp and not wp:
            return "B"
        opp = "B" if mover == "W" else "W"
        if rule == "mover":
            return mover
        if rule == "opponent":
            return opp
        sm = steps(wp if mover == "W" else bp, mover)
        so = steps(bp if mover == "W" else wp, opp)
        return opp if so <= sm else mover

    def gmoves(W, B, ep, side):
        mine, theirs = (W, B) if side == "W" else (B, W)
        d = 1 if side == "W" else -1
        home = 2 if side == "W" else NR - 1
        occ = W | B
        out = []
        for p in mine:
            f, r = p
            rest = mine - {p}
            r1 = r + d
            if not 1 <= r1 <= NR:
                continue
            if (f, r1) not in occ:
                out.append((rest | {(f, r1)}, theirs, None))
                if r == home and (f, r + 2 * d) not in occ:
                    nep = ((f, r1), (f, r + 2 * d), "B" if side == "W" else "W") if ep_on else None
                    out.append((rest | {(f, r + 2 * d)}, theirs, nep))
            for g in nbrs(f):
                t = (g, r1)
                if t in theirs:
                    out.append((rest | {t}, theirs - {t}, None))
                elif ep is not None and ep[2] == side and ep[0] == t:
                    out.append((rest | {t}, theirs - {ep[1]}, None))
        res = []
        for m, t, e in out:
            Wn, Bn = (m, t) if side == "W" else (t, m)
            res.append((frozenset(Wn), frozenset(Bn), e))
        return res

    @lru_cache(maxsize=None)
    def win(W, B, ep, h, side):
        """True iff `side`, to move in G + *h, wins."""
        other = "B" if side == "W" else "W"
        for Wn, Bn, e in gmoves(W, B, ep, side):
            r = resolve(Wn, Bn, e, side)
            if r == side:
                return True
            if r == other:
                continue
            if not win(Wn, Bn, e, h, other):
                return True
        for h2 in range(h):
            if scope == "global" and ep is not None:
                # the e.p. right lapses; with the aware test the pawn may now be passed
                r = resolve(W, B, None, side)
                if r == side:
                    return True
                if r == other:
                    continue
                if not win(W, B, None, h2, other):
                    return True
            else:
                if not win(W, B, ep, h2, other):
                    return True
        return False

    return win


def parse(text):
    w, b = text.split("/")
    sq = lambda t: ("abcdefghijklmnop".index(t[0]), int(t[1:]))
    return (frozenset(sq(t) for t in w.split(":")[1].split()),
            frozenset(sq(t) for t in b.split(":")[1].split()))


def outcome(win, W, B, h):
    lw = win(W, B, None, h, "W")
    rw = win(W, B, None, h, "B")
    return {(True, False): "L", (False, True): "R", (True, True): "N", (False, False): "P"}[(lw, rw)]


if __name__ == "__main__":
    pos = sys.argv[1] if len(sys.argv) > 1 else "W: a2 c2 / B: b7 d7"
    F = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    wrap = len(sys.argv) > 3 and sys.argv[3] == "wrap"
    W, B = parse(pos)
    print(f"{pos}  files={F} wrap={wrap}")
    print("rule      ep   passer scope  | G+0 G+* G+*2 G+*3")
    for rule in ("count", "mover", "opponent"):
        for ep_on, passer, scope in [(False, "plain", "local"), (True, "plain", "local"),
                                     (True, "plain", "global"), (True, "aware", "local"),
                                     (True, "aware", "global")]:
            win = make_solver(F, wrap, ep_on, passer, scope, rule)
            o = [outcome(win, W, B, h) for h in range(4)]
            print(f"{rule:9s} {'on ' if ep_on else 'off'}  {passer:6s} {scope:6s} |  {o[0]}   {o[1]}   {o[2]}    {o[3]}")
