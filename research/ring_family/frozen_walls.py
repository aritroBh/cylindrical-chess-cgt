"""Enumerate frozen periodic walls: cyclic rings made of w repeated, w a word of single-pawn files, in which every move
of every pawn is deleted (losing at once or poisoned) and no passer exists.  Output: primitive words up to rotation."""
import sys, itertools, subprocess
sys.path.insert(0, "research/ring_family")
from ringlib import *
SYMS = [((r,), ()) for r in range(2, 7)] + [((), (r,)) for r in range(3, 8)]
def sym_str(s): return cstr((s,))
def run(maxp, width=12):
    words = []
    for p in range(1, maxp + 1):
        for w in itertools.product(range(10), repeat=p):
            # primitive & canonical rotation only
            if any(w == w[d:] + w[:d] for d in range(1, p) if p % d == 0 and d < p and w == (w[:d] * (p // d))): continue
            if min(w[i:] + w[:i] for i in range(p)) != w: continue
            words.append(w)
    rings = []
    for w in words:
        m = max(1, -(-width // len(w)))
        rings.append(tuple(SYMS[i] for i in w) * m)
    # evaluate in batches with --reduced
    inp = "\n".join(to_text(r) for r in rings) + "\n"
    n_of = [len(r) for r in rings]
    out = []
    for width_ in sorted(set(n_of)):
        sel = [i for i, n in enumerate(n_of) if n == width_]
        text = "\n".join(to_text(rings[i]) for i in sel) + "\n"
        p = subprocess.run(["research/ring_family/ringeval_w", "--width", str(width_), "--reduced", "-", "--no-solve", "--rg-cap", "3"], input=text, capture_output=True, text=True)
        lines = p.stdout.strip().split("\n")
        # lines alternate: result line, [reduced line]  (result line has tabs; passers at root has single line)
        j = 0
        for i in sel:
            l = lines[j]; j += 1
            if "passed-at-root" in l or "RACE" in l: out.append((i, "passer")); continue
            red = lines[j]; j += 1
            out.append((i, red.strip()))
    res = []
    for i, r in out:
        if r != "passer" and "nodes=1 edges=0" in r and "terminal-win moves=0" in r:
            res.append(words[i])
    return res, words
if __name__ == "__main__":
    maxp = int(sys.argv[1])
    res, words = run(maxp)
    print(len(words), "primitive words;", len(res), "frozen")
    for w in res: print(" ".join(sym_str(SYMS[i]) for i in w))
