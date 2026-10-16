"""Adversarial re-check of claim C4 (engine/suite/cgt_verified.epd, cgt_disagree.epd).

Independent of the worker's code and of cylcgt: stdlib only. Reads (read-only)
the two EPD files, the worker's selection JSONs (just for the list of probed FENs)
and the raw Lichess responses in engine/suite/tbcache/.

    cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/engines/C4-refute/refute_c4.py

Model re-implemented from its written spec (cgtpos.py / pawns.py docstrings):
  component on files a-d, 8 ranks, en passant on; a position where exactly one side
  has a passed pawn is a win for that side; both sides passed after a move = race,
  rule "count": the opponent of the mover moves first, whoever needs fewer moves to
  promote wins, opponent wins ties; a side with no pawn move loses (king moves lose).
  A pawn move wins for the mover iff the resulting position is a win for the mover
  with the opponent to move.
"""
from __future__ import annotations

import collections
import glob
import json
import os
import sys
from fractions import Fraction
from functools import lru_cache

sys.setrecursionlimit(200000)
ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
SUITE = os.path.join(ROOT, "engine", "suite")
FILES = "abcdefgh"

# ----------------------------------------------------------------- EPD parsing


def parse_epd(line):
    toks = line.strip().split(" ", 4)
    if len(toks) < 5:
        return None
    fen4 = " ".join(toks[:4])
    rest = toks[4]
    ops, i, n = {}, 0, len(rest)
    while i < n:
        while i < n and rest[i] == " ":
            i += 1
        if i >= n:
            break
        j = rest.index(" ", i)
        opc = rest[i:j]
        i = j + 1
        args, cur, inq = [], "", False
        while i < n:
            ch = rest[i]
            if inq:
                if ch == '"':
                    inq = False
                    args.append(cur)
                    cur = ""
                else:
                    cur += ch
            elif ch == '"':
                inq = True
            elif ch == ";":
                if cur.strip():
                    args.extend(cur.split())
                cur = ""
                i += 1
                break
            else:
                cur += ch
            i += 1
        ops[opc] = args
    return fen4, ops


# ----------------------------------------------------------------- chess (K+P)


def parse_fen(fen):
    parts = fen.split()
    board = {}
    for i, row in enumerate(parts[0].split("/")):
        r = 8 - i
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                board[(f, r)] = ch
                f += 1
        assert f == 8, fen
    return board, parts[1], parts[2], parts[3]


def sqn(s):
    return f"{FILES[s[0]]}{s[1]}"


def attacked_by(board, sq, color):
    """Is square sq attacked by `color` ('w'/'b')? Only kings and pawns exist."""
    f, r = sq
    for (g, s), p in board.items():
        if color == "w":
            if p == "P" and s + 1 == r and abs(g - f) == 1:
                return True
            if p == "K" and max(abs(g - f), abs(s - r)) == 1:
                return True
        else:
            if p == "p" and s - 1 == r and abs(g - f) == 1:
                return True
            if p == "k" and max(abs(g - f), abs(s - r)) == 1:
                return True
    return False


def king_sq(board, color):
    k = "K" if color == "w" else "k"
    sqs = [s for s, p in board.items() if p == k]
    return sqs


def validity(fen):
    board, stm, castle, ep = parse_fen(fen)
    errs = []
    if set(board.values()) - set("KkPp"):
        errs.append("non K/P pieces")
    if len(king_sq(board, "w")) != 1 or len(king_sq(board, "b")) != 1:
        errs.append("king count")
        return errs, board
    if any(p in "Pp" and r in (1, 8) for (f, r), p in board.items()):
        errs.append("pawn on rank 1/8")
    wk, bk = king_sq(board, "w")[0], king_sq(board, "b")[0]
    if max(abs(wk[0] - bk[0]), abs(wk[1] - bk[1])) <= 1:
        errs.append("kings adjacent")
    other = "b" if stm == "w" else "w"
    if attacked_by(board, king_sq(board, other)[0], stm):
        errs.append("side not to move in check")
    if len(board) > 7:
        errs.append("more than 7 men")
    if sum(p == "P" for p in board.values()) > 8 or sum(p == "p" for p in board.values()) > 8:
        errs.append("pawn count")
    if castle != "-":
        errs.append("castling field")
    if ep != "-":
        errs.append("ep field present (unexpected)")
    return errs, board


