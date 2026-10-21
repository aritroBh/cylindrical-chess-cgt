"""Independent check of claim K1 (7.2 king group W Ke6 Pd7 / B Kd8 Pe7).

Written from scratch for the K1 refute pass. Imports nothing from cylcgt/, crosscheck/,
realchess/ or verify/diagrams/*.py.

Model: kings + pawns only on an 8x8 board, flat (wrap=False) or cylinder (wrap=True, files a,h adjacent).
Legal moves = full chess legality for K+P (own king not attacked after the move; kings never adjacent),
pawn pushes, double steps from the 2nd rank, diagonal captures (wrapping on the cylinder), en passant,
and promotion.

"Paper convention" search (bounded AND-OR):
  * a move that promotes wins for the mover;
  * a move after which the opponent has no pawns while the mover still has one wins for the mover
    (the paper's "drops the pawn, the other side promotes");
  * a side with no legal move loses (normal play).
A position is a mutual zugzwang under the convention if the side to move loses, whichever side it is.

Usage: python k1_check.py
"""
import itertools
import sys

N = 8


def fd(a, b, wrap):
    d = abs(a - b)
    return min(d, N - d) if wrap else d


def sq(s):
    return ("abcdefgh".index(s[0]), int(s[1]) - 1)


def name(t):
    return "abcdefgh"[t[0]] + str(t[1] + 1)


def attacked_by(pcs, target, colour, wrap):
    """Is square `target` attacked by `colour` ('w'/'b')?"""
    tf, tr = target
    for (f, r), p in pcs.items():
        if colour == "w" and p == "K" or colour == "b" and p == "k":
            if (f, r) != target and fd(f, tf, wrap) <= 1 and abs(r - tr) <= 1:
                return True
        if colour == "w" and p == "P" and tr == r + 1 and fd(f, tf, wrap) == 1:
            return True
        if colour == "b" and p == "p" and tr == r - 1 and fd(f, tf, wrap) == 1:
            return True
    return False


def king_sq(pcs, colour):
    k = "K" if colour == "w" else "k"
    return next(s for s, p in pcs.items() if p == k)


def in_check(pcs, colour, wrap):
    return attacked_by(pcs, king_sq(pcs, colour), "b" if colour == "w" else "w", wrap)


def norm(f, wrap):
    if wrap:
        return f % N
    return f if 0 <= f < N else None


def pseudo_moves(pcs, colour, ep, wrap):
    """Yield (desc, newpcs, new_ep, promoted)."""
    own = "KP" if colour == "w" else "kp"
    dirn = 1 if colour == "w" else -1
    for (f, r), p in list(pcs.items()):
        if p not in own:
            continue
        if p.upper() == "K":
            for df, dr in itertools.product((-1, 0, 1), repeat=2):
                if df == dr == 0:
                    continue
                nf, nr = norm(f + df, wrap), r + dr
                if nf is None or not 0 <= nr < N:
                    continue
                tgt = pcs.get((nf, nr))
                if tgt is not None and tgt in own:
                    continue
                new = dict(pcs)
                del new[(f, r)]
                new[(nf, nr)] = p
                yield (("K" if colour == "w" else "k") + ("x" if tgt else "") + name((nf, nr)), new, None, False)
        else:
            last = 7 if colour == "w" else 0
            start = 1 if colour == "w" else 6
            nr = r + dirn
            if 0 <= nr < N and (f, nr) not in pcs:
                new = dict(pcs)
                del new[(f, r)]
                new[(f, nr)] = p
                yield (name((f, nr)) + ("=Q" if nr == last else ""), new, None, nr == last)
                nr2 = r + 2 * dirn
                if r == start and (f, nr2) not in pcs:
                    new2 = dict(pcs)
                    del new2[(f, r)]
                    new2[(f, nr2)] = p
                    yield (name((f, nr2)), new2, (f, nr), False)
            for df in (-1, 1):
                nf = norm(f + df, wrap)
                if nf is None or not 0 <= nr < N:
                    continue
                tgt = pcs.get((nf, nr))
                if tgt is not None and tgt not in own and tgt.upper() == "P":
                    new = dict(pcs)
                    del new[(f, r)]
                    new[(nf, nr)] = p
                    yield ("abcdefgh"[f] + "x" + name((nf, nr)) + ("=Q" if nr == last else ""), new, None, nr == last)
                elif tgt is not None and tgt not in own and tgt.upper() == "K":
                    continue
                elif tgt is None and ep == (nf, nr):
                    new = dict(pcs)
                    del new[(f, r)]
                    del new[(nf, r)]
                    new[(nf, nr)] = p
                    yield ("abcdefgh"[f] + "x" + name((nf, nr)) + " e.p.", new, None, False)


