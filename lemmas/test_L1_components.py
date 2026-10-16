"""Falsification tests for Lemma L1 (empty files, components, arcs and rings,
en passant) and the symmetry lemma L0.

Run (from the project root):
    PYTHONPATH=. .venv/bin/python lemmas/test_L1_components.py [--n N] [--seed S]

Every check prints a count; any failure prints the offending position and the
script exits with status 1. Under pytest, test_* functions run a small sample.

Checks
  L1.a  invariance: every move maps Occ(X') into Occ(X)        (all reachable X)
  L1.b  locality: a move by a pawn on file f changes only squares on files
        f-1, f, f+1; passedness of a side = OR over components
  L1.c  arc = strip: an arc component of a cylinder (or any component of a flat
        board) has the same S- and W-values as the same pawns relabelled onto a
        flat strip of its own width
  L1.d  pure decomposition, e.p. off: pure(X) == sum of pure(X_i)   (identity)
  L1.e  pure decomposition, e.p. on, condition (E) holds  => identity
  L1.f  e.p. on, (E) fails: count how often the identity breaks at a root
        without a live right (none found so far: open question 1.8), and
        check the explicit counterexample WITH a live right (Prop. 1.7)
  L0    symmetries: colour reversal gives -G; file reflection, and rotation on
        the cylinder, give G   (S and W, all three race rules)
"""
from __future__ import annotations

import argparse
import random
import sys

from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos

from lemmas.common import (RULES, S, W, colour_reverse, occupied_files, pure,
                           pure_sum, random_position, relabel, reachable, split_ep,
                           terminal)

FAIL = []


def fail(msg):
    FAIL.append(msg)
    print("FAIL:", msg)


def boards(rng, max_ranks=7):
    files = rng.choice([3, 4, 5, 6, 7, 8])
    ranks = rng.choice([r for r in (5, 6, 7, 8) if r <= max_ranks])
    return Board(files, ranks, rng.random() < 0.6, rng.random() < 0.6)


def nonterminal_position(rng, b, nw, nb, tries=300):
    for _ in range(tries):
        p = random_position(rng, b, nw, nb)
        if terminal(b, p) is None:
            return p
    return None


# --------------------------------------------------------------------------
def check_invariance_locality(b: Board, x: Pos) -> int:
    n = 0
    for y in reachable(b, x, stop_at_terminal=False):
        occ = occupied_files(y)
        lpos, rpos = split_ep(y)
        for side, src in (("W", lpos), ("B", rpos)):
            for c in pawns.moves(b, src, side):
                n += 1
                if not occupied_files(c) <= occ:
                    fail(f"L1.a {b} {y} -> {c}")
                changed = {s[0] for s in (y.white ^ c.white) | (y.black ^ c.black)}
                mover_file = [s for s in ((y.white - c.white) if side == "W" else (y.black - c.black))]
                f = mover_file[0][0]
                allowed = {f} | {g for g in (b.nb(f, -1), b.nb(f, 1)) if g is not None}
                if not changed <= allowed:
                    fail(f"L1.b locality {b} {y} -> {c}")
        comps = pawns.components(b, y)
        for side in "WB":
            if pawns.passed(b, y, side) != any(pawns.passed(b, cc, side) for cc in comps):
                fail(f"L1.b passers {b} {y}")
    return n


def arc_map(b: Board, comp: Pos):
    """File map sending a component's files onto 0..k, in order."""
    fs = occupied_files(comp)
    if b.wrap and len(fs) == b.files:
        return None  # ring component
    if b.wrap:
        start = next(f for f in fs if (f - 1) % b.files not in fs)
        order = [(start + i) % b.files for i in range(len(fs))]
    else:
        order = sorted(fs)
    # a component is a run of consecutive files
    assert all(order[i + 1] == (order[i] + 1) % b.files for i in range(len(order) - 1)), order
    return {f: i for i, f in enumerate(order)}


