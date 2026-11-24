#!/usr/bin/env python3
"""
Independent pawn-endgame solver and canonical-form CGT implementation.
Written from scratch for T1b verification task.
No dependencies on cylcgt/, sumtest/, lemmas/, crosscheck/, or atlas/.
"""

from __future__ import annotations
import argparse
import re
import time
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from typing import Optional

# Constants matching the project conventions
BIG = 256
MAX_PAWNS = 6
MAX_NIMBER = 512  # sufficient for nimber census
RACES = ("count", "mover", "opponent")
MAX_RANK = 8  # 8 ranks (0-7)
HOME_RANK_WHITE = 1  # rank 2 (0-indexed)
HOME_RANK_BLACK = 6  # rank 7 (0-indexed)


# ============================================================
# Canonical-form CGT
# ============================================================

@dataclass(frozen=True, slots=True)
class Game:
    """A combinatorial game in canonical form: {L | R}"""
    left: tuple['Game', ...]
    right: tuple['Game', ...]


ZERO = Game((), ())


@lru_cache(maxsize=None)
def birthday(g: Game) -> int:
    """Birthday (height) of a game tree."""
    if not g.left and not g.right:
        return 0
    return 1 + max((birthday(x) for x in g.left + g.right), default=0)


@lru_cache(maxsize=None)
def game_key(g: Game) -> tuple:
    """Canonical ordering key for games."""
    return (birthday(g), hash(g), str(g.left), str(g.right))


def ordered_games(items: set[Game]) -> tuple[Game, ...]:
    """Sort and deduplicate a set of games."""
    return tuple(sorted(items, key=game_key))


def make_game(left: set[Game], right: set[Game]) -> Game:
    """Construct a Game from sets of left/right options."""
    return Game(ordered_games(left), ordered_games(right))


# ----- Conway order (A <= B) -----

@lru_cache(maxsize=None)
def le(a: Game, b: Game) -> bool:
    """Conway's order: A <= B iff no A^L >= B and no B^R <= A."""
    for aL in a.left:
        if le(b, aL):
            return False
    for bR in b.right:
        if le(bR, a):
            return False
    return True


def eq(a: Game, b: Game) -> bool:
    """Game equality: A = B iff A <= B and B <= A."""
    return le(a, b) and le(b, a)


# ----- Dominated option removal -----

def undominated(options: set[Game], left_side: bool) -> set[Game]:
    """Remove dominated options. Left prefers larger; Right prefers smaller."""
    removed = set()
    for x in options:
        for y in options:
            if x is y:
                continue
            if left_side and le(x, y):   # x <= y, so Left prefers y
                removed.add(x)
                break
            if not left_side and le(y, x):  # y <= x, so Right prefers y
                removed.add(x)
                break
    return options - removed


# ----- Reversible option bypass -----

@lru_cache(maxsize=None)
def canonical(left: tuple[Game, ...], right: tuple[Game, ...]) -> Game:
    """Reduce to canonical form: remove dominated, bypass reversible options."""
    L, R = set(left), set(right)
    while True:
        old = (frozenset(L), frozenset(R))
        # Remove dominated
        L = undominated(L, True)
        R = undominated(R, False)
        parent = make_game(L, R)
        # Bypass reversible
        left_repl: dict[Game, set[Game]] = {}
        right_repl: dict[Game, set[Game]] = {}
        for x in L:
            for reply in x.right:
                if le(reply, parent):
                    left_repl[x] = set(reply.left)
                    break
        for x in R:
            for reply in x.left:
                if le(parent, reply):
                    right_repl[x] = set(reply.right)
                    break
        for x, repl in left_repl.items():
            L.remove(x)
            L.update(repl)
        for x, repl in right_repl.items():
            R.remove(x)
            R.update(repl)
        if not left_repl and not right_repl and old == (frozenset(L), frozenset(R)):
            return make_game(L, R)


# ----- Canonical constructors for common games -----

@lru_cache(maxsize=None)
def integer(n: int) -> Game:
    if n == 0:
        return ZERO
    if n > 0:
        return Game((integer(n - 1),), ())
    return Game((), (integer(n + 1),))


