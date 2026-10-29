# Analyse the cyl:6x6 sample: chess (kpsolve cap 1, Q) against the frozen model (--frozen), one- and two-feature rules.
import json,glob,os,collections,re,sys
from fit import *
FILES='abcdef'
TAG0=sys.argv[1] if len(sys.argv)>1 else 's6'
meta=json.load(open('data/s6x6_meta.json' if TAG0=='s6' else 'data/sB_meta.json'))
def sqf(s): return (FILES.index(s[0]),int(s[1]))
def cd(a,b):  # cylinder Chebyshev distance
    df=abs(a[0]-b[0]); df=min(df,6-df); return max(df,abs(a[1]-b[1]))
def load(prefix,files=None):
    d={}
    for f in (files if files is not None else sorted(glob.glob(f'logs/b6_{prefix}_b_??.txt' if TAG0=='s6' else f'logs/bB_{prefix}_b_??.txt'))):
        for l in open(f):
            if l.startswith('['): continue
            a=l.rstrip('\n').split(' | ')
            pos=a[0]; r=a[1].split(); mv={}
            rest=a[2:]
            if rest and rest[0].startswith('A:'):
                A=dict(t.split(':') for t in rest[0][3:].split()); B=dict(t.split(':') for t in rest[1][3:].split())
                for m in A: mv[m]=(A[m],B[m])
            elif rest:
                for t in rest[0].split():
                    m,v=t.split(':'); mv[m]=(v,v)
            d[pos]=((r[0],r[1]),mv)
    return d
ch=load('chess'); fr=load('frozen')
CAP2=set()
c2=load('c2',sorted(glob.glob('logs/c2_u6_??.txt' if TAG0=='s6' else 'logs/c2_uB_??.txt')))
for p,v in c2.items():
    if v[0][0]==v[0][1] and ch.get(p) and ch[p][0][0]!=ch[p][0][1]:
        ch[p]=v; CAP2.add(p)
def flip(l):
    t=l.split(); t[-2]='b' if t[-2]=='w' else 'w'; return ' '.join(t)
FLIP={}
if TAG0=='s6':
    for l in open('logs/s6_flip_frozen.txt'):
        if l.startswith('['): continue
        a=l.rstrip('\n').split(' | '); FLIP[a[0]]=a[1].split()[0]
else:
    for l in open('logs/sB_flip_frozen.txt'):
        if l.startswith('['): continue
        a=l.rstrip('\n').split(' | '); FLIP[a[0]]=a[1].split()[0]
rows=[]; mrows=[]
def mover_res(v,stm):  # White-POV letter -> mover result
    if v=='D': return 'draw'
    return 'win' if (v=='W')==(stm=='w') else 'loss'
for m in meta:
    pos=m['pos']
    if pos not in ch or pos not in fr: continue
    (ca,cb),cmv=ch[pos]; (fa,fb),fmv=fr[pos]
    assert fa==fb
    stm=m['stm']
    resolved=(ca==cb)
    W=[sqf(x) for x in m['W']]; B=[sqf(x) for x in m['B']]
    r=m['r']; mir=m['mir']
    toks=pos.split()
    wk=sqf([t for t in toks if t[0]=='K'][0][1:]); bk=sqf([t for t in toks if t[0]=='k'][0][1:])
    ctx=W+B
    own=W if stm=='w' else B; opp=B if stm=='w' else W
    mk,ok=(wk,bk) if stm=='w' else (bk,wk)
    def reserve(P,color):
        t=0
        occ=set(W)|set(B)|{(1,r),(1,r+1)}
        for (f,rk) in P:
            s=1 if color=='w' else -1; x=rk
            while True:
                nx=x+s
                if nx<2 or nx>5 or (f,nx) in occ: break
                t+=1; x=nx
        return t
    resW=reserve(W,'w'); resB=reserve(B,'b')
    buf=[x for x in ctx if x[0] in (3,5)]
    faces=[(w[0],b[1]-w[1]) for w in W for b in B if w[0]==b[0] and b[1]>w[1]]
    fp=[x for w in W for b in B if w[0]==b[0] and b[1]>w[1] for x in (w,b)]
    row=dict(fa=min([w[1] for w in W if any(w[0]==b[0] and b[1]>w[1] for b in B)],default=0),fb=max([b[1] for b in B if any(w[0]==b[0] and b[1]>w[1] for w in W)],default=0),
        gapodd=int(min([g for _,g in faces],default=0)%2==1),dkm_face=min([cd(mk if False else (wk if stm=='w' else bk),x) for x in fp],default=9),dko_face=min([cd((bk if stm=='w' else wk),x) for x in fp],default=9),
        nface=len(faces),mingap=min([g for _,g in faces],default=9),nface_buf=sum(1 for f_,g in faces if f_ in (3,5)),nface_e=sum(1 for f_,g in faces if f_==4),
        npass=len(W)+len(B)-2*len(faces),pos=pos,stm=stm,r=r,mir=int(mir),nW=len(W),nB=len(B),n=len(ctx),nbuf=len(buf),
        dk_ctx_min=min(cd(wk,c) for c in ctx),dkmover_ctx=min(cd(mk,c) for c in ctx),dkopp_ctx=min(cd(ok,c) for c in ctx),
        dkmover_buf=min([cd(mk,c) for c in buf],default=9),dkopp_buf=min([cd(ok,c) for c in buf],default=9),
        resW=resW,resB=resB,res_mover=resW if stm=='w' else resB,res_opp=resB if stm=='w' else resW,res_diff=(resW-resB)*(1 if stm=='w' else -1),
        res_tot=resW+resB,frozen=mover_res(fa,stm),chess=mover_res(ca,stm) if resolved else None,resolved=int(resolved),cap2=int(pos in CAP2))
    nv=FLIP.get(flip(pos)); row['null_win']=int(nv is not None and mover_res(nv,stm)=='win'); row['null_loss']=int(nv is not None and mover_res(nv,stm)=='loss')
    row['zero_holds']=int(resolved and ca==fa) if resolved else None
    rows.append(row)
    if stm:
        for mv,(a,b) in cmv.items():
            if mv[0]!='K' or a!=b: continue
            to=sqf(mv[3:5])
            mm=dict(row); mm.update(move=mv,res=mover_res(a,stm),dest_ctx=min(cd(to,c) for c in ctx),
              dest_opp_pawn=min([cd(to,c) for c in opp],default=9),dest_own_pawn=min([cd(to,c) for c in own],default=9),
              dest_file=to[0],dest_buf=int(to[0] in (3,5)),fzn_root=row['frozen'])
            mrows.append(mm)
TAG=sys.argv[1] if len(sys.argv)>1 else 's6'
json.dump(dict(rows=rows,mrows=mrows),open(f'data/{TAG}_table.json','w'))
n=len(rows); res=[r for r in rows if r['resolved']]
print('cap-2 resolved extra:',sum(r['cap2'] for r in rows))
print('positions',n,'chess-resolved',len(res),'unresolved',n-len(res))
print('frozen root (mover POV):',collections.Counter(r['frozen'] for r in res))
print('chess root (mover POV):',collections.Counter(r['chess'] for r in res))
print('zero holds (chess root == frozen root):',sum(r['zero_holds'] for r in res),'/',len(res))
print('king moves (resolved)',len(mrows),collections.Counter(m['res'] for m in mrows))
