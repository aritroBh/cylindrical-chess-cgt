"""Independent whole-board pawn-game engine for C_n (adapted from research/ring_n_plus_2_check/odd/independent.py)."""
from functools import lru_cache
from time import perf_counter

W, B = 0, 1


def other(side):
    return B if side == W else W


def square(file, rank, n):
    return (rank - 1) * n + file


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def parse_ring(tokens, n):
    """tokens: list of strings like 'W4', 'B7', 'W2B5'. Return (white_mask, black_mask, None)."""
    white = black = 0
    assert len(tokens) == n, (len(tokens), n)
    for file, tok in enumerate(tokens):
        # A token may contain several W/B groups; ranks for each side.
        i = 0
        side = None
        num = ""
        groups = []
        for ch in tok:
            if ch in "WB":
                if num:
                    groups.append((side, int(num)))
                    num = ""
                side = W if ch == "W" else B
            else:
                num += ch
        if num:
            groups.append((side, int(num)))
        for side, rank in groups:
            idx = square(file, rank, n)
            if side == W:
                white |= 1 << idx
            else:
                black |= 1 << idx
    return white, black, None


def colour_reverse_tokens(tokens):
    out = []
    for tok in tokens:
        # swap colours and rank r -> 9-r
        # parse groups
        groups = []
        i = 0
        side = None
        num = ""
        for ch in tok:
            if ch in "WB":
                if num:
                    groups.append((side, int(num)))
                    num = ""
                side = W if ch == "W" else B
            else:
                num += ch
        if num:
            groups.append((side, int(num)))
        new_groups = []
        for side, rank in groups:
            new_groups.append((other(side), 9 - rank))
        # rebuild token with W groups then B groups? Keep original side order not matter; combine
        w_ranks = sorted(r for s, r in new_groups if s == W)
        b_ranks = sorted(r for s, r in new_groups if s == B)
        t = ""
        if w_ranks:
            t += "W" + "".join(map(str, w_ranks))
        if b_ranks:
            t += "B" + "".join(map(str, b_ranks))
        out.append(t)
    return out


def pawn_is_passed(n, enemy, side, file, rank, ep):
    near_files = {(file - 1) % n, file, (file + 1) % n}
    for target in bits(enemy):
        enemy_file, enemy_rank = target % n, target // n + 1
        if enemy_file in near_files and (enemy_rank > rank if side == W else enemy_rank < rank):
            return False
    # ep capturable: mover (side) just double-stepped this pawn; enemy on adjacent file same rank
    if ep is not None and ep[0] == side and ep[1] == file and rank == (4 if side == W else 5):
        if any(enemy & (1 << square((file + df) % n, rank, n)) for df in (-1, 1)):
            return False
    return True


def make_engine(n, ep_on_heap):
    @lru_cache(None)
    def passers(pos):
        white, black, ep = pos
        res = []
        for side, own, enemy in ((W, white, black), (B, black, white)):
            found = False
            for sq in bits(own):
                file, rank = sq % n, sq // n + 1
                if pawn_is_passed(n, enemy, side, file, rank, ep):
                    found = True
                    break
            res.append(found)
        return tuple(res)

    def promotion_distance(pos, side):
        white, black, ep = pos
        own, enemy = (white, black) if side == W else (black, white)
        ranks_by_file = {}
        for sq in bits(own):
            file, rank = sq % n, sq // n + 1
            ranks_by_file.setdefault(file, []).append(rank)
        best = None
        for file, own_ranks in ranks_by_file.items():
            front_rank = max(own_ranks) if side == W else min(own_ranks)
            for rank in own_ranks:
                if rank != front_rank:
                    continue
                if not pawn_is_passed(n, enemy, side, file, rank, ep):
                    continue
                distance = 8 - rank - (1 if rank == 2 else 0) if side == W else rank - 1 - (1 if rank == 7 else 0)
                best = distance if best is None else min(best, distance)
        return 10**6 if best is None else best

    @lru_cache(None)
    def terminal_winner(pos, side_to_move):
        white, black, ep = pos
        wp, bp = passers(pos)
        if not wp and not bp:
            return None
        if wp != bp:
            return W if wp else B
        wd = promotion_distance(pos, W)
        bd = promotion_distance(pos, B)
        if wd < bd:
            return W
        if bd < wd:
            return B
        return side_to_move

    def children(pos, side):
        white, black, ep = pos
        own, enemy = (white, black) if side == W else (black, white)
        occupied = own | enemy
        direction = 1 if side == W else -1
        start_rank = 2 if side == W else 7
        ep_victim_rank = 5 if side == W else 4
        enemy_side = other(side)
        seen = set()

        def emit(new_own, new_enemy, new_ep):
            if side == W:
                child = (new_own, new_enemy, new_ep)
            else:
                child = (new_enemy, new_own, new_ep)
            if child in seen:
                return None
            seen.add(child)
            return child

        for source in bits(own):
            file, rank = source % n, source // n + 1
            next_rank = rank + direction
            if not 1 <= next_rank <= 8:
                continue
            for target_file in ((file - 1) % n, (file + 1) % n):
                target = 1 << square(target_file, next_rank, n)
                if enemy & target:
                    child = emit(own ^ (1 << source) | target, enemy ^ target, None)
                    if child is not None:
                        yield child
                elif (ep is not None and ep[0] == enemy_side and ep[1] == target_file and rank == ep_victim_rank):
                    victim = 1 << square(target_file, rank, n)
                    if enemy & victim and not (occupied & target):
                        child = emit(own ^ (1 << source) | target, enemy ^ victim, None)
                        if child is not None:
                            yield child
            forward = 1 << square(file, next_rank, n)
            if occupied & forward:
                continue
            child = emit(own ^ (1 << source) | forward, enemy, None)
            if child is not None:
                yield child
            if rank == start_rank:
                double_rank = rank + 2 * direction
                double = 1 << square(file, double_rank, n)
                if not (occupied & double):
                    live_ep = any(enemy & (1 << square((file + df) % n, double_rank, n)) for df in (-1, 1))
                    new_ep = (side, file) if live_ep else None
                    child = emit(own ^ (1 << source) | double, enemy, new_ep)
                    if child is not None:
                        yield child

    @lru_cache(None)
    def wins(pos, side, heap):
        winner = terminal_winner(pos, side)
        if winner is not None:
            return winner == side
        for child in children(pos, side):
            if not wins(child, other(side), heap):
                return True
        heap_ep = pos[2] if ep_on_heap else None
        for smaller_heap in range(heap):
            if not wins((pos[0], pos[1], heap_ep), other(side), smaller_heap):
                return True
        return False

    def signature(pos, heap_max=4):
        out = []
        for heap in range(heap_max):
            left = wins(pos, W, heap)
            right = wins(pos, B, heap)
            out.append("N" if left and right else "L" if left else "R" if right else "P")
        return "".join(out)

    return {
        "passers": passers,
        "terminal_winner": terminal_winner,
        "children": children,
        "wins": wins,
        "signature": signature,
    }


def self_check():
    n = 8
    white = 1 << square(0, 4, n)
    black = 1 << square(1, 4, n)
    assert pawn_is_passed(n, black, W, 0, 4, None)
    assert not pawn_is_passed(n, black, W, 0, 4, (W, 0))
    empty = (0, 0, None)
    eng = make_engine(n, False)
    assert eng["signature"](empty, 2) == "PN"


if __name__ == "__main__":
    self_check()
    print("engine self-check ok")
