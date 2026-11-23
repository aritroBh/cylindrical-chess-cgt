"""Worker k of n: runs kpsolve (cyl:8x6, ep on, promote Q) one job at a time under nice 15, polls RSS, kills only its own
kpsolve PID above LIMIT. Usage: worker.py K N CAP"""
import sys, json, os, subprocess, time, re
D = '/Users/aritro/Downloads/Research/Chessendgames/research/sum_truth_cyl'
KP = '/Users/aritro/Downloads/Research/Chessendgames/kings/kpsolve'
k, n, cap = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
LIMIT = int(os.environ.get('LIMIT_KB', '3600000'))  # KB
open(f'{D}/workerC{k}_cap{cap}.pid', 'w').write(str(os.getpid()))
items = json.load(open(D + '/pairs.json'))
jobs = {}
jobs['Z'] = ['Pa3 pa4 Kh4 kb3 w -', 'Pa3 pa4 Kh4 kb3 b -']
for it in items:
    for t in ('A', 'B'):
        s = it['solo' + t]; jobs['solo_' + s[0][:-4].replace(' ', '_')] = list(s)
names = list(jobs)
MAXP = int(os.environ.get('MAXP', '99'))
ONLY = os.environ.get('ONLY')
npw = lambda s: len(s.replace('W:', '').replace('B:', '').replace('/', '').split())
order = sorted(range(len(items)), key=lambda i: (npw(items[i]['A']) + npw(items[i]['B']), i))
if ONLY: order = [int(x) for x in ONLY.split(',')]
for i in order:
    it = items[i]
    if npw(it['A']) + npw(it['B']) > MAXP: continue
    jobs[f'pair{i:02d}'] = [it['wtm'], it['btm']]; names.append(f'pair{i:02d}')
names = [x for x in names if x.startswith('pair')]
for j, name in enumerate(names):
    if j % n != k: continue
    out = f'{D}/jobs12/{name}_cap{cap}.json'
    if os.path.exists(out): continue
    t0 = time.time()
    p = subprocess.Popen(['nice', '-n', '15', '/usr/bin/time', '-l', KP, '--board', 'cyl:8x6', '--ep', 'on', '--promote', 'Q', '--cap', cap, '--threads', '2'],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    p.stdin.write('\n'.join(jobs[name]) + '\n'); p.stdin.close()
    killed = False; peak = 0; child = None
    while p.poll() is None:
        time.sleep(2)
        if child is None:
            r = subprocess.run(['pgrep', '-P', str(p.pid)], capture_output=True, text=True).stdout.split()
            child = int(r[0]) if r else None
            if child: open(f'{D}/workerC{k}_cap{cap}.kp.pid', 'w').write(str(child))
        if child:
            r = subprocess.run(['ps', '-o', 'rss=', '-p', str(child)], capture_output=True, text=True).stdout.strip()
            if r:
                peak = max(peak, int(r))
                if int(r) > LIMIT:
                    os.kill(child, 15); killed = True
    so = p.stdout.read(); se = p.stderr.read()
    m = re.search(r'(\d+)\s+maximum resident', se)
    res = {'name': name, 'lines': jobs[name], 'stdout': so.splitlines(), 'killed_over_limit': killed, 'peak_rss_kb_polled': peak,
           'maxrss_bytes': int(m.group(1)) if m else None, 'secs': round(time.time() - t0, 1),
           'kp_msg': [l for l in se.splitlines() if l.startswith('[kpsolve')]}
    json.dump(res, open(out, 'w'))
