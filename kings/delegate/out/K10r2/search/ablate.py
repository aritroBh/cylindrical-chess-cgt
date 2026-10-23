import sys,os,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from sweep import *

def parts(B,y,beta,p):
    om=other(beta); s=y.stm; f,r=p; rp=rho(B,beta,p)
    bps=y.wp if beta=='w' else y.bp
    ops=y.bp if beta=='w' else y.wp
    bkg=y.wk if beta=='w' else y.bk
    okg=y.bk if beta=='w' else y.wk
    P={}
    strip={f}|set(B.adjfiles(f))
    P['pass']=all(not(q[0] in strip and rho(B,beta,q)>rp) for q in ops)
    P['ep']=not(y.ep is not None and s==om and ep_victim(B,y)==p and any((g,r) in ops for g in B.adjfiles(f)))
    rng=range(r+1,B.H+1) if beta=='w' else range(r-1,0,-1)
    P['path_pawn']=all((f,rr) not in y.wp and (f,rr) not in y.bp for rr in rng)
    P['path_king']=all((f,rr)!=y.wk and (f,rr)!=y.bk for rr in rng)
    adj=B.adjfiles(f)
    P['h4']=all(not(q!=p and q[0] in adj and rho(B,beta,q)>rp+1) for q in bps)
    P['h4plus']=all(not(q!=p and q[0] in adj and rho(B,beta,q)>rp+2) for q in bps)
    badf=set(B.adjfiles(bkg[0]))
    P['h2']=not any(q[0] in badf for q in list(y.wp)+list(y.bp))
    allpf={q[0] for q in list(y.wp)+list(y.bp)}
    ok3=False
    for df in (-1,0,1):
        for dr in (-1,0,1):
            if df==0 and dr==0: continue
            g=B.nf(okg[0],df); rr=okg[1]+dr
            if g is None or not(1<=rr<=B.H): continue
            t=(g,rr)
            if B.kdist(t,bkg)<2: continue
            if ({g}|set(B.adjfiles(g)))&allpf: continue
            ok3=True
    P['h3']=ok3
    d=promo_dist(B,rp); e=d if s==om else d-1
    P['e']=e
    P['mu']=mu_search(B,y,beta,p,e+2)   # e+3 means > e+2
    P['h5']=P['mu']>=e+1
    P['h5weak']=P['mu']>=e   # one tempo slack
    return P

VARS={
 # name: (relaxed condition (must hold), strict condition (must fail))
 'drop_H1_ep':        (lambda P: P['pass'] and P['path_pawn'] and P['path_king'] and P['h2'] and P['h3'] and P['h4'] and P['h5'], lambda P: not P['ep']),
 'drop_H1_king_path': (lambda P: P['pass'] and P['ep'] and P['path_pawn'] and P['h2'] and P['h3'] and P['h4'] and P['h5'], lambda P: not P['path_king']),
 'drop_H2':           (lambda P: P['pass'] and P['ep'] and P['path_pawn'] and P['path_king'] and P['h3'] and P['h4'] and P['h5'], lambda P: not P['h2']),
 'drop_H3':           (lambda P: P['pass'] and P['ep'] and P['path_pawn'] and P['path_king'] and P['h2'] and P['h4'] and P['h5'], lambda P: not P['h3']),
 'drop_H4':           (lambda P: P['pass'] and P['ep'] and P['path_pawn'] and P['path_king'] and P['h2'] and P['h3'] and P['h5'], lambda P: not P['h4']),
 'H4_bound_rho+2':    (lambda P: P['pass'] and P['ep'] and P['path_pawn'] and P['path_king'] and P['h2'] and P['h3'] and P['h4plus'] and P['h5'], lambda P: not P['h4']),
 'H5_weakened_mu>=e': (lambda P: P['pass'] and P['ep'] and P['path_pawn'] and P['path_king'] and P['h2'] and P['h3'] and P['h4'] and P['h5weak'], lambda P: not P['h5']),
 'drop_H5':           (lambda P: P['pass'] and P['ep'] and P['path_pawn'] and P['path_king'] and P['h2'] and P['h3'] and P['h4'], lambda P: not P['h5']),
}

def ablation(B,gen,label,cap_per=4000):
    items={n:{} for n in VARS}
    cnt=collections.Counter()
    for y in gen:
        if not legal(B,y): continue
        txt=None
        for beta in 'wb':
            for p in (y.wp if beta=='w' else y.bp):
                P=parts(B,y,beta,p)
                for n,(rel,strict) in VARS.items():
                    if len(items[n])>=cap_per: continue
                    if rel(P) and strict(P):
                        if txt is None: txt=y.text(B)
                        items[n].setdefault(txt,[]).append(beta)
        if all(len(v)>=cap_per for v in items.values()): break
    res={}
    allt=set()
    for n in items: allt|=set(items[n])
    out,_=run_kp(B,sorted(allt))
    for n in VARS:
        tot=0; bad=0; ex=None
        for t,bl in items[n].items():
            r=out.get(t)
            if r is None or r[0]=='X': continue
            for b in bl:
                tot+=1
                win=(r[0]=='W') if b=='w' else (r[0]=='L')
                if not win:
                    bad+=1
                    if ex is None: ex=(t,b)
        res[n]=(tot,bad,ex)
    return res
