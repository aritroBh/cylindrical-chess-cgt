"""Validation of the T32 pawn-history search (run from the project root).

PYTHONPATH=. .venv/bin/python -I research/five_file_legal/validate_search.py

Checks, in order:
 1. Move generators agree: pawnhist._moves (bitboard) and replay_check.legal_moves
    (sets) give the same move sets on many random positions, including e.p. states.
 2. Reachable sets agree: on small starts (3 or 4 files) the bitboard BFS and the set BFS
    reach the same states.
 3. Pruning is sound: on small starts, find_history(prune=True) and prune=False agree
    on every random target (found vs exhausted), and every found history replays.
 4. Random reachable positions on the full 8x8 start are found, and the history replays.
"""
import random
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pawnhist as ph
import replay_check as rc


def bitboard_reachable(start_files):
    W0 = ph._mask([(f, 2) for f in start_files])
    B0 = ph._mask([(f, 7) for f in start_files])
    s0 = (W0, B0, None)
    seen = {s0}
    stack = [s0]
    while stack:
        W, B, last = stack.pop()
        for mv in ph._moves(W, B, last):
            W2, B2, l2 = ph._apply(W, B, mv)
            st = (W2, B2, l2)
            if st not in seen:
                seen.add(st)
                stack.append(st)
    return {(tuple(sorted(ph._unmask(W))), tuple(sorted(ph._unmask(B)))) for (W, B, _) in seen}


def set_reachable(start_files):
    W0, B0 = rc._start(start_files)
    states = rc.reachable_states(W0, B0)
    return {(tuple(sorted(W)), tuple(sorted(B))) for (W, B) in states}


def random_playout(rng, length, files=range(8)):
    """Random pawn-only game from the start; returns (W, B) frozensets."""
    W, B = rc._start(files)
    last = None
    for _ in range(length):
        mv = rng.choice(rc.legal_moves(W, B, last)) if rc.legal_moves(W, B, last) else None
        if mv is None:
            break
        W, B, last = rc.apply_move(W, B, mv)
    return W, B


def main():
    rng = random.Random(20261022)

    # 1. move generators agree on random states
    n_states = 0
    n_ep = 0
    for _ in range(3000):
        W, B, last = None, None, None
        W, B = rc._start()
        last = None
        for _k in range(rng.randint(0, 60)):
            moves_set = rc.legal_moves(W, B, last)
            Wb, Bb = ph._mask(W), ph._mask(B)
            # bitboard's `last` is (side, file) for a double step; rebuild it
            if last is not None and last[1] == "double":
                bb_last = (last[0], last[2][0])
            else:
                bb_last = None
            moves_bb = ph._moves(Wb, Bb, bb_last)
            a = sorted((k, s, frm, to) for (k, s, frm, to) in moves_bb)
            b = sorted(moves_set)
            if a != b:
                print("MOVE MISMATCH", sorted(W), sorted(B), last, set(a) ^ set(b))
                sys.exit(1)
            n_states += 1
            if any(m[0] == "ep" for m in moves_set):
                n_ep += 1
            if not moves_set:
                break
            mv = rng.choice(moves_set)
            W, B, last = rc.apply_move(W, B, mv)
    print(f"1. move generators agree on {n_states} random states ({n_ep} with an e.p. option)")

    # 2. reachable sets agree on small starts
    for files in ([0, 1, 2], [5, 6, 7], [0, 2, 3]):
        bb = bitboard_reachable(files)
        st = set_reachable(files)
        bbn = {(tuple(sorted(w)), tuple(sorted(b))) for (w, b) in bb}
        print(f"2. start files {files}: {len(bbn)} reachable states; bitboard == set BFS: {bbn == st}")
        if bbn != st:
            sys.exit(1)

    # 3. pruning sound on small starts; every found history replays
    files = [0, 1, 2]
    W0, B0 = rc._start(files)
    reach = list(set_reachable(files))
    ok = found = exhausted = 0
    targets = []
    for _ in range(120):
        w, b = rng.choice(reach)
        targets.append((set(w), set(b), True))
    # perturbed (mostly unreachable) targets
    for _ in range(120):
        w, b = rng.choice(reach)
        w, b = set(w), set(b)
        if rng.random() < 0.5 and w:
            p = rng.choice(sorted(w))
            w.discard(p)
            w.add((min(7, max(2, p[0] + rng.choice([-1, 1]))), min(7, p[1] + rng.choice([0, 1]))))
        elif b:
            p = rng.choice(sorted(b))
            b.discard(p)
            b.add((min(7, max(2, p[0] + rng.choice([-1, 1]))), max(2, p[1] - rng.choice([0, 1]))))
        if len(w) != 0 and len(b) != 0 and len(w) <= 4 and len(b) <= 4:
            targets.append((w, b, None))
    for w, b, expect in targets:
        if not w or not b:
            continue
        m1, i1 = ph.find_history(w, b, start_w=W0, start_b=B0, prune=True, node_cap=10**7)
        m0, i0 = ph.find_history(w, b, start_w=W0, start_b=B0, prune=False, node_cap=10**7)
        s1, s0 = i1["status"], i0["status"]
        if s1 == "cap" or s0 == "cap":
            print("cap hit in small test", i1, i0)
            sys.exit(1)
        if (s1 == "found") != (s0 == "found"):
            print("PRUNE UNSOUND", sorted(w), sorted(b), s1, s0)
            sys.exit(1)
        if s1 == "found":
            found += 1
            okr, msg = rc.replay(m1, w, b, start=(W0, B0))
            if not okr:
                print("REPLAY FAILED", sorted(w), sorted(b), msg)
                sys.exit(1)
        else:
            exhausted += 1
        ok += 1
    print(f"3. pruned vs unpruned agree on {ok} small-start targets ({found} reachable, all replayed; "
          f"{exhausted} unreachable)")

    # 4. random reachable positions on the full start: found and replayed
    got = 0
    tries = 0
    while got < 25 and tries < 2000:
        tries += 1
        W, B = random_playout(rng, rng.randint(20, 70))
        if len(W) + len(B) > 8:
            continue
        m, info = ph.find_history(W, B, prune=True, node_cap=3_000_000, max_seconds=120)
        if info["status"] != "found":
            print("4. full-start case not found:", sorted(W), sorted(B), info)
            continue
        okr, msg = rc.replay(m, W, B)
        if not okr:
            print("REPLAY FAILED (full)", msg)
            sys.exit(1)
        got += 1
    print(f"4. random reachable positions with <= 8 pawns on the full start: {got} found and replayed "
          f"(of {tries} playouts)")


if __name__ == "__main__":
    main()
