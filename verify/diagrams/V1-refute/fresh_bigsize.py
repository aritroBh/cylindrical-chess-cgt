"""fresh.py with BIG = 32 and 1024: do the V1 verdicts depend on the size of BIG?
(7.1 {h,a} is reported as {k|*} for the k found; 7.3 should equal BIG.)
Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/diagrams/V1-refute/fresh_bigsize.py
"""
import sys, threading
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import fresh as F

def main():
    for big in (32, 1024):
        F.BIG = big
        for ep in (True, False):
            for rule in ("count", "white", "black"):
                F.OPT.update(wrap=True, ep=ep, rule=rule, epaware=False); F.MEMO.clear()
                out = []
                for label, text in F.POS.items():
                    if label == "7.1ah":
                        ks = [k for k in range(big - 4, big + 6) if F.equal(text, F.G([k], [F.STAR]))]
                        out.append(f"7.1ah={{{ks}|*}}")
                    elif label == "7.3":
                        out.append(f"7.3=BIG:{F.equal(text, big)}")
                    elif label == "7.2abh":
                        out.append(f"7.2abh:{F.outcome(F.start(text))}")
                    else:
                        c = F.claimed(label, ep)
                        out.append(f"{label}:{'OK' if any(F.equal(text, X) for _, X in c) else 'FAIL'}")
                print(f"BIG={big} ep={'on ' if ep else 'off'} {rule:6s}: " + "  ".join(out), flush=True)

if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000); threading.stack_size(512 * 1024 * 1024)
    th = threading.Thread(target=main); th.start(); th.join()