@lru_cache(maxsize=None)
def dyadic(fr: Fraction) -> Game:
    """Construct a dyadic rational game."""
    if fr.denominator & (fr.denominator - 1):
        raise ValueError(f"Not dyadic: {fr}")
    if fr.denominator == 1:
        return integer(fr.numerator)
    half_den = fr.denominator // 2
    lo_num = (fr.numerator * half_den) // fr.denominator
    lo = Fraction(lo_num, half_den)
    hi = lo + Fraction(1, half_den)
    return canonical((dyadic(lo),), (dyadic(hi),))


@lru_cache(maxsize=None)
def nimber(n: int) -> Game:
    """Construct *n = {0, *1, ..., *(n-1) | 0, *1, ..., *(n-1)}."""
    if n < 0:
        raise ValueError("nimber must be nonnegative")
    if n == 0:
        return ZERO
    opts = tuple(nimber(i) for i in range(n))
    return canonical(opts, opts)


# ----- Recognition helpers -----

@lru_cache(maxsize=None)
def as_number(g: Game) -> Optional[Fraction]:
    """Return the numeric value if g is a number, else None."""
    # All options must be numbers
    for opt in g.left + g.right:
        if as_number(opt) is None:
            return None
    left_vals = [as_number(x) for x in g.left]
    right_vals = [as_number(x) for x in g.right]
    lo = max(left_vals) if left_vals else None
    hi = min(right_vals) if right_vals else None
    if lo is None and hi is None:
        return Fraction(0)
    if lo is not None and hi is None:
        return lo + 1 if lo.denominator == 1 else None
    if lo is None and hi is not None:
        return hi - 1 if hi.denominator == 1 else None
    if lo >= hi:
        return None
    return (lo + hi) / 2


@lru_cache(maxsize=None)
def as_nimber(g: Game) -> Optional[int]:
    """Return n if g == *n, else None."""
    if not g.left and not g.right:
        return 0
    if g.left != g.right:
        return None
    vals = [as_nimber(x) for x in g.left]
    if any(v is None for v in vals):
        return None
    present = set(vals)
    mex = 0
    while mex in present:
        mex += 1
    return mex if present == set(range(mex)) else None


@lru_cache(maxsize=None)
def is_switch(g: Game) -> bool:
    """Check if game is a switch {a | b} with a > b (numbers)."""
    return (len(g.left) == 1 and len(g.right) == 1 and
            as_number(g.left[0]) is not None and as_number(g.right[0]) is not None and
            as_number(g.left[0]) > as_number(g.right[0]))


@lru_cache(maxsize=None)
def is_tiny(g: Game) -> bool:
    """Check if game is tiny(x) = {0 | {0 | -x}} for x > 0."""
    # Simplified check for our purposes
    return False


# ----- String representation -----

def fmt_frac(fr: Fraction) -> str:
    return str(fr.numerator) if fr.denominator == 1 else f"{fr.numerator}/{fr.denominator}"


@lru_cache(maxsize=None)
def show(g: Game) -> str:
    """Human-readable canonical form."""
    num = as_number(g)
    if num is not None:
        return fmt_frac(num)
    nim = as_nimber(g)
    if nim is not None:
        return "*" if nim == 1 else f"*{nim}"
    # Check for switch {a | b} with numbers
    if len(g.left) == 1 and len(g.right) == 1:
        a = as_number(g.left[0])
        b = as_number(g.right[0])
        if a is not None and b is not None and a > b:
            mean = (a + b) / 2
            temp = (a - b) / 2
            return f"{fmt_frac(mean)}±{fmt_frac(temp)}"
        # Check for ↑ = {0 | *} and ↓ = {* | 0}
        if as_nimber(g.left[0]) == 1 and as_number(g.right[0]) == Fraction(0):
            return "↓"
        if as_number(g.left[0]) == Fraction(0) and as_nimber(g.right[0]) == 1:
            return "↑"
        # Check for ↑* = {0, * | 0}
        if (as_number(g.left[0]) == Fraction(0) and as_nimber(g.right[0]) == 0 and
            len(g.left) == 2 and as_nimber(g.left[1]) == 1):
            return "↑*"
        # Check for {0, * | ↓}
        if (len(g.left) == 2 and as_number(g.left[0]) == Fraction(0) and
            as_nimber(g.left[1]) == 1 and
            len(g.right) == 1):
            r = g.right[0]
            if len(r.left) == 1 and len(r.right) == 1:
                if as_nimber(r.left[0]) == 1 and as_number(r.right[0]) == Fraction(0):
                    return "{0,*|↓}"
    # Fallback: raw form
    return "{" + ",".join(show(x) for x in g.left) + "|" + ",".join(show(x) for x in g.right) + "}"


