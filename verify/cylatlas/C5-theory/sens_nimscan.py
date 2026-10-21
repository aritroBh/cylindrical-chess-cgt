"""C5-theory: scan the worker's sensitivity parts (parts_sens = atoms under all 6 settings incl. 5-pawn rings;
parts_sens_all = all positions w+b<=4) for nonzero nimbers *k (k>=2) and for values with a *k (k>=2) part
(classifier detail), per setting.
  cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/cylatlas/C5-theory/sens_nimscan.py
(after: mkdir -p verify/cylatlas/C5-theory/sens_x && tar -xzf atlas/cylinder/parts_sens.tar.gz -C verify/cylatlas/C5-theory/sens_x)
"""
import glob, json, re, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("parts_sens", "parts_sens_all"):
    vals = {}
    for f in glob.glob(os.path.join(HERE, "sens_x", sub, "*.vals")):
        for l in open(f):
            d = json.loads(l); vals[d["vid"]] = d
    hits = collections.defaultdict(list); partial = collections.defaultdict(set)
    n_rows = collections.Counter()
    for f in sorted(glob.glob(os.path.join(HERE, "sens_x", sub, "*.jsonl"))):
        for l in open(f):
            d = json.loads(l)
            st = (d["rule"], d["ep"]); n_rows[st] += 1
            v = vals[d["vid"]]
            if v["cls"] == "nimber" and v["key"] not in ("*1", "0"):
                hits[st].append(("cyl" if d["wrap"] else "flat", d["n"], d["pos"], v["key"], d["ncomp"]))
            det = v.get("detail") or ""
            if re.search(r"\*[2-9]", det) and v["cls"] != "nimber":
                partial[st].add((v["cls"], det))
            if re.search(r"\*[3-9]", v["key"]):
                partial[st].add(("key-contains-*k>=3", v["show"][:80]))
    print(f"== {sub}")
    for st in sorted(n_rows):
        print(f"  {st}: rows={n_rows[st]} pure *k>=2: {len(hits[st])}")
        for h in hits[st][:12]: print("      ", h)
        if len(hits[st]) > 12: print("       ...")
        for p in sorted(partial[st]): print("      part:", p)
