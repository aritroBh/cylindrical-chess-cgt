import json, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from driver import load
HERE = os.path.dirname(os.path.abspath(__file__))
rows = load("test")
fin = json.load(open(os.path.join(HERE, "results", "value_test_final.json")))
status = {}
for f in sorted(glob.glob(os.path.join(HERE, "tmp", "rerun_test_1000000000_*.out"))):
    cur = None
    for line in open(f):
        x = line.split()
        if x[0] == "J":
            cur = {"id": int(x[1]), "r": []}
        elif x[0] in "MH":
            cur["r"].append(int(x[-1]))
        elif x[0] == "E":
            ok = "disagree" if 1 in cur["r"] else "unknown" if (int(x[4]) or -1 in cur["r"]) else "agree"
            status[rows[cur["id"]]["id"]] = (ok, rows[cur["id"]]["k"], int(x[1]), int(x[2]), int(x[3]))
still = [rid for rid in fin["unknown"] if rid not in status or status[rid][0] != "agree"]
out = {"rerun (cap 1e9 nodes, 2^24 table)": status, "test rows agree in total": fin["agree"] + sum(1 for v in status.values() if v[0] == "agree"),
       "disagree": fin["disagree"] + [k for k, v in status.items() if v[0] == "disagree"], "still unknown": still,
       "still unknown k": [rows[[r["id"] for r in rows].index(x)]["k"] for x in still]}
json.dump(out, open(os.path.join(HERE, "results", "value_test_rerun.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
