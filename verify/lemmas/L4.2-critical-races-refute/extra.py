# Extra robustness checks with the independent engine (indep.py):
#  (a) does any reachable non-terminal node split into >1 component (empty file between pawns)?
#  (b) are the base value and the 4 single-flip values unchanged for BIG = 32 and BIG = 1024?
#  (c) single flips relative to the "mover" baseline (for context only; not part of the claim).
import sys, importlib.util, os
spec = importlib.util.spec_from_file_location("indep", os.path.join(os.path.dirname(__file__), "indep.py"))
I = importlib.util.module_from_spec(spec); spec.loader.exec_module(I)
for ep in (True, False):
    cfg = I.Cfg(4, ep); root = I.parse(I.ROOT)
    nodes, races = I.explore(cfg, root)
    split = 0
    for x in nodes:
        if I.status(cfg, x) is not None: continue
        fs = sorted({f for f, _ in x[0] | x[1]})
        if any(b - a > 1 for a, b in zip(fs, fs[1:])): split += 1
    print("ep=%s non-terminal reachable nodes that split: %d" % (ep, split))
    order = sorted(races, key=lambda cm: (I.pstr(cm[0]), cm[1]))
    cnt = lambda c, m: I.count_winner(cfg, c, m)
    for big in (32, 1024):
        I.BIG = big; I.init_big()
        base = I.Wvalue(cfg, root, cnt)
        res = []
        for key in order:
            w0 = cnt(*key); fl = "B" if w0 == "W" else "W"
            g = I.Wvalue(cfg, root, lambda c, m, key=key, fl=fl: fl if (c, m) == key else cnt(c, m))
            if g is not base: res.append((I.pstr(key[0]), key[1], I.show(g)))
        print("  BIG=%d base=%s flips=%s" % (big, I.show(base), res))
    I.BIG = 256; I.init_big()
    mov = lambda c, m: m
    base = I.Wvalue(cfg, root, mov)
    res = []
    for key in order:
        fl = "B" if key[1] == "W" else "W"
        g = I.Wvalue(cfg, root, lambda c, m, key=key, fl=fl: fl if (c, m) == key else m)
        if g is not base: res.append((I.pstr(key[0]), key[1], I.show(g)))
    print("  mover-baseline W=%s; single flips that change it (%d): %s" % (I.show(base), len(res), res))
    sys.stdout.flush()
