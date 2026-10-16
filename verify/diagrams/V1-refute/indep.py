"""Independent re-check of claim V1 (diagram rerun values).

Written from the stated conventions only. It imports NOTHING from cylcgt/,
crosscheck/ or verify/diagrams/*.py.  Method: the difference-game test.
    G = X   <=>   G + (-X) is a second-player win (outcome P)
decided by plain memoised minimax over sums.  No canonical-form engine is used,
so the check does not depend on any simplification code.

Pawn model (re-implemented):
  * White = Left, Black = Right, normal play.
  * single steps, double step from rank 2 (W) / rank 7 (B), diagonal captures,
    files wrap on the cylinder.  No promotion move exists: a pawn that is
    "passed" ends the game first.
  * passed: no enemy pawn on the same or an adjacent file strictly ahead.
  * exactly one side passed -> number +BIG / -BIG (BIG = 256).
  * a move that leaves both sides passed -> race, resolved by RULE:
      count    : opponent of the mover moves first; fewer moves to promote wins,
                 opponent wins ties (double step from the 2nd rank counted);
      mover    : the mover wins;   opponent: the mover loses.
  * en passant: after a double step the opponent may capture e.p. as its next
    move IN THIS COMPONENT; the right is lost if the double-stepper moves again
    in the component.  (Standard short-game approximation.)
  * SPLIT=True : after every move, the child is split into independent
    components at empty files and each component ends at its OWN passed pawn
    (the decomposition the audit's numbers are based on).
    SPLIT=False: the whole sub-game is one game that ends at the first passed
    pawn anywhere in it (stricter reading of "a passed pawn ends the game").

Run:  cd /Users/aritro/Downloads/Research/Chessendgames && \
      .venv/bin/python -I verify/diagrams/V1-refute/indep.py
"""
import sys
import threading

NF, NR, BIG = 8, 8, 256
FILES = "abcdefgh"
CFG = {"wrap": True, "ep": True, "rule": "count", "split": True}
STATS = {"race": 0, "ep_false_pass": 0}


def sq(s):
    return (FILES.index(s[0]), int(s[1:]))


def parse(text):
    w, b = text.split("/")
    W = frozenset(sq(t) for t in w.split(":")[1].split())
    B = frozenset(sq(t) for t in b.split(":")[1].split())
    return W, B


def adj(f):
    if CFG["wrap"]:
        return ((f - 1) % NF, (f + 1) % NF)
    return tuple(g for g in (f - 1, f + 1) if 0 <= g < NF)


def is_passed(W, B, side):
    mine, theirs = (W, B) if side == "W" else (B, W)
    for (f, r) in mine:
        fs = (f,) + adj(f)
        if side == "W":
            stop = any(g in fs and s > r for (g, s) in theirs)
        else:
            stop = any(g in fs and s < r for (g, s) in theirs)
        if not stop:
            return True
    return False


def dist(W, B, side):
    """moves needed by `side` to promote its best passed front pawn."""
    occ = W | B
    best = 10 ** 9
    mine, theirs = (W, B) if side == "W" else (B, W)
    for (f, r) in mine:
        one = (frozenset([(f, r)]), theirs) if side == "W" else (theirs, frozenset([(f, r)]))
        if not is_passed(one[0], one[1], side):
            continue
        if side == "W":
            if any((f, s) in occ for s in range(r + 1, NR + 1)):
                continue
            d = NR - r - (1 if r == 2 else 0)
        else:
            if any((f, s) in occ for s in range(1, r)):
                continue
            d = r - 1 - (1 if r == NR - 1 else 0)
        best = min(best, d)
    return best


def pawn_moves(W, B, ep, side):
    """yield (W', B', ep', was_double) for every move of `side`."""
    occ = W | B
    res = []
    if side == "W":
        for (f, r) in W:
            rest = W - {(f, r)}
            if r + 1 > NR:
                continue
            if (f, r + 1) not in occ:
                res.append((rest | {(f, r + 1)}, B, None, False))
                if r == 2 and (f, 4) not in occ:
                    e = ((f, 3), (f, 4), "B") if CFG["ep"] else None
                    res.append((rest | {(f, 4)}, B, e, True))
            for g in adj(f):
                t = (g, r + 1)
                if t in B:
                    res.append((rest | {t}, B - {t}, None, False))
                elif ep is not None and ep[2] == "W" and ep[0] == t:
                    res.append((rest | {t}, B - {ep[1]}, None, False))
    else:
        for (f, r) in B:
            rest = B - {(f, r)}
            if r - 1 < 1:
                continue
            if (f, r - 1) not in occ:
                res.append((W, rest | {(f, r - 1)}, None, False))
                if r == NR - 1 and (f, NR - 3) not in occ:
                    e = ((f, NR - 2), (f, NR - 3), "W") if CFG["ep"] else None
                    res.append((W, rest | {(f, NR - 3)}, e, True))
            for g in adj(f):
                t = (g, r - 1)
                if t in W:
                    res.append((W - {t}, rest | {t}, None, False))
                elif ep is not None and ep[2] == "B" and ep[0] == t:
                    res.append((W - {ep[1]}, rest | {t}, None, False))
    # de-duplicate identical results
    seen, out = set(), []
    for m in res:
        k = (m[0], m[1], m[2])
        if k not in seen:
            seen.add(k)
            out.append(m)
    return out


