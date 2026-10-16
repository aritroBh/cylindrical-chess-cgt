"""Print the tables quoted in dawson/REPORT.md.

    PYTHONPATH=. .venv/bin/python -m dawson.report_tables
(needs dawson/misere_c_100.txt from `dawson/misere_c 100` and dawson/quotient_Q32.pkl from
`python -m dawson.quotient 32`)
"""
import pickle
import re

from dawson.octal import grundy, paper_recurrence


def main():
    g = grundy("0.137", 400)
    print("g(n), n = 0..33:", " ".join(str(v) for v in g[0:34]))
    print("g(n), n = 34..67:", " ".join(str(v) for v in g[34:68]))
    print("g(n), n = 52..85 (one full period; g(n+34) = g(n) for all n >= 52):",
          " ".join(str(v) for v in g[52:86]))
    print("exceptions n with g(n) != g(n+34):", [n for n in range(0, 300) if g[n] != g[n + 34]])
    print("g(n) = 0 for n <= 200:", [n for n in range(201) if g[n] == 0])
    R = {n: (1 if g[n - 3] == 0 else 0) for n in range(3, 400)}
    print("cylinder: first player wins (R_n = 1), n <= 200:", [n for n in range(3, 201) if R[n]])
    last = max(n for n in range(3, 300) if R[n] != R[n + 34])
    print(f"cylinder: R_(n+34) = R_n for all n > {last}; last exception n = {last}")
    per = None
    for p in range(1, 35):
        if all(R[n] == R[n + p] for n in range(last + 1, 300)):
            per = p
            break
    print(f"cylinder: least period of R_n on n > {last}: {per}")
    G = paper_recurrence(400)
    pr = {n: (1 if G[n - 3] == 0 else 0) for n in range(3, 400)}
    print("paper's G(n), n = 0..33:", " ".join(str(v) for v in G[0:34]))
    print("paper's ring wins, n <= 100:", [n for n in range(3, 101) if pr[n]])
    print("correct ring wins, n <= 100:", [n for n in range(3, 101) if R[n]])

    txt = open("dawson/misere_c_100.txt").read()
    strip = re.search(r"single strip n=0\.\.100: (\S+)", txt).group(1)
    Pn = [n for n, c in enumerate(strip) if c == "P"]
    print("misere single strips P (n <= 100):", Pn)
    print("normal single strips P (n <= 100):", [n for n in range(101) if g[n] == 0])
    diff = [n for n in range(101) if (strip[n] == "P") != (g[n] == 0)]
    print("n <= 100 where misere and normal single-strip outcomes differ:", diff)
    # crude periodicity probe on the misere single-strip outcomes
    best = []
    for p in range(1, 35):
        bad = [n for n in range(0, 101 - p) if strip[n] != strip[n + p]]
        best.append((max(bad) if bad else -1, p))
    best.sort()
    print("periodicity probe, p <= 34: (last n with o(n) != o(n+p), p), best 5:", best[:5],
          "; a period p would need last n << 100 - p")
    print("misere rings: first player wins for n <= 103:", [n + 3 for n in Pn if n + 3 <= 103] if 0 not in Pn else None)

    d = pickle.load(open("dawson/quotient_Q32.pkl", "rb"))
    P, phi = d["P"], d["phi"]
    print("Q_32: |Q| =", len(P), " |P| =", sum(P))
    print("Q_32 single strips P:", [n for n in range(1, 33) if P[phi[1 if n == 2 else n]]])
    print("Q_32: strips equivalent to the empty position (Phi = identity):",
          [n for n in range(1, 33) if phi[1 if n == 2 else n] == 0])


if __name__ == "__main__":
    main()
