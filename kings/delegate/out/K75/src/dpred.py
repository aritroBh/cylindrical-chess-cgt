"""K72 copy of kings/delegate/out/K63/verify/src/dpred_h.py, unchanged except this line (the prediction depends on the ranks only, so the h table serves every context file).  K63 referee: D-sum prediction for F2 beside a context X of pawns on file h (written from LOOPY
Definitions 1.1-1.3, Proposition 4.6 and Lemma 4.15; no code of the investigator read or used).

X = the D-game of the h-file pawns alone: a White pawn steps up one square (two from rank 2) to an
empty square, a Black pawn down (two from rank 7); on one file there are no captures and no e.p.;
a move to the last rank is a promotion, a terminal win for the mover.  over_D has positions w (omega)
and 0: White may play w -> 0, Black may play w -> w (Proposition 4.6).  In the sum a side with no
move loses, a promotion ends the play, an infinite play is a draw.  Prediction (Corollary 4.17 with
Lemma 4.15): root, side s to move: r(w (+) X, s); q, side s: r(0 (+) X, s) = r(X, s).
Prints, for every context of at most 2 + 2 pawns on h2-h7 (in the investigator's enumeration order is
not assumed; contexts are keyed by their pawn list), the 8 predicted results in the order
A b, A w, B b, B w, qA b, qA w, qB b, qB w (White's view: W, L, D).
"""
import itertools, sys

RANKS = range(2, 8)

def moves(x, side):
    """x: tuple of 8 chars indexed by rank 1..8 (index 0 unused) -> list of (new x or 'PROM')."""
    out = []
    for r in RANKS:
        if side == 0 and x[r] == 'P':
            if r + 1 == 8:
                out.append('PROM'); continue
            if x[r + 1] == '.':
                y = list(x); y[r] = '.'; y[r + 1] = 'P'; out.append(tuple(y))
                if r == 2 and x[4] == '.':
                    y = list(x); y[r] = '.'; y[4] = 'P'; out.append(tuple(y))
        if side == 1 and x[r] == 'p':
            if r - 1 == 1:
                out.append('PROM'); continue
            if x[r - 1] == '.':
                y = list(x); y[r] = '.'; y[r - 1] = 'p'; out.append(tuple(y))
                if r == 7 and x[5] == '.':
                    y = list(x); y[r] = '.'; y[5] = 'p'; out.append(tuple(y))
    return out

def solve(x0):
    # states (g, x, s): g 1 = omega, 0 = zero
    states, stack = set(), []
    for g in (0, 1):
        for s in (0, 1):
            stack.append((g, x0, s))
    succ = {}
    while stack:
        st = stack.pop()
        if st in states: continue
        states.add(st)
        g, x, s = st
        lst = []
        if g == 1:
            lst.append((0, x, 1) if s == 0 else (1, x, 0))   # White w->0, Black w->w
        for y in moves(x, s):
            lst.append('PROM' if y == 'PROM' else (g, y, 1 - s))
        succ[st] = lst
        for t in lst:
            if t != 'PROM' and t not in states: stack.append(t)
    val = {}  # 1 mover wins, 2 mover loses
    ch = True
    while ch:
        ch = False
        for st, lst in succ.items():
            if st in val: continue
            if any(t == 'PROM' or val.get(t) == 2 for t in lst):
                val[st] = 1; ch = True
            elif all(val.get(t) == 1 for t in lst):   # includes no move at all
                val[st] = 2; ch = True
    def absv(g, s):
        v = val.get((g, x0, s))
        if v is None: return 'D'
        return ('W' if s == 0 else 'L') if v == 1 else ('L' if s == 0 else 'W')
    om = {s: absv(1, s) for s in (0, 1)}
    ze = {s: absv(0, s) for s in (0, 1)}
    return [om[1], om[0], om[1], om[0], ze[1], ze[0], ze[1], ze[0]]

def contexts():
    sq = list(RANKS)
    for nw in range(3):
        for ws in itertools.combinations(sq, nw):
            rest = [r for r in sq if r not in ws]
            for nb in range(3):
                for bs in itertools.combinations(rest, nb):
                    yield ws, bs

def name(ws, bs):
    return " ".join([f"Ph{r}" for r in ws] + [f"ph{r}" for r in bs]) or "empty"

if __name__ == "__main__":
    n = 0
    for ws, bs in contexts():
        x = ['.'] * 9
        for r in ws: x[r] = 'P'
        for r in bs: x[r] = 'p'
        print(f"{name(ws, bs):22s} {' '.join(solve(tuple(x)))}")
        n += 1
    print(f"# {n} contexts", file=sys.stderr)
