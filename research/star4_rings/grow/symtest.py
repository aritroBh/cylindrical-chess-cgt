import sys, random, subprocess, os
sys.path.insert(0, '.')
from growlib import *
random.seed(7)
seeds = [parse(l.split('\t')[0]) for l in open('seeds_all.txt')]
pool = {}
for s in seeds:
    for name, q in neighbours(s):
        pool[canon(q)] = name
cs = sorted(pool)
sample = random.sample(cs, 120)
lines, meta = [], []
for i, c in enumerate(sample):
    vs = variants(c)
    n = len(c)
    picks = [(vs[0], 0)] + [(vs[j], 1 if j >= 2 * n else 0) for j in random.sample(range(len(vs)), 3)]
    for v, fl in picks:
        lines.append(fmt(v)); meta.append((i, fl))
env = dict(os.environ, TBITS='22', NODELIM='3000000')
p = subprocess.run(['nice', '-n', '15', './rgf', 'solve', '7'], input='\n'.join(lines) + '\n', capture_output=True, text=True, env=env)
out = [l.split('\t') for l in p.stdout.splitlines()]
assert len(out) == len(lines), (len(out), len(lines))
from collections import defaultdict
g = defaultdict(set); ab = 0
for (m, fl), o in zip(meta, out):
    if o[1] == 'ABORT': ab += 1; continue
    sg = o[1].translate(str.maketrans('LR', 'RL')) if fl else o[1]
    g[m].add(sg)
bad = [m for m, s in g.items() if len(s) > 1]
print('positions', len(sample), 'evals', len(lines), 'aborts', ab, 'inconsistent groups', len(bad))
from collections import Counter
print(Counter(next(iter(s)) for s in g.values() if len(s) == 1).most_common(8))
