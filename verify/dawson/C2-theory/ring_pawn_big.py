"""Pawn-level outcome of larger 3 x n boards using check_c2.pawn_outcome (independent solver).
Run: cd verify/dawson/C2-theory && ../../../.venv/bin/python ring_pawn_big.py
"""
import sys, time
sys.setrecursionlimit(1000000)
import check_c2 as c
g = c.g_recurrence(40); G = c.G_paper(40)
for n, wrap in [(10,True),(11,True),(12,True),(13,True),(14,True),(15,True),(16,True),(17,True),(20,False),(23,True)]:
    t = time.time()
    w, p = c.pawn_outcome(n, wrap)
    pred = (g[n-3] == 0) if wrap else (g[n] != 0)
    ppred = (G[n-3] == 0) if wrap else (G[n] != 0)
    print(f"{'ring' if wrap else 'flat'} n={n}: first player wins={w} g-pred={pred} paperG-pred={ppred} promo={p} {time.time()-t:.1f}s", flush=True)
