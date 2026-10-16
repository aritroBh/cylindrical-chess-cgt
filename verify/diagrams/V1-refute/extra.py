"""Extra independent checks for V1 (uses only indep.py from this directory).
 (a) 7.3 {c,d} = tiny(1); (b) 7.1 total: outcome L and != 1 + (+-1) + {{2|1}|0};
 (c) 2.3 on the flat board = 0; (d) audit caveat: 2.2/2.3/3.2 shifted up one rank;
 (e) 7.2 {a,b,h}: is the VALUE the same under the three race rules?  (G_rule1 - G_rule2 = 0 ?)
 (f) 7.2 {a,b,h}: infinitesimal check  -1/16 < G < 1/16.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
     .venv/bin/python -I verify/diagrams/V1-refute/extra.py
"""
import sys, threading
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import indep as I
import builtins, functools
print = functools.partial(builtins.print, flush=True)


def eq_sum(text, Xs):
    """is  G - sum(Xs)  a P-position?"""
    comps, n = I.root_state(text)
    for X in Xs:
        nx = I.neg(X)
        if isinstance(nx, int):
            n += nx
        else:
            comps = tuple(sorted(comps + (nx,)))
    return I.outcome((comps, n)) == "P"


def dyadic(k):
    """the number 1/2^k as an explicit game"""
    g = 1
    for _ in range(k):
        g = I.G([0], [g])
    return g


# ---- (e) rule-tagged components so two race rules can live in one sum ----
def mirror(text):
    """-G for a pawn position: swap colours and reflect ranks."""
    W, B = I.parse(text)
    f = lambda s: I.FILES[s[0]] + str(I.NR + 1 - s[1])
    return "W: " + " ".join(sorted(map(f, B))) + " / B: " + " ".join(sorted(map(f, W)))


MEMO2 = {}


def opts2(state, side):
    comps, n = state
    out = []
    if side == "L" and n > 0: out.append((comps, n - 1))
    if side == "R" and n < 0: out.append((comps, n + 1))
    colour = "W" if side == "L" else "B"
    for i, c in enumerate(comps):
        rest = comps[:i] + comps[i + 1:]
        rule, enc = c
        W, B, ep = I.dec(enc)
        eff = ep if (ep is not None and ep[2] == colour) else None
        I.CFG["rule"] = rule
        for (W2, B2, e2, dbl) in I.pawn_moves(W, B, eff, colour):
            d, new = I.after_move(W2, B2, e2, colour, dbl)
            out.append((tuple(sorted(rest + tuple((rule, x) for x in new))), n + d))
    return out


def wins2(state, side):
    k = (state, side)
    if k in MEMO2: return MEMO2[k]
    o = "R" if side == "L" else "L"
    r = any(not wins2(s, o) for s in opts2(state, side))
    MEMO2[k] = r
    return r


def rule_diff(text, r1, r2):
    W, B = I.parse(text)
    W2, B2 = I.parse(mirror(text))
    comps = tuple(sorted([(r1, I.enc(*c)) for c in I.split(W, B, None)] +
                         [(r2, I.enc(*c)) for c in I.split(W2, B2, None)]))
    MEMO2.clear()
    lf, rf = wins2((comps, 0), "L"), wins2((comps, 0), "R")
    return {(True, True): "N", (True, False): "L", (False, True): "R", (False, False): "P"}[(lf, rf)]


def main():
    TINY1, PM1, F71 = I.TINY1, I.PM1, I.F71
    for ep in (True, False):
        for rule in ("count", "mover", "opponent"):
            I.CFG.update(ep=ep, rule=rule, split=True, wrap=True); I.reset()
            print(f"--- cylinder ep={'on' if ep else 'off'} rule={rule}")
            cd = "W: c1 c3 d3 / B: c2 d4 d5 d6"
            print("  (a) 7.3{c,d} = tiny(1):", eq_sum(cd, [TINY1]), "| = 1:", eq_sum(cd, [1]))
            # (b) 7.1 total skipped: not part of claim V1 and the BIG-integer sum is too large for plain minimax
            sh = {"2.2 up1": "W: a3 h2 / B: a4 h5", "3.2 up1": "W: a5 h2 / B: a6 h7"}
            for k, t in sh.items():
                cands = {"0": 0, "1": 1, "2": 2, "dbl-up*": I.G([0, I.UP], [0])}
                hit = [nm for nm, X in cands.items() if eq_sum(t, [X])]
                print(f"  (d) {k} {t}: equals {hit}")
            ab = "W: a2 b2 h3 / B: a6 b7 h7"
            x = dyadic(4)
            print("  (f) 7.2abh: G < 1/16:", I.outcome(I.root_state(ab, I.neg(x))) == "R" or
                  I.outcome((tuple(sorted(I.root_state(ab)[0] + (I.neg(x),))), 0)) == "R",
                  "| G > -1/16:", I.outcome((tuple(sorted(I.root_state(ab)[0] + (x,))), 0)) == "L")
        I.CFG.update(ep=ep, rule="count", split=True, wrap=False); I.reset()
        t23 = "W: c1 d2 / B: c4 d3"
        print(f"  (c) flat ep={'on' if ep else 'off'} 2.3 = 0:", eq_sum(t23, [0]))
        print(f"  (d) flat ep={'on' if ep else 'off'} 2.3 up1 W: c2 d3 / B: c5 d4 equals",
              [nm for nm, X in {"0": 0, "1": 1, "2": 2}.items() if eq_sum("W: c2 d3 / B: c5 d4", [X])])
        I.CFG.update(wrap=True)
        ab = "W: a2 b2 h3 / B: a6 b7 h7"
        # (e) cheap distinguisher: if G[r1] + X and G[r2] + X differ in outcome for some X, the values differ.
        S, U = I.STAR, I.UP
        D = I.neg(U)
        tests = {"0": 0, "*": S, "up": U, "down": D, "up*": I.G([0, S], [0]), "down*": I.G([0], [0, S]),
                 "*2": I.G([0, S], [0, S]), "+-1": I.PM1, "1/2": I.G([0], [1]), "-1/2": I.G([-1], [0]),
                 "{0|-256}": I.G([0], [-256]), "{256|0}": I.G([256], [0]), "1": 1, "-1": -1}
        for X_name, X in tests.items():
            row = {}
            for rule in ("count", "mover", "opponent"):
                I.CFG.update(ep=ep, rule=rule, split=True, wrap=True); I.reset()
                row[rule] = I.outcome(I.root_state(ab, X))
            tag = "DIFFER" if len(set(row.values())) > 1 else "same"
            print(f"  (e) 7.2abh ep={'on' if ep else 'off'}: outcome of G+{X_name}: {row} {tag}")


if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000)
    threading.stack_size(512 * 1024 * 1024)
    t = threading.Thread(target=main); t.start(); t.join()
