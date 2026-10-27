"""Whole-board pawn-game outcomes, implemented from the written rules."""

from functools import lru_cache
from time import perf_counter

from cylcgt.pawns import Board, Pos, passed

W, B = "W", "B"


def other(side):
    return B if side == W else W


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def square(file, rank, n):
    return rank * n + file


def coords(mask, n):
    return frozenset((i % n, i // n + 1) for i in bits(mask))


def library_ep(ep):
    """Convert (victim side, file) to Pos.ep's target/victim/eligible-side tuple."""
    if ep is None:
        return None
    victim, file = ep
    rank = 4 if victim == W else 5
    target_rank = rank - 1 if victim == W else rank + 1
    return ((file, target_rank), (file, rank), other(victim))


def start(n, moved_b7=False):
    assert n >= 8 and n % 2 == 0
    white, black = set(), set()
    for file, side, rank in (
        (0, W, 5), (1, B, 6 if moved_b7 else 7), (2, W, 4),
        (3, W, 4), (3, B, 7), (4, B, 6), (5, W, 3), (5, B, 6),
    ):
        (white if side == W else black).add(square(file, rank - 1, n))
    for file in range(6, n):
        if file % 2 == 0:
            white.add(square(file, 2 - 1, n))
        else:
            black.add(square(file, 4 - 1, n))
    return sum(1 << i for i in white), sum(1 << i for i in black), None


def children(n, white, black, ep, side):
    own, enemy = (white, black) if side == W else (black, white)
    occupied = own | enemy
    dr = 1 if side == W else -1
    start_rank = 2 if side == W else 7
    victim_rank = 5 if side == W else 4
    enemy_side = other(side)

    for source in bits(own):
        file, rank = source % n, source // n + 1
        next_rank = rank + dr
        if not 1 <= next_rank <= 8:
            continue

        for target_file in ((file - 1) % n, (file + 1) % n):
            target = square(target_file, next_rank - 1, n)
            if enemy & (1 << target):
                new_own = (own ^ (1 << source)) | (1 << target)
                new_enemy = enemy ^ (1 << target)
                yield ((new_own, new_enemy, None) if side == W else
                       (new_enemy, new_own, None))
            elif (ep is not None and ep[0] == enemy_side and ep[1] == target_file
                  and rank == victim_rank):
                victim = square(target_file, rank - 1, n)
                if enemy & (1 << victim) and not occupied & (1 << target):
                    new_own = (own ^ (1 << source)) | (1 << target)
                    new_enemy = enemy ^ (1 << victim)
                    yield ((new_own, new_enemy, None) if side == W else
                           (new_enemy, new_own, None))

        forward = square(file, next_rank - 1, n)
        if occupied & (1 << forward):
            continue
        new_own = (own ^ (1 << source)) | (1 << forward)
        new_enemy = enemy
        new_ep = None
        if rank == start_rank:
            double_rank = rank + 2 * dr
            double = square(file, double_rank - 1, n)
            if 1 <= double_rank <= 8 and not occupied & (1 << double):
                double_own = (own ^ (1 << source)) | (1 << double)
                if any(enemy & (1 << square((file + df) % n, double_rank - 1, n))
                       for df in (-1, 1)):
                    new_ep = (side, file)
                yield ((double_own, new_enemy, new_ep) if side == W else
                       (new_enemy, double_own, new_ep))
        yield ((new_own, new_enemy, new_ep) if side == W else
               (new_enemy, new_own, new_ep))


def game(n, ep_on_heap):
    board = Board(n, 8, True, True)

    @lru_cache(None)
    def passers(white, black, ep):
        pos = Pos(coords(white, n), coords(black, n), library_ep(ep))
        return passed(board, pos, W), passed(board, pos, B)

    @lru_cache(None)
    def terminal_winner(white, black, ep, side_to_move):
        wp, bp = passers(white, black, ep)
        if not wp and not bp:
            return None
        if wp and not bp:
            return W
        if bp and not wp:
            return B
        # In a race, only front pawns on their files count toward each side's
        # shortest promotion distance. Each candidate is checked with `passed`.
        def distance(side):
            own, enemy = (white, black) if side == W else (black, white)
            by_file = {}
            for i in bits(own):
                f, r = i % n, i // n + 1
                if f not in by_file or (r > by_file[f] if side == W else r < by_file[f]):
                    by_file[f] = r
            best = None
            for f, r in by_file.items():
                pos = (Pos(frozenset({(f, r)}), coords(enemy, n), library_ep(ep)) if side == W
                       else Pos(coords(enemy, n), frozenset({(f, r)}), library_ep(ep)))
                if passed(board, pos, side):
                    d = (8 - r - (r == 2)) if side == W else (r - 1 - (r == 7))
                    best = d if best is None else min(best, d)
            assert best is not None
            return best

        wd, bd = distance(W), distance(B)
        if wd < bd:
            return W
        if bd < wd:
            return B
        return side_to_move

    @lru_cache(None)
    def wins(white, black, ep, side, heap):
        winner = terminal_winner(white, black, ep, side)
        if winner is not None:
            return winner == side
        for child in children(n, white, black, ep, side):
            if not wins(*child, other(side), heap):
                return True
        next_ep = ep if ep_on_heap else None
        for smaller_heap in range(heap):
            if not wins(white, black, next_ep, other(side), smaller_heap):
                return True
        return False

    def signature(position, heap):
        white, black, ep = position
        left = wins(white, black, ep, W, heap)
        right = wins(white, black, ep, B, heap)
        return "N" if left and right else "L" if left else "R" if right else "P"

    def signatures(position):
        return "".join(signature(position, h) for h in range(4))

    def state_count():
        return wins.cache_info().currsize

    return signatures, passers, state_count


def self_check():
    board = Board(8, 8, True, True)
    white, black = frozenset({(0, 4)}), frozenset({(1, 4)})
    assert passed(board, Pos(white, black), W)
    assert not passed(board, Pos(white, black, ((0, 3), (0, 4), B)), W)
    w, b, ep = 1 << square(0, 3, 8), 1 << square(1, 3, 8), (W, 0)
    assert any(not child_w and child_b & (1 << square(0, 2, 8))
               for child_w, child_b, _ in children(8, w, b, ep, B))
    empty_game, _, _ = game(8, False)
    assert empty_game((0, 0, None))[:2] == "PN"


def main():
    self_check()
    for moved_b7 in (False, True):
        label = "b7-to-b6" if moved_b7 else "P"
        sizes = (8, 10, 12) if moved_b7 else range(8, 25, 2)
        for n in sizes:
            position = start(n, moved_b7)
            print(f"{label} n={n} pawns={position[0].bit_count()+position[1].bit_count()}")
            for ep_on_heap in (False, True):
                solve, passers, state_count = game(n, ep_on_heap)
                assert passers(*position) == (False, False), (label, n, passers(*position))
                began = perf_counter()
                sig = solve(position)
                variant = "expire" if not ep_on_heap else "keep"
                print(f"  ep={variant} h=0..3 {sig} states={state_count()} seconds={perf_counter()-began:.2f}")


if __name__ == "__main__":
    main()
