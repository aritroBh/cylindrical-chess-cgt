"""Text prompts for LLM evaluation on ChessSums, and answer extraction.

Tasks
    outcome   one item per instance: answer L, R, N or P
    move      one item per (instance, side to move) that HAS a winning move:
              answer a winning move such as e2-e4 or d4xe5
    value     one item per instance: answer the canonical CGT value

Print a few prompts:
    PYTHONPATH=. .venv/bin/python -m bench.prompts --split test --task move --limit 2
Write a prompt file (one JSON object per item, with the item key used by score.py):
    PYTHONPATH=. .venv/bin/python -m bench.prompts --split test --task value --write /tmp/items.jsonl
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from . import board as bd

DATA = Path(__file__).resolve().parent / "data"
TASKS = ("outcome", "move", "value")


def load(path) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def geometry(row) -> bd.Geometry:
    return bd.Geometry(row["board"]["files"], row["board"]["cylinder"])


def squares(row):
    w = frozenset(bd.parse_sq(s) for s in row["white"])
    b = frozenset(bd.parse_sq(s) for s in row["black"])
    return w, b


def rules_text(row) -> str:
    W = row["board"]["files"]
    last = bd.FILES[W - 1]
    cyl = row["board"]["cylinder"]
    geo = (f"a board with {W} files (a-{last}) and 8 ranks"
           + (f". The board is a CYLINDER: files a and {last} are adjacent, so pawns on them attack each other"
              f" across that edge (for example a White pawn on {last}4 attacks a5, and a White pawn on a4 attacks {last}5)"
              if cyl else ". The board is flat: files a and " + last + " are edges"))
    return (
        f"This is a pawn-only game on {geo}. White pawns (P) move up the board and Black pawns (p) move down. "
        "There are no kings or other pieces.\n"
        "Rules:\n"
        "- A pawn moves one square straight forward to an empty square, or two squares from its starting rank "
        "(rank 2 for White, rank 7 for Black) if both squares are empty. It captures one square diagonally forward. "
        "En passant is legal but can never occur in these positions.\n"
        "- A pawn is passed if no enemy pawn is ahead of it on its own file or on an adjacent file"
        + (" (adjacency wraps around the cylinder)" if cyl else "") + ". As soon as exactly one side has a "
        "passed pawn, that side wins at once.\n"
        "- A player who has no legal move on their turn loses.\n"
        "- (A move that gives both sides a passed pawn at once cannot change any answer in these positions.)\n"
    )


def board_text(row) -> str:
    w, b = squares(row)
    geo = geometry(row)
    return (bd.diagram(geo, w, b) + "\n"
            f"White pawns: {' '.join(row['white'])}\nBlack pawns: {' '.join(row['black'])}\n")


def task_text(task, side=None) -> str:
    if task == "outcome":
        return ("Question: who wins with perfect play? Answer L if White wins whoever moves first, R if Black wins "
                "whoever moves first, N if the player to move wins (whoever that is), P if the player to move loses "
                "(whoever that is). Put one letter inside <answer></answer>.")
    if task == "move":
        who = "White" if side == "W" else "Black"
        return (f"Question: {who} to move and win. Give one winning move as from-square and to-square, "
                "with '-' for a step and 'x' for a capture, e.g. <answer>e2-e4</answer> or <answer>d4xe5</answer>.")
    if task == "value":
        return ("Question: give the exact value of this position as a combinatorial game (Conway's theory, normal "
                "play, White = Left, Black = Right). Count a position in which exactly one side has a passed pawn "
                "as a huge number in that side's favour; such numbers never appear in the answers here. Give the "
                "canonical form in standard notation, for example "
                "0, 2, -3/2, *, *2, 1/2*, ↑, ⇑*, ±1, 3/2±1/2, {2 | 1/2}, {0, * | -1}. "
                "ASCII is fine: ^ for ↑, v for ↓, +- for ±. Put the value inside <answer></answer>.")
    raise ValueError(task)


def render(row, task, side=None) -> str:
    return rules_text(row) + "\nPosition (rank 8 at the top):\n" + board_text(row) + "\n" + task_text(task, side)


def items(rows, task):
    """Yield (item_key, row, side) for a task. Move items exist only for a
    side that has at least one winning move."""
    for r in rows:
        if task == "move":
            for side in "WB":
                if r["winning_moves"][side]:
                    yield f"{r['id']}:move:{side}", r, side
        else:
            yield f"{r['id']}:{task}", r, None


_ANS = re.compile(r"<answer>(.*?)</answer>", re.S | re.I)


def extract(text: str) -> str | None:
    """Last <answer>...</answer> block; otherwise the last non-empty line."""
    if text is None:
        return None
    m = _ANS.findall(text)
    if m:
        return m[-1].strip()
    lines = [x.strip() for x in str(text).strip().splitlines() if x.strip()]
    return lines[-1] if lines else None


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="test")
    ap.add_argument("--task", choices=TASKS, default="outcome")
    ap.add_argument("--limit", type=int, default=2)
    ap.add_argument("--write", type=Path)
    a = ap.parse_args()
    rows = load(DATA / f"{a.split}.jsonl")
    its = list(items(rows, a.task))
    if a.write:
        with a.write.open("w") as f:
            for key, r, side in its:
                f.write(json.dumps({"item": key, "id": r["id"], "task": a.task, "side": side,
                                    "prompt": render(r, a.task, side)}, ensure_ascii=False) + "\n")
        print(f"wrote {len(its)} items to {a.write}")
    else:
        for key, r, side in its[: a.limit]:
            print(f"===== {key}\n{render(r, a.task, side)}\n")