def legal_moves(pcs, colour, ep, wrap):
    return [m for m in pseudo_moves(pcs, colour, ep, wrap) if not in_check(m[1], colour, wrap)]


def pawns(pcs, colour):
    return sum(1 for p in pcs.values() if p == ("P" if colour == "w" else "p"))


def mover_wins_now(newpcs, colour, promoted):
    opp = "b" if colour == "w" else "w"
    return promoted or (pawns(newpcs, opp) == 0 and pawns(newpcs, colour) > 0)


def wins(pcs, colour, ep, wrap, d):
    if d <= 0:
        return False
    opp = "b" if colour == "w" else "w"
    for desc, new, nep, prom in legal_moves(pcs, colour, ep, wrap):
        if mover_wins_now(new, colour, prom):
            return True
        if loses(new, opp, nep, wrap, d - 1):
            return True
    return False


def loses(pcs, colour, ep, wrap, d):
    opp = "b" if colour == "w" else "w"
    ms = legal_moves(pcs, colour, ep, wrap)
    if not ms:
        return True
    if d <= 0:
        return False
    for desc, new, nep, prom in ms:
        if mover_wins_now(new, colour, prom):
            return False
        if not wins(new, opp, nep, wrap, d - 1):
            return False
    return True


def parse(spec):
    pcs = {}
    for tok in spec.split():
        pcs[sq(tok[1:])] = tok[0]
    return pcs


def report(label, pcs, wrap, depth=6):
    print(f"\n--- {label}  wrap={wrap} ---")
    print("  W in check:", in_check(pcs, "w", wrap), " B in check:", in_check(pcs, "b", wrap))
    for colour in ("w", "b"):
        opp = "b" if colour == "w" else "w"
        ms = legal_moves(pcs, colour, None, wrap)
        print(f"  {colour.upper()} to move: {len(ms)} legal moves")
        for desc, new, nep, prom in ms:
            replies = legal_moves(new, opp, nep, wrap)
            winning = [r[0] for r in replies if mover_wins_now(r[1], opp, r[3])]
            # two-ply wins for opponent (opponent move then forced win)
            deep = [r[0] for r in replies if not mover_wins_now(r[1], opp, r[3])
                    and loses(r[1], colour, r[2], wrap, depth - 2)]
            print(f"    {desc:8s} -> opponent immediate convention-wins: {winning or '-'}; "
                  f"opponent moves after which mover loses (depth {depth-2}): {deep or '-'}")
        print(f"  => {colour.upper()} to move LOSES under convention (depth {depth}):",
              loses(pcs, colour, None, wrap, depth))


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    group = parse("Ke6 Pd7 kd8 pe7")
    for wrap in (False, True):
        report("7.2 king group alone: W Ke6 Pd7 / B Kd8 Pe7", group, wrap)
    # Full 7.2 diagram (as read from prior_work/Pictures/ChessPuzzle2.png): list king moves only,
    # to show the other pawns do not add or remove king moves.
    full = parse("Ke6 Pd7 Pa2 Pb2 Ph3 kd8 pe7 pa6 pb7 ph7")
    for wrap in (False, True):
        print(f"\n--- full 7.2 diagram, king moves only, wrap={wrap} ---")
        for colour in ("w", "b"):
            ks = [m[0] for m in legal_moves(full, colour, None, wrap) if m[0][0] in "Kk"]
            gp = [m[0] for m in legal_moves(full, colour, None, wrap)
                  if m[0][0] not in "Kk" and m[0][0] in "de"]
            print(f"  {colour.upper()} king moves: {ks}; d/e-pawn moves: {gp or '-'}")
    # Control: the 7.3 king group should NOT be a mutual zugzwang (spare moves Kg8-f8, Kf6-g6).
    g73 = parse("Kg8 Pf7 kf6 pg7")
    for wrap in (False, True):
        report("control 7.3 king group: W Kg8 Pf7 / B Kf6 Pg7", g73, wrap, depth=4)
