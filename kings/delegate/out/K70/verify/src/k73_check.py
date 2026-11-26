"""K73 referee: independent checker of the case tables in kings/delegate/out/K70/PROOF.md.

Written from the prose conventions of PROOF.md ("How the remaining winning variations are proved",
"Why Kb4 and c4 draw") before reading anything in kings/delegate/out/K70/src/.

Run from the project root:  .venv/bin/python -B -I kings/delegate/out/K70/verify/src/k73_check.py [--dump DIR]

Game P: kings and pawns, chess moves (single/double steps, captures, e.p., check rule); the first promotion wins;
mate loses; stalemate draws.
"""
import re
import sys
from collections import defaultdict, Counter

import os
PROOF = os.environ.get("K73_PROOF", "kings/delegate/out/K70/PROOF.md")
MIXED_STRICT = os.environ.get("K73_MIXED_STRICT") == "1"

# ---------------------------------------------------------------- board
def sq(name):
    return (ord(name[0]) - 97) + 8 * (int(name[1]) - 1)


def nm(s):
    return "abcdefgh"[s % 8] + str(s // 8 + 1)


def F(s):
    return s % 8


def R(s):
    return s // 8


def kd(a, b):
    return max(abs(F(a) - F(b)), abs(R(a) - R(b)))


NEIGH = [[t for t in range(64) if t != s and kd(s, t) == 1] for s in range(64)]


def patt(side, p):
    """squares attacked by a pawn of side (0 White, 1 Black) on p"""
    r = R(p) + (1 if side == 0 else -1)
    if r < 0 or r > 7:
        return []
    return [f + 8 * r for f in (F(p) - 1, F(p) + 1) if 0 <= f < 8]


class Pos:
    __slots__ = ("wk", "bk", "wp", "bp", "stm", "ep")

    def __init__(self, wk, bk, wp, bp, stm, ep=None):
        self.wk, self.bk, self.wp, self.bp, self.stm, self.ep = wk, bk, frozenset(wp), frozenset(bp), stm, ep

    def key(self):
        return (self.wk, self.bk, self.wp, self.bp, self.stm, self.ep)

    def fen(self):
        rows = []
        for r in range(7, -1, -1):
            row, e = "", 0
            for f in range(8):
                s = f + 8 * r
                c = "K" if s == self.wk else "k" if s == self.bk else "P" if s in self.wp else "p" if s in self.bp else ""
                if not c:
                    e += 1
                    continue
                if e:
                    row += str(e)
                    e = 0
                row += c
            if e:
                row += str(e)
            rows.append(row)
        return "/".join(rows) + (" w" if self.stm == 0 else " b") + (" " + nm(self.ep) if self.ep is not None else " -")


def attacked_by_pawns(side_pawns_owner, pawns, s):
    """is s attacked by pawns of side side_pawns_owner"""
    return any(s in patt(side_pawns_owner, p) for p in pawns)


def in_check(p, side):
    if side == 0:
        return attacked_by_pawns(1, p.bp, p.wk)
    return attacked_by_pawns(0, p.wp, p.bk)


def legal_moves(p):
    """list of (token, result Pos or None, promo flag). Token: 'Ke4', 'Kxb7', 'c3', 'cxb3' (e.p. also 'cxb6')."""
    s = p.stm
    own = p.wp if s == 0 else p.bp
    opp = p.bp if s == 0 else p.wp
    mk = p.wk if s == 0 else p.bk
    ok = p.bk if s == 0 else p.wk
    out = []
    for t in NEIGH[mk]:
        if t in own or kd(t, ok) < 2:
            continue
        nopp = opp - {t}
        if attacked_by_pawns(1 - s, nopp, t):
            continue
        cap = t in opp
        if s == 0:
            q = Pos(t, p.bk, p.wp, nopp, 1)
        else:
            q = Pos(p.wk, t, nopp, p.bp, 0)
        out.append((("Kx" if cap else "K") + nm(t), q, False))
    d = 8 if s == 0 else -8
    last = 7 if s == 0 else 0
    home = 1 if s == 0 else 6
    occ = set(p.wp) | set(p.bp) | {p.wk, p.bk}
    for fr in own:
        cands = []
        to = fr + d
        if 0 <= to < 64 and to not in occ:
            cands.append((to, None, False))
            if R(fr) == home and (to + d) not in occ:
                cands.append((to + d, None, True))
        for df in (-1, 1):
            if not 0 <= F(fr) + df < 8:
                continue
            c = to + df
            if c in opp:
                cands.append((c, c, False))
            elif p.ep is not None and c == p.ep:
                cands.append((c, c - d, False))
        for dest, capsq, dbl in cands:
            nown = (own - {fr})
            nopp = opp - {capsq} if capsq is not None else opp
            promo = R(dest) == last
            if not promo:
                nown = nown | {dest}
            if s == 0:
                q = Pos(p.wk, p.bk, nown, nopp, 1)
            else:
                q = Pos(p.wk, p.bk, nopp, nown, 0)
            if in_check(q, s):
                continue  # own king left in check
            if dbl:
                # e.p. available to the opponent: an enemy pawn beside the arrival square whose capture is legal
                epsq = fr + d
                for df in (-1, 1):
                    if 0 <= F(dest) + df < 8 and (dest + df) in nopp:
                        # test legality of the e.p. capture for the opponent
                        e_own = (nopp - {dest + df}) | {epsq}
                        e_opp = nown - {dest}
                        if s == 0:
                            tq = Pos(p.wk, p.bk, e_opp, e_own, 0)
                        else:
                            tq = Pos(p.wk, p.bk, e_own, e_opp, 1)
                        if not in_check(tq, 1 - s):
                            q = Pos(q.wk, q.bk, q.wp, q.bp, q.stm, epsq)
                tok = nm(dest)
            elif capsq is not None:
                tok = "abcdefgh"[F(fr)] + "x" + nm(dest)
            else:
                tok = nm(dest)
            out.append((tok, None if promo else q, promo))
    return out


def reply_class(tok):
    """the class under which a reply is listed in the Replies column"""
    if tok.startswith("K") and not tok.startswith("Kx"):
        return "K"
    return tok


# ---------------------------------------------------------------- parsing
DASH = "–"


def parse_set(spec):
    spec = spec.strip()
    if spec == "*":
        return set(range(64))
    neg = spec.startswith("!")
    if neg:
        spec = spec[1:]
    u = set()
    for item in spec.split(","):
        item = item.strip()
        if DASH in item:
            a, b = item.split(DASH)
            a, b = sq(a), sq(b)
            for f in range(min(F(a), F(b)), max(F(a), F(b)) + 1):
                for r in range(min(R(a), R(b)), max(R(a), R(b)) + 1):
                    u.add(f + 8 * r)
        else:
            u.add(sq(item))
    return (set(range(64)) - u) if neg else u


HEAD = re.compile(r"^\*\*White pawn (\S+) · Black pawns (\S+), (\S+)\*\*\s*$")
ROW = re.compile(r"^\|\s*(\d+)\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|\s*$")


class Row:
    def __init__(self, table, num, wp, bp, king, ep, zone, play, replies, raw):
        self.table, self.num, self.wp, self.bp, self.king, self.ep = table, num, wp, bp, king, ep
        self.zone_spec, self.play, self.replies, self.raw = zone, play, replies, raw

    def label(self):
        return f"{self.table}{self.num}"


def parse_replies(txt):
    """'K→1,2 Kxb2→31 c3→121 end→P' -> dict class -> [nums] or terminal markers"""
    d = {}
    for tok in txt.split():
        if "→" not in tok:
            raise ValueError("bad reply token " + tok)
        a, b = tok.split("→")
        if a == "end":
            d.setdefault("end", []).append(b)
        else:
            if a in d:
                raise ValueError("duplicate reply class " + a)
            d[a] = [int(x) for x in b.split(",")]
    return d


def parse_proof(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    table = None
    head = None
    rows = {"B": {}, "D": {}}
    order = []
    for ln in lines:
        if ln.startswith("## Table B"):
            table = "B"
            continue
        if ln.startswith("## Table D"):
            table = "D"
            continue
        if ln.startswith("## ") and table:
            table = None
            continue
        if table is None:
            continue
        m = HEAD.match(ln)
        if m:
            wpn, b1, b2 = m.groups()
            wp = set() if wpn == "-" else {sq(wpn)}
            bp = {sq(x) for x in (b1, b2) if x != "-"}
            head = (frozenset(wp), frozenset(bp))
            continue
        m = ROW.match(ln)
        if m:
            num = int(m.group(1))
            kc = m.group(2).strip()
            ep = None
            mm = re.match(r"^(\w\d)\s*\(ep (\w\d)\)$", kc)
            if mm:
                kc, ep = mm.group(1), sq(mm.group(2))
            r = Row(table, num, head[0], head[1], sq(kc), ep, m.group(3).strip(), m.group(4).strip(),
                    parse_replies(m.group(5).strip()), ln)
            if num in rows[table]:
                raise ValueError("duplicate row " + table + str(num))
            rows[table][num] = r
            order.append(r)
    return rows, order


# ---------------------------------------------------------------- zones -> positions
def row_positions(r):
    """all positions of a row after the discards of the prose"""
    out = []
    occ = set(r.wp) | set(r.bp)
    for z in sorted(parse_set(r.zone_spec)):
        if z in occ or z == r.king or kd(z, r.king) <= 1:
            continue
        if r.table == "B":
            p = Pos(z, r.king, r.wp, r.bp, 1, r.ep)
            if in_check(p, 0):  # the other (White) king may not be in check on Black's turn
                continue
        else:
            p = Pos(r.king, z, r.wp, r.bp, 0, r.ep)
            if in_check(p, 1):
                continue
        out.append(p)
    return out


def row_member(r, p):
    if r.wp != p.wp or r.bp != p.bp or r.ep != p.ep:
        return False
    if r.table == "B":
        if p.stm != 1 or p.bk != r.king:
            return False
        other = p.wk
    else:
        if p.stm != 0 or p.wk != r.king:
            return False
        other = p.bk
    return other in r._zone


# ---------------------------------------------------------------- blockade F
def blockade_shape(p):
    """F of PROOF.md: Black to move, Black has a single c-pawn on rank r, White no pawn or one pawn on b6/b7"""
    if p.stm != 1 or len(p.bp) != 1:
        return None
    (b,) = tuple(p.bp)
    if F(b) != 2:
        return None
    if not (len(p.wp) == 0 or (len(p.wp) == 1 and tuple(p.wp)[0] in (sq("b6"), sq("b7")))):
        return None
    r = R(b) + 1
    W, K = p.wk, p.bk

    def S(f, rr):
        return f + 8 * (rr - 1) if 1 <= rr <= 8 else -1

    if 3 <= r <= 6:
        if (W == S(1, r - 2) and K == S(1, r)) or (W == S(3, r - 2) and K == S(3, r)):
            return "A"
        if W == S(2, r - 1):
            return "B"
        if W == S(2, r - 2) and K in (S(1, r + 1), S(2, r + 1), S(3, r + 1)):
            return "C"
    if r == 2 and W == sq("c1") and K in (sq("b3"), sq("d3")):
        return "L"
    return None


def legal_pos(p):
    if p.wk == p.bk or kd(p.wk, p.bk) < 2:
        return False
    occ = set(p.wp) | set(p.bp)
    if p.wk in occ or p.bk in occ or len(occ) != len(p.wp) + len(p.bp):
        return False
    if any(R(x) in (0, 7) for x in occ):
        return False
    if in_check(p, 1 - p.stm):
        return False
    return True


def blockade_instances():
    out = []
    for wpn in (None, "b6", "b7"):
        wp = set() if wpn is None else {sq(wpn)}
        for rk in range(2, 7):
            b = sq("c" + str(rk))
            for wk in range(64):
                for bk in range(64):
                    p = Pos(wk, bk, wp, {b}, 1)
                    if not legal_pos(p):
                        continue
                    if blockade_shape(p):
                        out.append(p)
    return out


# ---------------------------------------------------------------- the check
def main():
    dump = None
    if "--dump" in sys.argv:
        dump = sys.argv[sys.argv.index("--dump") + 1]
    rows, order = parse_proof(PROOF)
    for r in order:
        r._zone = set(p.wk if r.table == "B" else p.bk for p in row_positions(r))
    fails = []
    stats = Counter()
    notes = []

    def fail(msg):
        fails.append(msg)

    def find_rows(table, nums, p):
        hits = []
        for n in nums:
            r = rows[table].get(n)
            if r is None:
                fail(f"reference to missing row {table}{n}")
                continue
            if row_member(r, p):
                hits.append(n)
        return hits

    allpos = []  # (label, fen) for the solver comparison
    edges = defaultdict(set)  # row -> rows it actually uses
    empty_rows = []
    unused_classes = []
    # ---------------- Table B
    for r in [x for x in order if x.table == "B"]:
        ps = row_positions(r)
        if not ps:
            empty_rows.append(r.label())
        stats["B rows"] += 1
        used_classes = set()
        for p in ps:
            stats["B positions"] += 1
            allpos.append((r.label(), p.fen()))
            mv = {t: (q, pr) for t, q, pr in legal_moves(p)}
            if r.play not in mv:
                fail(f"{r.label()} {nm(p.wk)}: prescribed {r.play} illegal ({p.fen()})")
                continue
            q, promo = mv[r.play]
            if "end" in r.replies:
                if r.replies["end"] != ["P"] or len(r.replies) != 1:
                    fail(f"{r.label()}: odd terminal marker {r.replies}")
                if not promo:
                    fail(f"{r.label()} {nm(p.wk)}: end->P but {r.play} does not promote")
                stats["B terminal positions"] += 1
                continue
            if promo:
                notes.append(f"{r.label()}: promotes although replies are listed")
                continue
            wm = legal_moves(q)
            if not wm:
                if in_check(q, 0):
                    stats["B mates"] += 1
                    notes.append(f"{r.label()} {nm(p.wk)}: {r.play} mates")
                else:
                    fail(f"{r.label()} {nm(p.wk)}: {r.play} stalemates White ({q.fen()})")
                continue
            for t, q2, pr in wm:
                stats["B replies"] += 1
                if pr:
                    fail(f"{r.label()} {nm(p.wk)}: White reply {t} promotes")
                    continue
                cls = reply_class(t)
                if cls not in r.replies:
                    fail(f"{r.label()} {nm(p.wk)}: reply {t} (class {cls}) not listed; {q.fen()}")
                    continue
                used_classes.add(cls)
                nums = r.replies[cls]
                for n in nums:
                    if n >= r.num:
                        fail(f"{r.label()}: reference {n} not lower")
                hits = find_rows("B", nums, q2)
                if not hits:
                    fail(f"{r.label()} {nm(p.wk)}: reply {t} -> {q2.fen()} not in rows {nums}")
                    continue
                if len(hits) > 1:
                    stats["B replies in >1 cited row"] += 1
                for h in hits:
                    edges[r.label()].add("B" + str(h))
        for c in r.replies:
            if c != "end" and c not in used_classes:
                unused_classes.append(f"{r.label()}:{c}")
        for c, nums in r.replies.items():
            if c == "end":
                continue
            for n in nums:
                if "B" + str(n) not in edges[r.label()]:
                    unused_classes.append(f"{r.label()}:{c}->{n} (cited, never used)")
    # ---------------- Table D
    blockade_used = []
    for r in [x for x in order if x.table == "D"]:
        ps = row_positions(r)
        if not ps:
            empty_rows.append(r.label())
        stats["D rows"] += 1
        ends = r.replies.get("end", [])
        for p in ps:
            stats["D positions"] += 1
            allpos.append((r.label(), p.fen()))
            mv = {t: (q, pr) for t, q, pr in legal_moves(p)}
            if r.play not in mv:
                fail(f"{r.label()} {nm(p.bk)}: prescribed {r.play} illegal ({p.fen()})")
                continue
            q, promo = mv[r.play]
            if promo:
                if "P" not in ends:
                    notes.append(f"{r.label()}: promotes but no end->P")
                stats["D promote"] += 1
                continue
            if "P" in ends:
                fail(f"{r.label()} {nm(p.bk)}: end->P but no promotion")
                continue
            if "0" in ends:
                if q.bp:
                    fail(f"{r.label()} {nm(p.bk)}: end->0 but Black keeps pawns")
                else:
                    stats["D bare king"] += 1
                continue
            if "F" in ends and not (MIXED_STRICT and len(r.replies) > 1):
                shp = blockade_shape(q)
                if shp:
                    stats["D blockade"] += 1
                    blockade_used.append((r.label(), shp, q.fen()))
                    if len(r.replies) > 1:
                        stats["D mixed rows: F used"] += 1
                    continue
                if len(r.replies) == 1:
                    fail(f"{r.label()} {nm(p.bk)}: end->F but no blockade shape after {r.play}: {q.fen()}")
                    continue
                stats["D mixed rows: replies used"] += 1
            bm = legal_moves(q)
            if not bm:
                stats["D Black stalemated/mated"] += 1
                notes.append(f"{r.label()} {nm(p.bk)}: Black has no move after {r.play} ({'mate' if in_check(q,1) else 'stalemate'})")
                continue
            for t, q2, pr in bm:
                stats["D replies"] += 1
                if pr:
                    fail(f"{r.label()} {nm(p.bk)}: Black reply {t} promotes")
                    continue
                cls = reply_class(t)
                if cls not in r.replies:
                    fail(f"{r.label()} {nm(p.bk)}: reply {t} not listed; {q.fen()}")
                    continue
                hits = find_rows("D", r.replies[cls], q2)
                if not hits:
                    fail(f"{r.label()} {nm(p.bk)}: reply {t} -> {q2.fen()} not in D{r.replies[cls]}")
                    continue
                for h in hits:
                    edges[r.label()].add("D" + str(h))
    # ---------------- opening rule and entry rows
    entry = {
        "c2": {"K": [481, 486], "c3": [475, 480], "c4": [445, 448, 451]},
        "c3": {"K": [475, 480], "c4": [445, 448, 451]},
        "c4": {"K": [445, 448, 451], "c5": [414, 417]},
    }

    def opening_rule(pawn, x):
        if pawn in ("c2", "c3"):
            return "Kb5" if x == "d6" else "c5"
        if pawn == "c4":
            if x in ("d4", "d6"):
                return "Ka6"
            if x in ("d7", "e4", "e5", "e6", "e7"):
                return "Kc5"
            return "c5"
        if pawn == "c5":
            if x in ("d4", "d6"):
                return "Kb5"
            if x == "b4":
                return "DRAW"
            return "Kxc5"

    starts = []
    first_moves = 0
    entries = {}  # (gamma, wk) -> list of (white move, entry row)
    for g in ("c2", "c3", "c4"):
        for wk in range(64):
            p = Pos(wk, sq("b6"), {sq(g)}, {sq("b7"), sq("c6")}, 0)
            occ = {sq(g), sq("b7"), sq("c6"), sq("b6")}
            if wk in occ or kd(wk, sq("b6")) <= 1:
                continue
            starts.append((g, wk, p))
    stats["starts"] = len(starts)
    drawcase = None
    for g, wk, p in starts:
        lst = []
        for t, q, pr in legal_moves(p):
            first_moves += 1
            if pr:
                fail(f"start {g} K{nm(wk)}: White {t} promotes")
                continue
            cls = reply_class(t)
            pawn_after = nm(tuple(q.wp)[0])
            want = opening_rule(pawn_after, nm(q.wk))
            if want == "DRAW":
                drawcase = (g, nm(wk), t)
                lst.append((t, "draw"))
                continue
            nums = entry[g].get(cls)
            if nums is None:
                fail(f"start {g} K{nm(wk)}: move {t} has no entry")
                continue
            hits = find_rows("B", nums, q)
            if not hits:
                fail(f"start {g} K{nm(wk)}: move {t} -> {q.fen()} not in entry rows {nums}")
                continue
            for h in hits:
                if rows["B"][h].play != want:
                    fail(f"start {g} K{nm(wk)} {t}: entry row B{h} plays {rows['B'][h].play}, opening rule says {want}")
            lst.append((t, "B" + str(hits[0])))
        entries[(g, nm(wk))] = lst
    stats["first White moves"] = first_moves
    # ---------------- the drawn start: 1.c5+ enters D80/D81
    p = Pos(sq("b4"), sq("b6"), {sq("c4")}, {sq("b7"), sq("c6")}, 0)
    mvs = {t: q for t, q, pr in legal_moves(p)}
    dstart = sorted(mvs)
    q = mvs.get("c5")
    d_entries = []
    if q is None:
        fail("Kb4/c4: c5 illegal")
    else:
        for t, q2, pr in legal_moves(q):
            hits = find_rows("D", [80, 81], q2)
            d_entries.append((t, hits))
            if not hits:
                fail(f"Kb4/c4 1.c5+ {t}: not in D80/D81 ({q2.fen()})")
    # ---------------- blockade F instances
    inst = blockade_instances()
    # ---------------- report
    print("K73 checker of PROOF.md tables")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(f"  Table B rows parsed: {len(rows['B'])}, Table D rows parsed: {len(rows['D'])}")
    print(f"  rows with an empty zone after the discards: {empty_rows}")
    print(f"  Kb4/c4 White moves: {dstart}; 1.c5+ Black replies -> D rows: {d_entries}")
    print(f"  drawn start found by the opening rule: {drawcase}")
    print(f"  blockade F instances (legal, Black to move, all shapes, White pawn none/b6/b7): {len(inst)}")
    print(f"  F used in Table D at {len(blockade_used)} positions; shapes {Counter(s for _, s, _ in blockade_used)}")
    print(f"  cited row numbers never used by any position (class:row): {len(unused_classes)}")
    for u in unused_classes:
        print("     unused", u)
    print(f"  notes: {len(notes)}")
    for n in notes:
        print("     note", n)
    print(f"  FAILURES: {len(fails)}")
    for f_ in fails:
        print("     FAIL", f_)
    if dump:
        with open(dump + "/positions_B_D.txt", "w") as fh:
            for lab, fen in allpos:
                fh.write(f"{lab} {fen}\n")
        with open(dump + "/starts.txt", "w") as fh:
            for g, wk, p in starts:
                fh.write(f"{g} {nm(wk)} {p.fen()}\n")
        with open(dump + "/blockade.txt", "w") as fh:
            for p in inst:
                fh.write(f"F{blockade_shape(p)} {p.fen()}\n")
        with open(dump + "/edges.txt", "w") as fh:
            for k in sorted(edges, key=lambda s: (s[0], int(s[1:]))):
                fh.write(k + " " + " ".join(sorted(edges[k], key=lambda s: (s[0], int(s[1:])))) + "\n")
        with open(dump + "/entries.txt", "w") as fh:
            for (g, w), lst in sorted(entries.items()):
                fh.write(f"{g} {w} " + " ".join(f"{t}:{e}" for t, e in lst) + "\n")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
