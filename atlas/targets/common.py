"""Shared helpers for workstream A3-targets.

* read pcgt run files;
* parse pcgt's exact canonical keys back into cylcgt games (BIG-free values only;
  cylcgt/cgt.py is used read-only for all CGT arithmetic here);
* classify a BIG-free value: number, nimber, x + infinitesimal (ups family with
  up-second / up-third coordinates, tiny/miny with any subscript, other), hot
  (switch x +- y or other), with mean and temperature;
* position helpers (mirror, colour reversal, FEN of the 8x8 embedding).
"""
from __future__ import annotations

import os
import sys
from collections import defaultdict
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.path.join(HERE, "work")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from cylcgt import cgt  # noqa: E402  (read-only)

RACES = ["count", "mover", "opponent", "white", "black"]
EPV = [(1, 0), (1, 1), (0, 0)]
SETTINGS = [(r, ep, aw) for r in RACES for (ep, aw) in EPV]
CORE = [(r, ep, aw) for r in ("count", "mover", "opponent") for (ep, aw) in EPV]
TEXTBOOK = ("count", 1, 0)   # database setting of atlas/flat8/rerun
AWARE = ("count", 1, 1)      # adopted convention (count rule, e.p. on, e.p.-aware passed test)


def sname(s):
    r, ep, aw = s
    return f"{r}/{'epoff' if not ep else ('epon-aware' if aw else 'epon-textbook')}"


# ------------------------------------------------------------------ run files
def opener(path):
    """open() that also reads .gz files (and falls back to PATH.gz when PATH is missing)."""
    import gzip
    if not os.path.exists(path) and os.path.exists(path + ".gz"):
        path = path + ".gz"
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path)



class Run:
    """Compact view of a pcgt run file: positions x (wrap, setting) -> gid, outcome."""

    def __init__(self, path):
        from array import array
        self.index = {}          # (pos, width) -> i
        self.pos, self.width = [], []
        self.combo = {}          # (wrap, race, ep, aware) -> column
        self.vals = {}
        cols = [(wrap, r, ep, aw) for wrap in (0, 1) for (r, ep, aw) in SETTINGS]
        self.combo = {c: j for j, c in enumerate(cols)}
        self.ncol = len(cols)
        gid = array("i")
        oc = bytearray()
        if not os.path.exists(path) and os.path.exists(path + ".gz"):
            path = path + ".gz"
        with opener(path) as fh:
            for line in fh:
                p = line.rstrip("\n").split("\t")
                if p[0] == "#V":
                    self.vals[int(p[1])] = {"big": p[2] == "1", "hash": p[3], "show": p[4], "key": p[5]}
                    continue
                k = (p[0], int(p[1]))
                i = self.index.get(k)
                if i is None:
                    i = self.index[k] = len(self.pos)
                    self.pos.append(p[0]); self.width.append(int(p[1]))
                    gid.extend([-2] * self.ncol); oc.extend(b"?" * self.ncol)
                j = self.combo[(int(p[2]), p[3], int(p[4]), int(p[5]))]
                gid[i * self.ncol + j] = int(p[6])
                oc[i * self.ncol + j] = ord(p[7])
        self.gid, self.oc = gid, oc

    def g(self, i, wrap, setting):
        return self.gid[i * self.ncol + self.combo[(wrap,) + tuple(setting)]]

    def o(self, i, wrap, setting):
        return chr(self.oc[i * self.ncol + self.combo[(wrap,) + tuple(setting)]])

    def has(self, wrap, setting):
        j = self.combo[(wrap,) + tuple(setting)]
        return any(self.gid[i * self.ncol + j] != -2 for i in range(min(len(self.pos), 50)))


# ------------------------------------------------------------------ key parser
def parse_key(s: str) -> cgt.Game:
    """Inverse of pcgt's key(): "n", "n/d", "*k", or "{L,..|R,..}"."""
    pos = 0

    def atom(i):
        j = i
        while j < len(s) and s[j] not in ",|}":
            j += 1
        t = s[i:j]
        if t.startswith("*"):
            return cgt.nimber(int(t[1:])), j
        return cgt.number(Fraction(t)), j

    def game(i):
        if s[i] != "{":
            return atom(i)
        i += 1
        L, R = [], []
        cur = L
        while True:
            if s[i] == "|":
                cur = R
                i += 1
                continue
            if s[i] == "}":
                return cgt.make(L, R), i + 1
            if s[i] == ",":
                i += 1
                continue
            g, i = game(i)
            cur.append(g)

    g, pos = game(0)
    assert pos == len(s), (s, pos)
    return g


# ------------------------------------------------------------------ targets
Z, S, U, D = cgt.ZERO, cgt.STAR, cgt.UP, cgt.DOWN
UP2 = cgt.make([Z], [cgt.add(D, S)])                                   # {0 | v*}
UP3 = cgt.make([Z], [cgt.add(cgt.add(D, cgt.neg(UP2)), S)])            # {0 | * - up - up2}


def _mul(g, n):
    h = cgt.ZERO
    for _ in range(abs(n)):
        h = cgt.add(h, g if n > 0 else cgt.neg(g))
    return h


UPS = {}  # game id -> (a, b, c, k): a.up + b.up2 + c.up3 + *k
for _a in range(-8, 9):
    for _b in range(-4, 5):
        for _c in range(-2, 3):
            base = cgt.add(cgt.add(_mul(U, _a), _mul(UP2, _b)), _mul(UP3, _c))
            for _k in range(4):
                g = cgt.add(base, cgt.nimber(_k))
                UPS.setdefault(g.id, (_a, _b, _c, _k))


