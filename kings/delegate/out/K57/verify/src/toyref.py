"""K57 referee: abstract brute-force test of Lemma 4.15 and Proposition 4.14 (own code; not toy57.py).

Toy groups model the two chess features the proof has to handle and that the K56 referee's toy.py leaves out:
- checks: chk[g][s] = "side s is in check on board g". A side in check may not move in T (or spend a token). A move of
  side s into a board where s is in check is illegal (removed), so a side is never in check right after its own move.
  Alone (P), a side with no move is checkmated (loss) if in check, stalemated (draw) otherwise.
- e.p. rights: a move may be a "double step" (d = 1); it gives the opponent the right, i.e. access to the extra moves
  ep[g][s] at the target board, for one turn only. A move in T (or a token) clears it. States carry the flag f.
Terminals: WT (White has won), BT (Black has won) are the promotions. Roots 0, 1 (flag 0); Black's shuttle 0 <-> 1.
Definition 4.8 (over orientation) is applied in P; (B1) in the D-sum with -1; then r(G (+) T) is compared with
r(over_D (+) T) at both roots and every q state, both sides, every t, beside random and hand-made finite D-games T.
Also reports K56's tempo-exactness (T3) on White's side, to count groups where Lemma 4.15 goes beyond Lemma 4.13.
usage: python3 toyref.py SEED NGROUPS NRANDOMTESTS [random|gadget]
"""
import random
import sys
from collections import deque

WT, BT = "W", "B"


def lfp(nstates, side, opts, nomove):
    """Least fixed point. opts[i]: list of state indices or WT/BT. nomove[i]: value when no option ('W','L','D').
    side[i] 0 = White to move. Returns list of 'W','L','D' (White's view)."""
    val = ["D"] * nstates
    pred = [[] for _ in range(nstates)]
    cntW = [0] * nstates  # for Black-to-move states: options not yet known White wins
    cntL = [0] * nstates  # for White-to-move states: options not yet known Black wins
    q = deque()
    for i in range(nstates):
        o = opts[i]
        if not o:
            if nomove[i] != "D":
                val[i] = nomove[i]
                q.append(i)
            continue
        s = side[i]
        good = WT if s == 0 else BT
        if good in o:
            val[i] = "W" if s == 0 else "L"
            q.append(i)
            continue
        bad = BT if s == 0 else WT
        n_nonbad = sum(1 for t in o if t != bad)
        if n_nonbad == 0:
            val[i] = "L" if s == 0 else "W"
            q.append(i)
            continue
        if s == 1:
            cntW[i] = n_nonbad
        else:
            cntL[i] = n_nonbad
        for t in o:
            if t not in (WT, BT):
                pred[t].append(i)
    while q:
        v = q.popleft()
        for u in pred[v]:
            if val[u] != "D":
                continue
            s = side[u]
            if val[v] == "W":
                if s == 0:
                    val[u] = "W"
                    q.append(u)
                else:
                    cntW[u] -= 1
                    if cntW[u] == 0:
                        val[u] = "W"
                        q.append(u)
            else:
                if s == 1:
                    val[u] = "L"
                    q.append(u)
                else:
                    cntL[u] -= 1
                    if cntL[u] == 0:
                        val[u] = "L"
                        q.append(u)
    return val


class Group:
    def __init__(self, n, mv, ep, chk):
        self.n, self.mv, self.ep, self.chk = n, mv, ep, chk  # mv[g][s]: list of (target, d); ep[g][s]: list of (target, d)

    def moves(self, g, f, s):
        return self.mv[g][s] + (self.ep[g][s] if f else [])


def alone(G, X=None, tokens=0, sumrule=False):
    """G alone (P) or with k tokens of X. State (g, f, s, l). Returns dict -> value."""
    layers = range(tokens + 1)
    idx, st = {}, []
    for l in layers:
        for g in range(G.n):
            for f in (0, 1):
                for s in (0, 1):
                    idx[(g, f, s, l)] = len(st)
                    st.append((g, f, s, l))
    side, opts, nomove = [], [], []
    for (g, f, s, l) in st:
        o = []
        for (y, d) in G.moves(g, f, s):
            o.append(y if y in (WT, BT) else idx[(y, d, 1 - s, l)])
        if X == s and l > 0 and not G.chk[g][s]:
            o.append(idx[(g, 0, 1 - s, l - 1)])
        side.append(s)
        opts.append(o)
        lose = "L" if s == 0 else "W"
        nomove.append(lose if (sumrule or G.chk[g][s]) else "D")
    val = lfp(len(st), side, opts, nomove)
    return {st[i]: val[i] for i in range(len(st))}


