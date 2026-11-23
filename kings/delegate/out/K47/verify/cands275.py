# referee: candidate games against the investigator's full battery (../tests.txt, 275 games) and its Z column (../logs/full_A_N.out)
src=open('cands.py').read().split('names=list(C)')[0]; exec(src)
def tiny(x):  # {0 || 0 | -x}: nodes 0 root, 1 zero, 2 {0|-x}, then -x chain
    spec={0:([1],[2]),1:([],[]),2:([1],[3])}
    for i in range(x):
        spec[3+i]=([],[3+i+1] if i<x-1 else [1])
    return mk(spec)
for x in (1,2,3,4): C['tiny%d'%x]=tiny(x)
C['up2*']=C['up2*']
inv={}
for l in open('../logs/full_A_N.out'):
    p=[q.strip() for q in l.split('|')]; inv[(p[0],'A' if 'kd4' in p[1] else 'B',p[2])]=p[3].split()[1]
T275=readT('../tests.txt')
for r,cl in (('A',['tiny1','tiny2','tiny3','tiny4','up2','up2*']),('B',['up2*','up2','up*','tiny2'])):
    for n in cl:
        bad=[]
        for tn,T in T275:
            f=solve(summ(C[n],T))
            for s,ss in ((0,'w'),(1,'b')):
                if f(0,s)!=inv[(tn,r,ss)]: bad.append(tn+'/'+ss)
        print('root',r,n,'mismatches',len(bad),'of',2*len(T275),' '.join(bad[:12]))
