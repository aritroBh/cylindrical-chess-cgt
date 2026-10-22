from hc import *
g=Geo(7,6,True); C=Cert(g,[0,1,2])
Q=g.parse("Kf6 kb1 Pc2 Pf2 Pf3 pa3 pf4 pe5 w -")
print(C.L1_T(Q,False,6), C.mu(Q,8,True))
for T in (5,6): print(T, C.L3(Q,T,False))
