import json,glob,os
from showjson import objs
out=[]
out.append("| run | board | files | pawns max (W+B) | root passers | roots | frozen | on | off | dud | over | under |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for fn in sorted(glob.glob('runs/np_*.json')+glob.glob('runs/flatnp_*.json')):
    for o in objs(fn):
        if o['variant'] not in ('strict','passer'): continue
        t=o['total']; d=o['distinct_groups']
        out.append(f"| {os.path.basename(fn)[:-5]} | {o['board']} | {o['files']} | {o['wmax']}+{o['bmax']} | {o['root_passers']} | {o['roots']} | {d['frozen']} | n/a | n/a | {d['dud']} | n/a | n/a |")
open('runs/tables_np.md','w').write("\n".join(out)+"\n"); print("\n".join(out))
out=[]
out.append("| run | board | files | pawns max (W+B) | root passers | roots (no check) | zero (frozen-like) | on-signature | off-signature | dud-signature | over-signature | under-signature | other |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for fn in sorted(glob.glob('runs/tp_*.json')):
    for o in objs(fn):
        t=o['total']
        out.append(f"| {os.path.basename(fn)[:-5]} | {o['board']} | {o['files']} | {o['wmax']}+{o['bmax']} | {o['root_passers']} | {o['roots']} | {t['zero']} | {t['on']} | {t['off']} | {t['dud']} | {t['over']} | {t['under']} | {t['other']} |")
open('runs/tables_tp.md','w').write("\n".join(out)+"\n"); print("\n".join(out))
