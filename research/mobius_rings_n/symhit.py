import subprocess,sys,re
def parse(tok):
    w=[];b=[]
    if tok=='-': return w,b
    for m in re.finditer(r'([WB])(\d+)',tok):
        (w if m.group(1)=='W' else b).extend(int(c) for c in m.group(2))
    return sorted(w),sorted(b)
def fmt(w,b):
    s=('W'+''.join(map(str,sorted(w))) if w else '')+('B'+''.join(map(str,sorted(b))) if b else '')
    return s or '-'
def kappa(r): return ' '.join(fmt([9-x for x in parse(t)[1]],[9-x for x in parse(t)[0]]) for t in r.split())
def mirror(r): return ' '.join(reversed(r.split()))
hits=[l.strip() for l in open(sys.argv[1]) if l.strip()]
bad=0
for r in hits:
    n=len(r.split()); imgs=[r,mirror(r),kappa(r),mirror(kappa(r))]
    for binp,ex in (('bin/mob1_32',['solve']),('bin/mob2_32',['solve'])):
        o=subprocess.run([binp]+ex,input='\n'.join(imgs)+'\n',capture_output=True,text=True).stdout.split()
        if set(o)!={'NNPN'}: bad+=1; print('MISMATCH',r,binp,o)
    o=subprocess.run(['bin/check','mobius',str(n),'solve'],input='\n'.join(imgs)+'\n',capture_output=True,text=True).stdout.split()
    if set(o)!={'NNPN'}: bad+=1; print('MISMATCH check',r,o)
print(len(hits),'hits x 4 images x 3 programs; mismatches',bad)
