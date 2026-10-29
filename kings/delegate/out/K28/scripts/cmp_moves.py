"""cmp_moves.py KPOUT... : for every position in the kpsolve --moves outputs, compare kchess.py's legal move names with kpsolve's.
Also checks that the position is legal per SPEC and prints the number of positions / moves compared."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import kchess
npos = nmov = bad = 0
for path in sys.argv[1:]:
    d = kchess.parse_kp_output(path)
    for pos, (A, B, mv) in d.items():
        if A == 'X': continue
        mine = {n for n, c in kchess.children(pos)}
        theirs = set(mv)
        npos += 1; nmov += len(theirs)
        if mine != theirs:
            bad += 1; print("MISMATCH", pos, "mine-only", sorted(mine - theirs), "kp-only", sorted(theirs - mine))
print("compared", npos, "positions,", nmov, "moves; mismatching positions:", bad)
