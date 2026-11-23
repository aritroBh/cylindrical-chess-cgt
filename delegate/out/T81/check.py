"""Independent pawn-only referee checks. Run from the repository root."""
from collections import Counter
from functools import cache
from itertools import combinations, product
import sys

WHITE, BLACK = 0, 1
BIG = 256


class Board:
    def __init__(self, files, height, wrap=False, ep=True):
        self.n, self.h, self.ep = files, height, ep
        self.neighbours = []
        for f in range(files):
            self.neighbours.append({g for g in range(files) if abs(f-g) == 1
                                    or (wrap and abs(f-g) == files-1 and g != f)})

    def square(self, name):
        return (int(name[1:])-1)*self.n + ord(name[0])-ord('a')

    def pos(self, white, black):
        return (*[frozenset(map(self.square, s.split())) for s in (white, black)], -1)

    def usable(self, pos):
        w, b, ep = pos
        if ep == -1:
            return False
        return any(ep//self.n == q//self.n and q % self.n in self.neighbours[ep % self.n]
                   for q in (b if ep in w else w))

    def passers(self, pos):
        w, b, ep = pos
        protected = ep if self.usable(pos) else -1
        result = []
        for side, own, enemy in ((WHITE, w, b), (BLACK, b, w)):
            found = set()
            for p in own:
                if p == protected:
                    continue
                nearby = self.neighbours[p % self.n] | {p % self.n}
                if not any(q % self.n in nearby and
                           (q//self.n > p//self.n if side == WHITE else q//self.n < p//self.n)
                           for q in enemy):
                    found.add(p)
            result.append(found)
        return result

    def moves(self, pos, side):
        own, enemy = pos[side], pos[1-side]
        step = self.n if side == WHITE else -self.n
        home = 1 if side == WHITE else self.h-2
        for p in own:
            front = p+step
            if not 0 <= front < self.n*self.h:
                continue
            targets = []
            if front not in own | enemy:
                targets.append((front, -1, -1))
                dest = front+step
                if (p//self.n == home and 0 <= dest < self.n*self.h
                        and dest not in own | enemy):
                    targets.append((dest, -1, dest if self.ep else -1))
            for f in self.neighbours[p % self.n]:
                dest = front//self.n*self.n+f
                beside = dest-step
                if dest in enemy:
                    targets.append((dest, dest, -1))
                elif self.ep and beside == pos[2] and beside in enemy and dest not in own:
                    targets.append((dest, beside, -1))
            for dest, captured, right in targets:
                moved = (own - {p}) | {dest}
                other = enemy - {captured}
                yield p, dest, ((moved, other, right) if side == WHITE else (other, moved, right))

    def parts(self, pos):
        w, b, ep = pos
        files = {p % self.n for p in w | b}
        parts = []
        while files:
            group = {files.pop()}
            todo = list(group)
            while todo:
                extra = self.neighbours[todo.pop()] & files
                files -= extra
                group |= extra
                todo.extend(extra)
            pieces = [frozenset(p for p in pawns if p % self.n in group) for pawns in (w, b)]
            parts.append((*pieces, ep if ep != -1 and ep % self.n in group else -1))
        return tuple(parts)

    def advance(self, pos, side, move):
        src, dst = map(self.square, move.split('-'))
        return next(child for p, q, child in self.moves(pos, side) if (p, q) == (src, dst))


def calc_phi():
    # No interfile occupancy constraints in the unrestricted pawn diagram.
    for height in range(3, 13):
        ranks = range(2, height)
        for files in range(1, 9):
            for side in (WHITE, BLACK):
                per_file = max(sum((height-r if side == WHITE else r-1)
                                   for r, occupant in zip(ranks, column) if occupant == side)
                               for column in product((WHITE, BLACK, None), repeat=len(ranks)))
                assert files*per_file == files*(height-1)*(height-2)//2
    print("Per-file maxima agree for heights 3..12, widths 1..8, both sides; 8x8 maximum", 8*sum(range(1,7)))


def witnesses():
    b = Board(8, 8, wrap=True, ep=False)
    x = b.pos("b2 d4 g3 h5", "a7 c7 f7 g4")
    assert len(b.parts(x)) == 1

    def replay(pos, moves, final):
        assert b.passers(pos) == [set(), set()]
        for i, (side, move) in enumerate(moves, start=1):
            pos = b.advance(pos, side, move)
            expected = final if i == len(moves) else ("", "")
            assert b.passers(pos) == [set(map(b.square, names.split())) for names in expected]
        return pos

    y = replay(x, [(WHITE, "h5-h6"), (BLACK, "a7-h6")], ("", ""))
    assert set(b.parts(y)) == {b.pos("g3", "f7 g4 h6"), b.pos("b2 d4", "c7")}
    replay(y, [(BLACK, m) for m in ("f7-f6", "f6-f5", "f5-f4", "f4-g3")], ("", "g3 g4 h6"))
    replay(y, [(WHITE, "d4-d5"), (WHITE, "d5-d6"), (BLACK, "c7-d6")], ("b2", "d6"))
    print("A.14 first passers: black g3 g4 h6 on the f-line; white b2 and black d6 on the d-line")
    tiny = Board(2, 4)
    start = tiny.pos("a2", "b3")
    assert not any(tiny.passers(start))
    assert tiny.square("a4") in tiny.advance(start, WHITE, "a2-a4")[WHITE]
    short = Board(2, 5)
    start = short.pos("a2 b2", "b4")
    mid = short.advance(start, WHITE, "a2-a4")
    assert not any(short.passers(start)) and not any(short.passers(mid)) and short.usable(mid)
    assert short.square("a5") in short.advance(mid, WHITE, "a4-a5")[WHITE]
    print("Four-rank double promotion and five-rank same-colour local promotion reproduced")


def compare(board, order_example=False):
    # Caches are local to one geometry. S plays the integer bank even at the frontier.
    parts = cache(board.parts)
    passers = cache(board.passers)

    @cache
    def options(pos, side):
        result = []
        for _, dest, child in board.moves(pos, side):
            assert 0 < dest//board.n < board.h-1
            result.append(child)
        return tuple(result)

    def distance(p, side):
        d = board.h-1-p//board.n if side == WHITE else p//board.n
        return d - (d == board.h-2)

    @cache
    def terminal(pos, mover):
        w, b = passers(pos)
        if w and b:
            dw = min(distance(p, WHITE) for p in w)
            db = min(distance(p, BLACK) for p in b)
            return (1-mover) if dw == db else (WHITE if dw < db else BLACK)
        return WHITE if w else BLACK if b else None

    @cache
    def whole(pos, side):
        for child in options(pos, side):
            winner = terminal(child, side)
            if winner is None:
                winner = whole(child, 1-side)
            if winner == side:
                return side
        return 1-side

    @cache
    def threats(pos):
        w, b = passers(pos)
        if w or b:
            return (1 if w else 0) | (2 if b else 0)
        mask = 0
        for side in (WHITE, BLACK):
            for child in options(pos, side):
                mask |= threats(child)
        return mask

    @cache
    def violations(pos, side):
        blocks = parts(pos)
        masks = [threats(p) for p in blocks] if len(blocks) > 1 else []
        hss_bad = any(i != j and a & 1 and b & 2 for i, a in enumerate(masks)
                      for j, b in enumerate(masks))
        e_bad = len(blocks) > 1 and board.usable(pos)
        flags = int(hss_bad) | (2 if e_bad else 0)
        for child in options(pos, side):
            if terminal(child, side) is None:
                flags |= violations(child, 1-side)
        return flags

    @cache
    def summed(blocks, bank, side, split_first=False):
        if not blocks:
            if bank:
                return WHITE if bank > 0 else BLACK
            return 1-side
        unit = 1 if side == WHITE else -1
        for i, block in enumerate(blocks):
            others = blocks[:i] + blocks[i+1:]
            for child in options(block, side):
                child_blocks, child_bank = others, bank
                for region in parts(child) if split_first else (child,):
                    winner = terminal(region, side)
                    if winner is None:
                        child_blocks += parts(region)
                    else:
                        child_bank += BIG if winner == WHITE else -BIG
                if summed(child_blocks, child_bank, 1-side, split_first) == side:
                    return side
        if bank*unit > 0 and summed(blocks, bank-unit, 1-side, split_first) == side:
            return side
        return 1-side

    if order_example:
        x = board.pos("b2 d6", "c7")
        assert all(violations(x, s) == 0 for s in (WHITE, BLACK))
        results = [tuple(whole(x, s) for s in (WHITE, BLACK))]
        for split_first in (False, True):
            results.append(tuple(summed(parts(x), 0, s, split_first) for s in (WHITE, BLACK)))
        assert results == [(WHITE, WHITE), (WHITE, WHITE), (WHITE, BLACK)]
        # Two separate adjacent-file capture threats are a positive control for HSS failure.
        unsafe = board.pos("a5 d3", "b6 e4")
        assert violations(unsafe, WHITE) & 1
        print("White/Black starters: W = White/White, S (score first) = White/White,"
              " S (split first) = White/Black; separate HSS-failure control detected")
        return

    counts = Counter()
    squares = range(board.n, board.n*(board.h-1))
    for size in range(2, 6):
        for occupied in combinations(squares, size):
            pieces = frozenset(occupied)
            for k in range(1, size):
                for white in combinations(occupied, k):
                    w = frozenset(white)
                    pos = (w, pieces-w, -1)
                    if any(passers(pos)):
                        continue
                    counts["roots"] += 1
                    blocks = parts(pos)
                    if len(blocks) > 1:
                        counts["multiroot"] += 1
                    bad = violations(pos, WHITE) | violations(pos, BLACK)
                    if bad & 1:
                        counts["HSS_fail"] += 1
                    if bad & 2:
                        counts["E_fail"] += 1
                    if bad:
                        continue
                    counts["qualified"] += 1
                    if len(blocks) > 1:
                        counts["multi_qualified"] += 1
                    for side in (WHITE, BLACK):
                        a, b = whole(pos, side), summed(blocks, 0, side)
                        if a != b:
                            counts["disagreements"] += 1
                            if counts["disagreements"] == 1:
                                print("FIRST DISAGREEMENT", pos, side, a, b)
        # ponytail: discard memoized diagrams between material sizes to bound RSS;
        # the census deliberately recomputes lower-material descendants.
        for fn in (parts, passers, options, terminal, threats, violations, whole, summed):
            fn.cache_clear()
    print("cylinder" if len(board.neighbours[0]) == 2 else "flat", {k: counts[k] for k in
          ("roots", "multiroot", "HSS_fail", "E_fail", "qualified", "multi_qualified", "disagreements")})
    assert counts["disagreements"] == 0


if __name__ == "__main__":
    modes = {"phi": calc_phi, "replay": witnesses, "flat": lambda: compare(Board(4, 6)),
             "cylinder": lambda: compare(Board(4, 6, wrap=True)),
             "order": lambda: compare(Board(8, 8), order_example=True)}
    modes[sys.argv[1]]()
