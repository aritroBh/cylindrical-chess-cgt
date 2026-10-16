"""Second sanity test: flip P True -> False (can only be caught by the N-condition, step 6, or by
reducedness). Run from project root:
  PYTHONPATH=. .venv/bin/python verify/dawson/C1-reproduce/mutation_test2.py"""
import copy, os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mutation_test import base, run
random.seed(7)
Ps = [x for x in range(len(base["P"])) if base["P"][x]]
for x in random.sample(Ps, 6):
    d = copy.deepcopy(base); d["P"][x] = False
    run(d, f"flip P[{x}] True -> False")