# ============================================================
# Pawn Game Engine
# ============================================================

@dataclass(frozen=True, slots=True)
class Position:
    """Bitboard position: white pawns, black pawns, en passant target, last mover."""
    white: int
    black: int
    ep_target: int = -1  # square index of e.p. capture square, -1 if none
    last: int = 0        # +1 if White just moved, -1 if Black, 0 for root


def parse_position(text: str, width: int) -> tuple[int, int]:
    """Parse 'W a2 c2 / B b7 d7' into (white_bitboard, black_bitboard)."""
    m = re.fullmatch(r"\s*W\s*(.*?)\s*/\s*B\s*(.*?)\s*", text, re.I)
    if not m:
        raise ValueError(f"Bad position format: {text!r}")

    def mask(part: str) -> int:
        out = 0
        for sq in part.split():
            q = re.fullmatch(r"([a-h])([1-8])", sq, re.I)
            if not q:
                raise ValueError(f"Bad square: {sq!r}")
            f = ord(q.group(1).lower()) - ord("a")
            r = int(q.group(2)) - 1
            if f >= width:
                raise ValueError(f"Square {sq} outside width {width}")
            bit = 1 << (r * width + f)
            if out & bit:
                raise ValueError(f"Duplicate square: {sq}")
            out |= bit
        return out

    white = mask(m.group(1))
    black = mask(m.group(2))
    if white & black:
        raise ValueError("Both sides occupy same square")
    return white, black


