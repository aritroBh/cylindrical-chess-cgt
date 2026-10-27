import subprocess, sys
RG = './rg'
def solve(lines, chunk=40):
    out = []
    for i in range(0, len(lines), chunk):
        part = lines[i:i + chunk]
        r = subprocess.run([RG, 'solve', '7'], input='\n'.join(part) + '\n', capture_output=True, text=True)
        o = [x.split()[0] for x in r.stdout.split('\n') if x.strip()]
        if len(o) != len(part):
            o = []
            for p in part:
                r = subprocess.run([RG, 'solve', '7'], input=p + '\n', capture_output=True, text=True)
                x = [y.split()[0] for y in r.stdout.split('\n') if y.strip()]
                o.append(x[0] if x else 'FULL')
        out += o
    assert len(out) == len(lines)
    return out
lines = [l.strip() for l in open(sys.argv[1]) if l.strip()]
sig = solve(lines)
with open(sys.argv[2], 'w') as f:
    for l, s in zip(lines, sig): f.write(f'{s}\t{len(l.split())}\t{l}\n')
from collections import Counter
c = Counter(sig)
def nim(s):
    return s.index('P') if s.count('P') == 1 and set(s) <= {'N', 'P'} else None
nims = Counter(nim(s) for s in sig)
print('positions', len(lines), 'nimbers', dict(nims), 'FULL', c.get('FULL', 0))
