import subprocess,re,sys,gzip
sys.path.insert(0,'.')
from agg import configs
board,log,margin=sys.argv[1:4]
tot=0;rt=0;withs=[]
for cfg,_,_ in configs(log):
    pairs=','.join(cfg.split()) if cfg!='none' else 'none'
    out=subprocess.run(['./lk','classify',board,pairs,margin],capture_output=True,text=True).stdout
    m=re.search(r'short roots: (\d+) of (\d+)',out)
    tot+=int(m.group(1)); rt+=int(m.group(2))
    if int(m.group(1)): withs.append((cfg,int(m.group(1))))
print(board,margin,'short',tot,'of',rt,withs[:12])