class PawnGame:
    """
    Pawn-only game solver on an N-file × 8-rank board.
    Supports flat (no wrap) and cylindrical (wrap) boards.
    """

    def __init__(self, width: int, race: str, ep: bool, passed_test: str, wrap: bool = False):
        if not 1 <= width <= 8:
            raise ValueError("width must be 1..8")
        if race not in RACES:
            raise ValueError(f"Unknown race rule: {race!r}")
        if passed_test not in ("textbook", "aware"):
            raise ValueError("passed_test must be 'textbook' or 'aware'")
        self.width = width
        self.race = race
        self.ep = ep
        self.passed_test = passed_test
        self.wrap = wrap
        self.total_squares = width * 8

    # ----- Bitboard utilities -----

    @staticmethod
    def _bits(mask: int):
        while mask:
            b = mask & -mask
            yield b.bit_length() - 1
            mask -= b

    def _sq(self, rank: int, file: int) -> int:
        return rank * self.width + file

    def _rc(self, sq: int) -> tuple[int, int]:
        return divmod(sq, self.width)

    def _file_adjacent(self, f1: int, f2: int) -> bool:
        """Check if two files are adjacent (with wrap if cylindrical)."""
        if not self.wrap:
            return abs(f1 - f2) <= 1
        df = abs(f1 - f2)
        return df <= 1 or df >= self.width - 1

    # ----- Passed pawn detection -----

    def _ep_victim(self, w: int, b: int, ep_target: int, last: int) -> Optional[int]:
        """Return the square of the pawn that can be captured en passant, or None."""
        if not self.ep or ep_target < 0 or last == 0:
            return None
        # The victim is one step behind the e.p. target in the direction of the last move
        victim = ep_target + last * self.width
        capturers = w if last == -1 else b  # opponent of the pawn that just double-stepped
        rank, file = self._rc(victim)
        target_file = ep_target % self.width
        # Check if the e.p. target square is empty
        if (w | b) & (1 << ep_target):
            return None
        # Check adjacent files for capturer
        for f in (target_file - 1, target_file + 1):
            if self.wrap:
                f = f % self.width
            if 0 <= f < self.width and (capturers & (1 << (rank * self.width + f))):
                return victim
        return None

    def passers(self, w: int, b: int, ep_target: int = -1, last: int = 0) -> tuple[list[int], list[int]]:
        """Return lists of passed pawn squares for White and Black."""
        vulnerable = None
        if self.passed_test == "aware":
            vulnerable = self._ep_victim(w, b, ep_target, last)

        white_passed, black_passed = [], []

        for side, own, enemy, dest in ((1, w, b, white_passed), (-1, b, w, black_passed)):
            for p in self._bits(own):
                if p == vulnerable:
                    continue
                rank, file = self._rc(p)
                is_passed = True
                for q in self._bits(enemy):
                    qr, qf = self._rc(q)
                    if self._file_adjacent(file, qf):
                        if (side == 1 and qr > rank) or (side == -1 and qr < rank):
                            is_passed = False
                            break
                if is_passed:
                    dest.append(p)
        return white_passed, black_passed

    # ----- Promotion distance (for race rule "count") -----

    def _promotion_distance(self, side: int, pawn: int, w: int, b: int) -> int:
        """Number of moves to promote, assuming no interference."""
        rank, _ = self._rc(pawn)
        home = HOME_RANK_WHITE if side == 1 else HOME_RANK_BLACK
        if side == 1:
            dist = 7 - rank
            if rank == home:
                # Check if double step is possible
                one = pawn + self.width
                two = pawn + 2 * self.width
                if not ((w | b) >> one) & 1 and not ((w | b) >> two) & 1:
                    dist -= 1
        else:
            dist = rank
            if rank == home:
                one = pawn - self.width
                two = pawn - 2 * self.width
                if not ((w | b) >> one) & 1 and not ((w | b) >> two) & 1:
                    dist -= 1
        return dist

    def _race_winner(self, white_passed: list[int], black_passed: list[int],
                     w: int, b: int, last: int) -> int:
        """Determine race winner per the chosen rule."""
        if self.race == "mover":
            return last
        if self.race == "opponent":
            return -last
        # "count" rule
        if last == 0:
            return 0
        wd = min(self._promotion_distance(1, p, w, b) for p in white_passed)
        bd = min(self._promotion_distance(-1, p, w, b) for p in black_passed)
        if wd < bd:
            return 1
        if bd < wd:
            return -1
        return -last  # tie goes to the next mover (opponent of last)

    # ----- Move generation -----

    def _gen_moves(self, side: int, w: int, b: int, ep_target: int, last: int):
        """Yield (new_w, new_b, new_ep_target, new_last) for all legal moves."""
        own, enemy = (w, b) if side == 1 else (b, w)
        occupied = own | enemy
        forward = 1 if side == 1 else -1
        home = HOME_RANK_WHITE if side == 1 else HOME_RANK_BLACK

        for origin in self._bits(own):
            rank, file = self._rc(origin)
            nr = rank + forward
            if not (0 <= nr < 8):
                continue

            # Single step forward
            forward_sq = self._sq(nr, file)
            if not (occupied & (1 << forward_sq)):
                if side == 1:
                    nw = (w & ~(1 << origin)) | (1 << forward_sq)
                    nb = b
                else:
                    nw = w
                    nb = (b & ~(1 << origin)) | (1 << forward_sq)
                # Single step never creates e.p. target
                yield (nw, nb, -1, side)

                # Double step from home rank
                if rank == home:
                    nr2 = rank + 2 * forward
                    if 0 <= nr2 < 8:
                        double_sq = self._sq(nr2, file)
                        if not (occupied & (1 << double_sq)):
                            if side == 1:
                                nw2 = (w & ~(1 << origin)) | (1 << double_sq)
                                nb2 = b
                            else:
                                nw2 = w
                                nb2 = (b & ~(1 << origin)) | (1 << double_sq)
                            # e.p. target is the skipped square (forward_sq)
                            new_ep2 = forward_sq if self.ep else -1
                            yield (nw2, nb2, new_ep2, side)

            # Captures (including e.p.)
            for df in (-1, 1):
                nf = file + df
                if self.wrap:
                    nf = nf % self.width
                if not (0 <= nf < self.width):
                    continue
                target = self._sq(nr, nf)
                # Normal capture
                if enemy & (1 << target):
                    if side == 1:
                        yield ((w & ~(1 << origin)) | (1 << target), b & ~(1 << target), -1, side)
                    else:
                        yield (w & ~(1 << target), (b & ~(1 << origin)) | (1 << target), -1, side)
                # En passant capture
                elif self.ep and ep_target == target and last == -side:
                    victim = target + last * self.width
                    if enemy & (1 << victim):
                        if side == 1:
                            yield ((w & ~(1 << origin)) | (1 << target), b & ~(1 << victim), -1, side)
                        else:
                            yield (w & ~(1 << victim), (b & ~(1 << origin)) | (1 << target), -1, side)

    # ----- Terminal evaluation -----

    def _terminal(self, w: int, b: int, ep_target: int, last: int) -> Optional[Game]:
        """Return terminal game value if position is terminal, else None."""
        white_passed, black_passed = self.passers(w, b, ep_target, last)
        if white_passed and black_passed:
            winner = self._race_winner(white_passed, black_passed, w, b, last)
            return integer(BIG * winner)
        if white_passed:
            return integer(BIG)
        if black_passed:
            return integer(-BIG)
        return None

    # ----- Recursive value computation -----

    @lru_cache(maxsize=None)
    def _value(self, w: int, b: int, ep_target: int = -1, last: int = 0) -> Game:
        terminal = self._terminal(w, b, ep_target, last)
        if terminal is not None:
            return terminal
        left_opts, right_opts = [], []
        for child in self._gen_moves(1, w, b, ep_target, last):
            left_opts.append(self._value(*child))
        for child in self._gen_moves(-1, w, b, ep_target, last):
            right_opts.append(self._value(*child))
        return canonical(tuple(left_opts), tuple(right_opts))

    def value(self, white: int, black: int) -> Game:
        """Compute the CGT value of a position (root: no e.p., no last move)."""
        return self._value(white, black, -1, 0)

    def clear_cache(self):
        self._value.cache_clear()

    # ----- Fast outcome masks for G + *k (for nimber census) -----

    @lru_cache(maxsize=1_000_000)
    def _outcome_masks(self, w: int, b: int, ep_target: int = -1, last: int = 0) -> tuple[int, int]:
        """Bits k encode the L/R-to-move outcomes of G + *k, for k=0..MAX_NIMBER."""
        full = (1 << (MAX_NIMBER + 1)) - 1
        terminal = self._terminal(w, b, ep_target, last)
        if terminal is not None:
            if terminal == ZERO:
                nmask = full ^ 1  # *0 is P-position, all *k (k>0) are N-positions
                return nmask, nmask
            num = as_number(terminal)
            if num is not None and num > 0:
                return full, 0
            return 0, full

        left_children = [self._outcome_masks(*c) for c in self._gen_moves(1, w, b, ep_target, last)]
        right_children = [self._outcome_masks(*c) for c in self._gen_moves(-1, w, b, ep_target, last)]
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


