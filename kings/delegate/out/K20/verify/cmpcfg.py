import gzip,re,sys,subprocess,itertools,collections
sys.path.insert(0,'.')
LOGS='/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K20/logs/'
board,logname,margin=sys.argv[1:4]
cache={}
def mine(cfg,reg=None):
    key=(tuple(cfg),reg)
    if key in cache: return cache[key]
    pairs=','.join(cfg) if cfg else 'none'
    out=subprocess.run(['./lk','classify',board,pairs,reg if reg else margin],capture_output=True,text=True).stdout
    res=collections.Counter()
    for l in out.splitlines():
        m=re.match(r'\s+(\S+)\s+(\d+)\s+e\.g\.',l)
        if m: res[m.group(1)]=int(m.group(2))
    cache[key]=res; return res
# parse their log
theirs={}; cur=None; faith={}
for line in gzip.open(LOGS+logname,'rt'):
    m=re.match(r'CONFIG (.*?) : nodes \d+  faithful (\d)',line)
    if m:
        cur=m.group(1).strip(); theirs[cur]=collections.Counter(); faith[cur]=int(m.group(2)); continue
    m=re.match(r'\s+CLASS (.*?)\s+roots\s+(\d+)\s+short',line)
    if m and cur is not None:
        name=m.group(1).strip()
        name=name.replace('decisive ','')
        theirs[cur][name]+=int(m.group(2))
def regionfor(ps):
    if margin=='free' or not board.startswith('flat') or not ps: return None
    W=int(board.split(':')[1].split('x')[0])
    files=[ord(p[0])-97 for p in ps]
    return 'F%d-%d'%(max(0,min(files)-int(margin)),min(W-1,max(files)+int(margin)))
bad=0; ntot=0
for cfg,tc in theirs.items():
    if not faith[cfg]: continue
    ps=[] if cfg=='none' else cfg.split()
    mc=collections.Counter()
    for k in range(len(ps)+1):
        for sub in itertools.combinations(ps,k):
            mc.update(mine(list(sub),regionfor(ps)))
    # compare named
    names=set(tc)|set(mc)
    names.discard('UNMATCHED'); names.discard('other')
    tun=sum(v for k,v in tc.items() if k.startswith('UNMATCHED') or k.startswith('loopy'))
    row=[]
    for n in sorted(names):
        if tc.get(n,0)!=mc.get(n,0): row.append((n,tc.get(n,0),mc.get(n,0)))
    if mc.get('other',0)!=tun: row.append(('other/unmatched',tun,mc.get('other',0)))
    ntot+=1
    if row: bad+=1; print(cfg,row)
print(board,margin,'configs',ntot,'configs with any difference',bad)
