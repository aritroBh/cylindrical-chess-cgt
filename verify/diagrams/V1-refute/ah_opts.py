"""7.1 {h,a}: list Left's and Right's options and identify each one's value among
small candidates, by the difference-game test (indep.py only).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/diagrams/V1-refute/ah_opts.py
"""
import sys, threading
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import indep as I

def nm(S): return " ".join(sorted(I.FILES[f] + str(r) for f, r in S))

def main():
    for split in (True, False):
        I.CFG.update(ep=True, rule="count", split=split, wrap=True); I.reset()
        W, B = I.parse(I.POS["7.1ah"])
        cands = {str(k): k for k in range(250, 262)}
        cands.update({"0": 0, "*": I.STAR, "1": 1, "1*": I.G([1], [1]), "256*": I.G([256], [256])})
        print(f"--- split={split}")
        for side, colour in (("L", "W"), ("R", "B")):
            for (W2, B2, e2, dbl) in I.pawn_moves(W, B, None, colour):
                d, new = I.after_move(W2, B2, e2, colour, dbl)
                st = (tuple(sorted(new)), d)
                hit = []
                for k, X in cands.items():
                    nx = I.neg(X)
                    s2 = (st[0], st[1] + nx) if isinstance(nx, int) else (tuple(sorted(st[0] + (nx,))), st[1])
                    if I.outcome(s2) == "P":
                        hit.append(k)
                print(f"  {side}: -> W {nm(W2)} / B {nm(B2)}{' (ep)' if e2 else ''}: value in {hit or 'none of the candidates'}")

if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000); threading.stack_size(512 * 1024 * 1024)
    t = threading.Thread(target=main); t.start(); t.join()
