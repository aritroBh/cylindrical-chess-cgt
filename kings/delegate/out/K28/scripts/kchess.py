"""kchess.py -- K28: a small chess move generator for kings + pawns + officers on the flat 7x6 board (SPEC.md rules,
no double step and no en passant: assert that no pawn stands on its own second rank).  Written from SPEC.md.
Used only to walk game trees; every value comes from a solver (kpsolve / kq / ownchess), never from this file.
Move names are kpsolve's: piece letter (upper case for both colours), from, to, and "=Q" etc. for a promotion.
Position text: tokens like "Kb2 Pa3 ka4 pb3 w -" (kpsolve format)."""
import sys
W, H = 7, 6
FILES = "abcdefg"

def sq(f, r): return FILES[f] + str(r + 1)           # f 0..6, r 0..5
def parse_sq(s): return (FILES.index(s[0]), int(s[1:]) - 1)

def parse(line):
    t = line.split()
    assert t[-1] == '-' and t[-2] in ('w', 'b'), line
    stm = 0 if t[-2] == 'w' else 1
    board = {}
    for tok in t[:-2]:
        board[parse_sq(tok[1:])] = tok[0]
    return board, stm

def colour(p): return 0 if p.isupper() else 1

ORDER = "KQRBNPkqrbnp"
def fmt(board, stm):
    toks = sorted(board.items(), key=lambda kv: (ORDER.index(kv[1]), kv[0][1], kv[0][0]))
    return ' '.join(p + sq(*s) for s, p in toks) + (' w -' if stm == 0 else ' b -')

def canon(line):
    b, s = parse(line); return fmt(b, s)

KD = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
ND = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
RD = [(1, 0), (-1, 0), (0, 1), (0, -1)]
BD = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

def inb(f, r): return 0 <= f < W and 0 <= r < H

def attacked(board, s, by):
    """is square s attacked by a piece of colour `by` (board as it stands; s itself may be occupied)."""
    f, r = s
    for (pf, pr), p in board.items():
        if colour(p) != by: continue
        t = p.upper()
        if t == 'K':
            if max(abs(pf - f), abs(pr - r)) == 1: return True
        elif t == 'P':
            d = 1 if by == 0 else -1
            if pr + d == r and abs(pf - f) == 1: return True
        elif t == 'N':
            if (f - pf, r - pr) in ND: return True
        else:
            dirs = RD if t == 'R' else BD if t == 'B' else RD + BD
            for df, dr in dirs:
                x, y = pf + df, pr + dr
                while inb(x, y):
                    if (x, y) == s: return True
                    if (x, y) in board: break
                    x += df; y += dr
    return False

def king_sq(board, c):
    k = 'K' if c == 0 else 'k'
    for s, p in board.items():
        if p == k: return s

def in_check(board, c):
    return attacked(board, king_sq(board, c), 1 - c)

def legal_position(board, stm):
    """SPEC.md legality: kings not adjacent, no pawn on first/last rank, side not to move not in check."""
    kw, kb = king_sq(board, 0), king_sq(board, 1)
    if max(abs(kw[0] - kb[0]), abs(kw[1] - kb[1])) <= 1: return False
    for (f, r), p in board.items():
        if p == 'P' and (r == 0 or r == H - 1): return False
        if p == 'p' and (r == 0 or r == H - 1): return False
    return not in_check(board, 1 - stm)

def moves(board, stm):
    """list of (name, newboard) for all legal moves of colour stm.  Aborts if a pawn could double-step."""
    out = []
    for (f, r), p in list(board.items()):
        if colour(p) != stm: continue
        t = p.upper()
        def add(name, nb):
            if not in_check(nb, stm): out.append((name, nb))
        def land(to, name_extra=''):
            nb = dict(board); del nb[(f, r)]
            nb[to] = p
            return nb
        if t == 'K':
            for df, dr in KD:
                x, y = f + df, r + dr
                if not inb(x, y): continue
                q = board.get((x, y))
                if q is not None and colour(q) == stm: continue
                if q is not None and q.upper() == 'K': continue
                add('K' + sq(f, r) + sq(x, y), land((x, y)))
        elif t == 'P':
            d = 1 if stm == 0 else -1
            second = 1 if stm == 0 else H - 2
            assert r != second, "pawn on its second rank (double step) not supported"
            last = H - 1 if stm == 0 else 0
            cands = []
            if inb(f, r + d) and (f, r + d) not in board: cands.append((f, r + d))
            for df in (-1, 1):
                x, y = f + df, r + d
                if inb(x, y) and (x, y) in board and colour(board[(x, y)]) != stm and board[(x, y)].upper() != 'K':
                    cands.append((x, y))
            for to in cands:
                nb = land(to)
                if to[1] == last:
                    for pt in "QRBN":
                        nb2 = dict(nb); nb2[to] = pt if stm == 0 else pt.lower()
                        add('P' + sq(f, r) + sq(*to) + '=' + pt, nb2)
                else:
                    add('P' + sq(f, r) + sq(*to), nb)
        elif t == 'N':
            for df, dr in ND:
                x, y = f + df, r + dr
                if not inb(x, y): continue
                q = board.get((x, y))
                if q is not None and (colour(q) == stm or q.upper() == 'K'): continue
                add('N' + sq(f, r) + sq(x, y), land((x, y)))
        else:
            dirs = RD if t == 'R' else BD if t == 'B' else RD + BD
            for df, dr in dirs:
                x, y = f + df, r + dr
                while inb(x, y):
                    q = board.get((x, y))
                    if q is not None:
                        if colour(q) != stm and q.upper() != 'K':
                            add(t + sq(f, r) + sq(x, y), land((x, y)))
                        break
                    add(t + sq(f, r) + sq(x, y), land((x, y)))
                    x += df; y += dr
    return out

def children(line):
    """[(movename, childline)] for a position line."""
    b, s = parse(line)
    return [(n, fmt(nb, 1 - s)) for n, nb in moves(b, s)]

def npawns(line):
    return sum(1 for tok in line.split()[:-2] if tok[0] in 'Pp')

def nofficers(line):
    return sum(1 for tok in line.split()[:-2] if tok[0] in 'QRBNqrbn')

def parse_kp_output(path):
    """kpsolve output -> dict canonical-position -> (A, B, {movename: (A_after, B_after)})"""
    res = {}
    for ln in open(path):
        ln = ln.rstrip('\n')
        if not ln or ln.startswith('#') or ' | ' not in ln: continue
        parts = ln.split(' | ')
        pos = canon(parts[0])
        ab = parts[1].split()
        if len(ab) != 2: continue
        A, B = ab
        mv = {}
        if len(parts) >= 4 and parts[3].startswith('B: '):   # kpsolve: "| A: moves | B: moves"; kq3 --bound AB: "| moves | B: moves"
            ma = dict(x.rsplit(':', 1) for x in (parts[2][3:] if parts[2].startswith('A: ') else parts[2]).split())
            mb = dict(x.rsplit(':', 1) for x in parts[3][3:].split())
            for k in ma: mv[k] = (ma[k], mb[k])
        elif len(parts) == 3:
            ma = dict(x.rsplit(':', 1) for x in parts[2].split())
            for k in ma: mv[k] = (ma[k], ma[k])
        res[pos] = (A, B, mv)
    return res

if __name__ == '__main__':
    # self test / listing:  python3 kchess.py "POS" -> list of children
    for ln in sys.stdin if len(sys.argv) == 1 else [sys.argv[1]]:
        ln = ln.strip()
        if not ln: continue
        for n, c in children(ln): print(n, '->', c)
