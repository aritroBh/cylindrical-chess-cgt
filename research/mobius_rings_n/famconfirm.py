import subprocess,sys,re
sys.path.insert(0,'.')
def run(binp,ring,extra=[]):
    p=subprocess.run(['nice','-n','15',binp,'solve']+extra,input=ring+'\n',capture_output=True,text=True,timeout=300)
    m=re.search(r'nodes (\d+)',p.stderr); return p.stdout.strip(),(int(m.group(1)) if m else None)
fams={
 'F1 (B4 W2)^m B6 W2 W3 B6 B7 W3 B7 W5 ; n=2m+8': (lambda m: ['B4','W2']*m+'B6 W2 W3 B6 B7 W3 B7 W5'.split(), range(0,14)),
 'F2 (B4 W2)^m B6 W2 W3 B6 B7 W3 B7 W5 B7 ; n=2m+9': (lambda m: ['B4','W2']*m+'B6 W2 W3 B6 B7 W3 B7 W5 B7'.split(), range(0,13)),
 'F3 B6 W2 W3 B6 B7 W3 (B7 W5)^m W6B7 ; n=2m+7, n+1 pawns': (lambda m: 'B6 W2 W3 B6 B7 W3'.split()+['B7','W5']*m+['W6B7'], range(0,13)),
}
for name,(g,rg) in fams.items():
    print(name)
    for m in rg:
        t=g(m); n=len(t)
        if n>32: break
        r=' '.join(t)
        s2,_=run('bin/mob2_32',r); s1,nodes=run('bin/mob1_32',r)
        s3=run('bin/check',r,[]) [0] if False else None
        c=''
        if n<=21:
            q=subprocess.run(['nice','-n','15','bin/check','mobius',str(n),'solve'],input=r+'\n',capture_output=True,text=True)
            c=q.stdout.strip()
        print(f'  m={m} n={n} pawns={sum(len(x.replace("W","B").split("B"))-1 if False else 0 for x in t) or ""} mob1={s1} mob2={s2} check={c} mob1_nodes={nodes}',flush=True)
