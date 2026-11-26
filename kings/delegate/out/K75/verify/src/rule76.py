"""K76 referee: test K75's rule (R1), (R2), (R3) and simple alternatives on the per-pair recount logs/compare_11.txt
(written by cmp76.py from p74's values and my own distances and prediction).

Usage (repository root):  python3 -I kings/delegate/out/K75/verify/src/rule76.py logs/compare_11.txt
dB below means min(dA, dB), the nearer shuttle square, as in K75.
"""
import re, sys

rows = []
for l in open(sys.argv[1]):
    m = re.match(r"(C\d+_\d+) (\w) 1\+1 (\w+)\s+dW(\d+) dA(\d+) dB(\d+)\s+(\d+)/(\d+)\s+kind (\S+)", l)
    if m:
        g, f, cls, dW, dA, dB, a, fl, k = m.groups()
        rows.append(dict(g=g, f=f, cls=cls, dW=int(dW), dB=min(int(dA), int(dB)), fail=int(fl),
                         W="W" in k, B="B" in k))
P = lambda r: f"{r['g']} {r['f']} (dW {r['dW']}, dB {r['dB']}, {r['cls']}, {r['fail']} failing, kind " \
              f"{'B' if r['B'] else ''}{'W' if r['W'] else ''}{'-' if r['fail'] == 0 else ''})"
print(len(rows), "pairs;", sum(r["fail"] == 0 for r in rows), "clean;", sum(r["fail"] for r in rows), "failing contexts")
print("\n(R1) White-favour failures in every pair with dW <= 3:")
s = [r for r in rows if r["dW"] <= 3]
print(f"  {len(s)} pairs with dW <= 3; without a White-favour failure: {[P(r) for r in s if not r['W']]}")
print("  White-favour failures with dW >= 4:", [P(r) for r in rows if r["dW"] >= 4 and r["W"]])
print("\n(R2) Black-favour failures in every pair with dB <= 4:")
s = [r for r in rows if r["dB"] <= 4]
print(f"  {len(s)} pairs with dB <= 4; without a Black-favour failure: {[P(r) for r in s if not r['B']]}")
s = [r for r in rows if r["dB"] >= 5 and r["B"]]
print(f"  Black-favour failures with dB >= 5: {len(s)}; with dW <= 4 among them: {[P(r) for r in s if r['dW'] <= 4]}")
print("  pairs with dB >= 5 and dW >= 5:", sum(1 for r in rows if r["dB"] >= 5 and r["dW"] >= 5))
print("\n(R3) clean only if dW >= 4 and dB >= 5; clean pairs violating it:",
      [P(r) for r in rows if r["fail"] == 0 and not (r["dW"] >= 4 and r["dB"] >= 5)])
for lo in (4, 5):
    s = [r for r in rows if r["dW"] == 4 and r["dB"] >= 5] if lo == 4 else [r for r in rows if r["dW"] >= 5 and r["dB"] >= 5]
    print(f"  cell {'dW = 4' if lo == 4 else 'dW >= 5'}, dB >= 5: {len(s)} pairs, clean {sum(r['fail'] == 0 for r in s)}:",
          [P(r) for r in s])
print("\nclean pairs:", [P(r) for r in rows if r["fail"] == 0])
print("\nnecessary conditions tried (clean pairs violating each):")
for nm, c in [("dW + dB >= 8", lambda r: r["dW"] + r["dB"] >= 8), ("dW + dB >= 10", lambda r: r["dW"] + r["dB"] >= 10),
              ("min(dW, dB) >= 4", lambda r: min(r["dW"], r["dB"]) >= 4), ("dW >= 4", lambda r: r["dW"] >= 4)]:
    sat = [r for r in rows if c(r)]
    print(f"  {nm}: clean violating {[P(r) for r in rows if r['fail'] == 0 and not c(r)]}; "
          f"pairs satisfying it {len(sat)}, clean among them {sum(r['fail'] == 0 for r in sat)}")
print("\ncells (dW, dB): clean/total")
cells = {}
for r in rows: cells.setdefault((r["dW"], r["dB"]), []).append(r)
for k in sorted(cells):
    c = cells[k]
    print(f"  {k}: {sum(r['fail'] == 0 for r in c)}/{len(c)}  " + ", ".join(f"{r['g']} {r['f']}:{r['fail']}" for r in c))
