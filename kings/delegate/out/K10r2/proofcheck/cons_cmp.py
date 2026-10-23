import sys, json
out = sys.argv[1]
items = json.load(open(out + '.json'))
res = {}
for ln in open(out + '.res'):
    if ' | ' in ln:
        a, b = ln.rstrip().split(' | '); res[a] = b.split()
bad = 0; nw = nb = 0
for L, cw, cb in items:
    r = res[L][0]
    if cw:
        nw += 1
        if r != 'W': bad += 1; print("VIOL white", L, r)
    if cb:
        nb += 1
        if r != 'L': bad += 1; print("VIOL black", L, r)
print("cons wins checked", nw, nb, "violations", bad)
