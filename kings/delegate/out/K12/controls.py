import json, os, sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames')
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K12')
from cylcgt import pawns as P
import checker as C
import process as PR

OUT='/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K12'
roots=json.load(open(OUT+'/roots.json'))
meta=json.load(open(OUT+'/meta.json'))
assert len(roots)==len(meta)

def beta_of(i):
    return meta[i]['beta']

# map frozen agree
def agree(m):
    if m['beta']=='W': return m['frozen_A']=='W'
    return m['frozen_A']=='L'

for drop_h4, weaken_h5, name in [(True,False,'dropH4'),(False,True,'weakenH5')]:
    viol=0; certcount=0; totaldis=0
    byboard={}
    for i,root in enumerate(roots):
        W=root['W']; H=root['H']; Wp=root['Wp']; Bp=root['Bp']; ep=root['ep']; stm=root['stm']
        beta=meta[i]['beta']
        cert = C.check_certified(W,H,Wp,Bp,ep,stm,beta, drop_h4=drop_h4, weaken_h5=weaken_h5)
        if cert: certcount+=1
        ag = agree(meta[i])
        if cert and not ag:
            viol+=1
        if (not cert) and (not ag):
            totaldis+=1
        key=(W,H)
        byboard.setdefault(key,[0,0,0,0])
        # [cert&agree, cert&disagree, uncert&agree, uncert&disagree]
        if cert and ag: byboard[key][0]+=1
        if cert and not ag: byboard[key][1]+=1
        if (not cert) and ag: byboard[key][2]+=1
        if (not cert) and not ag: byboard[key][3]+=1
    print(f"\n=== {name} ===")
    print('certified total',certcount,'violations certified&disagree',viol)
    for key in sorted(byboard):
        print(key, byboard[key])