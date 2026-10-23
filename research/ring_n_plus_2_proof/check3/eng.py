# T50 verifier engine eng.py (copy of research/ring_family_proof/verify/eng.py, family P added): independent of rg.c
# Independent whole-board engine for the T50 verification (written from the rules in the brief / pawns.py semantics).
# Position: tuple of n (wmask, bmask) per file (bit r-1 = rank r, r=1..8), plus ep flag (f, stepper) or None.
# G + *h, normal play; a position where exactly one side has a passed pawn (or both and the race is won) is decided.
import sys, re
sys.setrecursionlimit(100000)
R = 8

def parse_file(tok):
    """'W23B4' -> (wmask, bmask)."""
    w = b = 0
    for col, digs in re.findall(r'([WB])(\d+)', tok):
        for d in digs:
            if col == 'W': w |= 1 << (int(d) - 1)
            else: b |= 1 << (int(d) - 1)
    return (w, b)

def parse(toks):
    return tuple(parse_file(t) for t in toks)

def npawns(pos):
    return sum(bin(w).count('1') + bin(b).count('1') for w, b in pos)

def hi(m):  # highest rank (1..8) or 0
    return m.bit_length()

def lo(m):  # lowest rank or 99
    return ((m & -m).bit_length()) if m else 99

def passed_ranks(pos, ep, side):
    """list of (f, r) passed pawns of side (respecting e.p. protection)."""
    n = len(pos)
    out = []
    if side == 'W':
        bh = [hi(b) for w, b in pos]
        for f in range(n):
            w = pos[f][0]
            if not w: continue
            m = max(bh[(f - 1) % n], bh[f], bh[(f + 1) % n])
            for r in range(1, R + 1):
                if w >> (r - 1) & 1 and m <= r:
                    out.append((f, r))
    else:
        wl = [lo(w) for w, b in pos]
        for f in range(n):
            b = pos[f][1]
            if not b: continue
            m = min(wl[(f - 1) % n], wl[f], wl[(f + 1) % n])
            for r in range(1, R + 1):
                if b >> (r - 1) & 1 and m >= r:
                    out.append((f, r))
    if ep is not None:
        # ep = (f, stepper); stepped pawn sits on rank 4 (W) or 5 (B); protected if an enemy pawn is beside it
        ef, es = ep
        if es == side:
            r = 4 if es == 'W' else 5
            ob = pos[(ef - 1) % n][1 if es == 'W' else 0] >> (r - 1) & 1 or pos[(ef + 1) % n][1 if es == 'W' else 0] >> (r - 1) & 1
            if ob:
                out = [x for x in out if x != (ef, r)]
    return out

def moves(pos, ep, side):
    """list of (newpos, newep) for side to move. ep is the flag in the node (usable only by the capturing side)."""
    n = len(pos)
    res = []
    d = 1 if side == 'W' else -1
    k = 0 if side == 'W' else 1       # index of own mask
    start = 2 if side == 'W' else 7
    seen = set()
    def put(np, ne):
        key = (np, ne)
        if key not in seen:
            seen.add(key); res.append(key)
    for f in range(n):
        own = pos[f][k]
        if not own: continue
        for r in range(1, R + 1):
            if not (own >> (r - 1) & 1): continue
            r1 = r + d
            if not (1 <= r1 <= R): continue
            occ_f = pos[f][0] | pos[f][1]
            if not (occ_f >> (r1 - 1) & 1):
                lst = list(pos)
                a = list(lst[f])
                a[k] = (own & ~(1 << (r - 1))) | (1 << (r1 - 1))
                lst[f] = tuple(a)
                put(tuple(lst), None)
                r2 = r + 2 * d
                if r == start and 1 <= r2 <= R and not (occ_f >> (r2 - 1) & 1):
                    lst = list(pos)
                    a = list(lst[f])
                    a[k] = (own & ~(1 << (r - 1))) | (1 << (r2 - 1))
                    lst[f] = tuple(a)
                    npos = tuple(lst)
                    # flag recorded only if an enemy pawn stands beside landing square
                    en = 1 - k
                    beside = (pos[(f - 1) % n][en] >> (r2 - 1) & 1) or (pos[(f + 1) % n][en] >> (r2 - 1) & 1)
                    put(npos, (f, side) if beside else None)
            for df in (-1, 1):
                g = (f + df) % n
                eb = pos[g][1 - k]
                if eb >> (r1 - 1) & 1:
                    lst = list(pos)
                    a = list(lst[f]); a[k] = own & ~(1 << (r - 1)); lst[f] = tuple(a)
                    c = list(lst[g]); c[k] |= 1 << (r1 - 1); c[1 - k] &= ~(1 << (r1 - 1)); lst[g] = tuple(c)
                    put(tuple(lst), None)
                elif ep is not None and ep[1] != side and ep[0] == g and r1 == (3 if ep[1] == 'W' else 6):
                    # e.p. capture of the pawn on (g, r) -- stepped pawn sits on same rank as our pawn
                    lst = list(pos)
                    a = list(lst[f]); a[k] = own & ~(1 << (r - 1)); lst[f] = tuple(a)
                    c = list(lst[g]); c[k] |= 1 << (r1 - 1); c[1 - k] &= ~(1 << (r - 1)); lst[g] = tuple(c)
                    put(tuple(lst), None)
    return res

