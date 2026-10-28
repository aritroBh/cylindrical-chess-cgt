import json,subprocess,collections
ctx=json.load(open('ctx_classes.json')); groups=json.load(open('es_groups.json'))
c11=[c for c in ctx if len(c['w'])==1 and len(c['b'])==1]
z12=[c for c in ctx if c['cls']=='zero' and (len(c['w']),len(c['b'])) in ((1,2),(2,1))]
print('1+1 contexts',len(c11),collections.Counter(c['cls'] for c in c11),'zero 1+2/2+1:',len(z12),[ (c['w'],c['b']) for c in z12])
ctxs=c11+z12; print('contexts used',len(ctxs))
def parse(Y):
    t=Y.split(); return t[:-2]
def apply(Y,mv):
    # mv like Ka1-h1 : king move of White
    frm,to=mv[1:].split('-')
    toks=Y.split()[:-2]; out=[]
    for x in toks:
        if x=='K'+frm: out.append('K'+to)
        else: out.append(x)
    return out
lines=[];meta=[]
for Y,sorts in groups:
    for mv in sorts:
        toks=apply(Y,mv)
        for c in ctxs:
            pw=" ".join("P"+s for s in c['w']); pb=" ".join("p"+s for s in c['b'])
            lines.append(" ".join(toks)+" "+pw+" "+pb+" b -"); meta.append((Y,mv,c))
# also bare sortie positions (control, expected L)
out=subprocess.run(['./ref3','--board','cyl:8x6'],input="\n".join(lines)+"\n",capture_output=True,text=True).stdout.strip().split("\n")
res=[l.rsplit('|',1)[1].strip() for l in out if '|' in l]
assert len(res)==len(lines)
C=collections.Counter(); notp=[]
for (Y,mv,c),r in zip(meta,res):
    C[(c['cls'],r)]+=1
    if c['cls'] in('zero','negative') and r not in('X','L'): notp.append((Y,mv,c['w'],c['b'],c['cls'],r))
for k in sorted(C): print(k,C[k])
sp=sum(v for (cl,r),v in C.items() if cl in('zero','negative') and r!='X')
print('second-player-win contexts legal:',sp,' not punished:',len(notp))
json.dump(notp,open('es_notpunished.json','w'))
