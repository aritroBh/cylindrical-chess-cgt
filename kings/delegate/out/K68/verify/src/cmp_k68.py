# Compare r68 P values with the K68 investigator's compare_values.txt (o68 and ax68q).
# usage: python3 cmp_k68.py <compare_values.txt> <r68 binary>
import subprocess, sys
def fen(wk, bk, wp, bp, side):
    b = {}
    b[wk] = 'K'; b[bk] = 'k'
    for s in wp: b[s] = 'P'
    for s in bp: b[s] = 'p'
    rows = []
    for r in range(8, 0, -1):
        row, e = '', 0
        for f in 'abcdefgh':
            c = b.get(f + str(r))
            if not c: e += 1; continue
            if e: row += str(e); e = 0
            row += c
        if e: row += str(e)
        rows.append(row)
    return '/'.join(rows) + ' ' + side
lines, theirs = [], []
for ln in open(sys.argv[1]):
    if ln.startswith('#') or ':' not in ln: continue
    a, b = ln.split(':')
    t = a.split()
    wk, bk, wp, bp, side = t
    wp = [] if wp == '-' else wp.split(','); bp = [] if bp == '-' else bp.split(',')
    lines.append(fen(wk, bk, wp, bp, side)); theirs.append(b.split())
out = subprocess.run([sys.argv[2], 'query'], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout
mine = {}
for ln in out.splitlines():
    if ln.startswith('   '): continue
    f = ' '.join(ln.split()[:2]); v = ln.split('P=')[1][0] if 'P=' in ln else 'INVALID'
    mine[f] = v
dis = 0
for f, t in zip(lines, theirs):
    m = mine.get(f, '?')
    if not (m == t[0] == t[1]): dis += 1; print('DIFF', f, 'r68', m, 'o68', t[0], 'ax68q', t[1])
print('positions', len(lines), 'disagreements', dis)
