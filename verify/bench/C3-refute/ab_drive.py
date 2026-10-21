"""Run a fresh build of bench/ab.c (verifier copy, compiled from the unmodified source) on every row,
exactly as bench/verify.py check D does (TT on, no node cap, CPU cap per search), with a driver
written here. usage: python ab_drive.py TCAP NPROC OUT"""
import json, subprocess, sys, threading, time
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
DATA = HERE.parents[2] / "bench" / "data"
FILES = "abcdefghijklmnopqrstuvwxyz"
sq = lambda t: (FILES.index(t[0]), int(t[1:]))
tcap, nproc, out = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
rows = [json.loads(l) for sp in ["train", "val", "test", "test_heldout"] for l in open(DATA / f"{sp}.jsonl")]
def line(r, side):
    w = sorted(sq(t) for t in r["white"]); b = sorted(sq(t) for t in r["black"])
    return (f"{r['board']['files']} {int(r['board']['cylinder'])} {side} 1 0 {tcap} {len(w)} "
            + " ".join(f"{f} {x}" for f, x in w) + f" {len(b)} " + " ".join(f"{f} {x}" for f, x in b))
idx = list(range(len(rows)))
chunks = [idx[i::nproc] for i in range(nproc)]
res = {}
def run(ch):
    inp = "\n".join(line(rows[i], s) for i in ch for s in (1, 0)) + "\n"
    o = subprocess.run([str(HERE / "ab_copy")], input=inp, capture_output=True, text=True, check=True).stdout.split("\n")
    o = [x for x in o if x.strip()]
    assert len(o) == 2 * len(ch)
    for j, i in enumerate(ch):
        res[i] = (o[2 * j].split(), o[2 * j + 1].split())
t0 = time.time()
ths = [threading.Thread(target=run, args=(c,)) for c in chunks]
[t.start() for t in ths]; [t.join() for t in ths]
s = Counter(); bad = []; capped = []
with open(out, "w") as fh:
    for i, r in enumerate(rows):
        (vw, nw, tw, ew), (vb, nb, tb, eb) = res[i]
        fh.write(f"{r['id']} {vw} {vb} {nw} {nb} {tw} {tb} {ew} {eb}\n")
        s["ep_events"] += int(ew) + int(eb)
        if vw == "0" or vb == "0":
            capped.append(r["id"]); continue
        a, c = vw == "1", vb == "1"
        oc = "L" if a and not c else "R" if c and not a else "N" if a else "P"
        s["solved"] += 1; s["agree"] += oc == r["outcome"]
        if oc != r["outcome"]: bad.append((r["id"], oc, r["outcome"]))
print(json.dumps({"rows": len(rows), "summary": dict(s), "capped": capped, "bad": bad[:50], "wall_s": round(time.time() - t0)}, indent=1))
