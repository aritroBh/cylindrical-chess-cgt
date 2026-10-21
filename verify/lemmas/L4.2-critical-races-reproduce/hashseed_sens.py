"""Run lemmas.test_L4_races.sensitivity for e.p. on and off and print the
random-trial histogram. Run under different PYTHONHASHSEED values to test
whether the 200-trial histogram depends on set iteration order."""
import os, time
from lemmas.test_L4_races import sensitivity
t = time.time()
for ep in (True, False):
    r = sensitivity(ep)
    print(os.environ.get("PYTHONHASHSEED"), "ep" if ep else "noep", r["base"], r["n_races"],
          [(c, m, v) for c, m, w, v in r["critical"]], r["critical_mover_rest_opponent"],
          sorted(r["random_rest"].items()), flush=True)
print("secs", round(time.time() - t, 1))
