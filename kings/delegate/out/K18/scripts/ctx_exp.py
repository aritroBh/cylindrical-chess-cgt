#!/usr/bin/env python3
"""context experiment driver.
usage: ctx_exp.py make BOARD CTXPREFIX SORTIES.json OUTDIR      -> writes one kpp input per sortie (A: Ym+G b, B: Y+G w)
       ctx_exp.py collect BOARD CTXPREFIX SORTIES.json OUTDIR   -> reads the kpp outputs, writes table JSON
Frozen outcome of G alone (kings at a1/c6, 'kp --frozen') gives the class: (res_w, res_b) from White's view."""
import sys, json, os
mode, board, pre, sorties_fn, outdir = sys.argv[1:6]
ctx = json.load(open(pre + "_contexts.json"))
sorties = json.load(open(sorties_fn))
os.makedirs(outdir, exist_ok=True)
def strip(pos): return " ".join(pos.split()[:-2])
if mode == "make":
    for i, s in enumerate(sorties):
        with open(f"{outdir}/in_{i}.txt", "w") as f:
            for c in ctx:
                g = " ".join("P" + x for x in c["w"]) + " " + " ".join("p" + x for x in c["b"])
                f.write(f"{strip(s['Ym'])} {g} b -\n")
                f.write(f"{strip(s['Y'])} {g} w -\n")
    print("wrote", len(sorties), "inputs")

# ------------------------------------------------------------------------------------------------ collect
if mode == "collect":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import kit, collections
    kit.setboard(board, "0:3")
    W_, H_ = kit.lg2.W, kit.lg2.H
    fro = {}
    outs = [l for l in open(pre + "_frozen_out.txt") if " | " in l]
    for l in outs:
        p, r = l.rstrip("\n").split(" | ")
        t = p.split(); fro[(" ".join(t[2:-2]), t[-2])] = r.split()[0]
    def cls(c):
        key = " ".join(["P" + x for x in c["w"]] + ["p" + x for x in c["b"]])
        # frozen out lines: tokens after the two kings, in file order as written
        return None
    # rebuild lookup in the order written by contexts.py
    cl = []
    for i, c in enumerate(ctx):
        cl.append((outs[2 * i].rstrip("\n").split(" | ")[1].split()[0], outs[2 * i + 1].rstrip("\n").split(" | ")[1].split()[0]))
    def cheb(a, b):
        df = abs(a[0] - b[0]);
        if kit.lg2.CYL: df = min(df, W_ - df)
        return max(df, abs(a[1] - b[1]))
    def sq(s): return (ord(s[0]) - 97, int(s[1:]) - 1)
    def promfree(c):
        ws = frozenset(sq(x) for x in c["w"]); bs = frozenset(sq(x) for x in c["b"])
        start = (ws, bs, (0, 0), (2, H_ - 1), "w", None)
        seen = set(); stack = [start]
        while stack:
            st = stack.pop()
            key = (st[0], st[1])
            if key in seen: continue
            seen.add(key)
            for color in "wb":
                s2 = (st[0], st[1], st[2], st[3], color, None)
                for ns, kd, frm, to in kit.lg2.moves(s2, color, False):
                    own = st[0] if color == "w" else st[1]
                    if frm not in own: continue            # pawn moves only
                    if kd == "promo": return False
                    stack.append((ns[0], ns[1], st[2], st[3], "w", None))
        return True
    pf = [promfree(c) for c in ctx]
    table = []
    for i, s in enumerate(sorties):
        rin = [l.rstrip("\n") for l in open(f"{outdir}/in_{i}.txt")]
        rout = [l.rstrip("\n") for l in open(f"{outdir}/out_{i}.txt") if " | " in l]
        assert len(rin) == len(rout) == 2 * len(ctx), (len(rin), len(rout))
        dst = sq(s["dst"]) ; T = s["T"]
        for j, c in enumerate(ctx):
            a = rout[2 * j].split(" | ")[1].split(); b = rout[2 * j + 1].split(" | ")[1].split()
            dB = min(cheb(dst, sq(x)) for x in c["b"]); dW = min(cheb(dst, sq(x)) for x in c["w"])
            table.append({"s": i, "c": j, "frozen": cl[j], "A": a[0] if a[0] == a[1] else a[0] + a[1], "B": b[0] if b[0] == b[1] else b[0] + b[1],
                          "T": T, "dB": dB, "dW": dW, "promfree": pf[j], "passers": c["passers"], "nw": len(c["w"]), "nb": len(c["b"])})
    json.dump(table, open(f"{outdir}/table.json", "w"))
    print("rows", len(table))