def sum_vals(G, T):
    """r(G (+) T), Definition 1.3 with the chess conventions above. T = (L, R) lists of options per position."""
    LT, RT = T
    k = len(LT)
    idx, st = {}, []
    for g in range(G.n):
        for f in (0, 1):
            for t in range(k):
                for s in (0, 1):
                    idx[(g, f, t, s)] = len(st)
                    st.append((g, f, t, s))
    side, opts, nomove = [], [], []
    for (g, f, t, s) in st:
        o = []
        for (y, d) in G.moves(g, f, s):
            o.append(y if y in (WT, BT) else idx[(y, d, t, 1 - s)])
        if not G.chk[g][s]:
            for y in (LT[t] if s == 0 else RT[t]):
                o.append(y if y in (WT, BT) else idx[(g, 0, y, 1 - s)])
        side.append(s)
        opts.append(o)
        nomove.append("L" if s == 0 else "W")
    val = lfp(len(st), side, opts, nomove)
    return {st[i]: val[i] for i in range(len(st))}


def over_vals(T):
    """r(over_D (+) T): positions 0 = omega (L = {0_D}, R = {omega}), 1 = 0_D."""
    LT, RT = T
    k = len(LT)
    idx, st = {}, []
    for o in (0, 1):
        for t in range(k):
            for s in (0, 1):
                idx[(o, t, s)] = len(st)
                st.append((o, t, s))
    side, opts, nomove = [], [], []
    for (o, t, s) in st:
        op = []
        if o == 0:
            op.append(idx[(1, t, 1)] if s == 0 else idx[(0, t, 0)])
        for y in (LT[t] if s == 0 else RT[t]):
            op.append(y if y in (WT, BT) else idx[(o, y, 1 - s)])
        side.append(s)
        opts.append(op)
        nomove.append("L" if s == 0 else "W")
    val = lfp(len(st), side, opts, nomove)
    return {st[i]: val[i] for i in range(len(st))}


M1 = ([[], []], [[1], []])  # -1: Black has one move, then 0


def exact_over(G):
    """Definition 4.8, over orientation. Returns (qstates, freezes) or None. qstates: list of (q, flag)."""
    if any(G.chk[r][s] for r in (0, 1) for s in (0, 1)):
        return None
    p = alone(G)
    for r, o in ((0, 1), (1, 0)):
        if (o, 0) not in G.mv[r][1]:
            return None
        for (y, d) in G.mv[r][1]:
            if (y, d) == (o, 0):
                continue
            if y == BT:
                return None
            if y != WT and p[(y, d, 0, 0)] != "W":
                return None
    qs = set()
    for r in (0, 1):
        fr = []
        for (y, d) in G.mv[r][0]:
            if y == WT:
                return None
            if y == BT:
                continue
            if p[(y, d, 1, 0)] != "L":
                fr.append((y, d))
        if not fr:
            return None
        qs.update(fr)
    for (q, d) in qs:
        if q in (0, 1) or G.chk[q][1]:
            return None
        bm = G.moves(q, d, 1)
        wm = G.moves(q, 0, 0)
        if not bm or not wm:
            return None
        if p[(q, d, 1, 0)] != "W" or p[(q, 0, 0, 0)] != "L":
            return None
        for (y, dd) in bm:  # every legal Black move loses at once (value W already says this unless checkmate)
            if y == BT or (y != WT and p[(y, dd, 0, 0)] != "W"):
                return None
        for (y, dd) in wm:
            if y == WT or (y != BT and p[(y, dd, 1, 0)] != "L"):
                return None
    return sorted(qs, key=str)


M2 = ([[], [], []], [[1], [2], []])  # -2
OFF = ([[]], [[0]])


def b1(G, T=M1, need="W"):
    sv = sum_vals(G, T)
    for r, o in ((0, 1), (1, 0)):
        for (y, d) in G.mv[r][1]:
            if (y, d) == (o, 0) or y == WT:
                continue
            if sv[(y, d, 0, 0)] != need:
                return False
    return True


def t3_fails(G, qs):
    """K56's (T3) on White's side, read with the pass game (stalemate draw): True if some non-freeze White root move
    is neither lost against unlimited White passes nor lost at once after a Black pass in reply."""
    pinf = alone_inf(G, 0)
    p0 = alone(G)
    for r in (0, 1):
        for (y, d) in G.mv[r][0]:
            if (y, d) in qs or y == BT:
                continue
            ninf = pinf[(y, d, 1)] == "L"
            v0 = (not G.chk[y][1]) and p0[(y, 0, 0, 0)] == "L"
            if not (ninf or v0):
                return True
    return False


