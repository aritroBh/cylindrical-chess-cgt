"""V1 verifier side-check (outside claim V1): the KEY-FACT *2 candidate
W a2 c2 / B b7 d7 (files a-d, flat) under an e.p.-aware passed-pawn test.

pawns.passed() / crosscheck._has_passed() ignore e.p. rights, so a pawn that has just
double-stepped past an enemy pawn counts as 'passed' (game over) although the enemy
can capture it en passant on the very next move.  Here both implementations are
monkeypatched at runtime (no project file is edited) so that, while a usable e.p. right
exists, the double-stepped pawn is not counted as a passer.

Distinguishing sum: G + up, where up = W g2 / B g5 on an isolated file (f empty).
  *2 + up > 0 (outcome L);   {2±1 | -2±1} + up is hot (outcome N).

Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
     PYTHONPATH=. .venv/bin/python verify/diagrams/V1-reproduce/key2_ep_check.py
"""
import sys

from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from crosscheck import minimax as mm

sys.setrecursionlimit(1000000)
ORIG_P = pawns.passed
ORIG_M = mm._has_passed


def usable_ep(nb, pos):
    if not pos.ep:
        return False
    _, (f, r), side = pos.ep
    capt = pos.black if side == "B" else pos.white
    return any(nb(f, d) is not None and (nb(f, d), r) in capt for d in (-1, 1))


def p_aware(board, pos, side):
    if pos.ep and pos.ep[2] != side and usable_ep(board.nb, pos):
        v = pos.ep[1]
        if side == "W":
            return ORIG_P(board, Pos(pos.white - {v}, pos.black, None), side)
        return ORIG_P(board, Pos(pos.white, pos.black - {v}, None), side)
    return ORIG_P(board, pos, side)


def m_aware(board, pos, side):
    if board.ep and pos.ep and pos.ep[2] != side and usable_ep(board.neighbor, pos):
        v = pos.ep[1]
        if side == "W":
            return ORIG_M(board, mm.Position(pos.white - {v}, pos.black, None), side)
        return ORIG_M(board, mm.Position(pos.white, pos.black - {v}, None), side)
    return ORIG_M(board, pos, side)


G = "W: a2 c2 / B: b7 d7"
GX = "W: a2 c2 g2 / B: b7 d7 g5"
for ep in (True, False):
    b4 = Board(4, 8, False, ep)
    b7 = Board(7, 8, False, ep)
    mb7 = mm.Board(7, 8, False, ep)
    for tag, pp, mp in (("standard", ORIG_P, ORIG_M), ("ep-aware", p_aware, m_aware)):
        pawns.passed, mm._has_passed = pp, mp
        res = []
        for rule in ("count", "mover", "opponent"):
            pawns.RACE_RULE = rule
            pawns._value.cache_clear()
            g = pawns.value(b4, Pos.parse(G))
            gx = pawns.value(b7, Pos.parse(GX))
            res.append(f"{rule}: G={cgt.show(g)} G+up={cgt.show(gx)[:30]} outcome(G+up)={cgt.outcome(gx)}")
        mm._winner.cache_clear()
        mres = mm.outcome_class(mb7, mm.parse_position(GX))
        mg = mm.outcome_class(mm.Board(4, 8, False, ep), mm.parse_position(G))
        print(f"ep={'on ' if ep else 'off'} {tag:9s} | " + " | ".join(res))
        print(f"           crosscheck minimax (count rule): outcome(G)={mg} outcome(G+up)={mres}")
        pawns.passed, mm._has_passed = ORIG_P, ORIG_M
        pawns.RACE_RULE = "count"
        pawns._value.cache_clear()
