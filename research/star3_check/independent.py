"""Independent whole-board pawn-game checks for the T/S star3 ring families.

Uses only Python's standard library. Move generation, en passant, passed
pawns, races, minimax, and the reduced graph are implemented from the brief.
"""

from collections import Counter, deque
from functools import lru_cache
from time import perf_counter
import argparse
import gc
import resource
import lzma
import os
import pickle
import sys

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


def start(n, family):
    """T/S rings as written in PROOF_S3T3.md, without project code."""
    if family == "T":
        assert n >= 12 and n % 2 == 0
        tokens = []
        for _ in range((n - 10) // 2):
            tokens.extend(("B4", "W2"))
        tokens.extend(("B5", "W2", "W6B7", "W3", "B7", "B6", "W3", "W2", "B6", "W2"))
    else:
        assert family == "S" and n >= 13 and n % 2 == 1
        tokens = ["B4", "B6", "W3"]
        for _ in range((n - 11) // 2):
            tokens.extend(("W2", "B4"))
        tokens.extend(("W6B7", "W3", "B7", "B6", "W3", "W2", "B6", "W2"))
    assert len(tokens) == n, (family, n, len(tokens))
    position = parse_files(tokens, n)
    assert position[0].bit_count() + position[1].bit_count() == n + 1
    return position


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
    def peak_rss_bytes():
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return peak if sys.platform == "darwin" else peak * 1024

    board_bits = 8 * n

    def position_code(pos):
        white, black, ep = pos
        code = white | (black << board_bits)
        if ep is not None:
            code |= (1 + ep[0] * n + ep[1]) << (2 * board_bits)
        return code

    passer_cache = {}

    def passers(pos):
        key = position_code(pos)
        if key in passer_cache:
            cached = passer_cache[key]
            return bool(cached & 1), bool(cached & 2)
        result = 0
        for side, own, enemy in ((W, pos[0], pos[1]), (B, pos[1], pos[0])):
            found = False
            for square_index in bits(own):
                file, rank = square_index % n, square_index // n + 1
                if pawn_is_passed(n, enemy, side, file, rank, pos[2]):
                    found = True
                    break
            if found:
                result |= 1 << side
        passer_cache[key] = result
        return bool(result & 1), bool(result & 2)

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

    win_cache = {}

    def wins(pos, side, heap):
        # One packed integer key avoids the nested tuple overhead of lru_cache.
        key = (position_code(pos) << 9) | (heap << 1) | side
        if key in win_cache:
            return win_cache[key]
        # Keep the shared-machine cap below 4 GB; poll every 200k states.
        if win_cache and len(win_cache) % 200_000 == 0:
            if peak_rss_bytes() > 3_400_000_000:
                raise MemoryError("whole-board search reached the 3.4 GB safety ceiling")
        winner = terminal_winner(pos, side)
        if winner is not None:
            result = winner == side
            win_cache[key] = result
            return result
        for child in children(pos, side):
            if not wins(child, other(side), heap):
                win_cache[key] = True
                return True
        heap_ep = pos[2] if ep_on_heap else None
        for smaller_heap in range(heap):
            if not wins((pos[0], pos[1], heap_ep), other(side), smaller_heap):
                win_cache[key] = True
                return True
        win_cache[key] = False
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
        "state_count": lambda: len(win_cache),
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


def insert_after(pos, old_n, cut):
    new_n = old_n + 2
    new_white = new_black = 0
    for side, mask in ((W, pos[0]), (B, pos[1])):
        for source in bits(mask):
            file, rank = source % old_n, source // old_n + 1
            target_file = file if file <= cut else file + 2
            target = 1 << square(target_file, rank, new_n)
            if side == W:
                new_white |= target
            else:
                new_black |= target
    # ponytail: duplicate the next two exact pattern files; no general remapper needed.
    for new_file, old_file in ((cut + 1, cut + 1), (cut + 2, cut + 2)):
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
    ep = None if pos[2] is None else (
        pos[2][0], pos[2][1] if pos[2][1] <= cut else pos[2][1] + 2
    )
    return new_white, new_black, ep


def graph_edges(graph, kind):
    return frozenset(
        (source, side, child)
        for source, by_side in graph["options"].items()
        for side, (k_children, t_children) in by_side.items()
        for child in (k_children if kind == "K" else t_children)
    )


def graph_summary(engine, graph, family, n, cut, step):
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
    arc_hi = cut + 5 + 2 * step
    arc = range(cut - 4, arc_hi + 1)
    for file in arc:
        initial = file_content(root, file, n)
        assert sum(part.bit_count() for part in initial) == 1, (family, n, file, initial)
        assert all(file_content(pos, file, n) == initial for pos in graph["nodes"]), (family, n, file)
    if family == "T":
        expected_zone = {n - 10, n - 9} | set(range(n - 7, n - 1))
        expected = (1305, 4018, 1212)
    else:
        expected_zone = {0, 1, 2, n - 10, n - 9} | set(range(n - 7, n))
        expected = (40445, 141252, 86822)
    assert zone == expected_zone, (family, n, zone, expected_zone)
    summary = (len(graph["nodes"]), len(k_edges), len(t_edges))
    assert summary == expected, (family, n, summary, expected)
    return {"nodes": summary[0], "K": summary[1], "T": summary[2],
            "T_node_side_pairs": t_pairs, "zone": sorted(zone), "arc": [arc.start, arc.stop - 1]}


def check_wall_lemma(engine, graph, n, family, cut, step):
    positions, moves, chosen_windows = Counter(), Counter(), {}
    arc_lo, arc_hi = cut - 4, cut + 5 + 2 * step
    last_central = cut + (4 if step == 0 else 6)
    central_files = range(cut - 3, last_central + 1)
    for pos in graph["nodes"]:
        for file in central_files:
            expected_side = (B if file % 2 == 0 else W) if family == "T" else (W if file % 2 else B)
            own = pos[expected_side]
            rank_squares = [s for s in bits(own) if s % n == file]
            assert len(rank_squares) == 1, (family, n, file, rank_squares)
            positions[file] += 1
            forward_window = (file - 1, file + 3)
            reverse_window = (file - 3, file + 1)
            if arc_lo <= forward_window[0] and forward_window[1] <= arc_hi:
                chosen_windows[file] = forward_window
            else:
                assert arc_lo <= reverse_window[0] and reverse_window[1] <= arc_hi, (
                    family, n, file, (arc_lo, arc_hi), forward_window, reverse_window
                )
                chosen_windows[file] = reverse_window
            for pattern_file in range(chosen_windows[file][0], chosen_windows[file][1] + 1):
                assert file_content(pos, pattern_file, n) == file_content(graph["root"], pattern_file, n)
            for side in SIDES:
                if side != expected_side:
                    continue
                for child in engine["children"](pos, side, only_file=file):
                    kind = engine["classify"](pos, side, child)
                    moves[(file, kind)] += 1
                    assert not engine["passers"](child)[side], (family, n, file, side, child)
                    assert kind in ("L", "P"), (family, n, file, kind)
    assert all(positions[file] == len(graph["nodes"]) for file in central_files)
    assert not any(kind in ("T", "K") for (file, kind), count in moves.items() if count)
    return positions, moves, chosen_windows


def check_insertion(family, cut, old_n, old_graph, new_graph):
    assert insert_after(old_graph["root"], old_n, cut) == new_graph["root"]
    mapped_nodes = frozenset(insert_after(pos, old_n, cut) for pos in old_graph["nodes"])
    assert mapped_nodes == new_graph["nodes"], (family, old_n)
    for kind in ("K", "T"):
        mapped_edges = frozenset(
            (insert_after(src, old_n, cut), side, insert_after(dst, old_n, cut))
            for src, side, dst in graph_edges(old_graph, kind)
        )
        assert mapped_edges == graph_edges(new_graph, kind), (family, old_n, kind)


def map_graph(graph, old_n, cut):
    """Map a reduced graph through one insertion, retaining only its K/T options."""
    mapped = lambda pos: insert_after(pos, old_n, cut)
    nodes = frozenset(mapped(pos) for pos in graph["nodes"])
    options = {}
    for pos, by_side in graph["options"].items():
        new_pos = mapped(pos)
        options[new_pos] = {
            side: (frozenset(mapped(child) for child in pair[0]),
                   frozenset(mapped(child) for child in pair[1]))
            for side, pair in by_side.items()
        }
    return {"root": mapped(graph["root"]), "nodes": nodes, "options": options}


def check_local_insertion(engine, family, cut, old_n, old_graph):
    """Check every mapped node/side's K/T children without rebuilding by BFS."""
    new_graph = map_graph(old_graph, old_n, cut)
    assert len(new_graph["nodes"]) == len(old_graph["nodes"])
    checked = 0
    for old_pos in old_graph["nodes"]:
        new_pos = insert_after(old_pos, old_n, cut)
        for side in SIDES:
            actual_k, actual_t = set(), set()
            for child in engine["children"](new_pos, side):
                kind = engine["classify"](new_pos, side, child)
                if kind == "K":
                    actual_k.add(child)
                elif kind == "T":
                    actual_t.add(child)
            expected_k, expected_t = new_graph["options"][new_pos][side]
            assert frozenset(actual_k) == expected_k, (family, old_n, "K", old_pos, side)
            assert frozenset(actual_t) == expected_t, (family, old_n, "T", old_pos, side)
            checked += 1
        if checked % 10000 == 0:
            print(f"{family}{old_n}->{old_n+2}: checked {checked}/{2*len(old_graph['nodes'])} node/side pairs",
                  flush=True)
    assert all(child in new_graph["nodes"]
               for src, by_side in new_graph["options"].items()
               for pair in by_side.values() for child in pair[0])
    print(f"{family}: insertion {old_n}->{old_n+2} exact on {len(new_graph['nodes'])} nodes, "
          f"{len(graph_edges(old_graph, 'K'))} K-edges, {len(graph_edges(old_graph, 'T'))} T-edges",
          flush=True)
    return new_graph


def save_graph(path, graph):
    with lzma.open(path, "wb", preset=3) as stream:
        pickle.dump(graph, stream, protocol=5)
    size = os.path.getsize(path)
    assert size < 50_000_000, (path, size)
    print(f"saved {path}: {size} bytes", flush=True)


def load_graph(path):
    with lzma.open(path, "rb") as stream:
        return pickle.load(stream)


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


def run_t_graphs():
    family, n0, cut = "T", 20, 4
    graphs = []
    for step in range(3):
        n = n0 + 2 * step
        engine = make_engine(n, False)
        graph = reduced_graph(engine, start(n, family))
        summary = graph_summary(engine, graph, family, n, cut, step)
        assert reduced_signature(graph, 6) == "NNNPNN"
        assert engine["signature"](graph["root"], 6) == "NNNPNN"
        positions, moves, windows = check_wall_lemma(engine, graph, n, family, cut, step)
        print(f"{family}{n} reduced={summary} sig(h=0..5)=NNNPNN; "
              f"wall positions={sum(positions.values())}, moves={sum(moves.values())}, "
              f"window files={dict(sorted(windows.items()))}", flush=True)
        graphs.append(graph)
        del engine
        gc.collect()
    for step in range(2):
        check_insertion(family, cut, n0 + 2 * step, graphs[step], graphs[step + 1])
        print(f"{family}: insertion {n0+2*step}->{n0+2*step+2} maps nodes, K-edges, T-edges exactly",
              flush=True)


def run_s_base():
    family, n, cut = "S", 23, 7
    engine = make_engine(n, False)
    graph = reduced_graph(engine, start(n, family))
    summary = graph_summary(engine, graph, family, n, cut, 0)
    assert reduced_signature(graph, 6) == "NNNPNN"
    positions, moves, windows = check_wall_lemma(engine, graph, n, family, cut, 0)
    print(f"S23 reduced={summary} sig(h=0..5)=NNNPNN; wall positions={sum(positions.values())}, "
          f"moves={sum(moves.values())}, window files={dict(sorted(windows.items()))}", flush=True)
    save_graph("research/star3_check/graph_S23.xz", graph)


def run_s_insertion(step):
    cut = 7
    if step == 1:
        old_n, next_n, source_path, target_path = (
            23, 25, "research/star3_check/graph_S23.xz", "research/star3_check/graph_S25.xz"
        )
    else:
        assert step == 2
        old_n, next_n, source_path, target_path = (
            25, 27, "research/star3_check/graph_S25.xz", "research/star3_check/graph_S27.xz"
        )
    source = load_graph(source_path)
    engine = make_engine(next_n, False)
    target = check_local_insertion(engine, "S", cut, old_n, source)
    assert target["root"] == start(next_n, "S"), (old_n, next_n, "inserted start")
    summary = graph_summary(engine, target, "S", next_n, cut, step)
    assert reduced_signature(target, 6) == "NNNPNN"
    print(f"S{next_n} mapped graph summary={summary} sig(h=0..5)=NNNPNN", flush=True)
    save_graph(target_path, target)


def run_base_checks(family, selected_sizes=None):
    size_table = {"T": (12, 14, 16, 18), "S": (13, 15, 17, 19, 21)}
    sizes = size_table[family]
    if selected_sizes:
        assert all(n in sizes for n in selected_sizes)
        sizes = tuple(selected_sizes)
    for family in (family,):
        for n in sizes:
            result = []
            for keep_ep in (False, True):
                engine = make_engine(n, keep_ep)
                started = perf_counter()
                sig = engine["signature"](start(n, family), 6)
                states = engine["state_count"]()
                assert sig == "NNNPNN", (family, n, keep_ep, sig)
                result.append((sig, states, perf_counter() - started))
                del engine
                gc.collect()
            assert result[0][0] == result[1][0]
            print(f"{family}{n} direct whole-board sig(expire/keep)={result[0][0]}/{result[1][0]} "
                  f"states={result[0][1]}/{result[1][1]} seconds={result[0][2]:.2f}/{result[1][2]:.2f}",
                  flush=True)
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_bytes = peak if sys.platform == "darwin" else peak * 1024
    print(f"direct search peak RSS={peak_bytes} bytes",
          flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("graphs-T", "S-base", "S-step1", "S-step2",
                                          "bases-T", "bases-S", "all"))
    parser.add_argument("sizes", nargs="*", type=int)
    args = parser.parse_args()
    self_check()
    print("Independent standard-library engine; no cylcgt, rg, or myeng imports.", flush=True)
    print("Adopted passed test; race=count. Heap moves checked with EP expire and keep.", flush=True)
    if args.mode == "graphs-T":
        run_t_graphs()
    elif args.mode == "S-base":
        run_s_base()
    elif args.mode == "S-step1":
        run_s_insertion(1)
    elif args.mode == "S-step2":
        run_s_insertion(2)
    elif args.mode == "bases-T":
        run_base_checks("T", args.sizes)
    elif args.mode == "bases-S":
        run_base_checks("S", args.sizes)
    if args.mode == "all":
        run_t_graphs()
        run_s_base()
        run_s_insertion(1)
        run_s_insertion(2)
        run_base_checks("T")
        run_base_checks("S")
    print("All independent checker assertions passed.", flush=True)


if __name__ == "__main__":
    main()
