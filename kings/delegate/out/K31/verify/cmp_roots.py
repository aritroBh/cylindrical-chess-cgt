import json,re,collections,sys
logs='/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31/logs/'
K=collections.defaultdict(set)
for f in ['structure_ext','structure_h4','structure_w26']:
    for l in open(logs+f+'.jsonl'):
        r=json.loads(l); K[(r['W'],r['H'],r['r'],r['cl'])].add((tuple(r['wk']),tuple(r['bk'])))
M=collections.defaultdict(set); pend=[]; allc=set()
for l in open(sys.argv[1]):
    if l.startswith('DUMP'):
        m=re.match(r'DUMP (\S+) :: K(.)(\d+) k(.)(\d+) ',l)
        pend.append((m.group(1),((ord(m.group(2))-97),int(m.group(3))),((ord(m.group(4))-97),int(m.group(5)))))
    else:
        m=re.match(r'cyl:(\d+)x(\d+) a(\d+)',l); W,H,r=map(int,m.groups()); allc.add((W,H,r))
        for cl,wk,bk in pend: M[(W,H,r,cl)].add((wk,bk))
        pend=[]
bad=0;n=0;tot=0
for (w,h,rr) in sorted(allc):
    for cl in ('+1','-1'):
        a=M.get((w,h,rr,cl),set()); b=K.get((w,h,rr,cl),set()); n+=1; tot+=len(a)
        if a!=b: bad+=1; print('DIFF',w,h,rr,cl,len(a),len(b))
print('cases',len(allc),'class-sets compared',n,'roots compared',tot,'differences',bad)