def legal_moves(board, stm, ep):
    """All legal moves (UCI) of a K+P position, with move kind."""
    out = {}
    me = stm
    them = "b" if me == "w" else "w"
    P, K = ("P", "K") if me == "w" else ("p", "k")
    d = 1 if me == "w" else -1
    start = 2 if me == "w" else 7
    last = 8 if me == "w" else 1
    eps = None if ep == "-" else (FILES.index(ep[0]), int(ep[1]))
    cand = []
    for (f, r), p in board.items():
        if p == P:
            r1 = r + d
            if (f, r1) not in board:
                cand.append(((f, r), (f, r1), "push"))
                if r == start and (f, r + 2 * d) not in board:
                    cand.append(((f, r), (f, r + 2 * d), "double"))
            for g in (f - 1, f + 1):
                if 0 <= g < 8:
                    t = (g, r1)
                    q = board.get(t)
                    if q is not None and (q.islower() if me == "w" else q.isupper()) and q not in "Kk":
                        cand.append(((f, r), t, "capture"))
                    elif eps == t:
                        cand.append(((f, r), t, "ep"))
        elif p == K:
            for df in (-1, 0, 1):
                for dr in (-1, 0, 1):
                    if df == dr == 0:
                        continue
                    t = (f + df, r + dr)
                    if not (0 <= t[0] < 8 and 1 <= t[1] <= 8):
                        continue
                    q = board.get(t)
                    if q is not None and (q.isupper() if me == "w" else q.islower()):
                        continue
                    if q is not None and q in "Kk":
                        continue
                    cand.append(((f, r), t, "king"))
    for fr, to, kind in cand:
        nb = dict(board)
        piece = nb.pop(fr)
        if kind == "ep":
            del nb[(to[0], fr[1])]
        nb[to] = piece
        if attacked_by(nb, king_sq(nb, me)[0], them):
            continue
        u = sqn(fr) + sqn(to)
        if kind != "king" and to[1] == last:
            for pr in "qrbn":
                out[u + pr] = kind
        else:
            out[u] = kind
    return out


def san_kp(board, uci, kind):
    fr = (FILES.index(uci[0]), int(uci[1]))
    to = (FILES.index(uci[2]), int(uci[3]))
    if kind == "king":
        cap = "x" if to in board else ""
        return "K" + cap + uci[2:4]
    if kind in ("capture", "ep"):
        return uci[0] + "x" + uci[2:4]
    return uci[2:4]


# ----------------------------------------------------------------- the model
# component state: (W frozenset, B frozenset, ep) ; ep = (target, captured, side) or None
NF = 4  # files a-d, flat
NR = 8


def passed(W, B, side):
    mine, theirs = (W, B) if side == "W" else (B, W)
    for f, r in mine:
        blocked = False
        for g, s in theirs:
            if abs(g - f) <= 1 and ((s > r) if side == "W" else (s < r)):
                blocked = True
                break
        if not blocked:
            return True
    return False


def dist(W, B, side):
    """moves needed to promote, best passed front pawn; double step counted."""
    mine, theirs = (W, B) if side == "W" else (B, W)
    occ = W | B
    best = None
    for f, r in mine:
        ahead = [(g, s) for g, s in theirs if abs(g - f) <= 1 and ((s > r) if side == "W" else (s < r))]
        if ahead:
            continue
        if side == "W":
            if any((f, s) in occ for s in range(r + 1, NR + 1)):
                continue
            dd = NR - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)):
                continue
            dd = r - 1 - (1 if r == NR - 1 else 0)
        best = dd if best is None else min(best, dd)
    return best if best is not None else 10 ** 6


