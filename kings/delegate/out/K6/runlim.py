"""Run one command with limits and measure it:  runlim.py LABEL MAX_SECONDS MAX_RSS_MB OUTFILE -- cmd ...

Polls `ps` ~5 times a second for the command and its descendants (processes this script started).
If any single process exceeds MAX_RSS_MB, or the wall time exceeds MAX_SECONDS, it terminates its OWN process
group (only processes it started) and exits 99.  Appends one JSON line to <OUTFILE>:
label, rc, seconds, peak_single_rss_mb, peak_total_rss_mb, killed (None | 'rss' | 'time'), tree_maxrss_mb (exact peak RSS of the largest process in the tree).
"""
import json
import os
import resource
import signal
import subprocess
import sys
import time


def snapshot():
    out = subprocess.run(['ps', '-axo', 'pid=,ppid=,rss='], capture_output=True, text=True).stdout
    rows = {}
    for line in out.splitlines():
        try:
            pid, ppid, rss = map(int, line.split())
        except ValueError:
            continue
        rows[pid] = (ppid, rss)
    return rows


def descendants(rows, root):
    kids = {root}
    changed = True
    while changed:
        changed = False
        for pid, (ppid, _) in rows.items():
            if ppid in kids and pid not in kids:
                kids.add(pid)
                changed = True
    return kids


def main():
    label, max_s, max_mb, outfile = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    cmd = sys.argv[sys.argv.index('--') + 1:]
    t0 = time.time()
    p = subprocess.Popen(cmd, start_new_session=True)
    peak_single = peak_total = 0
    killed = None
    while p.poll() is None:
        rows = snapshot()
        mine = descendants(rows, p.pid)
        rss = [rows[x][1] for x in mine if x in rows]
        if rss:
            peak_single = max(peak_single, max(rss))
            peak_total = max(peak_total, sum(rss))
        if max(rss or [0]) / 1024.0 > max_mb:
            killed = 'rss'
        elif time.time() - t0 > max_s:
            killed = 'time'
        if killed:
            os.killpg(p.pid, signal.SIGTERM)     # our own process group only
            time.sleep(1.0)
            if p.poll() is None:
                os.killpg(p.pid, signal.SIGKILL)
            break
        time.sleep(0.2)
    rc = p.wait()
    rec = dict(label=label, rc=rc, seconds=round(time.time() - t0, 1), peak_single_rss_mb=round(peak_single / 1024.0, 1),
               peak_total_rss_mb=round(peak_total / 1024.0, 1), killed=killed,
               # exact: largest RSS of any process in the waited-for tree (bytes on macOS)
               tree_maxrss_mb=round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1048576.0, 1))
    with open(outfile, 'a') as f:
        f.write(json.dumps(rec) + '\n')
    print(json.dumps(rec), flush=True)
    sys.exit(99 if killed else rc)


main()
