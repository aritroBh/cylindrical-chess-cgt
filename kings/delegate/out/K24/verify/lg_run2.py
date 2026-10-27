import sys
import psolve, lg2
from psolve import setup
def sqn(n): return (int(n[1:])-1)*psolve.W + ord(n[0])-97
for board in ("cyl:8x8",):
    setup(board)
    print("== 5.1 White sorties (s=White), reply Kxa4: Q = WK sortie square, bk a4, bp a5; F_Z = hab")
    for sk in ("g4","g5","g6","h6","a6"):
        for clause in (1,0):
            T = lg2.run(board, sqn(sk), sqn("a4"), sqn("a5"), "hab", clause)
            print(f"  K{sk} clause={clause}: Tmin={T[0]} stalemates_on_winning_lines={T[1]} s-nodes={T[2]}")
for board in ("cyl:8x8","flat:8x8"):
    setup(board)
    print("== 7.2 White sorties (s=White), reply Kxd7: bk d7, bp e7; F_Z = de ;", board)
    for sk in ("d5","e5","f5","f7"):
        for clause in (1,0):
            T = lg2.run(board, sqn(sk), sqn("d7"), sqn("e7"), "de", clause)
            print(f"  K{sk} clause={clause}: Tmin={T[0]} stale={T[1]} s-nodes={T[2]}")
# 6-rank analogue Z_72: Kc4 Pb5 kb6 pc5 ; White sorties Kb3 Kc3 Kd3 Kd5, reply Kxb5: bk b5, bp c5 ; F_Z = bc
setup("cyl:7x6")
print("== P5 Z_72 on cyl:7x6 White sorties, F_Z = bc")
for sk in ("b3","c3","d3","d5"):
    for clause in (1,0):
        T = lg2.run("cyl:7x6", sqn(sk), sqn("b5"), sqn("c5"), "bc", clause)
        print(f"  K{sk} clause={clause}: Tmin={T[0]} stale={T[1]} s-nodes={T[2]}")