def split(W, B, ep):
    occ = sorted({f for f, _ in W | B})
    if not occ:
        return []
    if not CFG["split"]:
        return [(W, B, ep)]
    groups = []
    for f in occ:
        if groups and f == groups[-1][-1] + 1:
            groups[-1].append(f)
        else:
            groups.append([f])
    if CFG["wrap"] and len(groups) > 1 and groups[0][0] == 0 and groups[-1][-1] == NF - 1:
        groups[0] = groups.pop() + groups[0]
    out = []
    for g in groups:
        fs = set(g)
        e = ep if (ep is not None and ep[0][0] in fs) else None
        out.append((frozenset(p for p in W if p[0] in fs), frozenset(p for p in B if p[0] in fs), e))
    return out


def enc(W, B, ep):
    return (0, tuple(sorted(W)), tuple(sorted(B)), ep if ep is not None else ())


def dec(c):
    return frozenset(c[1]), frozenset(c[2]), (c[3] if c[3] != () else None)


def after_move(W, B, ep, mover, was_double):
    """child of a pawn move: returns (int_delta, [components])."""
    wp, bp = is_passed(W, B, "W"), is_passed(W, B, "B")
    if wp and bp:
        STATS["race"] += 1
        rule = CFG["rule"]
        other = "B" if mover == "W" else "W"
        if rule == "mover":
            win = mover
        elif rule == "opponent":
            win = other
        else:
            win = other if dist(W, B, other) <= dist(W, B, mover) else mover
        return (BIG if win == "W" else -BIG), []
    if wp or bp:
        if was_double and ep is not None:
            # does the opponent have an e.p. capture of the pawn that just moved?
            (tf, tr), (cf, cr), cap = ep
            pieces = B if cap == "B" else W
            if any((g, cr) in pieces for g in adj(cf)):
                STATS["ep_false_pass"] += 1
        return (BIG if wp else -BIG), []
    return 0, [enc(*c) for c in split(W, B, ep)]


# ---------------- explicit games for the claimed values ----------------
NODES = []  # id -> (L options, R options); options are ints or (1, id)


def G(L, R):
    NODES.append((tuple(L), tuple(R)))
    return (1, len(NODES) - 1)


def neg(x):
    if isinstance(x, int):
        return -x
    L, R = NODES[x[1]]
    return G([neg(o) for o in R], [neg(o) for o in L])


# ---------------- minimax over sums ----------------
MEMO = {}


def options(state, side):
    comps, n = state
    out = []
    if side == "L" and n > 0:
        out.append((comps, n - 1))
    if side == "R" and n < 0:
        out.append((comps, n + 1))
    colour = "W" if side == "L" else "B"
    for i, c in enumerate(comps):
        rest = comps[:i] + comps[i + 1:]
        if c[0] == 0:
            W, B, ep = dec(c)
            eff = ep if (ep is not None and ep[2] == colour) else None
            for (W2, B2, e2, dbl) in pawn_moves(W, B, eff, colour):
                d, new = after_move(W2, B2, e2, colour, dbl)
                out.append((tuple(sorted(rest + tuple(new))), n + d))
        else:
            L, R = NODES[c[1]]
            for o in (L if side == "L" else R):
                if isinstance(o, int):
                    out.append((rest, n + o))
                else:
                    out.append((tuple(sorted(rest + (o,))), n))
    return out


def wins(state, side):
    key = (state, side)
    if key in MEMO:
        return MEMO[key]
    other = "R" if side == "L" else "L"
    r = any(not wins(s, other) for s in options(state, side))
    MEMO[key] = r
    return r


def root_state(text, extra=None):
    W, B = parse(text)
    wp, bp = is_passed(W, B, "W"), is_passed(W, B, "B")
    assert not (wp and bp), "race at root"
    n = 0
    comps = ()
    if wp or bp:
        n = BIG if wp else -BIG
    else:
        comps = tuple(sorted(enc(*c) for c in split(W, B, None)))
    if extra is not None:
        if isinstance(extra, int):
            n += extra
        else:
            comps = tuple(sorted(comps + (extra,)))
    return (comps, n)


