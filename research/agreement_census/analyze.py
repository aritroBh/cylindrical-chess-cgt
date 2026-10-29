"""Census analysis: model (cylcgt) vs exact kpsolve vs frozen kpsolve. Writes census.tsv, summary tables (summary.md, summary.json).
Usage: python3 -I analyze.py"""
import json, math, os, glob, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
PRED = {"L": ("W","W"), "R": ("L","L"), "N": ("W","L"), "P": ("L","W")}
INV = {v: k for k, v in PRED.items()}

def wilson(k, n, z=1.96):
    if n == 0: return (float("nan"),) * 2
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return max(0, c-h), min(1, c+h)

def load(d, tag):
    f = f"{d}/out_{tag}.txt"
    if not os.path.exists(f) or not os.path.exists(f"{d}/status_{tag}.txt"): return None
    if "exit 0" not in open(f"{d}/status_{tag}.txt").read(): return None
    res = {}
    for l in open(f):
        pos, rest = l.split("|")[0].strip(), l.split("|")[1].split()
        res[pos] = (rest[0], rest[1])
    return res

def side(r):  # (A,B) bounds -> exact value or None (X = illegal side to move is not a value)
    return r[0] if (r[0] == r[1] and r[0] != "X") else None

rows_out = []
for d in sorted(glob.glob(f"{HERE}/work/*/")):
    d = d.rstrip("/")
    if not os.path.exists(f"{d}/meta.json"): continue
    meta = json.load(open(f"{d}/meta.json")); rows = [json.loads(l) for l in open(f"{d}/rows.jsonl")]
    frozen = load(d, "F")
    mode = "ext3" if d.endswith("_x3") else "le2"
    for tag, promo, cap in (("Q2", "Q", 2), ("QRBN2", "QRBN", 2), ("Q1", "Q", 1), ("QRBN1", "QRBN", 1)):
        real = load(d, tag)
        if real is None: continue
        for r in rows:
            rw, rb = real[r["wtm"]], real[r["btm"]]
            ex = side(rw) is not None and side(rb) is not None
            fz = None
            if frozen:
                a, b = frozen[r["wtm"]], frozen[r["btm"]]
                fz = (a[0], b[0]) if side(a) and side(b) else None
            got = (side(rw), side(rb)) if ex else None
            rc = INV.get(got, "draw/other" if got else None) if got else None
            illegal = "X" in (rw[0], rb[0])
            if illegal: verdict = "illegal-side"
            elif r["model_class"] == "race": verdict = "race"
            elif not ex: verdict = "undetermined"
            else: verdict = "match" if got == PRED[r["model_class"]] else "MISMATCH"
            cause = ""
            if verdict == "MISMATCH":
                pred = PRED[r["model_class"]]
                if fz is None: cause = "no-frozen"
                elif fz == pred: cause = "king_effect"
                else: cause = "convention" + ("" if fz == got else "+king")
            rows_out.append(dict(board=meta["board"], layout=meta["layout"], mode=mode, promo=promo, cap=cap, P=r["P"], nw=r["nw"], nb=r["nb"],
                model_value=r["model_value"], model_class=r["model_class"], real_wtm="/".join(rw), real_btm="/".join(rb), exact=ex,
                real_class=rc, frozen_wtm=fz[0] if fz else "", frozen_btm=fz[1] if fz else "", verdict=verdict, cause=cause,
                real_has_draw=bool(got and "D" in got), side_w=side(rw) or "", side_b=side(rb) or ""))
cols = list(rows_out[0].keys())
with open(f"{HERE}/census.tsv", "w") as fh:
    fh.write("\t".join(cols) + "\n")
    for r in rows_out: fh.write("\t".join(str(r[c]) for c in cols) + "\n")

def cell(rs):
    m = sum(r["verdict"] == "match" for r in rs); mm = sum(r["verdict"] == "MISMATCH" for r in rs)
    n = m + mm; lo, hi = wilson(m, n)
    return dict(rows=len(rs), race=sum(r["verdict"] == "race" for r in rs), illegal=sum(r["verdict"] == "illegal-side" for r in rs), undet=sum(r["verdict"] == "undetermined" for r in rs),
                match=m, mismatch=mm, acc=(m/n if n else None), lo=lo, hi=hi,
                king=sum(r["cause"] == "king_effect" for r in rs), conv=sum(r["cause"].startswith("convention") for r in rs),
                draws=sum(1 for r in rs if r["verdict"] == "MISMATCH" and r["real_has_draw"]))