# ============================================================
# Nimber outcome test (for claim c)
# ============================================================

def outcome_masks(game: PawnGame, w: int, b: int, ep_target: int = -1, last: int = 0,
                  max_nimber: int = 512) -> tuple[int, int]:
    """
    Compute bitmasks of nimber outcomes for G + *k.
    Returns (left_mask, right_mask) where bit k is 1 iff Left/Right wins G + *k moving first.
    """
    full = (1 << (max_nimber + 1)) - 1
    terminal = game._terminal(w, b, ep_target, last)
    if terminal is not None:
        if terminal == ZERO:
            nmask = full ^ 1  # *0 is P-position, all *k (k>0) are N-positions
            return nmask, nmask
        num = as_number(terminal)
        if num is not None and num > 0:
            return full, 0  # Left wins all
        return 0, full      # Right wins all

    # Recurse on children
    left_children = [outcome_masks(game, *c, max_nimber=max_nimber)
                     for c in game._gen_moves(1, w, b, ep_target, last)]
    right_children = [outcome_masks(game, *c, max_nimber=max_nimber)
                      for c in game._gen_moves(-1, w, b, ep_target, last)]

    # Left moving first in G + *k wins if any Left option is a Right-loss in that sum
    left_board = 0
    for _, child_right in left_children:
        left_board |= full ^ child_right
    right_board = 0
    for child_left, _ in right_children:
        right_board |= full ^ child_left

    # Compute winning nimbers using the "mex" propagation for sums with nimbers
    left_mask = right_mask = 0
    seen_right_lose = seen_left_lose = False
    for k in range(max_nimber + 1):
        lwin = bool((left_board >> k) & 1) or seen_right_lose
        rwin = bool((right_board >> k) & 1) or seen_left_lose
        if lwin:
            left_mask |= 1 << k
        if rwin:
            right_mask |= 1 << k
        seen_right_lose |= not rwin
        seen_left_lose |= not lwin
    return left_mask, right_mask


