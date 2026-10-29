import sys
# compare my T=0 column (conv C) with kp_p --pmodel and ref3m outputs
mine, kpp, ref = sys.argv[1:4]
m = {}
for ln in open(mine):
    if ln.startswith('#'): continue
    pos, r = ln.rstrip('\n').split('\t'); m[pos] = r[12]
def load(fn, field):
    d = {}
    for ln in open(fn):
        if '|' not in ln: continue
        pos, r = ln.split('|'); pos = pos.strip(); pos = pos[:-2] if pos.endswith(' -') else pos
        d[pos] = r.split()[field]
    return d
a = load(kpp, 0); b = load(kpp, 1); c = load(ref, 0)
n = len(m); diff = sum(1 for p in m if not (m[p] == a.get(p) == b.get(p) == c.get(p)))
print(n, len(a), len(c), 'diffs', diff)
