"""lib.py -- helpers for the two-core experiment (research/star4_rings/two_core).

Rings are lists of per-file tokens ("W4B7", "B6", "W2", ...).  A ring has a pawn on every file.
Evaluation goes through a persistent `rgx` worker (rg.c + value-neutral patches, see REPORT.md) and a
append-only cache file results.tsv (ring-canonical-form <TAB> signature <TAB> nodes).
"""
import os, subprocess, re, sys, itertools, time

HERE = os.path.dirname(os.path.abspath(__file__))
RGX = os.path.join(HERE, "rgy")

# ---------------------------------------------------------------- tokens
def parse_token(t):
    w = set(); b = set(); mode = None
    for ch in t:
        if ch == 'W': mode = 'w'
        elif ch == 'B': mode = 'b'
        elif ch.isdigit():
            (w if mode == 'w' else b).add(int(ch))
    return w, b

def make_token(w, b):
    s = ""
    if w: s += "W" + "".join(str(r) for r in sorted(w))
    if b: s += "B" + "".join(str(r) for r in sorted(b))
    return s or "-"

def norm_token(t):
    w, b = parse_token(t); return make_token(w, b)

def mirror_token_color(t):
    """colour reversal: W r <-> B 9-r"""
    w, b = parse_token(t)
    return make_token({9 - r for r in b}, {9 - r for r in w})

def R(s):
    """'W5 B7 W4' -> ['W5','B7','W4']"""
    return [norm_token(t) for t in s.split()]

def S(ring):
    return " ".join(ring)

def npawns(ring):
    n = 0
    for t in ring:
        w, b = parse_token(t); n += len(w) + len(b)
    return n

# ---------------------------------------------------------------- walls
WALL = ("W2", "B4")          # alternating single-pawn wall: black pawn two ranks above the white one

def wall(L, first):
    """alternating wall of length L starting with 'W' (W2) or 'B' (B4)"""
    toks = []
    cur = 0 if first == 'W' else 1
    for i in range(L):
        toks.append(WALL[cur]); cur ^= 1
    return toks

def wall_first(L, first): return first
def wall_last(L, first):
    return first if L % 2 == 1 else ('B' if first == 'W' else 'W')

# ---------------------------------------------------------------- canonical form (rotation + reflection)
def canon(ring):
    best = None
    n = len(ring)
    for seq in (ring, ring[::-1]):
        for c in range(n):
            r = tuple(seq[c:] + seq[:c])
            if best is None or r < best: best = r
    return " ".join(best)

# ---------------------------------------------------------------- signatures
def nimber(sig):
    """'NNNPNNNN' -> 3 ; 'PNNNNNNN' -> 0 ; all-N -> 'N+' ; anything else -> None"""
    if not sig or sig[0] in 'AFE?': return None
    if set(sig) == {'N'}: return 'N+'
    if sig.count('P') == 1 and set(sig) <= {'N', 'P'}:
        return sig.index('P')
    return None

def lead_n(sig):
    k = 0
    while k < len(sig) and sig[k] == 'N': k += 1
    return k

# ---------------------------------------------------------------- worker
class Worker:
    def __init__(self, tbits=23, nodelim=6000000, H=7):
        env = dict(os.environ, TBITS=str(tbits), NODELIM=str(nodelim))
        self.H = H
        self.p = subprocess.Popen(["nice", "-n", "15", RGX, "solve", str(H)], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, env=env, bufsize=1)
    def eval(self, ringstr):
        self.p.stdin.write(ringstr + "\n"); self.p.stdin.flush()
        line = self.p.stdout.readline()
        if not line:
            raise RuntimeError("worker died on: " + ringstr)
        sig, _, rest = line.strip().partition(" ")
        nodes = int(rest.split("=")[1]) if "nodes=" in rest else -1
        return sig, nodes
    def close(self):
        try:
            self.p.stdin.close(); self.p.wait(timeout=10)
        except Exception:
            self.p.terminate()

class Evaluator:
    def __init__(self, cachefile="results.tsv", tbits=23, nodelim=6000000, H=7, extra=()):
        self.cachefile = os.path.join(HERE, cachefile)
        self.cache = {}
        for cf in [self.cachefile] + [os.path.join(HERE, e) for e in extra]:
            if os.path.exists(cf):
                with open(cf) as f:
                    for line in f:
                        p = line.rstrip("\n").split("\t")
                        if len(p) >= 2 and p[1] not in ("ABORT", "FULL"):
                            self.cache[p[0]] = (p[1], int(p[2]) if len(p) > 2 else -1)
        self.w = None; self.tbits = tbits; self.nodelim = nodelim; self.H = H
        self.out = open(self.cachefile, "a")
        self.n_new = 0
    def _worker(self):
        if self.w is None: self.w = Worker(self.tbits, self.nodelim, self.H)
        return self.w
    def sig(self, ring):
        """ring: list of tokens. returns signature string (ABORT/FULL possible)"""
        key = canon(ring)
        if key in self.cache: return self.cache[key][0]
        sig, nodes = self._worker().eval(key)
        self.cache[key] = (sig, nodes)
        self.out.write(f"{key}\t{sig}\t{nodes}\n"); self.out.flush(); self.n_new += 1
        return sig
    def val(self, ring):
        return nimber(self.sig(ring))
    def close(self):
        if self.w: self.w.close()
        self.out.close()

# ---------------------------------------------------------------- passed-pawn check (same rule as rg.c, no e.p. flag at the start)
def has_passed(ring, side):
    n = len(ring)
    ws = []; bs = []
    for t in ring:
        w, b = parse_token(t); ws.append(w); bs.append(b)
    for f in range(n):
        a, c = (f - 1) % n, (f + 1) % n
        if side == 0:
            for r in ws[f]:
                if not any(x > r for g in (a, f, c) for x in bs[g]): return True
        else:
            for r in bs[f]:
                if not any(x < r for g in (a, f, c) for x in ws[g]): return True
    return False

def legal_start(ring):
    return not has_passed(ring, 0) and not has_passed(ring, 1)

# ---------------------------------------------------------------- coordinate notation from star26_rings hits
def from_coord(line, n):
    """'W: a2 a5 c4 e2 f2 / B: a7 b4 d7 e5 g7' -> token list on n files"""
    m = re.match(r"W:\s*(.*?)\s*/\s*B:\s*(.*)$", line.strip())
    w = [set() for _ in range(n)]; b = [set() for _ in range(n)]
    for x in m.group(1).split():
        w["abcdefghijklmnop".index(x[0])].add(int(x[1:]))
    for x in m.group(2).split():
        b["abcdefghijklmnop".index(x[0])].add(int(x[1:]))
    return [make_token(w[i], b[i]) for i in range(n)]
