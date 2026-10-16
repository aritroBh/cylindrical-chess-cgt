"""V1 adversarial verifier (THEORY lens) scratch checks.  cylcgt is NOT edited; a few
module globals are monkeypatched at runtime and restored.

A. Exact canonical forms: "+W" in cgt.show is a display bucket for ANY number >= BIG/2.
   Print numbers relative to BIG ("B+k") so distinct canonical forms are not merged.
B. BIG invariance: recompute with BIG = 1024 and compare the B-relative forms.
C. Race-rule bounds: canonical values are monotone in leaf values, so
   value(all races -> -BIG) <= value(any race assignment) <= value(all races -> +BIG).
   'mover' and 'opponent' are NOT these bounds.  Compute both bounds.
D. Mean / temperature / outcome of 7.2{a,b,h} under every rule.
E. En passant semantics in sums.  cylcgt keeps an e.p. right alive in a component until
   someone moves in THAT component (docstring: "exact when the component is played alone").
   In chess the right lapses after any other move.  Compare outcome(G + X) under both
   semantics for a battery of abstract summands X.

Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
     PYTHONPATH=. .venv/bin/python verify/diagrams/V1-theory/theory_checks.py
"""
import sys
from dataclasses import replace
from fractions import Fraction

from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos

sys.setrecursionlimit(1_000_000)

CYL = Board(8, 8, True, True)
CYL0 = replace(CYL, ep=False)
FLAT = Board(8, 8, False, True)
FLAT0 = replace(FLAT, ep=False)

POS = [
    ("2.1", "W: e4 / B: e5", "cyl"),
    ("2.2", "W: a2 h1 / B: a3 h4", "cyl"),
    ("2.3", "W: c1 d2 / B: c4 d3", "flat"),
    ("3.1", "W: a3 h1 / B: a4 h5", "cyl"),
    ("3.2", "W: a4 h1 / B: a5 h6", "cyl"),
    ("4.1", "W: e4 / B: e6", "cyl"),
    ("4.2", "W: e3 / B: e6", "cyl"),
    ("4.3", "W: a4 h2 h4 / B: a5 a6 a7 h3", "cyl"),
    ("7.1c", "W: c2 c3 / B: c5 c6", "cyl"),
    ("7.1f", "W: f3 f4 / B: f7", "cyl"),
    ("7.1ah", "W: a4 a5 h2 h3 / B: a7 h6", "cyl"),
    ("7.2abh", "W: a2 b2 h3 / B: a6 b7 h7", "cyl"),
    ("7.3", "W: a1 a5 c1 c3 d3 f7 g1 h1 / B: c2 d4 d5 d6 g3 g7 h4", "cyl"),
    ("7.3cd", "W: c1 c3 d3 / B: c2 d4 d5 d6", "cyl"),
]

ORIG_FMT = cgt._fmt_num
ORIG_PD = pawns.promote_distance
ORIG_BIG = pawns.BIG


def rel_fmt(x: Fraction) -> str:
    B = pawns.BIG
    if abs(x) >= B // 2:
        k = x - B if x > 0 else x + B
        ks = "" if k == 0 else (f"+{k}" if k > 0 else f"{k}")
        return f"B{ks}" if x > 0 else f"-B{ks}"
    return ORIG_FMT(x)


def rshow(g):
    cgt._fmt_num = rel_fmt
    try:
        return cgt.show(g)
    finally:
        cgt._fmt_num = ORIG_FMT


def set_rule(rule):
    """rule in count/mover/opponent/allW/allB."""
    pawns.promote_distance = ORIG_PD
    if rule in ("count", "mover", "opponent"):
        pawns.RACE_RULE = rule
    else:
        pawns.RACE_RULE = "count"
        winner = "W" if rule == "allW" else "B"
        # count branch: winner = other if d(other) <= d(mover) else mover
        pawns.promote_distance = lambda board, pos, side: 0 if side == winner else 1
    pawns._value.cache_clear()
    pawns.race_hits.clear()


def boards(kind):
    return (CYL, CYL0) if kind == "cyl" else (FLAT, FLAT0)


def val(board, text, rule):
    set_rule(rule)
    g = pawns.value(board, Pos.parse(text))
    n = len(pawns.race_hits)
    return g, n


RULES = ("count", "mover", "opponent", "allW", "allB")


def part_ABC():
    print("=== A/C. exact forms (numbers >= BIG/2 shown as B+k), BIG=256, all race rules incl. bounds ===")
    for label, text, kind in POS:
        for b in boards(kind):
            res = {}
            for r in RULES:
                g, n = val(b, text, r)
                res[r] = (g, n)
            forms = {r: rshow(res[r][0]) for r in RULES}
            distinct = len(set(forms.values()))
            bounds_equal = res["allW"][0] is res["allB"][0]
            print(f"{label:7s} {'cyl ' if b.wrap else 'flat'} ep={'on ' if b.ep else 'off'} "
                  f"race nodes {res['count'][1]:4d}  count={forms['count']}")
            g = res["count"][0]
            print(f"        outcome {cgt.outcome(g)} mean {cgt.mean(g)} temp {cgt.temperature(g)}  "
                  f"bounds(allW==allB): {bounds_equal}  distinct forms over 5 rules: {distinct}")
            if distinct > 1:
                for r in RULES:
                    gg = res[r][0]
                    print(f"          {r:8s} outcome {cgt.outcome(gg)} mean {cgt.mean(gg)} "
                          f"temp {cgt.temperature(gg)}  {forms[r] if len(forms[r]) < 400 else forms[r][:400] + '...'}")
    set_rule("count")


