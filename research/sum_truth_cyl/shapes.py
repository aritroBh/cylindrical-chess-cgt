import json
rows=[json.loads(l) for l in open('/Users/aritro/Downloads/Research/Chessendgames/kings/results/exp_cyl7x6_epon_Q_conv.jsonl')]
def parse(r):
    w,b=r['P'].split(' / ');return w[3:].split(),b[3:].split()
sh={}
for r in rows:
    if r['verdict']!='match': continue
    w,b=parse(r)
    fs={s[0] for s in w+b}
    if len(fs)!=1: continue
    f=fs.pop()
    key=(tuple(s[1:] for s in w),tuple(s[1:] for s in b))
    sh.setdefault(key,{})[f]=r
print(len(sh))
for k,v in sh.items(): print(k,sorted(v), [ (x['value'],x['outcome'],x['real']['wtm'][0],x['real']['btm'][0]) for x in v.values()])
