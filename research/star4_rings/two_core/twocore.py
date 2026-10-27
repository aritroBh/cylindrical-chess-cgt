# Two-core experiment worker.  usage: python3 twocore.py K NWORKERS
# ring = A + W1 + B + W2 (W1 between A and B, W2 between B and A, cyclic); refA = A + W1 + W2 ; refB = B + W2 + W1.
import sys, json, os
from lib import *
K, NW = int(sys.argv[1]), int(sys.argv[2])
TASKS = sys.argv[3] if len(sys.argv) > 3 else "tasks.jsonl"
PFX = sys.argv[4] if len(sys.argv) > 4 else "rows"
ev = Evaluator(f"results_two_{K}.tsv", tbits=23, nodelim=3000000, extra=("results.tsv", "results_blocks.tsv", "results_two_0.tsv", "results_two_1.tsv"))
opp = lambda f: 'B' if f == 'W' else 'W'
def lastof(x): return x['f'] if x['par'] == 'odd' else opp(x['f'])
outname = f"{PFX}_{K}.tsv"
done = set()
if os.path.exists(outname):
    for line in open(outname): done.add(int(line.split("\t")[0]))
out = open(outname, "a")
tasks = [json.loads(l) for l in open(TASKS)]
t0 = time.time(); cnt = 0
for i, t in enumerate(tasks):
    if i % NW != K or i in done: continue
    A, B = t['A'], t['B']
    a, b = R(A['block']), R(B['block'])
    W1, W2 = wall(t['L1'], t['f1']), wall(t['L2'], t['f2'])
    ring = a + W1 + b + W2
    refA = a + W1 + W2
    refB = b + W2 + W1
    matched = int(t['f1'] == A['f'] and t['f2'] == B['f'] and wall_last(t['L1'], t['f1']) == lastof(B) and wall_last(t['L2'], t['f2']) == lastof(A))
    defA = int(W1[-1] == W2[0]); defB = int(W2[-1] == W1[0])
    if not legal_start(ring) or not legal_start(refA) or not legal_start(refB):
        rs, ra, rb = "ILLEGAL", "-", "-"
    else:
        rs = ev.sig(ring); ra = ev.sig(refA); rb = ev.sig(refB)
    vr, va, vb = nimber(rs), nimber(ra), nimber(rb)
    ps = A['v'] ^ B['v']
    pr = (va ^ vb) if isinstance(va, int) and isinstance(vb, int) else None
    out.write("\t".join(map(str, [i, t['kind'], A['block'], A['f'] + A['par'][0], A['v'], B['block'], B['f'] + B['par'][0], B['v'],
              t['f1'], t['L1'], t['f2'], t['L2'], matched, len(ring), S(ring), rs, vr, ra, va, rb, vb, ps, pr, defA, defB])) + "\n")
    cnt += 1
    if cnt % 25 == 0:
        out.flush(); print(K, cnt, f"{time.time()-t0:.0f}s", flush=True)
out.close(); ev.close()
print("worker", K, "done", cnt)
