"""DRAFT reward functions for GRPO / RLVR fine-tuning on ChessSums.

Nothing here calls a model or an external service; the rewards are computed
exactly from the gold record (cylcgt ground truth) and the board rules.

Plain use:
    from bench.reward import reward
    r = reward(completion_text, row, task="move", side="W")   # -> float

TRL-style use (GRPOTrainer(reward_funcs=[chesssums_reward], ...)): the
dataset needs the columns `gold` (the JSON record, as a dict or a JSON string),
`task` and `side` (None unless task == "move"); TRL passes dataset columns to
reward functions as keyword lists, one entry per completion.

Reward design (all in [-0.5, 1.1]; see WEIGHTS):
    format   +0.1 if the completion contains exactly one <answer>...</answer>
    outcome  +1 if the class letter is right, else 0
    move     -0.5 if the answer is not a legal move (unparseable, illegal,
             wrong side), +0.1 if legal but losing, +1 if winning
    value    +1 if the answer parses to the same canonical game (exact CGT
             equality), else 0; with partial=True, +0.2 if it is a different
             game but has the right outcome class (a denser but gameable
             signal, off by default)
The value parser enforces size limits (bench.cgtfmt), so a degenerate answer
like "*999999" is a parse failure, not a slow reward call.
"""
from __future__ import annotations

import json

from cylcgt import cgt

from . import board as bd
from . import cgtfmt
from .prompts import _ANS, extract, geometry, squares
from .score import norm_outcome

WEIGHTS = {
    "format": 0.1,
    "outcome": 1.0,
    "move_win": 1.0,
    "move_legal_losing": 0.1,
    "move_illegal": -0.5,
    "value": 1.0,
    "value_partial": 0.2,
}


def is_legal(row, side, answer) -> str | None:
    """Name of the legal move the answer denotes, or None."""
    w, b = squares(row)
    return bd.resolve_move(answer, bd.gen_moves(geometry(row), w, b, side)) if answer else None


def format_ok(text: str) -> bool:
    return isinstance(text, str) and len(_ANS.findall(text)) == 1


def reward(text: str, row: dict, task: str, side: str | None = None, partial: bool = False,
           weights: dict = WEIGHTS) -> float:
    ans = extract(text)
    r = weights["format"] if format_ok(text) else 0.0
    if task == "outcome":
        return r + (weights["outcome"] if norm_outcome(ans) == row["outcome"] else 0.0)
    if task == "move":
        name = is_legal(row, side, ans)
        if name is None:
            return r + weights["move_illegal"]
        return r + (weights["move_win"] if name in row["winning_moves"][side] else weights["move_legal_losing"])
    if task == "value":
        try:
            g = cgtfmt.parse(ans) if ans else None
        except (cgtfmt.ParseError, RecursionError, ValueError, ZeroDivisionError):
            g = None
        if g is None:
            return r
        gold = cgtfmt.parse(row["value_ascii"])
        if g is gold:
            return r + weights["value"]
        if partial and cgt.outcome(g) == row["outcome"]:
            return r + weights["value_partial"]
        return r
    raise ValueError(task)


def _text(c):
    # TRL passes either strings or chat-format lists of {"role", "content"}
    if isinstance(c, list):
        return "".join(m.get("content", "") for m in c if isinstance(m, dict))
    return c


def chesssums_reward(prompts=None, completions=None, gold=None, task=None, side=None, **kwargs):
    """TRL GRPO-compatible: returns one float per completion."""
    out = []
    n = len(completions)
    for i in range(n):
        g = gold[i]
        row = json.loads(g) if isinstance(g, str) else g
        t = task[i] if isinstance(task, (list, tuple)) else task
        s = side[i] if isinstance(side, (list, tuple)) else side
        out.append(reward(_text(completions[i]), row, t, s))
    return out


def legality_reward(prompts=None, completions=None, gold=None, side=None, **kwargs):
    """Separate 0/1 legality signal for move items (useful as a second reward_func)."""
    out = []
    for i, c in enumerate(completions):
        g = gold[i]
        row = json.loads(g) if isinstance(g, str) else g
        s = side[i] if isinstance(side, (list, tuple)) else side
        out.append(1.0 if is_legal(row, s, extract(_text(c))) else 0.0)
    return out
