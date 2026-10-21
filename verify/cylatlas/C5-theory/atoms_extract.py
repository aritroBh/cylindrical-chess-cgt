"""Extract the distinct atoms (single components) from the worker's values.jsonl:
flat components normalised so the leftmost occupied file is 'a' (widths 1..5), and cylinder rings
(every file occupied) on 3-, 4-, 5-file cylinders. Writes atoms.jsonl (with the worker's textbook value).
  cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/cylatlas/C5-theory/atoms_extract.py
"""
import json, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
idx = {json.loads(l)["vid"]: json.loads(l) for l in open("atlas/cylinder/value_index.jsonl")}
F = "abcdefghij"
def parse(p):
    w, b = p.split("/")
    W = [(F.index(t[0]), int(t[1:])) for t in w.split(":")[1].split()]
    B = [(F.index(t[0]), int(t[1:])) for t in b.split(":")[1].split()]
    return W, B
def txt(W, B):
    return "W: " + " ".join(f"{F[f]}{r}" for f, r in sorted(W)) + " / B: " + " ".join(f"{F[f]}{r}" for f, r in sorted(B))
atoms = {}
for line in open("atlas/cylinder/values.jsonl"):
    d = json.loads(line)
    if d["ncomp"] != 1:
        continue
    W, B = parse(d["pos"])
    v = d["val"] if d["val"] is not None else idx[d["vid"]]["show"]
    if d["board"] == "cyl":
        if d["ring"] != 1:
            continue
        key = ("cyl", d["n"], d["pos"])
    else:
        lo = min(f for f, _ in W + B); hi = max(f for f, _ in W + B)
        W2 = [(f - lo, r) for f, r in W]; B2 = [(f - lo, r) for f, r in B]
        # mirror-normalise
        wd = hi - lo
        Wm = [(wd - f, r) for f, r in W2]; Bm = [(wd - f, r) for f, r in B2]
        t = min(txt(W2, B2), txt(Wm, Bm))
        key = ("flat", wd + 1, t)
    prev = atoms.get(key)
    if prev is not None and prev != d["vid"]:
        print("INCONSISTENT translation/mirror value:", key, prev, d["vid"])
    atoms[key] = d["vid"]
ac = collections.Counter((k[0], k[1], len(parse(k[2])[0]) + len(parse(k[2])[1])) for k in atoms)
for k in sorted(ac): print(k, ac[k])
print("total atoms", len(atoms))
with open(os.path.join(HERE, "atoms.jsonl"), "w") as fh:
    for (b, n, p), vid in sorted(atoms.items()):
        fh.write(json.dumps({"board": b, "n": n, "pos": p, "vid": vid, "val_textbook": idx[vid]["show"] if len(idx[vid]["show"]) < 200 else None, "key_textbook": idx[vid]["key"]}) + "\n")
