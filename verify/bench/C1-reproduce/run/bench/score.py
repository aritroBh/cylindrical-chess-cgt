"""Score predictions on ChessSums.

Prediction file: JSON lines, one per item, with
    {"item": "<id>:outcome"}            or {"id": ..., "task": "outcome"}
    {"item": "<id>:move:W", ...}        or {"id": ..., "task": "move", "side": "W"}
    {"item": "<id>:value", ...}         or {"id": ..., "task": "value"}
and the model output in "answer" (raw text is fine: the last <answer>...</answer>
block is used if present, else the last line).

    PYTHONPATH=. .venv/bin/python -m bench.score --gold bench/data/test.jsonl --pred preds.jsonl
    PYTHONPATH=. .venv/bin/python -m bench.score --gold bench/data/test.jsonl --baseline random-legal

Metrics (missing predictions count as wrong):
    outcome  accuracy of the class letter (L/R/N/P; words like "first player" accepted)
    move     fraction of items whose answer is a WINNING move; also the legal-move rate and
             random_legal_expected = mean probability that a uniformly random legal move
             wins (often about 0.5, so read move accuracy against it, and use the
             "move: chance<=1/4" and "move: unique winning move" rows)
    value    fraction whose answer parses to the same canonical game as the gold value
             (so "1/2 + *", "1/2*" and "{1/2|1/2}" all count); also exact-string match.
             Outcome P <=> value 0, so the constant answer "0" scores 0.25 on balanced
             splits: read the "value!=0" row
Breakdowns: by k, board type (flat/cylinder), 8-file or wider, held-out components,
value kind.
"""
from __future__ import annotations

import argparse
import json
import random
import re
from collections import defaultdict
from pathlib import Path

from . import board as bd
from . import cgtfmt
from .prompts import extract, items, load, squares, geometry

_WORDS = {
    "l": "L", "left": "L", "r": "R", "right": "R",
    "n": "N", "next": "N", "first": "N", "first player": "N", "fuzzy": "N",
    "p": "P", "previous": "P", "second": "P", "second player": "P",
}


def norm_outcome(ans):
    if ans is None:
        return None
    t = re.sub(r"[^a-z ]", " ", str(ans).lower()).strip()
    t = re.sub(r"\s+", " ", t)
    if t in _WORDS:
        return _WORDS[t]
    for w in ("first player", "second player"):
        if w in t:
            return _WORDS[w]
    toks = t.split()
    if len(toks) == 1 and toks[0] in _WORDS:
        return _WORDS[toks[0]]
    return None


def legal_list(row, side):
    w, b = squares(row)
    return bd.gen_moves(geometry(row), w, b, side)


def judge(row, task, side, answer_text):
    """Return a dict of booleans for one item."""
    ans = extract(answer_text) if answer_text is not None else None
    if task == "outcome":
        return {"correct": norm_outcome(ans) == row["outcome"]}
    if task == "move":
        name = bd.resolve_move(ans, legal_list(row, side)) if ans else None
        return {"correct": name is not None and name in row["winning_moves"][side], "legal": name is not None}
    if task == "value":
        exact = ans is not None and ans.replace(" ", "") in (row["value"].replace(" ", ""), row["value_ascii"].replace(" ", ""))
        return {"correct": ans is not None and cgtfmt.same_value(ans, row["value_ascii"]), "exact_string": exact}
    raise ValueError(task)


def chance(row, side):
    """Probability that a uniformly random legal move wins."""
    return len(row["winning_moves"][side]) / len(row["legal_moves"][side])


def groups(row, task, side):
    yield "all"
    yield f"k={row['k']}"
    yield "cylinder" if row["board"]["cylinder"] else "flat"
    yield "8-file" if row["fits8"] else "wide"
    yield "heldout:" + ("+".join(row["heldout"]) if row["heldout"] else "none")
    yield f"kind={row['kind']}"
    yield f"outcome={row['outcome']}"
    if task == "value" and row["outcome"] != "P":
        yield "value!=0"
    if task == "move":
        c = chance(row, side)
        yield "move: chance<=1/4" if c <= 0.25 else "move: chance>1/4"
        if len(row["winning_moves"][side]) == 1:
            yield "move: unique winning move"


def baseline_answer(row, task, side, kind, rng):
    if kind == "constant":
        if task == "move":
            return row["legal_moves"][side][0] if row["legal_moves"][side] else None
        return {"outcome": "N", "value": "0"}[task]
    if kind in ("random-legal", "first-legal"):
        if task == "outcome":
            return rng.choice("LRNP")
        if task == "value":
            return "0"
        lm = row["legal_moves"][side]
        if not lm:
            return None
        return rng.choice(lm) if kind == "random-legal" else lm[0]
    raise ValueError(kind)


def score(gold_rows, preds: dict, tasks=("outcome", "move", "value")):
    res = {}
    for task in tasks:
        agg = defaultdict(lambda: defaultdict(int))
        for key, row, side in items(gold_rows, task):
            p = preds.get(key)
            j = judge(row, task, side, p)
            for g in groups(row, task, side):
                agg[g]["n"] += 1
                agg[g]["answered"] += p is not None
                for m, v in j.items():
                    agg[g][m] += bool(v)
                if task == "move":
                    agg[g]["random_legal_expected"] += chance(row, side)
        res[task] = {g: dict(v) for g, v in agg.items()}
    return res


def load_preds(path):
    preds = {}
    for r in load(path):
        key = r.get("item")
        if key is None:
            t = r["task"]
            key = f"{r['id']}:move:{r['side']}" if t == "move" else f"{r['id']}:{t}"
        preds[key] = r.get("answer", r.get("prediction"))
    return preds


def table(res) -> str:
    lines = []
    for task, by in res.items():
        metrics = [m for m in next(iter(by.values())) if m not in ("n", "answered")]
        lines.append(f"\n### {task}\n")
        lines.append("| group | n | " + " | ".join(metrics) + " |")
        lines.append("|---|---|" + "---|" * len(metrics))
        order = sorted(by, key=lambda g: (g != "all", g))
        for g in order:
            d = by[g]
            lines.append(f"| {g} | {d['n']} | " + " | ".join(f"{d.get(m, 0) / d['n']:.3f}" for m in metrics) + " |")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gold", type=Path, required=True)
    ap.add_argument("--pred", type=Path)
    ap.add_argument("--baseline", choices=["constant", "random-legal", "first-legal"])
    ap.add_argument("--tasks", default="outcome,move,value")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--json", type=Path, help="also write the full result as JSON")
    a = ap.parse_args(argv)
    gold = load(a.gold)
    tasks = tuple(a.tasks.split(","))
    if a.baseline:
        rng = random.Random(a.seed)
        preds = {key: baseline_answer(r, t, s, a.baseline, rng) for t in tasks for key, r, s in items(gold, t)}
    elif a.pred:
        preds = load_preds(a.pred)
    else:
        ap.error("give --pred or --baseline")
    res = score(gold, preds, tasks)
    print(table(res))
    if a.json:
        a.json.write_text(json.dumps(res, indent=1) + "\n")


if __name__ == "__main__":
    main()
