#!/usr/bin/env python3
"""Independent finite pawn-game and canonical short-game solver (stdlib only)."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
import re
import sys
import time

BIG = 256
MAX_PAWNS = 6
# A pawn makes at most six advances; a terminal +/-BIG number has birthday 256.
MAX_NIMBER = BIG + 6 * MAX_PAWNS
RACES = ("count", "mover", "opponent")


@dataclass(frozen=True, slots=True)
class Game:
    left: tuple[Game, ...]
    right: tuple[Game, ...]


ZERO = Game((), ())


@lru_cache(maxsize=None)
def birthday(g: Game) -> int:
    if not g.left and not g.right:
        return 0
    return 1 + max((birthday(x) for x in g.left + g.right), default=0)


@lru_cache(maxsize=None)
def raw_code(g: Game) -> str:
    return "{" + ",".join(raw_code(x) for x in g.left) + "|" + ",".join(
        raw_code(x) for x in g.right
    ) + "}"


def ordered_games(items) -> tuple[Game, ...]:
    return tuple(sorted(set(items), key=lambda g: (birthday(g), hash(g), raw_code(g))))


def raw_game(left, right) -> Game:
    return Game(ordered_games(left), ordered_games(right))


@lru_cache(maxsize=None)
def le(a: Game, b: Game) -> bool:
    """Conway order: A <= B iff no A-left option >= B and no B-right <= A."""
    for option in a.left:
        if le(b, option):
            return False
    for option in b.right:
        if le(option, a):
            return False
    return True


def undominated(options: set[Game], left_side: bool) -> set[Game]:
    removed = set()
    for x in options:
        for y in options:
            if x == y:
                continue
            if left_side and le(x, y):
                removed.add(x)  # Left prefers the larger option.
                break
            if not left_side and le(y, x):
                removed.add(x)  # Right prefers the smaller option.
                break
    return options - removed


@lru_cache(maxsize=None)
def canonical(left: tuple[Game, ...], right: tuple[Game, ...]) -> Game:
    """Delete dominated options and bypass reversible options to canonical form."""
    L, R = set(left), set(right)
    while True:
        old = (frozenset(L), frozenset(R))
        L = undominated(L, True)
        R = undominated(R, False)
        parent = raw_game(L, R)
        left_replacements: dict[Game, set[Game]] = {}
        right_replacements: dict[Game, set[Game]] = {}
        for x in L:
            for reply in x.right:
                if le(reply, parent):
                    left_replacements[x] = set(reply.left)
                    break
        for x in R:
            for reply in x.left:
                if le(parent, reply):
                    right_replacements[x] = set(reply.right)
                    break
        for x, repl in left_replacements.items():
            L.remove(x)
            L.update(repl)
        for x, repl in right_replacements.items():
            R.remove(x)
            R.update(repl)
        if not left_replacements and not right_replacements and old == (frozenset(L), frozenset(R)):
            return raw_game(L, R)


@lru_cache(maxsize=None)
def integer(n: int) -> Game:
    if n == 0:
        return ZERO
    if n > 0:
        return Game((integer(n - 1),), ())
    return Game((), (integer(n + 1),))


@lru_cache(maxsize=None)
def dyadic(n: Fraction) -> Game:
    if n.denominator & (n.denominator - 1):
        raise ValueError(f"not dyadic: {n}")
    if n.denominator == 1:
        return integer(n.numerator)
    scale = n.denominator // 2
    lo_num = (n.numerator * scale) // n.denominator
    lo = Fraction(lo_num, scale)
    hi = lo + Fraction(1, scale)
    return canonical((dyadic(lo),), (dyadic(hi),))


@lru_cache(maxsize=None)
def nimber(n: int) -> Game:
    if n < 0:
        raise ValueError("nimber must be nonnegative")
    if n == 0:
        return ZERO
    options = tuple(nimber(i) for i in range(n))
    return canonical(options, options)


@lru_cache(maxsize=None)
def as_number(g: Game) -> Fraction | None:
    if not all(as_number(x) is not None for x in g.left + g.right):
        return None
    left = [as_number(x) for x in g.left]
    right = [as_number(x) for x in g.right]
    lo = max(left) if left else None
    hi = min(right) if right else None
    if lo is None and hi is None:
        return Fraction(0)
    if lo is not None and hi is None:
        if lo.denominator != 1:
            return None
        return lo + 1
    if lo is None and hi is not None:
        if hi.denominator != 1:
            return None
        return hi - 1
    assert lo is not None and hi is not None
    if lo >= hi:
        return None
    return (lo + hi) / 2


@lru_cache(maxsize=None)
def as_nimber(g: Game) -> int | None:
    if not g.left and not g.right:
        return 0
    if g.left != g.right:
        return None
    values = [as_nimber(x) for x in g.left]
    if any(x is None for x in values):
        return None
    present = set(values)
    mex = 0
    while mex in present:
        mex += 1
    return mex if present == set(range(mex)) else None


def fmt_fraction(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


@lru_cache(maxsize=None)
def show(g: Game) -> str:
    n = as_number(g)
    if n is not None:
        return fmt_fraction(n)
    k = as_nimber(g)
    if k is not None:
        return "*" if k == 1 else f"*{k}"
    if len(g.left) == len(g.right) == 1:
        a, b = as_number(g.left[0]), as_number(g.right[0])
        if a is not None and b is not None and a > b:
            return f"{fmt_fraction((a + b) / 2)}±{fmt_fraction((a - b) / 2)}"
        if as_nimber(g.left[0]) == 1 and as_number(g.right[0]) == 0:
            return "↓"
        if as_number(g.left[0]) == 0 and as_nimber(g.right[0]) == 1:
            return "↑"
    return "{" + ",".join(show(x) for x in g.left) + "|" + ",".join(
        show(x) for x in g.right
    ) + "}"


def parse_position(text: str, width: int) -> tuple[int, int]:
    m = re.fullmatch(r"\s*W\s*(.*?)\s*/\s*B\s*(.*?)\s*", text, re.I)
    if not m:
        raise ValueError(f"bad position: {text!r}")

    def mask(part: str) -> int:
        out = 0
        for square in part.split():
            q = re.fullmatch(r"([a-z])([1-8])", square, re.I)
            if not q:
                raise ValueError(f"bad square: {square!r}")
            f = ord(q.group(1).lower()) - ord("a")
            r = int(q.group(2)) - 1
            if f >= width:
                raise ValueError(f"{square} is outside width {width}")
            bit = 1 << (r * width + f)
            if out & bit:
                raise ValueError(f"duplicate square: {square}")
            out |= bit
        return out

    white, black = mask(m.group(1)), mask(m.group(2))
    if white & black:
        raise ValueError("both sides occupy a square")
    return white, black


class PawnGame:
    def __init__(self, width: int, race: str, ep: bool, passed_test: str):
        if not 1 <= width <= 8:
            raise ValueError("width must be 1..8")
        if race not in RACES:
            raise ValueError(f"unknown race rule {race!r}")
        if passed_test not in ("textbook", "aware"):
            raise ValueError("passed_test must be 'textbook' or 'aware'")
        self.width = width
        self.race = race
        self.ep = ep
        self.passed_test = passed_test

    def _capturable_ep_victim(self, w: int, b: int, ep_target: int, last: int) -> int | None:
        if not self.ep or ep_target < 0 or last == 0:
            return None
        victim = ep_target + last * self.width
        capturers = w if last == -1 else b
        rank, file = divmod(victim, self.width)
        target_file = ep_target % self.width
        if (w | b) & (1 << ep_target):
            return None
        for f in (target_file - 1, target_file + 1):
            if 0 <= f < self.width and capturers & (1 << (rank * self.width + f)):
                return victim
        return None

    def passers(self, w: int, b: int, ep_target: int = -1, last: int = 0) -> tuple[list[int], list[int]]:
        vulnerable = None
        if self.passed_test == "aware":
            vulnerable = self._capturable_ep_victim(w, b, ep_target, last)
        white, black = [], []
        for side, own, enemy, dest in ((1, w, b, white), (-1, b, w, black)):
            bits = own
            while bits:
                bit = bits & -bits
                p = bit.bit_length() - 1
                bits -= bit
                if p == vulnerable:
                    continue
                rank, file = divmod(p, self.width)
                is_passed = True
                for qbits in self._iter_bits(enemy):
                    qr, qf = divmod(qbits, self.width)
                    if abs(qf - file) <= 1 and ((side == 1 and qr > rank) or (side == -1 and qr < rank)):
                        is_passed = False
                        break
                if is_passed:
                    dest.append(p)
        return white, black

    @staticmethod
    def _iter_bits(mask: int):
        while mask:
            bit = mask & -mask
            yield bit.bit_length() - 1
            mask -= bit

    def _promotion_moves(self, side: int, pawn: int, w: int, b: int) -> int:
        rank, _ = divmod(pawn, self.width)
        distance = 7 - rank if side == 1 else rank
        home = 1 if side == 1 else 6
        if rank == home:
            one = pawn + side * self.width
            two = pawn + 2 * side * self.width
            occupied = w | b
            if not ((occupied >> one) & 1) and not ((occupied >> two) & 1):
                distance -= 1
        return distance

    def _race_winner(self, white: list[int], black: list[int], w: int, b: int, last: int) -> int:
        if self.race == "mover":
            return last
        if self.race == "opponent":
            return -last
        if last == 0:
            return 0
        wd = min(self._promotion_moves(1, p, w, b) for p in white)
        bd = min(self._promotion_moves(-1, p, w, b) for p in black)
        if wd < bd:
            return 1
        if bd < wd:
            return -1
        return -last  # Count rule breaks equal promotion distances for the next mover.

    def _moves(self, side: int, w: int, b: int, ep_target: int, last: int):
        own, enemy = (w, b) if side == 1 else (b, w)
        occupied = own | enemy
        for origin in self._iter_bits(own):
            rank, file = divmod(origin, self.width)
            nr = rank + side
            if not 0 <= nr < 8:
                continue
            forward = nr * self.width + file
            if not (occupied & (1 << forward)):
                nw, nb = w, b
                if side == 1:
                    nw = (w & ~(1 << origin)) | (1 << forward)
                else:
                    nb = (b & ~(1 << origin)) | (1 << forward)
                yield (nw, nb, -1, side)
                home = 1 if side == 1 else 6
                nr2 = rank + 2 * side
                if rank == home and 0 <= nr2 < 8:
                    double = nr2 * self.width + file
                    if not (occupied & (1 << double)):
                        yield (nw & ~(1 << forward) | (1 << double), nb, forward if self.ep else -1, side) if side == 1 else (
                            nw, nb & ~(1 << forward) | (1 << double), forward if self.ep else -1, side
                        )
            for nf in (file - 1, file + 1):
                if not 0 <= nf < self.width:
                    continue
                target = nr * self.width + nf
                if enemy & (1 << target):
                    if side == 1:
                        yield ((w & ~(1 << origin)) | (1 << target), b & ~(1 << target), -1, side)
                    else:
                        yield (w & ~(1 << target), (b & ~(1 << origin)) | (1 << target), -1, side)
                elif self.ep and ep_target == target and last == -side:
                    victim = target + last * self.width
                    if enemy & (1 << victim):
                        if side == 1:
                            yield ((w & ~(1 << origin)) | (1 << target), b & ~(1 << victim), -1, side)
                        else:
                            yield (w & ~(1 << victim), (b & ~(1 << origin)) | (1 << target), -1, side)

    def _terminal(self, w: int, b: int, ep_target: int, last: int) -> Game | None:
        white, black = self.passers(w, b, ep_target, last)
        if white and black:
            winner = self._race_winner(white, black, w, b, last)
            return integer(BIG * winner)
        if white:
            return integer(BIG)
        if black:
            return integer(-BIG)
        return None

    @lru_cache(maxsize=None)
    def _value(self, w: int, b: int, ep_target: int = -1, last: int = 0) -> Game:
        terminal = self._terminal(w, b, ep_target, last)
        if terminal is not None:
            return terminal
        left, right = [], []
        for child in self._moves(1, w, b, ep_target, last):
            left.append(self._value(*child))
        for child in self._moves(-1, w, b, ep_target, last):
            right.append(self._value(*child))
        return canonical(tuple(left), tuple(right))

    def value(self, white: int, black: int) -> Game:
        return self._value(white, black, -1, 0)

    @lru_cache(maxsize=1_000_000)
    def _outcome_masks(self, w: int, b: int, ep_target: int = -1, last: int = 0) -> tuple[int, int]:
        """Bits k encode the L/R-to-move outcomes of G + *k, for k=0..MAX_NIMBER."""
        full = (1 << (MAX_NIMBER + 1)) - 1
        terminal = self._terminal(w, b, ep_target, last)
        if terminal is not None:
            if terminal == ZERO:
                nmask = full ^ 1
                return nmask, nmask
            if as_number(terminal) > 0:
                return full, 0
            return 0, full

        left_children = [self._outcome_masks(*c) for c in self._moves(1, w, b, ep_target, last)]
        right_children = [self._outcome_masks(*c) for c in self._moves(-1, w, b, ep_target, last)]
        left_board = 0
        for _, child_right in left_children:
            left_board |= full ^ child_right
        right_board = 0
        for child_left, _ in right_children:
            right_board |= full ^ child_left

        left_mask = right_mask = 0
        seen_right_losing = seen_left_losing = False
        for k in range(MAX_NIMBER + 1):
            lwin = bool((left_board >> k) & 1) or seen_right_losing
            rwin = bool((right_board >> k) & 1) or seen_left_losing
            if lwin:
                left_mask |= 1 << k
            if rwin:
                right_mask |= 1 << k
            seen_right_losing |= not rwin
            seen_left_losing |= not lwin
        return left_mask, right_mask


def headline_checks():
    positions = {
        "a": parse_position("W a2 c2 / B b7 d7", 4),
        "d": parse_position("W a2 a3 b2 / B a6 b5 b6", 4),
        "e": parse_position("W a2 b2 b6 / B a6 b7 c5", 4),
    }
    expected_a = {"count": "*2", "mover": "*2", "opponent": "0"}
    expected_b = "{2±1|-2±1}"
    expected_d, expected_e = "1/8", "{0,*|↓}"
    rows = []
    cache: dict[tuple[str, bool, str], PawnGame] = {}

    def evaluate(race, ep, passed, pos):
        key = (race, ep, passed)
        if key not in cache:
            cache[key] = PawnGame(4, race, ep, passed)
        return show(cache[key].value(*pos))

    for race in RACES:
        for ep in (False, True):
            got = evaluate(race, ep, "textbook", positions["a"])
            want = expected_a[race]
            rows.append(("a", f"{race}, textbook, e.p. {'on' if ep else 'off'}: {got} (expected {want})", got == want))
    # ponytail: solve whole boards directly; this is exponential in reachable states,
    # so component splitting is the upgrade if the stated <=6-pawn census stops fitting.
    star2_solver = cache[("count", True, "textbook")]
    left_mask, right_mask = star2_solver._outcome_masks(*positions["a"])
    full = (1 << (MAX_NIMBER + 1)) - 1
    p_mask = (full ^ left_mask) & (full ^ right_mask)
    rows.append(("nimber engine", "*2 plus *k is P exactly at k=2", p_mask == (1 << 2)))
    for race in ("count", "mover"):
        got = evaluate(race, True, "aware", positions["a"])
        rows.append(("b", f"{race}, e.p.-aware with e.p. on: {got} (expected {expected_b})", got == expected_b))

    modes = (("off", False, "textbook"), ("textbook", True, "textbook"), ("e.p.-aware", True, "aware"))
    for race in RACES:
        for mode, ep, passed in modes:
            got_d = evaluate(race, ep, passed, positions["d"])
            rows.append(("d", f"{race}, {mode}: {got_d} (expected {expected_d})", got_d == expected_d))
            got_e = evaluate(race, ep, passed, positions["e"])
            rows.append(("e", f"{race}, {mode}: {got_e} (expected {expected_e})", got_e == expected_e))
    return rows


def no_passed_root(game: PawnGame, w: int, b: int) -> bool:
    white, black = game.passers(w, b)
    return not white and not black


def positions_in_scope(width: int):
    squares = [r * width + f for r in range(1, 7) for f in range(width)]
    for total in range(2, MAX_PAWNS + 1):
        for nwhite in range(1, total):
            nblack = total - nwhite
            for wcells in combinations(squares, nwhite):
                w = sum(1 << p for p in wcells)
                remaining = [p for p in squares if not (w >> p) & 1]
                for bcells in combinations(remaining, nblack):
                    b = sum(1 << p for p in bcells)
                    yield w, b


def census(progress: bool = True) -> int:
    total = hits = 0
    full = (1 << (MAX_NIMBER + 1)) - 1
    nim_ge2 = full ^ 0b11
    started = time.monotonic()
    for width in range(1, 5):
        game = PawnGame(width, "count", True, "aware")
        width_total = width_hits = 0
        for w, b in positions_in_scope(width):
            if not no_passed_root(game, w, b):
                continue
            width_total += 1
            left, right = game._outcome_masks(w, b, -1, 0)
            possible = nim_ge2 & (full ^ left) & (full ^ right)
            if possible:
                width_hits += possible.bit_count()
                if width_hits <= 5:
                    ks = [k for k in range(2, MAX_NIMBER + 1) if (possible >> k) & 1]
                    print(f"P-hit width={width} W={w:x} B={b:x} k={ks}")
        total += width_total
        hits += width_hits
        if progress:
            print(
                f"width={width} positions={width_total} nimber_P_hits={width_hits} "
                f"cache={game._outcome_masks.cache_info()} elapsed={time.monotonic()-started:.1f}s",
                flush=True,
            )
        game._outcome_masks.cache_clear()
    print(f"TOTAL positions={total} nimber_P_hits={hits} k=2..{MAX_NIMBER} elapsed={time.monotonic()-started:.1f}s")
    return hits


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("headlines", help="compute claims a, b, d, and e")
    sub.add_parser("census", help="exhaustive nimber test for claim c")
    args = parser.parse_args(argv)
    if args.command == "headlines":
        rows = headline_checks()
        failed = 0
        for claim, detail, passed in rows:
            print(f"{'AGREE' if passed else 'DISAGREE'} {claim}: {detail}")
            failed += not passed
        print(f"headline_checks={len(rows)} failed={failed}")
        return int(bool(failed))
    return int(bool(census()))


if __name__ == "__main__":
    raise SystemExit(main())
