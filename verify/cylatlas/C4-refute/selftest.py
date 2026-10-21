import sys; sys.path.insert(0, '.')
from indep import *
Z=number(0); S=make([Z],[Z]); UP=make([Z],[S]); DN=neg(UP)
print('star', vkey(S), 'up', vkey(UP), 'up+up', vkey(add(UP,UP)), 'up+down', vkey(add(UP,DN)), 'star+star', vkey(add(S,S)))
S2=make([Z,S],[Z,S]); print('*2', vkey(S2), '*+*2', vkey(add(S,S2)))
h=make([number(1)],[number(0)]); print('{1|0}', vkey(h), '{1|0}+{1|0}', vkey(add(h,h)))
print('{0|1}', vkey(make([Z],[number(1)])), '{0,*|1}', vkey(make([Z,S],[number(1)])))
print('1/2+1/2', vkey(add(make([Z],[number(1)]), make([Z],[number(1)]))))
# ±1 + ±1 = 0? no: ±1+±1 = {1|-1}+{1|-1} = 0
pm=make([number(1)],[number(-1)]); print('pm1+pm1', vkey(add(pm,pm)))
# up + star = {0,*|0}
print('up*', vkey(add(UP,S)))
# 3/4 canonical {1/2|1}
print(vkey(make([number(Fr(1,2))],[number(1)])))
# * + 1/2 compare
print(le(S, number(Fr(1,2))), le(number(Fr(1,2)), S), le(UP, number(Fr(1,64))), le(number(0), UP))
# {256|-256} big
print(vkey(make([number(256)],[number(-256)])))
# tiny(2) = {0|{0|-2}}; check tiny > 0 and tiny < up
t=make([Z],[make([Z],[number(-2)])]); print('tiny', vkey(t), le(Z,t) and not le(t,Z), le(t,UP) and not le(UP,t))
