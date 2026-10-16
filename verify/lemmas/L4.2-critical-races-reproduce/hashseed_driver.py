"""Re-run the worker's sensitivity() unchanged; only PYTHONHASHSEED varies between runs.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONHASHSEED=<k> PYTHONPATH=. .venv/bin/python verify/lemmas/L4.2-critical-races-reproduce/hashseed_driver.py"""
import os
from lemmas.test_L4_races import sensitivity
for ep in (True, False):
    r = sensitivity(ep)
    print(os.environ.get("PYTHONHASHSEED"), "ep", ep, r["base"], r["n_races"], len(r["critical"]),
          r["critical_mover_rest_opponent"], r["random_rest"], flush=True)
