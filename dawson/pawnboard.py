"""Dawson's chess solved directly from the pawn rules on a 3 x n board, flat or
cylindrical, with no octal-game assumption. Written independently of
cylcgt/dawson.py and cylcgt/pawns.py.

Rules implemented:
  * ranks 1..3; White pawns start on rank 1, Black pawns on rank 3, rank 2 empty;
  * a pawn moves one square straight forward to an empty square, or captures one
    square diagonally forward (on the cylinder, files a and the last file are adjacent);
  * captures are compulsory (if the side to move has any capture it must capture);
  * no double steps (there is never room for one), so no en passant;
  * a pawn on its last rank has no moves (we record if this is ever reached).

For every position reachable from the start (White to move first, and separately Black
first) the program computes, by plain memoised minimax,
  - the normal-play outcome (side to move with no move loses), and
  - the misere outcome (side to move with no move wins),
and compares them, at every quiet position (side to move has no capture), with the
prediction of the octal game 0.137 on the multiset of maximal runs of untouched files
(on a full cylinder: the ring rule R_n = mex{g(n-3)}).

It also builds the "macro-move" graph (push, then all forced captures until the side to
move has no capture) and checks that:
  - every macro-move hands the turn to the opponent,
  - the set of resulting shapes is the same for White and for Black and equals the octal
    0.137 option set of the current shape,
and computes Grundy values on that graph straight from the pawn moves.

Run from the project root:
    PYTHONPATH=. .venv/bin/python -m dawson.pawnboard 10 10
(first argument: largest flat n, second: largest cylinder n)
"""
import sys
from functools import lru_cache

from dawson.octal import grundy
from dawson import misere as M

sys.setrecursionlimit(100000)

E, W, B = 0, 1, 2
FULL = (W, E, B)  # (rank1, rank2, rank3) of an untouched file


class Board:
    def __init__(self, n, wrap):
        self.n, self.wrap = n, wrap

    def nbrs(self, f):
        out = []
        for d in (-1, 1):
            x = f + d
            if self.wrap:
                x %= self.n
            if 0 <= x < self.n and x not in out:
                out.append(x)
        return out

    def start(self):
        return tuple(FULL for _ in range(self.n))

    def moves(self, pos, side):
        """Return (list of successor positions, is_capture_list, promoted_flag)."""
        me, them = (W, B) if side == 0 else (B, W)
        d = 1 if side == 0 else -1
        caps, pushes = [], []
        promo = False
        for f in range(self.n):
            for r in range(3):
                if pos[f][r] != me:
                    continue
                r1 = r + d
                if not 0 <= r1 <= 2:
                    continue
                for g in self.nbrs(f):
                    if pos[g][r1] == them:
                        caps.append(self._move(pos, f, r, g, r1, me))
                if pos[f][r1] == E:
                    pushes.append(self._move(pos, f, r, f, r1, me))
        res = caps if caps else pushes
        res = list(dict.fromkeys(res))
        for p in res:
            if (side == 0 and any(p[f][2] == W for f in range(self.n))) or \
               (side == 1 and any(p[f][0] == B for f in range(self.n))):
                promo = True
        return res, bool(caps), promo

    @staticmethod
    def _move(pos, f, r, g, r1, me):
        files = [list(x) for x in pos]
        files[f][r] = E
        files[g][r1] = me
        return tuple(tuple(x) for x in files)

    def has_capture(self, pos, side):
        return self.moves(pos, side)[1]

    def shape_heaps(self, pos):
        """Heaps = maximal runs of untouched files. Returns ('ring', n) if every file is
        untouched on a cylinder, else a sorted tuple of run lengths."""
        full = [pos[f] == FULL for f in range(self.n)]
        if all(full) and self.wrap:
            return ("ring", self.n)
        runs = []
        if self.wrap:
            k = full.index(False)
            order = [(k + i) % self.n for i in range(self.n)]
        else:
            order = list(range(self.n))
        cur = 0
        for f in order:
            if full[f]:
                cur += 1
            else:
                if cur:
                    runs.append(cur)
                cur = 0
        if cur:
            runs.append(cur)
        return tuple(sorted(runs))


def analyse(n, wrap, gvals):
    bd = Board(n, wrap)
    normal, misere = {}, {}
    promo_seen = [False]

    def solve(pos, side):
        key = (pos, side)
        if key in normal:
            return
        stack = [(key, False)]
        while stack:
            (p, s), expanded = stack.pop()
            if (p, s) in normal:
                continue
            succ, _, pr = bd.moves(p, s)
            if pr:
                promo_seen[0] = True
            if not expanded:
                stack.append(((p, s), True))
                for q in succ:
                    if (q, 1 - s) not in normal:
                        stack.append(((q, 1 - s), False))
            else:
                if not succ:
                    normal[(p, s)] = False
                    misere[(p, s)] = True
                else:
                    normal[(p, s)] = any(not normal[(q, 1 - s)] for q in succ)
                    misere[(p, s)] = any(not misere[(q, 1 - s)] for q in succ)

    start = bd.start()
    solve(start, 0)
    solve(start, 1)

    # predictions at quiet positions
    stats = dict(positions=len(normal), quiet=0, normal_bad=0, misere_bad=0, inert_bad=0)
    bad_examples = []
    for (p, s), win in normal.items():
        if bd.has_capture(p, s):
            continue
        stats["quiet"] += 1
        sh = bd.shape_heaps(p)
        if sh and sh[0] == "ring":
            pred_n = gvals[sh[1] - 3] == 0      # R_n = 1 iff g(n-3) = 0
            pred_m = M.misere_P(tuple(x for x in (sh[1] - 3,) if x > 0))  # mover wins iff strip n-3 is a misere P-position
        else:
            x = 0
            for h in sh:
                x ^= gvals[h]
            pred_n = x != 0
            pred_m = not M.misere_P(sh)
        if pred_n != win:
            stats["normal_bad"] += 1
            bad_examples.append(("normal", p, s, sh))
        if pred_m != misere[(p, s)]:
            stats["misere_bad"] += 1
            bad_examples.append(("misere", p, s, sh))
        # every legal move must start from an untouched file
        succ, _, _ = bd.moves(p, s)
        for q in succ:
            changed = [f for f in range(n) if q[f] != p[f]]
            if not all(p[f] == FULL for f in changed):
                stats["inert_bad"] += 1
    stats["promotion_reached"] = promo_seen[0]
    return bd, normal, misere, stats, bad_examples


