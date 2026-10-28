import json,subprocess,collections
ctx=json.load(open('ctx_classes.json')); groups=json.load(open('es_groups.json'))
pf=[c for c in ctx if c['promfree'] and c['cls']=='zero']
print('promotion-free zero contexts',len(pf),[(c['w'],c['b']) for c in pf])
lines=[];meta=[]
for Y,sorts in groups:
    for mv in sorts:
        frm,to=mv[1:].split('-'); toks=[('K'+to if x=='K'+frm else x) for x in Y.split()[:-2]]
        for c in pf:
            pw=" ".join("P"+s for s in c['w']); pb=" ".join("p"+s for s in c['b'])
            lines.append(" ".join(toks)+" "+pw+" "+pb+" b -"); meta.append((Y,mv,c))
out=subprocess.run(['./ref3','--board','cyl:8x6'],input="\n".join(lines)+"\n",capture_output=True,text=True).stdout.strip().split("\n")
res=[l.rsplit('|',1)[1].strip() for l in out if '|' in l]
print(len(lines),'pairs;',collections.Counter(res))
