import sys; sys.path.insert(0,'.')
from vlg import *
B=Board(8,8,True,[7,0,1])
# 5.1: Y = Kh5 Pa4 / Kb4 Pa5 ; White sorties Kg4 Kg5 Kg6 Kh6 Ka6; Black replies Kxa4
for qc in (True,False):
  for mv in ['g4','g5','g6','h6','a6']:
    Q=parse(B,'K%s kb4 Pa4 pa5'%mv)   # position after sortie, before reply
    # reply Kxa4: black king b4 takes a4
    q=parse(B,'K%s ka4 pa5'%mv)
    G=Game(B,0,qc)
    print(qc,mv,G.least_T(q,None),len(G.memo))