def outcome(state):
    lf, rf = wins(state, "L"), wins(state, "R")
    return {(True, True): "N", (True, False): "L", (False, True): "R", (False, False): "P"}[(lf, rf)]


def equals(text, X):
    return outcome(root_state(text, neg(X))) == "P"


def reset():
    MEMO.clear()
    STATS["race"] = 0
    STATS["ep_false_pass"] = 0


# ---------------- the claims ----------------
STAR = G([0], [0])
UP = G([0], [STAR])
TINY1 = G([0], [G([0], [-1])])
PM1 = G([1], [-1])
F71 = G([G([2], [1])], [0])
AH = {k: G([k], [STAR]) for k in (256, 257, 258, 259)}

POS = {
    "2.1": "W: e4 / B: e5",
    "2.2": "W: a2 h1 / B: a3 h4",
    "3.1": "W: a3 h1 / B: a4 h5",
    "3.2": "W: a4 h1 / B: a5 h6",
    "4.1": "W: e4 / B: e6",
    "4.2": "W: e3 / B: e6",
    "4.3": "W: a4 h2 h4 / B: a5 a6 a7 h3",
    "7.1c": "W: c2 c3 / B: c5 c6",
    "7.1f": "W: f3 f4 / B: f7",
    "7.1ah": "W: a4 a5 h2 h3 / B: a7 h6",
    "7.2abh": "W: a2 b2 h3 / B: a6 b7 h7",
    "7.3": "W: a1 a5 c1 c3 d3 f7 g1 h1 / B: c2 d4 d5 d6 g3 g7 h4",
}

# (label, claimed X or None for outcome-only, claimed outcome, alternatives that must FAIL)
def claims(ep):
    return [
        ("2.1", 0, None, [1, STAR]),
        ("2.2", 0, None, [1, STAR]),
        ("3.1", 1 if ep else 2, None, [2 if ep else 1]),
        ("3.2", 2, None, [1, 3]),
        ("4.1", STAR, None, [0, UP]),
        ("4.2", 0, None, [UP, STAR]),
        ("4.3", TINY1, None, [1, 0]),
        ("7.1c", PM1, None, [0, STAR]),
        ("7.1f", F71, None, [G([2], [0]), 1]),
        ("7.1ah", "AH", None, [1]),
        ("7.2abh", None, "N" if ep else "R", []),
        ("7.3", BIG, None, [BIG + 1, BIG - 1]),
    ]


def main():
    lines = []
    for split_mode in (True, False):
        for ep in (True, False):
            for rule in ("count", "mover", "opponent"):
                CFG.update(ep=ep, rule=rule, split=split_mode)
                reset()
                row = []
                for label, X, oc, alts in claims(ep):
                    text = POS[label]
                    st = root_state(text)
                    o = outcome(st)
                    if X == "AH":
                        exact = [k for k, g in AH.items() if equals(text, g)]
                        ok = bool(exact)
                        alt_fail = all(not equals(text, a) for a in alts)
                        row.append(f"{label}: outcome {o}; equals {{k|*}} for k in {exact} "
                                   f"{'OK' if ok else 'FAIL'}; alts rejected={alt_fail}")
                    elif X is None:
                        row.append(f"{label}: outcome {o} (claimed {oc}) {'OK' if o == oc else 'FAIL'}")
                    else:
                        ok = equals(text, X)
                        alt_fail = all(not equals(text, a) for a in alts)
                        row.append(f"{label}: outcome {o}; G-X is P: {'OK' if ok else 'FAIL'}; "
                                   f"alts rejected={alt_fail}")
                hdr = (f"--- split={'per-component' if split_mode else 'whole-game'} "
                       f"ep={'on' if ep else 'off'} rule={rule}  (race events {STATS['race']}, "
                       f"double-step 'passed' pawns capturable e.p. {STATS['ep_false_pass']}, "
                       f"memo {len(MEMO)})")
                print(hdr)
                for r in row:
                    print("   ", r)
                sys.stdout.flush()
    CFG.update(ep=True, rule="count", split=True)
    W, B = parse(POS["7.3"])
    print("7.3 passed W:", is_passed(W, B, "W"), " passed B:", is_passed(W, B, "B"),
          " passed white pawns:", sorted(FILES[f] + str(r) for (f, r) in W
                                          if is_passed(frozenset([(f, r)]), B, "W")))


if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000)
    threading.stack_size(512 * 1024 * 1024)
    t = threading.Thread(target=main)
    t.start()
    t.join()
