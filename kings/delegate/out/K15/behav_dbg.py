import sys
sys.argv=['x','8','6','0','0','0','1','']
exec(open('behav.py').read().split('if __name__ == "__main__":')[0])
root=parse("Ka2 kc4 Pa4 Pc2 pa5 pc3 w -")
start,opts=group_graph(root)
print("nodes",len(opts))
# D-model solve with explicit values
nodes=list(opts); nid={x:i for i,x in enumerate(nodes)}
ctxs=contexts(); cid={c:i for i,c in enumerate(ctxs)}; n=len(nodes)
def sidx(stm,ci,ni): return (stm*len(ctxs)+ci)*n+ni
S=2*len(ctxs)*n; succ=[None]*S; win=[False]*S
for stm in (0,1):
    for ci,(a,b,c) in enumerate(ctxs):
        for ni,x in enumerate(nodes):
            s=sidx(stm,ci,ni); lst=[]; w=False
            for o in opts[x][stm]:
                if o=="WIN": w=True
                else: lst.append(sidx(1-stm,ci,nid[o]))
            plain=(x[0],x[1],x[2],x[3],None); pn=nid[plain]
            mine=a if stm==0 else b
            if mine>0:
                na,nb=(a-1,b) if stm==0 else (a,b-1); lst.append(sidx(1-stm,cid[(na,nb,c)],pn))
            if c>0: lst.append(sidx(1-stm,cid[(a,b,c-1)],pn))
            succ[s]=lst; win[s]=w
preds=[[] for _ in range(S)]; cnt=[len(x) for x in succ]
for s in range(S):
    for t in succ[s]: preds[t].append(s)
val=[0]*S; q=[]; 
for s in range(S):
    if win[s]: val[s]=1; q.append(s)
    elif cnt[s]==0: val[s]=2; q.append(s)
qi=0
while qi<len(q):
    v=q[qi]; qi+=1
    for u in preds[v]:
        if val[u]: continue
        if val[v]==2: val[u]=1; q.append(u)
        else:
            cnt[u]-=1
            if cnt[u]==0: val[u]=2; q.append(u)
def show(s):
    stm=s//(len(ctxs)*n); r=s%(len(ctxs)*n); ci=r//n; ni=r%n
    x=nodes[ni]; nm=lambda sq:"abcdefgh"[sq[0]]+str(sq[1]+1)
    return f"stm={'wb'[stm]} ctx={ctxs[ci]} K{nm(x[0])} k{nm(x[1])} v={val[s]}"
r=nid[start]
s=sidx(1,cid[(0,0,1)],r)
print(show(s))
# follow winning line
for step in range(12):
    if val[s]==1:
        # mover wins: pick a successor with val 2 (or win)
        if win[s]: print("  mover promotes -> wins"); break
        nxt=[t for t in succ[s] if val[t]==2][0]
    elif val[s]==2:
        # mover loses: opponent wins; show all successors are val1; pick first
        nxt=succ[s][0] if succ[s] else None
        if nxt is None: print("  mover has no moves -> loses"); break
    else: break
    print("  ->",show(nxt)); s=nxt
