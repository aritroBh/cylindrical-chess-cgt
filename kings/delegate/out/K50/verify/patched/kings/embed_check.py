"""K50: does kings/theory/LOOPY.md certify the frozen-king model for a K+P position?

FEN in, JSON out. Standard library only. The program never says CERTIFIED for a clause unless a statement
that LOOPY proves applies; UNDECIDED is the default. Usage note, verdicts and limitations:
kings/delegate/out/K50/findings.txt.

Usage (from the project root):
  python3 kings/embed_check.py [--board flat:8x8|cyl:8x8|flat:WxH|cyl:WxH] [--fz f,g,h]
                               [--group Kf5,Pg4,kh4,pg5] [--tmax 8] [--cap 300000] [--ctx] [--pretty]
                               ['FEN' ...]
Positions are FEN (or EPD; only the first four fields are read) or kpsolve tokens
("Kf5 Pg4 kh4 pg5 Pa2 pa4 w -"). Without positions on the command line, one per line from stdin.

What is checked (LOOPY section numbers):
  separation   Definition 2.1: F_Z (default: the shortest arc holding both kings' files; --fz sets it,
               --group declares the king group's squares, and then every pawn on F_Z must be declared),
               buffer pawn-free, no officer, nobody in check, H >= 5.
  (V1)         check: Proposition 1.15(a) (a side in check at X is in check at every Y; no check arises later);
               (E):   L1.6, by enumerating an over-approximation of the reachable contexts;
               (V1b): a Z-move that is legal in every reachable context (Lemma 2.2); with --ctx also a king step
                      onto a buffer square that no reachable enemy context pawn attacks.
  (V3)         every Z-move m of each side: Theorem 2.7(a) with (L1_P), (L3_F) and (L2) (Proposition 2.10(a) for
               T = 1; otherwise a lower bound on mu_s over all reachable contexts). Same certificate gives (V2) at
               the Z-move terminals. With --ctx, (L3) itself (not only (L3_F)) is checked over the reachable
               contexts; that check is this program's argument (findings.txt), not a statement of LOOPY.
  (V2)         every passer or race terminal reachable: Proposition 2.11 / Corollary 2.11a ((H1)-(H5), a win in the
               frozen model F), carried to P by Corollary 2.7' (every king move of the loser along the push is a
               P-loss, by Theorem 2.7(a) at those nodes).
  conclusion   Theorem 1.14(i) when (V1)-(V3) all hold; otherwise the sharp form of Theorem 1.14 with the winner
               sigma of the D-game (computed here): (V1a), (V1b) for the loser, (V3) for the loser, (V2) at the
               terminals credited to sigma. Both give a result in P; chess needs (A_Q)(X), which is not checked.
"""
from __future__ import annotations

import json
import sys
import time

FILES = "abcdefghijklmnopqrstuvwxyz"
INF = 10**6
sys.setrecursionlimit(20000)


class Limit(Exception):
    pass


# ---------- board ----------

class Board:
    def __init__(self, W, H, wrap):
        self.W, self.H, self.wrap = W, H, wrap

    def nb(self, f, df):
        g = f + df
        if self.wrap:
            return g % self.W
        return g if 0 <= g < self.W else None

    def fdist(self, f, g):
        d = abs(f - g)
        return min(d, self.W - d) if self.wrap else d

    def kdist(self, a, b):
        return max(self.fdist(a[0], b[0]), abs(a[1] - b[1]))

    def steps(self, s):
        out = []
        for df in (-1, 0, 1):
            g = self.nb(s[0], df)
            if g is None:
                continue
            for dr in (-1, 0, 1):
                if (df or dr) and 1 <= s[1] + dr <= self.H and (g, s[1] + dr) != s:
                    out.append((g, s[1] + dr))
        return list(dict.fromkeys(out))


def nm(s):
    return f"{FILES[s[0]]}{s[1]}"


def sqp(t):
    return (FILES.index(t[0]), int(t[1:]))


def attacked(B, s, pawns, by_white):
    """Is square s attacked by one of `pawns` (white pawns if by_white)?"""
    r = s[1] - 1 if by_white else s[1] + 1
    return any((B.nb(s[0], df), r) in pawns for df in (-1, 1) if B.nb(s[0], df) is not None)


# ---------- chess moves for kings and pawns (no officers) ----------
# pos = (wk, bk, wp, bp, ep): ep is the target square the side to move may capture on, or None.

def moves(B, pos, white):
    """Legal moves of `white` (True) or Black: list of (kind, frm, to, promo, newpos)."""
    wk, bk, wp, bp, ep = pos
    k, ok = (wk, bk) if white else (bk, wk)
    mine, theirs = (wp, bp) if white else (bp, wp)
    d, last, start = (1, B.H, 2) if white else (-1, 1, B.H - 1)
    out = []

    def put(kind, frm, to, nk, nmine, ntheirs, nep, promo):
        if B.kdist(nk, ok) <= 1 or attacked(B, nk, ntheirs, not white):
            return
        np = (nk, ok, nmine, ntheirs, nep) if white else (ok, nk, ntheirs, nmine, nep)
        out.append((kind, frm, to, promo, np))

    for t in B.steps(k):
        if t not in mine and t != ok:
            put("K", k, t, t, mine, theirs - {t}, None, False)
    occ = mine | theirs | {wk, bk}
    for p in mine:
        f, r = p
        rest = mine - {p}
        r1 = r + d
        if not 1 <= r1 <= B.H:
            continue
        if (f, r1) not in occ:
            put("P", p, (f, r1), k, rest | {(f, r1)}, theirs, None, r1 == last)
            if r == start and (f, r1 + d) not in occ and 1 <= r1 + d <= B.H:
                put("P", p, (f, r1 + d), k, rest | {(f, r1 + d)}, theirs, (f, r1), r1 + d == last)
        for df in (-1, 1):
            g = B.nb(f, df)
            if g is None:
                continue
            t = (g, r1)
            if t in theirs:
                put("P", p, t, k, rest | {t}, theirs - {t}, None, r1 == last)
            elif ep is not None and t == ep:
                put("P", p, t, k, rest | {t}, theirs - {(g, r)}, None, False)
    return out


