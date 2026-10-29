import json,re,sys,collections,glob
mine=collections.defaultdict(set)
for f in sys.argv[1:]:
    for l in open(f):
        m=re.match(r'ROOT (\S+) (\d+) (\d+) a(\d+) (\S+) K([a-z])(\d+) k([a-z])(\d+)',l)
        if m:
            b,W,H,r,cl,wf,wr,bf,br=m.groups()
            mine[(int(W),int(H),int(r))].add((cl,ord(wf)-97,int(wr),ord(bf)-97,int(br)))
k31=collections.defaultdict(set)
for f in ['../../logs/structure_roots.jsonl','../../logs/structure_ext.jsonl','../../logs/structure_h4.jsonl','../../logs/structure_w26.jsonl']:
    for l in open(f):
        d=json.loads(l)
        if 'W' not in d: continue
        k31[(d['W'],d['H'],d['r'])].add((d['cl'],d['wk'][0],d['wk'][1],d['bk'][0],d['bk'][1]))
common=[k for k in k31 if k in mine]
bad=[k for k in common if k31[k]!=mine[k]]
print('K31 cases with dumps',len(k31),'in my sweep',len(common),'identical sets',len(common)-len(bad),'roots compared',sum(len(k31[k]) for k in common))
print('cases in K31 dumps with roots but not in my files',len([k for k in k31 if k not in mine and k31[k]]))
print(bad[:5])
# also zero-root cases: mine has none where K31 has some
