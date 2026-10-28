import json
exec(open('p3_rep.py').read().split("c11=")[0])
c11=[c for c in ctx if len(c['w'])==1 and len(c['b'])==1]
z12=[c for c in ctx if c['cls']=='zero' and (len(c['w']),len(c['b'])) in ((1,2),(2,1))]
lines=[];meta=[]
def nm(s): return "abcdefgh"[s[0]]+str(s[1]+1)
for Y,sorts in groups:
    for mv in sorts:
        frm,to=mv[1:].split('-'); toks=[('K'+to if x=='K'+frm else x) for x in Y.split()[:-2]]
        pos=" ".join(toks)+" b -"
        for c in c11+z12:
            if c['cls'] not in('zero','negative'): continue
            N=nbh(Xset(c))
            lines.append(pos+" | "+" ".join(sorted(nm(s) for s in N))); meta.append((Y,mv,c))
open('p3_in.txt','w').write("\n".join(lines)+"\n"); json.dump([(a,b,c) for a,b,c in meta],open('p3_meta.json','w'))
print(len(lines),'lines')