def in_check(B, pos, white):
    wk, bk, wp, bp, _ = pos
    return attacked(B, wk, bp, False) if white else attacked(B, bk, wp, True)


def mv_name(m, white):
    kind, frm, to, promo, _ = m
    c = ("K" if white else "k") if kind == "K" else ("P" if white else "p")
    return f"{c}{nm(frm)}-{nm(to)}" + ("=Q" if promo else "")


# ---------- pawn-only positions of the context (no kings) ----------
# state = (wset, bset, ep) with ep = (target, victim, capturer 'W'/'B') or None

def pawn_children(B, st, side, block=frozenset()):
    """Positions after one move of `side` ('W'/'B'), promotions included (pawn on the last rank).
    `block`: squares held by a king (they stop pushes and cannot be captured)."""
    w, b, ep = st
    mine, theirs = (w, b) if side == "W" else (b, w)
    d, start = (1, 2) if side == "W" else (-1, B.H - 1)
    occ = w | b | block
    tgt = ep if (ep and ep[2] == side) else None
    out = []

    def emit(nm_, nt, nep=None):
        out.append((frozenset(nm_), frozenset(nt), nep) if side == "W" else (frozenset(nt), frozenset(nm_), nep))

    for p in mine:
        f, r = p
        rest = mine - {p}
        r1 = r + d
        if not 1 <= r1 <= B.H:
            continue
        if (f, r1) not in occ:
            emit(rest | {(f, r1)}, theirs)
            if r == start and (f, r1 + d) not in occ:
                emit(rest | {(f, r1 + d)}, theirs, ((f, r1), (f, r1 + d), "B" if side == "W" else "W"))
        for df in (-1, 1):
            g = B.nb(f, df)
            if g is None:
                continue
            t = (g, r1)
            if t in theirs:
                emit(rest | {t}, theirs - {t})
            elif tgt and tgt[0] == t:
                emit(rest | {t}, theirs - {tgt[1]})
    return list(dict.fromkeys(out))


def ep_capturable(B, st, side, s):
    """cylcgt's test: side's pawn on s may be taken e.p. right now."""
    w, b, ep = st
    if not (ep and ep[1] == s and ep[2] != side):
        return False
    theirs = b if side == "W" else w
    return any((B.nb(s[0], df), s[1]) in theirs for df in (-1, 1) if B.nb(s[0], df) is not None)


def pawn_passed(B, st, side, p):
    """e.p.-aware passed test (cylcgt PASSED_RESPECTS_EP = True) for one pawn."""
    w, b, _ = st
    theirs = b if side == "W" else w
    files = {p[0]} | {B.nb(p[0], df) for df in (-1, 1)} - {None}
    if side == "W":
        blocked = any(g in files and s > p[1] for g, s in theirs)
    else:
        blocked = any(g in files and s < p[1] for g, s in theirs)
    return not blocked and not ep_capturable(B, st, side, p)


def has_passer(B, st, side):
    mine = st[0] if side == "W" else st[1]
    return any(pawn_passed(B, st, side, p) for p in mine)


def dp(B, side, p):
    """Moves a pawn needs to promote on its own (cylcgt promote_distance for one pawn)."""
    if side == "W":
        return B.H - p[1] - (1 if p[1] == 2 else 0)
    return p[1] - 1 - (1 if p[1] == B.H - 1 else 0)


def promote_distance(B, st, side):
    w, b, _ = st
    mine = w if side == "W" else b
    occ = w | b
    best = INF
    for p in mine:
        if not pawn_passed(B, st, side, p):
            continue
        ahead = range(p[1] + 1, B.H + 1) if side == "W" else range(1, p[1])
        if any((p[0], s) in occ for s in ahead):
            continue
        best = min(best, dp(B, side, p))
    return best


def credit(B, st, mover):
    """cylcgt's credit of a terminal reached by a move of `mover` (count rule for races); None if not terminal."""
    other = "B" if mover == "W" else "W"
    pm, po = has_passer(B, st, mover), has_passer(B, st, other)
    if not (pm or po):
        return None
    if pm and po:
        return other if promote_distance(B, st, other) <= promote_distance(B, st, mover) else mover
    return mover if pm else other


def file_groups(B, files):
    fs = sorted(set(files))
    groups = []
    for f in fs:
        if groups and f == groups[-1][-1] + 1:
            groups[-1].append(f)
        else:
            groups.append([f])
    if B.wrap and len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == B.W - 1:
        groups[0] = groups.pop() + groups[0]
    return groups


# ---------- input ----------

def parse(text, B):
    tok = text.split()
    if "/" in tok[0]:
        rows = tok[0].split("/")
        if len(rows) != B.H:
            raise ValueError(f"FEN has {len(rows)} ranks, board has {B.H}")
        pieces = {}
        for i, row in enumerate(rows):
            r, f = B.H - i, 0
            for ch in row:
                if ch.isdigit():
                    f += int(ch)
                else:
                    pieces[(f, r)] = ch
                    f += 1
            if f != B.W:
                raise ValueError(f"FEN rank {r} has {f} files, board has {B.W}")
        stm = tok[1] if len(tok) > 1 else "w"
        ep = tok[3] if len(tok) > 3 else "-"
    else:
        pieces = {}
        rest = []
        for t in tok:
            if len(t) >= 3 and t[0] in "KQRBNPkqrbnp" and t[1] in FILES:
                pieces[sqp(t[1:])] = t[0]
            else:
                rest.append(t)
        stm = rest[0] if rest else "w"
        ep = rest[1] if len(rest) > 1 else "-"
    return pieces, stm, (None if ep == "-" else sqp(ep))


