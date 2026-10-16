"""Definitive value comparison of 7.2 {a,b,h} under two race rules (e.p. off):
G[r1] + (-G[r2]) is P  <=>  equal values.  -G is the colour-swapped, rank-mirrored position.
Uses extra.py/indep.py from this directory only.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
     .venv/bin/python -I verify/diagrams/V1-refute/rulediff.py off count mover
"""
import sys, threading, time
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import indep as I
import extra as E

def main():
    ep, r1, r2 = sys.argv[1] == "on", sys.argv[2], sys.argv[3]
    I.CFG.update(ep=ep, split=True, wrap=True)
    t = time.time()
    ab = "W: a2 b2 h3 / B: a6 b7 h7"
    print(f"7.2abh ep={'on' if ep else 'off'}: G[{r1}] - G[{r2}] outcome:", E.rule_diff(ab, r1, r2),
          f"(P = same value)  states {len(E.MEMO2)}  {time.time()-t:.0f}s", flush=True)

if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000); threading.stack_size(512 * 1024 * 1024)
    th = threading.Thread(target=main); th.start(); th.join()
