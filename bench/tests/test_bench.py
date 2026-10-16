"""Tests for ChessSums.

    cd /Users/aritro/Downloads/Research/Chessendgames
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m pytest -q -p no:cacheprovider bench/tests
"""
import json
import random
from pathlib import Path

import pytest

from cylcgt import cgt, pawns
from bench import board as bd
from bench import cgtfmt
from bench.baseline import AB_BIN, Solver, c_solve
from bench.reward import chesssums_reward, reward
from bench.score import score

DATA = Path(__file__).resolve().parents[1] / "data"


def P(s):
    return cgtfmt.parse(s)


def test_parse_basics():
    assert P("0") is cgt.ZERO
    assert P("*") is cgt.STAR and P("*1") is cgt.STAR
    assert P("{0,*|0,*}") is cgt.nimber(2) and P("*2") is cgt.nimber(2)
    assert P("1/2 + *") is P("1/2*") is cgt.add(cgt.number(cgtfmt.Fraction(1, 2)), cgt.STAR)
    assert P("↑") is cgt.UP and P("^") is cgt.UP and P("v") is cgt.DOWN
    assert P("⇑*") is P("^^*") is P("↑ + ↑ + *")
    assert P("-1↑") is cgt.add(cgt.integer(-1), cgt.UP)          # unary minus binds to the number
    assert P("±1") is P("+-1") is P("+/-1") is cgt.make([cgt.integer(1)], [cgt.integer(-1)])
    assert P("1 + -1") is cgt.ZERO                              # spaced: plus, then minus one
    assert P("3/2±1/2") is cgt.make([cgt.integer(2)], [cgt.integer(1)])
    assert P("{2 | 1/2}") is P("{2|1/2}")
    assert P("{0|1}") is P("1/2")                               # canonicalised
    assert P("(1 + 1) - 2") is cgt.ZERO
    assert P("0.5") is P("1/2")


@pytest.mark.parametrize("bad", ["", "*999", "^" * 40, "1/3", "{" * 30 + "0|" + "}" * 30, "x", "1 +", "{1|", "9999",
                                 "1024 + 1024", " ".join(["^"] * 200), "+".join(["0"] * 600)])
def test_parse_rejects(bad):
    with pytest.raises((cgtfmt.ParseError, ValueError)):
        cgtfmt.parse(bad)


def test_format_roundtrip_on_sums():
    rng = random.Random(0)
    comps = [json.loads(x) for x in (DATA / "components.jsonl").read_text().splitlines()]
    games = [P(c["value_ascii"]) for c in comps]
    for c, g in zip(comps, games):
        assert P(c["value"]) is g
        assert cgtfmt.fmt(g) == c["value"]
    for _ in range(300):
        G = cgt.total(rng.choice(games) for _ in range(rng.randint(1, 6)))
        assert P(cgtfmt.fmt(G)) is G
        assert P(cgtfmt.fmt(G, ascii=True)) is G


def _random_pos(rng, W):
    sqs = [(f, r) for f in range(W) for r in range(2, 8)]
    pts = rng.sample(sqs, rng.randint(2, 7))
    cut = rng.randint(1, len(pts) - 1)
    return frozenset(pts[:cut]), frozenset(pts[cut:])


def test_move_generator_matches_cylcgt():
    rng = random.Random(1)
    for _ in range(2000):
        W = rng.randint(2, 9)
        wrap = rng.random() < 0.5
        w, b = _random_pos(rng, W)
        board = pawns.Board(W, 8, wrap, True)
        geo = bd.Geometry(W, wrap)
        for side in "WB":
            mine = {(p.white, p.black) for p in pawns.moves(board, pawns.Pos(w, b), side)}
            ours = {(nw, nb) for _, _, _, nw, nb in bd.gen_moves(geo, w, b, side)}
            assert mine == ours


def test_resolve_move():
    geo = bd.Geometry(8, True)
    w, b = frozenset({(4, 2), (3, 4), (7, 4)}), frozenset({(4, 5), (0, 5)})
    legal = bd.gen_moves(geo, w, b, "W")
    names = {n for n, *_ in legal}
    assert "e2-e4" in names and "d4xe5" in names and "h4xa5" in names     # wrap capture
    assert bd.resolve_move("e2-e4", legal) == "e2-e4"
    assert bd.resolve_move("e2e4", legal) == "e2-e4"
    assert bd.resolve_move("e4", legal) == "e2-e4"
    assert bd.resolve_move("dxe5", legal) == "d4xe5"
    assert bd.resolve_move("hxa5", legal) == "h4xa5"
    assert bd.resolve_move("e2-e5", legal) is None
    assert bd.resolve_move("a5-a4", legal) is None                          # Black's pawn


