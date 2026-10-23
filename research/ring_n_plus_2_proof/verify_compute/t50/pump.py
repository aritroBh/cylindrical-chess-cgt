import sys
from eng import *
from red import build, stats

W3 = parse_file('W3'); B5 = parse_file('B5'); W2 = parse_file('W2'); B4 = parse_file('B4')
def expected(kind, j):
    if kind == 'O': return W3 if j % 2 == 1 else B5
    return W2 if j % 2 == 1 else B4          # E and F walls: odd files W2, even files B4

def is_pat(kind, pos, j):
    return pos[j] == expected(kind, j)

def ins(pos, c):
    return pos[:c + 1] + (pos[c + 1], pos[c]) + pos[c + 1:]

def insn(nd, c):
    """insert on a node (pos, ep): the flag file index shifts when it is right of the cut."""
    p, e = nd
    return (ins(p, c), None if e is None else ((e[0] if e[0] <= c else e[0] + 2), e[1]))

def cls(pos, ep):
    """per side: (set of T-flag, frozenset of K children positions, counts)"""
    out = {}
    for side in 'WB':
        cl = classify_moves(pos, ep, side)
        out[side] = (any(k == 'T' for k, _, _ in cl),
                     frozenset((np_, ne) for k, np_, ne in cl if k == 'K'),
                     sorted(k for k, _, _ in cl))
    return out

def pump_check(kind, n, c):
    pos0 = ring(kind, n); pos1 = ring(kind, n + 2)
    assert ins(pos0, c) == pos1, 'start not mapped'
    ids0, order0, info0 = build(pos0)
    ids1, order1, info1 = build(pos1)
    img = {(ins(p, c), e) for p, e in order0 if e is None}
    ok = (img == set(order1)) and len(order0) == len(order1)
    # edges
    bad = 0
    for (p, e) in order0:
        for s in 'WB':
            T0, K0, _ = info0[(p, e)][s]
            T1, K1, _ = info1[(ins(p, c), e)][s]
            if bool(T0) != bool(T1): bad += 1
            if {(ins(q, c), qe) for q, qe in K0} != set(K1): bad += 1
    return ok, bad, len(order0), len(order1)

def lemma3_nodes(kind, n):
    """all nodes of reduced R_n, all admissible cuts: check Lemma 3's conclusion."""
    pos0 = ring(kind, n)
    ids, order, info = build(pos0)
    checked = bad = 0
    cutsused = set()
    for (p, e) in order:
        if e is not None: continue
        for c in range(4, n - 5):
            if not all(is_pat(kind, p, j) for j in range(c - 4, c + 6)): continue
            cutsused.add(c)
            ph = ins(p, c)
            a = cls(p, None); b = cls(ph, None)
            for s in 'WB':
                checked += 1
                if a[s][0] != b[s][0] or {(ins(q, c), qe) for q, qe in a[s][1]} != set(b[s][1]):
                    bad += 1
    return len(order), checked, bad, sorted(cutsused)

if __name__ == '__main__':
    mode = sys.argv[1]; kind = sys.argv[2]
    if mode == 'pump':
        c = int(sys.argv[3])
        for n in map(int, sys.argv[4:]):
            print('pump', kind, n, '->', n + 2, 'cut', c, pump_check(kind, n, c), flush=True)
    else:
        for n in map(int, sys.argv[3:]):
            print('lemma3 nodes', kind, n, lemma3_nodes(kind, n), flush=True)
