"""Re-run the value P-test for listed test rows with a bigger node cap and a 2^24-entry table (wb24)."""
import json, os, sys, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from driver import G, parse_value, job_line, load
HERE = os.path.dirname(os.path.abspath(__file__))
split, cap, nproc = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
ids = json.load(open(os.path.join(HERE, "results", f"value_{split}_final.json")))["unknown"]
rows = {r["id"]: (i, r) for i, r in enumerate(load(split))}
lines = []
for rid in ids:
    i, r = rows[rid]
    gm = G()
    H = gm.export(gm.neg(parse_value(gm, r["value_ascii"])))
    lines.append(job_line(i, r, "count", 1, 1, cap, 1, H))
t0 = time.time()
procs = []
for k in range(nproc):
    ch = lines[k::nproc]
    if not ch:
        continue
    inp, out = os.path.join(HERE, "tmp", f"rerun_{split}_{cap}_{k}.in"), os.path.join(HERE, "tmp", f"rerun_{split}_{cap}_{k}.out")
    open(inp, "w").write("\n".join(ch) + "\n")
    procs.append(subprocess.Popen([os.path.join(HERE, "wb24")], stdin=open(inp), stdout=open(out, "w")))
for p in procs:
    p.wait()
print("done", round(time.time() - t0))
