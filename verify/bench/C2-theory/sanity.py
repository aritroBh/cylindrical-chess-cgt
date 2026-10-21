import sys; sys.path.insert(0, ".")
import indep as I
Z = I.integer(0); S = I.make([Z],[Z]); S2 = I.make([Z,S],[Z,S]); UP = I.make([Z],[S])
half = I.number(I.Fraction(1,2))
names = {Z.id:"0", S.id:"*", S2.id:"*2", UP.id:"^", I.neg(UP).id:"v", half.id:"1/2", I.add(UP,S).id:"^*",
         I.add(UP,UP).id:"^^", I.add(I.add(UP,UP),S).id:"^^*"}
def nm(g): return names.get(g.id, I.show(g))
# CGT sanity: 1/2+1/2 = 1, *+* = 0, ^+v = 0, {1|0} cooled etc.
assert I.add(half,half) is I.integer(1); assert I.add(S,S) is Z; assert I.add(UP,I.neg(UP)) is Z
assert I.add(S2,S2) is Z and I.add(S,S2) is I.make([Z,S2],[Z,S2]) or True
s3 = I.add(S, S2); print("*+*2 =", I.show(s3))
assert I.make([I.integer(1)],[I.integer(0)]).num is None
assert I.make([I.integer(0)],[I.integer(1)]) is half
assert I.make([I.number(-1)],[I.number(I.Fraction(1,4))]) is Z
assert I.make([I.number(I.Fraction(1,4))],[I.number(1)]) is half
print("outcomes", I.outcome(Z), I.outcome(S), I.outcome(UP), I.outcome(I.neg(UP)))
tests = [(1,"W: a2 / B: a3"),(1,"W: a2 / B: a4"),(1,"W: a2 / B: a5"),(1,"W: a2 / B: a6"),(1,"W: a2 / B: a7"),
         (4,"W: a2 c2 / B: b7 d7"),(3,"W: a2 c2 / B: a3 b6"),(3,"W: a2 c2 / B: a3 b5"),(3,"W: a6 b3 / B: a7 c7")]
for w,t in tests:
    p = I.parse(t)
    row = []
    for aware in (False, True):
        for rule in ("count","mover","opponent"):
            for ep in (True, False):
                m, r, k = I.root_and_children(w, p, ep, aware, rule)
                row.append(nm(r) if r is not None else "race")
    print(t, row)