def arc(B, files):
    """Shortest arc (cylinder) or interval (flat) holding all `files`."""
    fs = sorted(set(files))
    if not B.wrap or len(fs) == 1:
        return list(range(fs[0], fs[-1] + 1))
    gaps = [((fs[(i + 1) % len(fs)] - fs[i]) % B.W, i) for i in range(len(fs))]
    g, i = max(gaps)
    start = fs[(i + 1) % len(fs)]
    return [(start + j) % B.W for j in range(B.W - g + 1)]


# ---------- the checker ----------

class Checker:
    def __init__(self, B, tmax=8, cap=300000, ctx=False, budget=50):
        self.B, self.tmax, self.cap, self.ctx, self.budget = B, tmax, cap, ctx, budget

    # --- separation ---
    def separate(self, pieces, stm, ep, fz_opt, group_opt):
        B = self.B
        R = {"verdict": "PASS"}
        wk = [s for s, c in pieces.items() if c == "K"]
        bk = [s for s, c in pieces.items() if c == "k"]
        off = [nm(s) for s, c in pieces.items() if c not in "KkPp"]
        fails = []
        if len(wk) != 1 or len(bk) != 1:
            return {"verdict": "FAILS", "witness": "not exactly one king per side"}
        wk, bk = wk[0], bk[0]
        wp = frozenset(s for s, c in pieces.items() if c == "P")
        bp = frozenset(s for s, c in pieces.items() if c == "p")
        if off:
            fails.append(f"officer on {', '.join(off)}")
        if any(p[1] in (1, B.H) for p in wp | bp):
            fails.append("pawn on its first or last rank")
        if B.kdist(wk, bk) <= 1:
            fails.append("kings adjacent")
        if B.H < 5:
            fails.append("fewer than 5 ranks (Proposition 2.10(a) and the e.p. arguments need H >= 5)")
        if group_opt:
            decl = {}
            for t in group_opt.split(","):
                decl[sqp(t[1:])] = t[0]
            for s, c in decl.items():
                if pieces.get(s) != c:
                    fails.append(f"declared group piece {c}{nm(s)} is not on the board")
            fz = arc(B, [s[0] for s in decl])
        elif fz_opt:
            fz = [FILES.index(x) for x in fz_opt.split(",")]
            fz = arc(B, fz)
        else:
            fz = arc(B, [wk[0], bk[0]])
        FZ = set(fz)
        if wk[0] not in FZ or bk[0] not in FZ:
            fails.append("a king is not on F_Z")
        buf = sorted({g for g in range(B.W) if g not in FZ and min(B.fdist(g, f) for f in FZ) == 1})
        if len(FZ) + len(buf) >= B.W:
            fails.append("no file left for a context")
        if group_opt:
            und = [nm(p) for p in sorted(wp | bp) if p[0] in FZ and p not in decl]
            if und:
                fails.append(f"pawn(s) {', '.join(und)} on F_Z are not part of the declared group (component pawn on a group file)")
        inbuf = [nm(p) for p in sorted(wp | bp) if p[0] in buf]
        if inbuf:
            fails.append(f"pawn(s) {', '.join(inbuf)} on the buffer file(s) {', '.join(FILES[g] for g in buf)}")
        pos = (wk, bk, wp, bp, None)
        white = stm == "w"
        if in_check(B, pos, not white):
            fails.append("the side not to move is in check (illegal position)")
        if in_check(B, pos, white):
            chk = [nm(p) for p in (bp if white else wp) if p in
                   {(B.nb((wk if white else bk)[0], df), (wk if white else bk)[1] + (1 if white else -1)) for df in (-1, 1)}]
            fails.append(f"the side to move is in check (by {', '.join(chk)}); (V1a) fails by Proposition 1.15(a)")
        ctx_files = [g for g in range(B.W) if g not in FZ and g not in buf]
        R["F_Z"] = [FILES[f] for f in fz]
        R["buffer"] = [FILES[g] for g in buf]
        R["context_files"] = [FILES[g] for g in ctx_files]
        R["files_left_for_components"] = len(ctx_files)
        zw = frozenset(p for p in wp if p[0] in FZ)
        zb = frozenset(p for p in bp if p[0] in FZ)
        R["king_group"] = " ".join(["K" + nm(wk)] + ["P" + nm(p) for p in sorted(zw)] + ["k" + nm(bk)]
                                   + ["p" + nm(p) for p in sorted(zb)])
        cw, cb = wp - zw, bp - zb
        R["context"] = " ".join(["P" + nm(p) for p in sorted(cw)] + ["p" + nm(p) for p in sorted(cb)])
        if fails:
            R["verdict"] = "FAILS"
            R["witness"] = fails
            return R
        if getattr(self, "FZ", None) != FZ:  # the local-game memo depends only on the board and F_Z
            for k in ("loc_True", "loc_False"):
                self.__dict__.pop(k, None)
        for k in ("uns_True", "uns_False"):
            self.__dict__.pop(k, None)
        self.FZ, self.buf = FZ, set(buf)
        self.wk, self.bk, self.zw, self.zb = wk, bk, zw, zb
        self.cw, self.cb = frozenset(cw), frozenset(cb)
        self.stm = stm
        # the root e.p. right: on F_Z it concerns Z-pawns only; off F_Z it goes with the context
        self.ep_z = None
        self.ep_ctx = None
        if ep is not None:
            if ep[0] in FZ:
                self.ep_z = ep
            else:
                vr = ep[1] - 1 if white else ep[1] + 1
                self.ep_ctx = (ep, (ep[0], vr), "W" if white else "B")
        return R

    # --- reachable contexts (over-approximation: any order of moves per component) ---
    def enumerate_context(self):
        B = self.B
        root = (self.cw, self.cb, self.ep_ctx)
        if credit(B, root, "B" if self.stm == "w" else "W") is not None:
            raise ValueError("root has a passer")
        comps = []
        groups = file_groups(B, [p[0] for p in self.cw | self.cb])
        total = 0
        for g in groups:
            fs = set(g)
            ep = self.ep_ctx if (self.ep_ctx and self.ep_ctx[0][0] in fs) else None
            st0 = (frozenset(p for p in self.cw if p[0] in fs), frozenset(p for p in self.cb if p[0] in fs), ep)
            seen = {st0}
            stack = [st0]
            terms = []
            while stack:
                st = stack.pop()
                for side in ("W", "B"):
                    for ch in pawn_children(B, st, side):
                        variants = [ch] if ch[2] is None else [ch, (ch[0], ch[1], None)]
                        for i, v in enumerate(variants):
                            mover = side if i == 0 else ("B" if side == "W" else "W")
                            c = credit(B, v, mover)
                            if c is not None:
                                terms.append((v, mover))
                            elif v not in seen:
                                seen.add(v)
                                stack.append(v)
                                total += 1
                                if total > self.cap:
                                    raise Limit("context enumeration exceeds the state cap")
            terms = list(dict.fromkeys(terms))
            comps.append({"files": g, "states": seen, "terms": terms})
        self.comps = comps
        self.ncomp_root = len(groups)
        for c in comps:
            for side in ("W", "B"):
                c["dmin_" + side] = min((dp(B, side, p) for st in c["states"]
                                         for p in (st[0] if side == "W" else st[1])), default=INF)
                c["mu_" + side] = self.multi_mu(c["states"], side)
                # a terminal of another component can be the position of this one at a terminal of the whole
                # board (a move here makes a passer here and lets an e.p. right lapse there: a race of two
                # components), so the bounds used at terminals also run over this component's terminal states
                tst = c["states"] | {t[0] for t in c["terms"]}
                c["dmin_t_" + side] = min((dp(B, side, p) for st in tst
                                           for p in (st[0] if side == "W" else st[1])), default=INF)
                c["mu_t_" + side] = self.multi_mu(tst, side)

    def multi_mu(self, states, side, limit=None):
        """min over states of mu_side: least number of consecutive side-moves to a promotion (pawns only)."""
        B = self.B
        limit = limit or B.H + 1
        last = B.H if side == "W" else 1
        front = {(st[0], st[1], None) for st in states}
        seen = set(front)
        for lev in range(1, limit + 1):
            nxt = set()
            for st in front:
                for ch in pawn_children(B, st, side):
                    ch = (ch[0], ch[1], None)
                    mine = ch[0] if side == "W" else ch[1]
                    if any(p[1] == last for p in mine):
                        return lev
                    if ch not in seen:
                        seen.add(ch)
                        nxt.add(ch)
            front = nxt
            if not front:
                return INF
        return INF

    # --- (V1) ---
    def check_v1(self):
        B = self.B
        R = {"check": {"verdict": "CERTIFIED", "why": "nobody in check at X; by Proposition 1.15(a) no check "
                                                        "arises before the first decisive event"}}
        usable = []
        for c in self.comps:
            for st in c["states"]:
                ep = st[2]
                if ep and ep_capturable(B, st, "W" if ep[2] == "B" else "B", ep[1]):
                    usable.append((c, st))
        if not usable:
            R["E"] = {"verdict": "CERTIFIED", "why": "no reachable context carries a usable e.p. right (L1.6 (E) "
                                                     "holds vacuously)"}
        else:
            multi = [(c, st) for c, st in usable if self.ncomp_root >= 2 or len(file_groups(B, [p[0] for p in st[0] | st[1]])) >= 2]
            if not multi:
                R["E"] = {"verdict": "CERTIFIED", "why": "usable e.p. rights occur only in one-component contexts"}
            else:
                c, st = multi[0]
                root = self.ep_ctx is not None and st == (frozenset(p for p in self.cw if p[0] in c["files"]),
                                                         frozenset(p for p in self.cb if p[0] in c["files"]), self.ep_ctx)
                v = "FAILS" if root else "UNDECIDED"
                R["E"] = {"verdict": v, "witness": f"usable e.p. right on {nm(st[2][0])} with >= 2 context "
                                                   f"components ({'at the root' if root else 'in a reachable context'})"}
        # (V1b)
        att = {"W": set(), "B": set()}  # squares attacked by some reachable context pawn of that colour
        for c in self.comps:
            for st in c["states"]:
                for p in st[0]:
                    for df in (-1, 1):
                        if B.nb(p[0], df) is not None:
                            att["W"].add((B.nb(p[0], df), p[1] + 1))
                for p in st[1]:
                    for df in (-1, 1):
                        if B.nb(p[0], df) is not None:
                            att["B"].add((B.nb(p[0], df), p[1] - 1))
        R["V1b"] = {}
        zpos = (self.wk, self.bk, self.zw, self.zb, None)
        for white, side in ((True, "white"), (False, "black")):
            safe = [m for m in moves(B, zpos, white) if m[0] == "P" or m[2][0] in self.FZ
                    or (self.ctx and m[2][0] in self.buf and m[2] not in att["B" if white else "W"])]
            if safe:
                R["V1b"][side] = {"verdict": "CERTIFIED", "move": mv_name(safe[0], white),
                                  "why": "a Z-move legal in every reachable context (Lemma 2.2)"}
            else:
                R["V1b"][side] = {"verdict": "UNDECIDED", "why": "no Z-move is legal in every reachable context"}
        white = self.stm == "w"
        full = (self.wk, self.bk, self.zw | self.cw, self.zb | self.cb,
                self.ep_z or (self.ep_ctx[0] if self.ep_ctx else None))
        if not moves(B, full, white) and not in_check(B, full, white):
            R["V1b"]["white" if white else "black"] = {"verdict": "FAILS", "witness": "stalemate at X"}
        return R

    # --- the local game of Definition 2.6 ---
    def local(self, s_white):
        key = "loc_" + str(s_white)
        if not hasattr(self, key):
            setattr(self, key, ({}, {}))
        return getattr(self, key)

    def A(self, pos, t, s_white):
        """s to move, s-bar has t moves left: does s-bar win (L1_P)?"""
        memo = self.local(s_white)[0]
        key = (pos, t)
        if key in memo:
            return memo[key]
        if len(memo) % 1000 == 0 and time.process_time() > self.deadline:
            raise Limit(f"CPU budget of {self.budget} s exceeded in the local game")
        B = self.B
        ms = moves(B, pos, s_white)
        chk = in_check(B, pos, s_white)
        if not ms and chk:
            res = True
        elif t == 0 or any(m[3] for m in ms):
            res = False
        else:
            opts = [m[4] for m in ms] + ([] if chk else [pos[:4] + (None,)])
            res = all(self.Bn(o, t, s_white) for o in opts)
        memo[key] = res
        return res

    def Bn(self, pos, t, s_white):
        memo = self.local(s_white)[1]
        key = (pos, t)
        if key in memo:
            return memo[key]
        res = False
        for m in self.sbar_moves(pos, s_white):
            if m[3] or self.A(m[4], t - 1, s_white):
                res = True
                break
        memo[key] = res
        return res

    def sbar_moves(self, pos, s_white):
        return [m for m in moves(self.B, pos, not s_white) if m[0] == "P" or m[2][0] in self.FZ]

    def l3f(self, Q, T, s_white):
        """(L3_F): on every line where s-bar plays only winning moves, s has a Z-pawn move or a king move onto F_Z."""
        B = self.B
        seen = {(Q, T)}
        stack = [(Q, T)]
        while stack:
            pos, t = stack.pop()
            ms = moves(B, pos, s_white)
            chk = in_check(B, pos, s_white)
            if not ms and chk:
                continue
            if not any(m[0] == "P" or m[2][0] in self.FZ for m in ms):
                return False
            for o in [m[4] for m in ms if not m[3]] + ([] if chk else [pos[:4] + (None,)]):
                for m in self.sbar_moves(o, s_white):
                    if not m[3] and self.A(m[4], t - 1, s_white) and (m[4], t - 1) not in seen:
                        seen.add((m[4], t - 1))
                        stack.append((m[4], t - 1))
        return True

    def l2_ok(self, s_white, ksq, T):
        """(L2): mu_s >= T + 1 at every reachable context, for s's king on ksq after m."""
        if T == 0:
            return True, "no window"
        if T == 1 and self.B.H >= 5:
            return True, "Proposition 2.10(a) (T = 1, H >= 5)"
        side = "W" if s_white else "B"
        dmin = min((c["dmin_" + side] for c in self.comps), default=INF)
        if dmin >= T + 1:
            return True, (f"every reachable {side} context pawn needs >= {dmin} moves" if dmin < INF
                          else f"no {side} context pawn")
        for c in self.comps:
            m = self.king_mu(c, side, ksq, T)
            if m <= T:
                return False, f"a {side} context pawn can promote in {m} moves with its king's help (component " \
                              f"{''.join(FILES[f] for f in c['files'])})"
        return True, f"breadth-first search with the king from {nm(ksq)}: mu_s >= {T + 1} in every reachable context"

    def king_mu(self, comp, side, ksq, T):
        """min over the component's reachable states of mu_s in Q-degree, within T levels (else T + 1)."""
        B = self.B
        white = side == "W"
        last = B.H if white else 1
        front = {(ksq, st[0], st[1]) for st in comp["states"]}
        seen = set(front)
        n = 0
        for lev in range(1, T + 1):
            nxt = set()
            for k, w, b in front:
                mine, theirs = (w, b) if white else (b, w)
                for t in B.steps(k):
                    if t in mine:
                        continue
                    nt = theirs - {t}
                    if attacked(B, t, nt, not white):
                        continue
                    ch = (t, w, nt) if white else (t, nt, b)
                    if ch not in seen:
                        seen.add(ch)
                        nxt.add(ch)
                for ch in pawn_children(B, (w, b, None), side, frozenset([k])):
                    nw, nb_, _ = ch
                    nmine = nw if white else nb_
                    if any(p[1] == last for p in nmine):
                        return lev
                    c2 = (k, nw, nb_)
                    if c2 not in seen:
                        seen.add(c2)
                        nxt.add(c2)
                n += 1
                if n > 4 * self.cap:
                    raise Limit("(L2) search exceeds the cap")
            front = nxt
        return T + 1

    # --- (V3): every Z-move of each side, Theorem 2.7(a) ---
    def check_v3(self):
        B = self.B
        R = {}
        self.sortie_T = {}
        for s_white, side in ((True, "white"), (False, "black")):
            zpos = (self.wk, self.bk, self.zw, self.zb, None)
            ms = moves(B, zpos, s_white)
            if self.ep_z and (self.stm == "w") == s_white:
                ms += [m for m in moves(B, zpos[:4] + (self.ep_z,), s_white) if m not in ms]
            rows = []
            for m in ms:
                try:
                    rows.append(self.certify_sortie(m, s_white))
                except Limit as e:
                    rows.append({"move": mv_name(m, s_white), "verdict": "UNDECIDED", "why": str(e)})
            self.sortie_T[s_white] = rows
            bad = [r for r in rows if r["verdict"] != "CERTIFIED"]
            if not rows:
                v = {"verdict": "CERTIFIED", "why": "no legal Z-move"}
            elif not bad:
                v = {"verdict": "CERTIFIED"}
            elif any(r["verdict"] == "FAILS" for r in bad):
                v = {"verdict": "FAILS", "witness": [r["move"] for r in bad if r["verdict"] == "FAILS"][0]}
            else:
                v = {"verdict": "UNDECIDED", "witness": bad[0]["move"]}
            v["sorties"] = rows
            R[side] = v
        return R

    def certify_sortie(self, m, s_white):
        B = self.B
        name = mv_name(m, s_white)
        if m[3]:
            return {"move": name, "verdict": "FAILS", "why": "the Z-move promotes: a P-win for the mover"}
        after = m[4]
        ksq = after[0] if s_white else after[1]
        replies = moves(B, after, not s_white)
        if any(r[3] and (r[0] == "P") for r in replies):
            r = [r for r in replies if r[3]][0]
            return {"move": name, "verdict": "CERTIFIED", "reply": mv_name(r, not s_white), "T": 0,
                    "why": "the reply promotes at once (P-win)"}
        best = strict = None  # (T, r, how): least T with (L1_P) and (L3_F) [strict], or with (L3) by --ctx
        for r in replies:
            if r[0] == "K" and r[2][0] not in self.FZ:
                continue
            Q = r[4]
            for T in range(1, self.tmax + 1):
                if self.A(Q, T, s_white):
                    if self.l3f(Q, T, s_white):
                        strict = min(strict or (T + 1,), (T, r, "(L3_F)"), key=lambda x: x[0])
                        best = min(best or (T + 1,), (T, r, "(L3_F)"), key=lambda x: x[0])
                        break
                    if self.ctx and self.l3c(Q, T, s_white):
                        best = min(best or (T + 1,), (T, r, "(L3) over the reachable contexts (--ctx)"),
                                   key=lambda x: x[0])
            if strict and strict[0] == 1:
                break
        if best is None:
            l1 = [(T, r) for r in replies if r[0] == "P" or r[2][0] in self.FZ
                  for T in [next((T for T in range(1, self.tmax + 1) if self.A(r[4], T, s_white)), None)] if T]
            if l1:
                T, r = min(l1, key=lambda x: x[0])
                return {"move": name, "verdict": "UNDECIDED", "L1_P": {"reply": mv_name(r, not s_white), "T": T},
                        "why": "(L1_P) holds but (L3_F) fails for every reply" +
                               (" and (L3) is not shown over the contexts" if self.ctx else "")}
            return {"move": name, "verdict": "UNDECIDED", "why": f"no reply r gives (L1_P) within T <= {self.tmax}"}
        T, r, how = best
        ok, why = self.l2_ok(s_white, ksq, T)
        row = {"move": name, "reply": mv_name(r, not s_white), "T": T, "L3": how, "L2": why}
        if strict:
            row["T_strict"] = strict[0]
        row["verdict"] = "CERTIFIED" if ok else "UNDECIDED"
        if not ok:
            row["why"] = "(L2) fails or is not shown: " + why
        return row

    def unsafe(self, s_white):
        """Squares off F_Z where s's king might be blocked or attacked by a context pawn in some window position:
        squares of s-bar context pawns and squares they attack (reachable contexts; they never move in the
        window), and the forward cones of s's context pawns on the context files (Lemma 2.2)."""
        key = "uns_" + str(s_white)
        if hasattr(self, key):
            return getattr(self, key)
        B = self.B
        ctx = {g for g in range(B.W) if g not in self.FZ and g not in self.buf}
        bad = set()
        for c in self.comps:
            for st in c["states"]:
                mine, theirs = (st[0], st[1]) if s_white else (st[1], st[0])
                for p in theirs:
                    bad.add(p)
                    for df in (-1, 1):
                        if B.nb(p[0], df) is not None:
                            bad.add((B.nb(p[0], df), p[1] + (-1 if s_white else 1)))
                for p in mine:
                    for r in range(1, B.H + 1):
                        if (r - p[1]) * (1 if s_white else -1) >= 0:
                            for g in ctx:
                                if B.fdist(g, p[0]) <= abs(r - p[1]):
                                    bad.add((g, r))
        setattr(self, key, bad)
        return bad

    def l3c(self, Q, T, s_white):
        """(L3) checked directly (--ctx): on every line where s-bar plays only winning moves, s has a local move
        that is legal in every real position projecting to it: a Z-pawn move, a king step onto F_Z, or a king
        step onto a square outside unsafe()."""
        B = self.B
        bad = self.unsafe(s_white)
        seen = {(Q, T)}
        stack = [(Q, T)]
        while stack:
            pos, t = stack.pop()
            ms = moves(B, pos, s_white)
            chk = in_check(B, pos, s_white)
            if not ms and chk:
                continue
            if not any(m[0] == "P" or m[2][0] in self.FZ or m[2] not in bad for m in ms):
                return False
            for o in [m[4] for m in ms if not m[3]] + ([] if chk else [pos[:4] + (None,)]):
                for m in self.sbar_moves(o, s_white):
                    if not m[3] and self.A(m[4], t - 1, s_white) and (m[4], t - 1) not in seen:
                        seen.add((m[4], t - 1))
                        stack.append((m[4], t - 1))
        return True

    # --- (V2) at passer and race terminals ---
    def check_v2_passers(self, only_credit=None):
        B = self.B
        zall = self.zw | self.zb
        root_files = {p[0] for p in self.cw | self.cb} | {p[0] for p in zall}
        stat = {}
        for beta in ("W", "B"):
            kb, kw = (self.wk, self.bk) if beta == "W" else (self.bk, self.wk)
            h2 = not any(p[0] in {B.nb(kb[0], -1), B.nb(kb[0], 1)} for p in zall)
            h3 = any(B.kdist(t, kb) >= 2 and not ({t[0], B.nb(t[0], -1), B.nb(t[0], 1)} & root_files)
                     for t in B.steps(kw))
            omega_white = beta == "B"
            zmoves = [m for m in moves(B, (self.wk, self.bk, self.zw, self.zb, None), omega_white)]
            zpawn = [m for m in zmoves if m[0] == "P"]
            Ts = [0 if r.get("T") == 0 else r.get("T_strict")
                  for r in self.sortie_T[omega_white] if r["move"][0] in "Kk"]
            stat[beta] = {"H2": h2, "H3": h3, "omega_zpawn_moves": [mv_name(m, omega_white) for m in zpawn],
                          "omega_king_T": Ts}
        n = 0
        for c in self.comps:
            for st, mover in c["terms"]:
                N = "B" if mover == "W" else "W"
                beta = credit(B, st, mover)
                if only_credit and beta != only_credit:
                    continue
                n += 1
                ok, why = self.cert_terminal(c, st, mover, N, beta, stat[beta])
                if not ok:
                    return {"verdict": "UNDECIDED", "terminals_checked": n,
                            "witness": f"terminal W: {' '.join(nm(p) for p in sorted(st[0]))} / B: "
                                       f"{' '.join(nm(p) for p in sorted(st[1]))} after a move of {mover}, "
                                       f"credited to {beta}: {why}"}
        if n == 0:
            return {"verdict": "CERTIFIED", "why": "no passer or race terminal is reachable" +
                    (f" with credit {only_credit}" if only_credit else "")}
        return {"verdict": "CERTIFIED", "terminals_checked": n,
                "why": "Corollary 2.11a (H1)-(H5) at every terminal, carried to P by Corollary 2.7' with "
                       "Theorem 2.7(a) at the nodes of the push" +
                       ("" if B.wrap else "; flat board: Proposition 2.11 is written out for cylinders, and LOOPY "
                                          "says the flat proof is the same with the neighbouring files that exist")}

    def cert_terminal(self, comp, st, mover, N, beta, sb):
        B = self.B
        omega = "B" if beta == "W" else "W"
        if not sb["H2"]:
            return False, f"(H2) fails: a Z-pawn stands on a file next to {beta}'s king"
        if not sb["H3"]:
            return False, f"(H3) fails at {omega}'s king"
        if sb["omega_zpawn_moves"]:
            return False, f"{omega} has a Z-pawn move ({sb['omega_zpawn_moves'][0]}), so Z may change along the push"
        if any(T is None for T in sb["omega_king_T"]):
            return False, f"a king move of {omega} has no local certificate ((L1_P) and (L3_F))"
        Tmax_k = max(sb["omega_king_T"], default=0)
        w, b, ep = st
        mine = w if beta == "W" else b
        reasons = []
        for p in sorted(mine):
            if not pawn_passed(B, st, beta, p):
                continue
            ahead = range(p[1] + 1, B.H + 1) if beta == "W" else range(1, p[1])
            if any((p[0], r) in (w | b) for r in ahead):
                continue  # (H1): path not empty
            rho = (lambda q: q[1]) if beta == "W" else (lambda q: B.H + 1 - q[1])
            adj = {B.nb(p[0], -1), B.nb(p[0], 1)}
            if any(q[0] in adj and rho(q) > rho(p) + 1 for q in mine if q != p):
                reasons.append(f"(H4) fails for {nm(p)}")
                continue
            d = dp(B, beta, p)
            e = d if beta == mover else d - 1
            # (H5): mu_omega >= e + 1 over the own component (p deleted), the other components and Z (frozen)
            own = (w - {p}, b, ep if (ep and ep[2] == omega and N == omega) else None) if beta == "W" else \
                (w, b - {p}, ep if (ep and ep[2] == omega and N == omega) else None)
            mu = self.mu_from(own, omega, e + 1)
            others = min((c["mu_t_" + omega] for c in self.comps if c is not comp), default=INF)
            mu = min(mu, others)
            if mu < e + 1:
                reasons.append(f"(H5) fails for {nm(p)}: mu = {mu}, e = {e}")
                continue
            # Corollary 2.7': omega's king moves at the nodes of the push are P-losses (Theorem 2.7(a));
            # (L2) there: omega's context pawns need >= D0 - j moves after j omega-moves, j <= e - 1
            if e >= 1 and Tmax_k >= 1:
                om = b if omega == "B" else w
                d0 = min([dp(B, omega, q) for q in om] + [c["dmin_t_" + omega] for c in self.comps if c is not comp],
                         default=INF)
                if d0 - (e - 1) < Tmax_k + 1 and not (Tmax_k == 0):
                    reasons.append(f"(L2) at the nodes of the push not shown for {nm(p)}: D0 = {d0}, e = {e}, "
                                   f"T = {Tmax_k}")
                    continue
            return True, f"p = {nm(p)}"
        return False, "; ".join(reasons) or "(H1) fails for every pawn of the beneficiary"

    def mu_from(self, st, side, limit):
        """mu in G_omega from one state (e.p. right usable only as the first move)."""
        B = self.B
        last = B.H if side == "W" else 1
        front = {st}
        seen = {st}
        for lev in range(1, limit + 1):
            nxt = set()
            for s0 in front:
                for ch in pawn_children(B, s0, side):
                    ch = (ch[0], ch[1], None)
                    if any(p[1] == last for p in (ch[0] if side == "W" else ch[1])):
                        return lev
                    if ch not in seen:
                        seen.add(ch)
                        nxt.add(ch)
            front = nxt
        return INF

    # --- the D-game: pawn moves of the context with chess e.p., first passer ends, no move loses ---
    def d_result(self, side):
        B = self.B
        memo = {}

        def win(st, s):
            key = (st, s)
            if key in memo:
                return memo[key]
            if len(memo) > self.cap:
                raise Limit("D-game exceeds the cap")
            res = False
            o = "B" if s == "W" else "W"
            for ch in pawn_children(B, st, s):
                c = credit(B, ch, s)
                if c is not None:
                    if c == s:
                        res = True
                        break
                    continue
                if not win(ch, o):
                    res = True
                    break
            memo[key] = res
            return res

        return win((self.cw, self.cb, self.ep_ctx), side)

    # --- everything ---
    def run(self, text, fz=None, group=None):
        B = self.B
        pieces, stm, ep = parse(text, B)
        self.deadline = time.process_time() + self.budget
        out = {"position": text.strip(), "board": f"{'cyl' if B.wrap else 'flat'}:{B.W}x{B.H}",
               "side_to_move": stm}
        sep = self.separate(pieces, stm, ep, fz, group)
        out["separation"] = sep
        und = {"verdict": "UNDECIDED", "why": "separation fails"}
        if sep["verdict"] != "PASS":
            out.update({"V1": und, "V2": und, "V3": und, "verdict": "FAILS",
                        "proves": "nothing: the position is not a king group with a buffer (Definition 2.1)"})
            return out
        try:
            self.enumerate_context()
        except ValueError as e:
            u = {"verdict": "UNDECIDED", "why": str(e) + " (outside Theorem 1.14)"}
            out.update({"V1": u, "V2": u, "V3": u, "verdict": "UNDECIDED", "proves": "nothing"})
            return out
        except Limit as e:
            u = {"verdict": "UNDECIDED", "why": str(e)}
            out.update({"V1": u, "V2": u, "V3": u, "verdict": "UNDECIDED", "proves": "nothing"})
            return out
        out["reachable_context_states"] = sum(len(c["states"]) for c in self.comps)
        v1 = self.check_v1()
        v3 = self.check_v3()
        try:
            v2p = self.check_v2_passers()
        except Limit as e:
            v2p = {"verdict": "UNDECIDED", "why": str(e)}
        out["V1"] = v1
        out["V3"] = v3
        v3all = combine([v3["white"]["verdict"], v3["black"]["verdict"]])
        out["V2"] = {"passer_and_race_terminals": v2p,
                     "z_move_terminals": {"verdict": v3all, "why": "the certificate of (V3) (Theorem 2.7(a))"},
                     "verdict": combine([v2p["verdict"], v3all])}
        v1all = combine([v1["check"]["verdict"], v1["E"]["verdict"], v1["V1b"]["white"]["verdict"],
                         v1["V1b"]["black"]["verdict"]])
        out["V1"]["verdict"] = v1all
        out["V3"]["verdict"] = v3all
        out["V4"] = "not checked (needed only for the BIG value S(X), Theorem 1.14(ii))"
        white = stm == "w"
        try:
            dwin = self.d_result("W" if white else "B")
            sigma = ("W" if white else "B") if dwin else ("B" if white else "W")
            out["D_result"] = {"side_to_move": "W" if dwin else "L",
                               "winner": "White" if sigma == "W" else "Black"}
        except Limit as e:
            sigma = None
            out["D_result"] = {"why": str(e)}
        if v1all == v3all == out["V2"]["verdict"] == "CERTIFIED":
            out["verdict"] = "CERTIFIED"
            out["proves"] = ("Theorem 1.14(i): P(X) = D(X), the normal-play result of the context components with Z "
                             "deleted" + (f"; here a P-win for {out['D_result']['winner']}" if sigma else "")
                             + ". Chess only under (A_Q)(X), not checked.")
            return out
        if sigma is not None:
            loser_white = sigma == "B"
            ls = "white" if loser_white else "black"
            try:
                v2s = self.check_v2_passers(only_credit=sigma)
            except Limit as e:
                v2s = {"verdict": "UNDECIDED", "why": str(e)}
            parts = {"V1a_check": v1["check"]["verdict"], "V1b_loser": v1["V1b"][ls]["verdict"],
                     "V3_loser": v3[ls]["verdict"], "V2_terminals_credited_to_winner": v2s["verdict"]}
            out["sharp_form"] = {"winner": "White" if sigma == "W" else "Black", "parts": parts,
                                 "V2_detail": v2s}
            if all(v == "CERTIFIED" for v in parts.values()):
                out["verdict"] = "CERTIFIED"
                out["proves"] = (f"sharp form of Theorem 1.14: X is a P-win for {out['sharp_form']['winner']} (the "
                                 "D-game winner). (E) is not needed for this form. Chess only under (A_Q)(X), "
                                 "not checked.")
                return out
        fails = [k for k in ("V1", "V2", "V3") if out[k]["verdict"] == "FAILS"]
        out["verdict"] = "FAILS" if fails else "UNDECIDED"
        out["proves"] = "nothing" + (f": {', '.join(fails)} fails as stated" if fails else "")
        return out


def combine(vs):
    if all(v == "CERTIFIED" for v in vs):
        return "CERTIFIED"
    if any(v == "FAILS" for v in vs):
        return "FAILS"
    return "UNDECIDED"


def main():
    args = sys.argv[1:]
    opt = {"--board": "flat:8x8", "--fz": None, "--group": None, "--tmax": "8", "--cap": "300000"}
    pretty = ctx = False
    pos = []
    i = 0
    while i < len(args):
        if args[i] in opt:
            opt[args[i]] = args[i + 1]
            i += 2
        elif args[i] in ("--pretty", "--ctx"):
            pretty, ctx = pretty or args[i] == "--pretty", ctx or args[i] == "--ctx"
            i += 1
        else:
            pos.append(args[i])
            i += 1
    kind, size = opt["--board"].split(":")
    W, H = map(int, size.split("x"))
    lines = pos or [l for l in sys.stdin if l.strip() and not l.startswith("#")]
    for text in lines:
        B = Board(W, H, kind == "cyl")
        res = Checker(B, int(opt["--tmax"]), int(opt["--cap"]), ctx).run(text, opt["--fz"], opt["--group"])
        print(json.dumps(res, indent=1 if pretty else None))


if __name__ == "__main__":
    main()
