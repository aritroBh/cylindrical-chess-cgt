import json,re,glob,sys
logs='/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31/logs/'
K={}
for f in ['sweep_main','sweep_ext','sweep_h4','sweep_small','sweep_wide']:
    for l in open(logs+f+'.jsonl'):
        r=json.loads(l); K[(r['W'],r['H'],r['rank'])]=(r['lk_p1'],r['lk_m1'],r['roots'])
M={}
for f in sys.argv[1:]:
    for l in open(f):
        m=re.match(r'cyl:(\d+)x(\d+) a(\d+) roots (\d+) races (\d+)\s+\+1 (\d+)\s+-1 (\d+)\s+notW/2file (\d+) oddrankdiff (\d+)',l)
        if not m: continue
        W,H,r,roots,races,p,mm,fb,pb=map(int,m.groups())
        M[(W,H,r)]=(p,mm,roots,races,fb,pb)
common=[k for k in M if k in K]
diff=[k for k in common if K[k]!=M[k][:3]]
print('mine',len(M),'in K31 logs',len(common),'differences',len(diff),diff[:5])
print('races nonzero',sum(1 for v in M.values() if v[3]),'file-bad',sum(v[4] for v in M.values()),'oddrank',sum(v[5] for v in M.values()))
viol=[]
for (W,H,r),v in M.items():
    exp=(W%2==0 and W>=6)
    if exp and not(v[0]>0 and v[1]>0): viol.append((W,H,r,v[:2]))
    if not exp and (v[0] or v[1]): viol.append((W,H,r,v[:2]))
print('rule violations',viol[:10],len(viol))
print('new (not in K31 logs):',sorted({(W,H) for (W,H,r) in M if (W,H,r) not in K})[:60])
print('total pm1 roots (mine)',sum(v[0]+v[1] for v in M.values()))