def alone_inf(G, X):
    idx, st = {}, []
    for g in range(G.n):
        for f in (0, 1):
            for s in (0, 1):
                idx[(g, f, s)] = len(st)
                st.append((g, f, s))
    side, opts, nomove = [], [], []
    for (g, f, s) in st:
        o = [y if y in (WT, BT) else idx[(y, d, 1 - s)] for (y, d) in G.moves(g, f, s)]
        if s == X and not G.chk[g][s]:
            o.append(idx[(g, 0, 1 - s)])
        side.append(s)
        opts.append(o)
        nomove.append(("L" if s == 0 else "W") if G.chk[g][s] else "D")
    val = lfp(len(st), side, opts, nomove)
    return {st[i]: val[i] for i in range(len(st))}


# ---------------- random groups ----------------
def legalize(G):
    for g in range(G.n):
        for s in (0, 1):
            G.mv[g][s] = [(y, d) for (y, d) in G.mv[g][s] if y in (WT, BT) or not G.chk[y][s]]
            G.ep[g][s] = [(y, d) for (y, d) in G.ep[g][s] if y in (WT, BT) or not G.chk[y][s]]
            # a side cannot be in check after its own move; also d only matters for real targets
    return G


def rand_moves(rng, n, p, pterm, pd):
    o = [(t, 1 if rng.random() < pd else 0) for t in range(n) if rng.random() < p]
    if rng.random() < pterm:
        o.append((WT, 0))
    if rng.random() < pterm:
        o.append((BT, 0))
    return o


def rand_group(rng):
    n = rng.randint(4, 9)
    p = rng.choice([0.15, 0.25, 0.35])
    pterm = rng.choice([0.15, 0.3])
    pd = rng.choice([0.0, 0.2, 0.4])
    pc = rng.choice([0.0, 0.15, 0.3])
    pe = rng.choice([0.0, 0.2, 0.4])
    chk = [[(g >= 2 and rng.random() < pc) for s in (0, 1)] for g in range(n)]
    mv = [[rand_moves(rng, n, p, pterm, pd) for s in (0, 1)] for g in range(n)]
    ep = [[(rand_moves(rng, n, p / 2, pterm / 2, 0.0) if rng.random() < pe else []) for s in (0, 1)] for g in range(n)]
    G = legalize(Group(n, mv, ep, chk))
    for _ in range(4):  # repair the roots towards Definition 4.8
        pv = alone(G)
        zz = []
        for q in range(2, n):
            if chk[q][1] or chk[q][0]:
                continue
            for d in (0, 1):
                if pv[(q, d, 1, 0)] == "W" and pv[(q, 0, 0, 0)] == "L" and G.moves(q, d, 1) and G.moves(q, 0, 0):
                    zz.append((q, d))
        if not zz:
            return None
        wl = [(y, d) for y in range(n) for d in (0, 1) if not chk[y][0] and pv[(y, d, 1, 0)] == "L"] + [(BT, 0)]
        bl = [(y, d) for y in range(n) for d in (0, 1) if not chk[y][1] and pv[(y, d, 0, 0)] == "W"] + [(WT, 0)]
        for r, o in ((0, 1), (1, 0)):
            G.mv[r][0] = list(set(rng.sample(zz, rng.randint(1, min(2, len(zz)))) + rng.sample(wl, rng.randint(0, min(4, len(wl))))))
            G.mv[r][1] = list(set([(o, 0)] + [x for x in rng.sample(bl, rng.randint(0, min(4, len(bl)))) if x[0] != o]))
            G.ep[r] = [[], []]
    return G


