"""Falsification tests for Lemma L3 (the trebuchet freeze).

Run (from the project root):
    PYTHONPATH=. .venv/bin/python lemmas/test_L3_trebuchet.py [--n N] [--seed S] [--deep]

Part A (convention, CGT):
  A1  outcome lemma: o(WF(Y)) == o(W(Y)) for every sampled non-terminal Y
  A2  value lemma: WF(Y) == W(Y) whenever every non-terminal Y' reachable from
      Y is BIG-interior (-BIG <| W(Y') <| BIG); every value difference found
      must come with a violation of that condition
  A3  robustness: replacing the "king move = -BIG" option by any game K with
      a Right option -BIG (resp. Left option +BIG for Black's king move)
      gives the same value whenever -BIG < W(Y) < BIG (tested on random Y with
      K = {W(Y) | -BIG}, i.e. a king that can step back)
  A4  the *2 candidate W a2 c2 / B b7 d7 (4-file flat strip and the 8x8
      board with the g4/g5 pair): S, W, WF for the three race rules, e.p. on
      and off; BIG-interior condition over its whole tree
Part B (real chess geometry, lemmas/minichess.py):
  B1  for EVERY non-terminal configuration of the a-d component reachable from
      W a2 c2 / B b7 d7 (e.p. rights included) and each side to move, in the
      8x8 position with WK f5, BK h4, W g4, B g5:
        no king is in check; the side to move has at least one king move;
        no king move captures a pawn; after every king move the enemy king
        can capture the g-pawn at once, after which the capturer has a passed
        pawn and the other side has none; the chess pawn moves on a-d are
        exactly the model's moves.
  B2  the bare flat trebuchet (WK f5 Pg4 / BK h4 Pg5) is a real mutual
      zugzwang: the side NOT to move forces a KQK leaf (forced-win search)
  B3  the paper's cylinder trebuchet (WK h5 Pa4 / BK b4 Pa5, 8x8 cylinder):
      legal king moves of each side, which of them leave the a-pawn en prise,
      and the squares each king attacks across the a/h seam
  B4  (heuristic indicator) race nodes of the candidate's tree in which a
      frozen king stands inside the "square" of an enemy passer
"""
from __future__ import annotations

import argparse
import random
import sys

from cylcgt import cgt, pawns
from cylcgt.pawns import BIG, Board, Pos

from lemmas import minichess as mc
from lemmas.common import (NBIG, PBIG, RULES, S, W, WF, alt_outcome, random_position,
                           reachable, split_ep, terminal)

FAIL = []


def fail(msg):
    FAIL.append(msg)
    print("FAIL:", msg)


def big_interior(g) -> bool:
    """-BIG <| g <| BIG, i.e. not g <= -BIG and not g >= BIG."""
    return not cgt.le(g, NBIG) and not cgt.le(PBIG, g)


def hereditary_interior(b, y, rule) -> bool:
    for z in reachable(b, y):
        if terminal(b, z) is None and not big_interior(W(b, z, rule)):
            return False
    return True


# ---------------------------------------------------------------------------
def part_a(n_samples, seed):
    rng = random.Random(seed)
    stats = dict(samples=0, equal=0, differ=0, differ_with_violation=0, interior_hered=0,
                 robust_tested=0)
    for _ in range(n_samples):
        b = Board(rng.choice([3, 4, 5]), rng.choice([5, 6, 7, 8]), rng.random() < 0.3, rng.random() < 0.5)
        y = None
        for _ in range(200):
            p = random_position(rng, b, rng.randint(1, 3), rng.randint(1, 3))
            if terminal(b, p) is None:
                y = p
                break
        if y is None:
            continue
        rule = rng.choice(RULES)
        try:
            w, wf = W(b, y, rule), WF(b, y, rule)
        except pawns.RaceError:
            continue
        stats["samples"] += 1
        if cgt.outcome(w) != cgt.outcome(wf):
            fail(f"A1 outcome {b} {y} {rule}: W {cgt.outcome(w)} WF {cgt.outcome(wf)}")
        alt_w = alt_outcome(b, y, rule, kings=False)
        alt_k = alt_outcome(b, y, rule, kings=True)
        if alt_w != cgt.outcome(w) or alt_k != cgt.outcome(wf):
            fail(f"A1 minimax check {b} {y} {rule}")
        hi = hereditary_interior(b, y, rule)
        stats["interior_hered"] += hi
        if w is wf:
            stats["equal"] += 1
        else:
            stats["differ"] += 1
            if hi:
                fail(f"A2 value differs although BIG-interior: {b} {y} {rule}: "
                     f"W={cgt.show(w)} WF={cgt.show(wf)}")
            else:
                stats["differ_with_violation"] += 1
        # A3 robustness at the root
        if big_interior(w) and cgt.le(NBIG, w) and cgt.le(w, PBIG):
            lpos, rpos = split_ep(y)
            L = [_child(b, c, "W", rule) for c in pawns.moves(b, lpos, "W")]
            R = [_child(b, c, "B", rule) for c in pawns.moves(b, rpos, "B")]
            KL = cgt.make([w], [NBIG])     # White's king steps away and may step back
            KR = cgt.make([PBIG], [w])
            g = cgt.make(L + [KL], R + [KR])
            stats["robust_tested"] += 1
            if g is not w:
                fail(f"A3 robustness {b} {y} {rule}: {cgt.show(g)} vs {cgt.show(w)}")
    return stats


