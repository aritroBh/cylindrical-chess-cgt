import sys
sys.path.insert(0,'..')
from kpgen import Board
from lc import Cert
B=Board(8,8,True); C=Cert(B,[7,0,1])   # F_Z = h,a,b
sq=B.sq
# 5.1: WK h5, WP a4, BK b4, BP a5.  White (s) sorties; Black (s-bar) replies Kxa4 (king capture of Z-pawn). Q: White to move.
for wk in ['g4','g5','g6','h6','a6']:
    Q=(sq(wk),sq('a4'),frozenset(),frozenset([sq('a5')]),0,-1)   # after ...Kxa4, White to move
    print(wk, B.legal_pos(Q), "T(P-version)",C.L1(Q,False,9),"T(queen-safe)",C.L1(Q,True,9))
# mirror: Black sorties, White punishes: BK b4 -> sorties; WK h5 captures a5: Kxa5
for bk in ['a3','c3','c4','c5','b5']:
    Q=(sq('a5'),sq(bk),frozenset([]),frozenset(),1,-1)
    # white pawn a4 is captured? In the mirror, Black's pawn a5 is captured by WK; White pawn a4 remains
    Q=(sq('a5'),sq(bk),frozenset([sq('a4')]),frozenset(),1,-1)
    print("black sortie",bk, B.legal_pos(Q), "T",C.L1(Q,False,9),"Tsafe",C.L1(Q,True,9))
