import sys
def roots(W,B,pawns):
    for w in W:
        for b in B:
            for s in "wb":
                print(f"K{w} k{b} {pawns} {s} -")
name=sys.argv[1]
if name=="zb": roots(["b2","c3"],["a4","b5"],"Pa3 Pb4 pb3 pc4")
if name=="zbm": roots(["a3","b2"],["b5","c4"],"Pb4 Pc3 pa4 pb3")
if name=="zc": roots(["c2","c3"],["a4","a5"],"Pa2 Pc4 pa3 pc5")
if name=="zcm": roots(["a2","a3"],["c4","c5"],"Pa4 Pc2 pa5 pc3")
