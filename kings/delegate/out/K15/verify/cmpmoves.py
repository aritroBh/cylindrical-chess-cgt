import sys
def parse(fn):
    d={}
    for ln in open(fn):
        ln=ln.strip()
        if not ln: continue
        parts=[p.strip() for p in ln.split('|')]
        pos=parts[0]
        if len(parts)==3:
            root=parts[1]; mv=parts[2]
        else:
            toks=parts[1].split(None,1); root=toks[0]; mv=toks[1] if len(toks)>1 else ''
        d[pos]=(root.replace(' ',''), tuple(sorted(mv.split())))
    return d
a=parse(sys.argv[1]); b=parse(sys.argv[2])
bad=0
for k in a:
    if k not in b or a[k]!=b[k]:
        bad+=1; print('DIFF',k,a[k],b.get(k))
nm=sum(len(v[1]) for v in a.values()); dr=sum(1 for v in a.values() for m in v[1] if m.endswith(':D'))
print(sys.argv[1],'roots',len(a),len(b),'diffs',bad,'moves',nm,'draw',dr,'nondraw',nm-dr)
