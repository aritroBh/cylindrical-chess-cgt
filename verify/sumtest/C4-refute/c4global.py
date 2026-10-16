"""Sum tests for C4 under two e.p.-scope conventions (aware passer test).

  component : an e.p. right survives moves made in other summands (CGT-in-isolation model)
  global    : chess-faithful; any move anywhere else ends the right, and the pawn
              component is re-resolved at once (a4 then counts as passed)

For each pawn position P, claimed value V and reference game H, compare
outcome(P + H) (brute force over explicit trees) with outcome(V + H).

Run:
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/sumtest/C4-refute/c4global.py
"""
import os
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.setrecursionlimit(5_000_000)
from c4check import Model, parse  # noqa: E402
from c4brute import G, pm, sw, STAR, STAR2  # noqa: E402


def outc(lw, rw):
    return {(True, True): "N", (True, False): "L", (False, True): "R", (False, False): "P"}[(lw, rw)]


class Solver:
    def __init__(self, model, scope):
        self.m, self.scope = model, scope
        self.memo = {}

    def norm(self, comps, n):
        """comps: tuple of ('p', state) / ('h', tree); ints folded into n"""
        out = []
        for c in comps:
            if c[0] == "h" and isinstance(c[1], int):
                n += c[1]
            elif c[0] == "p" and isinstance(c[1], int):
                n += c[1]
            else:
                out.append(c)
        return (tuple(sorted(out, key=repr)), n)

    def lapse(self, comps, mover, moved_index):
        """global scope: rights held by `mover` in components it did not move in lapse"""
        if self.scope != "global":
            return comps
        out = []
        for i, c in enumerate(comps):
            if i != moved_index and c[0] == "p" and not isinstance(c[1], int):
                W, B, ep = c[1]
                if ep and ep[2] == mover:
                    st = (W, B, None)
                    r = self.m.resolve(st, mover)
                    c = ("p", r if r is not None else st)
            out.append(c)
        return out

    def wins(self, S, left):
        key = (S, left)
        v = self.memo.get(key)
        if v is not None:
            return v
        comps, n = S
        side = "W" if left else "B"
        kids = []
        for i, c in enumerate(comps):
            if c[0] == "p":
                for ch in self.m.moves(*c[1], side):
                    r = self.m.resolve(ch, side)
                    new = list(comps)
                    new[i] = ("p", r if r is not None else ch)
                    kids.append(self.norm(self.lapse(new, side, i), n))
            else:
                for ch in (c[1][1] if left else c[1][2]):
                    new = list(comps)
                    new[i] = ("h", ch)
                    kids.append(self.norm(self.lapse(new, side, i), n))
        if left and n > 0:
            kids.append(self.norm(self.lapse(list(comps), side, -1), n - 1))
        if (not left) and n < 0:
            kids.append(self.norm(self.lapse(list(comps), side, -1), n + 1))
        v = any(not self.wins(k, not left) for k in kids)
        self.memo[key] = v
        return v

    def outcome(self, comps):
        S = self.norm(comps, 0)
        return outc(self.wins(S, True), self.wins(S, False))


def refs():
    up = G([0], [STAR])
    down = G([STAR], [0])
    half = G([0], [1])
    tiny1 = G([0], [G([0], [-1])])
    R = {"0": 0, "*": STAR, "*2": STAR2, "*3": G([0, STAR, STAR2], [0, STAR, STAR2]),
         "up": up, "down": down, "up*": G([0, STAR], [0]), "1/2": half, "-1/2": G([-1], [0]),
         "+-1": pm(1), "+-2": pm(2), "{1|0}": sw(1, 0), "tiny1": tiny1,
         "2+-1": sw(3, 1), "-2+-1": sw(-1, -3), "{2+-1|-2+-1}": G([sw(3, 1)], [sw(-1, -3)])}
    for k in range(-5, 6):
        R[str(k)] = k
    return R


def main():
    X = "W: a2 c2 / B: b4 d7"
    B5 = "W: a2 c2 / B: b5 d7"
    Gr = "W: a2 c2 / B: b7 d7"
    claims = [(X, -3, "X=-3"), (B5, sw(-1, -3), "B5=-2+-1"),
              (Gr, G([sw(3, 1)], [sw(-1, -3)]), "G={2+-1|-2+-1}")]
    R = refs()
    for race in ("count", "mover"):
        m = Model(4, 8, False, ep=True, aware=True, race=race)
        for scope in ("component", "global"):
            s = Solver(m, scope)
            for pos, V, label in claims:
                W, B = parse(pos)
                bad = []
                vec_p, vec_v = "", ""
                for name, H in R.items():
                    op = s.outcome((("p", (W, B, None)), ("h", H)))
                    ov = s.outcome((("h", V), ("h", H)))
                    vec_p += op
                    vec_v += ov
                    if op != ov:
                        bad.append((name, op, ov))
                print(f"race={race:6s} scope={scope:9s} {label:16s} P+H {vec_p}  V+H {vec_v}  "
                      f"{'ALL AGREE' if not bad else 'DIFFER: ' + str(bad)}")
    print("reference order:", " ".join(R))


if __name__ == "__main__":
    threading.stack_size(1 << 30)
    t = threading.Thread(target=main)
    t.start()
    t.join()