def prom_dist(pos, ep, side):
    """best promotion distance among passed, front pawns, not e.p.-capturable (race rule 'count')."""
    n = len(pos)
    best = 10**6
    for f, r in passed_ranks(pos, ep, side):
        w, b = pos[f]
        if side == 'W':
            if w >> r:   # another own pawn above on file? (any occupied square above)
                pass
            if (w | b) >> r:  # any piece above on same file -> not front pawn
                continue
            dd = R - r - (1 if r == 2 else 0)
        else:
            if (w | b) & ((1 << (r - 1)) - 1):
                continue
            dd = r - 1 - (1 if r == R - 1 else 0)
        best = min(best, dd)
    return best

def status(pos, ep, mover):
    """after `mover` moved to (pos, ep): 'W'/'B' = decided for that side, None = not terminal."""
    wp = passed_ranks(pos, ep, 'W'); bp = passed_ranks(pos, ep, 'B')
    if wp and bp:
        other = 'B' if mover == 'W' else 'W'
        dw = prom_dist(pos, ep, 'W'); db = prom_dist(pos, ep, 'B')
        dm, do = (dw, db) if mover == 'W' else (db, dw)
        return other if do <= dm else mover
    if wp: return 'W'
    if bp: return 'B'
    return None

def other(s): return 'B' if s == 'W' else 'W'

def classify_moves(pos, ep, side):
    """returns list of (kind, newpos, newep): kind in T,L,P,K."""
    out = []
    y = other(side)
    for np_, ne in moves(pos, ep, side):
        st = status(np_, ne, side)
        if st == side: out.append(('T', np_, ne))
        elif st == y: out.append(('L', np_, ne))
        else:
            poisoned = False
            for np2, ne2 in moves(np_, ne, y):
                if status(np2, ne2, y) == y:
                    poisoned = True; break
            out.append(('P' if poisoned else 'K', np_, ne))
    return out

# ---------- unreduced solver: win(pos, ep, h, mover) ----------
class Solver:
    def __init__(self):
        self.memo = {}
        self.nodes = 0
    def win(self, pos, ep, h, mover):
        key = (pos, ep, h, mover)
        v = self.memo.get(key)
        if v is not None: return v
        self.nodes += 1
        ch = moves(pos, ep, mover)
        y = other(mover)
        res = False
        sts = []
        for np_, ne in ch:
            st = status(np_, ne, mover)
            if st == mover:
                res = True; break
            sts.append((st, np_, ne))
        if not res:
            # heap moves and non-terminal pawn moves; test non-terminal pawn moves
            for st, np_, ne in sts:
                if st is None and not self.win(np_, ne, h, y):
                    res = True; break
        if not res:
            for h2 in range(h):
                if not self.win(pos, ep, h2, y):
                    res = True; break
        self.memo[key] = res
        return res

# ---------- families ----------
def O_toks(n):
    assert n % 2 == 1 and n >= 5
    k = (n - 3) // 2
    return ['W23B4', 'B5', 'W2B5'] + ['W3', 'B5'] * k
def E_toks(n):
    assert n % 2 == 0 and n >= 6
    m = (n - 6) // 2
    return ['B5', 'W2B5', 'W35B6', 'W2'] + ['B4', 'W2'] * (m + 1)
def F_toks(n):
    K = ['W3B6', 'B6', 'W4B7', 'W4', 'W6B7']
    if n % 2 == 1:
        return ['B4', 'W2'] * ((n - 5) // 2) + K
    else:
        return ['B4', 'W2'] * ((n - 6) // 2) + K + ['W2']
def P_toks(n):
    assert n % 2 == 0 and n >= 8
    return ['W5','B7','W4','W4B7','B6','W3B6'] + ['W2','B4'] * ((n - 6)//2)
def ring(kind, n):
    return parse({'O': O_toks, 'E': E_toks, 'F': F_toks, 'P': P_toks}[kind](n))

def outcomes(pos, hs=(0, 1, 2, 3)):
    s = Solver()
    sig = ''
    for h in hs:
        a = s.win(pos, None, h, 'W'); b = s.win(pos, None, h, 'B')
        sig += {(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(a, b)]
    return sig, s.nodes

if __name__ == '__main__':
    kind = sys.argv[1]
    for n in map(int, sys.argv[2:]):
        pos = ring(kind, n)
        sig, nodes = outcomes(pos)
        print(kind, n, 'pawns', npawns(pos), 'sig', sig, 'nodes', nodes, flush=True)
