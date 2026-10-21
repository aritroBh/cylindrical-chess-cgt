"""Independent re-check of claim C7 (adversarial / refute lens).

Written from scratch: imports nothing from cylcgt/ or atlas/.

The whole 8x8 board is modelled directly (no reduction to a 4-file strip):
  * component pawns: the 4-file *2 candidate W a2 c2 / B b7 d7, placed on files
    a-d (offset 0) or b-e (offset 1), optionally mirrored;
  * trebuchet: W pawn g<r>, B pawn g<r+1>; kings WK (g+s, r+1), BK (g-s, r),
    s = +1/-1, r = 2..6  (the only legal mutual-zugzwang king placements:
    a king on the pawns' own attack square would be in check);
  * component pawns move on the full board; kings and trebuchet pawns are
    obstacles; files wrap on the cylinder.

Part 1 (the decisive quantity): conservative freeze test, same definition as
the claim: at every node reachable in the component's game tree (any order of
moves, nodes with a passed pawn included but not expanded) no component pawn
may stand on a square the enemy king attacks, and none may attack the enemy
king's square.  Extra checks the worker did not make: a component pawn
attacking an enemy trebuchet pawn, a component pawn wanting to move onto a king
square, and a variant that keeps expanding past passed-pawn nodes.

Part 2 (is the conservative failure decisive?): outcome of G' + *2 with each
player moving first, where G' is the component on the real board and a pawn
move that gives check is scored as a win for the checker (the checked king
must leave the trebuchet and drop its g-pawn).  King captures are not
modelled (in the CGT model they hand the opponent a passed g-pawn, so they are
dominated unless they start a race).  G' = *2 iff G' + *2 is a second-player
win.  Run also with checks ignored (pure model G) as a control.

Run:
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python verify/cylatlas/C7-refute/freeze_indep.py
"""
from __future__ import annotations

import json
import sys
from collections import deque
from functools import lru_cache

N, H = 8, 8
FL = "abcdefgh"
X = 6  # trebuchet file g


def nm(s):
    return f"{FL[s[0]]}{s[1]}"


class Geo:
    def __init__(self, wrap, s, r, ep=True):
        self.wrap, self.s, self.r, self.ep = wrap, s, r, ep
        self.wk = ((X + s) % N, r + 1)
        self.bk = ((X - s) % N, r)
        self.tw = (X, r)       # white trebuchet pawn
        self.tb = (X, r + 1)   # black trebuchet pawn
        self.kings = {self.wk, self.bk}

    def f(self, f, df):
        g = f + df
        if self.wrap:
            return g % N
        return g if 0 <= g < N else None

    def katt(self, k):
        out = set()
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == dr == 0:
                    continue
                g = self.f(k[0], df)
                q = k[1] + dr
                if g is not None and 1 <= q <= H:
                    out.add((g, q))
        return out

    def patt(self, p, white):
        q = p[1] + (1 if white else -1)
        out = set()
        for df in (-1, 1):
            g = self.f(p[0], df)
            if g is not None and 1 <= q <= H:
                out.add((g, q))
        return out


def place(o, mirror):
    base_w = [(0, 2), (2, 2)]
    base_b = [(1, 7), (3, 7)]
    mp = (lambda c: o + 3 - c) if mirror else (lambda c: o + c)
    return (frozenset((mp(f), r) for f, r in base_w),
            frozenset((mp(f), r) for f, r in base_b))


def passed(geo, W, B, white):
    """Elkies passed pawn: no enemy pawn ahead on own or adjacent file.
    Enemy pawns include the trebuchet pawn (it never matters for a..e)."""
    mine = W if white else B
    theirs = (B | {geo.tb}) if white else (W | {geo.tw})
    for f, r in mine:
        fs = {f, geo.f(f, -1), geo.f(f, 1)} - {None}
        if white:
            if not any(g in fs and q > r for g, q in theirs):
                return True
        else:
            if not any(g in fs and q < r for g, q in theirs):
                return True
    return False


def gen(geo, W, B, ep, white, notes=None):
    """Component pawn moves for one side.  ep = (target, victim, side_allowed)."""
    mine, theirs = (W, B) if white else (B, W)
    occ = W | B | geo.kings | {geo.tw, geo.tb}
    d = 1 if white else -1
    start = 2 if white else H - 1
    side = "W" if white else "B"
    out = []
    for p in mine:
        f, r = p
        rest = mine - {p}
        r1 = r + d
        if not 1 <= r1 <= H:
            continue
        one = (f, r1)
        if one in geo.kings and notes is not None:
            notes.add("pawn blocked by a king")
        if one not in occ:
            out.append((rest | {one}, theirs, None))
            two = (f, r + 2 * d)
            if r == start and two not in occ:
                e = (one, two, "B" if white else "W") if geo.ep else None
                out.append((rest | {two}, theirs, e))
        for df in (-1, 1):
            g = geo.f(f, df)
            if g is None:
                continue
            t = (g, r1)
            if t in theirs:
                out.append((rest | {t}, theirs - {t}, None))
            elif ep and ep[2] == side and ep[0] == t:
                out.append((rest | {t}, theirs - {ep[1]}, None))
            if notes is not None and t == (geo.tb if white else geo.tw):
                notes.add("component pawn attacks enemy trebuchet pawn")
    res = []
    for m, t, e in out:
        res.append((frozenset(m), frozenset(t), e) if white else (frozenset(t), frozenset(m), e))
    return list(dict.fromkeys(res))