def comp_moves(W, B, ep, side):
    """list of (uci, kind, (W', B', ep'))"""
    mine, theirs = (W, B) if side == "W" else (B, W)
    occ = W | B
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else NR - 1
    epc = ep if (ep is not None and ep[2] == side) else None
    other = "B" if side == "W" else "W"
    out = []

    def mk(nm, nt, e=None):
        return (frozenset(nm), frozenset(nt), e) if side == "W" else (frozenset(nt), frozenset(nm), e)

    for f, r in mine:
        rest = mine - {(f, r)}
        r1 = r + d
        assert 1 < r1 < NR, "promotion inside the component tree"
        if (f, r1) not in occ:
            out.append((sqn((f, r)) + sqn((f, r1)), "push", mk(rest | {(f, r1)}, theirs)))
            r2 = r + 2 * d
            if r == start and (f, r2) not in occ:
                out.append((sqn((f, r)) + sqn((f, r2)), "double",
                            mk(rest | {(f, r2)}, theirs, ((f, r1), (f, r2), other))))
        for g in (f - 1, f + 1):
            if not (0 <= g < NF):
                continue
            t = (g, r1)
            if t in theirs:
                out.append((sqn((f, r)) + sqn(t), "capture", mk(rest | {t}, theirs - {t})))
            elif epc is not None and epc[0] == t:
                out.append((sqn((f, r)) + sqn(t), "ep", mk(rest | {t}, theirs - {epc[1]})))
    return out


def terminal(W, B, mover):
    """'W'/'B' winner if the position just reached is decided by passed pawns, else None."""
    wp, bp = passed(W, B, "W"), passed(W, B, "B")
    if wp and bp:
        other = "B" if mover == "W" else "W"
        return other if dist(W, B, other) <= dist(W, B, mover) else mover
    if wp:
        return "W"
    if bp:
        return "B"
    return None


@lru_cache(maxsize=None)
def winner(W, B, ep, stm):
    """Winner of the component game with `stm` to move (no passers present)."""
    other = "B" if stm == "W" else "W"
    for _, _, (W2, B2, e2) in comp_moves(W, B, ep, stm):
        t = terminal(W2, B2, stm)
        w = t if t is not None else winner(W2, B2, e2, other)
        if w == stm:
            return stm
    return other


def predicted_wins(W, B, stm):
    other = "B" if stm == "W" else "W"
    s = set()
    for uci, kind, (W2, B2, e2) in comp_moves(W, B, None, stm):
        t = terminal(W2, B2, stm)
        w = t if t is not None else winner(W2, B2, e2, other)
        if w == stm:
            s.add(uci)
    return s


# ----------------------------------------------------------------- tiny CGT engine
class Gm:
    __slots__ = ("L", "R", "id", "num", "nim")


_tab = {}
_le_memo = {}


def raw(L, R):
    key = (tuple(sorted({g.id for g in L})), tuple(sorted({g.id for g in R})))
    g = _tab.get(key)
    if g is None:
        g = Gm()
        byid = {x.id: x for x in list(L) + list(R)}
        g.L = tuple(byid[i] for i in key[0])
        g.R = tuple(byid[i] for i in key[1])
        g.id = len(_tab)
        g.num = None
        g.nim = None
        _tab[key] = g
        if key[0] == key[1] and all(x.nim is not None for x in g.L):
            ns = sorted(x.nim for x in g.L)
            if ns == list(range(len(ns))):
                g.nim = len(ns)
    return g


ZERO = raw([], [])
ZERO.num = Fraction(0)
_num_cache = {Fraction(0): ZERO}


def number(x):
    x = Fraction(x)
    if x in _num_cache:
        return _num_cache[x]
    if x.denominator == 1:
        g = raw([number(x - 1)], []) if x > 0 else raw([], [number(x + 1)])
    else:
        e = Fraction(1, x.denominator)
        g = raw([number(x - e)], [number(x + e)])
    g.num = x
    _num_cache[x] = g
    return g


def le(g, h):
    if g.num is not None and h.num is not None:
        return g.num <= h.num
    k = (g.id, h.id)
    v = _le_memo.get(k)
    if v is None:
        v = not (any(le(h, gl) for gl in g.L) or any(le(hr, g) for hr in h.R))
        _le_memo[k] = v
    return v


