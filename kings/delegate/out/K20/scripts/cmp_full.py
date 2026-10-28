import sys
pred = [l.rstrip('\n').split(' | ') for l in open(sys.argv[1])]
res = {}
for l in open(sys.argv[2]):
    if l.startswith('['): continue
    p, r = l.rstrip('\n').split(' | ')
    res[p.strip()] = r.split()
ok = bad = 0
rows = []
for pos, g, c, cv, pr in pred:
    r = res[pos.strip()]
    got = r[0] if r[0] == r[1] else r[0] + '/' + r[1]
    match = (r[0] == r[1] == pr)
    ok += match; bad += (not match)
    rows.append((g, c, pos.split()[-2], pr, got, 'ok' if match else 'MISMATCH'))
for r in rows: print(*r)
print('match', ok, 'mismatch', bad)
