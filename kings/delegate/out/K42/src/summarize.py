#!/usr/bin/env python3
"""summarise test runs. usage: summarize.py W CTXFILE K18TAG.json|- TESTOUT [TESTOUT...]
Per context: class, whether both sides have a pawn move at G (K18's context family), L/D/W/X counts,
failures among sorties that K18's search lists as plain-only at NOESC roots (P and Q variants)."""
import sys, json, collections
W = int(sys.argv[1]); ctx = {l.split()[0]: l.split()[1:] for l in open(sys.argv[2])}
tag = json.load(open(sys.argv[3])) if sys.argv[3] != "-" else {"P": [], "Q": []}
TP = {tuple(x) for x in tag["P"]}; TQ = {tuple(x) for x in tag["Q"]}
def canon(y): t = y.split(); return " ".join(sorted(t[:-2])) + " " + " ".join(t[-2:])
def sq(t): return ("abcdefghi".index(t[0]), int(t[1:]) - 1)
def hasmove(toks, color):
    ws = {sq(x[1:]) for x in toks if x[0] == "P"}; bs = {sq(x[1:]) for x in toks if x[0] == "p"}
    own, en, dr = (ws, bs, 1) if color == "w" else (bs, ws, -1)
    for f, r in own:
        if (f, r + dr) not in ws | bs: return True
        if any((((f + d) % W), r + dr) in en for d in (-1, 1)): return True
    return False
summ = {}; fails = collections.defaultdict(list)
for fn in sys.argv[4:]:
    for l in open(fn):
        p = l.rstrip("\n").split(" | ")
        if p[0] == "SUM":
            t = p[2].split(); summ[p[1]] = dict(zip(t[0::2], map(int, t[1::2])))
        elif p[0] == "FAIL" and len(p) == 7 and p[6] in ("D", "W"):
            fails[p[1]].append(p)
tot = collections.Counter()
print("context | class | family | legal | L | D | W | fails at K18 NOESC plain-only (P,Q)")
for cid in ctx:
    if cid not in summ: continue
    s = summ[cid]; fam = hasmove(ctx[cid], "w") and hasmove(ctx[cid], "b")
    fl = [f for f in fails[cid]]
    kp = sum(1 for f in fl if (canon(f[2]), f[3].replace("x", "").replace("ep", "")) in TP)
    kq = sum(1 for f in fl if (canon(f[2]), f[3].replace("x", "").replace("ep", "")) in TQ)
    legal = s["L"] + s["D"] + s["W"]
    print(f"{cid} {' '.join(ctx[cid])} | {cid.split(':')[1]} | {'both-move' if fam else 'one-or-none'} | {legal} | {s['L']} | {s['D']} | {s['W']} | {kp},{kq}")
    for k, v in (("legal", legal), ("L", s["L"]), ("D", s["D"]), ("W", s["W"]), ("kP", kp), ("kQ", kq)):
        tot[(fam, k)] += v; tot[("all", k)] += v
    tot[(fam, "nctx")] += 1; tot[("all", "nctx")] += 1
    tot[(fam, "ctx_with_fail")] += (s["D"] + s["W"] > 0); tot[("all", "ctx_with_fail")] += (s["D"] + s["W"] > 0)
for g in ("all", True, False):
    print("TOTAL", {True: "both-move", False: "one-or-none", "all": "all"}[g], {k[1]: v for k, v in tot.items() if k[0] == g})