def eq(g, h):
    return le(g, h) and le(h, g)


def simplest_between(lo, hi):
    """simplest number x with lo < x < hi (None = unbounded); assumes lo < hi."""
    import math
    if (lo is None or lo < 0) and (hi is None or hi > 0):
        return Fraction(0)
    if lo is not None and lo >= 0:
        n = math.floor(lo) + 1
        if hi is None or n < hi:
            return Fraction(n)
        k = 1
        while True:
            t = math.floor(lo * 2 ** k) + 1
            if Fraction(t, 2 ** k) < hi:
                return Fraction(t, 2 ** k)
            k += 1
    # hi <= 0
    n = math.ceil(hi) - 1
    if lo is None or n > lo:
        return Fraction(n)
    k = 1
    while True:
        t = math.ceil(hi * 2 ** k) - 1
        if Fraction(t, 2 ** k) > lo:
            return Fraction(t, 2 ** k)
        k += 1


def canon(L, R):
    L = list({g.id: g for g in L}.values())
    R = list({g.id: g for g in R}.values())
    changed = True
    while changed:
        changed = False
        # dominated
        L2 = [a for a in L if not any(b is not a and le(a, b) for b in L)]
        R2 = [a for a in R if not any(b is not a and le(b, a) for b in R)]
        if len(L2) != len(L) or len(R2) != len(R):
            L, R, changed = L2, R2, True
        G = raw(L, R)
        # reversible left options
        newL = []
        for a in L:
            rev = next((ar for ar in a.R if le(ar, G)), None)
            if rev is not None:
                newL.extend(rev.L)
                changed = True
            else:
                newL.append(a)
        if changed:
            L = list({g.id: g for g in newL}.values())
            continue
        newR = []
        for b in R:
            rev = next((bl for bl in b.L if le(G, bl)), None)
            if rev is not None:
                newR.extend(rev.R)
                changed = True
            else:
                newR.append(b)
        if changed:
            R = list({g.id: g for g in newR}.values())
    G = raw(L, R)
    if all(x.num is not None for x in L + R):
        lo = max((x.num for x in L), default=None)
        hi = min((x.num for x in R), default=None)
        if lo is None or hi is None or lo < hi:
            x = simplest_between(lo, hi)
            n = number(x)
            assert eq(n, G), (x, L, R)
            return n
    return G


_add_memo = {}


def add(g, h):
    if g.num is not None and h.num is not None:
        return number(g.num + h.num)
    k = (min(g.id, h.id), max(g.id, h.id))
    v = _add_memo.get(k)
    if v is None:
        v = canon([add(x, h) for x in g.L] + [add(g, x) for x in h.L],
                  [add(x, h) for x in g.R] + [add(g, x) for x in h.R])
        _add_memo[k] = v
    return v


def neg(g):
    if g.num is not None:
        return number(-g.num)
    return canon([neg(x) for x in g.R], [neg(x) for x in g.L])


STAR = canon([ZERO], [ZERO])
UP = canon([ZERO], [STAR])
DOWN = neg(UP)
UPS = canon([ZERO, STAR], [ZERO])
DUP = add(UP, UP)
NAMED = {}
for gg, nm in [(UP, "↑"), (DOWN, "↓"), (UPS, "↑*"), (neg(UPS), "↓*"), (DUP, "⇑"), (neg(DUP), "⇓"),
               (add(DUP, STAR), "⇑*"), (neg(add(DUP, STAR)), "⇓*"), (add(DUP, UP), "3↑"),
               (neg(add(DUP, UP)), "3↓")]:
    NAMED.setdefault(gg.id, nm)
BIGN = 256
BIG_DISPLAY = 128


