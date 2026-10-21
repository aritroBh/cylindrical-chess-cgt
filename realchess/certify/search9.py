"""realchess.search.Searcher extended to positions with 9 or more men.

The base Searcher resolves every capture by probing the PARENT position: that
is right for an 8-man parent (Lichess returns the exact category of every
capture into 7 men) but useless for a 9-man parent (Lichess returns
'unknown' for everything, checked on 8/8/8/5Kp1/Ppp3Pk/P1P5/8/8 w). Here a
capture from a position with >= 9 men is searched like any other move, so it
reaches an 8-man node, which the base class resolves as usual (its captures
into 7 men from one probe of the 8-man node). Same interval semantics: the
returned (lo, hi) always bounds the true value for the side to move.
"""
from __future__ import annotations

from realchess import movegen as mg
from realchess.search import Searcher


class DeepSearcher(Searcher):
    """l8=True: an 8-man node is first answered by Lichess's own category of
    that position (one probe, or the knowledge base), which Lichess computes
    by looking ahead into the 7-man tables; only if that is 'unknown' is the
    node searched. Results that may depend on such categories are labelled
    by the caller."""
    l8 = False

    def search(self, pos, ext: int, alpha: int = -1, beta: int = 1):
        if pos.men() == 8 and self.l8:
            key = mg.normal_fen(pos)
            hit = self.tt.get(key)
            if hit is not None and hit[0] == hit[1]:
                return (hit[0], hit[1])
            cat = self.kb.category(pos) if self.kb is not None else None
            if cat is None:
                rec = self._rec(pos)
                cat = (rec.get("data") or {}).get("category")
                self._note(key, "root-l8", cat)
            if cat in ("win", "loss", "draw"):
                v = {"win": 1, "loss": -1, "draw": 0}[cat]
                self.tt[key] = (v, v, 10**9, True)
                return (v, v)
        if pos.men() <= 8:
            return super().search(pos, ext, alpha, beta)
        self.nodes += 1
        if self.nodes > self.max_nodes:
            raise RuntimeError("node limit")
        key = mg.normal_fen(pos)
        hit = self.tt.get(key)
        if hit is not None:
            lo, hi, e, done = hit
            if lo == hi or lo >= beta or hi <= alpha or (done and e >= ext):
                return (lo, hi)
        moves = mg.legal_moves(pos)
        if not moves:
            iv = (-1, -1) if mg.in_check(pos) else (0, 0)
            self.tt[key] = (iv[0], iv[1], 10**9, True)
            return iv
        reg = self.region(pos)
        if reg == "off" and ext <= 0:
            self.unresolved_leaves.add(key)
            iv = (-1, 1)
            if hit is not None:
                iv = (max(iv[0], hit[0]), min(iv[1], hit[1]))
            return iv
        sub_ext = ext - 1 if reg == "off" else ext
        if self.order_hint:
            moves = self.order_hint(pos, moves)
        best_lo, best_hi = -1, -1
        complete = True
        for i, m in enumerate(moves):
            child = mg.make(pos, m)
            clo, chi = self.search(child, sub_ext, -beta, -max(alpha, best_lo))
            vlo, vhi = -chi, -clo
            best_lo = max(best_lo, vlo)
            best_hi = max(best_hi, vhi)
            if best_lo >= beta or best_lo == 1:
                complete = (i == len(moves) - 1)
                break
        lo, hi = best_lo, (best_hi if complete else 1)
        if best_lo == 1:
            hi = 1
        if hit is not None:
            lo, hi = max(lo, hit[0]), min(hi, hit[1])
        self.tt[key] = (lo, hi, ext if lo != hi else 10**9, complete or lo == hi)
        return (lo, hi)
