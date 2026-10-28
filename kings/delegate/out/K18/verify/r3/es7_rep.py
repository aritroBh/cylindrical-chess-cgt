import itertools,subprocess,collections,json,re,sys
W,H=7,6; files=[4,5]
sys.setrecursionlimit(10000)
exec(open('ctx_enum.py').read().split("ctx=[]")[0].replace("W,H=8,6","W,H=7,6").replace("files=[4,5,6]","files=[4,5]"))
ctx=[]
for nw in range(3):
  for ws in itertools.combinations(sqs,nw):
    for nbk in range(3):
      for bs in itertools.combinations(sqs,nbk):
        if set(ws)&set(bs) or not ws or not bs: continue
        ws_,bs_=frozenset(ws),frozenset(bs)
        if not(has_move(ws_,bs_,'w') and has_move(ws_,bs_,'b')): continue
        ctx.append((ws,bs))
print(len(ctx),'contexts on cyl:7x6 e,f (<=2+2)')
lines=[]
for ws,bs in ctx:
    pw=" ".join("P"+name(s) for s in ws); pb=" ".join("p"+name(s) for s in bs)
    lines+= [f"Ka1 kc6 {pw} {pb} w -",f"Ka1 kc6 {pw} {pb} b -"]
out=subprocess.run(['./ref3','--board','cyl:7x6','--frozen'],input="\n".join(lines)+"\n",capture_output=True,text=True).stdout.strip().split("\n")
res={l.rsplit('|',1)[0].strip():l.rsplit('|',1)[1].strip() for l in out if '|' in l}
cls=lambda a,b: {'LW':'zero','LL':'negative','WW':'positive','WL':'fuzzy'}.get(a+b,a+b)
data=[]
for ws,bs in ctx:
    pw=" ".join("P"+name(s) for s in ws); pb=" ".join("p"+name(s) for s in bs)
    data.append({'w':[name(s) for s in ws],'b':[name(s) for s in bs],'cls':cls(res[f"Ka1 kc6 {pw} {pb} w -"],res[f"Ka1 kc6 {pw} {pb} b -"])})
print(collections.Counter(d['cls'] for d in data))
json.dump(data,open('ctx7_classes.json','w'))
# groups from my own cyl:7x6 search
nf=3
def msq(s): return chr(97+nf-1-(ord(s[0])-97))+s[1:]
def canon(y):
    t=y.split(); a=tuple(sorted(t[:-2])); b=tuple(sorted(x[0]+msq(x[1:]) for x in t[:-2])); return min(a,b)
groups={}
for l in open('../mine/s_7x6_f3_22_q1.txt'):
    if l.startswith('#'): continue
    p=[x.strip() for x in l.split('|')]
    if p[3]!='NOESC': continue
    toks=p[1].split(); nP=sum(1 for t in toks if t[0]=='P'); nb=sum(1 for t in toks if t[0]=='p')
    if (nP,nb)!=(1,1): continue
    k=canon(p[1])
    if k in groups: continue
    groups[k]=(p[1],[s.split()[0] for s in re.findall(r"\[([^\]]*)\]",p[4]) if s.split()[1]=='PLAIN-ONLY' and s.split()[0].startswith('K')])
print('7x6 groups',len(groups),'king sorties',sum(len(v[1]) for v in groups.values()))
c11=[c for c in data if len(c['w'])==1 and len(c['b'])==1]
z12=[c for c in data if c['cls']=='zero' and (len(c['w']),len(c['b']))!=(1,1)]
print('1+1',len(c11),'zero 1+2/2+1',len(z12)); ctxs=c11+z12; print('contexts used',len(ctxs))
lines=[];meta=[]
for Y,sorts in groups.values():
    for mv in sorts:
        frm,to=mv[1:].split('-'); toks=[('K'+to if x=='K'+frm else x) for x in Y.split()[:-2]]
        for c in ctxs:
            pw=" ".join("P"+s for s in c['w']); pb=" ".join("p"+s for s in c['b'])
            lines.append(" ".join(toks)+" "+pw+" "+pb+" b -"); meta.append((Y,mv,c))
out=subprocess.run(['./ref3','--board','cyl:7x6'],input="\n".join(lines)+"\n",capture_output=True,text=True).stdout.strip().split("\n")
res=[l.rsplit('|',1)[1].strip() for l in out if '|' in l]
C=collections.Counter(); notp=[]
for (Y,mv,c),r in zip(meta,res):
    C[(c['cls'],r)]+=1
    if c['cls'] in('zero','negative') and r not in('X','L'): notp.append((Y,mv,c['w'],c['b'],c['cls'],r))
for k in sorted(C): print(k,C[k])
sp=sum(v for (cl,r),v in C.items() if cl in('zero','negative') and r!='X'); print('legal second-player-win',sp,'not punished',len(notp))
