"""Sequential queue: for each (family,n) run cyl_run sum then whole; cap 40 min / 3.5 GB; one child at a time."""
import sys, os, time, subprocess, signal, json
sys.path.insert(0, "research/ring_n_plus_2_proof")
import fam
ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
os.chdir(ROOT)
OUT = "research/sum_vs_whole_families"
PY = ROOT + "/.venv/bin/python"
MINN = {"odd":5,"even":6,"F":7,"P":8,"Q":8,"R":9,"Qo":9,"N1":9,"M":10,"O":11,"S3":13,"T3":12}
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 16
DEADLINE = time.time() + float(sys.argv[2]) * 3600 if len(sys.argv) > 2 else time.time() + 2.7 * 3600
TLIM, RLIM = 40 * 60, 3.5 * 2**30
done = set()
res = OUT + "/runs.tsv"
if os.path.exists(res):
    for l in open(res):
        p = l.rstrip("\n").split("\t"); done.add((p[0], p[1], p[2]))
cands = []
for k, f in fam.FAMILIES.items():
    for n in range(MINN[k], NMAX + 1):
        try: t = f(n)
        except AssertionError: continue
        cands.append((n, fam.ntoks_pawns(t), k, " ".join(t)))
cands.sort()
dead = set()
def run(k, n, ring, mode):
    log = f"{OUT}/logs/{k}_{n}_{mode}.log"
    args = [PY, "research/ring_family/cyl_run.py", ring] + (["whole"] if mode == "whole" else [])
    with open(log, "w") as lf:
        p = subprocess.Popen(args, stdout=lf, stderr=subprocess.STDOUT, env=dict(os.environ, PYTHONPATH=ROOT), preexec_fn=lambda: os.nice(15))
    open(f"{OUT}/current.pid", "w").write(str(p.pid))
    t0 = time.time(); status = "ok"; peak = 0
    while True:
        r = os.waitpid(p.pid, os.WNOHANG)
        if r[0]: break
        try:
            rss = int(subprocess.run(["ps", "-o", "rss=", "-p", str(p.pid)], capture_output=True, text=True).stdout.strip() or 0) * 1024
        except Exception: rss = 0
        peak = max(peak, rss)
        if time.time() - t0 > TLIM: status = "timeout40m"
        elif rss > RLIM: status = "rss>3.5GB"
        elif time.time() > DEADLINE: status = "deadline"
        if status != "ok":
            os.kill(p.pid, signal.SIGKILL); os.waitpid(p.pid, 0); break
        time.sleep(2)
    wall = time.time() - t0
    txt = open(log).read().strip().splitlines()
    val = ""
    for l in txt:
        if l.startswith("value = "): val = l[8:].split("  time ")[0]
    if status == "ok" and not val: status = "error"
    if len(val) > 60: val = "COMPLEX:" + val[:50]
    return status, val, wall, peak
for n, pw, k, ring in cands:
    for mode in ("sum", "whole"):
        if k in dead: break
        if (k, str(n), mode) in done: continue
        if time.time() > DEADLINE: sys.exit(0)
        st, val, wall, peak = run(k, n, ring, mode)
        with open(res, "a") as f:
            f.write("\t".join([k, str(n), mode, str(pw), ring, st, val, f"{wall:.1f}", f"{peak/2**20:.0f}"]) + "\n")
        if st != "ok": dead.add(k); break
