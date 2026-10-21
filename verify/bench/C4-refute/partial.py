"""Tally a (possibly interrupted) value-mode run on the test split, then finish the rows that
are not done with a node cap, and report.  Same comparisons as driver.py value."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from driver import G, parse_value, job_line, run_jobs, load
HERE = os.path.dirname(os.path.abspath(__file__))
split, tag, cap, nproc = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
rows = load(split)
done = {}
k = 0
while os.path.exists(os.path.join(HERE, "tmp", f"{tag}_{k}.out")):
    cur = None
    for line in open(os.path.join(HERE, "tmp", f"{tag}_{k}.out")):
        x = line.split()
        if x[0] == "J":
            cur = {"id": int(x[1]), "r": []}
        elif x[0] in "MH":
            cur["r"].append((x[1], int(x[-1])))
        elif x[0] == "E":
            cur["E"] = tuple(map(int, x[1:]))
            done[cur["id"]] = cur
    k += 1
todo = [i for i in range(len(rows)) if i not in done]
print(f"previously finished {len(done)}, to do {len(todo)} with cap {cap}", flush=True)
t0 = time.time()
if todo:
    lines = []
    for i in todo:
        gm = G()
        H = gm.export(gm.neg(parse_value(gm, rows[i]["value_ascii"])))
        lines.append(job_line(i, rows[i], "count", 1, 1, cap, 1, H))
    res = run_jobs(lines, nproc, tag + f"_rest_cap{cap}")
    for i, o in res.items():
        done[i] = {"id": i, "r": [(m[0], m[5]) for m in o["M"]] + [(h[0], h[2]) for h in o["H"]], "E": o["E"]}
from collections import Counter
c, bad, unk = Counter(), [], []
epa = epd = 0
for i, r in enumerate(rows):
    o = done[i]
    epa += o["E"][1]; epd += o["E"][2]
    vals = [v for _, v in o["r"]]
    if any(v == 1 for v in vals):
        c[("disagree", r["k"])] += 1; bad.append(r["id"])
    elif o["E"][3] or any(v < 0 for v in vals):
        c[("unknown", r["k"])] += 1; unk.append(r["id"])
    else:
        c[("agree", r["k"])] += 1
out = {"split": split, "rows": len(rows), "by_status_k": {f"{a} k={b}": n for (a, b), n in sorted(c.items())},
       "agree": sum(n for (a, _), n in c.items() if a == "agree"), "disagree": bad, "unknown": unk,
       "ep_capture_available_events": epa, "ep_test_differs_events": epd, "cap_for_rest": cap,
       "seconds_rest": round(time.time() - t0)}
json.dump(out, open(os.path.join(HERE, "results", f"value_{split}_final.json"), "w"), indent=1)
print(json.dumps(out))