def gadget_group(rng):
    """Adversarial family built from gadgets (then randomly perturbed):
    - Black's bad root moves enter a chain of length j: at each chain node Black's only moves are suicides (to WT),
      White's move goes on; White to move at the last node must move to BT. In P (no passes) the move loses at once;
      with k Black tokens it is saved iff k >= j. j = 1 breaks (B1), j = 2 gives (B1) but not two tokens, larger j more.
    - White's bad root moves enter the mirror chain (saved by j White passes; or a loop: saved by unlimited passes):
      the K56 (T3) failures that Lemma 4.15 claims not to need.
    - q gadget: a mutual zugzwang whose moves lose at once, possibly behind a double step / a check on the losers."""
    mv, ep, chk = [], [], []

    def new(c=(False, False)):
        mv.append([[], []])
        ep.append([[], []])
        chk.append(list(c))
        return len(mv) - 1
    A, B = new(), new()
    mv[A][1].append((B, 0))
    mv[B][1].append((A, 0))
    # q gadget(s)
    qs = []
    for _ in range(rng.randint(1, 2)):
        q = new()
        zb = new((rng.random() < 0.3, False))  # after a Black move at q: White to move wins (WT), maybe White in check
        mv[zb][0].append((WT, 0))
        mv[zb][1].append((rng.choice([zb, q]), 0))
        zw = new()  # after a White move at q: Black to move wins
        mv[zw][1].append((BT, 0))
        mv[zw][0].append((rng.choice([zw, q]), 0))
        mv[q][1].append((zb, 0))
        if rng.random() < 0.5:
            mv[q][1].append((WT, 0))
        mv[q][0].append((zw, rng.randint(0, 1)))
        if rng.random() < 0.3:
            ep[q][1].append((zb, 0))  # an extra Black move only with the e.p. right
        qs.append(q)
    for r in (A, B):
        for q in rng.sample(qs, rng.randint(1, len(qs))):
            mv[r][0].append((q, rng.randint(0, 1)))
    # Black's bad moves: chains
    for r, o in ((A, B), (B, A)):
        for _ in range(rng.randint(0, 3)):
            j = rng.choice([1, 2, 2, 3, 4])
            chain = [new((False, rng.random() < 0.15)) for _ in range(j)]
            for i, c in enumerate(chain):
                mv[c][1].append((WT, 0))
                if rng.random() < 0.3:
                    mv[c][1].append((rng.choice([A, B] + chain), 0))  # noise; legality/exactness filter decides
                mv[c][0].append((chain[i + 1], rng.randint(0, 1)) if i + 1 < j else (BT, 0))
            x = new()
            mv[x][0].append((chain[0], 0))
            if rng.random() < 0.3:
                mv[x][0].append((WT, 0))
            mv[r][1].append((x, rng.randint(0, 1)))
    # White's bad moves: mirror chains or loops
    for r in (A, B):
        for _ in range(rng.randint(0, 3)):
            j = rng.choice([1, 2, 3, 50])
            jj = min(j, 4)
            chain = [new((rng.random() < 0.15, False)) for _ in range(jj)]
            for i, c in enumerate(chain):
                mv[c][0].append((BT, 0))
                if i + 1 < jj:
                    mv[c][1].append((chain[i + 1], rng.randint(0, 1)))
                else:
                    mv[c][1].append((chain[0], 0) if j == 50 else (WT, 0))
            x = new()
            mv[x][1].append((chain[0], 0))
            mv[r][0].append((x, rng.randint(0, 1)))
    n = len(mv)
    for _ in range(rng.randint(0, 3)):  # random perturbation
        g = rng.randrange(2, n)
        s = rng.randint(0, 1)
        mv[g][s].append((rng.choice(list(range(n)) + [WT, BT]), rng.randint(0, 1)))
    return legalize(Group(n, mv, ep, chk))


# ---------------- test games ----------------
NAMED = {
    "0": ([[]], [[]]), "-1": M1, "1": ([[1], []], [[], []]), "2": ([[1], [2], []], [[], [], []]),
    "-2": ([[], [], []], [[1], [2], []]), "3": ([[1], [2], [3], []], [[], [], [], []]),
    "on": ([[0]], [[]]), "off": ([[]], [[0]]), "dud": ([[0]], [[0]]), "*": ([[1], []], [[1], []]),
    "up": ([[1], [], [1]], [[2], [], [1]]), "down": ([[2], [], [1]], [[1], [], [1]]),
    "Wthreat": ([[1], [WT]], [[], []]), "Bthreat": ([[], []], [[1], [BT]]),
    "Wthr_ans": ([[1], [WT], []], [[], [2], []]), "Bthr_ans": ([[], [2], []], [[1], [BT], []]),
    "hot": ([[WT]], [[BT]]), "onB": ([[0]], [[BT]]), "offW": ([[WT]], [[0]]),
    "Wspare_Bthr": ([[0, 1], [], []], [[2], [], [BT]]), "Bspare_Wthr": ([[2], [], [WT]], [[0, 1], [], []]),
    "Bslow": ([[], [], [], []], [[1], [2], [3], [BT]]), "Wslow": ([[1], [2], [3], [WT]], [[], [], [], []]),
    "W3_then_B": ([[1], [2], [3], []], [[], [], [], [BT]]),
}