def part_B():
    print("\n=== B. BIG invariance: BIG=256 vs BIG=1024 (B-relative forms, count rule) ===")
    out = {}
    for big in (256, 1024):
        pawns.BIG = big
        for label, text, kind in POS:
            for b in boards(kind):
                g, _ = val(b, text, "count")
                out[(big, label, b.ep)] = (rshow(g), cgt.outcome(g))
    pawns.BIG = ORIG_BIG
    set_rule("count")
    for label, text, kind in POS:
        for ep in (True, False):
            a, c = out[(256, label, ep)], out[(1024, label, ep)]
            print(f"{label:7s} ep={'on ' if ep else 'off'} same form: {a[0] == c[0]}  outcome {a[1]} / {c[1]}"
                  + ("" if a[0] == c[0] else f"\n     256: {a[0][:300]}\n    1024: {c[0][:300]}"))


# ---------------- E. e.p. semantics in sums ----------------
def classify(board, q, mover):
    wp, bp = pawns.passed(board, q, "W"), pawns.passed(board, q, "B")
    if wp and bp:
        other = "B" if mover == "W" else "W"
        return other if ORIG_PD(board, q, other) <= ORIG_PD(board, q, mover) else mover
    if wp:
        return "W"
    if bp:
        return "B"
    return None


def make_solver(board, sem):
    memo = {}

    def plain(p):
        return Pos(p.white, p.black, None) if p.ep else p

    def wins(p, X, side):
        key = (p, X.id, side)
        r = memo.get(key)
        if r is not None:
            return r
        other = "B" if side == "W" else "W"
        mp = p if (p.ep and p.ep[2] == side) else plain(p)
        res = False
        for q in pawns.moves(board, mp, side):
            c = classify(board, q, side)
            if c == side:
                res = True
                break
            if c == other:
                continue
            if not wins(q, X, other):
                res = True
                break
        if not res:
            q = p if sem == "model" else plain(p)
            for xo in (X.L if side == "W" else X.R):
                if not wins(q, xo, other):
                    res = True
                    break
        memo[key] = res
        return res

    def outcome(p, X):
        lw = wins(p, X, "W")
        rw = wins(p, X, "B")
        return {(True, True): "N", (True, False): "L", (False, True): "R", (False, False): "P"}[(lw, rw)]

    return outcome


def test_games():
    g = {}
    for n in range(-3, 4):
        g[str(n)] = cgt.integer(n)
    for x in (Fraction(1, 2), Fraction(-1, 2), Fraction(1, 4), Fraction(-1, 4), Fraction(3, 2), Fraction(-3, 2)):
        g[str(x)] = cgt.number(x)
    S, U = cgt.STAR, cgt.UP
    g["*"] = S
    g["*2"] = cgt.nimber(2)
    g["up"] = U
    g["down"] = cgt.DOWN
    g["up*"] = cgt.add(U, S)
    g["down*"] = cgt.neg(cgt.add(U, S))
    g["dup"] = cgt.add(U, U)
    g["ddown"] = cgt.neg(cgt.add(U, U))
    one, m1 = cgt.integer(1), cgt.integer(-1)
    g["+-1"] = cgt.make([one], [m1])
    g["{1|0}"] = cgt.make([one], [cgt.ZERO])
    g["{0|-1}"] = cgt.make([cgt.ZERO], [m1])
    tiny1 = cgt.make([cgt.ZERO], [cgt.make([cgt.ZERO], [m1])])
    g["tiny1"] = tiny1
    g["miny1"] = cgt.neg(tiny1)
    return g


def part_E():
    print("\n=== E. e.p. semantics: outcome(G + X), model (persistent e.p.) vs chess (lapsing e.p.), count rule ===")
    set_rule("count")
    T = test_games()
    for label, text, kind in POS:
        if label == "7.3":
            continue
        b = CYL if kind == "cyl" else FLAT
        p = Pos.parse(text)
        G = pawns.value(b, p)
        battery = dict(T)
        mG = cgt.neg(G)
        battery["-G"] = mG
        for nm in ("*", "up", "down", "1/4", "-1/4", "1", "-1", "tiny1", "miny1"):
            battery[f"-G+{nm}"] = cgt.add(mG, T[nm])
        model = make_solver(b, "model")
        chess = make_solver(b, "chess")
        n_agree_cgt = n_diff = 0
        diffs = []
        for nm, X in battery.items():
            o_cgt = cgt.outcome(cgt.add(G, X))
            o_mod = model(p, X)
            o_ch = chess(p, X)
            n_agree_cgt += (o_cgt == o_mod)
            if o_mod != o_ch:
                n_diff += 1
                diffs.append(f"{nm}: model {o_mod} chess {o_ch}")
        print(f"{label:7s} {len(battery)} summands; engine(model) == cylcgt outcome on {n_agree_cgt}/{len(battery)}; "
              f"model vs chess-lapsing differ on {n_diff}" + ("" if not diffs else ": " + "; ".join(diffs)))


if __name__ == "__main__":
    part_ABC()
    part_B()
    part_E()
