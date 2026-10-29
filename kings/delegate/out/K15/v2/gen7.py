#!/usr/bin/env python3
"""K15 v2: confirmation inputs for the dud_D-type groups on cyl:7x6 (group on files a-c, buffer d and g, context pawns on ONE of the files e, f).
D-model prediction G (+) dud_D by confirm.solve_d (Theorem 3.4(a), brute force).  Writes v2/conf7/g<i>.in and v2/conf7/rows.json."""
import sys, json, random, os
sys.path.insert(0, 'conf'); sys.path.insert(0, '.')
import confirm as c
random.seed(7615)
H = 6
groups = [("Z_B", "Kb2 ka4 Pa3 Pb4 pb3 pc4"), ("D2", "Ka1 ka4 Pb4 Pc3 pb3 pc4"),
          ("D2m", "Ka1 ka6 Pa3 Pb4 pa4 pb3"), ("D3", "Ka1 ka6 Pa3 Pb4 Pc3 pa4 pb3 pc4")]
named = {"C0_empty": ([], []), "C1_blocked_e3e4": (["e3"], ["e4"]), "C2_onemove_e3e5": (["e3"], ["e5"]),
         "C3_gap2_e2e5": (["e2"], ["e5"])}
ctx = dict(named); tries = 0
while len(ctx) < 12 and tries < 1000:
    tries += 1
    f = random.choice("ef"); nw = random.randint(0, 2); nb = random.randint(0, 2)
    if nw + nb == 0 or nw + nb > 3: continue
    sel = random.sample([f"{f}{r}" for r in range(2, 6)], nw + nb)
    wl = sorted(sel[:nw]); bl = sorted(sel[nw:])
    ctx["R_" + "".join(wl) + "_" + "".join(bl)] = (wl, bl)
os.makedirs('v2/conf7', exist_ok=True)
rows = []
for gi, (gname, grp) in enumerate(groups):
    toks = [t for t in grp.split() if len(t) >= 3]; lines = []; gr = []
    for cname, (cw, cb) in ctx.items():
        pw, pb = c.solve_d(H, [c.sq(x) for x in cw], [c.sq(x) for x in cb], "dud")
        ct = [f"P{x}" for x in cw] + [f"p{x}" for x in cb]
        for stm, pred in (("w", pw), ("b", pb)):
            p = " ".join(toks + ct) + f" {stm} -"
            lines.append(p); gr.append({"gname": gname, "group": grp, "ctx": cname, "stm": stm, "pos": p, "pred": pred})
    open(f'v2/conf7/g{gi}.in', 'w').write("\n".join(lines) + "\n"); rows.append(gr)
json.dump(rows, open('v2/conf7/rows.json', 'w'))
print([len(r) for r in rows], list(ctx))
