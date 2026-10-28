import subprocess, gzip, re, sys, collections
LOGS='/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K20/logs/'
def configs(logname):
    cfgs=[]
    for line in gzip.open(LOGS+logname,'rt'):
        m=re.match(r'CONFIG (.*?) : nodes (\d+)  faithful (\d)',line)
        if m: cfgs.append((m.group(1).strip(),int(m.group(2)),int(m.group(3))))
    return cfgs
def run(board,cfg,margin):
    pairs=','.join(cfg.split()) if cfg!='none' else 'none'
    out=subprocess.run(['./lk','classify',board,pairs,margin],capture_output=True,text=True).stdout
    res={}
    for l in out.splitlines()[1:]:
        m=re.match(r'\s+(\S+)\s+(\d+)\s+e\.g\.',l)
        if m: res[m.group(1)]=int(m.group(2))
    return res, out.splitlines()[0]
if __name__=='__main__':
    board,logname,margin=sys.argv[1:4]
    tot=collections.Counter(); n=0
    for cfg,nodes,f in configs(logname):
        r,h=run(board,cfg,margin)
        tot.update(r)
    print(board,margin,dict(tot), sum(tot.values()))
