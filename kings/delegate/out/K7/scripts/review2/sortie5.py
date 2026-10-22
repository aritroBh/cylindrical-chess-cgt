import time
from hc import Geo, Cert
g=Geo(8,8,True); C=Cert(g,[7,0,1])
# 5.1: WK h5, WP a4, BK b4, BP a5 (8-file cylinder, 8 ranks).  Sorties of White: Kg4,Kg5,Kg6,Kh6,Ka6.  reply Kxa4
for name in ["Kg4","Kg5","Kg6","Kh6","Ka6"]:
    Q=g.parse(f"{name} ka4 pa5 w -")
    assert g.legal(Q), name
    t0=time.time()
    r=[C.L1_T(Q,qc,8) for qc in (False,True)]
    print(name, "T(L1_P),T(L1 queen)=",r, "%.0fs"%(time.time()-t0), flush=True)
