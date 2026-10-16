"""Cross-check the ChessSums ground truth.

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.verify            # full run
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.verify --quick    # small samples

Checks (results in bench/results/verify_report.md and verify_summary.json):
 A. Components vs crosscheck/minimax.py (independent whole-board solver written
    by Codex; it does not import cylcgt; real-chess e.p. that expires after one ply):
    A1 outcome class of every component alone (e.p. on and off);
    A2 value equalities: component c next to a component r with value -v(c) taken
       from a DIFFERENT symmetry orbit must be a second-player win (P), which
       independently confirms v(c) = v(c') for the c' = -r class;
    A3 random pairs: outcome of c + r equals the CGT outcome of v(c) + v(r).
 B. Instances re-solved by cylcgt on the whole board (pawns.value does its
    own decomposition, including wrap-around groups): the value (e.p. on and
    off), and for every legal move the win/loss status. All rows of val, test
    and test_heldout plus a random 3,000 train rows (about 0.13 s each).
    Same implementation, different code path. Race rules "mover" and
    "opponent" re-checked on 250 rows per split.
 C. Instances vs crosscheck/minimax.py on samples: outcome class, and the full
    winning-move sets on a smaller sample. Per-instance time limit.
 D. EVERY instance vs bench/ab.c (alpha-beta + transposition table, own move
    generator, no cylcgt; identical results and node counts to the Python
    solver in bench/baseline.py, see bench/tests): outcome class, with a
    per-search time cap.
"""
from __future__ import annotations

import argparse
from multiprocessing import get_context
import json
import random
import signal
import time
from collections import Counter
from pathlib import Path

from crosscheck import minimax as mm
from cylcgt import cgt, pawns

from . import board as bd
from . import cgtfmt
from .baseline import c_solve
from .prompts import load

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RES = ROOT / "results"


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout


signal.signal(signal.SIGALRM, _alarm)


def with_timeout(seconds, fn, *args):
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        return fn(*args)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


def sqs(names):
    return frozenset(bd.parse_sq(s) for s in names)


# ---------------------------------------------------------------------------
# A. components
# ---------------------------------------------------------------------------

def check_components(comps, rng, n_random_pairs):
    out = Counter()
    bad = []
    for c in comps:
        w, b = bd.parse_pos_text(c["position"])
        for ep in (True, False):
            oc = mm.outcome_class(mm.Board(c["width"], 8, False, ep), mm.Position(w, b))
            mm._winner.cache_clear()
            out[f"A1 single outcome, ep={'on' if ep else 'off'} (agree)"] += oc == c["outcome"]
            out[f"A1 single outcome, ep={'on' if ep else 'off'} (total)"] += 1
            if oc != c["outcome"]:
                bad.append(("A1", c["comp_id"], ep, oc, c["outcome"]))
    by_val = {}
    for c in comps:
        by_val.setdefault(c["value_ascii"], []).append(c)

    def pair(c, r):
        w1, b1 = bd.parse_pos_text(c["position"])
        w2, b2 = bd.parse_pos_text(r["position"])
        off = c["width"] + 1
        W = off + r["width"]
        w = w1 | {(f + off, x) for f, x in w2}
        b = b1 | {(f + off, x) for f, x in b2}
        oc = mm.outcome_class(mm.Board(W, 8, False, True), mm.Position(frozenset(w), frozenset(b)))
        mm._winner.cache_clear()
        return oc

    for c in comps:
        g = cgtfmt.parse(c["value_ascii"])
        neg = cgtfmt.fmt(cgt.neg(g), ascii=True)
        cands = [r for r in by_val.get(neg, []) if r["orbit"] != c["orbit"]]
        same_orbit = False
        if not cands:
            cands = [r for r in by_val.get(neg, [])]
            same_orbit = True
        r = rng.choice(cands)
        oc = pair(c, r)
        tag = "A2 c + r(-v) is P, r from same orbit only" if same_orbit else "A2 c + r(-v) is P, r from another orbit"
        out[tag + " (agree)"] += oc == "P"
        out[tag + " (total)"] += 1
        if oc != "P":
            bad.append(("A2", c["comp_id"], r["comp_id"], oc))
    for _ in range(n_random_pairs):
        c, r = rng.choice(comps), rng.choice(comps)
        want = cgt.outcome(cgt.add(cgtfmt.parse(c["value_ascii"]), cgtfmt.parse(r["value_ascii"])))
        oc = pair(c, r)
        out["A3 random pair outcome (agree)"] += oc == want
        out["A3 random pair outcome (total)"] += 1
        if oc != want:
            bad.append(("A3", c["comp_id"], r["comp_id"], oc, want))
    return out, bad


# ---------------------------------------------------------------------------
# B. cylcgt whole-board recomputation
# ---------------------------------------------------------------------------

def child_positions(board, pos, side, geo):
    """(move name, pawns.Pos child) using cylcgt's own generator for the child
    (with its e.p. tuple) and bench.board for the name."""
    kids = pawns.moves(board, pos, side)
    by_sets = {(k.white, k.black): k for k in kids}
    named = bd.gen_moves(geo, pos.white, pos.black, side)
    assert len(named) == len(kids), "move generators disagree on the number of moves"
    return [(n, by_sets[(nw, nb)]) for n, fr, to, nw, nb in named]


