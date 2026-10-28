import itertools,subprocess,collections,sys,json
W,H=8,6
files=[4,5,6]
sqs=[(f,r) for f in files for r in range(1,H-1)]
def nb(f,d): return (f+d)%W
def name(s): return "abcdefgh"[s[0]]+str(s[1]+1)
def moves(ws,bs,ep,color):
    """all pawn moves of colour; returns list of (ws,bs,ep,promo)"""
    out=[]; occ=set(ws)|set(bs)
    own,en=(ws,bs) if color=='w' else (bs,ws); dr=1 if color=='w' else -1; start=1 if color=='w' else H-2; last=H-1 if color=='w' else 0
    for (f,r) in own:
        def mv(newpos,cap=None,e=None):
            o=set(own); o.discard((f,r)); 
            if newpos[1]!=last: o.add(newpos)
            e2=set(en)
            if cap: e2.discard(cap)
            nw,nb_=(frozenset(o),frozenset(e2)) if color=='w' else (frozenset(e2),frozenset(o))
            out.append((nw,nb_,e,newpos[1]==last))
        t=(f,r+dr)
        if t not in occ:
            mv(t)
            if r==start and (f,r+2*dr) not in occ:
                tt=(f,r+2*dr)
                # e.p. right only if an enemy pawn beside
                can=any(((nb(f,d),r+2*dr) in en) for d in (-1,1))
                mv(tt,None,(f,r+dr) if can else None)
        for d in (-1,1):
            g=(nb(f,d),r+dr)
            if g in en: mv(g,g)
            elif ep is not None and ep==g and (g[0],r) in en: mv(g,(g[0],r))
    return out
def can_promote(ws,bs):
    seen=set(); stack=[(ws,bs,None)]
    while stack:
        st=stack.pop()
        if st in seen: continue
        seen.add(st)
        for color in 'wb':
            for nw,nb_,e,pr in moves(st[0],st[1],st[2],color):
                if pr: return True
                stack.append((nw,nb_,e))
    return False
def has_move(ws,bs,color): return len(moves(ws,bs,None,color))>0
ctx=[]
for nw in range(3):
  for ws in itertools.combinations(sqs,nw):
    for nbk in range(3):
      for bs in itertools.combinations(sqs,nbk):
        if set(ws)&set(bs): continue
        if not ws or not bs: continue
        ws_,bs_=frozenset(ws),frozenset(bs)
        if not(has_move(ws_,bs_,'w') and has_move(ws_,bs_,'b')): continue
        ctx.append((ws,bs))
print(len(ctx),'contexts')
lines=[]
for ws,bs in ctx:
    pw=" ".join("P"+name(s) for s in ws); pb=" ".join("p"+name(s) for s in bs)
    lines.append(f"Ka1 kc6 {pw} {pb} w -"); lines.append(f"Ka1 kc6 {pw} {pb} b -")
open('ctx_frozen_in.txt','w').write("\n".join(lines)+"\n")
out=subprocess.run(['./ref3','--board','cyl:8x6','--frozen'],input="\n".join(lines)+"\n",capture_output=True,text=True).stdout.strip().split("\n")
res={}
for l in out:
    if '|' in l:
        p,v=l.rsplit('|',1); res[p.strip()]=v.strip()
cls=lambda a,b: {'LW':'zero','LL':'negative','WW':'positive','WL':'fuzzy'}.get(a+b,a+b)
C=collections.Counter(); CP=collections.Counter(); data=[]
for ws,bs in ctx:
    pw=" ".join("P"+name(s) for s in ws); pb=" ".join("p"+name(s) for s in bs)
    a=res[f"Ka1 kc6 {pw} {pb} w -"]; b=res[f"Ka1 kc6 {pw} {pb} b -"]
    c=cls(a,b); C[c]+=1
    pf=not can_promote(frozenset(ws),frozenset(bs))
    if pf: CP[c]+=1
    data.append({'w':[name(s) for s in ws],'b':[name(s) for s in bs],'cls':c,'promfree':pf})
print('classes',dict(C)); print('promotion-free classes',dict(CP),sum(CP.values()))
json.dump(data,open('ctx_classes.json','w'))