def _child(b, c, mover, rule):
    from lemmas.common import _W_child
    return _W_child(b, c, mover, rule, False)


CANDIDATE = "W: a2 c2 / B: b7 d7"


def part_a4():
    rows = []
    x4 = Pos.parse(CANDIDATE)
    x8 = Pos.parse("W: a2 c2 g4 / B: b7 d7 g5")
    for ep in (True, False):
        b4, b8 = Board(4, 8, False, ep), Board(8, 8, False, ep)
        for rule in RULES:
            vals = [S(b4, x4, rule), W(b4, x4, rule), WF(b4, x4, rule),
                    S(b8, x8, rule), W(b8, x8, rule), WF(b8, x8, rule)]
            hi = hereditary_interior(b4, x4, rule)
            rows.append((ep, rule, [cgt.show(v) for v in vals], hi))
            expect = cgt.nimber(2) if rule in ("count", "mover") else cgt.ZERO
            if any(v is not expect for v in vals):
                fail(f"A4 candidate ep={ep} {rule}: {[cgt.show(v) for v in vals]}")
    return rows


def part_a4_crosscheck():
    """Outcome of the candidate in Codex's independent minimax (count rule only)."""
    from crosscheck import minimax as mm
    x4 = Pos.parse(CANDIDATE)
    out = []
    for ep in (True, False):
        for files in (4, 8):
            o = mm.outcome_class(mm.Board(files, 8, False, ep), mm.Position(x4.white, x4.black, None))
            out.append((files, ep, o))
            if o != "N":
                fail(f"A4 crosscheck outcome {o} on {files} files, ep={ep}")
    return out


# ---------------------------------------------------------------------------
KINGS = "W: Kf5 Pg4 / B: Kh4 Pg5"


def chess_pos(y: Pos, stm: str, geo=mc.FLAT) -> mc.Pos:
    pieces = set()
    for s in y.white:
        pieces.add((s, "W", "P"))
    for s in y.black:
        pieces.add((s, "B", "P"))
    base = mc.make_pos(KINGS, stm, geo)
    pieces |= set(base.pieces)
    ep = y.ep[0] if (y.ep and y.ep[2] == stm) else None
    return mc.Pos(geo, frozenset(pieces), stm, ep)


def pawn_sets(p: mc.Pos):
    w = frozenset(s for s, c, k in p.pieces if c == "W" and k == "P")
    b = frozenset(s for s, c, k in p.pieces if c == "B" and k == "P")
    return w, b


