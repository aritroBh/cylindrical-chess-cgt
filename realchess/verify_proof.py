"""Independent, offline check of a real-chess result, from cached probes only.

A deliberately simple AND/OR prover, sharing nothing with realchess/search.py
except the (Lichess-validated) move generator and the on-disk probe cache:

  win(pos):  some legal move leads to a child that is lost for the opponent;
  loss(pos): every legal move leads to a child that is won for the opponent
             (no legal move: checkmate = loss, stalemate = draw = not a loss);
  a child with <= 7 men is decided by a CACHED probe record only: the root
  category of the child itself, or the move category inside the record of
  the parent. Nothing is ever fetched.

It writes an explicit certificate: the chosen move at every 'win' node and all
moves at every 'loss' node, each leaf citing the cached record it used.

    PYTHONPATH=. .venv/bin/python -m realchess.verify_proof \
        "8/1p1p4/8/5Kp1/6Pk/8/P1P5/8 w - - 0 1" --claim win --depth 40 \
        --out realchess/results/cert_root_w.json
"""
from __future__ import annotations

import argparse
import json
import sys

from . import movegen as mg
from .probe import Prober

DECISIVE = {"win": "win", "loss": "loss", "cursed-win": "win", "blessed-loss": "loss"}


class Prover:
    def __init__(self, cache_dir=None, fifty=False, kb=None):
        kw = {"cache_dir": cache_dir} if cache_dir else {}
        self.pr = Prober(0, offline=True, **kw)
        self.kb = kb  # optional realchess.kb.KB: also read the imported (read-only) caches
        self.fifty = fifty  # if True, cursed-win/blessed-loss are NOT decisive
        self.memo = {}
        self.failed = {}

    def _cat(self, cat):
        if cat in ("win", "loss"):
            return cat
        if not self.fifty and cat in ("cursed-win", "blessed-loss"):
            return DECISIVE[cat]
        return None

    def leaf(self, parent, m, child):
        """'win'/'loss' for the side to move in child, from cached data, or None."""
        rec = self.pr.cached(mg.normal_fen(child))
        if rec and rec.get("data"):
            c = self._cat(rec["data"].get("category"))
            if c:
                return c, {"source": "root category", "fen": rec["fen"]}
        if self.kb is not None and child.men() <= 7:
            c = self._cat(self.kb.category(child))
            if c:
                prov = self.kb.provenance(child)
                return c, {"source": "kb " + prov[0], "fen": prov[1],
                           **({"uci": prov[2]} if len(prov) > 2 else {})}
        prec = self.pr.cached(mg.normal_fen(parent))
        if prec and prec.get("data"):
            for mv in prec["data"].get("moves", []):
                if mv["uci"] == m.uci():
                    c = self._cat(mv.get("category"))
                    if c:
                        return c, {"source": "move category in parent record",
                                   "fen": prec["fen"], "uci": m.uci()}
        return None, None

    def prove(self, pos, claim: str, depth: int):
        """Certificate dict if `claim` ('win'/'loss' for side to move) is proved."""
        key = (mg.normal_fen(pos), claim)
        if key in self.memo:
            return self.memo[key]
        if self.failed.get(key, -1) >= depth or depth <= 0:
            return None
        res = self._prove(pos, claim, depth)
        if res is None:
            self.failed[key] = depth
        else:
            self.memo[key] = res
        return res

    def _prove(self, pos, claim: str, depth: int):
        moves = mg.legal_moves(pos)
        moves.sort(key=lambda m: (not mg.is_capture(pos, m)))  # cheap leaves first
        fen = mg.normal_fen(pos)
        if not moves:
            return {"fen": fen, "claim": claim, "terminal": "checkmate"} \
                if (claim == "loss" and mg.in_check(pos)) else None
        want_child = "loss" if claim == "win" else "win"
        kids = []
        for m in moves:
            child = mg.make(pos, m)
            if child.men() <= 7:
                c, src = self.leaf(pos, m, child)
                sub = {"move": m.uci(), "leaf": src, "child_result": c} if c == want_child else None
            else:
                cert = self.prove(child, want_child, depth - 1)
                sub = {"move": m.uci(), "child": cert} if cert else None
            if claim == "win" and sub:
                return {"fen": fen, "claim": "win", "by": sub}
            if claim == "loss":
                if not sub:
                    return None
                kids.append(sub)
        if claim == "win":
            return None
        return {"fen": fen, "claim": "loss", "all_moves": kids}


def stats(cert):
    """(#internal nodes, #leaves, max depth, cited records)."""
    nodes, leaves, cited = 0, 0, set()

    def walk(c, d):
        nonlocal nodes, leaves
        if c is None:
            return d
        nodes += 1
        subs = [c["by"]] if "by" in c else c.get("all_moves", [])
        best = d
        for s in subs:
            if "leaf" in s:
                leaves += 1
                cited.add(s["leaf"]["fen"])
            else:
                best = max(best, walk(s["child"], d + 1))
        return best
    depth = walk(cert, 0)
    return {"nodes": nodes, "leaves": leaves, "max_depth": depth, "cited_records": len(cited)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fen")
    ap.add_argument("--claim", choices=["win", "loss"], required=True)
    ap.add_argument("--depth", type=int, default=40)
    ap.add_argument("--fifty", action="store_true", help="cursed-win/blessed-loss count as draws")
    ap.add_argument("--out")
    ap.add_argument("--kb", action="store_true", help="also use the imported read-only caches (realchess/kb.py)")
    a = ap.parse_args()
    sys.setrecursionlimit(100000)
    kb = None
    if a.kb:
        from .kb import default_kb
        kb = default_kb()
    P = Prover(fifty=a.fifty, kb=kb)
    cert = P.prove(mg.parse_fen(a.fen), a.claim, a.depth)
    ok = cert is not None
    info = {"fen": mg.normal_fen(a.fen), "claim": a.claim, "proved": ok, "fifty": a.fifty}
    if ok:
        info.update(stats(cert))
    print(json.dumps(info))
    if a.out:
        with open(a.out, "w") as fh:
            json.dump({"summary": info, "certificate": cert}, fh)


if __name__ == "__main__":
    main()
