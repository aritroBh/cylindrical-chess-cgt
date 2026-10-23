"""Sensitivity control for audit4: same exhaustive local test with a SHORTER pattern arc of L files (cut in the middle).
If the harness can detect failures, short arcs must fail for some outside contents."""
import sys, itertools, time
from engine import *
from audit4_exhaustive_local import menu, cls, W2, B4

def run(m, kind, phase, L):
    M = menu(kind)
    arc = [(W2 if (j + phase) % 2 == 0 else B4) for j in range(L)]
    tested = skipped = bad = 0
    ex = None
    for combo in itertools.product(range(len(M)), repeat=m):
        outs = [M[i] for i in combo]
        pos = tuple([outs[0]] + arc + outs[1:])
        c = 1 + (L // 2 - 1)
        if passed_list(pos, None, 'W') or passed_list(pos, None, 'B'):
            skipped += 1; continue
        ph = ins(pos, c)
        if passed_list(ph, None, 'W') or passed_list(ph, None, 'B'):
            bad += 1; ex = ex or ('phat has passed', fmt(pos)); continue
        a = cls(pos); b = cls(ph)
        tested += 1
        for s in 'WB':
            if a[s][0] != b[s][0] or {ins_nd(k, c) for k in a[s][1]} != set(b[s][1]):
                bad += 1; ex = ex or ('mismatch', fmt(pos), 'c', c, s); break
    return tested, skipped, bad, ex

if __name__ == '__main__':
    m = int(sys.argv[1]); kind = sys.argv[2]
    for L in map(int, sys.argv[3:]):
        for phase in (0, 1):
            t0 = time.time()
            print('m', m, kind, 'arc length', L, 'phase', phase, run(m, kind, phase, L), '%.0fs' % (time.time() - t0), flush=True)
