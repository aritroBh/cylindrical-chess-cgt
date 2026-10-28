"""Independent whole-board pawn-game check for the odd n+2 ring families.

Uses only Python's standard library. Move generation, en passant, passed
pawns, races, minimax, and the reduced graph are implemented from the brief.
"""

from collections import Counter, deque
from functools import lru_cache
from time import perf_counter

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
                target = 1 << square(file, int(char), n)
                if side == W:
                    white |= target
                else:
                    black |= target
    return white, black, None


def start(n, family, lower_b7=False):
    assert n >= 9 and family in ("R", "Qo")
    tokens = ["W4" if family == "Qo" else "W5", "B6" if lower_b7 else "B7"]
    for file in range(2, n - 6):
        tokens.append("W2" if file % 2 == 0 else "B4")
    tokens.extend(("W3B6", "W3", "W2B5", "B5", "W2", "B4"))
    return parse_files(tokens, n)


def pawn_ep_capturable(n, enemy, side, file, rank, ep):
    if ep is None or ep != (side, file) or rank != (4 if side == W else 5):
        return False
    return any(enemy & (1 << square((file + df) % n, rank, n)) for df in (-1, 1))


def pawn_is_passed(n, enemy, side, file, rank, ep):
    near_files = {(file - 1) % n, file, (file + 1) % n}
    for target in bits(enemy):
        enemy_file, enemy_rank = target % n, target // n + 1
        if enemy_file in near_files and (enemy_rank > rank if side == W else enemy_rank < rank):
            return False
    return not pawn_ep_capturable(n, enemy, side, file, rank, ep)


def make_engine(n, ep_on_heap):
    @lru_cache(None)
    def passers(pos):
        result = []
        for side, own, enemy in ((W, pos[0], pos[1]), (B, pos[1], pos[0])):
            found = False
            for square_index in bits(own):
                file, rank = square_index % n, square_index // n + 1
                if pawn_is_passed(n, enemy, side, file, rank, pos[2]):
                    found = True
                    break
            result.append(found)
        return tuple(result)

    def promotion_distance(pos, side):
        own, enemy = (pos[0], pos[1]) if side == W else (pos[1], pos[0])
        ranks_by_file = {}
        for square_index in bits(own):
            file, rank = square_index % n, square_index // n + 1
            if file not in ranks_by_file:
                ranks_by_file[file] = []
            ranks_by_file[file].append(rank)
        best = None
        for file, own_ranks in ranks_by_file.items():
            front_rank = max(own_ranks) if side == W else min(own_ranks)
            for rank in own_ranks:
                if rank != front_rank or not pawn_is_passed(n, enemy, side, file, rank, pos[2]):
                    continue
                distance = 8 - rank - (rank == 2) if side == W else rank - 1 - (rank == 7)
                best = distance if best is None else min(best, distance)
        return 10**6 if best is None else best

    @lru_cache(None)
    def terminal_winner(pos, side_to_move):
        white_passed, black_passed = passers(pos)
        if not white_passed and not black_passed:
            return None
        if white_passed != black_passed:
            return W if white_passed else B
        white_distance = promotion_distance(pos, W)
        black_distance = promotion_distance(pos, B)
        if white_distance < black_distance:
            return W
        if black_distance < white_distance:
            return B
        return side_to_move  # count rule: a tie goes to the side that did not just move

    def children(pos, side, only_file=None):
        own, enemy = (pos[0], pos[1]) if side == W else (pos[1], pos[0])
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
                elif (pos[2] is not None and pos[2][0] == enemy_side
                      and pos[2][1] == target_file and rank == ep_victim_rank):
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

    @lru_cache(None)
    def classify(pos, side, child):
        winner = terminal_winner(child, other(side))
        if winner is not None:
            return "T" if winner == side else "L"
        for reply in children(child, other(side)):
            if terminal_winner(reply, side) == other(side):
                return "P"
        return "K"

    def signature(pos, heap_max=5):
        outcomes = []
        for heap in range(heap_max):
            left_wins = wins(pos, W, heap)
            right_wins = wins(pos, B, heap)
            outcomes.append("N" if left_wins and right_wins else
                            "L" if left_wins else "R" if right_wins else "P")
        return "".join(outcomes)

    return {
        "passers": passers,
        "terminal_winner": terminal_winner,
        "children": children,
        "wins": wins,
        "classify": classify,
        "signature": signature,
    }


