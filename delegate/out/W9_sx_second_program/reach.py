import sx2
X = sx2.parse("b2 d4 g3 h5 / a7 c7 f7 g4")
seen = {X}; stack = [X]; multi = []
while stack:
    w, b = stack.pop()
    for side in (0, 1):
        for (w2, b2) in sx2.moves(w, b, side):
            w2, b2 = tuple(sorted(w2)), tuple(sorted(b2))
            if sx2.verdict(w2, b2, side) is not None or (w2, b2) in seen: continue
            seen.add((w2, b2)); stack.append((w2, b2))
for (w, b) in seen:
    if len(sx2.split(w, b)) > 1: multi.append((w, b))
print("positions reachable with no passed pawn (either side, any order):", len(seen))
print("of these with >= 2 components:", len(multi))
# threats per component: can a side get a passed pawn by moves inside the component, no earlier passed pawn
from functools import lru_cache
@lru_cache(None)
def threats(comp):
    w, b = comp; res = set(); seenc = {comp}; st = [comp]
    while st:
        w, b = st.pop()
        for side in (0, 1):
            for (w2, b2) in sx2.moves(w, b, side):
                w2, b2 = tuple(sorted(w2)), tuple(sorted(b2))
                wp, bp = sx2.passed_side(w2, b2, 0), sx2.passed_side(w2, b2, 1)
                if wp: res.add(0)
                if bp: res.add(1)
                if not wp and not bp and (w2, b2) not in seenc:
                    seenc.add((w2, b2)); st.append((w2, b2))
    return frozenset(res)
opp = [p for p in multi if any(0 in threats(c) and 1 in threats(d) for c in sx2.split(*p) for d in sx2.split(*p) if c is not d)]
print("two components with opposite threats (one carries a White threat, a different one a Black threat):", len(opp))
fmt = lambda p: " ".join("abcdefgh"[f]+str(r) for f, r in p[0]) + " / " + " ".join("abcdefgh"[f]+str(r) for f, r in p[1])
print("root is", len(sx2.split(*X)), "component(s); example:", fmt(opp[0]) if opp else None)