def check_arc_strip(b: Board, x: Pos, rule: str) -> int:
    n = 0
    for comp in pawns.components(b, x):
        fmap = arc_map(b, comp)
        if fmap is None:
            continue
        flat = Board(len(fmap), b.ranks, False, b.ep)
        c2 = relabel(comp, fmap)
        try:
            if S(b, comp, rule) is not S(flat, c2, rule):
                fail(f"L1.c S {b} {comp} vs {flat} {c2}")
            if W(b, comp, rule) is not W(flat, c2, rule):
                fail(f"L1.c W {b} {comp} vs {flat} {c2}")
        except pawns.RaceError:
            continue
        n += 1
    return n


def ep_condition(b: Board, x: Pos) -> bool:
    """(E): no reachable position with >= 2 components carries a usable live
    e.p. right."""
    if not b.ep:
        return True
    for y in reachable(b, x, stop_at_terminal=False):
        if y.ep is None or len(pawns.components(b, y)) < 2:
            continue
        side = y.ep[2]
        plain = Pos(y.white, y.black, None)
        if set(pawns.moves(b, y, side)) != set(pawns.moves(b, plain, side)):
            return False
    return True


def check_symmetry(b: Board, x: Pos, rule: str) -> int:
    n = 0
    xr = colour_reverse(b, x)
    if b.wrap:
        maps = [{f: (b.files - 1 - f) for f in range(b.files)},
                {f: (f + 1) % b.files for f in range(b.files)}]
    else:
        maps = [{f: (b.files - 1 - f) for f in range(b.files)}]
    try:
        for model in (S, W):
            g = model(b, x, rule)
            if model(b, xr, rule) is not cgt.neg(g):
                fail(f"L0 colour {model.__name__} {rule} {b} {x}")
            for m in maps:
                if model(b, relabel(x, m), rule) is not g:
                    fail(f"L0 geometry {model.__name__} {rule} {b} {x} {m}")
            n += 1
    except pawns.RaceError:
        pass
    return n


def multi_component_position(rng, b: Board):
    """Two or three pawn groups on runs of files separated by empty files.
    Half of the time group 1 is seeded with an e.p. motif (a pawn on its start
    rank next to an enemy pawn on the double-step rank)."""
    n = b.files
    cut = rng.sample(range(n), 2 if b.wrap else 1)  # files kept empty
    if not b.wrap:
        cut = cut + [-1, n]
    free = [f for f in range(n) if f not in cut]
    runs, cur = [], []
    order = free if not b.wrap else sorted(free, key=lambda f: (f - cut[0]) % n)
    for f in order:
        if cur and (cur[-1] + 1) % n != f:
            runs.append(cur)
            cur = []
        cur.append(f)
    if cur:
        runs.append(cur)
    runs = [r for r in runs if r]
    if len(runs) < 2:
        return None
    white, black = set(), set()
    for k, run in enumerate(runs[:3]):
        squares = [(f, r) for f in run for r in range(2, b.ranks)]
        if k == 0 and len(run) >= 2 and rng.random() < 0.5:
            f = run[0]
            if rng.random() < 0.5:
                white.add((f, 2))
                black.add((run[1], 4))
            else:
                black.add((f, b.ranks - 1))
                white.add((run[1], b.ranks - 3))
        else:
            pick = rng.sample(squares, min(len(squares), rng.randint(1, 2)))
            for s in pick:
                (white if rng.random() < 0.5 else black).add(s)
    white -= black
    x = Pos(frozenset(white), frozenset(black))
    if len(pawns.components(b, x)) < 2 or len(white | black) > 5:
        return None
    return x


