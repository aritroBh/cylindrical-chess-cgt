"""Sanity: dawson.check_quotient must report disagreements for a corrupted quotient.
Flips P on the element Phi(strip 9) (and separately on Phi(5)*Phi(5)); runs the worker's checker at T=40.
Run from project root: PYTHONPATH=. .venv/bin/python verify/dawson/C1-reproduce/rerun/check_quotient_mutation.py"""
import copy, pickle, os
from dawson import check_quotient as CQ
V = "verify/dawson/C1-reproduce/rerun/"
base = pickle.load(open("dawson/quotient_Q32.pkl", "rb"))
for label, x in [("P[Phi(9)]", base["phi"][9]), ("P[Phi(5)^2]", base["mult"][base["phi"][5]][base["phi"][5]])]:
    d = copy.deepcopy(base); d["P"][x] = not d["P"][x]
    p = V + "mut.pkl"; pickle.dump(d, open(p, "wb"))
    print("mutation", label, "element", x, "->", end=" "); CQ.main(p, 40, V + "misere_c_70.bin")
    os.remove(p)
print("unmutated ->", end=" "); CQ.main("dawson/quotient_Q32.pkl", 40, V + "misere_c_70.bin")
