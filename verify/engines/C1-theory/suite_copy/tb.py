"""Thin wrapper around realchess/probe.py (read-only use of that module).

* First looks in the shared cache realchess/cache WITHOUT writing to it
  (offline Prober), so positions other workstreams already fetched cost nothing.
* Otherwise fetches through our own Prober, whose cache and ledger live inside
  engine/suite/ (this workstream may only write inside engine/). That Prober
  enforces >= 1.05 s between requests, a 60 s back-off on HTTP 429 and a hard
  cap of CAP HTTP attempts recorded in engine/suite/tb_ledger.jsonl.

Category conventions (Lichess): the root category is for the side to move; a
move's category is for the side to move AFTER that move.
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from realchess import probe as _probe  # noqa: E402

CAP = 300
LEDGER = os.path.join(HERE, "tb_ledger.jsonl")
CACHE = os.path.join(HERE, "tbcache")
SHARED_CACHE = os.path.join(ROOT, "realchess", "cache")

# Another workstream probes concurrently from this machine with its own lock,
# and we got HTTP 429 at 1.05 s spacing; space our requests further apart so the
# machine total stays near 1 request per second (module attribute, set at runtime;
# realchess/probe.py itself is not modified).
_probe.MIN_INTERVAL = 5.0

_shared = _probe.Prober(0, ledger=LEDGER, cache_dir=SHARED_CACHE, tag="engine-ro", offline=True)
_own = _probe.Prober(CAP, ledger=LEDGER, cache_dir=CACHE, tag="engine-suite", verbose=True)

# result for the MOVER, given the category of the side to move after the move
MOVER_RESULT = {"loss": "win", "blessed-loss": "cursed-win", "draw": "draw",
                "cursed-win": "blessed-loss", "win": "loss",
                "maybe-loss": "maybe-win", "maybe-win": "maybe-loss", "unknown": "unknown", None: None}


def lookup(fen: str, allow_network: bool = True) -> dict | None:
    for pr in (_shared, _own):
        rec = pr.cached(fen)
        if rec is not None:
            return rec
    if not allow_network:
        return None
    return _own.probe(fen)


def requests_used() -> int:
    return _own.ledger_count()


def summarize(rec: dict) -> dict:
    """{'root': cat, 'moves': {uci: (san, mover_result, dtz, dtm)}}"""
    d = rec.get("data") or {}
    moves = {}
    for m in d.get("moves", []):
        moves[m["uci"]] = (m.get("san"), MOVER_RESULT.get(m.get("category"), m.get("category")),
                           m.get("dtz"), m.get("dtm"))
    return {"root": d.get("category"), "dtz": d.get("dtz"), "dtm": d.get("dtm"), "moves": moves,
            "status": rec.get("status")}
