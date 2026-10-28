import re,sys,gzip
def norm(line):
    # strip replies "(..)" and sort moves
    p=[x.strip() for x in line.rstrip("\n").split("|")]
    var,Y,info,flag,rest=p[0],p[1],p[2],p[3],p[4]
    Y=" ".join(sorted(Y.split()[:-2]))+" "+" ".join(Y.split()[-2:])
    moves=sorted(re.sub(r"\([^)]*\)","",s) for s in re.findall(r"\[([^\]]*)\]",rest))
    return (var,Y,info,flag,tuple(moves))
theirs=set(); n=0
for l in gzip.open(sys.argv[1],'rt'):
    if l.startswith('#'): continue
    theirs.add(norm(l)); n+=1
mine=set(); m=0
for f in sys.argv[2:]:
    for l in open(f):
        if l.startswith('#'): continue
        mine.add(norm(l)); m+=1
print('theirs',n,len(theirs),'mine',m,len(mine))
print('only theirs',len(theirs-mine),'only mine',len(mine-theirs))
for x in list(theirs-mine)[:3]: print('T',x)
for x in list(mine-theirs)[:3]: print('M',x)
