from kb import B
from cert import Cert
Bd=B(7,6,True); C=Cert(Bd,[0,1,2])
for t in ["Kd6 kc4 Pe3 pa4 pe4 pf3 w f4","Kd6 kc4 Pe3 pa4 pe4 pf3 w -","Kd6 kc2 pa3 Pe4 pe5 pf5 w -","Kb5 kd5 Pb4 Pc5 pe2 b -","Ke6 ka1 Pc4 pb3 pc5 w -","Kb5 kd5 Pb4 Pc5 Pe3 Pf3 Pf4 Pf5 b -"]:
    Q=Bd.parse(t); mT=C.minT(Q,7)
    print(t, "minT",mT, "mu_ep",C.mu(Q,True), "mu_noep",C.mu(Q,False), {T:C.L3(Q,T) for T in range(mT or 1,(mT or 1)+3)})
