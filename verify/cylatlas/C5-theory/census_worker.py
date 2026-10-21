"""C5-theory: read the worker's values.jsonl (count rule, e.p. on, textbook passed test) and
(1) list every entry whose value is a nonzero nimber *k (k>=2) or whose classifier detail has a *k (k>=2) part,
(2) count atoms (single connected components: flat k-file with all k files occupied, or cylinder rings),
(3) write the distinct atoms to atoms.jsonl for the e.p.-aware recomputation.
  cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/cylatlas/C5-theory/census_worker.py
"""
import json, re, collections, os
HERE = os.path.dirname(os.path.abspath(__file__))
idx = {}
for line in open("atlas/cylinder/value_index.jsonl"):
    d = json.loads(line); idx[d["vid"]] = d
star2 = collections.Counter(); star2_rows = []
nimpart = [d for d in idx.values() if d["detail"] and re.search(r"\*[2-9]", d["detail"])]
print("value_index entries with a *k (k>=2) part in classifier detail:", [(d["cls"], d["detail"]) for d in nimpart])
shows_with_star2 = [d["show"] for d in idx.values() if re.search(r"\*[2-9]", d["show"])]
print("distinct values whose displayed form mentions *k (k>=2) anywhere:", len(shows_with_star2), shows_with_star2[:10])
atoms = {}
ncomp_ct = collections.Counter()
for line in open("atlas/cylinder/values.jsonl"):
    d = json.loads(line)
    ncomp_ct[(d["board"], d["ncomp"])] += 1
    v = d["val"] if d["val"] is not None else idx[d["vid"]]["show"]
    if re.fullmatch(r"\*[2-9][0-9]*", v):
        star2[(d["board"], d["n"], d["w"], d["b"], d["ncomp"], d["ring"], v)] += 1
        star2_rows.append((d["board"], d["n"], d["pos"]))
    if d["ncomp"] != 1:
        continue
    files = {ord(t[0]) - 97 for t in d["pos"].replace("W:", "").replace("B:", "").replace("/", " ").split()}
    if d["board"] == "flat" and len(files) == d["n"]:
        atoms[("flat", d["n"], d["pos"])] = d["vid"]
    elif d["board"] == "cyl" and d["ring"] == 1:
        atoms[("cyl", d["n"], d["pos"])] = d["vid"]
print("entries per (board, ncomp):", dict(ncomp_ct))
print("entries with value *k, k>=2:", dict(star2))
for r in star2_rows: print("   ", r)
ac = collections.Counter((k[0], k[1]) for k in atoms)
print("atoms:", dict(ac), "total", len(atoms))
with open(os.path.join(HERE, "atoms.jsonl"), "w") as fh:
    for (b, n, p), vid in sorted(atoms.items()):
        fh.write(json.dumps({"board": b, "n": n, "pos": p, "vid_textbook": vid}) + "\n")