def fmt_num(x):
    if abs(x) >= BIG_DISPLAY:
        return "+W" if x > 0 else "-W"
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def show(g):
    if g.num is not None:
        return fmt_num(g.num)
    if g.nim is not None:
        return "*" if g.nim == 1 else f"*{g.nim}"
    if g.id in NAMED:
        return NAMED[g.id]
    L, R = g.L, g.R
    if len(L) == 1 and len(R) == 1 and L[0].num is not None and R[0].num is not None:
        a, b = L[0].num, R[0].num
        if a == b:
            return f"{fmt_num(a)}*"
        m, d = (a + b) / 2, (a - b) / 2
        return f"±{fmt_num(d)}" if m == 0 else f"{fmt_num(m)}±{fmt_num(d)}"
    if [x.id for x in L] == [ZERO.id] and len(R) == 1 and [x.id for x in R[0].L] == [ZERO.id] \
            and len(R[0].R) == 1 and R[0].R[0].num is not None:
        return f"tiny({fmt_num(-R[0].R[0].num)})"
    if [x.id for x in R] == [ZERO.id] and len(L) == 1 and [x.id for x in L[0].R] == [ZERO.id] \
            and len(L[0].L) == 1 and L[0].L[0].num is not None:
        return f"miny({fmt_num(L[0].L[0].num)})"
    return "{" + ", ".join(show(x) for x in L) + " | " + ", ".join(show(x) for x in R) + "}"


ASCII = {"↑": "^", "↓": "v", "⇑": "^^", "⇓": "vv", "±": "+-", "∗": "*"}


def to_ascii(v):
    for a, b in ASCII.items():
        v = v.replace(a, b)
    return v


def norm_display(s):
    """Parse '{A, B | C}' recursively and sort option lists, so option order does not matter."""
    s = s.strip()
    if not s.startswith("{"):
        return s
    assert s.endswith("}"), s
    inner = s[1:-1]
    depth, parts, cur, side = 0, {"L": [], "R": []}, "", "L"
    for ch in inner:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        if depth == 0 and ch in ",|":
            if cur.strip():
                parts[side].append(norm_display(cur))
            cur = ""
            if ch == "|":
                side = "R"
            continue
        cur += ch
    if cur.strip():
        parts[side].append(norm_display(cur))
    return ("{", tuple(sorted(map(str, parts["L"]))), tuple(sorted(map(str, parts["R"]))))


def value_class(v):  # the worker's string heuristic, re-typed from its definition
    if "W" in v:
        return "hot-BIG" if "|" in v or "±" in v else "decided"
    if v.lstrip("-").replace("/", "").isdigit():
        return "number"
    if v.startswith("*"):
        return "nimber"
    if any(a in v for a in "↑↓⇑⇓"):
        return "infinitesimal"
    if "±" in v and "|" not in v:
        return "switch"
    return "other-tame"


@lru_cache(maxsize=None)
def cgt_value(W, B, ep):
    """CGT value of a component with no passers (ep usable only by its owner, dropped otherwise)."""
    Lpos_ep = ep if (ep is not None and ep[2] == "W") else None
    Rpos_ep = ep if (ep is not None and ep[2] == "B") else None
    L = [child_value(W2, B2, e2, "W") for _, _, (W2, B2, e2) in comp_moves(W, B, Lpos_ep, "W")]
    R = [child_value(W2, B2, e2, "B") for _, _, (W2, B2, e2) in comp_moves(W, B, Rpos_ep, "B")]
    return canon(L, R)


def child_value(W, B, ep, mover):
    t = terminal(W, B, mover)
    if t is not None:
        return number(BIGN if t == "W" else -BIGN)
    return cgt_value(W, B, ep)


# ----------------------------------------------------------------- tablebase cache
def load_cache():
    out = {}
    for p in glob.glob(os.path.join(SUITE, "tbcache", "*", "*.json")):
        rec = json.load(open(p))
        out[rec["fen"]] = rec
    return out


def comp_of(board):
    W = frozenset(s for s, p in board.items() if p == "P" and s[0] < 4)
    B = frozenset(s for s, p in board.items() if p == "p" and s[0] < 4)
    return W, B


def treb_of(board):
    return {s: p for s, p in board.items() if s[0] >= 4}


