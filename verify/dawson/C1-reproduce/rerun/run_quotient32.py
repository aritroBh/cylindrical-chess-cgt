"""Exact re-run of `python -m dawson.quotient 32` (same main(), same arguments); only the log and
pickle paths differ, so the worker's files are untouched. Run from project root:
  PYTHONPATH=. .venv/bin/python verify/dawson/C1-reproduce/rerun/run_quotient32.py
"""
import pickle
from dawson.quotient import main
n = 32
d = "verify/dawson/C1-reproduce/rerun/"
with open(d + f"quotient_run_{n}.txt", "w") as f:
    Q, sizes = main(n, f)
with open(d + f"quotient_Q{n}.pkl", "wb") as f:
    pickle.dump({"mult": Q.mult, "P": Q.P, "phi": Q.phi, "gens": Q.gens}, f)
