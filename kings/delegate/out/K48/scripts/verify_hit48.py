"""K48 copy of K45 verify_hit.py with a board-kind argument (cyl or flat).  K45: check Definition 4.8 for a hit using only the values of an independent P solver (ref3m or kp_p --pmodel, both with --moves).
This script has its own tiny move applier and no move generator: the legal moves and their values come from the solver.
usage: verify_hit48.py <solver: ref3m|kpp> <cyl|flat> <W> <sh 0|1> "<position of root with shuttler on z0, as in hit line, e.g. 'Kf5 kd4 Pb2 ... b -'>" <z1 square>"""
import subprocess,sys,re
HEAVY='../../heavy.sh'
KIND='cyl'
import os
H=int(os.environ.get('K48_H','6'))   # board height (default 6)
def run(solver,W,positions):
    if solver=='ref3m': cmd=[HEAVY,'./bin/ref3m','--board',('cyl:%dx%d' if KIND=='cyl' else 'pln:%dx%d')%(W,H),'--moves']
    else: cmd=[HEAVY,'./bin/kp_p10','--board',('cyl:%dx%d' if KIND=='cyl' else 'flat:%dx%d')%(W,H),'--pmodel','--cap','1','--threads','1','--moves']
    r=subprocess.run(cmd,input="\n".join(positions)+"\n",capture_output=True,text=True)
    out={}
    for line in r.stdout.splitlines():
        if ' | ' not in line: continue
        pos,rest=line.split(' | ',1)
        toks=rest.split()
        if solver=='ref3m': res=toks[0]; mv=toks[1:]
        else:
            res=toks[0]+toks[1]; mv=toks[3:] if toks[2]=='|' else toks[2:]
        out[pos]=(res,mv)
    return out
def parse(pos):
    t=pos.split(); pcs={}
    for x in t[:-2]: pcs[x[1:]]=x[0]
    return pcs,t[-2],t[-1]
def fmt(pcs,stm,ep):
    order=lambda x:(('KQRBNPkqrbnp'.index(x[1])),x[0])
    items=sorted(((sq,p) for sq,p in pcs.items()),key=lambda sp:('KkPp'.index(sp[1]) if sp[1] in 'KkPp' else 9,sp[0]))
    return " ".join(p+sq for sq,p in items)+" "+stm+" "+ep
