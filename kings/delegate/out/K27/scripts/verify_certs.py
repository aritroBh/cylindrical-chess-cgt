"""verify_certs.py -- cross-check every position and every reply cited in the certificates against the two independent
solvers (kpp --pmodel --moves  and  ref3m --moves).
usage: verify_certs.py children.txt KPP REF3M
For each certificate node: (i) the opponent's position q after the winner's move: the set of legal replies must equal the
reply list of the certificate and every reply must lead to a position won by the winner (value from White's point of view);
(ii) every leaf where the winner promotes: a promotion move exists and is valued as a win for the winner."""
import sys, subprocess, re, importlib
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm, greedy

def norm(lab):
    if '=' in lab: return 'promo'
    l=lab.replace('-','').replace('x','').replace('ep','')
    if l[0] not in 'K': l='P'+l
    return l

lines=[l.split('#') for l in open(sys.argv[1])]
KPP,REF=sys.argv[2],sys.argv[3]
qs={}      # q position string -> (winner, expected move-set)
leafs={}   # x position string -> winner
for ln in lines:
    p=pm.parse(ln[0].strip())
    importlib.reload(greedy)
    greedy.add(p)
    S=greedy.S
    for x,(lab,q,reps) in S.items():
        win='L' if x[5]==1 else 'W'    # White-POV letter of the winner's win
        if q=='PROMO':
            leafs[pm.show(x)]=win; continue
        qs[pm.show(q)]=(win,sorted(norm(l) for l,_ in pm.moves(q)))
def run(cmd,inp):
    return subprocess.run(cmd,input=inp,capture_output=True,text=True).stdout.splitlines()
allpos=sorted(set(qs)|set(leafs))
inp='\n'.join(allpos)+'\n'
kpp=run([KPP,'--board','flat:7x6','--ep','on','--promote','QRBN','--cap','1','--pmodel','--moves'],inp)
ref=run([REF,'--board','flat7x6','--moves'],inp)
def parse_kpp(l):
    h,rest=l.split(' | ',1)
    t=rest.split()
    A,B=t[0],t[1]
    mv={}
    for tok in t[2:]:
        if tok=='|': continue
        m,v=tok.rsplit(':',1)
        mv.setdefault('promo' if '=' in m else m,set()).add(v)
    return h.strip(),A,B,mv
def parse_ref(l):
    h,rest=l.split(' | ',1)
    t=rest.split()
    mv={}
    for tok in t[1:]:
        m,v=tok.rsplit(':',1)
        mv.setdefault(m,set()).add(v)
    return h.strip(),t[0],mv
K={}; R={}
for l in kpp:
    if ' | ' in l and not l.startswith('['):
        h,A,B,mv=parse_kpp(l); K[h]=(A,B,mv)
for l in ref:
    if ' | ' in l:
        h,v,mv=parse_ref(l); R[h]=(v,mv)
bad=0; nq=0; nm=0; nl=0
for pos,(win,exp) in qs.items():
    nq+=1
    A,B,mv=K[pos]
    v,mr=R[pos]
    if not(A==B==win and v==win): print('VALUE MISMATCH',pos,win,A,B,v); bad+=1
    for name,(mm,tag) in (('kpp',(mv,None)),('ref3m',(mr,None))):
        if sorted(mm.keys())!=sorted(set(exp)):
            print('MOVESET MISMATCH',name,pos,sorted(mm.keys()),exp); bad+=1
        for m,vals in mm.items():
            nm+=1
            if vals!={win}:
                print('REPLY VALUE',name,pos,m,vals,win); bad+=1
for pos,win in leafs.items():
    nl+=1
    A,B,mv=K[pos]; v,mr=R[pos]
    if not(A==B==win and v==win): print('LEAF VALUE MISMATCH',pos,win,A,B,v); bad+=1
    if 'promo' not in mv or mv['promo']!={win} or 'promo' not in mr or mr['promo']!={win}:
        print('LEAF PROMO',pos,win,mv.get('promo'),mr.get('promo')); bad+=1
print('checked opponent-to-move positions: %d (reply values checked: %d, two solvers); leaf positions: %d; problems: %d'%(nq,nm,nl,bad))
