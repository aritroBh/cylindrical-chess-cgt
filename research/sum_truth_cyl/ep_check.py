"""Regenerate K12's e.p. roots (gen.process_board, ep not None), certify with K12 checker.py and K10r2 chk.py, compare with kpsolve --frozen.
Usage: ep_check.py W H K"""
import sys, os, json, collections, subprocess
sys.dont_write_bytecode=True
R='/Users/aritro/Downloads/Research/Chessendgames'
sys.path[:0]=[R, R+'/kings/delegate/out/K12', R+'/kings/delegate/out/K10r2/search']
from cylcgt import pawns as P
import gen, checker as C, chk
W,H,K=map(int,sys.argv[1:4])
uniq,board=gen.process_board(W,H,K)
roots=[r for r in uniq if r[4] is not None]
print('ep roots',len(roots),'of',len(uniq),flush=True)
FN='abcdefghij'; B=chk.Bd(W,H,True)
rows=[]
for (_,_,Wp,Bp,ep,stm) in roots:
    pos=C.make_pos(Wp,Bp,ep,W,H)
    wp=bool(C.passed_pawns_list(board,pos,'W',W,H)); bp=bool(C.passed_pawns_list(board,pos,'B',W,H))
    cw,cb=P.passed(board,pos,'W'),P.passed(board,pos,'B')
    assert (wp,bp)==(cw,cb)
    if wp and bp:
        other='B' if stm=='W' else 'W'
        beta=stm if P.promote_distance(board,pos,stm)<=P.promote_distance(board,pos,other) else other; kind='race'
    else: beta='W' if wp else 'B'; kind='single'
    c1=C.check_certified(W,H,Wp,Bp,ep,stm,beta)
    y=chk.Pos((0,1),(0,H),set(map(tuple,Wp)),set(map(tuple,Bp)),stm.lower(),tuple(ep[0]))
    bl=beta.lower()
    c2=any(chk.certified(chk.hyps(B,y,bl,p)) for p in (y.wp if bl=='w' else y.bp))
    rows.append((y.text(B),kind,beta,bool(c1),bool(c2)))
lines=[r[0] for r in rows]
res={}
for i in range(0,len(lines),20000):
    pr=subprocess.run(['nice','-n','15',R+'/kings/kpsolve','--board',f'cyl:{W}x{H}','--frozen','--cap','1','--threads','2','--ep','on'],input='\n'.join(lines[i:i+20000])+'\n',capture_output=True,text=True)
    for ln in pr.stdout.splitlines():
        if ' | ' in ln:
            a,b=ln.rsplit(' | ',1); res[a]=b.split()
Cn=collections.Counter(); ex=collections.defaultdict(list)
for t,kind,beta,c1,c2 in rows:
    a,b=res[t]; want='W' if beta=='W' else 'L'
    k=(kind,'cert12' if c1 else 'unc12','cert10' if c2 else 'unc10','agree' if a==b==want else 'disagree')
    Cn[k]+=1
    if len(ex[k])<3: ex[k].append(t+' -> '+a+b)
out={'board':f'{W}x{H}','K':K,'ep_roots':len(rows),'classes':{'/'.join(k):v for k,v in sorted(Cn.items())},'examples':{'/'.join(k):v for k,v in ex.items()}}
json.dump(out,open(f'ep_{W}x{H}.json','w'),indent=1); print(json.dumps(out,indent=1))
