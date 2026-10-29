# Differential walk for one refuted P4 row. Builds the AND-OR graph of P-model winning play (kings move,
# promotion to Q = immediate win), evaluates every promotion leaf in real chess (kpsolve, cap 2, Q) and propagates
# by least fixed point under several leaf rules.  usage: walker.py "<root position>" <board> <out.json>
import subprocess,sys,json,collections
BOARD=sys.argv[2] if len(sys.argv)>2 else 'cyl:7x6'
def kp(lines,args):
    r=subprocess.run(['src/kpw','--board',BOARD,'--moves','--kids']+args,input='\n'.join(lines)+'\n',capture_output=True,text=True)
    out={}
    for l in r.stdout.splitlines():
        if l.startswith('['): continue
        a=l.split(' | ')
        pos=a[0]; res=a[1].split(); mv=[]
        for tok in (a[2].split() if len(a)>2 else []):
            m,rest=tok.split(':',1); v,p=rest.split('@',1)
            term=p.startswith('TERM:'); p=p[5:] if term else p
            mv.append((m,v,p.replace('_',' '),term))
        out[pos]=(res[0],mv)
    return out
root=sys.argv[1]
r0=kp([root],['--pmodel','--promote','Q'])[root]
assert r0[0] in 'WL',r0[0]
Sw='W' if r0[0]=='W' else 'L'   # White-POV value of a node in which the P-winner wins
nodes={}; frontier=[root]
while frontier:
    res=kp(frontier,['--pmodel','--promote','Q'])
    nxt=[]
    for p in frontier: nodes[p]=res[p]
    for p in frontier:
        for (m,cv,cp,term) in nodes[p][1]:
            if term or cv!=Sw: continue
            if cp not in nodes and cp not in nxt: nxt.append(cp)
    frontier=nxt
leaves=sorted({cp for n in nodes.values() for (m,cv,cp,term) in n[1] if term and cv==Sw})
print(f"root {root}: P-winner={'White' if Sw=='W' else 'Black'}; graph nodes {len(nodes)}; promotion leaves {len(leaves)}",flush=True)
chess={}; lmoves={}
if leaves:
    res=kp(leaves,['--cap','2','--promote','Q'])
    for l in leaves:
        chess[l]=res[l][0]; lmoves[l]=res[l][1]

def stm(p): return p.split()[-2]
def attrs(l):
    toks=l.split(); off=[t for t in toks if t[0] in 'QRBNqrbn' and len(t)==3]
    sq=off[0][1:]
    mv=lmoves[l]
    safe=not any(m[0]!='P' and m[-2:]==sq for (m,cv,cp,term) in mv)
    counter=any('=' in m for (m,cv,cp,term) in mv)
    return dict(sq=sq,safe=safe,counter=counter)
A={l:attrs(l) for l in leaves}
def fix(pred):
    cw={p:False for p in nodes}; ch=True
    while ch:
        ch=False
        for p,(v,mv) in nodes.items():
            if cw[p]: continue
            Smove=(stm(p)=='w')==(Sw=='W')
            def kw(k):
                m,cv,cp,term=k
                return pred(cp) if term else cw.get(cp,False)
            ok=any(kw(k) for k in mv if k[1]==Sw) if Smove else (all(kw(k) for k in mv) if mv else False)
            if ok: cw[p]=True; ch=True
    return cw
variants={'P (every promotion wins)':lambda l:True,
 'chess (true leaf value)':lambda l:chess[l]==Sw,
 'safe only (queen not capturable at once)':lambda l:A[l]['safe'],
 'no-counter only (opp cannot promote at once)':lambda l:not A[l]['counter'],
 'safe and no-counter':lambda l:A[l]['safe'] and not A[l]['counter']}
cws={k:fix(f) for k,f in variants.items()}
chess_cw=cws['chess (true leaf value)']
print('rule variant: root wins? ; graph nodes agreeing with chess fixpoint')
summ={}
for k,cw in cws.items():
    agree=sum(cw[p]==chess_cw[p] for p in nodes)
    print(f'  {k}: root_win={cw[root]}; agree with chess on {agree}/{len(nodes)} nodes'); summ[k]=dict(root_win=cw[root],agree=agree)
cnt=collections.Counter()
for l in leaves:
    cnt[(chess[l]==Sw, A[l]['safe'], A[l]['counter'])]+=1
print('leaf table (chess_win, safe, counter): count'); 
for k,v in sorted(cnt.items()): print('  ',k,v)
# shallowest non-win leaves
depth={root:0}; fr=[root]
while fr:
    nx=[]
    for p in fr:
        for (m,cv,cp,term) in nodes[p][1]:
            if term or cv!=Sw or cp in depth: continue
            depth[cp]=depth[p]+1; nx.append(cp)
    fr=nx
ex=[]
for p in nodes:
    for (m,cv,cp,term) in nodes[p][1]:
        if term and cv==Sw and chess[cp]!=Sw: ex.append((depth[p]+1,p,m,cp,chess[cp],A[cp]))
ex.sort(key=lambda t:(t[0],t[1],t[2]))
print('shallowest promotions that win in P but not in chess (plies from root, parent, move, leaf, chess value White-POV, attrs):')
for e in ex[:15]: print('  ',e)
other=[(l,chess[l],A[l]) for l in leaves if chess[l]!=Sw and A[l]['safe'] and not A[l]['counter']]
print('chess-non-win leaves that are safe and have no counter-promotion:',len(other))
for o in other[:25]: print('  ',o)
json.dump(dict(other_leaves=[list(map(str,o)) for o in other[:200]],root=root,sw=Sw,nodes=len(nodes),leaves=len(leaves),variants=summ,leaf_table={str(k):v for k,v in cnt.items()},shallowest=[list(map(str,e)) for e in ex[:40]]),open(sys.argv[3],'w'),indent=1)
