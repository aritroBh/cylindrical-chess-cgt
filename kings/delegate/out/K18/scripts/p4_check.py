#!/usr/bin/env python3
"""how often do the hypotheses (P4) (king clearance) and (P3) (promotion-free) of Proposition 8.1 hold in the tested matched cases?
R from R_all.py (plain game, P variant).  Writes logs/p4_check.json."""
import json, sys
sys.path.insert(0, "scripts"); import kit
kit.setboard("cyl:8x6", "0:3")
W, H = 8, 6
def sq(s): return (ord(s[0]) - 97, int(s[1:]) - 1)
def nbrs(x): return {((x[0] + df) % W, x[1] + dr) for df in (-1, 0, 1) for dr in (-1, 0, 1) if 0 <= x[1] + dr < H}
def closure(c):
    ws = frozenset(sq(x) for x in c["w"]); bs = frozenset(sq(x) for x in c["b"])
    seen = set(); stack = [(ws, bs)]; X = set()
    while stack:
        key = stack.pop()
        if key in seen: continue
        seen.add(key); X |= set(key[0]) | set(key[1])
        for color in "wb":
            st = (key[0], key[1], (0, 0), (2, H - 1), color, None); own = key[0] if color == "w" else key[1]
            for ns, kd, frm, to in kit.lg2.moves(st, color, False):
                if frm not in own or kd == "promo": continue
                stack.append((ns[0], ns[1]))
    return X
RS = json.load(open("logs/R_S.json")); RK = json.load(open("logs/R_k.json")); idx3 = json.load(open("logs/sorties_E3_idx.json"))
ctx = {"ES": json.load(open("logs/ctxS_contexts.json")), "EP": json.load(open("logs/ctxP_contexts.json")), "E3": json.load(open("logs/ctx8x6_efg_22_contexts.json"))}
cache = {}
def N(c):
    k = json.dumps(c, sort_keys=True)
    if k not in cache: cache[k] = set().union(*[nbrs(x) for x in closure(c)])
    return cache[k]
out = {}
for d, Rl, mp in (("ES", RS, None), ("EP", RS, None), ("E3", RK, idx3)):
    t = json.load(open(f"logs/{d}/table.json")); tot = p4 = 0
    for r in t:
        if r["cls"] not in ("zero", "neg") or r["A"] == "X": continue
        R = Rl[r["s"] if mp is None else mp[r["s"]]]
        if not R: continue
        tot += 1; p4 += not ({sq(x) for x in R["R"]} & N(ctx[d][r["c"]]))
    out[d] = {"matched_legal": tot, "P4_holds": p4}
RM = RK; ctxM = json.load(open("logs/ctxmod_contexts.json")); NM = [set().union(*[nbrs(x) for x in closure(c)]) for c in ctxM]
out["E1"] = {"cases": sum(len(NM) for R in RM if R), "P4_holds": sum(1 for R in RM if R for n in NM if not ({sq(x) for x in R["R"]} & n))}
out["L3F_true_of_sorties"] = {"S": sum(1 for r in RS if r and r["l3f"]), "k": sum(1 for r in RK if r and r["l3f"])}
json.dump(out, open("logs/p4_check.json", "w")); print(out)
