import sys,os,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import chk
from sweep import *
from ablate import *
# exhaustive parked (Ka1, black king top of a-file), ablations; plus Corollary 2.11b check on 8x6
for (W,H,mp,files) in [(6,6,3,[2,3,4]),(7,6,2,[2,3,4,5]),(8,6,2,[2,3,4,5,6])]:
    B=Bd(W,H)
    r=ablation(B,gen_exhaustive(B,files,mp,[((0,1),(0,H))],eps=True),'x',cap_per=6000)
    print('ABL_EXH %dx%d'%(W,H),json.dumps({k:(v[0],v[1],v[2]) for k,v in r.items()}),flush=True)
# Corollary 2.11b: cyl:8x6, Ka1 ka6, pawns on c-g: H2,H3 hold and no king on any pawn file, for either colour as beta, every pawn p
import ablate as AB
AB.mu_search=lambda *a: 99
B=Bd(8,6); n=0; bad=[]
for y in gen_exhaustive(B,[2,3,4,5,6],2,[((0,1),(0,6))],eps=True):
    if not legal(B,y): continue
    for beta in 'wb':
        for p in (y.wp if beta=='w' else y.bp):
            P=parts(B,y,beta,p); n+=1
            if not (P['h2'] and P['h3'] and P['path_king']): bad.append((y.text(B),beta,B.name(p)))
print('COR2.11b instances',n,'failures',len(bad),bad[:5],flush=True)
