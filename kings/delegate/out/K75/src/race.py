"""K75: race times of each group (a candidate quantity for the rule of question 3; COMPUTED-1, pk_sum only).

tau_W(m) = for a non-shuttle Black root move m, the least r >= 1 such that x_m (White to move) is a White win beside
           B_r, a chain of r Black moves ending in a Black terminal win (Black "promotes in r moves" elsewhere): the
           speed of White's punishment of m in tempi (KMAX + 1 = not a White win even beside B_KMAX).
tau_B(w) = for a non-freeze White move w at a root or any White move at a q, the least r >= 1 such that the position
           after w (Black to move) is a Black win beside W_r (White's chain of r moves to a White terminal win).
r = 0 is the bare board.  Per group the file logs/race.txt lists every move.
Usage (repository root):
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K75/src/race.py gen LOG65 LOG67  -> in/race.pos, in/race.lab
  bin/pk_sum -T "<chain>" < in/race.pos > logs/race.out     (the chain is printed by 'gen' on stderr)
  PYTHONDONTWRITEBYTECODE=1 .venv/bin/python kings/delegate/out/K75/src/race.py read OUTDIR           -> logs/race.txt
T state 0: no options; state j (1..KMAX) is B_j (Black option to B_(j-1), B_1 to a Black terminal); state KMAX + j is W_j.
Positions come from ax65's Definition 4.8 logs (the moves listed with P(after)); a move is applied by hand here
(king or pawn, capture by landing, e.p. right after a White double step if a Black pawn stands beside).
"""
import re, sys, os
V = "kings/delegate/out/K75"
KMAX = 12

def apply(pcs, mv, side):
    """pcs: dict square -> piece letter; mv like 'Kc5b4', 'ke5f6', 'Pf2f4'"""
    p, a, b = mv[0], mv[1:3], mv[3:5]
    d = dict(pcs); assert d.get(a) == p, (pcs, mv)
    del d[a]; d.pop(b, None); d[b] = p
    ep = "-"
    if p == "P" and int(b[1]) - int(a[1]) == 2:
        for df in (-1, 1):
            if d.get(chr(ord(b[0]) + df) + b[1]) == "p": ep = a[0] + str(int(a[1]) + 1)
    return d, ep

def fmt(d):
    order = {"K": 0, "k": 1, "P": 2, "p": 3}
    return " ".join(p + s for s, p in sorted(d.items(), key=lambda x: (order[x[1]], x[0])))

def todict(s): return {t[1:]: t[0] for t in s.split()}

if sys.argv[1] == "gen":
    names = [l.split("|")[0] for l in open(f"{V}/in/groups48.txt") if not l.startswith("#")]
    out = []
    for nm in names:
        fn = os.path.join(sys.argv[2], nm + ".out")
        if not os.path.exists(fn) or nm.startswith("C014") or nm.startswith("C034"):
            fn = os.path.join(sys.argv[3], nm + ".out")
        t = open(fn).read().splitlines()
        root = None
        for l in t:
            m = re.match(r"root (.*) ([bw]) - :", l)
            if m: root = (todict(m.group(1)), m.group(2)); continue
            m = re.match(r"\s+q = |\s+freeze P\w+ at \w+ -> q = (.*) b -", l)
            if m and m.group(1): q = todict(m.group(1)); continue
            m = re.match(r"\s+q White to move: .*\[ (.*) \]", l)
            if m:
                for x in m.group(1).split():
                    mv = x.split("=")[0]; d, ep = apply(q, mv, 0)
                    for k in range(KMAX + 1): out.append((f"{nm} W q {mv} {k}", f"{fmt(d)} b {ep} {0 if k == 0 else KMAX + k}"))
                continue
            m = re.match(r"\s+(\w\w\d\w\d)\s+P\(after\)=(\w)(.*)", l)
            if m and root and root[1] == "w" and m.group(1)[0] in "KP" and "FREEZE" not in m.group(3):
                d, ep = apply(root[0], m.group(1), 0)
                for k in range(KMAX + 1): out.append((f"{nm} W root {m.group(1)} {k}", f"{fmt(d)} b {ep} {0 if k == 0 else KMAX + k}"))
            m = re.match(r"B1 (\S+)\s+x_m = (.*) w (\S+) :", l)
            if m:
                for k in range(KMAX + 1): out.append((f"{nm} B {m.group(1)} {k}", f"{m.group(2)} w {m.group(3)} {k}"))
    with open(f"{V}/in/race.pos", "w") as fp, open(f"{V}/in/race.lab", "w") as fl:
        prev = None
        for lab, pos in out:            # one problem per group (blank line between groups)
            g = lab.split()[0]
            if prev and g != prev: fp.write("\n")
            prev = g; fp.write(pos + "\n"); fl.write(lab + "\n")
    ch = ["/"] + ["/B"] + [f"/{j - 1}" for j in range(2, KMAX + 1)] + ["W/"] + [f"{KMAX + j - 1}/" for j in range(2, KMAX + 1)]
    print(f'{2 * KMAX + 1}|' + ";".join(ch), file=sys.stderr)
else:
    # outputs per group: OUTDIR/gNN.out (NN = index of the group in in/groups48.txt), as written by slack.sh
    outdir = sys.argv[2]
    names = [l.split("|")[0] for l in open(f"{V}/in/groups48.txt") if not l.startswith("#")]
    lab0 = ["# " + l for l in open(f"{V}/in/race.lab").read().splitlines()]
    lab, vals = [], []
    for i, nm in enumerate(names):
        fn = f"{outdir}/g{i:02d}.out"
        if not os.path.exists(fn): continue
        mine = [L for L in lab0 if L.split()[1] == nm]
        v = [l for l in open(fn).read().splitlines() if l.strip()]
        if len(v) != len(mine): print("incomplete", nm, file=sys.stderr); continue
        lab += mine; vals += v
    res = {}
    for L, v in zip(lab, vals):
        _, nm, side, *mv, k = L.split()
        r = v.split()[-3] if "(configs" in v else v.split()[-1]
        ok = (r == "W") if side == "B" else (r == "L")
        res.setdefault((nm, side), {}).setdefault(" ".join(mv), {})[int(k)] = ok
    with open(f"{V}/logs/race.txt", "w") as fh:
        fh.write(f"# group tau_W tau_B (maxima over the moves = the slowest punishment; KMAX {KMAX}; per move: the least r at which the punisher wins, KMAX+1 = not at KMAX)\n")
        for nm in dict.fromkeys(k[0] for k in res):
            s = {}
            for side in "BW":
                per = {}
                for mv, d in res.get((nm, side), {}).items():
                    # tau = the least chain length r >= 1 at which the punisher wins (KMAX + 1: not even at KMAX);
                    # the punishment needs tau - 1 tempi more than the opponent's race... see the docstring
                    ok = [k for k in range(1, KMAX + 1) if d.get(k)]
                    per[mv] = ok[0] if ok else KMAX + 1
                    assert all(d.get(k) for k in range(per[mv], KMAX + 1)), (nm, mv, d)   # monotone in r
                s[side] = (max(per.values()), per)
            fh.write(f"{nm} {s['B'][0]} {s['W'][0]}  B: {s['B'][1]}  W: {s['W'][1]}\n")
