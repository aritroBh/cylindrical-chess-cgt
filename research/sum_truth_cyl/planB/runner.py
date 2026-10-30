"""usage: runner.py JOBS.json OUTDIR K N CAP [frozen]. One kpsolve process per job, nice 15, RSS watchdog (kills only its own PID)."""
import sys, json, os, subprocess, time, re
D = '/Users/aritro/Downloads/Research/Chessendgames/research/sum_truth_cyl/planB'
KP = '/Users/aritro/Downloads/Research/Chessendgames/kings/kpsolve'
jobs = json.load(open(sys.argv[1])); outd = sys.argv[2]; k, n, cap = int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
frozen = len(sys.argv) > 6
LIMIT = 3600000
os.makedirs(outd, exist_ok=True)
open(f'{outd}/runner{k}.pid', 'w').write(str(os.getpid()))
for j, name in enumerate(jobs):
    if j % n != k: continue
    out = f'{outd}/{name}.json'
    if os.path.exists(out): continue
    t0 = time.time()
    cmd = ['nice', '-n', '15', '/usr/bin/time', '-l', KP, '--board', 'cyl:8x6', '--ep', 'on', '--promote', 'Q', '--cap', cap, '--threads', '2'] + (['--frozen'] if frozen else [])
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    p.stdin.write('\n'.join(jobs[name]) + '\n'); p.stdin.close()
    killed = False; peak = 0; child = None
    while p.poll() is None:
        time.sleep(1)
        if child is None:
            r = subprocess.run(['pgrep', '-P', str(p.pid)], capture_output=True, text=True).stdout.split()
            child = int(r[0]) if r else None
            if child: open(f'{outd}/runner{k}.kp.pid', 'w').write(str(child))
        if child:
            r = subprocess.run(['ps', '-o', 'rss=', '-p', str(child)], capture_output=True, text=True).stdout.strip()
            if r:
                peak = max(peak, int(r))
                if int(r) > LIMIT: os.kill(child, 15); killed = True
    so = p.stdout.read(); se = p.stderr.read()
    m = re.search(r'(\d+)\s+maximum resident', se)
    json.dump({'name': name, 'lines': jobs[name], 'stdout': so.splitlines(), 'killed_over_limit': killed, 'maxrss_bytes': int(m.group(1)) if m else None,
               'secs': round(time.time() - t0, 1), 'kp_msg': [l for l in se.splitlines() if l.startswith('[kpsolve')]}, open(out, 'w'))
