"""Values of the all-six witnesses: independent model vs worker's parts_sens ring atoms.
  cd verify/cylatlas/C4-refute && ../../../.venv/bin/python check_witness.py
"""
import glob, json, re, sys, threading
sys.path.insert(0, ".")
from indep import Model, parse, vkey, show
POS = [(4, "W: a2 c3 / B: b6 b7 d6"), (4, "W: a2 a3 c3 / B: b6 d7"), (4, "W: a2 c2 / B: b7 d7")]
vals = {}
for vf in glob.glob("worker_data/parts_sens/*.vals"):
    for l in open(vf):
        x = json.loads(l); vals[x["vid"]] = x
wk = {}
for pf in glob.glob("worker_data/parts_sens/cyl4_*.jsonl"):
    m = re.search(r"_(count|mover|opponent)_ep(\d)_", pf)
    for l in open(pf):
        x = json.loads(l)
        wk[(x["pos"], m.group(1), int(m.group(2)))] = vals[x["vid"]]["key"]
def main():
    for n, s in POS:
        for e in (1, 0):
            for r in ("count", "mover", "opponent"):
                M = Model(r, bool(e)); W, B = parse(s)
                g = M.whole(n, True, W, B, None)
                w = wk.get((s, r, e), "(not in worker canonical list)")
                print(f"C{n} {s:26s} {r:8s} ep{e}: mine {show(g):28s} worker-key-match={vkey(g) == w}")
threading.stack_size(1 << 28); t = threading.Thread(target=main); t.start(); t.join()