def rand_T(rng, kmax=4):
    k = rng.randint(1, kmax)
    p = rng.choice([0.2, 0.35, 0.5])
    pt = rng.choice([0.0, 0.15, 0.3])
    L, R = [], []
    for _ in range(k):
        for side in (L, R):
            o = [t for t in range(k) if rng.random() < p]
            if rng.random() < pt:
                o.append(WT)
            if rng.random() < pt:
                o.append(BT)
            side.append(o)
    return (L, R)


def main():
    seed, ngroups, ntests = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    mode = sys.argv[4] if len(sys.argv) > 4 else "random"
    rng = random.Random(seed)
    tests = list(NAMED.items()) + [(f"r{i}", rand_T(rng)) for i in range(ntests)]
    ovs = [over_vals(T) for _, T in tests]
    # Proposition 4.14: r(0_D (+) t, s) <= r(omega (+) t, s) for White, on these and on larger random T
    order = {"L": 0, "D": 1, "W": 2}
    p414 = viol = 0
    for T in [T for _, T in tests] + [rand_T(rng, 7) for _ in range(3000)]:
        ov = over_vals(T)
        for t in range(len(T[0])):
            for s in (0, 1):
                p414 += 1
                if order[ov[(1, t, s)]] > order[ov[(0, t, s)]]:
                    viol += 1
                    print("P4.14 VIOLATION", T, t, s)
    print(f"Proposition 4.14: {p414} comparisons, {viol} violations")
    st = dict(tried=0, exact=0, exact_b1=0, b1_t3fail=0, b1_chk=0, b1_ep=0, b1_diff_groups=0, b1_results=0, b1_diffs=0,
              nob1=0, nob1_diff_groups=0)
    seen = set()
    while st["exact_b1"] < ngroups and st["tried"] < 3000 * ngroups:
        st["tried"] += 1
        G = gadget_group(rng) if mode == "gadget" else rand_group(rng)
        if G is None:
            continue
        key = repr((G.mv, G.ep, G.chk))
        if key in seen:
            continue
        seen.add(key)
        qs = exact_over(G)
        if qs is None:
            continue
        st["exact"] += 1
        hb1 = b1(G)
        if not hb1 and st["nob1"] >= ngroups:
            continue
        diff = nres = 0
        for (name, T), ov in zip(tests, ovs):
            sv = sum_vals(G, T)
            for t in range(len(T[0])):
                for s in (0, 1):
                    for r in (0, 1):
                        nres += 1
                        if sv[(r, 0, t, s)] != ov[(0, t, s)]:
                            diff += 1
                            if hb1 and diff <= 3:
                                print("COUNTEREXAMPLE to Lemma 4.15:", name, T, "root", r, "t", t, "s", s, sv[(r, 0, t, s)], ov[(0, t, s)])
                    for (q, d) in qs:
                        for (f, s2) in ((d, 1), (0, 1), (0, 0)):
                            if s2 != s:
                                continue
                            nres += 1
                            if sv[(q, f, t, s2)] != ov[(1, t, s2)]:
                                diff += 1
                                if hb1 and diff <= 3:
                                    print("COUNTEREXAMPLE (q):", name, T, "q", q, f, "t", t, "s", s2)
        if hb1:
            st["exact_b1"] += 1
            st["b1_results"] += nres
            st["b1_diffs"] += diff
            st["b1_diff_groups"] += diff > 0
            st["b1_t3fail"] += t3_fails(G, qs)
            st["b1_chk"] += any(G.chk[g][s] for g in range(G.n) for s in (0, 1))
            st["b1_ep"] += any(d for g in range(G.n) for s in (0, 1) for (_, d) in G.mv[g][s])
            st["b1_not_b2"] = st.get("b1_not_b2", 0) + (not b1(G, M2))
            st["b1_not_off"] = st.get("b1_not_off", 0) + (not b1(G, OFF))
            fr = [sorted((y, d) for (y, d) in G.mv[r][0] if (y, d) in qs) for r in (0, 1)]
            st["b1_diff_freezes"] = st.get("b1_diff_freezes", 0) + (fr[0] != fr[1])
            if diff:
                print("GROUP", G.n, G.mv, G.ep, G.chk, qs)
        else:
            st["nob1"] += 1
            st["nob1_diff_groups"] += diff > 0
    print(st)


if __name__ == "__main__":
    main()
