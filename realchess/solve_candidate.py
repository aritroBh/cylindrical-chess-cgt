"""Exact real-chess certification of an a-d pawn component embedded next to
the g-file trebuchet (WK f5, Pg4 / BK h4, Pg5; file e empty).

Default component: W a2 c2 / B b7 d7, i.e. the FEN
    8/1p1p4/8/5Kp1/6Pk/8/P1P5/8 w - - 0 1   (and the same with b to move).

Stages (each writes results/<tag>_*.json):
  roots    real-chess result of the embedded position, White and Black to move;
  nodes    real-chess result of every internal model node (8-man, trebuchet
           intact) reached so far / as budget allows, with the cylcgt outcome
           class of the component alone under every RACE_RULE;
  oracle   the "real-chess oracle value": the CGT value of the component with
           every model terminal replaced by its real-chess outcome class
           (see oracle_value.py).

Every 7-man (or smaller) position is resolved by the Lichess tablebase through
realchess.probe (cache first, <= 1 request/s, hard cap on the ledger).

Usage (from the project root):
  PYTHONPATH=. .venv/bin/python -m realchess.solve_candidate roots \
      --component "W: a2 c2 / B: b7 d7" --cap 1200 --max-new 300
  ... nodes  --max-new 200
  ... oracle --max-new 400
  add --dry-run to replace the tablebase by a crude heuristic oracle (no network)
  and print how many requests a stage would need.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter

from cylcgt import cgt, pawns
from cylcgt.pawns import Pos

from . import component as C
from . import movegen as mg
from .probe import Prober, CapReached, DEFAULT_LEDGER
from .search import Searcher

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
RULES = ("count", "mover", "opponent")
VAL_NAME = {1: "win", 0: "draw", -1: "loss"}


# ---------------------------------------------------------------- model glue
class Model:
    """cylcgt predictions for component positions (4-file flat, e.p. on)."""

    def __init__(self, board=C.BOARD4):
        self.board = board
        self._vals = {r: {} for r in RULES}

    def comp(self, pos: mg.Position) -> Pos:
        """Component Pos (with the e.p. right of the side to move, if any)."""
        c = C.component_of(pos)
        if pos.ep is not None and pos.ep % 8 < 4:
            f, r = pos.ep % 8, pos.ep // 8 + 1
            stm = "W" if pos.stm == mg.WHITE else "B"
            cap = (f, r - 1) if stm == "W" else (f, r + 1)
            c = Pos(c.white, c.black, ((f, r), cap, stm))
        return c

    def value(self, p: Pos, rule: str):
        d = self._vals[rule]
        if p not in d:
            old = pawns.RACE_RULE
            pawns.RACE_RULE = rule
            pawns._value.cache_clear()
            try:
                d[p] = pawns.value(self.board, p)
            finally:
                pawns.RACE_RULE = old
                pawns._value.cache_clear()
        return d[p]

    def outcome(self, p: Pos, rule: str) -> str:
        if C.is_terminal(self.board, p):
            return "terminal"
        return cgt.outcome(self.value(p, rule))

    def stm_wins(self, pos: mg.Position, rule: str = "count"):
        """Model prediction (True/False) that the side to move wins, or None
        if the position is outside the model (trebuchet broken, pieces...)."""
        if not C.only_component_and_trebuchet(pos):
            return None
        p = self.comp(pos)
        stm = "W" if pos.stm == mg.WHITE else "B"
        if C.is_terminal(self.board, p):
            other = "B" if stm == "W" else "W"
            v = C.model_terminal_value(self.board, Pos(p.white, p.black, None), other, rule)
            return (v > 0) == (stm == "W")
        o = self.outcome(Pos(p.white, p.black, p.ep), rule)
        return o == "N" or o == ("L" if stm == "W" else "R")


def is_model_internal(pos: mg.Position, model: Model) -> bool:
    if not C.only_component_and_trebuchet(pos):
        return False
    return not C.is_terminal(model.board, C.component_of(pos))


def make_order(model: Model, cached_fn):
    """Move ordering: cheap proven wins first, then model-predicted wins,
    captures, pawn moves, everything else; king moves last in model nodes."""

    def order(pos, moves):
        in_model = C.only_component_and_trebuchet(pos)
        rec = cached_fn(mg.normal_fen(pos)) if cached_fn else None
        cats = {}
        if rec and rec.get("data"):
            cats = {m["uci"]: m.get("category") for m in rec["data"].get("moves", [])}

        def key(m):
            cap = mg.is_capture(pos, m)
            if cap and cats.get(m.uci()) in ("loss", "blessed-loss"):
                return (0, 0)
            piece = pos.board[m.frm].upper()
            child = mg.make(pos, m)
            if in_model:
                if piece == "K":
                    return (9, 0)
                if not cap:
                    pred = model.stm_wins(child)
                    if pred is False:
                        return (1, 0)
                    return (4 if pred is None else 5, 0)
                return (3, 0)
            # off-model: captures first, then checks, promotions, pawn pushes
            if cap:
                return (2, 0)
            if mg.in_check(child):
                return (3, 0)
            if m.promo:
                return (3, 1 if m.promo == "q" else 2)
            if piece == "P":
                return (4, 0)
            return (6, 0)

        return sorted(moves, key=key)

    return order


# ---------------------------------------------------------------- oracles
class RealOracle:
    def __init__(self, prober: Prober, max_new: int):
        self.pr = prober
        self.max_new = max_new
        self.start = prober.requests_this_process

    def cached(self, fen):
        return self.pr.cached(fen)

    def __call__(self, fen):
        rec = self.pr.cached(fen)
        if rec is not None:
            return rec
        if self.pr.requests_this_process - self.start >= self.max_new:
            raise CapReached(f"--max-new {self.max_new} reached")
        rec = self.pr.probe(fen)
        if rec.get("status") != 200:
            raise RuntimeError(f"probe failed {rec.get('status')}: {fen} {rec.get('body')}")
        return rec

    @property
    def new_requests(self):
        return self.pr.requests_this_process - self.start


class HybridOracle:
    """Dry-run helper: real cached records where they exist, FakeOracle guesses
    elsewhere; counts only the positions that would need a NEW request."""

    def __init__(self, model, prober: Prober, max_new: int = 10**9):
        self.fake = FakeOracle(model, max_new)
        self.pr = prober

    def cached(self, fen):
        return self.pr.cached(fen) or self.fake.cached(fen)

    def __call__(self, fen):
        rec = self.pr.cached(fen)
        return rec if rec is not None else self.fake(fen)

    @property
    def new_requests(self):
        return self.fake.new_requests

    @property
    def max_new(self):
        return self.fake.max_new

    @max_new.setter
    def max_new(self, v):
        self.fake.max_new = v


class FakeOracle:
    """Crude heuristic stand-in for dry runs (NO claims are based on it):
    trebuchet intact -> cylcgt model (count rule); otherwise material count."""

    def __init__(self, model: Model, max_new: int = 10**9):
        self.model = model
        self.calls = set()
        self.store = {}
        self.max_new = max_new

    def cached(self, fen):
        return self.store.get(fen)

    def guess(self, pos: mg.Position) -> str:
        w = self.model.stm_wins(pos)
        if w is not None:
            return "win" if w else "loss"
        val = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9}
        s = 0
        for p in pos.board:
            if p != ".":
                if p.upper() == "K":
                    continue
                s += val[p.upper()] * (1 if p.isupper() else -1)
        if s == 0:
            return "draw"
        white_better = s > 0
        return "win" if white_better == (pos.stm == mg.WHITE) else "loss"

    def __call__(self, fen):
        if fen in self.store:
            return self.store[fen]
        if len(self.calls) >= self.max_new:
            raise CapReached("dry-run max_new reached")
        self.calls.add(fen)
        pos = mg.parse_fen(fen)
        moves = []
        for m in mg.legal_moves(pos):
            ch = mg.make(pos, m)
            cat = self.guess(ch) if ch.men() <= 7 else "unknown"
            moves.append({"uci": m.uci(), "category": cat})
        root = self.guess(pos) if pos.men() <= 7 else "unknown"
        rec = {"fen": fen, "status": 200, "data": {"category": root, "moves": moves}}
        self.store[fen] = rec
        return rec

    @property
    def new_requests(self):
        return len(self.calls)


# ---------------------------------------------------------------- helpers
def root_position(comp: Pos, stm: str) -> mg.Position:
    return C.embed(comp, stm)


def outcome_class(rw, rb):
    """rw = result for White when White moves first (+1/0/-1), rb = result for
    White when Black moves first. Returns L/R/N/P or a draw label."""
    if rw is None or rb is None:
        return "unresolved"
    if rw == 1 and rb == 1:
        return "L"
    if rw == -1 and rb == -1:
        return "R"
    if rw == 1 and rb == -1:
        return "N"
    if rw == -1 and rb == 1:
        return "P"
    return f"draw(W-first:{VAL_NAME[rw]},B-first:{VAL_NAME[rb]})"


def white_view(iv, stm):
    lo, hi = iv
    if lo != hi:
        return None
    return lo if stm == mg.WHITE else -lo


def comp_str(p: Pos) -> str:
    return str(Pos(p.white, p.black, None))


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(obj, fh, indent=1, default=str)
    os.replace(tmp, path)


def tag_of(comp: Pos) -> str:
    return "comp_" + comp_str(comp).replace("W: ", "W").replace(" / B: ", "_B").replace(" ", "")


# ---------------------------------------------------------------- stages
def build(args):
    comp = Pos.parse(args.component)
    for f, _ in comp.white | comp.black:
        if f > 3:
            raise SystemExit("component must use files a-d only")
    model = Model()
    if args.dry_run and args.hybrid:
        oracle = HybridOracle(model, Prober(0, args.ledger, offline=True), args.max_new)
        cached = oracle.cached
    elif args.dry_run:
        oracle = FakeOracle(model, args.max_new)
        cached = oracle.cached
    else:
        prober = Prober(args.cap, args.ledger, tag=f"A2-{args.stage}", verbose=args.verbose)
        oracle = RealOracle(prober, args.max_new)
        cached = oracle.cached
    region = lambda pos: "model" if is_model_internal(pos, model) else "off"
    return comp, model, oracle, cached, region


def refutation_of(searcher: Searcher, pos: mg.Position):
    """For a node whose value is known, the first move achieving it (from the
    TT / probe data, no new search)."""
    best = None
    for uci, (lo, hi), how in searcher.principal(pos, 0):
        if lo == hi and (best is None or lo > best[1]):
            best = (uci, lo, how)
    return best


def node_report(searcher: Searcher, model: Model, pos: mg.Position):
    key = mg.normal_fen(pos)
    h = searcher.tt.get(key)
    iv = (h[0], h[1]) if h else (-1, 1)
    entry = {"fen": key, "stm": pos.stm, "interval": iv,
             "result": VAL_NAME[iv[0]] if iv[0] == iv[1] else "unresolved"}
    if C.only_component_and_trebuchet(pos):
        p = model.comp(pos)
        entry["component"] = str(p)
        entry["model_stm_wins"] = {r: model.stm_wins(pos, r) for r in RULES}
    # king moves and their refutations
    kings = []
    for m in mg.legal_moves(pos):
        if pos.board[m.frm].upper() != "K":
            continue
        child = mg.make(pos, m)
        hc = searcher.tt.get(mg.normal_fen(child))
        civ = (hc[0], hc[1]) if hc else (-1, 1)
        ref = refutation_of(searcher, child) if hc and hc[0] == hc[1] else None
        kings.append({"move": m.uci(), "value_for_mover": (-civ[1], -civ[0]),
                      "refutation": ref})
    entry["king_moves"] = kings
    return entry


def deepen(s: Searcher, pos, max_ext: int):
    """Iterative deepening on the off-model ply budget; the TT and the probe
    cache make re-searches cheap. Stops as soon as the interval is exact."""
    iv = (-1, 1)
    for e in range(0, max_ext + 1):
        iv = s.search(pos, e)
        if iv[0] == iv[1]:
            break
    return iv


def stage_roots(args):
    comp, model, oracle, cached, region = build(args)
    out = {"component": comp_str(comp), "trebuchet": C.TREBUCHET, "mode": args.mode,
           "dry_run": args.dry_run, "roots": {}}
    s = Searcher(oracle, mode=args.mode, order_hint=make_order(model, cached), region=region,
                 cached=cached)
    t0 = time.time()
    status = "complete"
    for stm in ("W", "B"):
        pos = root_position(comp, stm)
        try:
            iv = deepen(s, pos, args.ext)
        except CapReached as e:
            status = f"stopped: {e}"
            iv = None
        rep = node_report(s, model, pos) if iv else {"fen": mg.normal_fen(pos), "result": "not finished"}
        rep["model_outcome_of_component"] = {r: model.outcome(comp, r) for r in RULES}
        out["roots"][stm] = rep
        if iv is None:
            break
    rw = out["roots"].get("W", {}).get("interval")
    rb = out["roots"].get("B", {}).get("interval")
    if rw and rb and rw[0] == rw[1] and rb[0] == rb[1]:
        out["real_outcome_class"] = outcome_class(rw[0], -rb[0])
    out["status"] = status
    out["new_requests"] = oracle.new_requests
    out["seconds"] = round(time.time() - t0, 1)
    out["categories_seen"] = dict(s.cats_seen)
    out["special_categories"] = s.special
    out["unresolved_leaves"] = sorted(s.unresolved_leaves)
    out["tt_size"] = len(s.tt)
    # every model-internal node in the TT
    out["model_nodes"] = model_node_table(s, model, comp)
    if not args.dry_run:
        write_json(os.path.join(RESULTS, f"{tag_of(comp)}_roots_{args.mode}.json"), out)
    summary = {k: v for k, v in out.items() if k not in ("model_nodes", "unresolved_leaves", "special_categories")}
    summary["roots"] = {k: {"result": v.get("result"), "interval": v.get("interval")} for k, v in out["roots"].items()}
    print(json.dumps(summary, indent=1, default=str))
    return out, s


def model_node_table(s: Searcher, model: Model, comp: Pos):
    """Real-chess results of every internal model node present in the TT,
    grouped by component configuration, with cylcgt predictions."""
    rows = {}
    for fen, (lo, hi, _, _) in s.tt.items():
        pos = mg.parse_fen(fen)
        if not is_model_internal(pos, model):
            continue
        p = C.component_of(pos)
        key = comp_str(p)
        r = rows.setdefault(key, {"component": key, "W": None, "B": None})
        side = "W" if pos.stm == mg.WHITE else "B"
        r[side + "_fen"] = fen
        r[side] = (lo, hi)
    for key, r in rows.items():
        p = Pos.parse(key)
        r["model_outcome"] = {rule: model.outcome(p, rule) for rule in RULES}
        w = r["W"]
        b = r["B"]
        rw = w[0] if w and w[0] == w[1] else None
        rb = -b[0] if b and b[0] == b[1] else None
        r["real_W_first_for_White"] = VAL_NAME.get(rw) if rw is not None else "unresolved"
        r["real_B_first_for_White"] = VAL_NAME.get(rb) if rb is not None else "unresolved"
        r["real_class"] = outcome_class(rw, rb)
        # partial class information when only one side is resolved
        r["agrees_with"] = [rule for rule in RULES
                            if r["real_class"] in "LRNP" and len(r["real_class"]) == 1
                            and r["model_outcome"][rule] == r["real_class"]]
    return sorted(rows.values(), key=lambda r: r["component"])


def stage_nodes(args):
    """Resolve every internal model node (both sides to move), cheapest first."""
    comp, model, oracle, cached, region = build(args)
    internal, terms, edges = C.enumerate_tree(model.board, comp)
    s = Searcher(oracle, mode=args.mode, order_hint=make_order(model, cached), region=region,
                 cached=cached)
    targets = []
    seen = set()
    for p in internal:
        for stm in "WB":
            pos = C.embed(p, stm)
            k = mg.normal_fen(pos)
            if k not in seen:
                seen.add(k)
                targets.append(pos)
    # deepest (most advanced) nodes first: their results feed the shallower ones
    def adv(pos):
        c = C.component_of(pos)
        return -(sum(r - 2 for _, r in c.white) + sum(7 - r for _, r in c.black))
    targets.sort(key=lambda pos: (adv(pos), mg.normal_fen(pos)))
    status = "complete"
    done = 0
    t0 = time.time()
    over_budget = []
    glob = oracle.max_new
    for pos in targets:
        oracle.max_new = min(glob, oracle.new_requests + args.per_target)
        try:
            deepen(s, pos, args.ext)
            done += 1
        except CapReached as e:
            if oracle.new_requests >= glob:
                status = f"stopped after {done}/{len(targets)} targets: {e}"
                break
            over_budget.append(mg.normal_fen(pos))
            done += 1
        finally:
            oracle.max_new = glob
    table = model_node_table(s, model, comp)
    out = {"component": comp_str(comp), "mode": args.mode, "dry_run": args.dry_run,
           "status": status, "targets": len(targets), "targets_done": done,
           "targets_over_per_target_budget": over_budget, "per_target": args.per_target,
           "ext": args.ext, "new_requests": oracle.new_requests,
           "seconds": round(time.time() - t0, 1), "categories_seen": dict(s.cats_seen),
           "special_categories": s.special, "nodes": table}
    cls = Counter(r["real_class"] for r in table)
    out["class_counts"] = dict(cls)
    agree = {rule: sum(1 for r in table if rule in r["agrees_with"]) for rule in RULES}
    out["agreement_with_rule"] = agree
    if not args.dry_run:
        write_json(os.path.join(RESULTS, f"{tag_of(comp)}_nodes_{args.mode}.json"), out)
    print(json.dumps({k: v for k, v in out.items() if k not in ("nodes", "special_categories")}, indent=1))
    return out, s


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["roots", "nodes", "oracle"])
    ap.add_argument("--component", default="W: a2 c2 / B: b7 d7")
    ap.add_argument("--cap", type=int, default=1200, help="hard cap on the ledger (total requests)")
    ap.add_argument("--ledger", default=DEFAULT_LEDGER)
    ap.add_argument("--max-new", type=int, default=100, help="max new requests in this run")
    ap.add_argument("--ext", type=int, default=6, help="off-model ply budget")
    ap.add_argument("--mode", choices=["pure", "fifty"], default="pure")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--hybrid", action="store_true",
                    help="with --dry-run: use cached real records where available")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--select", default="auto", help="oracle stage: 'auto' (bounds-driven) or 'all'")
    ap.add_argument("--goal", choices=["exclude", "pin"], default="exclude",
                    help="oracle stage: certify value != target (cheap) or pin the exact value")
    ap.add_argument("--target", default="*2")
    ap.add_argument("--resume", action="store_true", help="oracle stage: reuse previous results JSON")
    ap.add_argument("--per-target", type=int, default=25,
                    help="nodes stage: max new requests spent on one target position")
    ap.add_argument("--per-terminal", type=int, default=40,
                    help="oracle stage: max new requests spent on one 8-man terminal search")
    args = ap.parse_args(argv)
    sys.setrecursionlimit(100000)
    if args.stage == "roots":
        stage_roots(args)
    elif args.stage == "nodes":
        stage_nodes(args)
    else:
        from .oracle_value import stage_oracle
        stage_oracle(args, build)


if __name__ == "__main__":
    main()
