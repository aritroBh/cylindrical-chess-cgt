"""Find periodic families: base ring R, slot s, block B (two single-pawn files): R_k = R with B inserted k times at s."""
import sys, itertools, json, time
sys.path.insert(0, "research/ring_family")
from ringlib import *
from known import KNOWN
from closure import classes_of
from ins_search import SINGLES

def rk(ring, slot, block, k):
    return ring[:slot] + tuple(block) * k + ring[slot:]

def run(bases, maxw=10):
    fams = []
    for base in bases:
        n = len(base); kmax = (maxw - n) // 2
        cands = [(slot, blk) for slot in range(n) for blk in itertools.product(SINGLES, repeat=2)]
        alive = cands
        for k in range(1, kmax + 1):
            rings = [rk(base, s, b, k) for s, b in alive]
            res = evaluate(rings)
            alive = [c for c, r in zip(alive, res) if r[0] == "N" and r[1] == 2]
            print(f"  base C{n} {cstr(base)}: k={k} (C{n+2*k}) survivors {len(alive)}", flush=True)
            if not alive: break
        for s, b in alive:
            fams.append((base, s, b, kmax))
    return fams

if __name__ == "__main__":
    n = int(sys.argv[1]); maxw = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    bases = [b for b in classes_of(n) if evaluate([b])[0][:2] == ("N", 2)]
    fams = run(bases, maxw)
    print("FAMILIES surviving to the width limit:")
    seen = set()
    for base, s, b, kmax in fams:
        full = rk(base, s, b, kmax)
        key = (canon(rk(base, s, b, 0)), canon(full), cstr(b))
        print("  base", cstr(base), "slot", s, "block", cstr(b), "-> top", cstr(canon(full)), "(k up to", kmax, ")")