def check_cylcgt(row, rules=("count",)):
    W, cyl = row["board"]["files"], row["board"]["cylinder"]
    pos = pawns.Pos(sqs(row["white"]), sqs(row["black"]))
    gold = cgtfmt.parse(row["value_ascii"])
    res = {}
    assert cgtfmt.parse(row["value"]) is gold, "unicode and ASCII value strings differ"
    assert cgtfmt.fmt(gold) == row["value"], "value string does not round-trip"
    for rule in rules:
        if pawns.RACE_RULE != rule:
            pawns.RACE_RULE = rule
            pawns._value.cache_clear()
        ok = True
        for ep in (True, False):
            board = pawns.Board(W, 8, cyl, ep)
            ok &= pawns.value(board, pos) is gold
        board = pawns.Board(W, 8, cyl, True)
        geo = bd.Geometry(W, cyl)
        for side in "WB":
            wins = []
            for name, child in child_positions(board, pos, side, geo):
                v = pawns.value(board, child)
                if (cgt.le(cgt.ZERO, v) if side == "W" else cgt.le(v, cgt.ZERO)):
                    wins.append(name)
            ok &= sorted(wins) == row["winning_moves"][side]
        res[rule] = ok
    return res


# ---------------------------------------------------------------------------
# C, D. independent searches
# ---------------------------------------------------------------------------

def mm_outcome(row):
    board = mm.Board(row["board"]["files"], 8, row["board"]["cylinder"], True)
    pos = mm.Position(sqs(row["white"]), sqs(row["black"]))
    return mm.outcome_class(board, pos)


def mm_winning(row):
    board = mm.Board(row["board"]["files"], 8, row["board"]["cylinder"], True)
    pos = mm.Position(sqs(row["white"]), sqs(row["black"]))
    geo = bd.Geometry(row["board"]["files"], row["board"]["cylinder"])
    res = {}
    for side in "WB":
        other = "B" if side == "W" else "W"
        kids = mm.legal_moves(board, pos, side)
        by_sets = {(k.white, k.black): k for k in kids}
        wins = []
        for name, fr, to, nw, nb in bd.gen_moves(geo, pos.white, pos.black, side):
            child = by_sets[(nw, nb)]
            r = mm._winner_after_move(board, child, side)
            if r is None:
                r = mm.winner(board, child, other)
            if r == side:
                wins.append(name)
        res[side] = sorted(wins)
    return res


def ab_outcomes(rows, time_cap):
    """Outcome classes from bench/ab.c (alpha-beta + TT); None where a search hit the cap."""
    jobs = []
    for r in rows:
        w, b = sqs(r["white"]), sqs(r["black"])
        for side in (True, False):
            jobs.append((r["board"]["files"], r["board"]["cylinder"], w, b, side, True, 0, time_cap))
    res = c_solve(jobs)
    out = []
    for i in range(len(rows)):
        (vw, _, _), (vb, _, _) = res[2 * i], res[2 * i + 1]
        if vw == 0 or vb == 0:
            out.append(None)
            continue
        a, c = vw == 1, vb == 1
        out.append("L" if a and not c else "R" if c and not a else "N" if a else "P")
    return out


def _init_worker():
    signal.signal(signal.SIGALRM, _alarm)


def b_task(arg):
    split, r, rules = arg
    return split, r["id"], check_cylcgt(r, rules)


