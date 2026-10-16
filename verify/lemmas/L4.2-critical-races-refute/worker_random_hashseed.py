# Reproducibility probe of the worker's random-trial count (NOT the decisive check).
# Calls lemmas/test_L4_races.sensitivity unchanged; run under different PYTHONHASHSEED values.
import os, sys
from lemmas import test_L4_races as t
for ep in (True, False):
    r = t.sensitivity(ep)
    print("PYTHONHASHSEED=%s ep=%s base=%s n=%d crit=%d mixed=%s random=%s" % (
        os.environ.get("PYTHONHASHSEED"), ep, r["base"], r["n_races"], len(r["critical"]),
        r["critical_mover_rest_opponent"], dict(sorted(r["random_rest"].items()))))
    sys.stdout.flush()
