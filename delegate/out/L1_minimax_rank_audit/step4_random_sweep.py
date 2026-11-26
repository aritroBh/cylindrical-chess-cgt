"""Step 4b: random single-component passer-free positions on boards with 5,6,7,9 ranks.
Counts agreement of original minimax and fixed minimax with the cylcgt engine (default setting: count race, e.p. on/off, e.p.-aware passed test).
Run: nice -n 15 .venv/bin/python delegate/out/L1_minimax_rank_audit/step4_random_sweep.py [N_per_cell] [seed]"""
import sys, os, random, time
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "crosscheck_fixed")); sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
import minimax_orig as mo, minimax_fixed as mf
from cylcgt import cgt, pawns
N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20261125
rng = random.Random(seed)
tot = Counter(); t0 = time.time()
print(f"{'ranks':>5} {'-':>6} {'tried':>6} {'orig!=eng':>10} {'fixed!=eng':>11} {'orig!=fixed':>12} {'root_has_B_on_rank_ranks-1':>26}")
for ranks in (5, 6, 7, 9):
    c = Counter()
    for _ in range(N * 30):
        if c["tried"] >= N: break
        files = rng.choice([3, 4]); wrap = rng.random() < 0.4; ep = rng.random() < 0.5
        npawn = rng.randint(2, 5 if ranks < 9 else 4)
        squares = [(f, r) for f in range(files) for r in range(2, ranks)]
        pick = rng.sample(squares, npawn)
        k = rng.randint(1, npawn - 1)
        w, b = frozenset(pick[:k]), frozenset(pick[k:])
        mb = mf.Board(files, ranks, wrap, ep); pos = mf.Position(w, b)
        if any(mf.passed_flags(mb, pos)): continue
        eb = pawns.Board(files, ranks, wrap, ep); ep_pos = pawns.Pos(w, b)
        if len(pawns.components(eb, ep_pos)) != 1: continue
        try: e = cgt.outcome(pawns.value(eb, ep_pos))
        except Exception: continue
        o = mo.outcome_class(mo.Board(files, ranks, wrap, ep), mo.Position(w, b)); f = mf.outcome_class(mb, pos)
        c["tried"] += 1; c["o_bad"] += (o != e); c["f_bad"] += (f != e); c["of_diff"] += (o != f)
        # does a black pawn stand on the true double-step rank in the root?
        c["root_black_on_start"] += any(r == ranks - 1 for _, r in b)
        if f != e: c["f_bad_ex"] += 1; print("FIXED DISAGREES", files, ranks, wrap, ep, sorted(w), sorted(b), o, f, e)
    print(f"{ranks:>5} {'-':>6} {c['tried']:>6} {c['o_bad']:>10} {c['f_bad']:>11} {c['of_diff']:>12} {c['root_black_on_start']:>26}   ({time.time()-t0:.0f}s)", flush=True)
    tot.update(c)
print("TOTAL", dict(tot))
