"""T87 finite checks. Run from repository root with PYTHONPATH=. and -B."""
import argparse
from collections import Counter
from functools import lru_cache
import json
import os
import resource
import signal
import sys
from time import monotonic

from delegate.out.T82 import referee as rules

# T82 geometry depends only on width, square and direction.
rules.geometry = lru_cache(8192)(rules.geometry.__wrapped__)
SIDES = (rules.WHITE, rules.BLACK)


def start(family, m):
    if family == "TT":
        files = "B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2".split() + ["B4", "W2"] * m
    else:
        files = ["B6", "W3"] + ["W2", "B4"] * m + "W6B7 W3 B7 B6 W3 W2 B6 W2 B4".split()
    root = rules.parse([zip(token[::2], token[1::2]) for token in files])
    assert sum(bits.bit_count() for bits in root[:4]) == len(files) + 1
    assert root[4] == rules.CLEAR and rules.terminal(len(files), root) == rules.LIVE
    return len(files), root


@lru_cache(65536)
def terminal_reply(n, p, side):
    return any(rules.win_at_end(rules.terminal(n, child), side)
               for _, _, _, child in rules.moves(n, p, side))


def move_class(n, child, side):
    end = rules.terminal(n, child)
    if end != rules.LIVE:
        return "T" if rules.win_at_end(end, side) else "L"
    return "P" if terminal_reply(n, child, 1-side) else "K"


def traverse(family, m, audit):
    n, root = start(family, m)
    pending = [root]
    graph = {}
    changed_nodes = Counter()
    sources, seam, end_captures = Counter(), Counter(), Counter()
    flagged = passed = edges = threats = 0
    arc = range(10, 20) if family == "TT" else range(2, 12)
    watched = {0, 1, n-1, *arc}
    while pending:
        p = pending.pop()
        if p in graph:
            continue
        assert len(graph) < 100000, "graph size guard"
        pair = []
        if audit:
            flagged += p[4] != rules.CLEAR
            passed += rules.terminal(n, p) != rules.LIVE
            delta = (p[0] ^ root[0]) | (p[1] ^ root[1]) | (p[2] ^ root[2]) | (p[3] ^ root[3])
            changed_nodes.update({s // 8 for s in rules.squares(delta)})
        for side in SIDES:
            kept = []
            has_t = False
            for src, dst, victim, child in rules.moves(n, p, side):
                kind = move_class(n, child, side)
                if kind == "T":
                    threats += 1
                    has_t = True
                if kind == "K":
                    kept.append(child)
                    edges += 1
                if audit:
                    f, g = src // 8, dst // 8
                    if victim != rules.CLEAR:
                        method = "ep" if victim != dst else "ordinary"
                        if n-1 in (f, g):
                            end_captures[f, g, method, kind] += 1
                        if {f, g} == {0, n-1}:
                            seam[f, g, method, kind] += 1
                    else:
                        method = "single" if abs(dst-src) == 1 else "double"
                    if f in watched:
                        sources[f, method, kind] += 1
            pair.append((kept, has_t))
            pending.extend(kept)
        graph[p] = pair
    if audit:
        # Check the phase and exact piece/direction of the root arc explicitly.
        wall = ["B4", "W2"] if family == "TT" else ["W2", "B4"]
        root_files = rules.tokens(n, root).split()
        assert all(root_files[f] == wall[i % 2] for i, f in enumerate(arc))
        assert set(changed_nodes).isdisjoint(arc), (changed_nodes, arc)

        @lru_cache(262144)
        def win(p, side, h):
            children, has_t = graph[p][side]
            return (has_t or any(not win(q, 1-side, h) for q in children)
                    or any(not win(p, 1-side, j) for j in range(h)))

        sig = rules.signature(lambda s, h: win(root, s, h), 4)
        win.cache_clear()
        emit("base", family=family, m=m, n=n, nodes=len(graph), k=edges, t=threats,
             flagged=flagged, passed=passed, zone=sorted(changed_nodes), signature=sig,
             changed_nodes=dict(sorted(changed_nodes.items())))
        for label, data in (("sources", sources), ("seam", seam), ("last_file_captures", end_captures)):
            emit(label, family=family, entries=[[*key, v] for key, v in sorted(data.items())])
    return graph


def insertion(family):
    m, c = (5, 14) if family == "TT" else (6, 6)
    n, root = start(family, m)
    _, next_root = start(family, m+1)
    old = traverse(family, m, True)
    assert rules.insert(root, c) == next_root
    new = traverse(family, m+1, False)
    images = {p: rules.insert(p, c) for p in old}
    assert len(old) == len(new) and set(images.values()) == new.keys()
    for p, image in images.items():
        for side in SIDES:
            children, flag = old[p][side]
            targets, new_flag = new[image][side]
            assert {images[q] for q in children} == set(targets), (p, side)
            assert flag == new_flag, (p, side)
    emit("insertion", family=family, cut=c, m=m, n=n, nodes=len(old),
         target_nodes=len(new), side_comparisons=2*len(old), root=True, bijection=True)


def whole_board(family, m):
    n, root = start(family, m)

    @lru_cache(32768)
    def options(p, side):
        live = []
        for _, _, _, q in rules.moves(n, p, side):
            end = rules.terminal(n, q)
            if rules.win_at_end(end, side):
                return True, ()
            if end == rules.LIVE:
                live.append(q)
        return False, tuple(live)

    @lru_cache(131072)
    def win(p, side, h):
        immediate, live = options(p, side)
        return (immediate or any(not win(p, 1-side, j) for j in range(h))
                or any(not win(q, 1-side, h) for q in live))

    sig = rules.signature(lambda s, h: win(root, s, h), 3)
    emit("whole", family=family, m=m, n=n, signature=sig)
    options.cache_clear()
    win.cache_clear()


def emit(check, **result):
    print(json.dumps(dict(check=check, **result)), flush=True)


def report_usage(t0):
    usage = resource.getrusage(resource.RUSAGE_SELF)
    rss = usage.ru_maxrss if sys.platform == "darwin" else 1024 * usage.ru_maxrss
    emit("usage", wall_seconds=round(monotonic()-t0, 3), peak_rss_bytes=rss,
         cpu_seconds=round(usage.ru_utime+usage.ru_stime, 3))


def require_priority(allow_background_qos):
    priority = os.getpriority(os.PRIO_PROCESS, 0)
    if priority >= 15:
        emit("priority", nice=priority)
        return
    if allow_background_qos and sys.platform == "darwin":
        import ctypes
        lib = ctypes.CDLL(None)
        # The worker is single-threaded. Verify the calling thread's actual QoS.
        if lib.pthread_set_qos_class_self_np(0x09, 0) == 0 and lib.qos_class_self() == 0x09:
            emit("priority", nice=priority, thread_qos="background")
            return
    raise SystemExit(f"Required niceness >=15; observed {priority}. Search did not start.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["TT", "SS", "full", "all"])
    parser.add_argument("--allow-background-qos", action="store_true")
    args = parser.parse_args()
    t0 = monotonic()
    try:
        require_priority(args.allow_background_qos)
        signal.alarm(39*60)
        rules.selfcheck()
        if args.mode in ("all", "TT"):
            insertion("TT")
        if args.mode in ("all", "SS"):
            insertion("SS")
        if args.mode in ("all", "full"):
            for m in range(6):
                if m < 5:
                    whole_board("TT", m)
                whole_board("SS", m)
    finally:
        report_usage(t0)
