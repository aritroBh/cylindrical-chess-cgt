"""Do the V1 verdicts depend on the size of BIG?  Re-run the claim list with BIG = 32 and 1024
(7.1 {h,a} tested as {BIG+2 | *}; 7.3 as BIG).  indep.py only.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/diagrams/V1-refute/bigsize.py
"""
import sys, threading
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import indep as I

def main():
    for big in (32, 1024):
        I.BIG = big
        for ep in (True, False):
            I.CFG.update(ep=ep, rule="count", split=True, wrap=True); I.reset()
            out = []
            for label, X, oc, alts in I.claims(ep):
                t = I.POS[label]
                if X == "AH":
                    ok = I.equals(t, I.G([big + 2], [I.STAR]))
                elif X is None:
                    ok = I.outcome(I.root_state(t)) == oc
                else:
                    if X == 256: X = big
                    ok = I.equals(t, X)
                out.append(f"{label}:{'OK' if ok else 'FAIL'}")
            print(f"BIG={big} ep={'on' if ep else 'off'}: " + "  ".join(out), flush=True)

if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000); threading.stack_size(512 * 1024 * 1024)
    th = threading.Thread(target=main); th.start(); th.join()
