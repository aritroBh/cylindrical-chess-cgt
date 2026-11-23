# referee: which small candidate games G have the same results as root A / root B of Z_O against the 27 referee tests?
import sys
src=open('small.py').read().split('tests=readT')[0]; exec(src)
tests=readT('tests_ref.txt')
def mk(spec):
    n=len(spec); return ([spec[i][0] for i in range(n)],[spec[i][1] for i in range(n)])
def prepend(Lroot,Rroot,g):  # new root 0 with options into shifted copy of g (g's nodes +1); Lroot/Rroot index g's nodes
    L=[[x+1 for x in l] for l in g[0]]; R=[[x+1 for x in r] for r in g[1]]
    return ([[x+1 for x in Lroot]]+L,[[x+1 for x in Rroot]]+R)
C={k:G[k] for k in ['0','*','up','down','over','over+*','over+down','over+up','{over|0}','{0|0,over}','tiny1','miny1']}
C['up*']=mk({0:([1,2],[1]),1:([],[]),2:([1],[1])})
C['up2']=prepend([0],[2],mk({0:([],[]),1:([0],[0]),2:([0,1],[0])}))  # {0 | up*}: 0=0, 1=*, 2=up*
C['up2*']=summ(C['up2'],G['*'])
C['up+up']=summ(G['up'],G['up'])
C['tiny2']=mk({0:([1],[2]),1:([],[]),2:([1],[3]),3:([],[4]),4:([],[1])})
ost=summ(G['over'],G['*'])   # node 0 = over+*, node 3 = 0+0
C['{0|over*}']=prepend([3],[0],ost)
C['over+down+*']=summ(G['over'],G['down'],G['*'])
C['over+tiny1']=summ(G['over'],G['tiny1'])
names=list(C)
sig={n:[] for n in names}
for n in names:
    for tn,T in tests:
        f=solve(summ(C[n],T)); sig[n].append(f(0,0)+f(0,1))
Z={'A':[],'B':[]}
for l in open('logs/main_N.out'):
    p=[x.strip() for x in l.split('|')]; Z['A'].append(p[1]); Z['B'].append(p[2])
tn=[t for t,_ in tests]
for r in 'AB':
    print('root',r,' '.join('%s:%s'%(a,b) for a,b in zip(tn,Z[r])))
    for n in names:
        d=[tn[i] for i in range(len(tn)) if sig[n][i]!=Z[r][i]]
        print('   %-14s mismatches %2d %s'%(n,len(d),' '.join(d[:10])))
