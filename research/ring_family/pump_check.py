"""pump_check.py: verify that the reduced game graph of ring_{k+1} maps onto that of ring_k by deleting two interior files.
Usage: python pump_check.py <family: odd|even> kmin kmax
"""
import sys, subprocess, re, os
sys.path.insert(0, "research/ring_family")
from ringlib import *

FAMS = {"odd": ("B5 W2B5", "W3 B5", "W23B4"), "even": ("B4 W2", "B4 W2", "B5 W2B5 W35B6 W2")}
def fam(name, k):
    pre, per, suf = FAMS[name]
    return from_cstr(pre) + from_cstr(per) * k + from_cstr(suf)

def dump(ring, path):
    n = len(ring)
    subprocess.run(["research/ring_family/ringeval_w", "--width", str(n), "--reduced", path], input=to_text(ring) + "\n",
                   capture_output=True, text=True, check=True)
    return [l.rstrip("\n").split("\t") for l in open(path)]

sq = re.compile(r"([a-u])(\d)")
def remap_text(text, delete, n):
    """rename files in a string, deleting pawns on `delete` files (must be empty of any mention) -> raises if mention"""
    def rep(m):
        f = ord(m.group(1)) - 97
        if f in delete: raise ValueError("mentions deleted file: " + text)
        g = f - sum(1 for d in delete if d < f)
        return chr(97 + g) + m.group(2)
    return sq.sub(rep, text)

def state_files(text, delete):
    """check deleted files hold exactly their original pawns (given by `inter`) -> return text with those pawns removed"""
    pass

def image(edges, inter, nplus):
    """edges of ring_{k+1}; inter = dict file-> (colour, rank) pawn on the two deleted files. returns set of edges of the image"""
    delete = set(inter)
    out = set()
    for a, side, mv, b in edges:
        def strip(state):
            # remove the interior pawns from the state string and rename
            head, _, ep = state.partition(" ep")
            w, bl = head.split(" / B:")
            ws = w[2:].split(); bs = bl.split()
            for f, (col, rk) in inter.items():
                tok = chr(97 + f) + str(rk)
                lst = ws if col == "W" else bs
                if tok not in lst: raise ValueError(f"interior pawn {tok} missing in {state}")
                lst.remove(tok)
            s = "W: " + " ".join(remap_text(t, delete, nplus) for t in ws) + " / B: " + " ".join(remap_text(t, delete, nplus) for t in bs)
            if ep: s += " ep" + remap_text(ep, delete, nplus)
            return s
        sa = strip(a)
        if b == "TERMINAL-WIN":
            out.add((sa, side, remap_text(mv, delete, nplus), b))
        else:
            out.add((sa, side, remap_text(mv, delete, nplus), strip(b)))
    return out

if __name__ == "__main__":
    name = sys.argv[1]; kmin, kmax = int(sys.argv[2]), int(sys.argv[3])
    prev = None
    for k in range(kmin, kmax + 1):
        ring = fam(name, k)
        edges = dump(ring, f"research/ring_family/dumps/{name}_k{k}.tsv")
        if prev is not None:
            pk, pring, pedges = prev
            # choose interior pair: files p, p+1 in the middle of the chain; both must keep their original pawn in all states
            n = len(ring)
            p = (n // 2) - 1   # middle of the ring (chain is longer than half the ring for k >= 3)
            inter = {}
            for f in (p, p + 1):
                a, b = ring[f]
                inter[f] = ("W", a[0]) if a else ("B", b[0])
            try:
                img = image(edges, inter, n)
                ok = (img == set(tuple(e) for e in pedges))
                print(f"{name}: ring_k{k} (C{n}) --delete files {p},{p+1} {inter}--> equals reduced graph of k{k-1} (C{n-2})? {ok}   |edges| {len(edges)} -> {len(img)} vs {len(pedges)}")
                if not ok:
                    d1 = img - set(tuple(e) for e in pedges); d2 = set(tuple(e) for e in pedges) - img
                    print("    only in image:", len(d1), list(d1)[:2]); print("    only in smaller:", len(d2), list(d2)[:2])
            except ValueError as e:
                print(f"{name}: k{k}: interior pawn moved / mentioned: {e}")
        prev = (k, ring, edges)
