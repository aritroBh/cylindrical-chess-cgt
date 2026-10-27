from lib import *
ev = Evaluator("results_t4.tsv", tbits=23, nodelim=20000000)
cores = {"X3": R("W5 B7 W4 W4B7 B6 W3B6 W2 B5"), "X2": R("W5 B7 W4 W4B7 B6 W3B6"), "QC": R("W3B6 W3 W2B5 B5 W2 B4 W4 B7")}
for nm, A in cores.items():
    for f in "WB":
        row = []
        for L in range(2, 13):
            full = A + wall(L, f)
            s = ev.sig(full) if legal_start(full) else "ILL"
            row.append(f"{L}:{nimber(s) if nimber(s) is not None else s[:4]}")
        print(nm, f, " ".join(row), flush=True)
