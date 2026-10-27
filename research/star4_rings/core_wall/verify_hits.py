#!/usr/bin/env python3
"""Re-evaluate every HIT line (examples of *0..*2 plus all first-non-N>=3) of out/*.res with the unmodified rg (MAXN=64, solve 7),
batches of 30, one position per call on a count mismatch.  Prints disagreements and a summary."""
import glob, subprocess, os, sys
hits = []
for f in sorted(glob.glob('out/*.res')):
    if not os.path.exists(f[:-4] + '.done'): continue
    for line in open(f):
        if line.startswith('HIT\t'):
            p = line.rstrip('\n').split('\t'); hits.append((p[1], p[2]))
seen = {}
for r, s in hits: seen[r] = s
items = sorted(seen.items())
print('distinct HIT rings:', len(items))
bad = 0; checked = 0
def ref_sig(r):
    for tb in ('21', '23'):
        o = subprocess.run(['nice', '-n', '15', './rg', 'solve', '7'], input=r + '\n', capture_output=True, text=True, env=dict(os.environ, TBITS=tb))
        lines = o.stdout.strip().split('\n')
        if o.returncode == 0 and len(lines) == 1 and lines[0]: return lines[0].split()[0]
    return None
for i in range(0, len(items), 30):
    batch = items[i:i + 30]
    inp = '\n'.join(r for r, _ in batch) + '\n'
    o = subprocess.run(['nice', '-n', '15', './rg', 'solve', '7'], input=inp, capture_output=True, text=True, env=dict(os.environ, TBITS='21'))
    lines = o.stdout.strip().split('\n') if o.stdout.strip() else []
    if o.returncode != 0 or len(lines) != len(batch):
        lines = [ref_sig(r) or 'FAIL' for r, _ in batch]
    else:
        lines = [l.split()[0] for l in lines]
    for (r, s), l in zip(batch, lines):
        checked += 1
        # rgq early-stop signature: compare prefix to first non-N, and tail N if P
        k = next((j for j, c in enumerate(l) if c != 'N'), None)
        if k is None: exp = 'N' * 8
        elif l[k] == 'P': exp = l[:k] + 'P' + 'N' * (7 - k)
        else: exp = l[:k + 1] + '.' * (7 - k)
        if exp != s:
            bad += 1; print('DISAGREE', r, 'rgq=', s, 'rg=', l)
        else:
            print('ok', r, '|', l)
print('checked', checked, 'disagreements', bad)
