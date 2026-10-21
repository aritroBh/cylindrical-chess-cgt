"""Compare g (0.137) and the paper's G with OEIS data fetched 2026-10-16 (A002187, A071426).
Run: cd verify/dawson/C2-theory && ../../../.venv/bin/python lit_compare.py
"""
import check_c2 as c
A002187 = [0,1,1,2,0,3,1,1,0,3,3,2,2,4,0,5,2,2,3,3,0,1,1,3,0,2,1,1,0,4,5,2,7,4,0,1,1,2,0,3,1,1,0,3,3,2,2,4,4,5,5,2,3,3,0,1,1,3,0,2]  # offset 0
A071426 = [1,1,1,2,2,0,3,3,1,1,1,0,4,3,3,3,2,2,2,4,4,0,5,5,2,2,2,3,3,0,5,0,1,1,1,3,3,3,5,6]  # offset 1; .007 value at n is a(n-2)
g = c.g_recurrence(300); G = c.G_paper(300)
print("g(0..59) == OEIS A002187 (Dawson's chess .137):", g[:60] == A002187)
print("paper G(n) == A071426(n-2) for n=3..42 (octal .007, Treblecross):", [G[n] for n in range(3, 43)] == A071426)
# OEIS 'exceptions' = n where g(n) differs from the eventual period-34 value
ev = lambda n: g[52 + ((n - 52) % 34)]
print("n with g(n) != eventual periodic value:", [n for n in range(52) if g[n] != ev(n)])
print("n with g(n) != g(n+34):", [n for n in range(0, 267) if g[n] != g[n + 34]])
# Is there any eventual period visible in the paper's G up to 300? (not evidence either way)
def lastexc(seq, p):
    return max([n for n in range(len(seq) - p) if seq[n] != seq[n + p]], default=-1)
cands = [(p, lastexc(G, p)) for p in range(1, 150)]
print("paper G: smallest last-exception over periods p<150 within n<=300:", min(cands, key=lambda t: t[1]))
