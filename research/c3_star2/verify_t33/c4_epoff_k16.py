from mysolve import solve_text
for race in ("count","mover","opponent"):
    oc,k,s = solve_text(4,"W: a4 b2 c2 / B: b6 c5 d6 d7",race,False,False,kmax=16)
    print(f"C4 e.p. off, {race}: outcome {oc}, nimber *k with k<16: {k}")
