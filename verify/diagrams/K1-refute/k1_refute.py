"""K1 refute-lens check, written from scratch (imports nothing from cylcgt/, crosscheck/,
realchess/ or verify/diagrams/*.py).

Claim K1: in Position 7.2 the king group W Ke6, Pd7 / B Kd8, Pe7 is a mutual zugzwang under the
paper's convention (losing the group's pawn = losing).  White's legal king moves are Kd5, Ke5, Kf5,
Kf7, each allowing ...Kxd7; Black's only legal king move is Kc7, allowing Kxe7 and then d8=Q.
Neither pawn can move.

This script uses a full orthodox legal-move generator (K, Q, R, B, N, P; checks; pins; captures;
double steps; en passant; under-promotion) on an 8x8 board, optionally with the a- and h-files
glued (cylinder: every file step is taken mod 8; sliders stop after 7 steps so a rook cannot travel
round the rank back to its own square).

Run:  cd /Users/aritro/Downloads/Research/Chessendgames && python3 verify/diagrams/K1-refute/k1_refute.py
"""
import itertools

N = 8
KDIRS = [(df, dr) for df in (-1, 0, 1) for dr in (-1, 0, 1) if (df, dr) != (0, 0)]
NDIRS = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
RDIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
BDIRS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]


def sqn(s):
    return "abcdefgh"[s[0]] + str(s[1] + 1)


def sq(t):
    return ("abcdefgh".index(t[0]), int(t[1]) - 1)


def parse(board):
    pcs = {}
    for i, row in enumerate(board.split("/")):
        r, f = 7 - i, 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                pcs[(f, r)] = ch
                f += 1
    return pcs


def to_fen(pcs):
    rows = []
    for r in range(7, -1, -1):
        row, e = "", 0
        for f in range(8):
            c = pcs.get((f, r))
            if c:
                row += (str(e) if e else "") + c
                e = 0
            else:
                e += 1
        rows.append(row + (str(e) if e else ""))
    return "/".join(rows)


def step(s, df, dr, wrap):
    f, r = s[0] + df, s[1] + dr
    if not 0 <= r < N:
        return None
    if wrap:
        f %= N
    elif not 0 <= f < N:
        return None
    return (f, r)


def white(c):
    return c.isupper()


def side_of(c):
    return "W" if c.isupper() else "B"


def attacks_from(pcs, s, wrap):
    """Squares attacked by the piece on s (pawn: diagonal captures only)."""
    c = pcs[s]
    p = c.upper()
    out = set()
    if p == "K":
        for d in KDIRS:
            t = step(s, *d, wrap)
            if t:
                out.add(t)
    elif p == "N":
        for d in NDIRS:
            t = step(s, *d, wrap)
            if t:
                out.add(t)
    elif p == "P":
        dr = 1 if white(c) else -1
        for df in (-1, 1):
            t = step(s, df, dr, wrap)
            if t:
                out.add(t)
    else:
        dirs = (RDIRS if p == "R" else BDIRS if p == "B" else RDIRS + BDIRS)
        for d in dirs:
            t = s
            for _ in range(N - 1):
                t = step(t, *d, wrap)
                if t is None or t == s:
                    break
                out.add(t)
                if t in pcs:
                    break
    return out


def attacked_by(pcs, side, wrap):
    a = set()
    for s, c in pcs.items():
        if side_of(c) == side:
            a |= attacks_from(pcs, s, wrap)
    return a


def king_sq(pcs, side):
    k = "K" if side == "W" else "k"
    return next(s for s, c in pcs.items() if c == k)


def in_check(pcs, side, wrap):
    return king_sq(pcs, side) in attacked_by(pcs, "B" if side == "W" else "W", wrap)


def pseudo(pcs, side, wrap, ep):
    """Yield (from, to, promo, newpcs, new_ep)."""
    for s, c in list(pcs.items()):
        if side_of(c) != side:
            continue
        p = c.upper()
        if p == "P":
            dr = 1 if side == "W" else -1
            last = 7 if side == "W" else 0
            start = 1 if side == "W" else 6
            t = step(s, 0, dr, wrap)
            targets = []
            if t and t not in pcs:
                targets.append((t, None))
                t2 = step(t, 0, dr, wrap)
                if s[1] == start and t2 and t2 not in pcs:
                    targets.append((t2, t))  # double step; ep square = t
            for df in (-1, 1):
                t = step(s, df, dr, wrap)
                if t and t in pcs and side_of(pcs[t]) != side:
                    targets.append((t, None))
                elif t and ep is not None and t == ep:
                    targets.append((t, "EP"))
            for t, extra in targets:
                new = dict(pcs)
                del new[s]
                if extra == "EP":
                    del new[(t[0], s[1])]
                new_ep = extra if isinstance(extra, tuple) else None
                if t[1] == last:
                    for pr in "QRBN":
                        n2 = dict(new)
                        n2[t] = pr if side == "W" else pr.lower()
                        yield s, t, pr, n2, None
                else:
                    new[t] = c
                    yield s, t, None, new, new_ep
        else:
            for t in attacks_from(pcs, s, wrap):
                if t in pcs and side_of(pcs[t]) == side:
                    continue
                new = dict(pcs)
                del new[s]
                new[t] = c
                yield s, t, None, new, None


def legal(pcs, side, wrap, ep=None):
    return [m for m in pseudo(pcs, side, wrap, ep) if not in_check(m[3], side, wrap)]


