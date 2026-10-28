"""Independent finite checks for the M_n and O_n insertion proof.

Only the standard library is used. The move generator, en-passant handling,
passed-pawn/race test, whole-board minimax, and reduced graph are implemented
here from the task's stated rules; no project solver is imported.
"""

from collections import Counter, deque
from functools import lru_cache

W, B = 0, 1
SIDES = (W, B)


def other(side):
    return B if side == W else W


def square(file, rank, n):
    return (rank - 1) * n + file


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def file_content(pos, file, n):
    mask = sum(1 << square(file, rank, n) for rank in range(1, 9))
    return pos[0] & mask, pos[1] & mask


def parse_files(tokens, n):
    assert len(tokens) == n
    white = black = 0
    for file, token in enumerate(tokens):
        side = None
        for char in token:
            if char == "W":
                side = W
            elif char == "B":
                side = B
            else:
                assert side is not None and char in "12345678", token
                bit = 1 << square(file, int(char), n)
                if side == W:
                    white |= bit
                else:
                    black |= bit
    return white, black, None


def start(n, family):
    if family == "M":
        assert n >= 10 and n % 2 == 0
        tokens = ["B4", "W2"] * ((n - 8) // 2)
        tokens += ["B6", "W2", "W3", "B6", "B7", "W3", "B7", "W5"]
    else:
        assert family == "O" and n >= 11 and n % 2 == 1
        tokens = ["B4"] + ["B7", "W5"] * ((n - 9) // 2)
        tokens += ["B7", "W3", "B7", "B6", "W3", "W2", "B6", "W2"]
    assert len(tokens) == n
    pos = parse_files(tokens, n)
    assert pos[0].bit_count() + pos[1].bit_count() == n
    return pos


def ep_capturable(n, enemy, side, file, rank, ep):
    if ep is None or ep != (side, file) or rank != (4 if side == W else 5):
        return False
    return any(enemy & (1 << square((file + df) % n, rank, n)) for df in (-1, 1))


def is_passed(n, enemy, side, file, rank, ep):
    near = {(file - 1) % n, file, (file + 1) % n}
    for sq in bits(enemy):
        enemy_file, enemy_rank = sq % n, sq // n + 1
        ahead = enemy_rank > rank if side == W else enemy_rank < rank
        if enemy_file in near and ahead:
            return False
    return not ep_capturable(n, enemy, side, file, rank, ep)


def make_engine(n, keep_ep_on_heap=False):
    @lru_cache(None)
    def passers(pos):
        found = []
        for side in SIDES:
            own, enemy = pos[side], pos[other(side)]
            found.append(any(
                is_passed(n, enemy, side, sq % n, sq // n + 1, pos[2])
                for sq in bits(own)
            ))
        return tuple(found)

    def promotion_distance(pos, side):
        own, enemy = pos[side], pos[other(side)]
        by_file = {}
        for sq in bits(own):
            file, rank = sq % n, sq // n + 1
            by_file.setdefault(file, []).append(rank)
        best = None
        for file, ranks in by_file.items():
            front = max(ranks) if side == W else min(ranks)
            if not is_passed(n, enemy, side, file, front, pos[2]):
                continue
            distance = 8 - front - (front == 2) if side == W else front - 1 - (front == 7)
            best = distance if best is None else min(best, distance)
        return 10**6 if best is None else best

    @lru_cache(None)
    def terminal_winner(pos, side_to_move):
        wp, bp = passers(pos)
        if not wp and not bp:
            return None
        if wp != bp:
            return W if wp else B
        dw, db = promotion_distance(pos, W), promotion_distance(pos, B)
        if dw < db:
            return W
        if db < dw:
            return B
        return side_to_move  # count race: a tied race goes to the non-mover.

    def children(pos, side, only_file=None):
        own, enemy = pos[side], pos[other(side)]
        occupied = own | enemy
        direction = 1 if side == W else -1
        start_rank = 2 if side == W else 7
        victim_rank = 5 if side == W else 4
        seen = set()

        def emit(new_own, new_enemy, new_ep):
            child = (new_own, new_enemy, new_ep) if side == W else (new_enemy, new_own, new_ep)
            if child not in seen:
                seen.add(child)
                return child
            return None

        for source in bits(own):
            file, rank = source % n, source // n + 1
            if only_file is not None and file != only_file:
                continue
            next_rank = rank + direction
            if not 1 <= next_rank <= 8:
                continue
            for target_file in ((file - 1) % n, (file + 1) % n):
                target = 1 << square(target_file, next_rank, n)
                if enemy & target:
                    child = emit(own ^ (1 << source) | target, enemy ^ target, None)
                    if child is not None:
                        yield child
                elif (pos[2] is not None and pos[2][0] == other(side)
                      and pos[2][1] == target_file and rank == victim_rank):
                    victim = 1 << square(target_file, rank, n)
                    if enemy & victim and not occupied & target:
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
                if not occupied & double:
                    live_ep = any(
                        enemy & (1 << square((file + df) % n, double_rank, n))
                        for df in (-1, 1)
                    )
                    child = emit(own ^ (1 << source) | double, enemy,
                                 (side, file) if live_ep else None)
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
        heap_pos = pos if keep_ep_on_heap else (pos[0], pos[1], None)
        for smaller in range(heap):
            if not wins(heap_pos, other(side), smaller):
                return True
        return False

    @lru_cache(None)
    def classify(pos, side, child):
        winner = terminal_winner(child, other(side))
        if winner is not None:
            return "T" if winner == side else "L"
        for reply in children(child, other(side)):
            if terminal_winner(reply, side) == other(side):
                return "P"
        return "K"

    def signature(pos, heap_count=5):
        result = []
        for heap in range(heap_count):
            left = wins(pos, W, heap)
            right = wins(pos, B, heap)
            result.append("N" if left and right else "L" if left else "R" if right else "P")
        return "".join(result)

    return {"passers": passers, "terminal_winner": terminal_winner,
            "children": children, "wins": wins, "classify": classify,
            "signature": signature}


def reduced_graph(engine, root):
    nodes, pending, options = {root}, deque([root]), {}
    while pending:
        pos = pending.popleft()
        by_side = {}
        for side in SIDES:
            ks, ts = set(), set()
            for child in engine["children"](pos, side):
                kind = engine["classify"](pos, side, child)
                if kind == "K":
                    ks.add(child)
                    if child not in nodes:
                        nodes.add(child)
                        pending.append(child)
                elif kind == "T":
                    ts.add(child)
            by_side[side] = (frozenset(ks), frozenset(ts))
        options[pos] = by_side
    return {"root": root, "nodes": frozenset(nodes), "options": options}


def edges(graph, kind):
    return frozenset(
        (src, side, dst)
        for src, by_side in graph["options"].items()
        for side, (ks, ts) in by_side.items()
        for dst in (ks if kind == "K" else ts)
    )


def reduced_signature(graph, heap_count=5):
    @lru_cache(None)
    def wins(pos, side, heap):
        ks, ts = graph["options"][pos][side]
        if ts:
            return True
        if any(not wins(child, other(side), heap) for child in ks):
            return True
        return any(not wins(pos, other(side), smaller) for smaller in range(heap))

    out = []
    for heap in range(heap_count):
        left, right = wins(graph["root"], W, heap), wins(graph["root"], B, heap)
        out.append("N" if left and right else "L" if left else "R" if right else "P")
    return "".join(out)


def expected_zone(family, n):
    if family == "M":
        return set(range(n - 8, n - 2)) | {n - 1}
    return {0} | set(range(n - 7, n))


def graph_summary(engine, graph, family, n, arc):
    root, nodes = graph["root"], graph["nodes"]
    zone = {f for f in range(n)
            if any(file_content(p, f, n) != file_content(root, f, n) for p in nodes)}
    ke, te = edges(graph, "K"), edges(graph, "T")
    t_pairs = sum(bool(graph["options"][p][side][1]) for p in nodes for side in SIDES)
    assert all(p[2] is None for p in nodes)
    assert all(engine["passers"](p) == (False, False) for p in nodes)
    assert zone == expected_zone(family, n), (family, n, sorted(zone))
    assert all(file_content(p, f, n) == file_content(root, f, n) for p in nodes for f in arc)
    assert all(file_content(p, f, n) == file_content(root, f, n)
               for p in nodes for f in range(n) if f not in zone)
    return {"nodes": len(nodes), "K": len(ke), "T": len(te),
            "T_pairs": t_pairs, "zone": sorted(zone),
            "signature": reduced_signature(graph, 5)}


def insert(pos, c, old_n):
    new_n = old_n + 2
    white = black = 0
    for side in SIDES:
        for source in bits(pos[side]):
            file, rank = source % old_n, source // old_n + 1
            target_file = file if file <= c else file + 2
            target = 1 << square(target_file, rank, new_n)
            if side == W:
                white |= target
            else:
                black |= target
    for target_file, source_file in ((c + 1, c + 1), (c + 2, c)):
        for side in SIDES:
            for source in bits(pos[side]):
                file, rank = source % old_n, source // old_n + 1
                if file == source_file:
                    target = 1 << square(target_file, rank, new_n)
                    if side == W:
                        white |= target
                    else:
                        black |= target
    ep = None
    if pos[2] is not None:
        side, file = pos[2]
        ep = (side, file if file <= c else file + 2)
    return white, black, ep


def check_insertion(family, c, old_graph, new_graph, old_n):
    assert insert(old_graph["root"], c, old_n) == new_graph["root"]
    image_nodes = frozenset(insert(p, c, old_n) for p in old_graph["nodes"])
    assert image_nodes == new_graph["nodes"]
    for kind in ("K", "T"):
        image_edges = frozenset(
            (insert(src, c, old_n), side, insert(dst, c, old_n))
            for src, side, dst in edges(old_graph, kind)
        )
        assert image_edges == edges(new_graph, kind), (family, old_n, kind)


def check_wall_moves(engine, graph, family, n, c):
    # Every central pawn has a 5-file window inside the 10-file Lemma-3 arc.
    checked_positions, checked_moves = Counter(), Counter()
    lo, hi = c - 3, c + 4
    end_classes = {}
    for pos in graph["nodes"]:
        for file in range(lo, hi + 1):
            own_side = W if pos[0] & sum(1 << square(file, r, n) for r in range(1, 9)) else B
            own_bits = [sq for sq in bits(pos[own_side]) if sq % n == file]
            assert len(own_bits) == 1
            checked_positions[file] += 1
            for child in engine["children"](pos, own_side, only_file=file):
                assert child[other(own_side)] == pos[other(own_side)], ("wall capture", file)
                assert not engine["passers"](child)[own_side], ("Lemma 2(a)", file)
                kind = engine["classify"](pos, own_side, child)
                assert kind in ("L", "P"), ("Lemma 2(b)", file, kind)
                checked_moves[file, kind] += 1
                if file in (lo, hi):
                    end_classes.setdefault(file, Counter())[kind] += 1
    assert all(checked_positions[f] == len(graph["nodes"]) for f in range(lo, hi + 1))
    return checked_positions, checked_moves, end_classes


def self_check():
    n = 8
    white = 1 << square(0, 4, n)
    black = 1 << square(1, 4, n)
    assert is_passed(n, black, W, 0, 4, None)
    assert not is_passed(n, black, W, 0, 4, (W, 0))
    ep_child = next(child for child in make_engine(n)["children"]((white, black, (W, 0)), B)
                    if child[0] == 0 and child[1] == 1 << square(0, 3, n))
    assert ep_child[2] is None
    assert make_engine(n)["signature"]((0, 0, None), 2) == "PN"
    pos = start(18, "M")
    assert pos[0].bit_count() + pos[1].bit_count() == 18


def main():
    self_check()
    print("Independent checker: stdlib-only rules implementation; e.p.-aware passers; count race.")
    for family, n0, c, arc in (("M", 18, 4, range(0, 10)), ("O", 19, 5, range(1, 11))):
        print(f"\n{family}: base n={n0}, insertion c={c}", flush=True)
        graphs = []
        for step in range(3):
            n = n0 + 2 * step
            engine = make_engine(n)
            graph = reduced_graph(engine, start(n, family))
            summary = graph_summary(engine, graph, family, n,
                                   range(c - 4, c + 6) if step == 0 else range(c - 4, c + 6 + 2 * step))
            graphs.append(graph)
            print(f"n={n}: {summary}", flush=True)
            if step == 0:
                positions, moves, ends = check_wall_moves(engine, graph, family, n, c)
                print(f"  Lemma 2: {sum(positions.values())} pawn-node pairs, "
                      f"{sum(moves.values())} moves; classes={dict(sorted(moves.items()))}; "
                      f"arc-end classes={{{', '.join(f'{j}: {dict(v)}' for j, v in sorted(ends.items()))}}}",
                      flush=True)
        for step in range(2):
            check_insertion(family, c, graphs[step], graphs[step + 1], n0 + 2 * step)
            print(f"  insertion n={n0 + 2 * step}->{n0 + 2 * step + 2}: "
                  "root, node set, K edges, and T edges map bijectively", flush=True)

    print("\nDirect full-game searches below n0 (h=0..4):", flush=True)
    for family, ns in (("M", (10, 12, 14, 16)), ("O", (11, 13, 15, 17))):
        for n in ns:
            signatures = []
            for keep in (False, True):
                engine = make_engine(n, keep_ep_on_heap=keep)
                sig = engine["signature"](start(n, family), 5)
                states = engine["wins"].cache_info().currsize
                assert sig == "NNPNN", (family, n, keep, sig)
                signatures.append(sig)
                print(f"{family} n={n} {'keep' if keep else 'expire'}={sig} states={states}", flush=True)
            assert signatures[0] == signatures[1]
    print("All independent assertions passed.", flush=True)


if __name__ == "__main__":
    main()