def analyse(fen, cache):
    errs, board = validity(fen)
    _, stm, _, ep = parse_fen(fen)
    S = "W" if stm == "w" else "B"
    legal = legal_moves(board, stm, ep)
    W, B = comp_of(board)
    assert not passed(W, B, "W") and not passed(W, B, "B"), fen
    # e-file empty and trebuchet layout
    assert not any(s[0] == 4 for s in board), fen
    pawn_legal = {u for u, k in legal.items() if k != "king"}
    cm = {u: k for u, k, _ in comp_moves(W, B, None, S)}
    assert set(cm) == pawn_legal, (fen, set(cm) ^ pawn_legal)  # only component pawns move
    pred = predicted_wins(W, B, S)
    rec = cache.get(fen)
    res = {"fen": fen, "errs": errs, "stm": S, "legal": legal, "pred": pred, "rec": rec, "kinds": legal,
           "board": board}
    if rec is None or rec.get("status") != 200:
        return res
    d = rec["data"]
    tbm = {m["uci"]: m["category"] for m in d["moves"]}
    res["tb_moves_equal_legal"] = set(tbm) == set(legal)
    res["tb_root"] = d["category"]
    res["tb_win"] = {u for u, c in tbm.items() if c == "loss"}
    res["tb_win_cursed"] = {u for u, c in tbm.items() if c == "blessed-loss"}
    res["tb_draw"] = {u for u, c in tbm.items() if c == "draw"}
    res["tb_odd"] = {u: c for u, c in tbm.items() if c not in ("loss", "win", "draw")}
    res["tb_san"] = {m["uci"]: m["san"] for m in d["moves"]}
    res["checkmate_or_stalemate"] = d.get("checkmate") or d.get("stalemate")
    return res