def c_task(arg):
    split, r, timeout, moves = arg
    out = {"split": split, "row": r}
    try:
        out["outcome"] = with_timeout(timeout, mm_outcome, r)
        if moves:
            out["moves"] = with_timeout(timeout, mm_winning, r)
    except Timeout:
        out["timeout"] = True
    finally:
        mm._winner.cache_clear()
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--seed", type=int, default=99)
    ap.add_argument("--jobs", type=int, default=4, help="worker processes for checks B and C")
    ap.add_argument("--b-train", type=int, default=3000, help="train rows re-solved in check B (all rows of the other splits)")
    ap.add_argument("--timeout", type=float, default=10.0, help="seconds per instance for crosscheck searches")
    ap.add_argument("--ab-time", type=float, default=3.0, help="CPU seconds per ab.c search (check D)")
    a = ap.parse_args(argv)
    rng = random.Random(a.seed)
    t0 = time.time()
    summary, bad = Counter(), []
    comps = load(DATA / "components.jsonl")
    ctx = get_context("spawn")

    print("A. components vs crosscheck ...", flush=True)
    s, b = check_components(comps if not a.quick else comps[:60], rng, 300 if not a.quick else 30)
    summary.update(s)
    bad += b
    print(f"   {dict(s)}  [{time.time() - t0:.0f}s]", flush=True)

    splits = ["train", "val", "test", "test_heldout"]
    rows = {sp: load(DATA / f"{sp}.jsonl") for sp in splits}

    print("B. cylcgt whole-board recomputation ...", flush=True)
    tasks = []
    for sp in splits:
        rs = rows[sp]
        if sp == "train":
            rs = rng.sample(rs, min(a.b_train, len(rs)))
        if a.quick:
            rs = rs[:100]
        triple = set(rng.sample(range(len(rs)), min(len(rs), 250 if not a.quick else 10)))
        tasks += [(sp, r, ("count", "mover", "opponent") if i in triple else ("count",)) for i, r in enumerate(rs)]
    with ctx.Pool(a.jobs, initializer=_init_worker) as pool:
        for sp, rid, res in pool.imap_unordered(b_task, tasks, chunksize=25):
            for rule, ok in res.items():
                summary[f"B {sp} rule={rule} (agree)"] += ok
                summary[f"B {sp} rule={rule} (total)"] += 1
                if not ok:
                    bad.append(("B", rid, rule))
    print(f"   done [{time.time() - t0:.0f}s]", flush=True)

    print("C. instances vs crosscheck ...", flush=True)
    tasks = []
    for sp in splits:
        rs = rows[sp]
        eight = [r for r in rs if r["fits8"]]
        wide = [r for r in rs if not r["fits8"]]
        n8 = {"train": 600, "val": len(eight), "test": len(eight), "test_heldout": len(eight)}[sp]
        nw = {"train": 200, "val": 200, "test": 60, "test_heldout": 200}[sp]
        if a.quick:
            n8, nw = min(n8, 20), min(nw, 10)
        sample = rng.sample(eight, min(n8, len(eight))) + rng.sample(wide, min(nw, len(wide)))
        mw = set(rng.sample(range(len(sample)), min(len(sample), 150 if not a.quick else 10)))
        tasks += [(sp, r, a.timeout, i in mw) for i, r in enumerate(sample)]
    with ctx.Pool(a.jobs, initializer=_init_worker) as pool:
        for out in pool.imap_unordered(c_task, tasks, chunksize=10):
            r, sp = out["row"], out["split"]
            grp = f"{sp} {'8-file' if r['fits8'] else 'wide'} k={r['k']}"
            if "outcome" in out:
                summary[f"C outcome {grp} (agree)"] += out["outcome"] == r["outcome"]
                summary[f"C outcome {grp} (total)"] += 1
                if out["outcome"] != r["outcome"]:
                    bad.append(("C", r["id"], out["outcome"], r["outcome"]))
            if "moves" in out:
                ok = out["moves"] == r["winning_moves"]
                summary[f"C winning moves {sp} (agree)"] += ok
                summary[f"C winning moves {sp} (total)"] += 1
                if not ok:
                    bad.append(("C-moves", r["id"], out["moves"], r["winning_moves"]))
            if out.get("timeout"):
                summary[f"C timeout {grp}"] += 1
    print(f"   done [{time.time() - t0:.0f}s]", flush=True)

    print("D. every instance vs ab.c (alpha-beta + TT) ...", flush=True)
    for sp in splits:
        rs = rows[sp] if not a.quick else rows[sp][:100]
        for i in range(0, len(rs), 500):
            chunk = rs[i:i + 500]
            for r, oc in zip(chunk, ab_outcomes(chunk, a.ab_time)):
                grp = f"{sp} k={r['k']}"
                if oc is None:
                    summary[f"D time cap {grp}"] += 1
                    continue
                summary[f"D outcome {grp} (agree)"] += oc == r["outcome"]
                summary[f"D outcome {grp} (total)"] += 1
                if oc != r["outcome"]:
                    bad.append(("D", r["id"], oc, r["outcome"]))
        print(f"   {sp} done [{time.time() - t0:.0f}s]", flush=True)

    RES.mkdir(exist_ok=True)
    name = "verify_quick" if a.quick else "verify"
    meta = {"seed": a.seed, "b_train": a.b_train, "timeout": a.timeout, "ab_time": a.ab_time}
    (RES / f"{name}_summary.json").write_text(json.dumps({"meta": meta, "summary": dict(sorted(summary.items())),
                                                           "disagreements": bad[:200],
                                                           "n_disagreements": len(bad)}, indent=1) + "\n")
    (RES / f"{name}_report.md").write_text(report(summary, bad, time.time() - t0))
    print(report(summary, bad, time.time() - t0))


def report(summary, bad, secs):
    lines = ["# ChessSums ground-truth verification", "",
             "Generated by `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.verify`.", "",
             "| check | agree | total |", "|---|---|---|"]
    keys = sorted({k.rsplit(" (", 1)[0] for k in summary if k.endswith("(agree)")})
    for k in keys:
        lines.append(f"| {k} | {summary[k + ' (agree)']} | {summary[k + ' (total)']} |")
    others = sorted(k for k in summary if not k.endswith("(agree)") and not k.endswith("(total)"))
    if others:
        lines += ["", "| not finished | count |", "|---|---|"]
        lines += [f"| {k} | {summary[k]} |" for k in others]
    lines += ["", f"Disagreements: {len(bad)}."]
    for x in bad[:30]:
        lines.append(f"- `{x}`")
    lines += ["", f"Run time {secs:.0f} s."]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
