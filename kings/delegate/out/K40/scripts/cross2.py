"""K40: compare kpsum.c with ksum2.py on one board, all tests, both conventions.
Usage: python cross2.py W H K   (K = half-width of the integer chain given to ksum2)  -> one JSON line."""
import json, subprocess, sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/..'
PY = sys.executable
W, H, K = sys.argv[1], sys.argv[2], sys.argv[3]
out = {'board': f'cyl:{W}x{H}', 'compared': 0, 'diff': 0, 'examples': []}
for normal in (False, True):
    nf = ['--normal'] if normal else []
    for t in ['ints', 'on', 'off', 'dud', 'over', 'under', 'star', 'up', 'down', 'pm1']:
        a = subprocess.run([f'{D}/bin/kpsum', W, H, '1', t] + nf, capture_output=True, text=True, check=True).stdout.splitlines()
        b = subprocess.run([PY, f'{D}/scripts/ksum2.py', W, H, f'ints:{K}' if t == 'ints' else t] + nf,
                           capture_output=True, text=True, check=True).stdout.splitlines()
        na, nb = a[0].split(':', 1)[1].split(), b[0].split(':', 1)[1].split()
        assert len(a) == len(b)
        for la, lb in zip(a[1:], b[1:]):
            pa, ra = la.split('|'); pb, rb = lb.split('|')
            assert pa == pb
            if t != "ints": na = nb
            da, db = dict(zip(na, ra.split())), dict(zip(nb, rb.split()))
            for k in db:
                out['compared'] += 1
                if da[k] != db[k]:
                    out['diff'] += 1
                    if len(out['examples']) < 10:
                        out['examples'].append([normal, t, k, pa.strip(), da[k], db[k]])
print(json.dumps(out))
