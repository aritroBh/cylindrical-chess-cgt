"""run_race_rules.py -- sensitivity of the result to the race rule (informational; the task's setting is 'count').
PROOF.md H4 says the race rule enters the argument only through the passed-pawn set of a child.  Here P_n is solved under
the three rules of cylcgt/pawns.py RACE_RULE: 'count' (default), 'mover' (the mover wins every race), 'opponent' (the mover
loses every race): unreduced signatures for n = 8..22, reduced graph size and the c = 12 insertion step n -> n+2 for n = 18, 20."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import myeng as M

HS = tuple(range(8))
def insn(nd, c):
    p, e = nd
    return (M.ins(p, c), e)
for rule in ('count', 'mover', 'opponent'):
    M.RACE_RULE = rule
    sigs = []
    for n in range(8, 23, 2):
        sigs.append((n, M.Full('keep').signature(M.P_start(n), HS)))
    gs = {n: M.Graph(M.P_start(n)) for n in (18, 20)}
    st = gs[18].stats()
    iso = {insn(nd, 12) for nd in gs[18].order} == set(gs[20].order)
    for nd in gs[18].order:
        for c in (0, 1):
            T0, K0, _, _ = gs[18].info[nd][c]
            T1, K1, _, _ = gs[20].info[insn(nd, 12)][c]
            iso &= bool(T0) == bool(T1) and {insn(x, 12) for x in K0} == K1
    print('race rule %-8s: unreduced signatures %s | R_18: %s, graph signature %s | ins_12(R_18) == R_20: %s' % (
        rule, ' '.join('%d:%s' % x for x in sigs), st, gs[18].signature(HS), iso), flush=True)
