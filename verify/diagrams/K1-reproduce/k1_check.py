"""K1 adversarial re-check: the 7.2 king group (W Ke6, Pd7 / B Kd8, Pe7).

Independent of verify/diagrams/rerun.py: a fresh king+pawn legal-move generator
for an 8x8 board, cylinder (files mod 8) or flat, with
  - single and double pawn steps, diagonal captures (wrapping on the cylinder),
    promotion on the last rank (as a flag), en passant ignored (no double step
    has just been played in any position examined here),
  - full legality: a move is legal iff the mover's king is not attacked afterwards.
It is run on the FULL 7.2 diagram (all pawns present), not only the isolated
group, and on the isolated 4-man group. For each legal king move in the d/e group
it lists the opponent's legal captures of a group pawn; for Black's Kc7 it plays
Kxe7 and checks that Black cannot stop or win the d-pawn (d8=Q next is legal and
the promoted piece is not capturable).

Cross-check (flat board only): realchess.movegen.legal_uci (a third, separate
legal-move generator), on the full position and the isolated group.

Run from the project root:
  PYTHONPATH=. .venv/bin/python verify/diagrams/K1-reproduce/k1_check.py
"""
from __future__ import annotations

FILES = "abcdefgh"


def parse(fen_board):
    pcs = {}
    for i, row in enumerate(fen_board.split("/")):
        r = 8 - i
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                pcs[(f, r)] = ch
                f += 1
        assert f == 8
    return pcs


def name(s):
    return FILES[s[0]] + str(s[1])


def sqn(n):
    return (FILES.index(n[0]), int(n[1]))


def norm(f, r, wrap):
    if not 1 <= r <= 8:
        return None
    if wrap:
        return (f % 8, r)
    return (f, r) if 0 <= f <= 7 else None


def white(c):
    return c.isupper()


def attacked_by(pcs, sq, side, wrap):
    """Is square sq attacked by `side` ('w' or 'b')?"""
    for s, c in pcs.items():
        if (side == "w") != white(c):
            continue
        f, r = s
        if c in "Kk":
            for df in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    if (df or dr) and norm(f + df, r + dr, wrap) == sq:
                        return True
        elif c == "P":
            if sq in (norm(f - 1, r + 1, wrap), norm(f + 1, r + 1, wrap)):
                return True
        elif c == "p":
            if sq in (norm(f - 1, r - 1, wrap), norm(f + 1, r - 1, wrap)):
                return True
    return False


def legal(pcs, side, wrap):
    """List of (from, to, captured, newpcs)."""
    out = []
    for s, c in list(pcs.items()):
        if (side == "w") != white(c):
            continue
        f, r = s
        targets = []
        if c in "Kk":
            for df in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    t = norm(f + df, r + dr, wrap)
                    if (df or dr) and t and (t not in pcs or white(pcs[t]) != white(c)):
                        targets.append(t)
        else:
            d = 1 if c == "P" else -1
            one = norm(f, r + d, wrap)
            if one and one not in pcs:
                targets.append(one)
                start = 2 if c == "P" else 7
                two = norm(f, r + 2 * d, wrap)
                if r == start and two and two not in pcs:
                    targets.append(two)
            for df in (-1, 1):
                t = norm(f + df, r + d, wrap)
                if t and t in pcs and white(pcs[t]) != white(c):
                    targets.append(t)
        for t in targets:
            new = dict(pcs)
            del new[s]
            cap = new.pop(t, None)
            new[t] = c
            k = next(q for q, x in new.items() if x == ("K" if side == "w" else "k"))
            if attacked_by(new, k, "b" if side == "w" else "w", wrap):
                continue
            out.append((s, t, cap, new))
    return out


def mv(m):
    s, t, cap, new = m
    return f"{new[t].upper() if new[t] in 'Kk' else ''}{name(s)}{'x' if cap else '-'}{name(t)}"


def analyse(label, board, wrap, group_files="de"):
    pcs = parse(board)
    print(f"\n### {label} ({'cylinder' if wrap else 'flat'})  {board}")
    for side in ("w", "b"):
        ms = legal(pcs, side, wrap)
        grp = [m for m in ms if m[0][0] in [FILES.index(x) for x in group_files]
               or pcs[m[0]] in "Kk"]
        print(f"  {side} legal moves ({len(ms)}): {', '.join(mv(m) for m in ms)}")
        print(f"  {side} moves touching the d/e king group: {', '.join(mv(m) for m in grp)}")
        opp = "b" if side == "w" else "w"
        for m in grp:
            new = m[3]
            caps = [mv(r) for r in legal(new, opp, wrap)
                    if r[2] and r[1][0] in [FILES.index(x) for x in group_files]]
            print(f"     after {mv(m)}: opponent's legal captures in group: {caps or 'NONE'}")


def kc7_followup(board, wrap):
    pcs = parse(board)
    after_kc7 = next(m[3] for m in legal(pcs, "b", wrap) if m[1] == sqn("c7"))
    kxe7 = [m for m in legal(after_kc7, "w", wrap) if m[1] == sqn("e7")]
    print(f"\n  Kc7 follow-up ({'cyl' if wrap else 'flat'}): White Kxe7 legal? {bool(kxe7)}")
    pos = kxe7[0][3]
    replies = legal(pos, "b", wrap)
    bad = []
    for r in replies:
        nxt = r[3]
        if sqn("d7") not in nxt or nxt[sqn("d7")] != "P":
            bad.append(mv(r) + " (takes d7)")
            continue
        prom = [m for m in legal(nxt, "w", wrap) if m[0] == sqn("d7") and m[1] == sqn("d8")]
        if not prom:
            bad.append(mv(r) + " (d8 promotion not legal)")
            continue
        q = prom[0][3]
        if any(x[1] == sqn("d8") for x in legal(q, "b", wrap)):
            bad.append(mv(r) + " (promoted piece capturable)")
    group_replies = [mv(r) for r in replies if pos[r[0]] == "k"]
    print(f"  Black king replies after Kc7 Kxe7: {group_replies}")
    print(f"  replies that stop d8=Q or win the new queen: {bad or 'NONE'}")


def flat_crosscheck(board):
    from realchess import movegen
    out = {}
    for stm in "wb":
        out[stm] = sorted(movegen.legal_uci(f"{board} {stm} - - 0 1"))
    return out


if __name__ == "__main__":
    FULL = "3k4/1p1Pp2p/p3K3/8/8/7P/PP6/8"   # 7.2 as drawn (ChessPuzzle2.png)
    GROUP = "3k4/3Pp3/4K3/8/8/8/8/8"           # isolated king group
    for wrap in (True, False):
        analyse("7.2 full diagram", FULL, wrap)
        analyse("7.2 isolated king group", GROUP, wrap)
        kc7_followup(FULL, wrap)
        kc7_followup(GROUP, wrap)

    print("\n### flat-board cross-check with realchess.movegen.legal_uci")
    for b in (FULL, GROUP):
        cc = flat_crosscheck(b)
        mine = {stm: sorted(
            f"{name(m[0])}{name(m[1])}" + ("q" if parse(b)[m[0]] in "Pp" and m[1][1] in (1, 8) else "")
            for m in legal(parse(b), stm, False)) for stm in "wb"}
        for stm in "wb":
            print(f"  {b} {stm}: movegen={cc[stm]}")
            # movegen lists 4 promotion pieces; compare on the from-to squares only
            same = sorted({u[:4] for u in cc[stm]}) == sorted({u[:4] for u in mine[stm]})
            print(f"      matches my generator (from-to): {same}")