def ups_name(t):
    a, b, c, k = t
    parts = []
    for coef, nm in ((a, "↑"), (b, "↑²"), (c, "↑³")):
        if coef == 0:
            continue
        if nm == "↑":
            parts.append({1: "↑", -1: "↓"}.get(coef, f"{coef}·↑" if coef > 0 else f"{-coef}·↓"))
        else:
            dn = nm.replace("↑", "↓")
            parts.append({1: nm, -1: dn}.get(coef, f"{coef}·{nm}" if coef > 0 else f"{-coef}·{dn}"))
    s = " + ".join(parts) if parts else ""
    if k:
        s += ("" if not s else " + ") + ("*" if k == 1 else f"*{k}")
    return s or "0"


def fnum(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def classify(g: cgt.Game) -> dict:
    """Classify a BIG-free canonical game."""
    if g.num is not None:
        x = g.num
        return {"cls": "integer" if x.denominator == 1 else "dyadic", "num": fnum(x), "den": x.denominator,
                "mean": fnum(x), "temp": None}
    if g.nim is not None:
        return {"cls": "nimber", "nim": g.nim, "mean": "0", "temp": "0"}
    try:
        lw, rw, m, t = cgt.thermograph(g)
    except AssertionError as e:  # pragma: no cover
        return {"cls": "thermo-error", "err": str(e)}
    out = {"mean": fnum(Fraction(m)), "temp": fnum(Fraction(t))}
    if t == 0:
        h = cgt.add(g, cgt.number(-Fraction(m))) if m != 0 else g
        shift = "" if m == 0 else fnum(Fraction(m))
        out["shift"] = shift
        if h.nim is not None:
            out["cls"] = "number+nimber"
            out["inf"] = "*" if h.nim == 1 else f"*{h.nim}"
        elif h.id in UPS:
            a, b, c, k = UPS[h.id]
            out["cls"] = "ups" if (b == 0 and c == 0) else "upsecond-family"
            out["ups"] = [a, b, c, k]
            out["inf"] = ups_name(UPS[h.id])
        elif (h.L == (Z,) and len(h.R) == 1 and h.R[0].L == (Z,) and len(h.R[0].R) == 1):
            sub = cgt.neg(h.R[0].R[0])
            out["cls"] = "tiny"
            out["sub"] = cgt.show(sub)
            out["sub_is_number"] = sub.num is not None
            out["sub_is_integer"] = sub.num is not None and sub.num.denominator == 1
            out["inf"] = f"tiny({out['sub']})"
        elif (h.R == (Z,) and len(h.L) == 1 and h.L[0].R == (Z,) and len(h.L[0].L) == 1):
            sub = h.L[0].L[0]
            out["cls"] = "miny"
            out["sub"] = cgt.show(sub)
            out["sub_is_number"] = sub.num is not None
            out["sub_is_integer"] = sub.num is not None and sub.num.denominator == 1
            out["inf"] = f"miny({out['sub']})"
        else:
            out["cls"] = "other-infinitesimal"
            out["inf"] = cgt.show(h)
        out["infinitesimal"] = m == 0
    else:
        if len(g.L) == 1 and len(g.R) == 1 and g.L[0].num is not None and g.R[0].num is not None:
            out["cls"] = "switch"
        else:
            out["cls"] = "hot-other"
        out["stops"] = [fnum(Fraction(x)) for x in cgt.stops(g)]
    return out


# ------------------------------------------------------------------ positions
def parse_pos(s):
    w, b = s.split("/")
    f = lambda part: [(ord(t[0]) - 97, int(t[1:])) for t in part.split(":")[1].split()]
    return f(w), f(b)


def fmt_pos(W, B):
    n = lambda q: f"{chr(97 + q[0])}{q[1]}"
    return "W: " + " ".join(sorted(map(n, W))) + " / B: " + " ".join(sorted(map(n, B)))


def mirror(s, width):
    W, B = parse_pos(s)
    return fmt_pos([(width - 1 - f, r) for f, r in W], [(width - 1 - f, r) for f, r in B])


def colour_reverse(s):
    W, B = parse_pos(s)
    return fmt_pos([(f, 9 - r) for f, r in B], [(f, 9 - r) for f, r in W])


def npawns(s):
    W, B = parse_pos(s)
    return len(W) + len(B)


def fen(position, width, to_move="w", component_offset=0, treb="g", king_files=("f", "h")):
    """8x8 embedding: component on files a.. (+offset), trebuchet W g4 / B g5,
    WK f5, BK h4 (the proposed embedding)."""
    W, B = parse_pos(position)
    board = {}
    for f, r in W:
        board[(f + component_offset, r)] = "P"
    for f, r in B:
        board[(f + component_offset, r)] = "p"
    board[(5, 5)] = "K"; board[(6, 4)] = "P"; board[(6, 5)] = "p"; board[(7, 4)] = "k"
    rows = []
    for r in range(8, 0, -1):
        s, e = "", 0
        for f in range(8):
            c = board.get((f, r))
            if c is None:
                e += 1
            else:
                s += (str(e) if e else "") + c
                e = 0
        rows.append(s + (str(e) if e else ""))
    return "/".join(rows) + f" {to_move} - - 0 1"
