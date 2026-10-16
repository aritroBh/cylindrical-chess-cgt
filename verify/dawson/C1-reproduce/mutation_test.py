"""Sanity test of indep_verify.py: it must reject corrupted quotients.
Run from project root: PYTHONPATH=. .venv/bin/python verify/dawson/C1-reproduce/mutation_test.py"""
import copy, io, pickle, random, sys, contextlib, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep_verify as IV
base = pickle.load(open(os.path.join(os.path.dirname(__file__), "quotient_Q32.pkl"), "rb"))
N = len(base["mult"])
random.seed(1)

def run(d, label):
    fd, p = tempfile.mkstemp(suffix=".pkl", dir=os.path.dirname(os.path.abspath(__file__)))
    os.close(fd)
    pickle.dump(d, open(p, "wb"))
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            IV.main(p)
        res = "ACCEPTED"
    except AssertionError as e:
        lines = [l for l in buf.getvalue().splitlines() if l.strip()]
        res = "rejected after: " + (lines[-1].strip()[:90] if lines else "start") + (f" [{e}]" if str(e) else "")
    os.remove(p)
    print(f"{label:55s} {res}")

run(copy.deepcopy(base), "unmodified")
for i in range(6):                      # flip one P bit
    d = copy.deepcopy(base); x = random.randrange(1, N); d["P"][x] = not d["P"][x]
    run(d, f"flip P[{x}]")
for h in (32, 31, 24, 13, 9):           # move Phi(h) to a different element
    d = copy.deepcopy(base)
    old = d["phi"][h]
    d["phi"][h] = random.choice([y for y in range(N) if y != old])
    run(d, f"Phi({h}) {old} -> {d['phi'][h]}")
for h in (32, 24):                      # Phi(h) := Phi(h') for another strip (keeps onto more often)
    d = copy.deepcopy(base)
    other = 31 if h == 32 else 23
    d["phi"][h] = d["phi"][other]
    run(d, f"Phi({h}) := Phi({other})")
# Q31 restricted check: drop generator 32 -> should still verify (as quotient of A_31? not reduced/onto in general)
d = copy.deepcopy(base); del d["phi"][32]; d["gens"] = [g for g in d["gens"] if g != 32]
run(d, "drop strip 32 (Q32 table, gens <= 31)")
