import json,glob,os
from showjson import objs
rows=[]
def label(fn,o):
    b=os.path.basename(fn).replace('.json','')
    return b
files=sorted(glob.glob('runs/cen_*.json'))+sorted(glob.glob('runs/ex_*.json'))
out=[]
out.append("| run | board | files | pawns (white,black max) | root passer | leak | roots | frozen | on | off | dud | over | under | near-over/under roots |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for fn in files:
    try: os_=objs(fn)
    except Exception as e: continue
    for o in os_:
        t=o["total"]; d=o["distinct_groups"]
        out.append(f"| {label(fn,o)}:{o['variant']} | {o['board']} | {o['files']} | {o['wmax']}+{o['bmax']} | {o['root_passers']} | {'ignored' if o['ignore_leak'] else 'strict'} | {o['roots']} | {t['frozen']} | {t['on']} | {t['off']} | {t['dud']} | {t['over']} | {t['under']} | {o['near_over_roots']}/{o['near_under_roots']} |")
open('runs/tables_main.md','w').write("\n".join(out)+"\n")
print("\n".join(out))