def main():
    cache = load_cache()
    print("cache records:", len(cache))
    ver = [parse_epd(l) for l in open(os.path.join(SUITE, "cgt_verified.epd")) if l.strip()]
    dis = [parse_epd(l) for l in open(os.path.join(SUITE, "cgt_disagree.epd")) if l.strip()]
    print("verified lines", len(ver), "disagree lines", len(dis))
    allfens = [f for f, _ in ver] + [f for f, _ in dis]
    print("distinct FENs (verified+disagree):", len(set(allfens)), "of", len(allfens))
    print("distinct components+stm in verified:", len({(f.split()[0].split('/'), ) and
                                                       (tuple(sorted(comp_of(parse_fen(f)[0])[0])),
                                                        tuple(sorted(comp_of(parse_fen(f)[0])[1])),
                                                        f.split()[1]) for f, _ in ver}))

    problems = collections.Counter()
    stats = collections.Counter()
    cls = collections.Counter()
    my_cls = collections.Counter()
    value_mismatch = []
    for fen4, ops in ver:
        fen = fen4 + " 0 1"
        a = analyse(fen, cache)
        stats["n"] += 1
        stats["stm_" + a["stm"]] += 1
        if a["errs"]:
            problems["invalid:" + ",".join(a["errs"])] += 1
        if a["rec"] is None:
            problems["no cache"] += 1
            continue
        if not a["tb_moves_equal_legal"]:
            problems["tb moves != my legal moves"] += 1
        if a["tb_root"] != "win":
            problems["tb root not win: " + str(a["tb_root"])] += 1
        if a["tb_win_cursed"] or a["tb_odd"]:
            problems["cursed/odd categories"] += 1
        bm_uci = set(" ".join(ops["c2"]).split())
        sans = {a["tb_san"][u] for u in bm_uci}
        if sans != set(ops["bm"]):
            problems["bm SAN != c2 UCI"] += 1
        # my own SAN
        mysans = {san_kp(a["board"], u, a["legal"][u]) for u in bm_uci}
        if mysans != set(ops["bm"]):
            problems["bm SAN != my SAN"] += 1
        if a["tb_win"] != a["pred"]:
            problems["VERIFIED but my CGT-pred != TB win set"] += 1
            print("  MISMATCH", fen, "pred", sorted(a["pred"]), "tb", sorted(a["tb_win"]))
        if bm_uci != a["tb_win"]:
            problems["c2 != TB win set"] += 1
        if bm_uci != a["pred"]:
            problems["c2 != my pred"] += 1
        if len(bm_uci) == 1:
            stats["unique"] += 1
        kinds = {u: k for u, k in a["legal"].items() if k != "king"}
        slow = bool(a["tb_win"]) and all(kinds.get(u) == "push" for u in a["tb_win"]) and \
            any(k in ("double", "capture", "ep") for k in kinds.values())
        stats["slow"] += slow
        c5 = ops.get("c5", [""])[0]
        if ("only-slow-winning-move true" in c5) != slow:
            problems["slow flag mismatch"] += 1
        claimed_class = c5.split(";")[0].replace("class ", "").strip()
        cls[claimed_class] += 1
        # CGT value string
        W, B = comp_of(a["board"])
        v = cgt_value(W, B, None)
        mine = show(v)
        my_cls[value_class(mine)] += 1
        if value_class(mine) != claimed_class:
            problems["class mismatch"] += 1
        c0 = ops["c0"][0]
        claimed_v = c0.split("count=")[1].split(";")[0].strip()
        if norm_display(to_ascii(mine)) != norm_display(claimed_v):
            value_mismatch.append((fen, mine, claimed_v))
        # sign test vs minimax
        if a["stm"] == "W":
            root_win = not le(v, ZERO)
        else:
            root_win = not le(ZERO, v)
        if root_win != bool(a["pred"]):
            problems["CGT sign != minimax"] += 1
    print("VERIFIED stats:", dict(stats))
    print("claimed classes:", dict(cls))
    print("my classes     :", dict(my_cls))
    print("value-string mismatches:", len(value_mismatch))
    for x in value_mismatch[:20]:
        print("   ", x)
    print("VERIFIED problems:", dict(problems) or "none")

    # ----- disagreement file
    dp = collections.Counter()
    droot = collections.Counter()
    for fen4, ops in dis:
        fen = fen4 + " 0 1"
        a = analyse(fen, cache)
        if a["errs"]:
            dp["invalid:" + ",".join(a["errs"])] += 1
        if a["rec"] is None:
            dp["no cache"] += 1
            continue
        if not a["tb_moves_equal_legal"]:
            dp["tb moves != legal"] += 1
        droot[a["tb_root"]] += 1
        expect = a["tb_win"] if a["tb_win"] else a["tb_draw"]
        if set(" ".join(ops["c2"]).split()) != expect:
            dp["c2 != TB win-or-draw set"] += 1
        if a["tb_win_cursed"] or a["tb_odd"]:
            dp["cursed/odd"] += 1
        agree = (a["tb_root"] == "win" and a["tb_win"] == a["pred"]) or \
                (a["tb_root"] == "loss" and not a["pred"])
        if agree:
            dp["actually agrees with my CGT pred"] += 1
    print("DISAGREE roots:", dict(droot), "problems:", dict(dp) or "none")

    # ----- completeness: every probed selection position
    sel = json.load(open(os.path.join(SUITE, "selection.json"))) + \
        json.load(open(os.path.join(SUITE, "selection_ext.json")))
    sel_fens = [c["fen"] for c in sel]
    print("selected positions:", len(sel_fens), "distinct:", len(set(sel_fens)))
    vset = {f + " 0 1" for f, _ in ver}
    dset = {f + " 0 1" for f, _ in dis}
    cat = collections.Counter()
    missing_dis = []
    for fen in sel_fens:
        a = analyse(fen, cache)
        if a["rec"] is None or a["rec"].get("status") != 200:
            cat["unprobed"] += 1
            continue
        if a["tb_root"] == "win" and a["tb_win"] == a["pred"]:
            k = "verified"
        elif a["tb_root"] == "loss" and not a["pred"]:
            k = "agree-loss"
        else:
            k = "disagree"
        where = "V" if fen in vset else "D" if fen in dset else "-"
        cat[(k, where, a["tb_root"])] += 1
        if k == "disagree" and where != "D":
            missing_dis.append((fen, sorted(a["pred"]), a["tb_root"]))
    for k, v in sorted(cat.items(), key=str):
        print("  ", k, v)
    print("disagreements NOT in cgt_disagree.epd:", len(missing_dis))
    for x in missing_dis:
        print("   ", x)


if __name__ == "__main__":
    main()
