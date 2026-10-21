"""Real-chess results of embedded terminal (and node) positions, keyed by the
normal FEN, so that both passed-pawn trees and every script share them.

File: realchess/certify/results/realdb.jsonl, one JSON object per line:
  {"fen", "men", "result_stm": +1/0/-1 (side to move), "white": +1/0/-1,
   "how", "ext", "t"}
Only exact results are stored (lo == hi). Later lines win.

Resolution (resolve_fen):
  * <= 7 men: the Lichess category of the position (KB first, else 1 probe);
  * 8 men: realchess.search.Searcher with the tablebase at every capture
    (iterative deepening on the off-model ply budget `ext`);
  * 9+ men: the same search; captures into 8 men are searched in turn.
"""
from __future__ import annotations

import json
import os
import time

from realchess import movegen as mg

from . import infra

DB = os.path.join(infra.RESULTS, "realdb.jsonl")


def load(path: str = DB) -> dict:
    out = {}
    try:
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    r = json.loads(line)
                    out[r["fen"]] = r
    except FileNotFoundError:
        pass
    return out


def append(rows, path: str = DB):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")


def white_view(pos: mg.Position, v: int) -> int:
    return v if pos.stm == mg.WHITE else -v


def make_row(pos, iv, how, ext=None):
    v = iv[0]
    return {"fen": mg.normal_fen(pos), "men": pos.men(), "result_stm": v, "white": white_view(pos, v),
            "how": how, "ext": ext, "t": time.time()}
