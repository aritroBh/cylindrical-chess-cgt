"""The 48 v1 components whose value changes under the e.p.-aware test (bench/results/conventions_summary.json):
compare outcome classes of textbook ab.c and my e.p.-aware abx1 with the outcome of cylcgt's textbook/aware root value,
and check that ab.c's counter fires whenever abx1 differs."""
import json, subprocess, sys
P = "/Users/aritro/Downloads/Research/Chessendgames"; D = P + "/verify/bench/C3-reproduce"
sys.path.insert(0, P)
from bench import cgtfmt, board as bd
from cylcgt import cgt
comps = [json.loads(l) for l in open(P + "/bench/data/components.jsonl")]
print("kept comps with width == max file + 1:", sum(1 for c in comps if c["width"] == 1 + max(f for f, _ in (lambda w, b: list(w) + list(b))(*bd.parse_pos_text(c["position"])))), "of", len(comps))
ch = json.load(open(P + "/bench/results/conventions_summary.json"))["v1_changed"]
def oc(vw, vb):
    a, c = vw == 1, vb == 1
    return "L" if a and not c else "R" if c and not a else "N" if a else "P"
for tt in (0, 1):
    jobs = []
    for c in ch:
        w, b = bd.parse_pos_text(c["position"]); W = 1 + max(f for f, _ in list(w) + list(b))
        for side in (1, 0):
            jobs.append(f"{W} 0 {side} {tt} 0 0 {len(w)} " + " ".join(f"{f} {r}" for f, r in sorted(w)) + f" {len(b)} " + " ".join(f"{f} {r}" for f, r in sorted(b)))
    inp = "\n".join(jobs) + "\n"
    A = [l.split() for l in subprocess.run([D + "/ab_mine"], input=inp, capture_output=True, text=True, check=True).stdout.splitlines()]
    X = [l.split() for l in subprocess.run([D + "/abx1"], input=inp, capture_output=True, text=True, check=True).stdout.splitlines()]
    s = dict(n=0, tb_agree=0, aw_agree=0, outcome_changes=0, abx_differs=0, differs_but_counter0=0, counter_fires=0)
    for i, c in enumerate(ch):
        a = oc(int(A[2*i][0]), int(A[2*i+1][0])); x = oc(int(X[2*i][0]), int(X[2*i+1][0]))
        t = cgt.outcome(cgtfmt.parse(c["textbook"])); w_ = cgt.outcome(cgtfmt.parse(c["aware"]))
        s["n"] += 1; s["tb_agree"] += a == t; s["aw_agree"] += x == w_; s["outcome_changes"] += t != w_
        dif = A[2*i][:2] != X[2*i][:2] or A[2*i+1][:2] != X[2*i+1][:2]
        ev = int(A[2*i][3]) + int(A[2*i+1][3])
        s["abx_differs"] += dif; s["counter_fires"] += ev > 0; s["differs_but_counter0"] += dif and ev == 0
        if a != t or x != w_: print("  mismatch", c["position"], "ab", a, "cyl-tb", t, "abx1", x, "cyl-aw", w_)
    print("tt", tt, s)
