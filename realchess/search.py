"""Exact real-chess search over positions with more than 7 men, resolved by
the Lichess tablebase at every capture into <= 7 men.

Values are from the side to move: +1 win, 0 draw, -1 loss. A search returns an
interval (lo, hi) that always bounds the true game-theoretic value; lo == hi
means resolved. An interval is returned when the depth budget runs out.

Probe economy: probing an 8-man position X costs ONE request and returns the
category of every capture of X (those lead to <= 7 men), so a node is probed
only when one of its capture children is actually needed.

Two scoring modes (see cat_interval):
  * "pure":  no 50-move rule (cursed-win = win, blessed-loss = loss);
  * "fifty": the 50-move rule counted from the capture that entered the
    tablebase position (cursed-win / blessed-loss = draw; maybe-* = interval).
Every probed category is recorded, so occurrences of cursed/blessed/maybe
categories can be reported.
"""
from __future__ import annotations

from collections import Counter

from . import movegen as mg

WIN, DRAW, LOSS = 1, 0, -1


def cat_interval(cat: str | None, mode: str):
    """Interval of the value for the side to move IN the categorised position."""
    if cat == "win":
        return (1, 1)
    if cat == "loss":
        return (-1, -1)
    if cat == "draw":
        return (0, 0)
    if cat == "cursed-win":
        return (1, 1) if mode == "pure" else (0, 0)
    if cat == "blessed-loss":
        return (-1, -1) if mode == "pure" else (0, 0)
    if cat == "maybe-win":
        return (1, 1) if mode == "pure" else (0, 1)
    if cat == "maybe-loss":
        return (-1, -1) if mode == "pure" else (-1, 0)
    return (-1, 1)  # unknown / missing


class Searcher:
    def __init__(self, oracle, mode: str = "pure", order_hint=None, region=None, max_nodes=10**7,
                 cached=None):
        """oracle(fen) -> probe record (realchess.probe.Prober.probe or a fake).
        order_hint(pos, moves) -> moves in preferred order (optional).
        region(pos) -> 'model' or 'off' ; off-model nodes consume `ext` depth."""
        self.oracle = oracle
        self.cached = cached  # fen -> record or None, never touches the network
        self.mode = mode
        self.order_hint = order_hint
        self.region = region or (lambda pos: "off")
        self.tt: dict[str, tuple] = {}
        self.cats_seen = Counter()
        self.special = []  # (fen-of-probed-position, uci-or-root, category) for cursed/blessed/maybe
        self.unresolved_leaves = set()
        self.nodes = 0
        self.max_nodes = max_nodes
        self.probed = set()

    # --------------------------------------------------------- oracle use
    def _rec(self, pos):
        fen = mg.normal_fen(pos)
        rec = self.oracle(fen)
        self.probed.add(fen)
        return rec

    def _note(self, fen, what, cat):
        self.cats_seen[cat] += 1
        if cat in ("cursed-win", "blessed-loss", "maybe-win", "maybe-loss"):
            self.special.append((fen, what, cat))

    def root_interval(self, pos):
        """Interval for a <= 7-man position, by probing it."""
        rec = self._rec(pos)
        d = rec.get("data") or {}
        cat = d.get("category")
        self._note(mg.normal_fen(pos), "root", cat)
        return cat_interval(cat, self.mode)

    def capture_child(self, pos, m, allow_probe: bool = True):
        """Interval for the side to move AFTER capture m (child perspective)."""
        if allow_probe:
            rec = self._rec(pos)
        else:
            rec = self.cached(mg.normal_fen(pos)) if self.cached else None
            if rec is None:
                return (-1, 1)
        d = rec.get("data") or {}
        u = m.uci()
        for mv in d.get("moves", []):
            if mv["uci"] == u:
                cat = mv.get("category")
                self._note(mg.normal_fen(pos), u, cat)
                return cat_interval(cat, self.mode)
        return (-1, 1)

    def is_cached(self, pos, cached_fn) -> bool:
        return cached_fn(mg.normal_fen(pos)) is not None

    # -------------------------------------------------------------- search
    def search(self, pos, ext: int, alpha: int = -1, beta: int = 1):
        """Interval for side to move. ext = remaining off-model plies."""
        self.nodes += 1
        if self.nodes > self.max_nodes:
            raise RuntimeError("node limit")
        key = mg.normal_fen(pos)
        hit = self.tt.get(key)
        if hit is not None:
            lo, hi, e, done = hit
            if lo == hi or lo >= beta or hi <= alpha or (done and e >= ext):
                return (lo, hi)
        if pos.men() <= 7:
            iv = self.root_interval(pos)
            self.tt[key] = (iv[0], iv[1], 10**9, True)
            return iv
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
            if mg.is_capture(pos, m):
                clo, chi = self.capture_child(pos, m)
            else:
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
        if hit is not None:  # both are valid bounds: intersect
            lo, hi = max(lo, hit[0]), min(hi, hit[1])
        self.tt[key] = (lo, hi, ext if lo != hi else 10**9, complete or lo == hi)
        return (lo, hi)

    # ----------------------------------------------------------- proof
    def principal(self, pos, ext: int):
        """For a resolved node, the list of (uci, child-value-for-mover, how)
        for every move, re-using the transposition table (no new search unless
        a child is missing from it)."""
        out = []
        for m in mg.legal_moves(pos):
            if mg.is_capture(pos, m):
                clo, chi = self.capture_child(pos, m, allow_probe=False)
                how = "probe" if clo == chi else "not probed"
            else:
                child = mg.make(pos, m)
                h = self.tt.get(mg.normal_fen(child))
                if h is None:
                    clo, chi, how = -1, 1, "unexplored"
                else:
                    clo, chi, how = h[0], h[1], "search"
            out.append((m.uci(), (-chi, -clo), how))
        return out
