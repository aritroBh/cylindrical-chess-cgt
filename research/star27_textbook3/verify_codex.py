#!/usr/bin/env python3
"""T27 step 3: evaluate positions with the independent whole-board solver verify_ext/codex/solver.py.

Usage (project root):
  PYTHONPATH=. nice -n 10 .venv/bin/python research/star27_textbook3/verify_codex.py RACE EP PASSED "POSITION" [...]
    RACE   = count | mover | opponent
    EP     = on | off
    PASSED = textbook | aware
Prints one TSV line per position: position, race/ep/test, value, outcome, nimber, states, seconds, maxrss_MB.
"""
import resource
import sys
import time

sys.path.insert(0, "verify_ext/codex")
import solver  # noqa: E402
from solver import PawnGame, parse_position, show  # noqa: E402


def main():
    race, ep, passed = sys.argv[1], sys.argv[2] == "on", sys.argv[3]
    game = PawnGame(6, race, ep, passed)
    for text in sys.argv[4:]:
        w, b = parse_position(text.replace(":", ""), 6)
        t0 = time.time()
        g = game.value(w, b)
        dt = time.time() - t0
        k = solver.as_nimber(g)
        n = solver.as_number(g)
        # outcome of the canonical form: nimber -> N (k>0) or P (k=0); number -> sign
        if k is not None:
            out = "P" if k == 0 else "N"
        elif n is not None:
            out = "P" if n == 0 else ("L" if n > 0 else "R")
        else:
            out = "?"
        states = game._value.cache_info().currsize
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
        print(f"{text}\t{race}/ep-{'on' if ep else 'off'}/{passed}\t{show(g)}\t{out}\t"
              f"{-1 if k is None else k}\t{states}\t{dt:.1f}\t{rss:.0f}", flush=True)


if __name__ == "__main__":
    main()
