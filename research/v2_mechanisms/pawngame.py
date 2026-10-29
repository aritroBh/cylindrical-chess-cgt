"""Scratch re-implementation (read-only w.r.t. kings/ and cylcgt/) of
  * FG: the frozen-king pawn game (kings may not move, a king move loses at once, a promotion wins at once,
        a side with no pawn move loses) -- cross-checked against `kings/kpsolve --frozen` (see validate.py);
  * CG: the cylcgt pawn convention (a passed pawn is an immediate win; both passed -> race rule "count"),
        boolean-minimax form of cylcgt.pawns.value for a single connected component -- cross-checked against
        the stored cylcgt outcomes;
  * CC: the corrected convention (certified passers only).

Pieces: pawns on k adjacent files 0..k-1 (no wrap, buffer files empty), ranks 1..H. Position = (W, B, ep)
with W, B frozensets of (file, rank); ep = ((target), (captured), side_allowed_to_capture) or None.
Move generation copies cylcgt.pawns.moves (pawn reaching the last rank simply sits there = promoted).
"""
from __future__ import annotations

from functools import lru_cache

FILES = "abcdefgh"


def sq(t):
    return FILES.index(t[0]), int(t[1:])


def nm(s):
    return f"{FILES[s[0]]}{s[1]}"


class Game:
    def __init__(self, k, H, ep_on=True, off=0):
        self.k, self.H, self.ep_on, self.off = k, H, ep_on, off
        self.cache_fg, self.cache_cg = {}, {}

    # ---- geometry -------------------------------------------------------
    def nb(self, f, df):
        g = f + df
        return g if 0 <= g < self.k else None

    def parse(self, P):
        w, b = P.split("/")
        W = frozenset((f - self.off, r) for f, r in map(sq, w.split(":")[1].split()))
        B = frozenset((f - self.off, r) for f, r in map(sq, b.split(":")[1].split()))
        return (W, B, None)

    def show(self, pos):
        W, B, ep = pos
        f = lambda s: FILES[s[0] + self.off] + str(s[1])
        return "W: " + " ".join(sorted(map(f, W))) + " / B: " + " ".join(sorted(map(f, B)))

    # ---- moves (copy of cylcgt.pawns.moves, with move labels) -----------
    def moves(self, pos, side):
        """list of (label, newpos, promoted_flag)"""
        W, B, ep = pos
        mine, theirs = (W, B) if side == "W" else (B, W)
        occ = W | B
        d = 1 if side == "W" else -1
        start = 2 if side == "W" else self.H - 1
        last = self.H if side == "W" else 1
        ep_target = ep if (ep and ep[2] == side) else None
        out = []
        nm = lambda s_: f"{FILES[s_[0] + self.off]}{s_[1]}"

        def emit(label, nm_, nt, epv=None):
            newpos = (frozenset(nm_), frozenset(nt), epv) if side == "W" else (frozenset(nt), frozenset(nm_), epv)
            out.append((label, newpos))

        for (f, r) in sorted(mine):
            rest = mine - {(f, r)}
            r1 = r + d
            if not (1 <= r1 <= self.H):
                continue
            if (f, r1) not in occ:
                emit((f"{nm((f, r))}-{nm((f, r1))}", r1), rest | {(f, r1)}, theirs)
                r2 = r + 2 * d
                if r == start and 1 <= r2 <= self.H and (f, r2) not in occ:
                    epv = None
                    if self.ep_on:
                        epv = ((f, r1), (f, r2), "B" if side == "W" else "W")
                    emit((f"{nm((f, r))}-{nm((f, r2))}", r2), rest | {(f, r2)}, theirs, epv)
            for df in (-1, 1):
                g = self.nb(f, df)
                if g is None:
                    continue
                t = (g, r1)
                if t in theirs:
                    emit((f"{nm((f, r))}x{nm(t)}", r1), rest | {t}, theirs - {t})
                elif ep_target and ep_target[0] == t:
                    emit((f"{nm((f, r))}x{nm(t)}ep", r1), rest | {t}, theirs - {ep_target[1]})
        seen, res = set(), []
        for lab, p in out:
            if p in seen:
                continue
            seen.add(p)
            res.append((lab[0], p, lab[1] == last))
        return res

    # ---- FG: frozen-king game, exact ------------------------------------
    def fg(self, pos, side):
        """-> (winner 'W'|'L' = White wins / Black wins, plies-to-end under best play: winner minimises,
        loser maximises)."""
        key = (pos, side)
        r = self.cache_fg.get(key)
        if r is not None:
            return r
        W, B, ep = pos
        # an e.p. right that the mover is not entitled to is dropped by moves()
        mv = self.moves(pos, side)
        me = "W" if side == "W" else "L"
        other = "L" if side == "W" else "W"
        if not mv:
            r = (other, 0)  # no pawn move: only a king move, which loses at once
        else:
            best_win, best_loss = None, 0
            for lab, p, promo in mv:
                if promo:
                    res, n = me, 1
                else:
                    res, n = self.fg(p, "B" if side == "W" else "W")
                    n += 1
                if res == me:
                    best_win = n if best_win is None else min(best_win, n)
                else:
                    best_loss = max(best_loss, n)
            r = (me, best_win) if best_win is not None else (other, best_loss)
        self.cache_fg[key] = r
        return r

    def fg_moves(self, pos, side):
        """{label: (result, plies)} for each pawn move, result from White's view."""
        out = {}
        for lab, p, promo in self.moves(pos, side):
            if promo:
                out[lab] = ("W" if side == "W" else "L", 1, True)
            else:
                res, n = self.fg(p, "B" if side == "W" else "W")
                out[lab] = (res, n + 1, False)
        return out

    # ---- passed-pawn tests ----------------------------------------------
    def ep_capturable(self, pos, side, s, respect_ep):
        W, B, ep = pos
        if not (respect_ep and ep and ep[1] == s and ep[2] != side):
            return False
        f, r = s
        theirs = B if side == "W" else W
        return any((g, r) in theirs for g in (self.nb(f, -1), self.nb(f, 1)) if g is not None)

    def passed_set(self, pos, side, respect_ep):
        """pawns of `side` that satisfy the textbook (or e.p.-aware) passed test"""
        W, B, ep = pos
        mine, theirs = (W, B) if side == "W" else (B, W)
        res = []
        for f, r in mine:
            files = {f} | {g for g in (self.nb(f, -1), self.nb(f, 1)) if g is not None}
            if side == "W":
                blocked = any(g in files and s > r for g, s in theirs)
            else:
                blocked = any(g in files and s < r for g, s in theirs)
            if not blocked and not self.ep_capturable(pos, side, (f, r), respect_ep):
                res.append((f, r))
        return res

    def passed(self, pos, side, respect_ep):
        return bool(self.passed_set(pos, side, respect_ep))

    def promote_distance(self, pos, side, respect_ep):
        """cylcgt.pawns.promote_distance"""
        W, B, ep = pos
        mine = W if side == "W" else B
        occ = W | B
        best = None
        for f, r in mine:
            sub = (frozenset([(f, r)]), B, None) if side == "W" else (W, frozenset([(f, r)]), None)
            if not self.passed(sub, side, respect_ep):
                continue
            if self.ep_capturable(pos, side, (f, r), respect_ep):
                continue
            if side == "W":
                if any((f, s) in occ for s in range(r + 1, self.H + 1)):
                    continue
                d = self.H - r - (1 if r == 2 else 0)
            else:
                if any((f, s) in occ for s in range(1, r)):
                    continue
                d = r - 1 - (1 if r == self.H - 1 else 0)
            best = d if best is None else min(best, d)
        return best if best is not None else 10 ** 6

    # ---- CG: cylcgt convention, boolean minimax ---------------------------
    def cg_decisive(self, pos, respect_ep):
        wp, bp = self.passed(pos, "W", respect_ep), self.passed(pos, "B", respect_ep)
        if wp != bp:
            return "W" if wp else "L"
        return None

    def cg(self, pos, side, respect_ep, trace=None):
        """outcome 'W'/'L' (White wins / Black wins) of position `pos` with `side` to move under cylcgt's convention.
        Raises ValueError('race') if both have passed pawns at the root."""
        wp, bp = self.passed(pos, "W", respect_ep), self.passed(pos, "B", respect_ep)
        if wp and bp:
            raise ValueError("race")
        return self._cg_node(pos, side, respect_ep)

    def _cg_node(self, pos, side, respect_ep):
        key = (pos, side, respect_ep)
        r = self.cache_cg.get(key)
        if r is not None:
            return r
        wp, bp = self.passed(pos, "W", respect_ep), self.passed(pos, "B", respect_ep)
        if wp and bp:
            raise ValueError("race")
        if wp:
            r = "W"
        elif bp:
            r = "L"
        else:
            W, B, ep = pos
            mv = self.moves(pos, side)
            me = "W" if side == "W" else "L"
            other = "L" if side == "W" else "W"
            r = other
            for lab, p, promo in mv:
                if self._cg_child(p, side, respect_ep) == me:
                    r = me
                    break
        self.cache_cg[key] = r
        return r

    def _cg_child(self, p, mover, respect_ep):
        wp, bp = self.passed(p, "W", respect_ep), self.passed(p, "B", respect_ep)
        if wp and bp:
            other = "B" if mover == "W" else "W"
            winner = other if self.promote_distance(p, other, respect_ep) <= self.promote_distance(p, mover, respect_ep) else mover
            return "W" if winner == "W" else "L"
        return self._cg_node(p, "B" if mover == "W" else "W", respect_ep)
