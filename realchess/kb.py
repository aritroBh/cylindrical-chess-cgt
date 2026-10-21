"""Offline knowledge base built from cached Lichess tablebase records.

Every cached record of a position X (a probe of X) gives
  * the category of X itself for the side to move (unless 'unknown'), and
  * the category of every child X+m, for the side to move AFTER m.
So one record answers its own position and each of its children. This module
indexes every record of one or more cache directories under the normal FEN
of every answered position (realchess.movegen.normal_fen), and keeps the
provenance (which record, root or which move) of each answer.

Nothing here touches the network. Cache directories other than the primary
realchess/cache are read-only inputs (records fetched by other workstreams
through the same probe client, each under its own request ledger).

    PYTHONPATH=. .venv/bin/python -m realchess.kb            # statistics
"""
from __future__ import annotations

import glob
import json
import os
from collections import Counter

from . import movegen as mg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PRIMARY = os.path.join(HERE, "cache")
# Read-only caches written by other workstreams with the same client (same key
# scheme: sha256 of the normal FEN). Only records whose stored "fen" hashes to
# their file name are used.
EXTRA = [os.path.join(ROOT, "engine", "suite", "tbcache")] + sorted(
    glob.glob(os.path.join(ROOT, "verify", "engines", "*", "tbcache*")))

SPECIAL = ("cursed-win", "blessed-loss", "maybe-win", "maybe-loss")


class KB:
    def __init__(self, dirs=None):
        self.dirs = [PRIMARY] + EXTRA if dirs is None else list(dirs)
        self.records: dict[str, dict] = {}
        self.record_dir: dict[str, str] = {}
        self.cat: dict[str, tuple] = {}       # fen -> (category, provenance)
        self.conflicts: list = []
        self.special: list = []
        self._load()

    def _load(self):
        import hashlib
        for d in self.dirs:
            for p in sorted(glob.glob(os.path.join(d, "*", "*.json"))):
                try:
                    rec = json.load(open(p))
                except (json.JSONDecodeError, OSError):
                    continue
                fen = rec.get("fen")
                if not fen or hashlib.sha256(fen.encode()).hexdigest() + ".json" != os.path.basename(p):
                    continue
                if rec.get("status") != 200 or not rec.get("data"):
                    continue
                if fen in self.records:
                    continue
                self.records[fen] = rec
                self.record_dir[fen] = d
        for fen, rec in self.records.items():
            self._index(fen, rec)

    def _put(self, fen, cat, prov):
        if cat is None or cat == "unknown":
            return
        if cat in SPECIAL:
            self.special.append((fen, cat, prov))
        old = self.cat.get(fen)
        if old is None:
            self.cat[fen] = (cat, prov)
        elif old[0] != cat:
            self.conflicts.append((fen, old, (cat, prov)))

    def _index(self, fen, rec):
        d = rec["data"]
        self._put(fen, d.get("category"), ("root", fen))
        par = mg.parse_fen(fen)
        cats = {m["uci"]: m.get("category") for m in d.get("moves", [])}
        for m in mg.legal_moves(par):
            c = cats.get(m.uci())
            if c in (None, "unknown"):
                continue
            self._put(mg.normal_fen(mg.make(par, m)), c, ("move", fen, m.uci()))

    # ------------------------------------------------------------ queries
    def category(self, fen_or_pos):
        """Category for the side to move, or None."""
        f = mg.normal_fen(fen_or_pos)
        hit = self.cat.get(f)
        return hit[0] if hit else None

    def provenance(self, fen_or_pos):
        hit = self.cat.get(mg.normal_fen(fen_or_pos))
        return hit[1] if hit else None

    def stats(self):
        by_dir = Counter(os.path.relpath(self.record_dir[f], ROOT) for f in self.records)
        men = Counter(mg.parse_fen(f).men() for f in self.cat)
        return {"records": len(self.records), "records_by_dir": dict(by_dir),
                "answered_positions": len(self.cat),
                "answered_by_men": dict(sorted(men.items())),
                "categories": dict(Counter(c for c, _ in self.cat.values())),
                "special_50_move_categories": len(self.special),
                "conflicts": len(self.conflicts)}


_DEFAULT = None


def default_kb() -> KB:
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = KB()
    return _DEFAULT


if __name__ == "__main__":
    k = KB()
    print(json.dumps(k.stats(), indent=1))
    for c in k.conflicts[:20]:
        print("CONFLICT", c)
