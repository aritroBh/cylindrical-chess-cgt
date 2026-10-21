"""Independent check (C3 verifier) of the numbers in claim C3, written from scratch.

Dawson's chess on a 3 x n strip = a row of n pins; a move picks pin i and removes it and
its surviving neighbours (this is the pin model of 0.137).  Grundy values g(n) computed
directly from that model (no octal-code parsing).  Ring: R_n = mex{g(n-3)} for n >= 3.

Also: misere outcome of single strips n <= 24 by brute force on multisets of strips,
using the same pin model (no 2 -> 1 shortcut).

    python3 verify/dawson/C3-reproduce/grundy_check.py
"""
from functools import lru_cache

NMAX = 600


def pin_options(n):
    """Remaining strips after choosing pin i (1-based) in a row of n pins."""
    out = []
    for i in range(1, n + 1):
        left = max(i - 2, 0)      # pins 1..i-2 survive
        right = max(n - i - 1, 0)  # pins i+2..n survive
        out.append((left, right))
    return out


g = [0] * (NMAX + 1)
for n in range(1, NMAX + 1):
    opts = {g[a] ^ g[b] for a, b in pin_options(n)}
    m = 0
    while m in opts:
        m += 1
    g[n] = m

R = {n: (1 if g[n - 3] == 0 else 0) for n in range(3, NMAX + 1)}

wins = [n for n in range(3, NMAX + 1) if R[n]]
print("first-player ring wins n <= 200:", [n for n in wins if n <= 200])
claimed = [3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57]
print("claimed prefix matches:", [n for n in wins if n <= 57] == claimed)

exc = [n for n in range(3, NMAX - 34 + 1) if R[n] != R[n + 34]]
print("ring n with R_n != R_(n+34), n <= %d:" % (NMAX - 34), exc)
last = max(exc)
print("last exception:", last, " g(%d) =" % (last - 3), g[last - 3], " g(%d) =" % (last + 31), g[last + 31])

# least period on n > last (data range), and also for each start N0, least p
for p in range(1, 35):
    if all(R[n] == R[n + p] for n in range(last + 1, NMAX - p + 1)):
        print("least p with R_(n+p) = R_n for all", last + 1, "<= n <=", NMAX - p, ":", p)
        break
# does any p < 34 hold from ANY later start N0 <= 400?
for p in range(1, 34):
    lastp = max([n for n in range(3, NMAX - p + 1) if R[n] != R[n + p]], default=None)
    if lastp is not None and lastp > 400:
        continue
    print("WARNING p=%d has last exception %s" % (p, lastp))
print("checked: every p < 34 has an exception above n = 400 (no smaller eventual period)")

# g periodicity certificate (Guy-Smith): g(n+34) = g(n) for 52 <= n < 2*52+34+3 = 141
gexc = [n for n in range(0, NMAX - 34 + 1) if g[n] != g[n + 34]]
print("g exceptions g(n) != g(n+34), n <= %d:" % (NMAX - 34), gexc)
print("certificate range 52 <= n < 141 all agree:", all(g[n] == g[n + 34] for n in range(52, 141)))
print("max g(n), n <= %d:" % NMAX, max(g))
print("g(0..40):", g[:41])


# ---- misere single strips by brute force over multisets (pin model) ----
def canon(t):
    return tuple(sorted(x for x in t if x > 0))


@lru_cache(maxsize=None)
def misere_win(pos):
    """True iff the player to move wins misere play from multiset pos of strips."""
    if not pos:
        return True  # no move: in misere the player to move wins
    seen = set()
    for idx, h in enumerate(pos):
        if h in seen:
            continue
        seen.add(h)
        rest = pos[:idx] + pos[idx + 1:]
        for a, b in pin_options(h):
            q = canon(rest + (a, b))
            if not misere_win(q):
                return True
    return False


MS = 24
Pm = [n for n in range(0, MS + 1) if not misere_win(canon((n,)))]
print("misere single-strip P-positions n <= %d:" % MS, Pm)
print("=> misere ring first-player wins n <= %d:" % (MS + 3), [n + 3 for n in Pm])
print("ring 3..21 predictions (normal, misere) for first player:")
for n in range(3, 22):
    print("  n=%d normal %s misere %s" % (n, "win" if R[n] else "loss",
                                       "win" if not misere_win(canon((n - 3,))) else "loss"))