def interactions(geo, W, B):
    """Return list of (kind, text) freeze violations at one node."""
    out = []
    wka, bka = geo.katt(geo.wk), geo.katt(geo.bk)
    for p in B:
        if p in wka:
            prot = any(p in geo.patt(q, False) for q in B | {geo.tb})
            out.append(("capture" + ("(protected)" if prot else ""), f"black pawn {nm(p)} next to WK {nm(geo.wk)}"))
        if geo.wk in geo.patt(p, False):
            out.append(("check", f"black pawn {nm(p)} checks WK {nm(geo.wk)}"))
    for p in W:
        if p in bka:
            prot = any(p in geo.patt(q, True) for q in W | {geo.tw})
            out.append(("capture" + ("(protected)" if prot else ""), f"white pawn {nm(p)} next to BK {nm(geo.bk)}"))
        if geo.bk in geo.patt(p, True):
            out.append(("check", f"white pawn {nm(p)} checks BK {nm(geo.bk)}"))
    return out


def reach(geo, W0, B0, expand_terminal=False):
    start = (W0, B0, None)
    dist = {start: 0}
    dq = deque([start])
    notes = set()
    while dq:
        node = dq.popleft()
        W, B, ep = node
        if not expand_terminal and (passed(geo, W, B, True) or passed(geo, W, B, False)):
            continue
        for white in (True, False):
            for ch in gen(geo, W, B, ep, white, notes):
                if ch not in dist:
                    dist[ch] = dist[node] + 1
                    dq.append(ch)
    return dist, notes


def part1():
    rows = []
    for wrap in (False, True):
        for o in (0, 1):
            for mirror in (False, True):
                for s in (1, -1):
                    for r in range(2, 7):
                        geo = Geo(wrap, s, r)
                        W0, B0 = place(o, mirror)
                        res = {}
                        for expand in (False, True):
                            dist, notes = reach(geo, W0, B0, expand)
                            configs = {(W, B) for (W, B, _e) in dist}
                            viol = []
                            for node, d in dist.items():
                                for kind, txt in interactions(geo, node[0], node[1]):
                                    viol.append((d, kind, txt))
                            viol.sort()
                            kinds = sorted({k for _d, k, _t in viol})
                            first_check = min((d for d, k, _t in viol if k == "check"), default=None)
                            res[expand] = dict(nodes=len(configs), ok=not viol, kinds=kinds,
                                               first=viol[0] if viol else None,
                                               first_check_depth=first_check, notes=sorted(notes))
                        rows.append(dict(board="cyl8" if wrap else "flat8", o=o, mirror=mirror, s=s, r=r,
                                         wk=nm(geo.wk), bk=nm(geo.bk),
                                         W=" ".join(sorted(map(nm, W0))), B=" ".join(sorted(map(nm, B0))),
                                         std=res[False], expand_terminal=res[True]))
    return rows


# ---------------- Part 2: G' + *2 outcome ----------------

def race_count(geo, W, B, mover_white):
    """Count rule: the opponent of the mover moves first; fewer moves wins;
    ties go to the opponent.  Distance of a passed front pawn, double step
    from the start rank counted."""
    def dist(white):
        best = None
        mine = W if white else B
        occ = W | B
        for f, r in mine:
            if not passed(geo, frozenset([(f, r)]) if white else W,
                          B if white else frozenset([(f, r)]), white):
                continue
            if white:
                if any((f, q) in occ for q in range(r + 1, H + 1)):
                    continue
                d = H - r - (1 if r == 2 else 0)
            else:
                if any((f, q) in occ for q in range(1, r)):
                    continue
                d = r - 1 - (1 if r == H - 1 else 0)
            best = d if best is None else min(best, d)
        return 10**6 if best is None else best
    other_white = not mover_white
    if dist(other_white) <= dist(mover_white):
        return other_white
    return mover_white


