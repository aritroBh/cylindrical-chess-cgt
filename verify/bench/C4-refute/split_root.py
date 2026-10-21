"""Finish the last capped test rows by splitting the P-test over root moves: one job per
(side, root move); the row agrees iff every root move loses for its mover."""
import json, os, sys, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from driver import G, parse_value, job_line, load
HERE = os.path.dirname(os.path.abspath(__file__))
ids, cap, nproc = sys.argv[1].split(","), int(sys.argv[2]), int(sys.argv[3])
rows = {r["id"]: (i, r) for i, r in enumerate(load("test"))}
jobs = []
for rid in ids:
    i, r = rows[rid]
    gm = G()
    H = gm.export(gm.neg(parse_value(gm, r["value_ascii"])))
    nH = {"W": len(H[0][0]), "B": len(H[0][1])}
    for side, c in (("W", 1), ("B", 2)):
        n = len(r["legal_moves"][side]) + nH[side]
        for k in range(n):
            base = job_line(i, r, "count", 1, 1, cap, 0, H).split()
            base.insert(8, str(c)); base.insert(9, str(k))   # after the stop flag
            jobs.append((rid, side, k, " ".join(base)))
print(len(jobs), "jobs", flush=True)
t0 = time.time()
queue = list(enumerate(jobs))
running, results = [], {}
while queue or running:
    while queue and len(running) < nproc:
        j, (rid, side, k, line) = queue.pop(0)
        p = subprocess.Popen([os.path.join(HERE, "wbroot")], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        p.stdin.write(line + "\n"); p.stdin.close()
        running.append((j, rid, side, k, p))
    time.sleep(2)
    for t in list(running):
        j, rid, side, k, p = t
        if p.poll() is not None:
            out = p.stdout.read().split("\n")
            res = [int(x.split()[-1]) for x in out if x[:1] in ("M", "H")]
            E = [x for x in out if x.startswith("E")][0].split()
            results[(rid, side, k)] = (res, E[1:])
            running.remove(t)
            print(rid, side, k, res, E[1:], round(time.time() - t0), flush=True)
summary = {}
for rid in ids:
    rs = [v for (a, _, _), v in results.items() if a == rid]
    flat = [x for v in rs for x in v[0]]
    summary[rid] = {"jobs": len(rs), "any mover win (disagree)": 1 in flat, "any unknown": -1 in flat,
                    "all lose (agree)": len(flat) > 0 and all(x == 0 for x in flat),
                    "ep events": sum(int(v[1][1]) + int(v[1][2]) for v in rs)}
json.dump(summary, open(os.path.join(HERE, "results", "value_test_split_root.json"), "w"), indent=1)
print(json.dumps(summary, indent=1))
