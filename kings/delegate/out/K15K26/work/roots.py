import sys
def roots(W,B,pawns):
    for w in W:
        for b in B:
            for s in "wb":
                print(f"K{w} k{b} {pawns} {s} -")
n=sys.argv[1]
if n=="zc88": roots(["c3","c4"],["a5","a6"],"Pa3 Pc5 pa4 pc6")
if n=="k15_22_88": roots(["c3"],["a5"],"Pa3 Pc5 pa4 pc6")
if n=="zc86": roots(["c2","c3"],["a4","a5"],"Pa2 Pc4 pa3 pc5")
if n=="d2_86": roots(["a1"],["a4"],"Pb4 Pc3 pb3 pc4")
