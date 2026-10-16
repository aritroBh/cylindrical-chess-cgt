"""Self-tests for sumtest/sumsolver.py (no cylcgt, no crosscheck).

Run:  cd <root> && PYTHONPATH=. .venv/bin/python -m pytest -q sumtest/test_sumsolver.py
"""
import itertools
import random

import pytest

from sumtest.sumsolver import (REF_NAMES, Geometry, Rules, SumSolver, Trees, canonical_alternatives,
                               make, reference_set)

# Textbook outcome classes of the reference games themselves (G = 0).
TEXTBOOK = {"0": "P", "*": "N", "*2": "N", "*3": "N", "up": "L", "down": "R", "up*": "N",
            "dup*": "L", "1/2": "L", "-1/2": "R", "1": "L", "-1": "R", "{1|0}": "N",
            "+-1": "N", "tiny1": "L"}


def test_empty_board_gives_reference_outcomes():
    geo, rules, T, ref, s = make(4, False)
    out = s.outcomes(0, 0, [ref[n] for n in REF_NAMES])
    assert dict(zip(REF_NAMES, out)) == TEXTBOOK


def test_abstract_identities():
    T = Trees()
    ref = reference_set(T)
    extra = {
        "*2+*2": T.add(ref["*2"], ref["*2"]),          # = 0  -> P
        "*2+*": T.add(ref["*2"], ref["*"]),            # = *3 -> N
        "*2+*3": T.add(ref["*2"], ref["*3"]),          # = *  -> N
        "*+*3+*2": T.add(T.add(ref["*"], ref["*3"]), ref["*2"]),   # = 0 -> P
        "up+down": T.add(ref["up"], ref["down"]),      # = 0 -> P
        "half+half-1": T.add(T.add(ref["1/2"], ref["1/2"]), ref["-1"]),  # = 0 -> P
        "pm1+pm1": T.add(ref["+-1"], ref["+-1"]),      # = 0 -> P
        "tiny-down": T.add(ref["tiny1"], ref["down"]),  # tiny < up, so tiny + down < 0 -> R
    }
    alt = canonical_alternatives(T)
    extra["up*-alt"] = T.add(ref["up*"], T.neg(alt["up*"]))       # = 0 -> P
    extra["dup*-alt"] = T.add(ref["dup*"], T.neg(alt["dup*"]))    # = 0 -> P
    geo = Geometry(1, False)
    s = SumSolver(Rules(geo), T)
    wl, wr = s.solve((0, 0, -1))
    got = {k: s.outcome(wl, wr, v) for k, v in extra.items()}
    assert got == {"*2+*2": "P", "*2+*": "N", "*2+*3": "N", "*+*3+*2": "P", "up+down": "P",
                   "half+half-1": "P", "pm1+pm1": "P", "tiny-down": "R",
                   "up*-alt": "P", "dup*-alt": "P"}


def test_hand_checked_single_file_positions():
    # W a4 / B a6 on one file: either side plays to a5 and the file locks: {0|0} = *
    geo, rules, T, ref, s = make(1, False)
    W, B = geo.parse("W: a4 / B: a6")
    assert s.outcomes(W, B, [ref["*"]]) == ["P"]
    # W a2 / B a5: {0,*|*} = up (hand computation in REPORT.md)
    W, B = geo.parse("W: a2 / B: a5")
    assert s.outcomes(W, B, [ref["down"]]) == ["P"]
    assert s.outcomes(W, B, [ref["0"]]) == ["L"]


def test_hand_checked_switch_big():
    # W a2 / B b3 on a 2-file flat board: White captures a2xb3 (passer), Black captures
    # b3xa2 or plays b2 (wins the race), so G = {+BIG | -BIG}: first player wins any sum.
    for rule in ("count", "mover", "opponent"):
        geo, rules, T, ref, s = make(2, False, race_rule=rule)
        W, B = geo.parse("W: a2 / B: b3")
        out = s.outcomes(W, B, [ref[n] for n in REF_NAMES])
        if rule == "mover":
            # b3-b2 now loses the race for Black, but b3xa2 still wins
            assert set(out) == {"N"}
        else:
            assert set(out) == {"N"}


def random_positions(geo, rules, nw, nb, k, seed):
    rng = random.Random(seed)
    sqs = [geo.sq(f, r) for f in range(geo.F) for r in range(2, 8)]
    out = []
    while len(out) < k:
        pick = rng.sample(sqs, nw + nb)
        W = sum(1 << s for s in pick[:nw])
        B = sum(1 << s for s in pick[nw:])
        if not rules.has_initial_passer(W, B):
            out.append((W, B))
    return out


