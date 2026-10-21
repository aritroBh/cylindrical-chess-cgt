"""Theory-lens checks for claim L4.2, part 2 (verifier scratch; worker files untouched).

A. The 8x8 embedding's convention model is WF (frozen kings: every non-terminal node
   gets an extra Left option -BIG and Right option +BIG), not W. The worker's
   sensitivity analysis (test_L4_races.W_override) is done in W only. Here the same
   single-flip analysis is repeated in WF, at the count baseline.
B. Outcomes of the flipped values (does a single flip change the outcome, not just the value?).
C. The note's extra statement: "four critical lost by the mover, rest by count -> 0";
   and "four won by the mover, every other race lost by the mover -> *2", in W and WF.
D. e.p. twins: race nodes (child, mover) that differ only in the e.p. field; is the
   right usable (does it change the capturing side's move list)? If not, the twins are
   one and the same chess position.
E. Reproducible (sorted-order) random trials, 200, seed 1, W and WF.

Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/lemmas/L4.2-critical-races-theory/wf_sensitivity.py
"""
import random
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from lemmas.common import PBIG, NBIG, race_winner, terminal, split_ep, W as W_common, WF as WF_common
from lemmas.test_L4_races import race_nodes, W_override

other = lambda m: "B" if m == "W" else "W"


def WF_override(board, pos, rule, override, memo):
    g = memo.get(pos)
    if g is not None:
        return g
    t = terminal(board, pos)
    if t == 1:
        g = PBIG
    elif t == -1:
        g = NBIG
    else:
        lpos, rpos = split_ep(pos)
        L = [_ch(board, c, "W", rule, override, memo) for c in pawns.moves(board, lpos, "W")]
        R = [_ch(board, c, "B", rule, override, memo) for c in pawns.moves(board, rpos, "B")]
        L.append(NBIG)
        R.append(PBIG)
        g = cgt.make(L, R)
    memo[pos] = g
    return g


def _ch(board, c, mover, rule, override, memo):
    if terminal(board, c) == 0:
        w = override.get((c, mover)) or race_winner(board, c, mover, rule)
        return PBIG if w == "W" else NBIG
    return WF_override(board, c, rule, override, memo)


def key(t):
    c, m = t
    return (str(c), str(c.ep), m)


def main(ep):
    b = Board(4, 8, False, ep)
    x = Pos.parse("W: a2 c2 / B: b7 d7")
    races = sorted(race_nodes(b, x), key=key)
    print(f"=== e.p. {'on' if ep else 'off'}: {len(races)} race nodes (child, mover)")
    models = {"W": W_override, "WF": WF_override}
    # sanity: overrides-free values equal lemmas.common W / WF
    assert W_override(b, x, "count", {}, {}) is W_common(b, x, "count")
    assert WF_override(b, x, "count", {}, {}) is WF_common(b, x, "count")
    crits = {}
    for name, F in models.items():
        for base in ("count", "mover", "opponent"):
            v0 = F(b, x, base, {}, {})
            crit = []
            for c, m in races:
                w = race_winner(b, c, m, base)
                v = F(b, x, base, {(c, m): other(w)}, {})
                if v is not v0:
                    crit.append(((c, m), w, cgt.show(v), cgt.outcome(v)))
            print(f"  [{name}] baseline {base}: root {cgt.show(v0)} (outcome {cgt.outcome(v0)}); "
                  f"single flips changing it: {len(crit)}")
            for (c, m), w, s, o in crit:
                print(f"       {str(c):22s} ep={c.ep} mover {m} verdict {w} -> {s} (outcome {o})")
            if base == "count":
                crits[name] = [k for k, _, _, _ in crit]
    print("  critical set W == critical set WF:", set(crits["W"]) == set(crits["WF"]))
    crit = crits["W"]
    rest = [k for k in races if k not in crit]
    for name, F in models.items():
        ov1 = {k: other(k[1]) for k in crit}  # 4 lost by mover, rest count
        ov2 = {k: k[1] for k in crit}
        ov2.update({k: other(k[1]) for k in rest})  # 4 won by mover, all others lost by mover
        ov3 = {k: k[1] for k in races}  # everything won by the mover (= mover rule)
        ov4 = {k: other(k[1]) for k in races}  # = opponent rule
        print(f"  [{name}] 4 lost by mover, rest count: {cgt.show(F(b, x, 'count', ov1, {}))}; "
              f"4 won, rest lost by mover: {cgt.show(F(b, x, 'count', ov2, {}))}; "
              f"all won by mover: {cgt.show(F(b, x, 'count', ov3, {}))}; "
              f"all lost by mover: {cgt.show(F(b, x, 'count', ov4, {}))}")
        rng = random.Random(1)
        hist = {}
        for _ in range(200):
            ov = {k: k[1] for k in crit}
            for k in rest:
                ov[k] = rng.choice("WB")
            s = cgt.show(F(b, x, "count", ov, {}))
            hist[s] = hist.get(s, 0) + 1
        print(f"  [{name}] 4 won by mover, rest uniform random (200, seed 1, sorted order): "
              f"{dict(sorted(hist.items()))}")
    # D. e.p. twins
    by_cfg = {}
    for c, m in races:
        by_cfg.setdefault((c.white, c.black, m), []).append(c)
    twins = {k: v for k, v in by_cfg.items() if len(v) > 1}
    usable = 0
    for k, cs in twins.items():
        for c in cs:
            if c.ep:
                s = c.ep[2]
                plain = Pos(c.white, c.black, None)
                if set(pawns.moves(b, c, s)) != set(pawns.moves(b, plain, s)):
                    usable += 1
    n_ep = sum(1 for c, m in races if c.ep)
    print(f"  distinct (white, black, mover) configurations: {len(by_cfg)}; groups with e.p. twins: "
          f"{len(twins)}; race nodes carrying an e.p. field: {n_ep}; of those in twin groups with a usable right: {usable}")
    usable_all = 0
    for c, m in races:
        if c.ep:
            s = c.ep[2]
            plain = Pos(c.white, c.black, None)
            if set(pawns.moves(b, c, s)) != set(pawns.moves(b, plain, s)):
                usable_all += 1
    print(f"  race nodes whose e.p. right is usable by the side to move: {usable_all}")
    print(f"  any critical race carries an e.p. field: {any(k[0].ep for k in crit)}")


if __name__ == "__main__":
    for ep in (True, False):
        main(ep)
