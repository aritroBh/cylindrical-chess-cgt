"""cmp_own.py OWN_A.out OWN_B.out REF.out : OWN_A / OWN_B are ownchess/ownref outputs ("pos | X", one bound each, bound A and bound B);
REF.out is a kpsolve / kq3 --bound AB output ("pos | A B | ...").  Compares (A, B) position by position (X = illegal skipped)."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import kchess
def rd(path):
    d = {}
    for ln in open(path):
        if ' | ' not in ln: continue
        p, v = ln.rstrip('\n').split(' | ')[:2]
        d[kchess.canon(p)] = v.split()[0]
    return d
A = rd(sys.argv[1]); B = rd(sys.argv[2]); R = kchess.parse_kp_output(sys.argv[3])
n = bad = 0
for p, (a, b, _) in R.items():
    if a == 'X': continue
    if p not in A or p not in B: print('MISSING', p); bad += 1; continue
    n += 1
    if (A[p], B[p]) != (a, b): bad += 1; print('DIFF', p, 'own', (A[p], B[p]), 'ref', (a, b))
print(f"compared {n} positions; differences {bad}")
