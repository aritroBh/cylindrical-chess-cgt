"""K40 step 2: the bare P result of every legal K+P vs K position on cyl:WxH, three ways, plus the atlas table.

kpsum (zero test game) vs kp_p --pmodel vs ref3m (P is its default model) vs the atlas KPK code
(atlas/cylinder/kpk for 8 ranks; for 6 ranks the same code recompiled with RANKS=6, scripts/kpk_ranks.c).
Usage: python compare_base.py W H   -> writes data/base_cyl_WxH.tsv.xz and prints a summary line (JSON).
"""
import json, lzma, subprocess, sys, os

D = os.path.dirname(os.path.abspath(__file__)) + '/..'
W, H = int(sys.argv[1]), int(sys.argv[2])
board = f'cyl:{W}x{H}'


def run(cmd, inp):
    r = subprocess.run(cmd, input=inp, capture_output=True, text=True, check=True)
    return r.stdout


ks = run([f'{D}/bin/kpsum', str(W), str(H), '1', 'zero'], '')
pos = []  # (wk, bk, p, s, res)
for ln in ks.splitlines():
    if ln.startswith('#'):
        continue
    a, b = ln.split('|')
    wk, bk, p, s = a.split()
    pos.append((wk, bk, p, s, b.split()[0]))

lines = ''.join(f'K{wk} P{p} k{bk} {s} -\n' for wk, bk, p, s, _ in pos)
kp = run([f'{D}/bin/kp_p', '--board', board, '--pmodel', '--cap', '1'], lines).splitlines()
rf = run([f'{D}/bin/ref3m', '--board', board], lines).splitlines()
kp = [l for l in kp if '|' in l]
rf = [l for l in rf if '|' in l]
assert len(kp) == len(pos) == len(rf), (len(kp), len(pos), len(rf))
atl_bin = os.path.abspath(f'{D}/../../../../atlas/cylinder/kpk') if H == 8 else f'{D}/bin/kpk{H}'
aq = ''.join(f'{wk} {bk} {p} {s.upper()}\n' for wk, bk, p, s, _ in pos)
at = run([atl_bin, str(W), '1', '0'], aq).splitlines()
assert len(at) == len(pos)

out = []
cnt = {'n': len(pos), 'kp_diff': 0, 'ref_diff': 0, 'kp_inexact': 0, 'atlas_illegal': 0,
       'atlas_diff': 0, 'atlas_diff_by': {}}
for (wk, bk, p, s, r0), k, f, a in zip(pos, kp, rf, at):
    kr = k.split('|')[1].split()
    if kr[0] != kr[1]:
        cnt['kp_inexact'] += 1
    rk = kr[0]
    rr = f.split('|')[1].strip()
    ra = a.split()[-1]
    if rk != r0:
        cnt['kp_diff'] += 1
    if rr != r0:
        cnt['ref_diff'] += 1
    if ra == 'ILLEGAL':
        cnt['atlas_illegal'] += 1
    elif ra != r0:
        cnt['atlas_diff'] += 1
        key = f'P={r0} atlas={ra} {s}'
        cnt['atlas_diff_by'][key] = cnt['atlas_diff_by'].get(key, 0) + 1
    out.append(f'{wk}\t{bk}\t{p}\t{s}\t{r0}\t{rk}\t{rr}\t{ra}\n')
with lzma.open(f'{D}/data/base_cyl_{W}x{H}.tsv.xz', 'wt') as fh:
    fh.write('wk\tbk\tp\tstm\tkpsum\tkp_p\tref3m\tatlas\n')
    fh.writelines(out)
for s in 'wb':
    cnt['P_win_' + s] = sum(1 for x in pos if x[3] == s and x[4] == 'W')
    cnt['n_' + s] = sum(1 for x in pos if x[3] == s)
print(json.dumps({'board': board, **cnt}))
