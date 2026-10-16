"""Offline replay of the tablebase line quoted in C2, from the worker's raw cache files only
(no worker code, no network). Applies UCI moves with a minimal board updater.

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      .venv/bin/python verify/engines/C2-refute/pv_replay.py "8/8/3p4/5Kp1/6Pk/2P5/8/8 w - - 0 1" f5e6 5
"""
import glob, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CACHES = [os.path.join(ROOT, "engine", "suite", "tbcache"), os.path.join(os.path.dirname(os.path.abspath(__file__)), "tbcache")]
F = "abcdefgh"
idx = {}
for c in CACHES:
    for p in glob.glob(os.path.join(c, "*", "*.json")):
        r = json.load(open(p)); idx.setdefault(r["fen"], r)

def parse(fen):
    b, stm = fen.split()[:2]; pcs = {}
    for i, row in enumerate(b.split("/")):
        f = 0
        for ch in row:
            if ch.isdigit(): f += int(ch)
            else: pcs[(f, 8 - i)] = ch; f += 1
    return pcs, stm

def fen(pcs, stm):
    rows = []
    for r in range(8, 0, -1):
        s, e = "", 0
        for f in range(8):
            p = pcs.get((f, r))
            if p is None: e += 1
            else:
                if e: s += str(e); e = 0
                s += p
        if e: s += str(e)
        rows.append(s)
    return "/".join(rows) + f" {stm} - - 0 1"

def apply(pcs, stm, u):
    fr = (F.index(u[0]), int(u[1])); to = (F.index(u[2]), int(u[3]))
    p = dict(pcs); pc = p.pop(fr); p[to] = pc  # no ep / castling / promotion in this line
    assert len(u) == 4
    return p, ("b" if stm == "w" else "w")

f0, mv, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
pcs, stm = parse(f0)
r0 = idx[fen(pcs, stm)]
print("root", fen(pcs, stm), "category", r0["data"]["category"])
for m in r0["data"]["moves"]:
    print(f"   {m['san']:6s} after-move category {m['category']}")
line = []
for i in range(n):
    pcs, stm = apply(pcs, stm, mv); line.append(mv)
    f = fen(pcs, stm)
    r = idx.get(f)
    if r is None:
        print("NOT CACHED:", f); break
    d = r["data"]
    best = d["moves"][0]
    print(f"after {' '.join(line):30s} {f:40s} stm={stm} category={d['category']} dtz={d['dtz']}; "
          f"listed-first {best['san']} ({best['category']}); all: " + ", ".join(f"{m['san']}:{m['category']}" for m in d['moves']))
    mv = best["uci"]
