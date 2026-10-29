#!/usr/bin/env python3
"""build_table.py : candidates x outcome.  One row per symmetry-class representative of every configuration:
config | class size | T_P(w) T_P(b) | outcome | first failing context (Phi | Psi) | mechanism class(es) | where the survivor was checked.
T_P(side) = (loss depth in plies of the side to move in the bare group) / 2 = number of punisher moves in the slowest punished move (see FINDINGS).
Output: data/table_all.tsv, data/table_summary.txt, data/survivors.txt."""
import re, os, glob, collections
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/data/'
cfg = [l.split() for l in open(D + '../scripts/configs.txt') if l.strip() and not l.startswith('#')]
def norm(z): return ' '.join(sorted(z.split()))
BOUND = {
 'cyl7x6_f3': ('all 885 contexts on e,f', ['screen_cyl7x6_f3.txt'], None),
 'cyl8x6_f3': ('first 300 of 4579 (e-g), then all 885 on e,g', ['A_cyl8x6_f3.txt'], 'B_cyl8x6_f3_cf_eg.txt'),
 'cyl7x6_f4': ('all 63 contexts on f', ['A_cyl7x6_f4.txt'], 'B_cyl7x6_f4.txt'),
 'cyl8x6_f4': ('first 300 of 885 (f,g) and all 63 on f', ['A_cyl8x6_f4.txt'], 'B_cyl8x6_f4_cf_f.txt'),
 'flat7x6_f3_z0': ('first 300 of 4579 (e-g), then all 885 on e,f', ['A_flat7x6_f3_z0.txt'], 'B_flat7x6_f3_z0_cf_ef.txt'),
 'flat7x6_f3_z2': ('all 885 contexts on a,g', ['A_flat7x6_f3_z2.txt'], 'B_flat7x6_f3_z2.txt'),
 'flat7x6_f4_z0': ('first 300 of 885 (f,g) and all 63 on f', ['A_flat7x6_f4_z0.txt'], 'B_flat7x6_f4_z0_cf_f.txt'),
 'flat8x6_f3_z0': ('first 300 of 14793 (e-h)', ['A_flat8x6_f3_z0.txt'], None),
 'flat8x6_f3_z2': ('first 300 of 4579 (a,g,h)', ['A_flat8x6_f3_z2.txt'], None),
 'flat8x6_f4_z0': ('first 300 of 4579 (f-h)', ['A_flat8x6_f4_z0.txt'], None),
 'cyl8x6_f3_d3': ('all 63 contexts on f', ['A_cyl8x6_f3_d3.txt'], None),
 'flat7x6_f3_z0_d3': ('first 300 of 885 (f,g)', ['A_flat7x6_f3_z0_d3.txt'], None),
 'flat8x6_f3_z0_d3': ('first 300 of 4579 (f-h)', ['A_flat8x6_f3_z0_d3.txt'], None),
}
def rlines(fn):
    out = {}
    if not fn or not os.path.exists(D + fn): return out
    for l in open(D + fn):
        m = re.match(r'R (.*?) \| contexts_checked (\d+) differ (\d+) parking_mismatch (\d+) \| first fail:(.*)$', l.rstrip('\n'))
        if m: out[norm(m.group(1))] = (m.group(1), int(m.group(2)), int(m.group(3)), m.group(5).strip())
    return out
mech = collections.defaultdict(dict)
for name in BOUND:
    fn = D + 'M_%s.txt' % name
    if not os.path.exists(fn): continue
    for l in open(fn):
        p = [x.strip() for x in l.rstrip('\n').split(' | ')]
        if len(p) >= 6: mech[name].setdefault(norm(p[0]), []).append('%s:%s:%s' % (p[2], p[4].replace(' ', '_'), p[5]))
rows = []; surv = []
summ = []
for name, board, zs, fz, dmin, rep in cfg:
    bound, afiles, bfile = BOUND[name]
    A = {}
    for f in afiles: A.update(rlines(f))
    B = rlines(bfile) if bfile else {}
    classes = [l.rstrip('\n').split(' | ') for l in open(D + 'classes_%s.txt' % rep) if l.strip()]
    DEP = {}
    for l in open(D + 'enum_%s.txt' % rep):
        q = l.rstrip('\n').split(' | ')
        if len(q) >= 2 and q[1].split()[:2] and all(x.isdigit() for x in q[1].split()[:2]): DEP[norm(q[0])] = tuple(map(int, q[1].split()[:2]))
    nf = ns = 0; ngroups = 0; nfgroups = 0; nsgroups = 0
    for rp, dd, size, members in classes:
        dw, db = map(int, dd.split()); k = None
        for mem in [rp] + members.split('; '):
            if norm(mem) in A: k = norm(mem); break
        if k is None: continue
        r = A.get(k)
        dw, db = DEP[k]
        where = 'A'
        if k in B and (B[k][2] > 0 or r[2] == 0): r = B[k]; where = 'B'
        ngroups += int(size)
        if r[2] > 0:
            ph = r[3].rsplit(' | ', 1)
            nf += 1; nfgroups += int(size)
            m = ';'.join(mech[name].get(k, []))
            rows.append((name, A[k][0], size, dw // 2, db // 2, 'FAIL', ph[0].strip(), ph[1] if len(ph) > 1 else '', m, ''))
        else:
            ns += 1; nsgroups += int(size)
            rows.append((name, A[k][0], size, dw // 2, db // 2, 'SURVIVES', '', '', '', bound))
            surv.append((name, A[k][0], size, dw // 2, db // 2))
    summ.append('%s | classes %d | groups %d | failing classes %d (groups %d) | surviving classes %d (groups %d) | boundary: %s' % (name, nf + ns, ngroups, nf, nfgroups, ns, nsgroups, bound))
with open(D + 'table_all.tsv', 'w') as f:
    f.write('config\trep\tclass_size\tTw\tTb\toutcome\tfirst_fail_ctx\tPhi_Psi\tmechanism\tboundary\n')
    for r in rows: f.write('\t'.join(map(str, r)) + '\n')
open(D + 'table_summary.txt', 'w').write('\n'.join(summ) + '\n')
with open(D + 'survivors.txt', 'w') as f:
    for s in surv: f.write(' | '.join(map(str, s)) + '\n')
print('\n'.join(summ))
