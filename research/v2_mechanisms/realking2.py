"""Cap-2 pilot: a SUBSET of the real-king roots (argv[2] = comma-separated indices into realking_cap1.json roots),
root + all pawn-move children in ONE kpsolve process (layers shared).  Usage: python3 -I realking2.py 2 0,5,7 2"""
import sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms")
import realking as rk
idx = [int(i) for i in sys.argv[2].split(",")]
cap1 = json.load(open(rk.HERE + "realking_cap1.json"))
lines, meta = [], []
for i in idx:
    d = cap1["roots"][i]
    pos = rk.G.parse(d["P"])
    root = "Pa3 pa4 Kg4 kb3 " + " ".join(["P" + rk.pg.nm((f + 3, r)) for f, r in sorted(pos[0])] + ["p" + rk.pg.nm((f + 3, r)) for f, r in sorted(pos[1])]) + f" {d['side']} -"
    ch = {m: rk.apply(root, m) for m in d["moves"] if m[0] == "P"}
    lines += [root] + list(ch.values())
    meta.append((i, d, root, ch))
res, log, peak, secs = rk.run_kp(lines, "realking_cap2_pilot")
out = dict(cap=rk.CAP, log=log, peak_rss_mb=peak, seconds=secs, roots=[])
print(log, peak, secs, flush=True)
for i, d, root, ch in meta:
    a, b, mv = res[root]
    e = dict(idx=i, P=d["P"], side=d["side"], real=(a, b), frozen=d["frozen"], moves=mv, children={})
    for m, line in ch.items():
        a2, b2, mv2 = res[line]
        e["children"][m] = dict(line=line, value=(a2, b2), replies=mv2)
    out["roots"].append(e)
    print("\n==", d["P"], "mover", d["side"], "real", (a, b), "frozen", d["frozen"], "\n  root moves:", mv)
    for m, c in e["children"].items():
        print("  after", m, c["value"], c["replies"])
json.dump(out, open(rk.HERE + "realking_cap2_pilot.json", "w"), indent=1)