def macro_check(bd, normal, gvals):
    """Macro-move graph on quiet positions; returns (#quiet positions checked, problems,
    grundy value of the start computed on the graph)."""
    from dawson.octal import heap_moves, octal_options
    mv = octal_options("0.137")

    def endpoints(pos, side):
        """Quiet endpoints (pos, side_to_move) after `side` pushes and forced captures run out."""
        out = set()
        succ, iscap, _ = bd.moves(pos, side)
        assert not iscap
        for q in succ:
            stack = [(q, 1 - side)]
            while stack:
                p, s = stack.pop()
                nxt, c, _ = bd.moves(p, s)
                if c:
                    for r in nxt:
                        stack.append((r, 1 - s))
                else:
                    out.add((p, s))
        return out

    def octal_opts_of_shape(sh):
        if sh and sh[0] == "ring":
            return {tuple(sorted(x for x in (sh[1] - 3,) if x > 0))}
        res = set()
        for i, h in enumerate(sh):
            rest = list(sh[:i] + sh[i + 1:])
            for parts in heap_moves(mv, h):
                res.add(tuple(sorted(rest + list(parts))))
        return res

    quiet_boards = {p for (p, s) in normal if not bd.has_capture(p, 0) and not bd.has_capture(p, 1)}
    problems = []
    shape_opts = {}
    for p in quiet_boards:
        sh = bd.shape_heaps(p)
        per_side = []
        for side in (0, 1):
            eps = endpoints(p, side)
            if any(s != 1 - side for (_, s) in eps):
                problems.append(("turn does not pass", p, side))
            per_side.append({bd.shape_heaps(q) for (q, _) in eps})
        if per_side[0] != per_side[1]:
            problems.append(("White and Black option shapes differ", p))
        if per_side[0] != octal_opts_of_shape(sh):
            problems.append(("option shapes differ from 0.137", p, sh, per_side[0]))
        shape_opts.setdefault(sh, per_side[0])

    @lru_cache(maxsize=None)
    def G(sh):
        opts = {G(o) for o in shape_opts[sh]} if sh in shape_opts else None
        if opts is None:
            raise KeyError(sh)
        m = 0
        while m in opts:
            m += 1
        return m

    start_shape = bd.shape_heaps(bd.start())
    gdirect = {sh: G(sh) for sh in shape_opts}
    xor_bad = 0
    for sh, v in gdirect.items():
        if sh and sh[0] == "ring":
            pred = 1 if gvals[sh[1] - 3] == 0 else 0
        else:
            pred = 0
            for h in sh:
                pred ^= gvals[h]
        if pred != v:
            xor_bad += 1
    return len(quiet_boards), problems, G(start_shape), len(gdirect), xor_bad


def main(nflat=10, nring=10):
    gvals = grundy("0.137", 400)
    print("Dawson's chess from the pawn rules (3 x n board). 'W-first' / 'B-first' = normal-play"
          " result for the side to move at the start; misere likewise.")
    print(f"{'board':>9} | {'positions':>9} | {'quiet':>6} | normal W/B first | misere W/B first |"
          f" pred mismatches (normal, misere, inert) | promo | macro: graph-Grundy vs octal, problems, xor-mismatch")
    for wrap, top in ((False, nflat), (True, nring)):
        for n in range(1 if not wrap else 3, top + 1):
            bd, normal, misere, st, bad = analyse(n, wrap, gvals)
            s = bd.start()
            nw = "win" if normal[(s, 0)] else "loss"
            nb = "win" if normal[(s, 1)] else "loss"
            mw = "win" if misere[(s, 0)] else "loss"
            mb = "win" if misere[(s, 1)] else "loss"
            nq, probs, gd, nshapes, xb = macro_check(bd, normal, gvals)
            octv = (1 if gvals[n - 3] == 0 else 0) if wrap else gvals[n]
            name = f"{'cyl' if wrap else 'flat'} {n:2d}"
            print(f"{name:>9} | {st['positions']:9d} | {st['quiet']:6d} | {nw:>5}/{nb:<5}        |"
                  f" {mw:>5}/{mb:<5}       | {st['normal_bad']}, {st['misere_bad']}, {st['inert_bad']}"
                  f"{'':28s} | {str(st['promotion_reached']):5s} | {gd} vs {octv}, {len(probs)}, {xb} (shapes {nshapes})")
            for b in bad[:3]:
                print("   MISMATCH", b)
            for p in probs[:3]:
                print("   PROBLEM", p)
            sys.stdout.flush()


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:]]
    main(*a)
