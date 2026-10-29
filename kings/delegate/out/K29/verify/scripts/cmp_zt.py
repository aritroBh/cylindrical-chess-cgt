import sys
def load(f): return [l.rsplit(' | ',1)[1].strip() for l in open(f)]
P=load('data/zt_P.ref3'); A=load('data/zt_park0.ref3'); B=load('data/zt_park1.ref3')
ins=[l.strip() for l in open('data/zt_P.in')]
assert len(P)==len(A)==len(B)==1770
nd=0; npk=0; X=0; diffs=[]
for c in range(885):
    p=(P[2*c],P[2*c+1]); a=(A[2*c],A[2*c+1]); b=(B[2*c],B[2*c+1])
    if 'X' in p+a+b: X+=1
    if p!=a: nd+=1; diffs.append((ins[2*c],p,a))
    if a!=b: npk+=1
print('contexts 885; Phi!=Psi(park0):',nd,' park0!=park1:',npk,' with X:',X)
nopass=0
for d in diffs[:5]: print(d)
