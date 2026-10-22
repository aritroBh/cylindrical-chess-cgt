"""Cross-check the C search (t32_search.c) against the Python search and the replay checker.

PYTHONPATH=. .venv/bin/python -I research/five_file_legal/crosscheck_c.py <path-to-t32_search binary>

On small starts (3 files, 3 pawns a side) every target is decided three ways:
  * Python find_history with prune=False (exhaustive, no pruning);
  * Python find_history with prune=True;
  * the C program.
Statuses must agree; every found history is replayed by replay_check.replay.
Then a few random reachable positions on the full 8-pawn start are checked (C vs Python prune=True).
"""
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pawnhist as ph
import replay_check as rc


def mask_of(pawns):
    m = 0
    for f, r in pawns:
        m |= 1 << ((r - 1) * 8 + f)
    return m


def run_c(binary, targets, start_w, start_b, log2=22, cap=50_000_000):
    args = [binary, str(log2), str(cap), format(mask_of(start_w), "x"), format(mask_of(start_b), "x")]
    inp = "".join(f"{mask_of(w)} {mask_of(b)}\n" for (w, b) in targets)
    out = subprocess.run(args, input=inp, capture_output=True, text=True, check=True).stdout
    results = []
    lines = out.splitlines()
    i = 0
    while i < len(lines):
        parts = lines[i].split()
        if parts and parts[0] == "RESULT":
            status = parts[1].lower()
            nodes = int(parts[3])
            moves = []
            if status == "found":
                nm = int(parts[5])
                for k in range(nm):
                    p = lines[i + 1 + k].split()
                    # MV kind side f r tf tr
                    kind, side = p[1], p[2]
                    f, r, tf, tr = int(p[3]), int(p[4]), int(p[5]), int(p[6])
                    moves.append((kind, side, (f, r), (tf, tr)))
                i += nm
            results.append((status, nodes, moves))
        i += 1
    return results


def main():
    binary = sys.argv[1]
    rng = random.Random(7)
    files = [0, 1, 2]
    W0 = frozenset((f, 2) for f in files)
    B0 = frozenset((f, 7) for f in files)
    reach = sorted(rc.reachable_states(W0, B0), key=lambda s: (sorted(s[0]), sorted(s[1])))
    print(f"small start files {files}: {len(reach)} reachable (W,B) sets")
    targets = []
    for _ in range(60):
        w, b = rng.choice(reach)
        targets.append((frozenset(w), frozenset(b)))
    for _ in range(60):
        w, b = rng.choice(reach)
        w, b = set(w), set(b)
        if rng.random() < 0.5 and w:
            p = rng.choice(sorted(w))
            w.discard(p)
            w.add((min(7, max(2, p[0] + rng.choice([-1, 0, 1]))), min(7, max(2, p[1] + rng.choice([0, 1])))))
        elif b:
            p = rng.choice(sorted(b))
            b.discard(p)
            b.add((min(7, max(2, p[0] + rng.choice([-1, 0, 1]))), min(7, max(2, p[1] - rng.choice([0, 1])))))
        if w and b and len(w) <= 4 and len(b) <= 4:
            targets.append((frozenset(w), frozenset(b)))

    c_res = run_c(binary, targets, W0, B0, log2=20, cap=5_000_000)
    assert len(c_res) == len(targets), (len(c_res), len(targets))
    n_found = n_exh = 0
    for (w, b), (cst, cn, cm) in zip(targets, c_res):
        py0, i0 = ph.find_history(w, b, start_w=W0, start_b=B0, prune=False, node_cap=10**7)
        py1, i1 = ph.find_history(w, b, start_w=W0, start_b=B0, prune=True, node_cap=10**7)
        s0, s1 = i0["status"], i1["status"]
        assert s0 != "cap" and s1 != "cap", "python cap in small test"
        if not ((cst == "found") == (s0 == "found") == (s1 == "found")):
            print("STATUS MISMATCH", sorted(w), sorted(b), "C", cst, "py-unpruned", s0, "py-pruned", s1)
            sys.exit(1)
        if cst == "found":
            n_found += 1
            ok, msg = rc.replay(cm, w, b, start=(W0, B0))
            if not ok:
                print("C HISTORY FAILED REPLAY", sorted(w), sorted(b), msg)
                sys.exit(1)
        else:
            n_exh += 1
    print(f"small starts: C agrees with Python (pruned and unpruned) on {len(targets)} targets "
          f"({n_found} reachable, all C histories replay; {n_exh} exhausted)")

    # full start: a few random reachable positions, C vs Python prune=True
    full_targets = []
    tries = 0
    while len(full_targets) < 6 and tries < 400:
        tries += 1
        W, B = rc._start()
        last = None
        for _ in range(rng.randint(15, 45)):
            mvs = rc.legal_moves(W, B, last)
            if not mvs:
                break
            W, B, last = rc.apply_move(W, B, rng.choice(mvs))
        if len(W) + len(B) <= 10 and len(W) >= 1 and len(B) >= 1:
            full_targets.append((W, B))
    c_full = run_c(binary, full_targets, rc._start()[0], rc._start()[1], log2=24, cap=20_000_000)
    for (w, b), (cst, cn, cm) in zip(full_targets, c_full):
        py, info = ph.find_history(w, b, prune=True, node_cap=3_000_000, max_seconds=300)
        ok = None
        if cst == "found":
            ok, msg = rc.replay(cm, w, b)
            assert ok, msg
        print("full start", sorted(w), sorted(b), "C:", cst, cn, "| Python prune:", info["status"], info["nodes"],
              "| replay:", ok)
        if info["status"] in ("found", "exhausted") and info["status"] != cst:
            print("  disagreement (C vs Python prune)")
            sys.exit(1)
    print("crosscheck done")


if __name__ == "__main__":
    main()
