import json, collections
tot = collections.Counter(); ex = []
for b in ('6x6', '8x6', '7x6'):
    rows = json.load(open(f'ep_{b}.json')); out = open(f'ep_{b}_out.txt').read().splitlines()
    assert len(rows) == len(out)
    c = collections.Counter()
    for r, o in zip(rows, out):
        assert o.split('|')[0].strip() == r['line'], (o, r['line'])
        a, bb = o.split('|')[1].split(); assert a == bb
        agree = (a == 'W') if r['beta'] == 'W' else (a == 'L')
        k = ('single' if r['single'] else 'race', 'cert' if r['certified'] else 'uncert', 'agree' if agree else 'disagree')
        c[k] += 1; c['selftest_bad'] += (not r['selftest_ok'])
        if r['certified'] and not agree: ex.append((b, r['line'], a))
    print(b, len(rows), dict(sorted(c.items(), key=str)))
    tot.update(c)
print('TOTAL', sum(v for k, v in tot.items() if k != 'selftest_bad'), dict(sorted(tot.items(), key=str)))
print('certified disagreements:', ex[:20], len(ex))
