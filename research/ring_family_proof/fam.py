"""Families of rings and small helpers shared by the proof scripts.

A position is a list of per-file tokens, e.g. ['W23B4', 'B5', 'W2B5', 'W3', 'B5'] (see rg.c); an e.p. flag is a
trailing string 'epW=<file>' / 'epB=<file>'.

Families (rotations/reflections/colour reversals of the REPORT's families, written as in ring_family/family.py):
  odd(n)  n = 2k+3 >= 5:  W23B4 B5 W2B5 (W3 B5)^k                 wall block (W3,B5)
  even(n) n = 2m+6 >= 6:  B5 W2B5 W35B6 W2 (B4 W2)^(m+1)          wall block (B4,W2)
  F(n)    verifier's single-step family, n = 5 or n >= 7:  n odd (B4 W2)^((n-5)/2) K ; n even (B4 W2)^((n-6)/2) K W2
          with K = W3B6 B6 W4B7 W4 W6B7
"""
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
RG = os.path.join(HERE, "rg")

def toks(s):
    return s.split()

def odd(n):
    assert n % 2 == 1 and n >= 5
    k = (n - 3) // 2
    return toks("W23B4 B5 W2B5") + toks("W3 B5") * k

def even(n):
    assert n % 2 == 0 and n >= 6
    m = (n - 6) // 2
    return toks("B5 W2B5 W35B6 W2") + toks("B4 W2") * (m + 1)

K_CORE = toks("W3B6 B6 W4B7 W4 W6B7")

def F(n):
    assert n == 5 or n >= 7
    if n % 2 == 1:
        return toks("B4 W2") * ((n - 5) // 2) + K_CORE
    return toks("B4 W2") * ((n - 6) // 2) + K_CORE + toks("W2")

FAMILIES = {"odd": odd, "even": even, "F": F}
# wall blocks (the two files that are inserted when n -> n+2) and the file index (in the position lists above) at
# which the block region starts, i.e. the files [start, start + 2k) are the periodic wall
def wall_start(fam, n):
    return {"odd": 3, "even": 4, "F": 0}[fam]

def wall_len(fam, n):
    if fam == "odd": return n - 3
    if fam == "even": return n - 4
    if fam == "F": return (n - 5) if n % 2 == 1 else (n - 6)

def ntoks_pawns(ts):
    return sum(len([c for c in t if c.isdigit()]) for t in ts if t != "-")

def run_rg(mode, text, extra=(), timeout=None):
    cmd = ["nice", "-n", "15", RG, mode, *extra]
    return subprocess.run(cmd, input=text, capture_output=True, text=True, timeout=timeout).stdout

def split_file(tok):
    """'W23B4' -> ((2,3),(4,)) ; '-' -> ((),())"""
    w = []; b = []; mode = None
    if tok == "-": return ((), ())
    for ch in tok:
        if ch in "WB": mode = ch
        else: (w if mode == "W" else b).append(int(ch))
    return (tuple(sorted(w)), tuple(sorted(b)))

def join_file(wb):
    w, b = wb
    if not w and not b: return "-"
    return ("W" + "".join(map(str, sorted(w))) if w else "") + ("B" + "".join(map(str, sorted(b))) if b else "")

def parse_classify(text):
    """parse the output of `rg classify` into a list of {'pos', 'passed', 'mv': [(side, code, move, child)]}"""
    blocks = []; cur = None
    for line in text.splitlines():
        if line.startswith("POS "): cur = {"pos": line[4:], "mv": []}
        elif line.startswith("END"): blocks.append(cur)
        elif line.startswith("PASSED"): cur["passed"] = line
        else:
            head, _, child = line.partition(" => ")
            child, _, pp = child.partition(" | pp=")
            side, code, mv = head.split(" ", 2)
            cur["mv"].append((side, code, mv, child))
            cur.setdefault("pp", []).append(pp)         # '10' = White has a passed pawn in the child, Black has none
    return blocks

def wall_files(famname, n):
    """set of file indices that hold the periodic wall pattern in the start position (a cyclic arc)"""
    if famname == "odd": return set(range(3, n))              # W3 B5 W3 B5 ... B5   (file 3 .. n-1)
    if famname == "even": return set(range(3, n))             # W2 B4 W2 ... W2      (file 3 .. n-1)
    if famname == "F":
        if n % 2 == 1: return set(range(0, n - 5))            # B4 W2 ... B4 W2      (files 0 .. n-6), then K
        return set(range(0, n - 6)) | {n - 1}                 # W2 | B4 W2 ... B4 W2 (files n-1, 0 .. n-7), K in between
    raise ValueError(famname)

def is_wall_pattern(famname, S, n):
    """sanity: the wall arc really is 2-periodic with single pawns alternating colours"""
    w = sorted(wall_files(famname, n))
    for j in w:
        if (j + 2) % n in wall_files(famname, n) and S[j] != S[(j + 2) % n]: return False
    return True
