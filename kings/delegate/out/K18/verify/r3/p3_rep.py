import json,collections
exec(open('ctx_enum.py').read().split("ctx=[]")[0])
ctx=json.load(open('ctx_classes.json')); groups=json.load(open('es_groups.json'))
def sqidx(s): return ("abcdefgh".index(s[0]),int(s[1:])-1)
def Xset(c):
    ws=frozenset(sqidx(s) for s in c['w']); bs=frozenset(sqidx(s) for s in c['b'])
    seen=set(); st=[(ws,bs,None)]; X=set()
    while st:
        s=st.pop()
        if s in seen: continue
        seen.add(s); X|=set(s[0])|set(s[1])
        for col in 'wb':
            for nw,nb_,e,pr in moves(s[0],s[1],s[2],col):
                if not pr: st.append((nw,nb_,e))
    return X
def nbh(X):
    N=set()
    for (f,r) in X:
        for df in (-1,0,1):
            for dr in (-1,0,1):
                if 0<=r+dr<H: N.add(((f+df)%W,r+dr))
    return N
c11=[c for c in ctx if len(c['w'])==1 and len(c['b'])==1]
z12=[c for c in ctx if c['cls']=='zero' and (len(c['w']),len(c['b'])) in ((1,2),(2,1))]
notp=json.load(open('es_notpunished.json'))
# pairs: legal zero/neg = need legality -> recompute with ref3 results is heavy; use sortie king square after m instead and count over all zero/neg contexts
tot=inN=0
for Y,sorts in groups:
    for mv in sorts:
        to=sqidx(mv[1:].split('-')[1])
        for c in c11+z12:
            if c['cls'] not in('zero','negative'): continue
            N=nbh(Xset(c)); tot+=1; inN+= to in N
print('ES zero/neg pairs (incl. illegal):',tot,' sortie king square after m already in N(X):',inN)
