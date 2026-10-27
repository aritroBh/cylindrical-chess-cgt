"""verify_ref.py -- re-evaluate results with the UNMODIFIED engine (rg.c, built with -DMAXN=64) and compare.

  python3 verify_ref.py hits      every *3 / *4+ / NNNN* ring in cache.tsv (rg solve 7, batches of 30, line-count check)
  python3 verify_ref.py sample N  N random non-ABORT rings of any value
One rg process at a time, nice 15, TBITS=22 (562 MB).
Compares the full 8-character signature of rg with the (possibly early-stopped, '?'-padded) one of rgf.
"""
import sys, os, random, subprocess, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grow import load_cache, kind

mode = sys.argv[1]
cache = load_cache()
rows = [f for f in cache.values() if f[3] == 'OK']
if mode == 'hits':
    # every *3 of rounds 0-1, every *4+/NNNN* ring, and a random 600 of the *3 of rounds 2-3 (full set too slow on the loaded machine)
    allh = [f for f in rows if kind(f[1]) in ('*3', '*4', '*5', '*6', '*7') or (f[1].startswith('NNNN') and f[1] != 'NNNNNNNN')]
    early = [f for f in allh if int(f[4]) <= 1 or kind(f[1]) != '*3']
    late = [f for f in allh if int(f[4]) >= 2 and kind(f[1]) == '*3']
    random.seed(5)
    sel = early + random.sample(late, min(int(os.environ.get('NLATE', '600')), len(late)))
else:
    random.seed(99)
    sel = random.sample(rows, int(sys.argv[2]))
env = dict(os.environ, TBITS='22')


def run(batch):
    p = subprocess.run(['nice', '-n', '15', './rg', 'solve', '7'], input='\n'.join(b[0] for b in batch) + '\n',
                       capture_output=True, text=True, env=env, timeout=3000)
    out = [l for l in p.stdout.splitlines() if l.strip()]
    return out if len(out) == len(batch) and p.returncode == 0 else None


res = {}
B = 20
for i in range(0, len(sel), B):
    batch = sel[i:i + B]
    out = run(batch)
    if out is None:                       # table full or crash: one position per call
        out = []
        for b in batch:
            o = run([b])
            out.append(o[0] if o else 'FAIL nodes=0')
    for b, o in zip(batch, out):
        res[b[0]] = o.split()[0]
    print('progress', i + len(batch), '/', len(sel), flush=True)
agree = disagree = fail = 0
bad = []
for f in sel:
    r = res[f[0]]
    if r == 'FAIL':
        fail += 1
        continue
    mine = f[1]
    ok = all(m == '?' or m == c for m, c in zip(mine, r))
    if ok:
        agree += 1
    else:
        disagree += 1
        bad.append((f[0], mine, r))
print('mode', mode, 'checked', len(sel), 'agree', agree, 'disagree', disagree, 'fail', fail)
cnt = collections.Counter(kind(res[f[0]]) for f in sel if res[f[0]] != 'FAIL')
print('reference engine values:', dict(cnt))
for b in bad[:20]:
    print('DISAGREE', b)