def make_solver(geo, checks_win, real_ep, race="count"):
    stats = {"races": 0, "check_ends": 0, "check_and_opp_passer": 0}

    @lru_cache(maxsize=None)
    def win(W, B, ep, heap, white_to_move):
        """True iff the side to move wins (normal play; passers end the game)."""
        moves = []
        for (W2, B2, e2) in gen(geo, W, B, ep, white_to_move):
            moves.append(("pawn", W2, B2, e2))
        for h2 in range(heap):
            moves.append(("nim", W, B, None if real_ep else ep, h2))
        if not moves:
            return False
        for mv in moves:
            if mv[0] == "pawn":
                _, W2, B2, e2 = mv
                wp, bp = passed(geo, W2, B2, True), passed(geo, W2, B2, False)
                chk = False
                if checks_win:
                    if white_to_move:
                        chk = any(geo.bk in geo.patt(p, True) for p in W2)
                    else:
                        chk = any(geo.wk in geo.patt(p, False) for p in B2)
                mine_p = (wp if white_to_move else bp) or chk
                opp_p = bp if white_to_move else wp
                if chk:
                    stats["check_ends"] += 1
                    if opp_p:
                        stats["check_and_opp_passer"] += 1
                if mine_p and opp_p:
                    stats["races"] += 1
                    if race == "count" and not chk:
                        w = race_count(geo, W2, B2, white_to_move)
                    elif race == "opponent":
                        w = not white_to_move
                    else:  # mover (also used when a check meets an opposing passer)
                        w = white_to_move
                    if w == white_to_move:
                        return True
                    continue
                if mine_p:
                    return True
                if opp_p:
                    continue
                # e.p. right only for the very next ply (real chess) or until
                # the e.p.-holder's opponent moves in this component (model)
                if not win(W2, B2, e2, heap, not white_to_move):
                    return True
            else:
                _, W2, B2, e2, h2 = mv
                if not win(W2, B2, e2, h2, not white_to_move):
                    return True
        return False
    return win, stats


def part2():
    out = []
    for wrap in (False, True):
        for o in (0, 1):
            for mirror in (False, True):
                for s in (1, -1):
                    for r in range(2, 7):
                        geo = Geo(wrap, s, r)
                        W0, B0 = place(o, mirror)
                        row = dict(board="cyl8" if wrap else "flat8", o=o, mirror=mirror, s=s, r=r,
                                   wk=nm(geo.wk), bk=nm(geo.bk))
                        for label, cw in (("model", False), ("checks_win", True)):
                            for re_ in (True, False):
                                win, st = make_solver(geo, cw, re_)
                                res = {}
                                for heap in (0, 1, 2):
                                    res[heap] = (win(W0, B0, None, heap, True), win(W0, B0, None, heap, False))
                                # G = *2  iff  G + *2 is a 2nd-player win
                                is_star2 = res[2] == (False, False)
                                row[f"{label}_{'realep' if re_ else 'modelep'}"] = dict(
                                    g0=res[0], g_plus_star=res[1], g_plus_star2=res[2],
                                    equals_star2=is_star2, **st)
                        out.append(row)
    return out


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("1", "all"):
        rows = part1()
        with open(__file__.replace("freeze_indep.py", "part1_freeze.jsonl"), "w") as fh:
            for x in rows:
                fh.write(json.dumps(x) + "\n")
        for b in ("flat8", "cyl8"):
            sub = [x for x in rows if x["board"] == b]
            ok = [x for x in sub if x["std"]["ok"]]
            ok_e = [x for x in sub if x["expand_terminal"]["ok"]]
            chk = [x for x in sub if "check" in x["std"]["kinds"]]
            print(f"{b}: pass {len(ok)}/{len(sub)} (expanding past passers: {len(ok_e)}/{len(sub)}); "
                  f"placements with a reachable check: {len(chk)}; nodes {sorted({x['std']['nodes'] for x in sub})}")
            print("   passing offsets:", sorted({(x['o'], x['mirror']) for x in ok}))
            notes = sorted({n for x in sub for n in x["std"]["notes"]})
            print("   notes:", notes)
        for x in rows:
            if x["board"] == "cyl8":
                print("  cyl8 o=%d m=%d s=%+d r=%d WK %s BK %s first=%s firstcheck=%s kinds=%s" % (
                    x["o"], x["mirror"], x["s"], x["r"], x["wk"], x["bk"], x["std"]["first"],
                    x["std"]["first_check_depth"], x["std"]["kinds"]))
    if which in ("2", "all"):
        rows = part2()
        with open(__file__.replace("freeze_indep.py", "part2_star2.jsonl"), "w") as fh:
            for x in rows:
                fh.write(json.dumps(x) + "\n")
        for b in ("flat8", "cyl8"):
            sub = [x for x in rows if x["board"] == b]
            for k in ("model_realep", "model_modelep", "checks_win_realep", "checks_win_modelep"):
                n = sum(x[k]["equals_star2"] for x in sub)
                print(f"{b} {k}: G'=*2 in {n}/{len(sub)} placements")
        for x in rows:
            if x["board"] == "cyl8" and (x["checks_win_realep"]["equals_star2"] or x["checks_win_modelep"]["equals_star2"]):
                print("  cyl8 placement still *2 with checks:", {k: x[k] for k in ("o", "mirror", "s", "r", "wk", "bk")})