def sqfr(sq,W): return ord(sq[0])-97,int(sq[1:])-1
def apply(pos,mv,W):
    pcs,stm,ep=parse(pos)
    m=re.match(r'([KPQRBNkpqrbn])([a-z]\d+?)([a-z]\d+)([QRBNqrbn]?)$',mv)
    # squares have 1-digit ranks (H<=8)
    m=re.match(r'([A-Za-z])([a-l][1-9])([a-l][1-9])([QRBNqrbn]?)$',mv)
    pt,fr,to,pro=m.groups()
    col='w' if stm=='w' else 'b'
    me=pt.upper() if col=='w' else pt.lower()
    if pro: return None
    cap=pcs.pop(to,None)
    ff,fr_=sqfr(fr,W); tf,tr=sqfr(to,W)
    newep='-'
    if pt.upper()=='P':
        if tf!=ff and cap is None:     # e.p. capture
            pcs.pop(to[0]+str(fr_+1),None)
        if abs(tr-fr_)==2: newep=fr[0]+str((fr_+tr)//2+1)
    del pcs[fr]; pcs[to]=me
    return fmt(pcs,'b' if stm=='w' else 'w',newep)
def lose_at_once(res,stm):    # res: W/D/L from White's view after the move; the move loses at once for the mover
    return res=='L' if stm=='w' else res=='W'
def attacked_by_pawn(sq,pcs,col,W):   # square attacked by a pawn of colour col ('w' or 'b')
    f,r=sqfr(sq,W)
    for sq2,p in pcs.items():
        if p==('P' if col=='w' else 'p'):
            f2,r2=sqfr(sq2,W)
            if r2+(1 if col=='w' else -1)==r and (min((f-f2)%W,(f2-f)%W)==1 if KIND=='cyl' else abs(f-f2)==1): return True
    return False
def kdist(a,b,W):
    fa,ra=sqfr(a,W); fb,rb=sqfr(b,W); df=abs(fa-fb); df=min(df,W-df) if KIND=='cyl' else df; return max(df,abs(ra-rb))
def main():
    global KIND
    solver,KIND,W,sh,root,z1=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),sys.argv[5],sys.argv[6]
    pcs,stm,ep=parse(root); K=[s for s,p in pcs.items() if p=='K'][0]; k=[s for s,p in pcs.items() if p=='k'][0]
    z0=k if sh else K; t=K if sh else k
    zs=[z0,z1]; fr_stm='w' if sh else 'b'; sh_stm='b' if sh else 'w'
    ok=True; log=[]
    # K1, K2
    for z in zs:
        c1=not attacked_by_pawn(z,pcs,'w' if sh else 'b',W); c2=kdist(z,t,W)>=2
        if not (c1 and c2): ok=False; log.append('K1/K2 fails at %s'%z)
    if attacked_by_pawn(t,pcs,'b' if sh else 'w',W): ok=False; log.append('K1 fails for the freezer king')
    base={}
    def pos_with(zq,stm_,ep_='-'):
        q=dict(pcs); 
        for s in list(q):
            if q[s] in ('K','k') and ((q[s]=='k')==bool(sh)): del q[s]
        q[zq]='k' if sh else 'K'
        return fmt(q,stm_,ep_)
    roots=[(aa,s) for aa in (0,1) for s in (sh_stm,fr_stm)]
    plist=[pos_with(zs[aa],s) for aa,s in roots]
    res=run(solver,W,plist)
    freezes=[]
    for (aa,s),p in zip(roots,plist):
        r,mv=res[p]
        if r[0]=='X': ok=False; log.append('root illegal '+p); continue
        moves=[]
        for x in mv:
            name,val=x.rsplit(':',1); moves.append((name,val))
        if s==sh_stm:
            shuttle=[n for n,v in moves if n[0] in 'Kk' and n[3:5]==zs[1-aa] ]
            if len(shuttle)!=1: ok=False; log.append('U1: shuttle not legal exactly once at '+p)
            for n,v in moves:
                if n in shuttle: continue
                if len(n)>5 or not lose_at_once(v,s): ok=False; log.append('U1 fails at %s by %s:%s'%(p,n,v))
        else:
            fz=[(n,v) for n,v in moves if not lose_at_once(v,s)]
            if any(len(n)>5 for n,v in moves): ok=False; log.append('U2: a promotion is available at '+p)
            if not fz: ok=False; log.append('U2: no freeze at '+p)
            for n,v in fz:
                q=apply(p,n,W)
                if q is None: continue
                freezes.append((p,n,q))
    # q positions
    qs=[]
    for p,n,q in freezes:
        pc,st,epq=parse(q)
        qs.append(q); qs.append(fmt(pc,'w' if st=='b' else 'b','-'))
    if qs:
        res2=run(solver,W,sorted(set(qs)))
        for p,n,q in freezes:
            pc,st,epq=parse(q); qf=fmt(pc,'w' if st=='b' else 'b','-')
            r,mv=res2[q]
            moves=[x.rsplit(':',1) for x in mv]
            if r[0]=='X' or not moves or not all(lose_at_once(v,sh_stm) and len(nm)<=5 for nm,v in moves): ok=False; log.append('U3 fails: freeze %s from %s gives %s'%(n,p,q))
            r4,mv4=res2[qf]
            m4=[x.rsplit(':',1) for x in mv4]
            if r4[0]=='X' or not m4 or not all(lose_at_once(v,fr_stm) and len(nm)<=5 for nm,v in m4): ok=False; log.append('U4 fails: freeze %s from %s gives %s (freezer to move: %s, %d moves)'%(n,p,qf,r4,len(m4)))
    print(('PASS' if ok else 'FAIL'),solver,KIND,'W=%d'%W,'sh=%d'%sh,root,'shuttle',z0+z1,'freezes:',[(n) for p,n,q in freezes]); 
    for l in log: print('   ',l)
main()
