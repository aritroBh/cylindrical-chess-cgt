"""K21: the small examples quoted in REPORT.md"""
from dsum import *
def show(title, comps, Bs=(2, 5, 9)):
    root = tuple(c.root for c in comps)
    d = d_results(comps)
    print("%s\n  D-result (L first, R first): %s %s" % (title, d[(root, 0)], d[(root, 1)]))
    for B in Bs:
        c = cgt_results(comps, B)
        dom = dominance(comps, B)[0]
        cr, mx = reserve_criterion(comps, B)
        print("  B=%d  CGT outcome: %s %s   dominance=%s  reserve-criterion=%s" % (B, c[(root, 0)], c[(root, 1)], dom, cr))
PL = Comp([[PLUS]], [[]]);  MI = Comp([[]], [[MINUS]])
show("{+|} + off", [PL, mk_off()])
show("{+|} + dud", [PL, mk_dud()])
show("{+|} + on", [PL, mk_on()])
show("{+|} + over", [PL, mk_over()])
show("{|-} + on", [MI, mk_on()])
show("{|-} + off", [MI, mk_off()])
show("{|-} + over", [MI, mk_over()])
show("{|-} + under", [MI, mk_under()])
show("{+|} + {|-}  (cancellation, Prop 1.12)", [PL, MI])
SU = Comp([[MINUS]], [[]])   # {-|}: a Left suicide
show("{+|} + {-|}  (a Left suicide beside a + threat: tau-unsafe, reserve-safe)", [PL, SU])
S3 = Comp([[2], [], [1, 2]], [[1, 2], [0, 1], []], 0)  # '0:{2/1,2}|1:{/0,1}|2:{1,2/}'
K = Comp([[1], []], [[MINUS, 1], []], 0)
print("C1 counterexample: K={1|-,1} (1=0), S=%s, stopper=%s" % (comp_str(S3), S3.is_stopper()))
r = solve([K, S3], [(0, 0)]); print("  D:", r[((0, 0), 0)], r[((0, 0), 1)])
for B in (3, 14, 40):
    c = solve([translate(K, B)[0], S3], [(0, 0)]); print("  CGT B=%d:" % B, c[((0, 0), 0)], c[((0, 0), 1)])
r_off = solve([K, mk_off()], [(0, 0)]); r_on = solve([K, mk_on()], [(0, 0)])
print("  K+off:", r_off[((0, 0), 0)], r_off[((0, 0), 1)], " K+on:", r_on[((0, 0), 0)], r_on[((0, 0), 1)])
SX = Comp([[0, 1], []], [[0], []], 0)
print("non-stopper S={S,0|S}: stopper=%s lam,rho=%s" % (SX.is_stopper(), reserves(SX, 4, 12)))
show("{+|} + S  (S={S,0|S}, a non-stopper with finite lambda)", [PL, SX])
