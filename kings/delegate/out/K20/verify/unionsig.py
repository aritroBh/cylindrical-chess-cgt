import sys,subprocess,os
sys.path.insert(0,'.')
from agg import configs
board,log=sys.argv[1:3]
S=set()
env=dict(os.environ,DUMPSIG='1')
for cfg,_,f in configs(log):
    pairs=','.join(cfg.split()) if cfg!='none' else 'none'
    out=subprocess.run(['./lk','classify',board,pairs,'free'],capture_output=True,text=True,env=env).stdout
    for l in out.splitlines():
        if l.startswith('SIG '): S.add(l)
print(board,'union distinct unclassified B34 signatures over all configs:',len(S))