def mv_str(pcs, m):
    s, t, pr, _, _ = m
    c = pcs[s]
    cap = "x" if t in pcs else "-"
    return f"{c.upper() if c.upper() != 'P' else ''}{sqn(s)}{cap}{sqn(t)}{('=' + pr) if pr else ''}"


def passed_pawnonly(pcs, s, wrap):
    """Pawn-only definition: no enemy pawn ahead on own or adjacent file (with wrap)."""
    c = pcs[s]
    w = white(c)
    enemy = "p" if w else "P"
    for df in (-1, 0, 1):
        f = (s[0] + df) % N if wrap else s[0] + df
        if not 0 <= f < N:
            continue
        for r in range(N):
            if pcs.get((f, r)) == enemy and ((r > s[1]) if w else (r < s[1])):
                return False
    return True


GROUP = {sq("e6"), sq("d8"), sq("d7"), sq("e7")}
FULL = "3k4/1p1Pp2p/p3K3/8/8/7P/PP6/8"        # Position 7.2 as drawn
ISOL = "3k4/3Pp3/4K3/8/8/8/8/8"               # king group alone


def report(board, wrap):
    pcs = parse(board)
    tag = "cylinder" if wrap else "flat"
    print(f"\n##### {board}  ({tag})")
    print(f"  W in check: {in_check(pcs, 'W', wrap)}   B in check: {in_check(pcs, 'B', wrap)}")
    print(f"  pawn-only 'passed' status at move 0: d7={passed_pawnonly(pcs, sq('d7'), wrap)} "
          f"e7={passed_pawnonly(pcs, sq('e7'), wrap)}")
    verdict = {}
    for side in ("W", "B"):
        ms = legal(pcs, side, wrap)
        grp = [m for m in ms if m[0] in GROUP]
        other = [m for m in ms if m[0] not in GROUP]
        print(f"  {side} to move: {len(ms)} legal moves; in the group: {[mv_str(pcs, m) for m in grp]}; "
              f"elsewhere: {[mv_str(pcs, m) for m in other]}")
        opp = "B" if side == "W" else "W"
        my_pawn = sq("d7") if side == "W" else sq("e7")
        their_pawn = sq("e7") if side == "W" else sq("d7")
        all_lose = True
        for m in grp:
            after = m[3]
            caps = [r for r in legal(after, opp, wrap, m[4]) if r[1] == my_pawn]
            line = f"    {mv_str(pcs, m)}: opponent captures of {sqn(my_pawn)}: {[mv_str(after, r) for r in caps]}"
            good = False
            for r in caps:
                a2 = r[3]
                # the capturer's group pawn survives, is pawn-only passed, and cannot be taken next move
                alive = a2.get(their_pawn) == ("p" if side == "W" else "P")
                pp = alive and passed_pawnonly(a2, their_pawn, wrap)
                retake = [x for x in legal(a2, side, wrap) if x[1] == their_pawn]
                mover_passers = [sqn(s) for s, c in a2.items()
                                 if c == ("P" if side == "W" else "p") and passed_pawnonly(a2, s, wrap)]
                line += (f"\n        after {mv_str(after, r)}: {sqn(their_pawn)} alive={alive} passed={pp}; "
                         f"can mover retake it next move: {[mv_str(a2, x) for x in retake] or 'no'}; "
                         f"mover's passed pawns: {mover_passers or 'none'}")
                if alive and pp and not retake and not mover_passers:
                    good = True
            # Black's king move: show the promotion follow-up too
            if side == "B" and caps:
                r = caps[0]
                a2 = r[3]
                worst = []
                for b in legal(a2, "B", wrap, r[4]):
                    a3 = b[3]
                    promos = [x for x in legal(a3, "W", wrap, b[4])
                              if x[0] == sq("d7") and x[1] == sq("d8") and x[2] == "Q"]
                    safe = []
                    for x in promos:
                        a4 = x[3]
                        qcap = [y for y in legal(a4, "B", wrap, None) if y[1] == sq("d8")]
                        safe.append(not qcap)
                    if not (promos and all(safe)):
                        worst.append(mv_str(a2, b))
                line += (f"\n        after {mv_str(after, r)}: Black replies that stop d7-d8=Q with the queen safe: "
                         f"{worst or 'none'} (of {len(legal(a2, 'B', wrap, r[4]))} legal Black replies)")
            print(line)
            all_lose &= good
        pawn_moves = [mv_str(pcs, m) for m in grp if pcs[m[0]].upper() == "P"]
        print(f"    group pawn moves available: {pawn_moves or 'none'}")
        print(f"    => every group move by {side} lets the opponent win the pawn with a clean passer: {all_lose}")
        verdict[side] = all_lose and bool(grp) and not pawn_moves
    return verdict


if __name__ == "__main__":
    results = {}
    for board in (FULL, ISOL):
        for wrap in (True, False):
            results[(board, wrap)] = report(board, wrap)
    print("\nSUMMARY (True = every group move by that side drops its pawn to a clean enemy passer):")
    for (b, w), v in results.items():
        print(f"  {b:34s} {'cylinder' if w else 'flat    '}  W:{v['W']}  B:{v['B']}")
    print("\nFENs for real-chess probing (isolated group, flat):")
    print(f"  {ISOL} w - - 0 1")
    print(f"  {ISOL} b - - 0 1")
