# referee's own test games (D-games, node 0 = start): name | n | i: L=.. R=..
import sys
def g(L,R): return (L,R)
base = {}
def integer(n):
    # n>0: chain n -> n-1 ... 0 by Left; n<0 by Right
    k=abs(n); L=[[] for _ in range(k+1)]; R=[[] for _ in range(k+1)]
    for i in range(k):
        (L if n>0 else R)[i].append(i+1)
    return (L,R)
for n in range(-3,4): base[str(n)]=integer(n)
base['*']=([[1],[]],[[1],[]])
base['up']=([[2],[2],[]],[[1],[2],[]])      # up={0|*}: 1=*,2=0
base['down']=([[1],[2],[]],[[2],[2],[]])    # down={*|0}
base['pm1']=([[1],[3],[],[]],[[2],[],[3],[]])  # {1|-1}: 1={0|},2={|0},3=0
base['over']=([[1],[]],[[0],[]])            # {0|over}
base['under']=([[0],[]],[[1],[]])           # {under|0}
base['on']=([[0]],[[]]); base['off']=([[]],[[0]]); base['dud']=([[0]],[[0]])
def summ(a,b):
    (La,Ra),(Lb,Rb)=a,b; na,nb=len(La),len(Lb); idx=lambda i,j:i*nb+j
    L=[[] for _ in range(na*nb)]; R=[[] for _ in range(na*nb)]
    for i in range(na):
        for j in range(nb):
            for x in La[i]: L[idx(i,j)].append(idx(x,j))
            for x in Lb[j]: L[idx(i,j)].append(idx(i,x))
            for x in Ra[i]: R[idx(i,j)].append(idx(x,j))
            for x in Rb[j]: R[idx(i,j)].append(idx(i,x))
    return (L,R)
out=[]
names=['0','*','up','down','pm1','over','under','on','off','dud','-3','-2','-1','1','2','3']
for n in names: out.append((n,base[n]))
for a,b in [('*','down'),('*','up'),('*','under'),('up','under'),('down','under'),('under','under'),('down','down'),('1','pm1'),('*','*'),('over','*'),('over','under')]:
    out.append((a+'+'+b, summ(base[a],base[b])))
for n,(L,R) in out:
    print(n,'|',len(L),'|',' ; '.join('%d: L=%s R=%s'%(i,','.join(map(str,L[i])),','.join(map(str,R[i]))) for i in range(len(L))))
