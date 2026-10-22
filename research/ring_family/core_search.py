"""Search 3-file cores (6 pawns) + alternating chain (W r, B r+2) of length L; list cores giving *2."""
import itertools, sys, time, subprocess, os, json
sys.path.insert(0, "research/ring_family")
from ringlib import *
from core_enum import contents

HERE = os.path.dirname(os.path.abspath(__file__))
def chain(r, start, L):
    W = ((r,), ()); B = ((), (r + 2,))
    seq = (W, B) if start == "W" else (B, W)
    return tuple(seq[i % 2] for i in range(L))

def cores(npawns=6, nfiles=3):
    C = contents(); by = {}
    for c in C: by.setdefault(len(c[0]) + len(c[1]), []).append(c)
    def rec(k, left):
        if k == 1:
            if left in by:
                for c in by[left]: yield (c,)
            return
        for p in range(1, 4):
            if p <= left - (k - 1) and p in by:
                for c in by[p]:
                    for rest in rec(k - 1, left - p): yield (c,) + rest
    return list(rec(nfiles, npawns))

def run_batch(rings, n):
    binary = "ringeval8" if n <= 8 else "ringeval" if n <= 10 else "ringeval_w"
    inp = "\n".join(to_text(r) for r in rings) + "\n"
    p = subprocess.run(["nice", "-n", "15", os.path.join(HERE, binary), "--width", str(n), "--max-entries", str(1 << 22)],
                       input=inp, capture_output=True, text=True)
    return p.stdout.strip().split("\n")

if __name__ == "__main__":
    L = int(sys.argv[1]); out = sys.argv[2]
    cs = cores()
    print(len(cs), "cores", flush=True)
    res = {}
    t0 = time.time()
    for r in (2, 3):
        for start in ("W", "B"):
            ch = chain(r, start, L)
            hits = []
            B = 20000
            for i in range(0, len(cs), B):
                part = cs[i:i + B]
                rings = [ch + c for c in part]
                lines = run_batch(rings, len(rings[0]))
                assert len(lines) == len(rings), (len(lines), len(rings))
                for c, line in zip(part, lines):
                    f = line.split("\t")
                    if len(f) >= 4 and f[1] == "N" and f[2] == "2":
                        hits.append(cstr(c))
            res[f"{r}{start}"] = hits
            print(f"r={r} start={start} L={L}: {len(hits)} hits  ({time.time()-t0:.0f}s)", flush=True)
    json.dump(res, open(out, "w"))
