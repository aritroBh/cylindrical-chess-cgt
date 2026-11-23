"""Helpers: solve rings with mob1_32 / mob2_32, one width per process (mob2's memo key omits the width)."""
import subprocess, collections, os
BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mobius_rings_n', 'bin')
M1, M2 = os.path.join(BIN, 'mob1_32'), os.path.join(BIN, 'mob2_32')
def _run(binp, rs, tmo):
    try:
        p = subprocess.run(['nice', '-n', '15', binp, 'solve'], input='\n'.join(rs) + '\n',
                           capture_output=True, text=True, timeout=tmo)
    except subprocess.TimeoutExpired:
        if len(rs) == 1: return ['TIMEOUT']
        h = len(rs) // 2
        return _run(binp, rs[:h], tmo) + _run(binp, rs[h:], tmo)
    o = p.stdout.split('\n')[:len(rs)]
    if len(o) != len(rs):
        if len(rs) == 1: return ['ERR']
        h = len(rs) // 2
        return _run(binp, rs[:h], tmo) + _run(binp, rs[h:], tmo)
    return o
def solve(rings, binp=M2, batch=40, tmo=60):
    """returns dict ring -> signature; batches contain one width only."""
    byw = collections.defaultdict(list)
    for r in dict.fromkeys(rings): byw[len(r.split())].append(r)
    res = {}
    for w, rs in sorted(byw.items()):
        for i in range(0, len(rs), batch):
            ch = rs[i:i + batch]
            for r, s in zip(ch, _run(binp, ch, tmo)): res[r] = s
    return res
def npawns(ring): return sum(ch.isdigit() for ch in ring)
def legal_root(ring):
    """W ranks 2..7 up, B ranks 2..7, at most one pawn of each colour... just format check."""
    for t in ring.split():
        cur = None; seen = set()
        for ch in t:
            if ch in 'WB': cur = ch
            else:
                r = int(ch)
                if not (2 <= r <= 7) or (r in seen): return False
                seen.add(r)
    return True
