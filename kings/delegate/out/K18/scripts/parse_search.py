#!/usr/bin/env python3
"""parse lg --search output; mirror-dedupe; summarise.  usage: parse_search.py FILE NF [variant] -> prints stats, writes JSON list"""
import re, sys, json, collections
fn, nf = sys.argv[1], int(sys.argv[2]); var = sys.argv[3] if len(sys.argv) > 3 else "Q"
def mirror_sq(s): return chr(97 + nf - 1 - (ord(s[0]) - 97)) + s[1:]
def mirror_pos(y):
    toks = y.split()
    out = [t[0] + mirror_sq(t[1:]) if t[0] in "KkPp" else t for t in toks[:-2]] + toks[-2:]
    head = sorted(out[:-2], key=lambda t: (t[0].lower() != 'k', t[0].islower(), t[1:]))
    return " ".join(out)
def canon(y):
    toks = y.split()
    def norm(ts): return tuple(sorted(ts))
    a = norm(toks[:-2]); b = norm([t[0] + mirror_sq(t[1:]) for t in toks[:-2]])
    return min(a, b)
cands = {}
for line in open(fn):
    if line.startswith("#"): continue
    p = [x.strip() for x in line.rstrip("\n").split("|")]
    if p[0] != var: continue
    Y, info, flag, sorties = p[1], p[2], p[3], p[4]
    m = re.match(r"only=(\d+) esc=(\d+)", info)
    sl = re.findall(r"\[([^\]]*)\]", sorties)
    moves = []
    for s in sl:
        t = s.split()
        d = {"move": t[0], "cls": t[1]}
        for x in t[2:]:
            if x.startswith("k="):
                d["kvec"] = [None if y == "-" else int(y) for y in x[2:].split(",")]
                continue
            mm = re.match(r"(Tplain|Tpass)=(\d+)\((.*)\)", x)
            if mm: d[mm.group(1)] = int(mm.group(2)); d[mm.group(1) + "_r"] = mm.group(3)
        moves.append(d)
    key = canon(Y)
    if key in cands: continue
    cands[key] = {"Y": Y, "flag": flag, "only": int(m.group(1)), "esc": int(m.group(2)), "moves": moves}
allc = list(cands.values())
noesc = [c for c in allc if c["flag"] == "NOESC"]
print(fn, var, "distinct(any)=", len(allc), "distinct(noesc)=", len(noesc))
def npawns(Y):
    t = Y.split(); return (sum(1 for x in t if x[0]=='P'), sum(1 for x in t if x[0]=='p'))
cnt = collections.Counter(npawns(c["Y"]) for c in noesc); print("pawn counts (W,B):", sorted(cnt.items()))
Ts = collections.Counter(max(m.get("Tplain", 0) for m in c["moves"] if m["cls"] == "PLAIN-ONLY") for c in noesc); print("max T over plain-only sorties:", sorted(Ts.items()))
nmoves = collections.Counter(len(c["moves"]) for c in noesc); print("number of White moves:", sorted(nmoves.items()))
kinds = collections.Counter(("king" if m["move"].startswith("K") else "pawn") for c in noesc for m in c["moves"] if m["cls"] == "PLAIN-ONLY"); print("plain-only sortie kinds:", dict(kinds))
json.dump(allc, open(fn.replace(".out", ".%s.json" % var), "w"))
