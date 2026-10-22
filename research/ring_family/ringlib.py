"""Ring helpers: a ring is a tuple of files, each file = (wranks, branks) (sorted tuples)."""
import subprocess, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
FILES = "abcdefghijklmnopqrstu"
RANKS = 8

def parse(text):
    w, b = text.split("/")
    ws = w.split(":")[1].split(); bs = b.split(":")[1].split()
    n = max(FILES.index(s[0]) for s in ws + bs) + 1
    return n, ws, bs

def to_ring(text, n=None):
    nn, ws, bs = parse(text)
    n = n or nn
    ring = [([], []) for _ in range(n)]
    for s in ws: ring[FILES.index(s[0])][0].append(int(s[1:]))
    for s in bs: ring[FILES.index(s[0])][1].append(int(s[1:]))
    return tuple((tuple(sorted(a)), tuple(sorted(b))) for a, b in ring)

def to_text(ring):
    ws = []; bs = []
    for f, (a, b) in enumerate(ring):
        ws += [f"{FILES[f]}{r}" for r in a]; bs += [f"{FILES[f]}{r}" for r in b]
    return "W: " + " ".join(ws) + " / B: " + " ".join(bs)

def cstr(ring):
    """compact: W2/B5 style per file separated by spaces, e.g. 'W23 B5 W2B5 W3 B56'"""
    out = []
    for a, b in ring:
        s = ""
        if a: s += "W" + "".join(map(str, a))
        if b: s += "B" + "".join(map(str, b))
        out.append(s or "-")
    return " ".join(out)

def from_cstr(s):
    ring = []
    for tok in s.split():
        w = []; b = []; mode = None
        for ch in tok:
            if ch == "W": mode = "W"
            elif ch == "B": mode = "B"
            elif ch.isdigit():
                (w if mode == "W" else b).append(int(ch))
        ring.append((tuple(sorted(w)), tuple(sorted(b))))
    return tuple(ring)

def colour_reverse(ring):
    return tuple((tuple(sorted(RANKS + 1 - r for r in b)), tuple(sorted(RANKS + 1 - r for r in a))) for a, b in ring)

def canon(ring):
    n = len(ring); best = None
    for cr in (ring, colour_reverse(ring)):
        for refl in (cr, tuple(reversed(cr))):
            for k in range(n):
                cand = refl[k:] + refl[:k]
                if best is None or cand < best: best = cand
    return best

def evaluate(rings, width=None, extra_args=(), binary=None, max_entries=1 << 24, timeout=None):
    """returns list of (outcome, nimber, sig) parallel to rings"""
    if not rings: return []
    n = len(rings[0])
    binary = binary or ("ringeval8" if n <= 8 else "ringeval" if n <= 10 else "ringeval_w")
    inp = "\n".join(to_text(r) for r in rings) + "\n"
    cmd = ["nice", "-n", "15", os.path.join(HERE, binary), "--width", str(n), "--max-entries", str(max_entries), *extra_args]
    out = subprocess.run(cmd, input=inp, capture_output=True, text=True, timeout=timeout).stdout.strip().split("\n")
    res = []
    for line in out:
        f = line.split("\t")
        if len(f) >= 4:
            res.append((f[1], int(f[2]), f[3]))
        else:
            res.append((f[1] if len(f) > 1 else "?", -9, ""))
    assert len(res) == len(rings), (len(res), len(rings))
    return res

def nparts(ring):
    return sum(len(a) + len(b) for a, b in ring)
