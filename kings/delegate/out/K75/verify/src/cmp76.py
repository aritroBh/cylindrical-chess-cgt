"""K76 referee: compare p74 outputs with K75's per-pair tables and with my own prediction; recount the table and the rule.

Usage (repository root):  python3 -I kings/delegate/out/K75/verify/src/cmp76.py K75RAW TAG...
  K75RAW: folder with K75's <G>_<F>_<NN>_table.txt (from kings/delegate/out/K75/logs/raw_outputs.tar.xz)
  TAG: G_F_N (p74 output logs/runs/TAG.out; if TAG.out is missing, every run of the pair G_F is read)
Prints one line per pair and the totals; "all" as the only TAG means every 1 + 1 pair of logs/freezes76.txt.
Values: W, D, L in White's view; failure "B" if P < prediction (Black's favour), "W" if P > prediction.
AUXL groups (Aux lost at one bad move): at the roots only P <= r(omega + X) is proved (Theorem 4.18 (a)); a root value
below the prediction is reported as "within the bound", not as a failure of a proved statement.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mk76

V = "kings/delegate/out/K75/verify"
ORD = {"L": 0, "D": 1, "W": 2}
AUXW = {"C125_09", "C125_13", "C125_22", "C125_23", "C145_16", "C145_24", "C145_25", "C014_04", "C014_09"}
AUXL = {"C125_14", "C125_15", "C125_16", "C145_19", "C014_08"}   # K65 VERIFY table 1, K67 findings section 0


def read_p74(tag):
    paths = [f"{V}/logs/runs/{tag}.out"]
    if not os.path.exists(paths[0]):          # parts (contexts split by colour word): every run of the same pair,
        paths = sorted(f"{V}/logs/runs/{x}" for x in os.listdir(f"{V}/logs/runs")   # values do not depend on the run
                       if x.startswith(tag[:10]) and x.endswith(".out"))
    vals = {}
    for p in paths:
        for l in open(p):
            pos, v = l.rstrip("\n").split("  P=")
            vals[pos.strip()] = v[0]
    return vals


def read_k75(raw, g, f, n):
    fn = f"{raw}/{g}_{f}_{n}{n}_table.txt"
    if not os.path.exists(fn): return None
    t = {}
    for l in open(fn):
        if l.startswith("#"): continue
        a = l.split()
        i = a.index("P")
        name = " ".join(a[:i])
        j = a.index("ref3m"); k = a.index("pred")
        t[name] = (a[i + 1:j], a[j + 1:k], a[k + 1:k + 9], a[k + 9])
    return t


def main():
    raw = sys.argv[1]
    tags = sys.argv[2:]
    G = mk76.groups(); F = mk76.load_freezes()
    info = {}
    for l in open(mk76.FREEZE):
        if l.startswith("#"): continue
        r = l.strip().split("|")
        for d in r[13].split(";") if r[13] else []:
            fl, x = d.split(":"); info[(r[0], fl)] = tuple(int(y) for y in x.split(","))
    if tags == ["all"]:
        tags = [f"{g}_{f}_1" for (g, f) in sorted(info)]
    tot = dict(pairs=0, ctx=0, fail=0, pos=0, posdiff=0, mism_pk=0, mism_ref=0, mism_pred=0, onecol_fail=0,
               k75cmp=0, clean=0)
    for tag in tags:
        g, f, n = tag[:7], tag[8], int(tag[10:])
        vals = read_p74(tag)
        k75 = read_k75(raw, g, f, n)
        ctxs = mk76.contexts(n)
        agree = fail = posdiff = mpk = mref = mpred = onecol = 0
        kinds = set(); qfail = rootbelow = rootabove = 0
        failing = []
        for ws, bs in ctxs:
            name = mk76.cname(f, ws, bs)
            ps = mk76.positions(G, F, g, f, ws, bs)
            P = [vals[p] for p in ps]
            pr = mk76.pred(ws, bs)
            if k75 is not None and name in k75:
                kp, kr, kpred, _ = k75[name]
                mpk += sum(a != b for a, b in zip(P, kp)); mref += sum(a != b for a, b in zip(P, kr))
                mpred += sum(a != b for a, b in zip(pr, kpred)); tot["k75cmp"] += 8
            d = [(i, ORD[a] - ORD[b]) for i, (a, b) in enumerate(zip(P, pr)) if a != b]
            tot["pos"] += 8
            if d:
                fail += 1; posdiff += len(d); failing.append(name)
                for i, x in d:
                    kinds.add("B" if x < 0 else "W")
                    if g in AUXL:
                        if i >= 4: qfail += 1
                        elif x < 0: rootbelow += 1
                        else: rootabove += 1
                if not (ws and bs): onecol += 1
            else:
                agree += 1
        dW, dA, dB = info[(g, f)]
        cls = "AUXL" if g in AUXL else ("AUXW" if g in AUXW else "B1")
        ext = ""
        if g in AUXL:
            ctxq = sum(1 for nm in failing if any(
                vals[p] != pr_ for p, pr_ in list(zip(mk76.positions(G, F, g, f, *ctx_of(nm, f)),
                                                      mk76.pred(*ctx_of(nm, f))))[4:]))
            ext = f"  AUXL: positions failing at q's {qfail}, root below bound {rootbelow}, root above {rootabove};" \
                  f" contexts failing a proved statement {ctxq}"
        print(f"{g} {f} {n}+{n} {cls:4s} dW{dW} dA{dA} dB{dB}  {agree}/{fail}  kind {''.join(sorted(kinds)) or '-'}"
              f"  posdiff {posdiff}  one-colour failing {onecol}"
              + (f"  vs K75: pk {mpk} ref3m {mref} pred {mpred}" if k75 is not None else "  (no K75 table)") + ext)
        tot["pairs"] += 1; tot["ctx"] += len(ctxs); tot["fail"] += fail; tot["posdiff"] += posdiff
        tot["mism_pk"] += mpk; tot["mism_ref"] += mref; tot["mism_pred"] += mpred; tot["onecol_fail"] += onecol
        tot["clean"] += fail == 0
        if fail and "-v" in os.environ.get("CMP76", ""):
            print("   failing:", "; ".join(failing))
    print("TOTAL", tot)


def ctx_of(name, f):
    if name == "empty": return (), ()
    ws = tuple(int(x[2]) for x in name.split() if x[0] == "P")
    bs = tuple(int(x[2]) for x in name.split() if x[0] == "p")
    return ws, bs


if __name__ == "__main__":
    main()
