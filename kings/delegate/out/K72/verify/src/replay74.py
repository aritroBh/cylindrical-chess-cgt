"""K74 referee: replay lines move by move with realchess.movegen (an ordinary chess move generator, not a P solver).

Usage (repository root):
  python3 -I -B kings/delegate/out/K72/verify/src/replay74.py LINESFILE > positions
LINESFILE holds blocks "# tag" / "<piece list> <w|b> - | <value> | line: <moves>" (K72's ref3pv format:
Pb3b4 ...kc5c6 Kg3h3x Ph7h8=promotes) or lines of p74 -l output ("   line: 1.Ke5-f4 Kc5-d4 ... (promotes)") after
a position line "<piece list> <w|b> -  P=W37".  Every move must be legal in chess; the last move must be a
promotion.  Prints every position on every line (piece list, side to move, e.p. square if an e.p. capture is
legal) followed by "# tag value", for p74.
"""
import re, sys, os
sys.path.insert(0, os.getcwd())
from realchess import movegen as mg


def pos_from_list(s):
    t = s.split()
    b = ["."] * 64
    stm = None
    for x in t:
        if x in ("w", "b"):
            stm = x
        elif x == "-":
            pass
        else:
            b[mg.sq(x[1:])] = x[0]
    fen_rows = []
    for r in range(7, -1, -1):
        row, e = "", 0
        for f in range(8):
            p = b[8 * r + f]
            if p == ".":
                e += 1
            else:
                row += (str(e) if e else "") + p; e = 0
        fen_rows.append(row + (str(e) if e else ""))
    return mg.parse_fen("/".join(fen_rows) + f" {stm} - - 0 1")


def to_list(p):
    out = []
    for s, x in enumerate(p.board):
        if x in "Kk":
            out.append(x + mg.sqname(s))
    for s, x in enumerate(p.board):
        if x in "Pp":
            out.append(x + mg.sqname(s))
        elif x not in ".Kk" and x != mg.EMPTY:
            raise ValueError("officer on board")
    ep = mg.sqname(p.ep) if p.ep is not None and any(m.ep for m in mg.legal_moves(p)) else "-"
    return " ".join(out) + f" {p.stm} {ep}"


def parse_k72(tok):
    tok = tok.lstrip(".")
    m = re.fullmatch(r"([KkPp])([a-h][1-8])([a-h][1-8])(x?)(=promotes)?", tok)
    return m.group(2), m.group(3), bool(m.group(5))


def parse_p74(tok):
    tok = re.sub(r"^\d+\.(\.\.)?", "", tok)
    m = re.fullmatch(r"K?([a-h][1-8])[-x]([a-h][1-8])(=?)", tok)
    return m.group(1), m.group(2), m.group(3) == "="


def replay(tag, start, value, toks, parser):
    p = pos_from_list(start)
    print(f"{to_list(p)}  # {tag} {value}")
    for i, t in enumerate(toks):
        a, b, promo = parser(t)
        ms = [m for m in mg.legal_moves(p) if mg.sqname(m.frm) == a and mg.sqname(m.to) == b]
        if not ms:
            raise SystemExit(f"{tag}: illegal move {t} at ply {i + 1}")
        if promo:
            if not ms[0].promo or i != len(toks) - 1:
                raise SystemExit(f"{tag}: promotion mark wrong at {t}")
            print(f"#   {tag}: {len(toks)} plies, legal, ends with a promotion by {'White' if p.stm == 'w' else 'Black'}",
                  file=sys.stderr)
            return
        if ms[0].promo:
            raise SystemExit(f"{tag}: unmarked promotion {t}")
        p = mg.make(p, ms[0])
        print(f"{to_list(p)}  # {tag} {value}")
    print(f"#   {tag}: {len(toks)} plies, legal, NO promotion at the end", file=sys.stderr)


if __name__ == "__main__":
    lines = open(sys.argv[1]).read().splitlines()
    tag = None
    for i, l in enumerate(lines):
        if l.startswith("# "):
            tag = l[2:].strip()
        elif "| line:" in l:
            start, value, rest = l.split("|", 2)
            replay(tag, start.strip(), value.strip(), rest.split("line:")[1].split(), parse_k72)
        elif l.strip().startswith("line:"):
            prev = [x for x in lines[:i] if "P=" in x and not x.startswith(" ")][-1]
            start, v = prev.split("P=")
            if v[0] == "D":
                continue                      # draw lines do not end; not replayed
            toks = [t for t in l.split("line:")[1].split() if t != "(promotes)"]
            replay(f"p74 line {start.strip()}", start.strip(), v[0], toks, parse_p74)
