"""Fresh whole-board search. Bit index is (rank-1)*width+file. No project imports."""
import argparse
from functools import lru_cache


def signature(n):
    if n % 2:
        files = ["W23B4", "B5", "W2B5"] + ["W3", "B5"] * ((n - 3) // 2)
    else:
        files = ["B5", "W2B5", "W35B6", "W2"] + ["B4", "W2"] * ((n - 4) // 2)
    start = [0, 0]
    for f, code in enumerate(files):
        for char in code:
            if char.isdigit():
                start[side] |= 1 << ((int(char) - 1) * n + f)
            else:
                side = int(char == "B")
    assert len(files) == n and sum(b.bit_count() for b in start) == n + 3
    rank = [(2**n - 1) << (n * r) for r in range(8)]
    first = sum(1 << (n * r) for r in range(8))
    last = first << (n - 1)
    board = 2**(8*n) - 1

    def left(b):
        return ((b & ~first) >> 1) | ((b & first) << (n-1))

    def right(b):
        return ((b & ~last) << 1) | ((b & last) >> (n-1))

    def forward(b, side):
        return b >> n if side else (b << n) & board

    def behind(b, side):
        # Fill squares strictly behind any bit, in this side's forward direction.
        if side:
            b <<= n
            b |= b << n
            b |= b << (2*n)
            return (b | b << (4*n)) & board
        b >>= n
        b |= b >> n
        b |= b >> (2*n)
        return b | b >> (4*n)

    def terminal(w, b, ep, mover):
        wp = w & ~behind(b | left(b) | right(b), 0) & ~ep
        bp = b & ~behind(w | left(w) | right(w), 1) & ~ep
        if wp and bp:
            # A passer with a friendly pawn in front cannot lead its file's race.
            wf = wp & ~behind(w, 0)
            bf = bp & ~behind(b, 1)
            wr = (wf.bit_length() - 1) // n + 1
            br = ((bf & -bf).bit_length() - 1) // n + 1
            dw = 8 - wr - (wr == 2) if wf else 99
            db = br - 1 - (br == 7) if bf else 99
            return int(db < dw) if dw != db else 1 - mover
        if wp or bp:
            return int(bool(bp))
        return None

    def bits(mask):
        while mask:
            bit = mask & -mask
            yield bit
            mask ^= bit

    def children(w, b, ep, side):
        own, enemy = (b, w) if side else (w, b)
        empty = board ^ (own | enemy)
        step = forward(own, side) & empty
        for shift, inverse in ((left, right), (right, left)):
            attacks = shift(forward(own, side))
            victim = ep & enemy
            target = forward(victim, side) & empty
            for to in bits(attacks & (enemy | target)):
                old = inverse(forward(to, 1-side))
                ours = own ^ old ^ to
                theirs = enemy ^ (victim if to & target else to)
                yield (theirs, ours, 0) if side else (ours, theirs, 0)
        for to in bits(step):
            ours = own ^ forward(to, 1-side) ^ to
            yield (enemy, ours, 0) if side else (ours, enemy, 0)
        doubles = forward(step & rank[5 if side else 2], side) & empty
        for to in bits(doubles):
            ours = own ^ forward(forward(to, 1-side), 1-side) ^ to
            flag = to if enemy & (left(to) | right(to)) else 0
            yield (enemy, ours, flag) if side else (ours, enemy, flag)

    # ponytail: bounded memo tables keep this small-width check within its memory budget.
    @lru_cache(8192)
    def options(w, b, ep, side):
        live = []
        for child in children(w, b, ep, side):
            winner = terminal(*child, side)
            if winner == side:
                return True, ()
            if winner is None:
                live.append(child)
        return False, tuple(live)

    @lru_cache(65536)
    def win(w, b, ep, side, heap):
        immediate, moves = options(w, b, ep, side)
        if immediate:
            return True
        if any(not win(*child, 1-side, heap) for child in moves):
            return True
        # A disjunctive heap move leaves the board summand, including its flag, alone.
        return any(not win(w, b, ep, 1-side, h) for h in range(heap))

    # A double step on file 0, with an en passant capturer across the seam.
    at = lambda f, r: 1 << ((r - 1) * n + f)
    supports = at(2, 2) | at(n-2, 2)
    guards = at(1, 4) | at(n-1, 4)
    double = (supports | at(0, 4), guards, at(0, 4))
    assert double in children(supports | at(0, 2), guards, 0, 0)
    assert terminal(*double, 0) is None
    assert terminal(double[0], guards, 0, 0) == 0
    assert (supports, at(1, 4) | at(0, 3), 0) in children(*double, 1)
    for mover in (0, 1):
        assert terminal(at(0, 6), at(2, 3), 0, mover) == 1 - mover
    assert terminal(*start, 0, 0) is None
    pairs = [(win(*start, 0, 0, h), win(*start, 0, 1, h)) for h in range(4)]
    options.cache_clear()
    win.cache_clear()
    return ''.join({(True, True): 'N', (False, False): 'P',
                    (True, False): 'L', (False, True): 'R'}[p] for p in pairs)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('widths', nargs='+', type=int, choices=range(5, 18))
    for width in ap.parse_args().widths:
        result = signature(width)
        print(width, result, flush=True)
        assert result == 'NNPN', (width, result)