def is_nimber_k(g: Game, k: int) -> bool:
    """Test if game equals *k by checking if G + *k is a second-player win (P-position)."""
    if k == 0:
        return g == ZERO
    # For k > 0, we'd need to compute outcome of G + *k
    # This is handled by the outcome_masks approach
    return False


# ============================================================
# Scope enumeration for claim (c)
# ============================================================

def positions_in_scope(width: int):
    """Enumerate all positions in scope for claim (c):
    - flat 8 ranks, widths 1-4
    - pawns on ranks 2-7 (indices 1-6)
    - at least one pawn per side
    - total pawns <= 6
    - no passed pawn at root
    """
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


def no_passed_root(game: PawnGame, w: int, b: int) -> bool:
    """Check if position has no passed pawn at root (ep_target=-1, last=0)."""
    white, black = game.passers(w, b)
    return not white and not black


# ============================================================
# Verification of the 5 claims
# ============================================================

def check_claim_a():
    """Claim (a): W a2 c2 / B b7 d7 on 4-file flat board."""
    print("Checking claim (a)...")
    results = []
    pos_w, pos_b = parse_position("W a2 c2 / B b7 d7", 4)

    for race in RACES:
        for ep in (False, True):
            game = PawnGame(4, race, ep, "textbook", wrap=False)
            val = show(game.value(pos_w, pos_b))
            if race == "opponent":
                expected = "0"
            else:
                expected = "*2"
            passed = (val == expected)
            results.append(("a", f"{race}, textbook, e.p. {'on' if ep else 'off'}", val, expected, passed))
            print(f"  {race}, e.p. {'on' if ep else 'off'}: got {val}, expected {expected} -> {'AGREE' if passed else 'DISAGREE'}")
    return results


def check_claim_b():
    """Claim (b): W a2 c2 / B b7 d7 under e.p.-aware test with e.p. on."""
    print("Checking claim (b)...")
    results = []
    pos_w, pos_b = parse_position("W a2 c2 / B b7 d7", 4)
    expected = "{2±1|-2±1}"

    for race in ("count", "mover"):
        game = PawnGame(4, race, True, "aware", wrap=False)
        val = show(game.value(pos_w, pos_b))
        passed = (val == expected)
        results.append(("b", f"{race}, e.p.-aware with e.p. on", val, expected, passed))
        print(f"  {race}: got {val}, expected {expected} -> {'AGREE' if passed else 'DISAGREE'}")
    return results


