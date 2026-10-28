import sys, collections
pre = sys.argv[1]
ins = [l.strip() for l in open(pre + '.in')]
meta = [l.split() for l in open(pre + '.meta')]
out = [l.strip() for l in open(pre + '.out')]
assert len(ins) == len(meta) == len(out), (len(ins), len(meta), len(out))
C = collections.Counter()
for l, m, o in zip(ins, meta, out):
    beta = int(m[0]); ok = int(m[4]); h = int(m[6]); kind = m[5]
    v = o.split('|')[1].split()
    assert v[0] == v[1], o
    win = (v[0] == 'W') if beta == 0 else (v[0] == 'L')
    C[('NSok' if ok else 'NSfail:' + kind, 'betaWins' if win else 'notwin:' + v[0])] += 1
    if h and not ok: C['H3K_but_NSfail'] += 1
    if ok and not win: print('COUNTEREXAMPLE to Theorem 2.11K:', l, o)
for k, v in sorted(C.items(), key=str): print(k, v)
