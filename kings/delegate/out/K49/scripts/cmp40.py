"""K49: compare kn.c output with K40's tables.  Usage: python cmp40.py W H MINE [normal|P]"""
import lzma, sys, os
W, H, mine, conv = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
D = os.path.dirname(os.path.abspath(__file__)) + '/../../K40/data'
fh = lzma.open(f'{D}/sums_{"normal_" if conv == "normal" else ""}cyl_{W}x{H}.tsv.xz', 'rt')
cols = fh.readline().rstrip('\n').split('\t')[1:]
ref = {}
for ln in fh:
    pos, *r = ln.rstrip('\n').split('\t'); ref[pos] = r
m = {}
with open(mine) as f:
    rc = f.readline().split()[1:]
    assert rc == cols, (rc, cols)
    for ln in f:
        a, b = ln.split('|'); m[a.strip()] = b.split()
diff = sum(1 for p in ref if m.get(p) != ref[p]) + sum(1 for p in m if p not in ref)
print(f'cyl:{W}x{H} {conv}: positions {len(ref)} mine {len(m)} results {len(ref)*len(cols)} rows differing {diff}')
