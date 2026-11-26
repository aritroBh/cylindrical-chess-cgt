"""K77 referee: chess verdicts (Definition 4.8 read with tablebase values) for the new groups with at most seven men,
read offline from K67's cached Lichess (Syzygy) answers, unpacked into verify/tmp/tbc/.  Own FEN builder and own
reading; it does not import realchess or K67's tb67.py.

Reading (checked on the cache: a winning position's best move carries category 'loss'): the top-level category is
from the side to move; a move's category is from the side to move AFTER the move.  So a move loses for the mover iff
its category is 'win'.  Definition 4.8 in chess: (O1) at both Black-to-move roots the shuttle is legal and every other
Black move loses; (O2) at both White-to-move roots the non-losing White moves (the chess freezes) exist and none is a
promotion; (O3) after each chess freeze, q with Black to move: every Black move loses; (O4) q with White to move:
legal, and every White move loses.  Also checks that C034_01, C034_02 are reflected translates of C145_07, C145_09.
usage (repository root): python tbr77.py
"""
import glob, json, sys

V = "kings/delegate/out/K67/verify"
CACHE = {}
for f in glob.glob(V + "/tmp/tbc/tbcache/*/*.json"):
    r = json.load(open(f))
    CACHE[r["fen"]] = r

GROUPS = [("C014_01", "Ka5 Pa4 Pa6 Pb2 pa7", "c4", "c5"),
          ("C014_04", "Ke6 Pb5 Pe2 pa7 pb6 pe7", "d8", "e8"),
          ("C014_05", "Kf5 Pb5 Pe2 Pe6 pa7 pe7", "d5", "d6"),
          ("C034_01", "Kc4 Pd2 Pd5 Pe6 pd6 pe7", "e4", "e5"),
          ("C034_02", "Kf4 Pd6 Pe2 Pe5 pd7 pe6", "d4", "d5")]


def sq(s):
    return (ord(s[0]) - 97, int(s[1]))


def fen(pcs, stm, ep=None):
    """pcs: dict square -> letter (K k P p); ep: square behind a double-stepped pawn (kept only if a capture is legal)"""
    rows = []
    for r in range(8, 0, -1):
        row, e = "", 0
        for f in range(8):
            c = pcs.get((f, r))
            if c is None:
                e += 1
            else:
                row += (str(e) if e else "") + c; e = 0
        rows.append(row + (str(e) if e else ""))
    eps = "-"
    if ep:
        # side to move captures onto ep from the two adjacent files of the double-stepped pawn
        dr = -1 if stm == "w" else 1          # White captures from rank ep-1 (rank 5 onto 6); Black from rank 4 onto 3
        mine = "P" if stm == "w" else "p"
        if any(pcs.get((ep[0] + df, ep[1] + dr)) == mine for df in (-1, 1)):
            eps = "abcdefgh"[ep[0]] + str(ep[1])  # (no pin by a king and pawns can make it illegal here)
    return "%s %s - %s 0 1" % ("/".join(rows), stm, eps)


def look(f, need):
    r = CACHE.get(f)
    if r is None or r.get("data") is None:
        need.append(f)
        return None
    return r["data"]


