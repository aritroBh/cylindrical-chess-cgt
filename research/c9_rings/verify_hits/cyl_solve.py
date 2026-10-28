"""cyl_solve.py MODE "<ring tokens>" [OUTFILE]  -- evaluate a ring with cylcgt (default setting: RACE_RULE=count,
PASSED_RESPECTS_EP=True, ep on).  MODE = whole  (pawns.components = lambda b, p: [p], the whole-board game)
                                         sum    (cylcgt's default: split into components, the sum model)
Prints the value, the signature of G+*h for h = 0..3, wall time, CPU time, max RSS.  Appends one TSV line to OUTFILE.
A watchdog thread exits the process (rc 4) if the RSS exceeds 3.6 GB.
Run from the project root:  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -B <this file> ...
"""
import sys, os, time, resource, threading, subprocess, json
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ringtools as rt
from cylcgt import pawns, cgt
from cylcgt.pawns import Board, Pos

mode, ring_txt = sys.argv[1], sys.argv[2]
outfile = sys.argv[3] if len(sys.argv) > 3 else None
LIMIT = int(3.6 * 2**30)

def rss_now():
    try:
        return int(subprocess.run(["ps", "-o", "rss=", "-p", str(os.getpid())], capture_output=True, text=True).stdout.strip()) * 1024
    except Exception:
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

peak = [0]
def watchdog():
    while True:
        time.sleep(5)
        r = rss_now(); peak[0] = max(peak[0], r)
        if r > LIMIT:
            sys.stderr.write("WATCHDOG: RSS %.2f GB over limit, exiting\n" % (r / 2**30)); sys.stderr.flush()
            if outfile:
                open(outfile, "a").write("%s\t%s\tRSS_LIMIT\t-\t-\t%.0f\t%.0f\t%.0f\n" % (mode, ring_txt, time.time() - t0, time.process_time(), r / 2**20))
            os._exit(4)
# a (mode, ring) is solved by at most one process: lock file next to the logs (queues A and B may overlap)
import hashlib
os.makedirs(os.path.join(HERE, "logs", "locks"), exist_ok=True)
lock = os.path.join(HERE, "logs", "locks", hashlib.md5((mode + "|" + ring_txt).encode()).hexdigest())
try:
    os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
except FileExistsError:
    print("SKIP: %s %s already started by another process" % (mode, ring_txt)); sys.exit(0)
t0 = time.time()
threading.Thread(target=watchdog, daemon=True).start()

ring = rt.parse(ring_txt); n = len(ring)
pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True; pawns._value.cache_clear()
if mode == "whole":
    pawns.components = lambda b, p: [p]
elif mode != "sum":
    raise SystemExit("mode must be whole or sum")
pos_text = rt.to_pos_text(ring)
assert not rt.legality(ring, n), rt.legality(ring, n)
print("C%d pawns=%d mode=%s: %s" % (n, sum(len(w) + len(b) for w, b in ring), mode, pos_text), flush=True)
b = Board(n, 8, True, True)
g = pawns.value(b, Pos.parse(pos_text))
val = cgt.show(g)
sig = "".join(cgt.outcome(cgt.add(g, cgt.nimber(h))) for h in range(4))
wall = time.time() - t0; cpu = time.process_time()
rss = max(peak[0], resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 2**20   # macOS: bytes
print("value = %s   signature(G+*h,h=0..3) = %s   wall %.1fs cpu %.1fs  maxrss %.0f MB  race_hits=%d  games=%d" %
      (val, sig, wall, cpu, rss, len(pawns.race_hits), len(cgt._table)), flush=True)
if outfile:
    open(outfile, "a").write("%s\t%s\t%s\t%s\t%s\t%.0f\t%.0f\t%.0f\n" % (mode, ring_txt, val, sig, "ok", wall, cpu, rss))
