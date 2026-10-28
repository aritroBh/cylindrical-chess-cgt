#!/usr/bin/env python3
"""enumerate pawn contexts G on the context files of a cylinder; write frozen-convention batch.
usage: contexts.py BOARD FILES(e.g. 4,5,6) MAXW MAXB OUTPREFIX
G-alone frozen test positions use the kings at the two corners a1 / (last file of F_Z)6: neutral."""
import sys, itertools, json
board, files, maxw, maxb, pre = sys.argv[1], [int(x) for x in sys.argv[2].split(",")], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
kind, dims = board.split(":"); CYL = kind == "cyl"; W, H = map(int, dims.split("x"))
def nb(f, d):
    g = f + d
    return g % W if CYL else (g if 0 <= g < W else None)
def name(s): return "abcdefgh"[s[0]] + str(s[1] + 1)
sqs = [(f, r) for f in files for r in range(1, H - 1)]
def subsets(k):
    for n in range(k + 1):
        yield from itertools.combinations(sqs, n)
def has_move(ws, bs, color):
    occ = set(ws) | set(bs); own, en = (ws, bs) if color == "w" else (bs, ws); dr = 1 if color == "w" else -1
    for (f, r) in own:
        if (f, r + dr) not in occ: return True
        for d in (-1, 1):
            g = nb(f, d)
            if g is not None and (g, r + dr) in en: return True
    return False
def passers(ws, bs):
    out = {"w": [], "b": []}
    for (f, r) in ws:
        fl = {f} | {nb(f, -1), nb(f, 1)}
        if not any(g in fl and s > r for g, s in bs): out["w"].append((f, r))
    for (f, r) in bs:
        fl = {f} | {nb(f, -1), nb(f, 1)}
        if not any(g in fl and s < r for g, s in ws): out["b"].append((f, r))
    return out
ctx = []
for ws in subsets(maxw):
    for bs in subsets(maxb):
        if set(ws) & set(bs): continue
        if not ws or not bs: continue                      # tempo moves for both sides need pawns of both colours
        if not (has_move(ws, bs, "w") and has_move(ws, bs, "b")): continue
        ps = passers(ws, bs)
        ctx.append({"w": [name(s) for s in ws], "b": [name(s) for s in bs], "passers": len(ps["w"]) + len(ps["b"])})
json.dump(ctx, open(pre + "_contexts.json", "w"))
kw = "Ka1 kc6" if W >= 6 else "Ka1 kc6"
with open(pre + "_frozen_in.txt", "w") as f:
    for c in ctx:
        pw = " ".join("P" + s for s in c["w"]); pb = " ".join("p" + s for s in c["b"])
        f.write(f"{kw} {pw} {pb} w -\n{kw} {pw} {pb} b -\n")
print(len(ctx), "contexts")
