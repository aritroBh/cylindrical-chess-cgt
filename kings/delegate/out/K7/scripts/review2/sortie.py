from kb import B
from cert import Cert
Bd=B(8,8,True); C=Cert(Bd,[7,0,1])
for sort in ["g4","g5","g6","h6","a6"]:
    # after Kxa4: white king on sortie square, black king a4, black pawn a5, white to move
    pos=Bd.parse(f"K{sort} ka4 pa5 w -")
    Ts=[C.minT(pos,9,qs=False), C.minT(pos,9,qs=True)]
    print(sort, "T (L1_P, L1)", Ts, "mu_s(no ctx pawns)", C.mu(pos))
