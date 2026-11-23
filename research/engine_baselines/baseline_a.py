"""Recompute the paper's Table (Stockfish depth vs CGT class) and the agree-only restriction. Offline.
Run from repo root: python3 research/engine_baselines/baseline_a.py
Metric = analyze_sf.py's eval_ok: Stockfish score verdict (win >= +150cp or mate, loss <= -150, else draw)
equals the tablebase root result. Classes from the c5 field of the two EPD files."""
import json, re, math, collections
tb, cls, grp = {}, {}, {}
for path, g in [("engine/suite/cgt_verified.epd", "agree"), ("engine/suite/cgt_disagree.epd", "disagree")]:
    for line in open(path):
        if not line.strip(): continue
        i = re.search(r'id "([^"]+)"', line).group(1)
        tb[i] = re.search(r"tablebase root: (\w+)", line).group(1)
        cls[i] = re.search(r'c5 "class ([^;]+);', line).group(1); grp[i] = g
def verdict(sc):
    k, v = sc.split()[0], int(sc.split()[1])
    return ("win" if v > 0 else "loss") if k == "mate" else "win" if v >= 150 else "loss" if v <= -150 else "draw"
d = json.load(open("engine/runs/sf19_depth.json"))["results"]
depths = [1, 2, 4, 6, 8, 12]
ok = collections.defaultdict(dict)
for r in d:
    ok[int(r["limit"].split()[1])][r["id"]] = r["score"] is not None and verdict(r["score"]) == tb[r["id"]]
assert all(len(ok[x]) == 233 for x in depths)
def wilson(k, n, z=1.96):
    if n == 0: return (float("nan"),) * 2
    p = k / n; den = 1 + z * z / n; c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return 100 * (c - h), 100 * (c + h)
order = ["hot-BIG", "number", "switch", "other-tame", "nimber", "infinitesimal"]
def table(sel, title):
    out = [f"### {title}", "| class | n | " + " | ".join(f"d{x}" for x in depths) + " | Wilson95 d1 | Wilson95 d2 |", "|" + "---|" * (len(depths) + 4)]
    for c in order + ["ALL (excl. decided)"]:
        ids = [i for i in tb if sel(i) and cls[i] != "decided" and (c.startswith("ALL") or cls[i] == c)]
        n = len(ids)
        cells = []; ci = []
        for x in depths:
            k = sum(ok[x][i] for i in ids); cells.append(f"{100*k/n:.0f} ({k})" if n else "-")
            if x in (1, 2): lo, hi = wilson(k, n); ci.append(f"{lo:.0f}-{hi:.0f}")
        out.append(f"| {c} | {n} | " + " | ".join(cells) + " | " + " | ".join(ci) + " |")
    return "\n".join(out)
print("class counts all 233:", dict(collections.Counter(cls.values())), " groups:", dict(collections.Counter(grp.values())))
print("class x group:", dict(collections.Counter((grp[i], cls[i]) for i in tb)))
t1 = table(lambda i: True, "Full suite (226 excl. 7 decided) - paper Table")
t2 = table(lambda i: grp[i] == "agree", "Agree-only (verified) positions, decided excluded")
t3 = table(lambda i: grp[i] == "disagree", "Disagree-only positions, decided excluded (context)")
print(t1); print(t2); print(t3)
open("research/engine_baselines/baseline_a_tables.md", "w").write("\n\n".join([t1, t2, t3]) + "\n")
