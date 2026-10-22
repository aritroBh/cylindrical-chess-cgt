from kb import B
from cert import Cert
Bd=B(7,6,True); C=Cert(Bd,[0,1,2])
for t in ["Kf5 kc6 Pe3 pb3 w -","Kf5 kc6 Pe3 pb3 w -"]:
    Q=Bd.parse(t); print(t, "minT",C.minT(Q,6), "mu",C.mu(Q), [ (T,C.L3(Q,T)) for T in (2,3)])
