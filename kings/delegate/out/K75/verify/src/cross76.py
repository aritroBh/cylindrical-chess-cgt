"""K76 referee: compare every K75 per-pair table (1 + 1, 2 + 2, 3 + 3) with p74's values from my runs, whichever run
covers the positions (the 1 + 1 run, or a larger run of the same pair: values do not depend on the other positions).

Usage (repository root):  python3 -I kings/delegate/out/K75/verify/src/cross76.py K75RAW
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mk76, cmp76

raw = sys.argv[1]
have = {}
for x in os.listdir(f"{cmp76.V}/logs/runs"):
    t = x[:-4]
    base = t[:11] if len(t) > 11 and t[11] == "p" else t
    have.setdefault(base[:9], set()).add(base)
G = mk76.groups(); F = mk76.load_freezes()
tot = mis = 0
for fn in sorted(os.listdir(raw)):
    if not fn.endswith("_table.txt"): continue
    g, f, nn = fn[:7], fn[8], fn[10:12]
    k = cmp76.read_k75(raw, g, f, int(nn[0]))
    vals = {}
    for base in sorted(have.get(f"{g}_{f}", ())):
        vals.update(cmp76.read_p74(base))
    n = m = 0
    for name, (kp, kr, kpred, _) in k.items():
        ws, bs = cmp76.ctx_of(name, f)
        ps = mk76.positions(G, F, g, f, ws, bs)
        if not all(p in vals for p in ps): continue
        P = [vals[p] for p in ps]
        n += 8; m += sum(a != b for a, b in zip(P, kp)) + sum(a != b for a, b in zip(P, kr))
    print(f"{g} {f} {nn}: K75 contexts {len(k)}, positions compared {n}, disagreements with pk or ref3m {m}")
    tot += n; mis += m
print("TOTAL positions compared", tot, "disagreements", mis)
