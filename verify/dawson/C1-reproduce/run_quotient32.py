"""Re-run of `python -m dawson.quotient 32`, identical to its __main__ block except that the
log and pickle are written into verify/dawson/C1-reproduce/ (worker files untouched).
Run from project root:
  PYTHONPATH=. .venv/bin/python verify/dawson/C1-reproduce/run_quotient32.py
"""
import pickle, sys
from dawson.quotient import main
n = 32
d = "verify/dawson/C1-reproduce/"
with open(d + f"quotient_run_{n}.txt", "w") as f:
    Q, sizes = main(n, f)
with open(d + f"quotient_Q{n}.pkl", "wb") as f:
    pickle.dump({"mult": Q.mult, "P": Q.P, "phi": Q.phi, "gens": Q.gens}, f)