def reduced_graph(engine, root):
    nodes = {root}
    pending = deque([root])
    options = {}
    while pending:
        pos = pending.popleft()
        by_side = {}
        for side in SIDES:
            k_children, t_children = set(), set()
            for child in engine["children"](pos, side):
                kind = engine["classify"](pos, side, child)
                if kind == "K":
                    k_children.add(child)
                    if child not in nodes:
                        nodes.add(child)
                        pending.append(child)
                elif kind == "T":
                    t_children.add(child)
            by_side[side] = (frozenset(k_children), frozenset(t_children))
        options[pos] = by_side
    return {"root": root, "nodes": frozenset(nodes), "options": options}


def reduced_signature(graph, heap_max=5):
    @lru_cache(None)
    def wins(pos, side, heap):
        k_children, t_children = graph["options"][pos][side]
        if t_children:
            return True
        for child in k_children:
            if not wins(child, other(side), heap):
                return True
        for smaller_heap in range(heap):
            if not wins(pos, other(side), smaller_heap):
                return True
        return False

    output = []
    for heap in range(heap_max):
        left_wins = wins(graph["root"], W, heap)
        right_wins = wins(graph["root"], B, heap)
        output.append("N" if left_wins and right_wins else
                      "L" if left_wins else "R" if right_wins else "P")
    return "".join(output)


def insertion_after_6(pos, old_n):
    new_n = old_n + 2
    new_white = new_black = 0
    for side, mask in ((W, pos[0]), (B, pos[1])):
        for source in bits(mask):
            file, rank = source % old_n, source // old_n + 1
            target_file = file if file <= 6 else file + 2
            target = 1 << square(target_file, rank, new_n)
            if side == W:
                new_white |= target
            else:
                new_black |= target
    # New files 7 and 8 copy old files 7 (B4) and 6 (W2), respectively.
    for new_file, old_file in ((7, 7), (8, 6)):
        for side, mask in ((W, pos[0]), (B, pos[1])):
            for source in bits(mask):
                file, rank = source % old_n, source // old_n + 1
                if file != old_file:
                    continue
                target = 1 << square(new_file, rank, new_n)
                if side == W:
                    new_white |= target
                else:
                    new_black |= target
    ep = None if pos[2] is None else (pos[2][0], pos[2][1] if pos[2][1] <= 6 else pos[2][1] + 2)
    return new_white, new_black, ep


def graph_edges(graph, kind):
    return frozenset(
        (source, side, child)
        for source, by_side in graph["options"].items()
        for side, (k_children, t_children) in by_side.items()
        for child in (k_children if kind == "K" else t_children)
    )


def graph_summary(engine, graph, family, n):
    root = graph["root"]
    zone = set()
    for file in range(n):
        initial = file_content(root, file, n)
        if any(file_content(pos, file, n) != initial for pos in graph["nodes"]):
            zone.add(file)
    k_edges = graph_edges(graph, "K")
    t_edges = graph_edges(graph, "T")
    t_pairs = sum(bool(graph["options"][pos][side][1])
                  for pos in graph["nodes"] for side in SIDES)
    assert all(pos[2] is None for pos in graph["nodes"])
    assert all(engine["passers"](pos) == (False, False) for pos in graph["nodes"])
    assert all(file_content(pos, file, n) == file_content(root, file, n)
               for pos in graph["nodes"] for file in range(2, 12))
    expected_zone = set(range(n - 7, n - 2)) | {n - 1}
    if family == "Qo":
        expected_zone |= {0, 1}
    assert zone == expected_zone, (family, n, zone, expected_zone)
    expected_counts = (429, 805, 653, 277) if family == "R" else (1287, 2996, 1959, 831)
    summary = (len(graph["nodes"]), len(k_edges), len(t_edges), t_pairs)
    assert summary == expected_counts, (family, n, summary, expected_counts)
    return {"nodes": summary[0], "K": summary[1], "T": summary[2],
            "T_node_side_pairs": summary[3], "zone": sorted(zone)}


def check_wall_lemma(engine, graph, n, family):
    assert n == 19
    positions, moves = Counter(), Counter()
    for pos in graph["nodes"]:
        for file in range(3, 11):
            expected_side = W if file % 2 == 0 else B
            own = pos[expected_side]
            rank_squares = [s for s in bits(own) if s % n == file]
            assert len(rank_squares) == 1, (file, rank_squares)
            positions[file] += 1
            for side in SIDES:
                if side != expected_side:
                    continue
                for child in engine["children"](pos, side, only_file=file):
                    moves[(file, engine["classify"](pos, side, child))] += 1
                    assert not engine["passers"](child)[side], (file, side, child)
                    assert engine["classify"](pos, side, child) in ("L", "P"), (file, side, child)
    assert all(positions[file] == len(graph["nodes"]) for file in range(3, 11))
    assert moves[(3, "P")] == len(graph["nodes"]) and moves[(3, "L")] == 0
    expected_l, expected_p = (18, 840) if family == "R" else (54, 2520)
    assert moves[(10, "L")] == expected_l and moves[(10, "P")] == expected_p
    assert not any(kind in ("T", "K") for (file, kind), count in moves.items() if count)
    return positions, moves


