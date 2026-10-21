"""Sanity check that fresh.py's e.p.-aware switch and race rules actually bite, using the known
*2 candidate (RESULTS.md section 1): W a2 c2 / B b7 d7 on files a-d of a flat board (file e empty).
Expected from RESULTS.md: textbook test -> *2 under count and mover, 0 under opponent;
e.p.-aware test (count) -> {2+-1 | -2+-1}.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python -I verify/diagrams/V1-refute/fresh_sanity.py
"""
import sys, threading
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import fresh as F

def main():
    t = "W: a2 c2 / B: b7 d7"
    STAR2 = F.G([0, F.STAR], [0, F.STAR])
    SW = F.G([F.G([3], [1])], [F.G([-1], [-3])])
    for epaware in (False, True):
        for ep in (True, False):
            if epaware and not ep:
                continue
            for rule in ("count", "mover", "opponent"):
                F.OPT.update(wrap=False, ep=ep, rule=rule, epaware=epaware); F.MEMO.clear()
                print(f"{'epaware ' if epaware else 'textbook'} ep={'on ' if ep else 'off'} {rule:8s}: outcome {F.outcome(F.start(t))}"
                      f"  =*2 {F.equal(t, STAR2)}  =0 {F.equal(t, 0)}  ={{2+-1|-2+-1}} {F.equal(t, SW)}", flush=True)

if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000); threading.stack_size(512 * 1024 * 1024)
    th = threading.Thread(target=main); th.start(); th.join()
