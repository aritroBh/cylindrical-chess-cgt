import json
rs=[json.loads(l) for l in open('/Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms/mechanisms_34.jsonl')]
out=["| # | component P (7x6 cylinder) | mover | convention | exact frozen | decisive node N* the convention declares won | n_X | d_Y | Y's winning line | real = frozen at this side? | real = frozen at both sides? |","|---|---|---|---|---|---|---|---|---|---|---|"]
i=0
for x in rs:
    for s in x['sides']:
        i+=1
        cw = 'White wins' if s['convention_winner']=='W' else 'Black wins'
        fw = 'White wins' if s['frozen_winner']=='L' and False else None
        yw = 'Black wins' if s['frozen_winner']=='L' else 'White wins'
        out.append(f"| {i} | {x['P']} | {s['mover_at_root']} | {cw} | {yw} | {s['Nstar']} ({s['mover']} to move) | {min(s['X_passer_dist'].values())} | {min(s['Y_pawn_dist'].values())} | {' '.join(s['pv'])} | {'yes' if x['real'][('wtm' if s['mover_at_root']=='W' else 'btm')][0]==x['frozen'][('wtm' if s['mover_at_root']=='W' else 'btm')][0] else 'NO'} | {'yes' if x['real_matches_frozen'] else 'NO'} |")
open('/Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms/tables_34.md','w').write("\n".join(out)+"\n")
print("\n".join(out[:6]))
