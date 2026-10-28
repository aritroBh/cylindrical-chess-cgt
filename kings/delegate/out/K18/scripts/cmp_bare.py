#!/usr/bin/env python3
"""relation between the local game (lg --dumpbare) and bare kpsolve P values of the position after the sortie (Black to move)."""
import collections
bits = {}
for l in open("logs/bare_c8x6_f3_22.txt"):
    p, b = l.rstrip("\n").split(" | ")
    bits[p] = tuple(int(x) for x in b.split())
res = {}
for l in open("logs/bare_out.txt"):
    if " | " not in l: continue
    p, r = l.rstrip("\n").split(" | ")
    res[p] = r.split()[0]   # exact (frozen-free P model: both bounds equal at cap 0)
cnt = collections.Counter(); viol = []
names = ["plain/P", "plain/Q", "pass/P", "pass/Q"]
for p, b in bits.items():
    r = res.get(p)
    if r is None: continue
    for i in range(4):
        win = b[i] or (b[4] if i % 2 == 0 else b[5])
        cnt[(names[i], "local win" if win else "no local win", "kpp:" + r)] += 1
        if win and r != "L": viol.append((p, names[i], r))
for k in sorted(cnt): print(k, cnt[k])
print("violations of 'local win => bare P Black win':", len(viol)); print(viol[:10])
