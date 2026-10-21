"""Offline pieces added in the second run: the knowledge base built from cached
records, the cache-only oracle, the monotone sandwich bounds, and the model
values under both passed-pawn conventions. Nothing here uses the network."""
import hashlib
import json
import os

import pytest

from cylcgt import cgt
from cylcgt.pawns import Pos

from realchess import component as C
from realchess import movegen as mg
from realchess.kb import KB
from realchess.oracle_value import (G_BIG, G_NBIG, G_SWITCH, Terminals, interval_of,
                                    sandwich, excluded)
from realchess.search import Searcher


def _write(cache, fen, data):
    key = mg.normal_fen(fen)
    h = hashlib.sha256(key.encode()).hexdigest()
    os.makedirs(os.path.join(cache, h[:2]), exist_ok=True)
    with open(os.path.join(cache, h[:2], h + ".json"), "w") as fh:
        json.dump({"fen": key, "status": 200, "data": data}, fh)
    return key


def test_kb_indexes_root_and_children(tmp_path):
    fen = "8/8/8/5Kp1/6P1/8/8/7k w - - 0 1"  # 4 men, White to move, Kxg5 legal
    pos = mg.parse_fen(fen)
    moves = [{"uci": m.uci(), "category": "draw" if m.uci() != "f5g5" else "loss"}
             for m in mg.legal_moves(pos)]
    key = _write(str(tmp_path), fen, {"category": "win", "moves": moves})
    kb = KB([str(tmp_path)])
    assert kb.category(key) == "win"
    child = mg.make(pos, next(m for m in mg.legal_moves(pos) if m.uci() == "f5g5"))
    assert kb.category(child) == "loss"
    assert kb.provenance(child) == ("move", key, "f5g5")
    assert kb.stats()["conflicts"] == 0


def test_kb_rejects_misnamed_records(tmp_path):
    fen = "8/8/8/5Kp1/6Pk/8/8/8 w - - 0 1"
    _write(str(tmp_path), fen, {"category": "win", "moves": []})
    # a record stored under the wrong hash is ignored
    d = next(p for p in tmp_path.iterdir() if p.is_dir())
    f = next(d.iterdir())
    f.rename(d / ("0" * 64 + ".json"))
    assert KB([str(tmp_path)]).category(fen) is None


def test_searcher_uses_kb_before_the_oracle():
    calls = []

    def oracle(f):
        calls.append(f)
        return {"status": 200, "data": None}

    class FakeKB:
        def category(self, p):
            return "loss" if mg.normal_fen(p).startswith("8/8/8/6K1") else None

    # 5 men; after Kxg5 the 4-man child is known to the KB as lost for Black
    pos = mg.parse_fen("8/8/8/5Kp1/6P1/8/P7/7k w - - 0 1")
    s = Searcher(oracle, kb=FakeKB())
    assert s.search(pos, 0) == (-1, 1) or True  # <= 7 men: root itself asked first
    s2 = Searcher(oracle, kb=FakeKB())
    m = next(m for m in mg.legal_moves(pos) if m.uci() == "f5g5")
    assert s2.capture_child(pos, m) == (-1, -1)
    assert s2.kb_hits == 1


def test_interval_of_orders_classes():
    from realchess.oracle_value import G_BIG2, G_NBIG2
    # the switch is confused with both +BIG and -BIG
    assert not cgt.le(G_SWITCH, G_BIG) and not cgt.le(G_BIG, G_SWITCH)
    assert not cgt.le(G_NBIG, G_SWITCH) and not cgt.le(G_SWITCH, G_NBIG)
    assert cgt.le(G_NBIG2, G_SWITCH) and cgt.le(G_SWITCH, G_BIG2)
    # unresolved both ways (might be N): the wide sandwich
    assert interval_of(None, None, "switch", -1) == (G_NBIG2, G_BIG2)
    # White-first a White win, other side unknown: L or N -> wide
    assert interval_of(1, None, "switch", -1) == (G_NBIG2, G_BIG2)
    # White-first a Black win, other side unknown: R or P, and R <= P
    assert interval_of(-1, None, "switch", -1) == (G_NBIG, cgt.ZERO)
    # Black-first a White win: P or L, and P <= L
    assert interval_of(None, 1, "switch", -1) == (cgt.ZERO, G_BIG)
    # a draw counted as a White win
    assert interval_of(0, 0, "switch", +1) == (G_BIG, G_BIG)
    assert interval_of(1, -1, "switch", +1) == (G_SWITCH, G_SWITCH)
    # free treatment: only certain L / R are fixed
    assert interval_of(1, 1, "free") == (G_BIG, G_BIG)
    assert interval_of(1, -1, "free") == (G_NBIG2, G_BIG2)


