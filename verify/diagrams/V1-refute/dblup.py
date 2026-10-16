"""Shifted 3.2 (W a5 h2 / B a6 h7) without e.p.: is it up+up+* (= double-up-star)?
Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/diagrams/V1-refute/dblup.py
"""
import sys, threading
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import indep as I
import extra as E

def main():
    U, S = I.UP, I.STAR
    cand = I.G([0, U], [0])
    # sanity of my explicit forms: {0,up|0} - (up+up+*) = 0 ?
    st = (tuple(sorted([cand, I.neg(U), I.neg(U), I.neg(S)])), 0)
    print("sanity {0,up|0} == up+up+* :", I.outcome(st) == "P")
    for ep in (True, False):
        for rule in ("count", "mover", "opponent"):
            I.CFG.update(ep=ep, rule=rule, split=True, wrap=True); I.reset()
            t = "W: a5 h2 / B: a6 h7"
            print(f"ep={'on' if ep else 'off'} rule={rule}: 3.2 up1 == up+up+* : {E.eq_sum(t, [U, U, S])}; == 2: {E.eq_sum(t, [2])}; outcome {I.outcome(I.root_state(t))}")

if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000); threading.stack_size(512 * 1024 * 1024)
    th = threading.Thread(target=main); th.start(); th.join()
