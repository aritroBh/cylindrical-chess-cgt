#!/usr/bin/env python3
"""Validation 3: confirm each reported *2 / *3 minimum hit (and every *>=4 candidate) with cylcgt (whole-board).
usage (project root, PYTHONPATH=.): .venv/bin/python research/tall_boards/val3.py out.txt [TLIM_S]
For every (board,R) and q in {2,3} it takes the first hit at the least p in results/hits.tsv and runs pycheck.py on it in a subprocess
(timeout TLIM_S, killed by its own PID only)."""
import subprocess, sys, os, collections, resource, time
T = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(T + "/../..")
out = open(sys.argv[1], "a"); tl = int(sys.argv[2]) if len(sys.argv) > 2 else 300
best = {}
for line in open(T + "/results/hits.tsv"):
    f = line.rstrip("\n").split("\t")
    F, w, R, p = int(f[0]), int(f[1]), int(f[2]), int(f[3]); q = int(f[5][1:]); pos = f[8]; sig = f[9]
    k = (F, w, R, q)
    if k not in best or p < best[k][0]: best[k] = (p, pos, sig)
env = dict(os.environ, PYTHONPATH=ROOT)
for k in sorted(best, key=lambda k: (best[k][0], k[2], k[0], k[1], k[3])):
    F, w, R, q = k; p, pos, sig = best[k]
    if len(sys.argv) > 3 and str(R) not in sys.argv[3].split(","): continue
    cmd = ["nice", "-n", "15", ROOT + "/.venv/bin/python", T + "/pycheck.py", str(F), str(w), str(R), pos]
    t0 = time.time()
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env, cwd=ROOT)
    open(T + "/logs/val3.pid", "w").write(str(pr.pid))
    try:
        o, e = pr.communicate(timeout=tl); res = o.strip() or e.strip()[-200:]
    except subprocess.TimeoutExpired:
        pr.kill(); pr.communicate(); res = f"TIMEOUT {tl}s"
    ok = ("MATCH" if res.split("|")[1].strip() == sig else "MISMATCH") if "|" in res else "NO-RESULT"
    out.write(f"{ok}\tF={F} {'cyl' if w else 'flat'} R={R} *{q} p={p}\tC: {sig}\tcylcgt: {res}\t({time.time()-t0:.0f}s)\n"); out.flush()