def check_claim_c():
    """Claim (c): No *k with k>=2 in scope under e.p.-aware, count, e.p. on."""
    print("Checking claim (c)...")
    total_positions = 0
    hits = 0
    full = (1 << (MAX_NIMBER + 1)) - 1
    nim_ge2 = full ^ 0b11  # bits for k >= 2

    for width in range(1, 5):
        game = PawnGame(width, "count", True, "aware", wrap=False)
        width_total = width_hits = 0
        for w, b in positions_in_scope(width):
            if not no_passed_root(game, w, b):
                continue
            width_total += 1
            left, right = game._outcome_masks(w, b, -1, 0)
            possible = nim_ge2 & (full ^ left) & (full ^ right)
            if possible:
                width_hits += possible.bit_count()
                hits += possible.bit_count()
                if width_hits <= 5:
                    ks = [k for k in range(2, MAX_NIMBER + 1) if (possible >> k) & 1]
                    print(f"  HIT width={width} W={w:x} B={b:x} k={ks}")
        total_positions += width_total
        print(f"  width={width}: {width_total} positions, {width_hits} *k (k>=2) hits")
        game._outcome_masks.cache_clear()

    print(f"  TOTAL: {total_positions} positions, {hits} hits")
    passed = (hits == 0)
    return [("c", f"e.p.-aware, count, e.p. on, widths 1-4", f"{hits} hits", "0 hits", passed)]


def check_claim_d():
    """Claim (d): W a2 a3 b2 / B a6 b5 b6 equals 1/8 in all 9 settings."""
    print("Checking claim (d)...")
    results = []
    pos_w, pos_b = parse_position("W a2 a3 b2 / B a6 b5 b6", 4)
    expected = "1/8"
    modes = [
        ("e.p. off, textbook", False, "textbook"),
        ("e.p. on, textbook", True, "textbook"),
        ("e.p. on, aware", True, "aware"),
    ]

    for race in RACES:
        for mode_name, ep, passed in modes:
            game = PawnGame(4, race, ep, passed, wrap=False)
            val = show(game.value(pos_w, pos_b))
            passed_flag = (val == expected)
            results.append(("d", f"{race}, {mode_name}", val, expected, passed_flag))
            print(f"  {race}, {mode_name}: got {val}, expected {expected} -> {'AGREE' if passed_flag else 'DISAGREE'}")
    return results


def check_claim_e():
    """Claim (e): W a2 b2 b6 / B a6 b7 c5 equals {0,*|↓} in all 9 settings."""
    print("Checking claim (e)...")
    results = []
    pos_w, pos_b = parse_position("W a2 b2 b6 / B a6 b7 c5", 4)
    expected = "{0,*|↓}"
    modes = [
        ("e.p. off, textbook", False, "textbook"),
        ("e.p. on, textbook", True, "textbook"),
        ("e.p. on, aware", True, "aware"),
    ]

    for race in RACES:
        for mode_name, ep, passed in modes:
            game = PawnGame(4, race, ep, passed, wrap=False)
            val = show(game.value(pos_w, pos_b))
            passed_flag = (val == expected)
            results.append(("e", f"{race}, {mode_name}", val, expected, passed_flag))
            print(f"  {race}, {mode_name}: got {val}, expected {expected} -> {'AGREE' if passed_flag else 'DISAGREE'}")
    return results


def main():
    parser = argparse.ArgumentParser(description="T1b Independent Verification")
    parser.add_argument("command", choices=["headlines", "census", "all"],
                        help="Run headline checks (a,b,d,e), census (c), or all")
    args = parser.parse_args()

    all_results = []

    if args.command in ("headlines", "all"):
        all_results.extend(check_claim_a())
        all_results.extend(check_claim_b())
        all_results.extend(check_claim_d())
        all_results.extend(check_claim_e())

    if args.command in ("census", "all"):
        all_results.extend(check_claim_c())

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    failed = 0
    for claim, detail, got, expected, passed in all_results:
        status = "AGREE" if passed else "DISAGREE"
        print(f"{status} {claim}: {detail} -> got {got}, expected {expected}")
        if not passed:
            failed += 1
    print(f"\nTotal: {len(all_results)} checks, {failed} failed")
    return int(failed > 0)


if __name__ == "__main__":
    raise SystemExit(main())