def check_insertion(family, graph19, graph21):
    root19, root21 = graph19["root"], graph21["root"]
    assert insertion_after_6(root19, 19) == root21
    mapped_nodes = frozenset(insertion_after_6(pos, 19) for pos in graph19["nodes"])
    assert mapped_nodes == graph21["nodes"], family
    for kind in ("K", "T"):
        mapped_edges = frozenset(
            (insertion_after_6(src, 19), side, insertion_after_6(dst, 19))
            for src, side, dst in graph_edges(graph19, kind)
        )
        assert mapped_edges == graph_edges(graph21, kind), (family, kind)


def self_check():
    n = 8
    white = 1 << square(0, 4, n)
    black = 1 << square(1, 4, n)
    assert pawn_is_passed(n, black, W, 0, 4, None)
    assert not pawn_is_passed(n, black, W, 0, 4, (W, 0))
    ep_child = next(child for child in make_engine(n, False)["children"]((white, black, (W, 0)), B)
                    if child[0] == 0 and child[1] == 1 << square(0, 3, n))
    assert ep_child[2] is None
    empty = (0, 0, None)
    assert make_engine(n, False)["signature"](empty, 2) == "PN"


def main():
    self_check()
    print("Engine: standard-library whole-board minimax; custom moves, EP-aware passers, count race.")
    print("EP-on-heap modes: expire (immediate-turn rule) and keep (sum convention).")
    print("n | R expire | R keep | Qo expire | Qo keep | states expire R/Qo")
    base_engines = {}
    for n in range(9, 24, 2):
        row = []
        for family in ("R", "Qo"):
            position = start(n, family)
            assert (position[0].bit_count() + position[1].bit_count()) == n + 2
            expire = make_engine(n, False)
            expire_started = perf_counter()
            signature_expire = expire["signature"](position, 5)
            expire_states = expire["wins"].cache_info().currsize
            keep = make_engine(n, True)
            signature_keep = keep["signature"](position, 5)
            keep_states = keep["wins"].cache_info().currsize
            assert signature_expire == signature_keep, (family, n, signature_expire, signature_keep)
            if n == 9:
                assert signature_expire == "LLLLL", (family, signature_expire)
            else:
                expected = "NNPNN" if family == "R" else "NNNPN"
                assert signature_expire == expected, (family, n, signature_expire, expected)
            row.append((signature_expire, signature_keep, expire_states, keep_states))
            if n == 19:
                base_engines[family] = expire
            elapsed = perf_counter() - expire_started
            print(f"{family} n={n}: {signature_expire}/{signature_keep} states={expire_states}/{keep_states} "
                  f"seconds={perf_counter() - expire_started:.2f}")
            del expire, keep
        print(f"  row R={row[0][0]} Qo={row[1][0]}")

    base_graphs = {}
    for family in ("R", "Qo"):
        engine19 = base_engines[family]
        graph19 = reduced_graph(engine19, start(19, family))
        summary19 = graph_summary(engine19, graph19, family, 19)
        signature19 = reduced_signature(graph19, 5)
        expected = "NNPNN" if family == "R" else "NNNPN"
        assert signature19 == expected
        assert engine19["signature"](graph19["root"], 5) == signature19

        engine21 = make_engine(21, False)
        graph21 = reduced_graph(engine21, start(21, family))
        summary21 = graph_summary(engine21, graph21, family, 21)
        check_insertion(family, graph19, graph21)
        positions, moves = check_wall_lemma(engine19, graph19, 19, family)
        assert summary21["nodes"] == summary19["nodes"]
        base_graphs[family] = (graph19, graph21)
        print(f"{family} reduced n=19: {summary19}; signature={signature19}")
        print(f"{family} reduced n=21: {summary21}; ins_6 node/K/T mapping=exact")
        print(f"{family} Lemma 2 on n=19 files 3..10: positions={sum(positions.values())}, "
              f"moves={sum(moves.values())}, failures=0, j=3 P={moves[(3, 'P')]}, "
              f"j=10 L/P={moves[(10, 'L')]}/{moves[(10, 'P')]}")

    # One structurally nearby control: lower the file-1 B7 pawn to B6.
    control = start(19, "R", lower_b7=True)
    control_engine = make_engine(19, False)
    control_signature = control_engine["signature"](control, 5)
    assert control_signature != "NNPNN", control_signature
    print(f"control R19 with file-1 B7 lowered to B6: {control_signature} "
          f"(not NNPNN; states={control_engine['wins'].cache_info().currsize})")
    print("All independent checker assertions passed.")


if __name__ == "__main__":
    main()
