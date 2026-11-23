import ast,collections,sys
for fn in sys.argv[1:]:
  tot=collections.Counter(); cur=None; named=collections.Counter(); pm=collections.defaultdict(collections.Counter); odd=[]
  for l in open(fn):
    if l.startswith('W='): W=l.split()[0][2:]; R=l.split()[1].rstrip(':')
    elif l.strip().startswith('classes'): tot.update(ast.literal_eval(l.split('classes',1)[1].strip()))
    elif l.strip().startswith('NAMED'):
        p=l.split(); nm=p[1]; reg=p[2]; cfg=p[3:-2]
        if R=='free' and nm=='+1': named[W]+=1
        pm[nm][(len(cfg),R)]+=1
        if nm in ('+1','-1') and int(W)%2==1: odd.append((W,R,nm,' '.join(cfg),p[-2],p[-1]))
  print(fn, dict(sorted(tot.items()))); print(' free +1 roots by W',dict(named))
  for k,v in pm.items(): print(' ',k,dict(v))
  print(' odd-width +-1 (pairs):',collections.Counter(len(o[3].split()) for o in odd)); print(' examples', odd[:6])
