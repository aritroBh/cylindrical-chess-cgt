#!/usr/bin/env python3
"""cyl_check.py RINGFILE OUT.tsv [--count K] [--skip S]

Whole-board solve of the first K rings of RINGFILE (after skipping S) with
  (1) cylcgt whole-board:  pawns.components = lambda b, p: [p]; value = pawns.value(Board(9, 8, True, True), pos);
      signature = outcome(G + *h) for h = 0..3
  (2) the original rg (research/ring_family_proof/rg, one process, <= 40 rings, TBITS=21)
  (3) Codex's non-Claude solver research/ring_n_plus_2_check/independent.py, both e.p. conventions
      ("keep" = the e.p. right survives moves in the *h heap, like rg and like the CGT game form; "expire" = it does not)
and print/write one row per ring.  Run from the project root with PYTHONPATH=. and the project venv:
  PYTHONPATH=. .venv/bin/python research/c9_rings/p9/cyl_check.py RINGFILE OUT.tsv --count 20
Two processes at a time at most (this python + the rg call, which is sequential)."""
import sys, os, time, subprocess, importlib.util

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ROOT)
from cylcgt import pawns, cgt
from cylcgt.pawns import Board, Pos

pawns.RACE_RULE = "count"
pawns.PASSED_RESPECTS_EP = True
pawns.components = lambda b, p: [p]          # whole-board game: no splitting into components

N = 9


def parse(ring):
    toks = ring.split()
    assert len(toks) == N
    W, B = set(), set()
    for f, t in enumerate(toks):
        (W if t[0] == 'W' else B).add((f, int(t[1:])))
    return Pos(frozenset(W), frozenset(B))


def masks(ring):
    w = b = 0
    for f, t in enumerate(ring.split()):
        sq = (int(t[1:]) - 1) * N + f           # independent.py: square = rank0 * n + file, rank0 = rank - 1
        if t[0] == 'W':
            w |= 1 << sq
        else:
            b |= 1 << sq
    return (w, b, None)


def load_codex():
    p = os.path.join(ROOT, "research", "ring_n_plus_2_check", "independent.py")
    spec = importlib.util.spec_from_file_location("codex_independent", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    a = sys.argv[1:]
    ringfile, outfn = a[0], a[1]
    k = int(a[a.index("--count") + 1]) if "--count" in a else 20
    skip = int(a[a.index("--skip") + 1]) if "--skip" in a else 0
    rings = [l.strip() for l in open(ringfile) if l.strip()][skip:skip + k]
    board = Board(N, 8, True, True)
    codex = load_codex()
    keep_solve, _, _ = codex.game(N, True)
    exp_solve, _, _ = codex.game(N, False)
    # (2) original rg, one process, at most 40 rings
    assert len(rings) <= 40
    p = subprocess.run(["nice", "-n", "15", os.path.join(ROOT, "research", "ring_family_proof", "rg"), "solve", "3"],
                       input="\n".join(rings) + "\n", capture_output=True, text=True, env=dict(os.environ, TBITS="21"))
    rgsigs = [l.split()[0] for l in p.stdout.splitlines() if l.strip()]
    assert p.returncode == 0 and len(rgsigs) == len(rings), (p.returncode, len(rgsigs), len(rings))
    bad = 0
    with open(outfn, "w") as f:
        f.write("ring\trg_original\tcylcgt_whole\tcylcgt_value\tcodex_keep\tcodex_expire\tcylcgt_seconds\tall_agree\n")
        for ring, rgs in zip(rings, rgsigs):
            pos = parse(ring)
            pawns._value.cache_clear()
            t0 = time.time()
            g = pawns.value(board, pos)
            sig = "".join(cgt.outcome(cgt.add(g, cgt.nimber(h))) for h in range(4))
            sec = time.time() - t0
            ck = keep_solve(masks(ring))
            ce = exp_solve(masks(ring))
            agree = (sig == rgs == ck)
            bad += (not agree)
            f.write("%s\t%s\t%s\t%s\t%s\t%s\t%.2f\t%s\n" % (ring, rgs, sig, cgt.show(g), ck, ce, sec, "yes" if agree else "NO"))
            f.flush()
            print("%-45s rg %s  cylcgt %s (%s, %.2fs)  codex keep %s expire %s  %s" % (
                ring, rgs, sig, cgt.show(g), sec, ck, ce, "agree" if agree else "DISAGREE"), flush=True)
    print("rings %d, rg/cylcgt/codex-keep disagreements %d" % (len(rings), bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
