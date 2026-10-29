import json
ids=json.load(open('data/suite_pilot_ids.json')); res={x['id']:x for x in json.load(open('/Users/aritro/Downloads/Research/Chessendgames/engine/suite/results.json'))}
lines=[l for l in open('logs/suite_pilot.txt') if not l.startswith('[')]
tot=ok=0; rootok=0; unres=0; mism=[]
for i,l in zip(ids,lines):
    a=l.rstrip('\n').split(' | '); r=a[1].split(); x=res[i]; stm=x['stm']
    def mv(v): return 'draw' if v=='D' else ('win' if (v=='W')==(stm=='W') else 'loss')
    A=dict(t.split(':') for t in a[2][3:].split()) if a[2].startswith('A:') else None
    if A is not None:
        B=dict(t.split(':') for t in a[3][3:].split())
    else:
        A=B=dict(t.split(':') for t in a[2].split())
    # root
    root_tb=x['tb_root']
    if r[0]==r[1]:
        rootok+= (mv(r[0])==root_tb)
        if mv(r[0])!=root_tb: mism.append((i,'root',mv(r[0]),root_tb))
    else: unres+=1
    for m,v in A.items():
        uci=m[1:5] if m[0] in 'KP' else m
        tb=x['tb_moves'].get(uci)
        if tb is None: continue
        if A[m]==B[m]:
            tot+=1; good=(mv(A[m])==tb); ok+=good
            if not good: mism.append((i,m,mv(A[m]),tb))
print('positions',len(lines),'root resolved',len(lines)-unres,'root agree',rootok)
print('moves resolved',tot,'agree with tablebase',ok); print(mism)
