"""K74 referee: compare p74's P values with the K72 tables, recount the K72 claims, check the prediction column.

Usage (repository root):  python3 -I kings/delegate/out/K72/verify/src/cmp74.py G F N [G F N ...]
For each run: reads logs/G_F_NN_p74.out (this folder), kings/delegate/out/K72/logs/G_F_NN_table.txt, and the own
prediction (mk74.pred).  Prints per run: positions compared, P disagreements (p74 vs pk column, p74 vs ref3m column),
prediction disagreements (own vs K72 column), contexts agreeing with the own prediction, contexts failing, positions
differing, how many failing contexts have pawns of both colours, how many one-colour contexts fail.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mk74

K = "kings/delegate/out/K72"
V = K + "/verify"
LAB = ["A b", "A w", "B b", "B w", "qA b", "qA w", "qB b", "qB w"]


def table(g, f, nn):
    rows = {}
    for line in open(f"{K}/logs/{g}_{f}_{nn}_table.txt"):
        if line.startswith("#"):
            continue
        a = line.split()
        i = a.index("P")
        name = " ".join(a[:i])
        pk = a[i + 1:i + 9]
        j = a.index("ref3m"); rm = a[j + 1:j + 9]
        k = a.index("pred"); pr = a[k + 1:k + 9]
        rows[name] = (pk, rm, pr, " ".join(a[k + 9:]))
    return rows


def run(g, f, n):
    nn = f"{n}{n}"
    out = [l.split("P=")[1].strip()[0] for l in open(f"{V}/logs/{g}_{f}_{nn}_p74.out")]
    ctxs = mk74.contexts(n)
    assert len(out) == 8 * len(ctxs), (len(out), len(ctxs))
    tab = table(g, f, nn)
    assert len(tab) == len(ctxs)
    npos = dpk = drm = dpred = 0
    agree = fail = posdiff = both = onecol_fail = 0
    favour = {"White": 0, "Black": 0}
    pairs = {}
    fails = []
    for c, (ws, bs) in enumerate(ctxs):
        name = mk74.name(f, ws, bs)
        mine = out[8 * c:8 * c + 8]
        pred = mk74.pred(ws, bs)
        pk, rm, pr, verdict = tab[name]
        npos += 8
        dpk += sum(a != b for a, b in zip(mine, pk))
        drm += sum(a != b for a, b in zip(mine, rm))
        dpred += sum(a != b for a, b in zip(pred, pr))
        d = [i for i in range(8) if mine[i] != pred[i]]
        if ("agree" in verdict) != (not d):
            print(f"  VERDICT MISMATCH {name}: K72 '{verdict}', own {d}")
        if d:
            fail += 1; posdiff += len(d)
            if ws and bs:
                both += 1
            else:
                onecol_fail += 1
            val = {"W": 2, "D": 1, "L": 0}
            for i in d:
                favour["White" if val[mine[i]] > val[pred[i]] else "Black"] += 1
                pairs[f"{pred[i]}->{mine[i]}"] = pairs.get(f"{pred[i]}->{mine[i]}", 0) + 1
            fails.append((name, [(LAB[i], pred[i], mine[i]) for i in d]))
        else:
            agree += 1
    print(f"{g} {f} {n}+{n}: positions {npos}; p74 vs pk differ {dpk}, vs ref3m differ {drm}; own pred vs K72 pred "
          f"differ {dpred}; contexts {len(ctxs)}, agree {agree}, fail {fail}, positions differing {posdiff} "
          f"(for White {favour['White']}, for Black {favour['Black']}); failing with both colours {both}, "
          f"one-colour failing {onecol_fail}; pairs {dict(sorted(pairs.items()))}")
    return fails


def own(g, f, n, tag):
    """p74 against the own prediction only (contexts beyond K72's tables); n = 6 means every context."""
    out = [l.split("P=")[1].strip()[0] for l in open(f"{V}/logs/{tag}_p74.out")]
    ctxs = mk74.contexts(n)
    assert len(out) == 8 * len(ctxs)
    by = {}
    fails = []
    for c, (ws, bs) in enumerate(ctxs):
        mine, pred = out[8 * c:8 * c + 8], mk74.pred(ws, bs)
        d = [i for i in range(8) if mine[i] != pred[i]]
        k = (len(ws), len(bs))
        a = by.setdefault(k, [0, 0]); a[0] += 1; a[1] += bool(d)
        if d:
            fails.append((mk74.name(f, ws, bs), [(LAB[i], pred[i], mine[i]) for i in d]))
    tot = sum(v[0] for v in by.values()); bad = sum(v[1] for v in by.values())
    print(f"{g} {f} {tag}: contexts {tot}, positions {8 * tot}, failing contexts {bad}")
    for k in sorted(by):
        print(f"   {k[0]} White + {k[1]} Black: {by[k][0]} contexts, {by[k][1]} failing")
    for name, d in fails:
        print(f"   FAIL {name:22s} {d}")


if __name__ == "__main__":
    if sys.argv[1] == "own":
        own(sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]); sys.exit()
    a = sys.argv[1:]
    verbose = False
    if a and a[0] == "-v":
        verbose = True; a = a[1:]
    for i in range(0, len(a), 3):
        fl = run(a[i], a[i + 1], int(a[i + 2]))
        if verbose:
            for name, d in fl:
                print(f"   FAIL {name:22s} {d}")
