"""K32: third computation of (lambda, rho): K21's dsum.reserves (read-only import, no bytecode written) against implementation B's
output file.  usage: crosscheck_k21.py N resultfile classfile [stride]"""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K21/scripts")
import dsum
N, res, cls = int(sys.argv[1]), sys.argv[2], sys.argv[3]
stride = int(sys.argv[4]) if len(sys.argv) > 4 else 1
rl = [l.split() for l in open(res)]
cl = [l.split() for l in open(cls)]
assert len(rl) == len(cl)
bad = 0; n = 0
for i in range(0, len(cl), stride):
    toks = cl[i]
    L, R = [], []
    k = len(toks)
    for t in toks:
        l, r = (int(x, 16) for x in t.split("/"))
        L.append([y for y in range(k) if l >> y & 1]); R.append([y for y in range(k) if r >> y & 1])
    comp = dsum.Comp(L, R, 0)
    assert comp.is_stopper() and comp.terminal_free()
    lam, rho = dsum.reserves(comp, 1, 2 * N + 3)
    a = lam[0]; b = rho[0]
    a = "inf" if a is None else str(a); b = "inf" if b is None else str(b)
    n += 1
    if (a, b) != (rl[i][3], rl[i][4]):
        bad += 1
        if bad < 5: print("MISMATCH", cl[i], (a, b), rl[i])
print("N=%d: %d graphs compared with K21 dsum.reserves, %d mismatches" % (N, n, bad))
