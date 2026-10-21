"""Per-position comparison of the verifier's independent run with the worker's JSON files.
  cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/engines/C1-refute/static_eval_c1/compare_worker.py
"""
import json
from collections import Counter
R = "/Users/aritro/Downloads/Research/Chessendgames/"
me = {d["id"]: d for d in json.load(open(R + "verify/engines/C1-refute/static_eval_c1/indep_eval.json"))}
se = {r["id"]: r for r in json.load(open(R + "engine/experiments/results/static_eval.json"))["rows"]}
lc = {r["id"]: r for r in json.load(open(R + "engine/experiments/results/lc0_value_n1.json"))["rows"]}
sf_diff = [i for i in me if abs(me[i]["sf_final_white"] - se[i]["final"]) > 1e-9 or abs(me[i]["sf_nnue_white"] - se[i]["nnue"]) > 1e-9]
def lc_white(d): return d["lc0_cp_stm"] if d["stm"] == "w" else -d["lc0_cp_stm"]
lc_diff = [(i, lc_white(me[i]), lc[i]["lc0_orig_white_cp"]) for i in me if lc_white(me[i]) != lc[i]["lc0_orig_white_cp"]]
lc_sign = [x for x in lc_diff if (x[1] > 0) != (x[2] > 0)]
tb_diff = [i for i in me if me[i]["tb"] != se[i]["tb_root"]]
o_diff = [i for i in me if me[i]["o"] != se[i]["o"]]
print("SF eval differences:", len(sf_diff), sf_diff[:5])
print("Lc0 cp differences:", len(lc_diff), "max |diff|", max((abs(a-b) for _, a, b in lc_diff), default=0), "sign flips:", lc_sign)
print("TB root differences:", tb_diff, "| outcome-class differences:", o_diff)
wl = [d for d in me.values() if d["tb"] in ("win", "loss")]
zero = [(d["id"], d["show"], d["o"], d["tb"], d["sf_final_white"]) for d in me.values() if d["sf_final_white"] == 0]
print("SF 0.00 positions:", zero)
def stm(d): return d["sf_final_white"] if d["stm"] == "w" else -d["sf_final_white"]
print("nimber positions (id, fen, SF stm-POV, Lc0 cp stm-POV, race-sensitive value, worker race_sensitive):")
for d in sorted([d for d in wl if d["nim"]], key=lambda d: d["id"]):
    print(" ", d["id"], d["fen"], f"{stm(d):+.2f}", d["lc0_cp_stm"], d["rs_value"], se[d["id"]]["race_sensitive"], d["comp"])
small = [d for d in wl if abs(stm(d)) < 0.10]
print("win/loss positions with |SF eval| < 0.10:", len(small), Counter((d['o'], (stm(d) > 0) == (d['tb'] == 'win')) for d in small))
# number positions excluded from the worker's 45 by the race filter
nums = [d for d in wl if d["is_num"]]
excl = [d for d in nums if se[d["id"]]["race_sensitive"] or se[d["id"]]["class"] in ("hot-BIG", "decided")]
print("number positions:", len(nums), "| excluded by worker's race filter:", len(excl),
      "| SF right among excluded:", sum((stm(d) > 0) == (d["tb"] == "win") for d in excl))
print("worker 45 set == my race-insensitive-value set:",
      {d["id"] for d in nums if not d["rs_value"]} == {d["id"] for d in nums if not se[d["id"]]["race_sensitive"]})
print("STM counts among win/loss:", Counter(d["stm"] for d in wl), "| N positions by stm:", Counter(d["stm"] for d in wl if d["o"] == "N"))
