"""Driver for mysolve (verifier C3-refute). Does not import any bench/ or cylcgt code.

usage: python drive.py MODE RULE TCAP NPROC OUT [ids_file]
Writes OUT (one result line per row) and prints a summary vs the stored outcome.
"""
import json
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[2] / "bench" / "data"
FILES = "abcdefghijklmnopqrstuvwxyz"


def sq(t):
    return FILES.index(t[0]), int(t[1:])


def rows():
    for sp in ["train", "val", "test", "test_heldout"]:
        for line in open(DATA / f"{sp}.jsonl"):
            yield json.loads(line)


def job(r, mode, rule, tcap):
    w = [sq(t) for t in r["white"]]
    b = [sq(t) for t in r["black"]]
    return (f"{r['id']} {r['board']['files']} {int(r['board']['cylinder'])} {mode} {rule} {tcap} "
            f"{len(w)} " + " ".join(f"{f} {x}" for f, x in w) + f" {len(b)} " + " ".join(f"{f} {x}" for f, x in b))


def outcome(rw, rb):
    if rw < 0 or rb < 0:
        return None
    return {(1, 0): "L", (0, 1): "R", (1, 1): "N", (0, 0): "P"}[(rw, rb)]


def main():
    mode, rule, tcap, nproc, out = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    allrows = list(rows())
    if len(sys.argv) > 6:
        keep = set(Path(sys.argv[6]).read_text().split())
        allrows = [r for r in allrows if r["id"] in keep]
    gold = {r["id"]: r for r in allrows}
    # interleave rows over processes so each gets a similar mix of k
    chunks = [allrows[i::nproc] for i in range(nproc)]
    procs = []
    t0 = time.time()
    for i, ch in enumerate(chunks):
        inp = "\n".join(job(r, mode, rule, tcap) for r in ch) + "\n"
        p = subprocess.Popen([str(HERE / "mysolve")], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        procs.append((p, inp))
    outs = []
    import threading

    def feed(p, inp, store):
        o, _ = p.communicate(inp)
        store.append(o)

    ths = []
    for p, inp in procs:
        t = threading.Thread(target=feed, args=(p, inp, outs))
        t.start()
        ths.append(t)
    for t in ths:
        t.join()
    lines = [l for o in outs for l in o.strip().splitlines()]
    Path(out).write_text("\n".join(sorted(lines)) + "\n")
    s = Counter()
    bad = []
    for l in lines:
        tag, m, ru, rw, rb, nodes, races, epc, diffj, rootp = l.split()
        r = gold[tag]
        oc = outcome(int(rw), int(rb))
        grp = f"{r['split']} k={r['k']}"
        if oc is None:
            s["capped " + grp] += 1
            continue
        s["solved"] += 1
        s["agree"] += oc == r["outcome"]
        if oc != r["outcome"]:
            bad.append((tag, oc, r["outcome"]))
        s["races"] += int(races)
        s["rows_with_race"] += int(races) > 0
        s["epcap_generated"] += int(epc)
        s["diffjudged"] += int(diffj)
        s["rootpass"] += int(rootp)
    print(json.dumps({"mode": mode, "rule": rule, "tcap": tcap, "rows": len(allrows), "lines": len(lines),
                      "summary": dict(sorted(s.items())), "disagreements": bad[:50], "n_bad": len(bad),
                      "wall_s": round(time.time() - t0, 1)}, indent=1))


if __name__ == "__main__":
    main()
