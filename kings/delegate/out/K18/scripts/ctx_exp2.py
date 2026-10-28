#!/usr/bin/env python3
"""context experiment driver (v2).
  ctx_exp2.py make    BOARD CTXPREFIX SORTIES.json OUTDIR [--sample NZ NN NP NF] [--withB]
  ctx_exp2.py collect BOARD CTXPREFIX SORTIES.json OUTDIR
CTXPREFIX_contexts.json / _frozen_out.txt: contexts and the frozen outcome of G alone (kp --frozen, kings a1/c6).
Class of G from (White to move, Black to move): zero = (L,W), neg = (L,L), pos = (W,W), fuzzy = (W,L).  --sample takes at most
NZ zero, NN neg, NP pos, NF fuzzy contexts (seeded), default: all.  Lines: A = Y.m + G with Black to move; B = Y + G with White to move."""
import sys, json, os, random, collections
args = sys.argv[1:]
mode, board, pre, sorties_fn, outdir = args[:5]
opts = args[5:]
ctx = json.load(open(pre + "_contexts.json")); sorties = json.load(open(sorties_fn)); os.makedirs(outdir, exist_ok=True)
outs = [l for l in open(pre + "_frozen_out.txt") if " | " in l]
froz = [(outs[2 * i].rstrip("\n").split(" | ")[1].split()[0], outs[2 * i + 1].rstrip("\n").split(" | ")[1].split()[0]) for i in range(len(ctx))]
CLS = {("L", "W"): "zero", ("L", "L"): "neg", ("W", "W"): "pos", ("W", "L"): "fuzzy"}
def strip(p): return " ".join(p.split()[:-2])
withB = "--withB" in opts
if mode == "make":
    idx = list(range(len(ctx)))
    if "--sample" in opts:
        k = opts.index("--sample"); lim = dict(zip(["zero", "neg", "pos", "fuzzy"], map(int, opts[k + 1:k + 5])))
        random.seed(1802); by = collections.defaultdict(list)
        for j in idx: by[CLS[froz[j]]].append(j)
        idx = []
        for c, v in by.items(): random.shuffle(v); idx += sorted(v[:lim[c]])
        idx.sort()
    json.dump(idx, open(f"{outdir}/ctxidx.json", "w"))
    for i, s in enumerate(sorties):
        with open(f"{outdir}/in_{i}.txt", "w") as f:
            for j in idx:
                c = ctx[j]; g = " ".join("P" + x for x in c["w"]) + " " + " ".join("p" + x for x in c["b"])
                f.write(f"{strip(s['Ym'])} {g} b -\n")
                if withB: f.write(f"{strip(s['Y'])} {g} w -\n")
    print("wrote", len(sorties), "inputs with", len(idx), "contexts each")
if mode == "collect":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import kit
    kit.setboard(board, "0:3"); W_, H_ = kit.lg2.W, kit.lg2.H
    idx = json.load(open(f"{outdir}/ctxidx.json"))
    def cheb(a, b):
        df = abs(a[0] - b[0])
        if kit.lg2.CYL: df = min(df, W_ - df)
        return max(df, abs(a[1] - b[1]))
    def sq(s): return (ord(s[0]) - 97, int(s[1:]) - 1)
    def pawn_closure(c):
        """X = every square a context pawn can ever occupy (both colours, any order, no kings); promotion flag"""
        ws = frozenset(sq(x) for x in c["w"]); bs = frozenset(sq(x) for x in c["b"])
        seen = set(); stack = [(ws, bs)]; X = set(); promo = False
        while stack:
            key = stack.pop()
            if key in seen: continue
            seen.add(key); X |= set(key[0]) | set(key[1])
            for color in "wb":
                st = (key[0], key[1], (0, 0), (2, H_ - 1), color, None)
                own = key[0] if color == "w" else key[1]
                for ns, kd, frm, to in kit.lg2.moves(st, color, False):
                    if frm not in own: continue
                    if kd == "promo": promo = True; continue
                    stack.append((ns[0], ns[1]))
        return X, promo
    pc = {}
    table = []
    for i, s in enumerate(sorties):
        rin = [l.rstrip("\n") for l in open(f"{outdir}/in_{i}.txt")]
        try: rout = [l.rstrip("\n") for l in open(f"{outdir}/out_{i}.txt") if " | " in l]
        except OSError: continue
        step = 2 if withB else 1
        if len(rout) != step * len(idx): print("skipping unfinished sortie", i); continue
        dst = sq(s["dst"]); T = s["T"]
        for jj, j in enumerate(idx):
            if j not in pc: pc[j] = pawn_closure(ctx[j])
            X, promo = pc[j]
            a = rout[step * jj].split(" | ")[1].split()
            row = {"s": i, "c": j, "frozen": froz[j], "cls": CLS[froz[j]], "A": a[0] if a[0] == a[1] else a[0] + a[1], "T": T,
                   "dB": min(cheb(dst, sq(x)) for x in ctx[j]["b"]), "dX": min(cheb(dst, x) for x in X), "promfree": not promo, "passers": ctx[j]["passers"]}
            if withB:
                b = rout[step * jj + 1].split(" | ")[1].split(); row["B"] = b[0] if b[0] == b[1] else b[0] + b[1]
            table.append(row)
    json.dump(table, open(f"{outdir}/table.json", "w")); print("rows", len(table))