def part_b1(ep=True):
    b4 = Board(4, 8, False, ep)
    b8 = Board(8, 8, False, ep)
    start = Pos.parse(CANDIDATE)
    gpair_w, gpair_b = {(6, 4)}, {(6, 5)}
    n_conf = n_checked = 0
    king_targets = {"W": set(), "B": set()}
    terminals = 0
    for y in reachable(b4, start):
        if terminal(b4, y) is not None:
            terminals += 1
            continue
        n_conf += 1
        for stm in "WB":
            opp = "B" if stm == "W" else "W"
            p = chess_pos(y, stm)
            if mc.in_check(p, "W") or mc.in_check(p, "B"):
                fail(f"B1 check in {y} {stm}")
            moves = mc.legal_moves(p)
            kmoves = [(d, ch) for d, ch in moves if d.startswith("K")]
            pmoves = [(d, ch) for d, ch in moves if not d.startswith("K")]
            if not kmoves:
                fail(f"B1 no king move in {y} {stm}")
            # pawn moves on a-d == model moves
            lpos, rpos = split_ep(y)
            model = {(c.white, c.black) for c in pawns.moves(b4, lpos if stm == "W" else rpos, stm)}
            chess = set()
            for d, ch in pmoves:
                w, bl = pawn_sets(ch)
                chess.add((w - gpair_w, bl - gpair_b))
            if model != chess:
                fail(f"B1 pawn moves differ in {y} {stm}: model {len(model)} chess {len(chess)}")
            gsq = (6, 4) if stm == "W" else (6, 5)
            for d, ch in kmoves:
                n_checked += 1
                king_targets[stm].add(d[-2:])
                if "x" in d:
                    fail(f"B1 king captures in {y} {stm}: {d}")
                caps = [(d2, ch2) for d2, ch2 in mc.legal_moves(ch)
                        if d2.startswith("K") and d2.endswith("x" + mc.sqname(gsq))]
                if not caps:
                    fail(f"B1 after {d} the g-pawn is not capturable in {y}")
                    continue
                w, bl = pawn_sets(caps[0][1])
                after = Pos(w, bl)
                if not pawns.passed(b8, after, opp) or pawns.passed(b8, after, stm):
                    fail(f"B1 after {d} and the capture, passers wrong in {y}")
    return n_conf, n_checked, terminals, {k: sorted(v) for k, v in king_targets.items()}


def part_b2(max_depth=17):
    out = []
    for stm in "WB":
        p = mc.make_pos(KINGS, stm)
        who = "B" if stm == "W" else "W"
        d = mc.min_forced_win(p, who, max_depth)
        if d is None:
            fail(f"B2 no forced win for {who} within {max_depth} plies")
        line = mc.principal_line(p, who, d) if d is not None else []
        out.append((stm, who, d, " ".join(line)))
    return out


def part_b3():
    rep = []
    for stm in "WB":
        p = mc.make_pos("W: Kh5 Pa4 / B: Kb4 Pa5", stm, mc.CYL)
        bd = p.board()
        if mc.in_check(p, "W") or mc.in_check(p, "B"):
            fail("B3 a king is in check in the cylinder trebuchet")
        ks = mc.king_sq(bd, stm)
        seen = sorted(mc.sqname(s) for s in mc.attacks_from(p.geo, bd, ks, stm, "K"))
        kmoves = [(d, ch) for d, ch in mc.legal_moves(p) if d.startswith("K")]
        mine = (0, 4) if stm == "W" else (0, 5)
        drops = []
        for d, ch in kmoves:
            caps = [d2 for d2, _ in mc.legal_moves(ch) if d2.startswith("K") and d2.endswith("x" + mc.sqname(mine))]
            drops.append((d, bool(caps)))
            if not caps:
                fail(f"B3 {stm} king move {d} keeps the a-pawn")
        pm = [d for d, _ in mc.legal_moves(p) if not d.startswith("K")]
        rep.append((stm, mc.sqname(ks), seen, drops, pm))
    return rep


def part_b3_flat_copy():
    """The same diagram read on a FLAT board: is it still a trebuchet?"""
    rep = []
    for stm in "WB":
        p = mc.make_pos("W: Kh5 Pa4 / B: Kb4 Pa5", stm, mc.FLAT)
        kmoves = [d for d, _ in mc.legal_moves(p) if d.startswith("K")]
        rep.append((stm, kmoves))
    return rep


def square_inside(king, pawn_sq, side, ranks, king_to_move):
    """Heuristic square rule on a flat board."""
    f, r = pawn_sq
    d = (ranks - r - (1 if r == 2 else 0)) if side == "W" else (r - 1 - (1 if r == ranks - 1 else 0))
    promo = (f, ranks) if side == "W" else (f, 1)
    dist = max(abs(king[0] - promo[0]), abs(king[1] - promo[1]))
    return dist <= (d if king_to_move else d - 1)


