# random terminal-free T: Theorem 2, Proposition 3, Theorem 4 (third item) and the two-type pattern (Conjecture 7), vk.c
import sys, random, subprocess
def run(W, H, t, extra=()):
    d = {}
    for l in subprocess.run(["./vk", str(W), str(H), t, *extra], capture_output=True, text=True).stdout.split("\n"):
        if l:
            a = l.split(); d[(a[0], a[1], a[2], a[3])] = a[4]
    return d
def onT(nodes):  # Left wins on (+) T: returns dict (t, 'L'/'R') -> bool
    n = len(nodes); win = set(); ch = True
    while ch:
        ch = False
        for t in range(n):
            L, R = nodes[t]
            if (t, "L") not in win and ((t, "R") in win or any((u, "R") in win for u in L)): win.add((t, "L")); ch = True
            if (t, "R") not in win and all((u, "L") in win for u in R): win.add((t, "R")); ch = True
    return win
def reserve(nodes):
    S = set(range(len(nodes))); ch = True
    while ch:
        ch = False
        for t in list(S):
            L, R = nodes[t]
            if not any(u in S for u in R) or any(u not in S for u in L): S.discard(t); ch = True
    return S
W, H, NTRIAL, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
rng = random.Random(seed)
Z = run(W, H, "t/zero.t"); D = run(W, H, "t/dud.t"); ZO = run(W, H, "t/zoff.t"); ZD = run(W, H, "t/zdud.t")
typ = {}
for k in Z:
    if Z[k] == "W" and D[k] != "W":
        typ[k] = {("W", "W"): "L", ("D", "D"): "R"}.get((ZO[k], ZD[k]), "?")
v2 = v3 = v4 = v7 = nT = nres = nsep = 0
for trial in range(NTRIAL):
    n = rng.randint(1, 4)
    nodes = [([rng.randrange(n) for _ in range(rng.randint(0, 2))], [rng.randrange(n) for _ in range(rng.randint(0, 2))]) for _ in range(n)]
    with open("t/rand.t", "w") as f:
        f.write(f"{n}\n")
        for i, (L, R) in enumerate(nodes):
            f.write(f"n{i} {len(L)} {' '.join(map(str, L))} {len(R)} {' '.join(map(str, R))}\n")
    win = onT(nodes); S = reserve(nodes); Rr = run(W, H, "t/rand.t"); nT += 1
    if 0 in S: nres += 1
    if ((0, "L") in win) != ((0, "R") in win): nsep += 1
    for k, r in Rr.items():
        wk, p, bk, s = k
        if Z[k] == "W":
            if s == "b" and (0, "R") in win and r != "W": v2 += 1
            if s == "w":
                twin = (wk, p, bk, "b")
                if ((0, "R") in win or (Z.get(twin) == "W" and any((u, "R") in win for u in nodes[0][0]))) and r != "W": v2 += 1
        if 0 in S and D[k] != "W" and r != "D": v3 += 1
        if Z[k] != "W" and r != "D": v4 += 1
        if k in typ:
            pred = "W" if (0, typ[k]) in win else "D"
            if typ[k] == "?" or r != pred: v7 += 1
print(f"cyl:{W}x{H} seed {seed}: {nT} random T ({nres} with root in a Right reserve, {nsep} separating (on,L) from (on,R)); "
      f"violations: Thm 2 {v2}, Prop 3 {v3}, Thm 4(iii) {v4}, two-type (type read from {{0|off}}, {{0|dud}}) {v7}; ON positions {len(typ)}, untyped {sum(1 for v in typ.values() if v == '?')}")
