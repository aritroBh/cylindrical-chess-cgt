"""Value-level differential test: outcome of G + *h (h = 0..3) from the independent full solver `rg solve` versus
the project's cylcgt in WHOLE-BOARD mode (pawns.components = lambda b, p: [p]), on random small cylinder positions.
Run from the project root:  PYTHONPATH=. .venv/bin/python research/ring_family_proof/difftest_solve.py [N] [SEED]
"""
import sys, random, os, subprocess
from cylcgt import pawns, cgt
from cylcgt.pawns import Board, Pos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from difftest import to_tok, norm_ep, rand_pos

pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True
pawns.components = lambda b, p: [p]          # whole-board game

def main():
    npos = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    rng = random.Random(seed)
    cases = []
    while len(cases) < npos:
        n = rng.choice([3, 4, 4, 5, 5, 6])
        npawn = rng.randrange(3, min(2 * n, 9))
        r = rand_pos(n, npawn, rng, want_ep=(rng.random() < 0.4))
        if r: cases.append(r)
    inp = "\n".join(to_tok(p, b.files) for b, p in cases) + "\n"
    out = subprocess.run([os.path.join(os.path.dirname(os.path.abspath(__file__)), "rg"), "solve", "3"], input=inp,
                         capture_output=True, text=True).stdout.strip().splitlines()
    assert len(out) == len(cases)
    bad = 0; hist = {}
    for (board, pos), line in zip(cases, out):
        sig = line.split()[0]
        pawns._value.cache_clear()
        g = pawns.value(board, pos)
        ref = "".join(cgt.outcome(cgt.add(g, cgt.nimber(h))) for h in range(4))
        hist[ref] = hist.get(ref, 0) + 1
        if ref != sig:
            bad += 1
            if bad <= 5: print("MISMATCH", pos, "cylcgt", ref, "rg", sig)
    print(f"value-level test: {len(cases)} random positions, outcomes of G+*h for h=0..3 compared, mismatches {bad}; "
          f"distinct signatures seen {len(hist)}: {sorted(hist.items(), key=lambda x: -x[1])[:8]}")
    return bad

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
