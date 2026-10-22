"""run a command (a child of this process), poll its process tree RSS every 0.5 s, stop OUR child tree if it
exceeds LIMIT_MB or TIMEOUT seconds; append a record to logs/limits.jsonl.
usage: v6_lim.py label limit_mb timeout_s -- cmd..."""
import json, os, subprocess, sys, time
label, limit_mb, timeout_s = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
cmd = sys.argv[sys.argv.index('--') + 1:]
HERE = os.path.dirname(os.path.abspath(__file__))
t0 = time.time()
p = subprocess.Popen(cmd)


def tree_rss(pid):
    out = subprocess.run(['ps', '-axo', 'pid=,ppid=,rss='], capture_output=True, text=True).stdout.split('\n')
    kids = {}
    rss = {}
    for l in out:
        f = l.split()
        if len(f) == 3:
            a, b, c = int(f[0]), int(f[1]), int(f[2])
            kids.setdefault(b, []).append(a)
            rss[a] = c
    todo, seen = [pid], []
    while todo:
        x = todo.pop()
        seen.append(x)
        todo += kids.get(x, [])
    return [(x, rss.get(x, 0) / 1024.0) for x in seen]


peak_single = peak_total = 0.0
killed = None
while p.poll() is None:
    time.sleep(0.5)
    t = tree_rss(p.pid)
    tot = sum(r for _, r in t)
    peak_total = max(peak_total, tot)
    peak_single = max([peak_single] + [r for _, r in t])
    if tot > limit_mb or time.time() - t0 > timeout_s:
        killed = 'rss %.0f MB' % tot if tot > limit_mb else 'timeout'
        for pid, _ in t:      # only processes in OUR child's tree
            try:
                os.kill(pid, 15)
            except OSError:
                pass
        break
rc = p.wait()
os.makedirs(os.path.join(HERE, 'logs'), exist_ok=True)
with open(os.path.join(HERE, 'logs', 'limits.jsonl'), 'a') as f:
    f.write(json.dumps(dict(label=label, rc=rc, seconds=round(time.time() - t0, 1), peak_single_mb=round(peak_single, 1),
                            peak_tree_mb=round(peak_total, 1), killed=killed)) + '\n')
sys.exit(rc)