def apply(pcs, uci):
    a, b = sq(uci[:2]), sq(uci[2:4])
    p = dict(pcs)
    c = p.pop(a)
    ep = None
    if c in "Pp" and a[0] != b[0] and b not in p:   # e.p. capture
        p.pop((b[0], a[1]), None)
    p[b] = c
    if c in "Pp" and abs(b[1] - a[1]) == 2:
        ep = (a[0], (a[1] + b[1]) // 2)
    return p, ep


def wattacks(pcs, s):
    return any(pcs.get((s[0] + df, s[1] - 1)) == "P" for df in (-1, 1))


need, out = [], []
for name, men, z0, z1 in GROUPS:
    base = {}
    for t in men.split():
        base[sq(t[1:])] = t[0]
    notes, lines = [], []
    for z, o in ((z0, z1), (z1, z0)):
        pcs = dict(base); pcs[sq(z)] = "k"
        rb = look(fen(pcs, "b"), need)
        rw = look(fen(pcs, "w"), need)
        if rb:
            sh = z + o
            if sh not in [m["uci"] for m in rb["moves"]]:
                notes.append("O1: shuttle illegal at %s" % z)
            nl = [m["uci"] for m in rb["moves"] if m["uci"] != sh and m["category"] != "win"]
            if nl:
                notes.append("O1 fails at %s: %s" % (z, ",".join(nl)))
            lines.append("  root %s Black to move: %-5s non-losing Black moves %s" % (z, rb["category"], [m["uci"] for m in rb["moves"] if m["category"] != "win"]))
        if rw:
            frz = [m["uci"] for m in rw["moves"] if m["category"] != "win"]
            lines.append("  root %s White to move: %-5s non-losing White moves (chess freezes) %s" % (z, rw["category"], frz))
            if not frz:
                notes.append("O2: no non-losing White move at %s" % z)
            for u in frz:
                if len(u) == 5:
                    notes.append("O2: freeze %s is a promotion" % u); continue
                q, ep = apply(pcs, u)
                qb = look(fen(q, "b", ep), need)
                kz = [s for s, c in q.items() if c == "k"][0]
                qw = None if wattacks(q, kz) else look(fen(q, "w"), need)
                if qb:
                    bad = [m["uci"] for m in qb["moves"] if m["category"] != "win"]
                    lines.append("    q after %s (%s), Black to move: %-5s non-losing %s" % (u, z, qb["category"], bad))
                    if bad or not qb["moves"]:
                        notes.append("O3 fails after %s at %s" % (u, z))
                if wattacks(q, kz):
                    notes.append("O4: q after %s at %s with White to move is illegal" % (u, z))
                elif qw:
                    bad = [m["uci"] for m in qw["moves"] if m["category"] != "win"]
                    lines.append("    q after %s (%s), White to move: %-5s non-losing %s" % (u, z, qw["category"], bad))
                    if bad or not qw["moves"]:
                        notes.append("O4 fails after %s at %s" % (u, z))
    print("%s %s k%s/k%s: exact over group in chess: %s" % (name, men, z0, z1, "YES" if not notes else "no"))
    for l in lines:
        print(l)
    for n in notes:
        print("    -", n)

# reflected translates
def grp(s):
    return frozenset((t[0], sq(t[1:])) for t in s.split())
def canon(g):
    best = None
    for refl in (0, 1):
        h = [(c, ((7 - s[0]) if refl else s[0], s[1])) for c, s in g]
        lo = min(s[0] for _, s in h)
        t = tuple(sorted((c, (s[0] - lo, s[1])) for c, s in h))
        best = t if best is None or t < best else best
    return best
pairs = [("C034_01", "Kc4 ke4 ke5 Pd2 Pd5 Pe6 pd6 pe7", "C145_07", "Kg4 ke4 ke5 Pe6 Pf2 Pf5 pe7 pf6"),
         ("C034_02", "Kf4 kd4 kd5 Pd6 Pe2 Pe5 pd7 pe6", "C145_09", "Kd4 kf4 kf5 Pe2 Pe5 Pf6 pe6 pf7")]
for a, ga, b, gb in pairs:
    A, B = grp(ga), grp(gb)
    refl = frozenset((c, (7 - s[0], s[1])) for c, s in B)
    shifts = [d for d in range(-7, 8) if frozenset((c, (s[0] + d, s[1])) for c, s in refl) == A]
    plain = [d for d in range(-7, 8) if frozenset((c, (s[0] + d, s[1])) for c, s in B) == A]
    print("%s = %s reflected and moved %s file(s); plain translate: %s" % (a, b, shifts, plain or "no"))
chess_exact = {"C125_05": "Kd4 kb4 kb5 Pb6 Pc2 Pc5 pb7 pc6", "C125_08": "Ke5 kc5 kc6 Pb2 Pb6 Pf6 pb7 pf7",
               "C125_10": "Kc5 ke5 ke6 Pb6 Pf2 Pf6 pb7 pf7", "C145_07": "Kg4 ke4 ke5 Pe6 Pf2 Pf5 pe7 pf6",
               "C145_09": "Kd4 kf4 kf5 Pe2 Pe5 Pf6 pe6 pf7", "C034_01": "Kc4 ke4 ke5 Pd2 Pd5 Pe6 pd6 pe7",
               "C034_02": "Kf4 kd4 kd5 Pd6 Pe2 Pe5 pd7 pe6"}
sh = {}
for k, g in chess_exact.items():
    sh.setdefault(canon(grp(g)), []).append(k)
print("the 7 chess-exact groups fall into %d shapes: %s" % (len(sh), " | ".join(", ".join(v) for v in sh.values())))
print("positions needed but not in the cache: %d" % len(need))
for f in need:
    print("   ", f)