def fmt(c):
    if c["acc"] is None: return f"{c['rows']} | {c['race']} | {c['illegal']} | {c['undet']} | 0 | - | - | - | - | - | -"
    return (f"{c['rows']} | {c['race']} | {c['illegal']} | {c['undet']} | {c['match']}/{c['match']+c['mismatch']} | {100*c['acc']:.1f}% | "
            f"[{100*c['lo']:.1f}, {100*c['hi']:.1f}] | {c['king']} | {c['conv']} | {c['draws']} | {c['mismatch']}")
HDR = "| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n"
md = []; summ = {}
def table(title, keyf, rs):
    g = defaultdict(list)
    for r in rs: g[keyf(r)].append(r)
    md.append(f"\n#### {title}\n\n" + HDR)
    for k in sorted(g, key=str):
        c = cell(g[k]); summ[f"{title}|{k}"] = c; md.append(f"| {k} | " + fmt(c) + " |\n")
cfgs = sorted({(r["board"], r["mode"], r["promo"], r["cap"]) for r in rows_out})
md.append("### Headline per configuration (board, pawn set, promotion set, cap)\n\n" + HDR)
for cf in cfgs:
    rs = [r for r in rows_out if (r["board"], r["mode"], r["promo"], r["cap"]) == cf]
    c = cell(rs); summ["cfg|" + str(cf)] = c; md.append(f"| {cf} | " + fmt(c) + " |\n")
for cf in cfgs:
    rs = [r for r in rows_out if (r["board"], r["mode"], r["promo"], r["cap"]) == cf]
    if len(rs) < 6: continue
    table(f"{cf}: by model class", lambda r: r["model_class"], rs)
    table(f"{cf}: by pawns (W/B)", lambda r: f"{r['nw']}/{r['nb']}", rs)
    ra = [r for r in rs if r["verdict"] == "race"]
    if ra:
        md.append(f"\nRaces at start, {cf}: real outcome (wtm,btm) counts: " + str(dict(Counter((r['real_wtm'], r['real_btm']) for r in ra))) + "\n")
# pooled over boards, Q cap 2
pool = [r for r in rows_out if r["promo"] == "Q" and r["cap"] == 2]
table("POOLED Q cap2 all boards/sets: by board", lambda r: (r["board"], r["mode"]), pool)
table("POOLED Q cap2 le2 sets: by model class", lambda r: r["model_class"], [r for r in pool if r["mode"] == "le2"])
table("POOLED Q cap2 le2 sets: all", lambda r: "all", [r for r in pool if r["mode"] == "le2"])
# side-level (each legal side to move separately; non-race)
sl = defaultdict(lambda: [0, 0])
for r in pool:
    if r["mode"] != "le2" or r["model_class"] == "race": continue
    for sd, k in (("side_w", 0), ("side_b", 1)):
        if r[sd] == "": continue
        key = (r["board"], "all")
        sl[key][1] += 1; sl[key][0] += (r[sd] == PRED[r["model_class"]][k])
md.append("\n#### Side-level (each legal, exactly valued side to move, non-race, Q cap 2, le2)\n\n| board | agree/sides | accuracy | Wilson 95% CI |\n|---|---|---|---|\n")
for k, (a, n) in sorted(sl.items()):
    lo, hi = wilson(a, n); md.append(f"| {k[0]} | {a}/{n} | {100*a/n:.1f}% | [{100*lo:.1f}, {100*hi:.1f}] |\n")
# Q vs QRBN agreement
cmp = defaultdict(Counter)
for r in rows_out:
    pass
qd = {(r["board"], r["mode"], r["P"]): r for r in rows_out if r["promo"] == "Q" and r["cap"] == 2}
for r in rows_out:
    if r["promo"] == "QRBN" and r["cap"] == 2:
        q = qd.get((r["board"], r["mode"], r["P"]))
        if q is None: continue
        k = (r["board"], r["mode"])
        if q["exact"] and r["exact"]: cmp[k]["both exact, equal" if (q["real_wtm"], q["real_btm"]) == (r["real_wtm"], r["real_btm"]) else "both exact, DIFFER"] += 1
        else: cmp[k]["one or both undetermined"] += 1
md.append("\n#### Q-only vs QRBN (cap 2) per position\n\n" + "\n".join(f"- {k}: {dict(v)}" for k, v in cmp.items()) + "\n")
open(f"{HERE}/summary.md", "w").write("".join(md)); json.dump(summ, open(f"{HERE}/summary.json", "w"), indent=1, default=str)
print("".join(md))
