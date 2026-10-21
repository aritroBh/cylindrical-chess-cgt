"""Attempt a REAL-CHESS proof that White wins the embedded component (with
the given side to move), built on White's pawn strategy from a certify_check
lower-test certificate (see strategy.py):

  White-to-move strategy node: White plays the strategy's pawn move.
  Black-to-move strategy node (real position, Black to move): EVERY legal
  move must lose for Black:
    * pawn moves: exactly the model's options (checked); each leads to a
      White-to-move strategy node or to a support terminal, whose real
      result with White to move is a certified White win;
    * king moves (outside the pawn tree): the child (White to move) must be
      a real-chess White win, shown by the tablebase (<= 7 men), by search
      with the tablebase at every capture, and, if --use-l8, Lichess's own
      categories of 8-man positions (labelled).
    A Black-to-move node with <= 8 men may instead be resolved as a whole.
Every leaf is recorded; the proof is complete iff every leaf is resolved.

    PYTHONPATH=. .venv/bin/python -m realchess.certify.realproof <cert.json> --first B --cap 1200 \
        --max-new 200 --per-pos 15 --ext 6 --use-l8 --out <json>
"""
from __future__ import annotations

import argparse
import json
import sys
from functools import lru_cache

from cylcgt.pawns import Pos

from realchess import component as C
from realchess import movegen as mg
from realchess.oracle_value import Terminals
from realchess.probe import CapReached

from . import infra, termdb
from .search9 import DeepSearcher


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("--first", default="B")
    ap.add_argument("--cap", type=int, default=1200)
    ap.add_argument("--max-new", type=int, default=200)
    ap.add_argument("--per-pos", type=int, default=15)
    ap.add_argument("--ext", type=int, default=6)
    ap.add_argument("--use-l8", action="store_true")
    ap.add_argument("--no-whole-node", action="store_true", help="do not resolve <=8-man Black nodes as a whole")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    sys.setrecursionlimit(1000000)
    from realchess.solve_candidate import Model, RealOracle, deepen, is_model_internal, make_order
    d = json.load(open(a.cert))
    T = Terminals(Pos.parse(d["component"]))
    by = {str(t): t for t in T.terms}
    fixed = {by[s["terminal"]]: s["class"] for s in d["tests"]["lower"]["support"]}
    val = {t: (1 if fixed.get(t) == "L" else (-1 if fixed.get(t) == "R" else -2)) for t in T.terms}
    db = termdb.load()

    @lru_cache(maxsize=None)
    def win(p, side):
        other = "B" if side == "W" else "W"
        for q in C.options(T.board, p, side):
            if q in T.terms:
                if (val[q] > 0) == (side == "W"):
                    return True
                continue
            if not win(q, other):
                return True
        return False

    pr = infra.CertProber(a.cap, tag="certify-realproof")
    oracle = RealOracle(pr, a.max_new)
    model = Model()
    region = lambda pos: "model" if is_model_internal(pos, model) else "off"
    s = DeepSearcher(oracle, order_hint=make_order(model, pr.cached), region=region, cached=pr.cached,
                     kb=infra.kb(), max_nodes=4 * 10**6)
    if a.use_l8:
        s.l8, s.kb_max_men = True, 8
    glob = oracle.max_new
    leaves = []
    memo = {}

    def resolve(pos, want_white, what):
        """Is pos a real White win (want_white=1)? Returns (ok, how)."""
        key = mg.normal_fen(pos)
        if key in memo:
            return memo[key]
        r = db.get(key)
        if r is not None:
            res = (r["white"] == want_white, "realdb: " + r["how"])
        else:
            oracle.max_new = min(glob, oracle.new_requests + a.per_pos)
            try:
                iv = s.search(pos, 0) if pos.men() <= 7 else deepen(s, pos, a.ext)
                how = ("tablebase (<=7 men)" if pos.men() <= 7 else f"search ({pos.men()} men, ext<={a.ext})") + \
                      (" [may use Lichess 8-man categories]" if a.use_l8 and pos.men() >= 8 else "")
            except CapReached:
                if oracle.new_requests >= glob:
                    raise
                iv, how = (-1, 1), "per-position budget"
            except RuntimeError as e:
                iv, how = (-1, 1), repr(e)
            finally:
                oracle.max_new = glob
            if iv[0] == iv[1]:
                w = iv[0] if pos.stm == mg.WHITE else -iv[0]
                row = termdb.make_row(pos, iv, how, a.ext)
                row.update(source="realproof", l8=bool(a.use_l8 and pos.men() >= 8))
                termdb.append([row])
                res = (w == want_white, how + f" -> white {w}")
            else:
                res = (None, how + " -> unresolved")
        memo[key] = res
        leaves.append({"what": what, "fen": key, "men": pos.men(), "ok": res[0], "how": res[1]})
        return res

    stats = {"white_nodes": 0, "black_nodes": 0, "terminal_leaves": 0, "king_leaves": 0, "whole_node_leaves": 0}
    seen = set()

    def walk(p, side):
        if (p, side) in seen:
            return
        seen.add((p, side))
        if side == "W":
            stats["white_nodes"] += 1
            for q in C.options(T.board, p, "W"):
                if q in T.terms and val[q] > 0:
                    stats["terminal_leaves"] += 1
                    resolve(C.embed(q, "B"), 1, f"support terminal {q}, Black to move")
                    return
                if q not in T.terms and not win(q, "B"):
                    walk(q, "B")
                    return
            raise AssertionError("no winning White move at " + str(p))
        stats["black_nodes"] += 1
        pos = C.embed(p, "B")
        if pos.men() <= 8 and not a.no_whole_node:
            ok, how = resolve(pos, 1, f"strategy node {p}, Black to move, as a whole")
            if ok:
                stats["whole_node_leaves"] += 1
                return
        legal = mg.legal_moves(pos)
        pawn_children = {mg.normal_fen(mg.make(pos, m)) for m in legal if pos.board[m.frm].upper() != "K"}
        model_children = {mg.normal_fen(C.embed(q, "W")) for q in C.options(T.board, p, "B")}
        assert pawn_children == model_children, (str(p), pawn_children ^ model_children)
        for m in legal:
            if pos.board[m.frm].upper() == "K":
                stats["king_leaves"] += 1
                resolve(mg.make(pos, m), 1, f"king move {m.uci()} at {p}")
        for q in C.options(T.board, p, "B"):
            if q in T.terms:
                assert val[q] > 0
                stats["terminal_leaves"] += 1
                resolve(C.embed(q, "W"), 1, f"support terminal {q}, White to move")
            else:
                walk(q, "W")

    status = "complete"
    try:
        walk(T.comp, a.first)
    except CapReached:
        status = "stopped: --max-new"
    ok = [l for l in leaves if l["ok"] is True]
    bad = [l for l in leaves if l["ok"] is False]
    open_ = [l for l in leaves if l["ok"] is None]
    out = {"component": d["component"], "first": a.first, "status": status, "stats": stats,
           "leaves": len(leaves), "leaves_ok": len(ok), "leaves_refuted": len(bad), "leaves_open": len(open_),
           "proof_complete": status == "complete" and not bad and not open_,
           "uses_l8": any("Lichess 8-man" in l["how"] for l in ok),
           "new_requests": oracle.new_requests, "ledger": pr.ledger_count(), "leaf_list": leaves}
    with open(a.out, "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "leaf_list"}, indent=1))
    for l in bad + open_:
        print("NOT OK:", l)


if __name__ == "__main__":
    main()
