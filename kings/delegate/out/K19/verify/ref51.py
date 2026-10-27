from lg import *
import sys
# White sorties from Kh5 Pa4 kb4 pa5; reply Kxa4
res={}
for q in (True, False):
    row=[]
    for sq in ('g4','g5','g6','h6','a6'):
        G=Game(8,8,True,'b',{7,0,1},queen=q)
        st=parse(f'K{sq} ka4 pa5')
        row.append(G.T(st,None,tmax=12))
    print('White sorties queen=%s'%q, row)
# Black sorties mirror: Y=Kh5 Pa4 kb4 pa5, s=Black, reply Kxa5 by White; A=White, FZ={h,a,b}
for q in (True, False):
    row=[]
    for sq in ('a3','b3','c3','c4','c5'):
        G=Game(8,8,True,'w',{7,0,1},queen=q)
        st=parse(f'Ka5 Pa4 k{sq}')   # white king captured pawn a5 (from h5? no: from b4's mirror) 
        row.append(G.T(st,None,tmax=12))
    print('Black sorties queen=%s'%q, row)
