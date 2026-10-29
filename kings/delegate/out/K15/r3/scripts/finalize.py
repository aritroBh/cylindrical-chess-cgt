#!/usr/bin/env python3
"""K15 r3: write the parts of FINDINGS.md that depend on this attempt's own runs (fin2/body_head.md, fin2/body_verdicts.md, fin2/logs/over_followup.md,
r3/additions.md) from the logs in r3/logs, then run fin2/scripts/assemble.py.  Numbers are read from the logs, never typed."""
import os, re, json, subprocess, sys
R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); K15 = os.path.dirname(R3); FIN2 = os.path.join(K15, 'fin2')
def rd(p, d=''):
    try: return open(p).read()
    except Exception: return d
L = lambda n: rd(os.path.join(R3, 'logs', n))

# ---- Z* contexts ----
zs = [l for l in L('ctxexh_surv_chunked.txt').splitlines() if l.startswith('Kd5 kb5')]
def zline(l):
    m = re.search(r'(cyl:\d+x\d+)?.*file (\w): (\d+) contexts \((\d+) to (\d+) pawns\) x 2 sides = (\d+) positions: agree (\d+), DISAGREE (\d+), inexact (\d+), missing (\d+)', l)
    return m
zrows = []
for l in zs:
    m = zline(l)
    if m: zrows.append(m.groups())
zs_text = ''
tot = [0, 0, 0, 0, 0]
for g in zrows:
    zs_text += ''
    for i, k in enumerate((5, 6, 7, 8, 9)): tot[i] += int(g[k])
ref16 = [l for l in rd(os.path.join(R3, 'data', 'zstar_ref16.out')).splitlines() if ' | ' in l]
ref16_in = [l.strip() for l in rd(os.path.join(R3, 'data', 'zstar_ref16.in')).splitlines() if l.strip()]
sys.path.insert(0, FIN2)
try:
    import confirm as C
except Exception:
    C = None
def pred_of(pos):
    t = pos.split(); stm = t[-2]; pw = [x[1:] for x in t if x[0] == 'P' and x[1] == 'g']; pb = [x[1:] for x in t if x[0] == 'p' and x[1] == 'g']
    w, b = C.solve_d(6, [C.sq(x) for x in pw], [C.sq(x) for x in pb], 'over'); return w if stm == 'w' else b
ref_ok = ref_bad = 0
for l in ref16:
    p = l.split(' | ');
    if C is not None and pred_of(p[0].strip()) == p[1].strip(): ref_ok += 1
    else: ref_bad += 1
chess_z = L('chess_zstar_c1.out').strip()
chess_z_err = L('chess_zstar_c1.err').strip().splitlines()[-2:] if L('chess_zstar_c1.err') else []
open(os.path.join(R3, 'zstar_summary.json'), 'w').write(json.dumps({'rows': zrows, 'ref3_sample_positions': len(ref16), 'ref3_agree_with_over_prediction': ref_ok, 'ref3_other': ref_bad, 'chess_cap1': chess_z, 'chess_log': chess_z_err}, indent=1))
print('Z* rows', zrows, 'ref3', ref_ok, ref_bad, 'chess', chess_z.replace('\n', ' / '))
