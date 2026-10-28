#!/usr/bin/env python3
import json, sys, collections
sys.path.insert(0,'scripts'); import kit
kit.setboard("cyl:8x6","0:3")
norm=lambda p: " ".join(sorted(p.split()))
res={}
for l in open('logs/bare_out.txt'):
    if ' | ' in l:
        p,r=l.rstrip().split(' | '); res[norm(p)]=r.split()[0]
c=json.load(open('logs/search_c8x6_f3_22.Q.json'))
cnt=collections.Counter(); bad=[]
for g in c:
    if g['flag']!='NOESC': continue
    Y=kit.lg2.parse(g['Y'])
    for m in g['moves']:
        Ym=kit.apply_move(Y,m['move'])
        r=res.get(norm(kit.fmt(Ym)))
        cnt[(m['cls'],r)]+=1
        if m['cls'] in('PLAIN-ONLY','both','IMM') and r!='L': bad.append((g['Y'],m['move'],r))
print(sorted(cnt.items(),key=str)); print('bad',len(bad),bad[:5])