def part_b4(ep=True):
    """Race nodes of the candidate's tree: count those where a frozen king is
    inside the square of the leading enemy passer (heuristic indicator only)."""
    b4 = Board(4, 8, False, ep)
    start = Pos.parse(CANDIDATE)
    races = set()
    for y in reachable(b4, start, stop_at_terminal=True):
        lpos, rpos = split_ep(y)
        if terminal(b4, y) is not None:
            continue
        for side, src in (("W", lpos), ("B", rpos)):
            for c in pawns.moves(b4, src, side):
                if terminal(b4, c) == 0:
                    races.add((c, side))
    sensitive = 0
    for c, mover in races:
        to_move = "B" if mover == "W" else "W"
        hit = False
        for side, king in (("W", (7, 4)), ("B", (5, 5))):  # BK h4 = (7,4) vs W passers; WK f5 = (5,5) vs B passers
            # side = owner of the passer; king = the enemy king square (0-based file)
            pawns_side = c.white if side == "W" else c.black
            for s in pawns_side:
                one = Pos(frozenset([s]), c.black) if side == "W" else Pos(c.white, frozenset([s]))
                if pawns.passed(b4, one, side):
                    king_to_move = (to_move != side)
                    if square_inside(king, s, side, 8, king_to_move):
                        hit = True
        sensitive += hit
    return len(races), sensitive


def part_b4_terminals(ep=True):
    """Children with exactly one passer (convention: +-BIG at once): count those
    where the frozen enemy king is inside the passer's square (heuristic)."""
    b4 = Board(4, 8, False, ep)
    start = Pos.parse(CANDIDATE)
    term = set()
    for y in reachable(b4, start):
        if terminal(b4, y) is not None:
            continue
        lpos, rpos = split_ep(y)
        for side, src in (("W", lpos), ("B", rpos)):
            for c in pawns.moves(b4, src, side):
                t = terminal(b4, c)
                if t in (1, -1):
                    term.add((c, side, t))
    sensitive = 0
    for c, mover, t in term:
        owner = "W" if t == 1 else "B"
        king = (7, 4) if owner == "W" else (5, 5)
        to_move = "B" if mover == "W" else "W"
        hit = False
        for s in (c.white if owner == "W" else c.black):
            one = Pos(frozenset([s]), c.black) if owner == "W" else Pos(c.white, frozenset([s]))
            if pawns.passed(b4, one, owner) and square_inside(king, s, owner, 8, to_move != owner):
                hit = True
        sensitive += hit
    return len(term), sensitive


# ---------------------------------------------------------------------------
def test_part_a_small():
    FAIL.clear()
    part_a(40, 3)
    part_a4()
    assert not FAIL, FAIL


def test_geometry():
    FAIL.clear()
    part_b1(True)
    part_b3()
    assert not FAIL, FAIL


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--seed", type=int, default=20261015)
    ap.add_argument("--deep", action="store_true", help="also run the forced-win search B2")
    a = ap.parse_args()
    st = part_a(a.n, a.seed)
    print("A1-A3:", st)
    for ep, rule, vals, hi in part_a4():
        print(f"A4 ep={ep!s:5s} {rule:8s} S4,W4,WF4,S8,W8,WF8 = {vals}  hereditarily BIG-interior: {hi}")
    print("A4 crosscheck/minimax.py outcome (files, e.p., class):", part_a4_crosscheck())
    for ep in (True, False):
        n_conf, n_checked, terms, kt = part_b1(ep)
        print(f"B1 ep={ep}: {n_conf} non-terminal configurations x 2 sides, {n_checked} king moves checked, "
              f"{terms} terminal configurations; king destinations {kt}")
    if a.deep:
        for row in part_b2():
            print("B2 bare trebuchet, %s to move: %s forces a KQK leaf in %s plies: %s" % row)
    for row in part_b3():
        print("B3 cylinder trebuchet, %s to move: K on %s attacks %s; king moves (move, pawn then en prise) %s; pawn moves %s" % row)
    print("B3 same diagram on a flat board, king moves:", part_b3_flat_copy())
    for ep in (True, False):
        print("B4 ep=%s: race nodes (child, mover) = %d, of which a frozen king is inside an enemy passer's square: %d" % ((ep,) + part_b4(ep)))
        print("B4 ep=%s: single-passer children (child, mover) = %d, of which the frozen enemy king is inside the square: %d" % ((ep,) + part_b4_terminals(ep)))
    print("FAILURES:", len(FAIL))
    sys.exit(1 if FAIL else 0)