def _rows(split, n=400):
    p = DATA / f"{split}.jsonl"
    if not p.exists():
        pytest.skip("data not generated")
    rows = [json.loads(x) for x in p.read_text().splitlines()]
    return random.Random(2).sample(rows, min(n, len(rows)))


@pytest.mark.parametrize("split", ["train", "val", "test", "test_heldout"])
def test_rows_consistent(split):
    comps = {json.loads(x)["comp_id"]: json.loads(x) for x in (DATA / "components.jsonl").read_text().splitlines()}
    for r in _rows(split):
        G = P(r["value_ascii"])
        assert cgt.outcome(G) == r["outcome"]
        vals = [P(c["value"]) for c in r["components"]]
        assert cgt.total(vals) is G
        assert cgt.total(reversed(vals)) is G                    # order of summation is irrelevant
        assert all(comps[c["comp_id"]]["value"] == c["value"] for c in r["components"])
        assert len(r["components"]) == r["k"]
        assert bool(r["winning_moves"]["W"]) == (r["outcome"] in "LN")
        assert bool(r["winning_moves"]["B"]) == (r["outcome"] in "RN")
        for s in "WB":
            assert set(r["winning_moves"][s]) <= set(r["legal_moves"][s])
        assert r["fits8"] == (r["board"]["files"] == 8)
        assert (split == "test_heldout") == bool(r["heldout"])


def test_python_solver_on_rows():
    for r in _rows("val", 60):
        s = Solver(r["board"]["files"], r["board"]["cylinder"], tt=True)
        w = {bd.parse_sq(x) for x in r["white"]}
        b = {bd.parse_sq(x) for x in r["black"]}
        assert (s.solve(w, b, True) == 1) == (r["outcome"] in "LN")
        assert (s.solve(w, b, False) == 1) == (r["outcome"] in "RN")


@pytest.mark.skipif(not AB_BIN.exists(), reason="build bench/ab with cc -O2 -o bench/ab bench/ab.c")
def test_c_solver_matches_python_exactly():
    rng = random.Random(3)
    cases = []
    while len(cases) < 150:  # random positions with no passed pawn at the root
        W = rng.randint(2, 8)
        wrap = rng.random() < 0.5
        w, b = _random_pos(rng, W)
        s = Solver(W, wrap)
        if not (s.passed(w, b, True) or s.passed(b, w, False)):
            cases.append((W, wrap, w, b))
    for r in _rows("val", 60) + _rows("test", 20):
        cases.append((r["board"]["files"], r["board"]["cylinder"],
                      {bd.parse_sq(x) for x in r["white"]}, {bd.parse_sq(x) for x in r["black"]}))
    jobs, py = [], []
    for W, wrap, w, b in cases:
        for side in (True, False):
            s = Solver(W, wrap, tt=False, node_cap=50_000)
            try:
                v = s.solve(w, b, side)
            except Exception:
                continue
            py.append((v, s.nodes))
            jobs.append((W, wrap, w, b, side, False, 50_000, 0))
    assert len(jobs) >= 400
    res = c_solve(jobs)
    assert [(v, n) for v, n, _ in res] == py          # same results AND same node counts


def test_reward_and_score():
    r = _rows("val", 50)
    for row in r:
        for s in "WB":
            if row["winning_moves"][s]:
                m = row["winning_moves"][s][0]
                assert reward(f"<answer>{m}</answer>", row, "move", s) == pytest.approx(1.1)
                assert reward("<answer>z9-z10</answer>", row, "move", s) == pytest.approx(-0.4)
                losing = [x for x in row["legal_moves"][s] if x not in row["winning_moves"][s]]
                if losing:
                    assert reward(f"<answer>{losing[0]}</answer>", row, "move", s) == pytest.approx(0.2)
        assert reward(f"<answer>{row['value']}</answer>", row, "value") == pytest.approx(1.1)
        assert reward(f"<answer>{row['outcome']}</answer>", row, "outcome") == pytest.approx(1.1)
        assert reward("the answer is " + row["outcome"], row, "outcome") == 0.0
    out = chesssums_reward(completions=[f"<answer>{x['value_ascii']}</answer>" for x in r],
                           gold=[json.dumps(x) for x in r], task=["value"] * len(r), side=[None] * len(r))
    assert out == [pytest.approx(1.1)] * len(r)
    preds = {}
    for x in r:
        preds[f"{x['id']}:outcome"] = x["outcome"]
        preds[f"{x['id']}:value"] = x["value_ascii"]
        for s in "WB":
            if x["winning_moves"][s]:
                preds[f"{x['id']}:move:{s}"] = x["winning_moves"][s][-1]
    res = score(r, preds)
    for t in ("outcome", "move", "value"):
        assert res[t]["all"]["correct"] == res[t]["all"]["n"]
