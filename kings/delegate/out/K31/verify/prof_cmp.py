import subprocess,re,json,collections,sys,time
logs='/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31/logs/'
K=collections.defaultdict(lambda: {k:collections.Counter() for k in ('Lw','Fw','Lb','Fb')})
for l in open(logs+'profile_N12.jsonl'):
    r=json.loads(l)
    for k in ('Lw','Fw','Lb','Fb'): K[(r['board'],r['pairs'])][k][r[k]]+=r['n']
cfgs=sorted(K.keys())
bad=0;n=0;t0=time.time();tot=0
for b,p in cfgs:
    kind,dims=b.split(':'); W,H=dims.split('x')
    o=subprocess.run(['nice','-n','15','./src/prof',kind,W,H,p,'12'],capture_output=True,text=True).stdout
    mine={}
    for line in o.splitlines():
        m=re.match(r' (Lw|Fw|Lb|Fb) \{(.*)\}',line)
        if m: mine[m.group(1)]={int(a):int(c) for a,c in (x.split(':') for x in m.group(2).split())}
    n+=1
    for k in mine:
        if dict(K[(b,p)][k])!=mine[k]: bad+=1; print('DIFF',b,p,k,mine[k],dict(K[(b,p)][k]))
    tot+=sum(mine['Lw'].values())
print('configs compared',n,'diffs',bad,'root entries',tot,'secs',time.time()-t0)