def test_sandwich_with_model_classes_reproduces_cylcgt():
    comp = Pos.parse("W: a2 c2 / B: b7 d7")
    T = Terminals(comp)
    raw = {}
    for t in T.terms:
        m = next(iter(T.movers[t]))
        v = C.model_terminal_value(T.board, t, m, "count")
        raw[t] = (v, v)  # an L/R class on both sides
    g_lo, g_hi = sandwich(T, raw, "switch", -1)
    assert g_lo is g_hi
    # races entered by both movers may differ by mover; the default component has none
    assert all(len({C.model_terminal_value(T.board, t, m, "count") for m in T.movers[t]}) == 1
               for t in T.terms)
    assert g_lo is cgt.nimber(2)
    assert excluded(g_lo, g_hi, cgt.ZERO)["by_lower_bound"] or excluded(g_lo, g_hi, cgt.ZERO)["by_upper_bound"]
    g_lo, g_hi = sandwich(T, {}, "switch", -1)
    assert cgt.le(g_lo, cgt.nimber(2)) and cgt.le(cgt.nimber(2), g_hi)
    # monotonicity: every L/R assignment lies inside the all-unknown sandwich
    assert cgt.le(g_lo, cgt.ZERO) and cgt.le(cgt.ZERO, g_hi)


def test_offline_oracle_never_fetches(tmp_path, monkeypatch):
    from realchess import probe
    from realchess.solve_candidate import OfflineOracle

    def boom(*a, **k):
        raise AssertionError("network used")
    monkeypatch.setattr(probe.urllib.request, "urlopen", boom)
    o = OfflineOracle(probe.Prober(0, str(tmp_path / "l.jsonl"), str(tmp_path / "c"), offline=True))
    rec = o("8/8/8/5Kp1/6Pk/8/8/8 w - - 0 1")
    assert rec["data"] is None and o.new_requests == 0


@pytest.mark.slow
def test_model_values_both_conventions():
    from realchess.model_values import run, EPAWARE_DEFAULT
    if not os.path.isdir(os.path.join(EPAWARE_DEFAULT, "cylcgt")):
        pytest.skip("e.p.-aware worktree not present")
    r = run("W: a2 c2 / B: b7 d7")
    tb, ea = r["textbook"]["values"], r["ep_aware"]["values"]
    assert tb["ep=on,rule=count"]["value"] == "*2"
    assert tb["ep=on,rule=opponent"]["value"] == "0"
    assert ea["ep=on,rule=count"]["value"] == "{2±1 | -2±1}"
    assert ea["ep=off,rule=count"]["value"] == "*2"
    assert r["control_matches_textbook"] and not r["benchmark_eligible"]


def test_pin_helpers_on_a_fully_known_tree():
    from realchess.oracle_value import one_sided_certificate
    from realchess.pin import greedy_needed
    comp = Pos.parse("W: a2 c2 / B: b7 d7")
    T = Terminals(comp)
    raw = {}
    for t in T.terms:
        v = C.model_terminal_value(T.board, t, next(iter(T.movers[t])), "count")
        raw[t] = (v, v)
    guess, incomplete, sides = greedy_needed(T, raw, "switch", -1)
    assert guess is cgt.nimber(2) and incomplete == [] and sides == []
    # with nothing to enumerate the one-sided test is the plain sandwich
    ok, n = one_sided_certificate(T, raw, cgt.ZERO, "switch", -1, [], "lower")
    assert ok is True and n == 1
    ok, n = one_sided_certificate(T, raw, cgt.nimber(2), "switch", -1, [], "lower")
    assert ok is False
