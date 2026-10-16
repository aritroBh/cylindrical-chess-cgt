"""Hidden-assumption probe: the solver forbids a double step from rank 1, but the
paper's own option list for 3.2 ({0,1|}: h1-h3 'to the zero game') implies the paper
let the rank-1 white pawns double-step.  Recompute the rank-1 diagrams under that
alternative rule (indep.py model otherwise unchanged).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/diagrams/V1-refute/rank1.py
"""
import sys, threading
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import indep as I
import extra as E

orig = I.pawn_moves

def pm(W, B, ep, side):
    res = orig(W, B, ep, side)
    if side == "W":
        occ = W | B
        for (f, r) in W:
            if r == 1 and (f, 2) not in occ and (f, 3) not in occ:
                e = ((f, 2), (f, 3), "B") if I.CFG["ep"] else None
                res.append((W - {(f, 1)} | {(f, 3)}, B, e, True))
    return res

def main():
    U, S = I.UP, I.STAR
    cands = {"0": 0, "1": 1, "2": 2, "3": 3, "*": S, "up": U, "1*": I.G([1], [1])}
    for variant in (False, True):
        I.pawn_moves = pm if variant else orig
        for ep in (True, False):
            for wrap, label, t in ((True, "2.2", "W: a2 h1 / B: a3 h4"), (True, "3.1", "W: a3 h1 / B: a4 h5"),
                                   (True, "3.2", "W: a4 h1 / B: a5 h6"), (False, "2.3 flat", "W: c1 d2 / B: c4 d3")):
                I.CFG.update(ep=ep, rule="count", split=True, wrap=wrap); I.reset()
                hit = [k for k, X in cands.items() if E.eq_sum(t, [X])]
                print(f"rank1_double={variant} ep={'on ' if ep else 'off'} {label:8s} {t}: outcome {I.outcome(I.root_state(t))}, equals {hit}")

if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000); threading.stack_size(512 * 1024 * 1024)
    th = threading.Thread(target=main); th.start(); th.join()
