import re,glob
rows=[]
for f in sorted(glob.glob('logs/A_cyl*x6_f*.out')):
    m=re.search(r'cyl(\d+)x6_f([0-9_]+)\.out',f); W=int(m.group(1)); tri=m.group(2).replace('_',',')
    for line in open(f):
        if line.startswith('RESULT'):
            kv=dict(re.findall(r'(\w+)=(\d+)',line)); who='over' if 'black' in line.split()[2] else 'under'
            rows.append((W,tri,who,int(kv['placements']),int(kv['F1']) if 'F1' in kv else None,line))
def g(line,key):
    return int(re.search(key+r'=(\d+)',line).group(1))
print('W\tfiles\ttest\tplacements\tF1(O1)\tnoFreeze\tpromoFreeze\tF2(O2)\tF3(O3,loose)\tF4(O4,exact)\thalfExact')
for W,tri,who,pl,_,line in sorted(rows):
    f1=int(re.search(r'F1\(U1 at both shuttler roots\)=(\d+)',line).group(1))
    f2=int(re.search(r'F2\(U2\)=(\d+)',line).group(1)); f3=int(re.search(r'F3\(U3 loose\)=(\d+)',line).group(1))
    f4=int(re.search(r'F4\(exact U4\)=(\d+)',line).group(1))
    print('\t'.join(map(str,[W,tri,who,pl,f1,g(line,'noFreeze'),g(line,'promoFreeze'),f2,f3,f4,g(line,'halfExact')])))