# --------------------------------------------------------------------------
def run(n_samples: int, seed: int, verbose: bool = True):
    rng = random.Random(seed)
    counts = dict(moves=0, arcs=0, pure_off=0, pure_E=0, pure_notE=0, pure_notE_break=0, sym=0)
    smallest_ep_break = None
    for i in range(n_samples):
        b = boards(rng)
        nw, nb = rng.randint(1, 3), rng.randint(1, 3)
        x = nonterminal_position(rng, b, nw, nb)
        if x is None:
            continue
        rule = rng.choice(RULES)
        counts["moves"] += check_invariance_locality(b, x)
        counts["arcs"] += check_arc_strip(b, x, rule)
        counts["sym"] += check_symmetry(b, x, rule)
    # pure decomposition: a dedicated generator of multi-component positions
    for i in range(n_samples):
        b = Board(rng.choice([5, 6, 7]), rng.choice([5, 6]), rng.random() < 0.5, rng.random() < 0.7)
        x = multi_component_position(rng, b)
        if x is None:
            continue
        same = pure(b, x) is pure_sum(b, x)
        if not b.ep:
            counts["pure_off"] += 1
            if not same:
                fail(f"L1.d pure, ep off: {b} {x}")
        elif ep_condition(b, x):
            counts["pure_E"] += 1
            if not same:
                fail(f"L1.e pure, (E) holds: {b} {x}")
        else:
            counts["pure_notE"] += 1
            if not same:
                counts["pure_notE_break"] += 1
                size = (len(x.white | x.black), b.files * b.ranks)
                if smallest_ep_break is None or size < smallest_ep_break[0]:
                    smallest_ep_break = (size, b, x)
    if verbose:
        print("L1.a/b moves checked:", counts["moves"])
        print("L1.c arc/strip components checked:", counts["arcs"])
        print("L1.d pure sums, e.p. off:", counts["pure_off"])
        print("L1.e pure sums, e.p. on with (E):", counts["pure_E"])
        print("L1.f pure sums, e.p. on without (E):", counts["pure_notE"],
              "of which the sum identity breaks:", counts["pure_notE_break"])
        if smallest_ep_break:
            _, b, x = smallest_ep_break
            print("   smallest break found:", b, x)
            print("   pure(whole) =", cgt.show(pure(b, x)), "  sum of pure(components) =", cgt.show(pure_sum(b, x)))
        print("L0 symmetry checks:", counts["sym"])
    return counts, smallest_ep_break


def explicit_ep_example():
    """L1.f, the explicit counterexample: flat 6x6 board, e.p. on, White has
    just played a2-a4 next to the black pawn on b4, so Black may take
    b4xa3 e.p. on this move only. Components: {a,b} and {e,f}; files c, d
    empty. In the sum the right survives Black's moves on e/f (a stale right)."""
    b = Board(6, 6, False, True)
    x = Pos(frozenset({(0, 4), (5, 4)}), frozenset({(1, 4), (4, 5)}), ((0, 3), (0, 4), "B"))
    return b, x, pure(b, x), pure_sum(b, x)


def test_explicit_ep_counterexample():
    b, x, g1, g2 = explicit_ep_example()
    assert g1 is not g2 and cgt.outcome(g1) == "N" and cgt.outcome(g2) == "R"


def test_small():
    FAIL.clear()
    run(60, 1, verbose=False)
    assert not FAIL, FAIL


def test_paper_ring_and_candidate():
    # the 8x8 embedding: component on a-d is the 4-file strip
    b8 = Board(8, 8, False, True)
    x8 = Pos.parse("W: a2 c2 g4 / B: b7 d7 g5")
    comps = pawns.components(b8, x8)
    assert len(comps) == 2
    b4 = Board(4, 8, False, True)
    assert S(b8, comps[0]) is S(b4, Pos.parse("W: a2 c2 / B: b7 d7"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=600)
    ap.add_argument("--seed", type=int, default=20261015)
    a = ap.parse_args()
    run(a.n, a.seed)
    b, x, g1, g2 = explicit_ep_example()
    print("L1.f explicit e.p. counterexample:", b, x)
    print("   pure(whole) =", cgt.show(g1), f"(outcome {cgt.outcome(g1)})",
          "  sum of pure(components) =", cgt.show(g2), f"(outcome {cgt.outcome(g2)})")
    if g1 is g2:
        fail("L1.f explicit counterexample no longer breaks the identity")
    print("FAILURES:", len(FAIL))
    sys.exit(1 if FAIL else 0)