@pytest.mark.parametrize("files,wrap", [(4, False), (4, True), (5, True)])
def test_tree_independence(files, wrap):
    """Outcome must not depend on which tree represents a game."""
    geo = Geometry(files, wrap)
    T = Trees()
    ref = reference_set(T)
    alt = canonical_alternatives(T)
    star3_as_sum = T.add(ref["*2"], ref["*"])
    s = SumSolver(Rules(geo), T)
    for W, B in random_positions(geo, s.rules, 2, 2, 150, seed=files):
        wl, wr = s.solve(s.start_state(W, B))
        o = lambda k: s.outcome(wl, wr, k)
        assert o(ref["up*"]) == o(alt["up*"])
        assert o(ref["dup*"]) == o(alt["dup*"])
        assert o(ref["*3"]) == o(star3_as_sum)


def mirror_colours(geo, W, B):
    """Colour-reversed position (ranks flipped): the negative -G."""
    def flip(m):
        out = 0
        for s in range(geo.N):
            if (m >> s) & 1:
                f, r = geo.fileof[s], geo.rankof[s]
                out |= 1 << geo.sq(f, geo.NR + 1 - r)
        return out
    return flip(B), flip(W)


@pytest.mark.parametrize("rule", ["count", "mover", "opponent"])
@pytest.mark.parametrize("ep", [True, False])
def test_colour_symmetry(rule, ep):
    """outcome(-G + -X) is outcome(G + X) with L and R swapped."""
    geo = Geometry(4, True)
    T = Trees()
    ref = reference_set(T)
    negs = {n: T.neg(ref[n]) for n in REF_NAMES}     # build before the solver freezes T
    s = SumSolver(Rules(geo, ep=ep, race_rule=rule), T)
    swap = {"L": "R", "R": "L", "N": "N", "P": "P"}
    for W, B in random_positions(geo, s.rules, 2, 1, 80, seed=7):
        W2, B2 = mirror_colours(geo, W, B)
        wl, wr = s.solve(s.start_state(W, B))
        wl2, wr2 = s.solve(s.start_state(W2, B2))
        for n in REF_NAMES:
            k, kn = ref[n], negs[n]
            assert s.outcome(wl2, wr2, kn) == swap[s.outcome(wl, wr, k)]


def test_cylinder_rotation_and_flat_reflection():
    for files, wrap in [(5, True), (4, False)]:
        geo = Geometry(files, wrap)
        T = Trees()
        ref = reference_set(T)
        s = SumSolver(Rules(geo), T)

        def move_files(m, fmap):
            out = 0
            for sq in range(geo.N):
                if (m >> sq) & 1:
                    out |= 1 << geo.sq(fmap(geo.fileof[sq]), geo.rankof[sq])
            return out
        fmap = (lambda f: (f + 2) % files) if wrap else (lambda f: files - 1 - f)
        for W, B in random_positions(geo, s.rules, 2, 2, 80, seed=3):
            a = s.solve(s.start_state(W, B))
            b = s.solve(s.start_state(move_files(W, fmap), move_files(B, fmap)))
            assert a == b


def test_comp_mode_G_minus_G_is_zero():
    """In component mode the BIG integers add, so G + (-G) must be P (and G-G+X ~ X)."""
    geo = Geometry(5, False)           # G on files a-b, -G on files d-e, c empty
    T = Trees()
    ref = reference_set(T)
    for ep in (True, False):
        s = SumSolver(Rules(geo, ep=ep), T, mode="comp")
        small = Geometry(2, False)
        sr = Rules(small)
        for W, B in random_positions(small, sr, 1, 1, 30, seed=11) + random_positions(small, sr, 2, 1, 30, seed=12):
            # re-embed on the 5-file board
            def emb(m, shift):
                out = 0
                for sq in range(small.N):
                    if (m >> sq) & 1:
                        out |= 1 << geo.sq(small.fileof[sq] + shift, small.rankof[sq])
                return out
            Wg, Bg = emb(W, 0), emb(B, 0)
            Wn, Bn = mirror_colours(geo, emb(W, 3), emb(B, 3))
            wl, wr = s.solve(s.start_state(Wg | Wn, Bg | Bn))
            for n in REF_NAMES:
                assert s.outcome(wl, wr, ref[n]) == TEXTBOOK[n], (geo.show(Wg | Wn, Bg | Bn), n)
