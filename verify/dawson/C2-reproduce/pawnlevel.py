"""Independent pawn-level minimax for 3 x W Dawson's chess (verifier scratch).

Rules: W pawns on rank 1 move up, B pawns on rank 3 move down, one square straight onto
an empty square or one square diagonally to capture; captures compulsory; normal play
(no legal move = loss).  A pawn reaching its last rank is counted in PROMO (should stay 0).
Files wrap if cyl=True.  Does not import dawson/ or cylcgt/.

For every pattern of untouched / empty files on boards of width <= WMAX (flat) and
3 <= W <= WMAX (cylinder), compares the minimax outcome (both sides to move) with the
prediction from g (xor over runs; cyclic runs on the cylinder; full ring -> R_W).
It also checks the paper's G against the same outcomes, to list contradictions.

Run:  cd <root> && .venv/bin/python verify/dawson/C2-reproduce/pawnlevel.py 11
"""
import sys
from functools import lru_cache
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from indep import pin_model, paper_recurrence  # noqa: E402

sys.setrecursionlimit(100000)
PROMO = [0]


def make_solver(Wd, cyl):
    def nb(f):
        out = []
        for d in (-1, 1):
            h = f + d
            if cyl:
                h %= Wd
            if 0 <= h < Wd and h != f:
                out.append(h)
        return out
    NB = [nb(f) for f in range(Wd)]

    def moves(s, side):
        # s: tuple of length 3*Wd, index f*3 + (rank-1)
        me, opp, dr = ("W", "B", 1) if side == 0 else ("B", "W", -1)
        caps, pushes = [], []
        for f in range(Wd):
            for r in range(3):
                if s[f * 3 + r] != me:
                    continue
                t = r + dr
                if not (0 <= t < 3):
                    continue
                for h in NB[f]:
                    if s[h * 3 + t] == opp:
                        caps.append((f * 3 + r, h * 3 + t, t))
                if s[f * 3 + t] == ".":
                    pushes.append((f * 3 + r, f * 3 + t, t))
        out = []
        for a, b, t in (caps if caps else pushes):
            if (side == 0 and t == 2) or (side == 1 and t == 0):
                PROMO[0] += 1
            l = list(s)
            l[b] = l[a]
            l[a] = "."
            out.append(tuple(l))
        return out

    @lru_cache(maxsize=None)
    def win(s, side):
        for t in moves(s, side):
            if not win(t, 1 - side):
                return True
        return False
    return win


def start(pattern):
    s = []
    for c in pattern:
        s += ["W", ".", "B"] if c == "1" else [".", ".", "."]
    return tuple(s)


def runs(pattern, cyl):
    if cyl and "0" not in pattern:
        return None  # full ring
    if cyl:
        k = pattern.index("0")
        pattern = pattern[k:] + pattern[:k]
    return [len(x) for x in pattern.split("0") if x]


def main(WMAX):
    N = WMAX + 5
    g = pin_model(N)
    G = paper_recurrence(N)
    bad = 0
    tested = 0
    paper_contra = []
    for cyl in (False, True):
        for Wd in range(1 if not cyl else 3, WMAX + 1):
            win = make_solver(Wd, cyl)
            for m in range(1 << Wd):
                pat = format(m, f"0{Wd}b")
                rs = runs(pat, cyl)
                if rs is None:
                    pred = (g[Wd - 3] == 0)
                    ppred = (G[Wd - 3] == 0)
                else:
                    x = 0
                    xp = 0
                    for r in rs:
                        x ^= g[r]
                        xp ^= G[r]
                    pred = x != 0
                    ppred = xp != 0
                s = start(pat)
                ow, ob = win(s, 0), win(s, 1)
                tested += 1
                if ow != pred or ob != pred:
                    bad += 1
                    print("MISMATCH", "cyl" if cyl else "flat", pat, ow, ob, pred)
                if ow != ppred and (rs is None or len(rs) == 1):
                    paper_contra.append(("cyl" if cyl else "flat", Wd, pat, ow))
            print(f"{'cyl ' if cyl else 'flat'} W={Wd:2d}: done, cache={win.cache_info().currsize}", flush=True)
    print(f"patterns tested: {tested}, mismatches vs g: {bad}, promotions seen: {PROMO[0]}")
    single = sorted({(k, Wd, pat.count('1'), o) for k, Wd, pat, o in paper_contra
                     if (k == 'flat' and pat == '1' * Wd) or (k == 'cyl' and pat == '1' * Wd)})
    print("full-board contradictions of the paper's G (kind, width, -, first player wins):")
    for c in single:
        print("  ", c)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 10)
