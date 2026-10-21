"""The real-chess oracle value of a component.

Take the CGT game tree of the a-d component (cylcgt rules, 4-file flat board,
e.p. on). Every model terminal T (a position, entered by a move, in which some
side has a passed pawn; races included) is replaced by a game built from its
REAL-CHESS outcome class, measured on the 8x8 embedding with the g-file
trebuchet:

    rW = result for White when White moves first in T,
    rB = result for White when Black moves first in T,

    L (White wins either way)  -> +BIG
    R (Black wins either way)  -> -BIG
    N (mover wins)             -> {+BIG | -BIG}   (treatment, see REPORT.md)
    P (mover loses)            -> 0               (treatment)
    any draw                   -> unknown in [-BIG, +BIG] (sandwich only)

An e.p. right created by the move into T belongs only to the opponent of
that mover, exactly as in cylcgt; so "the opponent moves first" uses the e.p.
square and "the mover moves again" does not.

Budget: resolving all terminals is too expensive (an 8-man terminal needs a
search), so terminals are resolved adaptively and the value is CERTIFIED by
monotonicity (Conway: raising any option of any position never lowers the
game). With the unresolved terminals all set to -BIG we get G_lo, all set to
+BIG gives G_hi, and every assignment of numbers +-BIG (classes L/R) lies in
between. If G_lo == G_hi the value is pinned whatever L/R classes the
unresolved terminals turn out to have. A second, wider sandwich (+-2*BIG)
also covers N and P terminals (+-BIG switch and 0 lie strictly inside it).

Selection: with the cylcgt model (RACE_RULE 'count') as a prior for the
unknown terminals, find a small sufficient set (greedy "un-fix" pass, trying
to drop 8-man terminals first because they need a search), resolve the
unknown members of that set, recompute, and repeat until G_lo == G_hi.
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

from cylcgt import cgt, pawns
from cylcgt.pawns import Pos

from . import component as C
from . import movegen as mg
from .probe import CapReached
from .search import Searcher, cat_interval

BIG = C.BIG
G_BIG, G_NBIG = cgt.integer(BIG), cgt.integer(-BIG)
G_BIG2, G_NBIG2 = cgt.integer(2 * BIG), cgt.integer(-2 * BIG)
G_SWITCH = cgt.make([G_BIG], [G_NBIG])


def other(side):
    return "B" if side == "W" else "W"


class Terminals:
    def __init__(self, comp: Pos, board=C.BOARD4):
        self.comp, self.board = comp, board
        self.internal, self.terms, self.edges = C.enumerate_tree(board, comp)
        self.movers = {}
        self.parents = {}  # T -> list of (internal node, mover) with T among the mover's options
        for (p, side), kids in self.edges.items():
            for q in kids:
                if q in self.terms:
                    self.movers.setdefault(q, set()).add(side)
                    self.parents.setdefault(q, []).append((p, side))
        self.order = sorted(self.terms, key=lambda t: (self.men(t), str(t)))

    def men(self, t):
        return 4 + len(t.white) + len(t.black)

    def real_pos(self, t: Pos, stm: str) -> mg.Position:
        return C.embed(t, stm)  # keeps t.ep only if it belongs to stm

    def value(self, assign):
        """assign(t) -> cgt.Game for every terminal."""
        return C.value_with(self.board, self.comp, lambda q, mover: assign(q))


def class_of(rw, rb):
    if rw is None or rb is None:
        return None
    if rw == 1 and rb == 1:
        return "L"
    if rw == -1 and rb == -1:
        return "R"
    if rw == 1 and rb == -1:
        return "N"
    if rw == -1 and rb == 1:
        return "P"
    return "D"  # some draw involved


def game_for(cls, lo_side: bool, wide: bool = False):
    """Replacement game for a resolved class (lo_side picks the sandwich end
    used for draws)."""
    if cls == "L":
        return G_BIG
    if cls == "R":
        return G_NBIG
    if cls == "N":
        return G_SWITCH
    if cls == "P":
        return cgt.ZERO
    if wide:
        return G_NBIG2 if lo_side else G_BIG2
    return G_NBIG if lo_side else G_BIG


def bounds(T: Terminals, known: dict, prior: dict | None = None, wide: bool = False):
    """(G_lo, G_hi). known[t] = class; prior[t] = class used for unknowns
    instead of the sandwich (None: sandwich)."""
    def lo(t):
        c = known.get(t) or (prior.get(t) if prior else None)
        return game_for(c, True, wide)

    def hi(t):
        c = known.get(t) or (prior.get(t) if prior else None)
        return game_for(c, False, wide)
    return T.value(lo), T.value(hi)


def sufficient_set(T: Terminals, known: dict, prior: dict, cost, forced_free=frozenset()):
    """Greedy: start from 'everything fixed' (known classes, prior for the
    rest), then try to un-fix each unknown terminal (most expensive first);
    keep it un-fixed if the bounds still coincide with the target value.
    Terminals in forced_free (could not be resolved) always use the sandwich.
    Returns (needed, target) or (None, None) if no choice can pin the value."""
    def fixed(x, lo_side):
        if x in forced_free:
            return G_NBIG if lo_side else G_BIG
        return game_for(known.get(x) or prior[x], lo_side)
    target = T.value(lambda t: fixed(t, True))
    if T.value(lambda t: fixed(t, False)) is not target:
        return None, None
    unknown_fixed = [t for t in T.terms if t not in known and t not in forced_free]
    unknown_fixed.sort(key=lambda t: (-cost(t), str(t)))
    free = set(forced_free)
    for t in unknown_fixed:
        free.add(t)

        def lo(x):
            if x in free:
                return G_NBIG
            return fixed(x, True)

        g_lo = T.value(lo)
        if g_lo is not target:
            free.discard(t)
            continue

        def hi(x):
            if x in free:
                return G_BIG
            return fixed(x, False)

        if T.value(hi) is not target:
            free.discard(t)
    return [t for t in unknown_fixed if t not in free], target


# --------------------------------------------------------------- resolution
class Resolver:
    """Real-chess results (White's view) of terminal positions, both sides to
    move, sharing one Searcher (TT + probe cache) with the other stages."""

    def __init__(self, T: Terminals, searcher: Searcher, oracle, cached, ext: int, per_terminal=0):
        self.T, self.s, self.oracle, self.cached, self.ext = T, searcher, oracle, cached, ext
        self.per_terminal = per_terminal
        self.result = {}  # (t, side) -> +1/0/-1 for White, or None if unresolved
        self.how = {}
        self.child_index = {}  # child normal FEN -> (category, parent FEN)

    def index_record(self, parent_fen: str):
        """Make every child of a cached parent available without a request."""
        rec = self.cached(parent_fen)
        if not rec or not rec.get("data"):
            return
        par = mg.parse_fen(parent_fen)
        cats = {m["uci"]: m.get("category") for m in rec["data"].get("moves", [])}
        for m in mg.legal_moves(par):
            cat = cats.get(m.uci())
            if cat in (None, "unknown"):
                continue
            self.child_index.setdefault(mg.normal_fen(mg.make(par, m)), (cat, parent_fen))

    def white_result(self, t: Pos, side: str):
        key = (t, side)
        if key in self.result and self.result[key] is not None:
            return self.result[key]
        pos = self.T.real_pos(t, side)
        errs = mg.validity_errors(pos)
        if errs:
            self.result[key] = None
            self.how[key] = "illegal: " + "; ".join(errs)
            return None
        iv = None
        if pos.men() <= 7:
            # 1) free: the position as a capture child of a cached parent probe
            for (p, mover) in self.T.parents.get(t, []):
                if other(mover) != side:
                    continue
                parent = C.embed(p, mover)
                rec = self.cached(mg.normal_fen(parent))
                if rec is None:
                    continue
                want = mg.normal_fen(pos)
                for m in mg.legal_moves(parent):
                    if mg.is_capture(parent, m) and mg.normal_fen(mg.make(parent, m)) == want:
                        iv = self.s.capture_child(parent, m, allow_probe=False)
                        self.how[key] = "child of cached parent " + mg.normal_fen(parent)
                        break
                if iv is not None and iv[0] == iv[1]:
                    break
            if (iv is None or iv[0] != iv[1]) and mg.normal_fen(pos) in self.child_index:
                cat, pf = self.child_index[mg.normal_fen(pos)]
                self.s._note(pf, "child " + mg.normal_fen(pos), cat)
                iv = cat_interval(cat, self.s.mode)
                self.how[key] = "child of cached parent " + pf
            if iv is None or iv[0] != iv[1]:
                iv = self.s.search(pos, 0)  # probes the 7-man position itself
                self.how[key] = "probe"
        else:
            from .solve_candidate import deepen
            budget = getattr(self.oracle, "max_new", None)
            if budget is not None and self.per_terminal:
                self.oracle.max_new = min(budget, self.oracle.new_requests + self.per_terminal)
            try:
                iv = deepen(self.s, pos, self.ext)
                self.how[key] = f"search (ext<={self.ext})"
            except CapReached:
                if budget is not None and self.oracle.new_requests >= budget:
                    raise
                h = self.s.tt.get(mg.normal_fen(pos))
                iv = (h[0], h[1]) if h else (-1, 1)
                self.how[key] = f"search aborted (per-terminal budget {self.per_terminal})"
            finally:
                if budget is not None:
                    self.oracle.max_new = budget
        if iv[0] != iv[1]:
            self.result[key] = None
            self.how[key] += " -> unresolved"
            return None
        v = iv[0] if pos.stm == mg.WHITE else -iv[0]
        self.result[key] = v
        return v

    def resolve(self, t: Pos):
        rw = self.white_result(t, "W")
        rb = self.white_result(t, "B")
        return class_of(rw, rb), rw, rb


def retraction_parents(pos: mg.Position):
    """Positions one single pawn step earlier (the other side to move) whose
    child after that step is `pos`: probing one of them answers pos for free."""
    out = []
    mover = mg.BLACK if pos.stm == mg.WHITE else mg.WHITE
    pawn = "P" if mover == mg.WHITE else "p"
    back = -8 if mover == mg.WHITE else 8
    for s, pc in enumerate(pos.board):
        if pc != pawn:
            continue
        t = s + back
        r = t // 8
        if not (1 <= r <= 6) or pos.board[t] != mg.EMPTY:
            continue
        b = list(pos.board)
        b[s], b[t] = mg.EMPTY, pawn
        par = mg.Position(tuple(b), mover, None, 0, 1)
        if mg.validity_errors(par):
            continue
        out.append(par)
    return out


def plan_7man_probes(T: Terminals, todo, cached, known_fens=frozenset()):
    """Greedy set cover: which parents to probe so that one request answers
    several needed 7-man (terminal, side) pairs."""
    need = {}
    for t in todo:
        for side in "WB":
            pos = T.real_pos(t, side)
            f = mg.normal_fen(pos)
            if pos.men() <= 7 and f not in known_fens:
                need[f] = (t, side)
    cands = {}
    for f in list(need):
        for par in retraction_parents(mg.parse_fen(f)):
            cands.setdefault(mg.normal_fen(par), par)
    for fen, (t, side) in need.items():
        # the parent internal node (8-man), mover = opponent of side
        for (p, mover) in T.parents.get(t, []):
            if other(mover) == side:
                par = C.embed(p, mover)
                cands.setdefault(mg.normal_fen(par), par)
    cover = {}
    for f, par in cands.items():
        kids = {mg.normal_fen(mg.make(par, m)) for m in mg.legal_moves(par)
                if par.men() <= 7 or mg.is_capture(par, m)}
        cover[f] = kids & set(need)
    chosen, left = [], set(need)
    # already-cached parents first (free)
    for f, c in cover.items():
        if cached(f) is not None:
            left -= c
    while True:
        best = max(cover, key=lambda f: len(cover[f] & left), default=None)
        if best is None or len(cover[best] & left) < 2:
            break  # a direct probe is as cheap as a parent covering one pair
        chosen.append(best)
        left -= cover[best]
    return chosen, cands


def classes_under(raw: dict, draw_as: int):
    """Fully resolved terminals -> class, a draw counted as `draw_as` (+1 a
    White win, -1 a Black win)."""
    out = {}
    for t, (rw, rb) in raw.items():
        if rw is None or rb is None:
            continue
        f = lambda v: v if v != 0 else draw_as
        out[t] = class_of(f(rw), f(rb))
    return out


def _excluded(T, assign, target, direction):
    g = T.value(assign)
    if direction == "left":      # Left moving first wins g - target: g is not <= target
        return not cgt.le(g, target)
    return not cgt.le(target, g)  # Right moving first wins g - target


def certificate(T, raw, target, draw_as, direction, max_combos=4096):
    """True iff, with every fully resolved terminal at its real class (draws
    as draw_as), every partially resolved terminal at EVERY completion of its
    missing side, and every other terminal free in the wide sandwich
    (-2BIG for the left test, +2BIG for the right test), the value differs
    from target. By monotonicity this excludes target for every class
    (L, R, N, P) of the free terminals."""
    import itertools
    known = classes_under(raw, draw_as)
    partial = [t for t, (rw, rb) in raw.items() if (rw is None) != (rb is None)]
    free_game = G_NBIG2 if direction == "left" else G_BIG2
    n = 0
    for k2 in _completions(raw, draw_as):
        n += 1
        if n > max_combos:
            return None
        if not _excluded(T, lambda t: game_for(k2[t], True) if t in k2 else free_game, target, direction):
            return False
    return True


def need_for_exclusion(T, raw, prior, attempted, target, draw_as, direction):
    """Greedy small set of unattempted terminals that, at their model (prior)
    classes, would make the exclusion test pass (partials completed by the
    prior during selection; the final certificate enumerates them)."""
    known = classes_under(raw, draw_as)
    for t, (rw, rb) in raw.items():
        if (rw is None) != (rb is None):
            v = 1 if prior[t] == "L" else -1
            f = lambda x: x if x != 0 else draw_as
            known[t] = class_of(f(rw if rw is not None else v), f(rb if rb is not None else v))
    cands = [t for t in T.terms if t not in known and t not in attempted]
    free_game = G_NBIG2 if direction == "left" else G_BIG2
    free = set()

    def ok():
        return _excluded(T, lambda t: game_for(known[t], True) if t in known else
                         (free_game if t in free else game_for(prior[t], True)), target, direction)
    if not ok():
        return None
    for t in sorted(cands, key=lambda t: (-T.men(t), str(t))):
        free.add(t)
        if not ok():
            free.discard(t)
    return [t for t in cands if t not in free]


def _completions(raw, draw_as, prior=None):
    """Yield class dicts for the resolved terminals, enumerating the missing
    side of every partial terminal (or completing it from `prior`)."""
    import itertools
    known = classes_under(raw, draw_as)
    partial = [t for t, (rw, rb) in raw.items() if (rw is None) != (rb is None)]
    f = lambda x: x if x != 0 else draw_as
    if prior is not None:
        k2 = dict(known)
        for t in partial:
            rw, rb = raw[t]
            v = 1 if prior[t] == "L" else -1
            k2[t] = class_of(f(rw if rw is not None else v), f(rb if rb is not None else v))
        yield k2
        return
    opts = []
    for t in partial:  # distinct classes only (a draw maps onto draw_as)
        rw, rb = raw[t]
        opts.append(sorted({class_of(f(rw if rw is not None else v), f(rb if rb is not None else v))
                            for v in (1, 0, -1)}))
    for combo in itertools.product(*opts):
        k2 = dict(known)
        k2.update(zip(partial, combo))
        yield k2


def pinned_value(T, raw, draw_as, wide=True):
    """The value if it is the same for every completion of the partial
    terminals and every class of the unattempted ones (sandwich), else None."""
    LO, HI = (G_NBIG2, G_BIG2) if wide else (G_NBIG, G_BIG)
    val = None
    for k in _completions(raw, draw_as):
        lo = T.value(lambda t: game_for(k[t], True) if t in k else LO)
        hi = T.value(lambda t: game_for(k[t], True) if t in k else HI)
        if lo is not hi or (val is not None and lo is not val):
            return None
        val = lo
    return val


def need_for_pin(T, raw, prior, attempted, draw_as, wide=True):
    LO, HI = (G_NBIG2, G_BIG2) if wide else (G_NBIG, G_BIG)
    known = next(_completions(raw, draw_as, prior))
    fixed = lambda t: game_for(known.get(t) or prior[t], True)
    target = T.value(fixed)
    cands = sorted([t for t in T.terms if t not in known and t not in attempted],
                   key=lambda t: (-T.men(t), str(t)))
    free = set()
    for t in cands:
        free.add(t)
        if T.value(lambda x: LO if x in free else fixed(x)) is not target or \
                T.value(lambda x: HI if x in free else fixed(x)) is not target:
            free.discard(t)
    return [t for t in cands if t not in free], target


def stage_oracle(args, build):
    from .solve_candidate import RESULTS, write_json, tag_of, comp_str, make_order
    comp, model, oracle, cached, region = build(args)
    T = Terminals(comp)
    s = Searcher(oracle, mode=args.mode, order_hint=make_order(model, cached), region=region,
                 cached=cached, kb=oracle.kb)
    R = Resolver(T, s, oracle, cached, args.ext, per_terminal=args.per_terminal)
    prior = {}
    for t in T.terms:
        m = next(iter(T.movers[t]))
        prior[t] = "L" if C.model_terminal_value(T.board, t, m, "count") > 0 else "R"
    target = cgt.nimber(2) if args.target == "*2" else None
    if target is None:
        raise SystemExit("--target: only '*2' is implemented")
    path = os.path.join(RESULTS, f"{tag_of(comp)}_oracle_{args.mode}{args.label}.json")
    raw, attempted, log = {}, set(), []
    byname = {str(t): t for t in T.terms}
    if args.resume and os.path.exists(path):
        old = json.load(open(path))
        for r in old["terminals"]:
            t = byname[r["terminal"]]
            if r.get("how_W") or r.get("how_B"):
                attempted.add(t)
                raw[t] = (r["real_W_first"], r["real_B_first"])
                R.how[(t, "W")], R.how[(t, "B")] = r.get("how_W"), r.get("how_B")
                R.result[(t, "W")], R.result[(t, "B")] = r["real_W_first"], r["real_B_first"]
        log = old.get("iterations", [])
    status = "complete"
    t0 = time.time()

    def cost(t):  # prefer to leave 8-man terminals unresolved
        return 2 if T.men(t) >= 8 else 1

    def resolve_list(todo):
        todo = sorted(todo, key=lambda t: (T.men(t), str(t)))
        for (p, mover) in T.edges:
            f = mg.normal_fen(C.embed(p, mover))
            if cached(f) is not None:
                R.index_record(f)
        chosen, cands = plan_7man_probes(T, todo, cached, frozenset(R.child_index))
        for f in cands:
            if cached(f) is not None:
                R.index_record(f)
        for f in chosen:
            s._rec(mg.parse_fen(f))
            R.index_record(f)
        for t in todo:
            cls, rw, rb = R.resolve(t)
            raw[t] = (rw, rb)
            attempted.add(t)

    try:
        for it in range(len(log) + 1, len(log) + 40):
            known = classes_under(raw, -1)
            g_lo, g_hi = bounds(T, known)
            entry = {"iter": it, "goal": args.goal, "attempted": len(attempted),
                     "G_lo": cgt.show(g_lo), "G_hi": cgt.show(g_hi), "requests": oracle.new_requests}
            if args.goal == "exclude":
                cert = {d: {dr: certificate(T, raw, target, d, dr) for dr in ("left", "right")}
                        for d in (+1, -1)}
                entry["certificate"] = {("draw=White win" if d > 0 else "draw=Black win"): v
                                        for d, v in cert.items()}
            log.append(entry)
            print(json.dumps(entry), flush=True)
            if args.goal == "pin":
                pins = {d: pinned_value(T, raw, d) for d in (-1, +1)}
                entry["pinned"] = {("draw=White win" if d > 0 else "draw=Black win"):
                                   (cgt.show(v) if v is not None else None) for d, v in pins.items()}
                print(json.dumps(entry["pinned"]), flush=True)
                todo = set()
                for d in (-1, +1):
                    if pins[d] is None:
                        nd, _ = need_for_pin(T, raw, prior, attempted, d)
                        todo |= set(nd)
                if all(v is not None for v in pins.values()):
                    break
                todo = [t for t in todo if t not in attempted]
            else:
                todo = set()
                undone = [d for d in (+1, -1) if not any(cert[d].values())]
                if not undone:
                    break
                for d in undone:
                    best = None
                    for dr in ("left", "right"):
                        nd = need_for_exclusion(T, raw, prior, attempted, target, d, dr)
                        if nd is not None and (best is None or len(nd) < len(best)):
                            best = nd
                    if best is None:
                        status = "cannot exclude target even if every unattempted terminal had its model class"
                        break
                    todo |= set(best)
                if status != "complete":
                    break
                todo = [t for t in todo if t not in attempted]
            if not todo:
                status = "stalled: nothing left to resolve that would help"
                break
            resolve_list(todo)
    except CapReached as e:
        status = f"stopped: {e}"
    rows = []
    for t in T.order:
        rw, rb = raw.get(t, (None, None))
        rows.append({"terminal": str(t), "men": T.men(t), "entered_by": sorted(T.movers[t]),
                     "race": pawns.passed(T.board, t, "W") and pawns.passed(T.board, t, "B"),
                     "model_count": prior[t],
                     "model_by_rule": {rule: sorted({("L" if C.model_terminal_value(T.board, t, m, rule) > 0 else "R")
                                                     for m in T.movers[t]}) for rule in ("count", "mover", "opponent")},
                     "real_W_first": rw, "real_B_first": rb,
                     "real_class": class_of(rw, rb) if rw is not None and rb is not None else None,
                     "how_W": R.how.get((t, "W")), "how_B": R.how.get((t, "B"))})
    resolved = [r for r in rows if r["real_class"]]
    out = {
        "component": comp_str(comp), "mode": args.mode, "dry_run": args.dry_run, "status": status,
        "goal": args.goal, "target": args.target,
        "terminals_total": len(T.terms), "terminals_attempted": len(attempted),
        "terminals_resolved_both_sides": len(resolved),
        "terminals_partial": [r["terminal"] for r in rows
                              if (r["real_W_first"] is None) != (r["real_B_first"] is None)],
        "class_counts": dict(Counter(r["real_class"] for r in resolved)),
        "non_LR_terminals": [r for r in resolved if r["real_class"] not in ("L", "R")],
        "disagree_with_count_model": [r for r in resolved if r["real_class"] in ("L", "R")
                                      and r["real_class"] != r["model_count"]],
        "iterations": log, "new_requests_this_run": oracle.new_requests,
        "seconds_this_run": round(time.time() - t0, 1),
        "categories_seen_this_run": dict(s.cats_seen), "special_categories_this_run": s.special,
    }
    for d, name in ((+1, "draw=White win"), (-1, "draw=Black win")):
        known = classes_under(raw, d)
        g_lo, g_hi = bounds(T, known)
        w_lo, w_hi = bounds(T, known, wide=True)
        g_prior = T.value(lambda t: game_for(known.get(t) or prior[t], True))
        out[name] = {
            "value_if_unresolved_take_model_class": cgt.show(g_prior),
            "narrow_bounds": [cgt.show(g_lo), cgt.show(g_hi)], "narrow_pinned": g_lo is g_hi,
            "wide_bounds": [cgt.show(w_lo), cgt.show(w_hi)], "wide_pinned": w_lo is w_hi,
            "certificate_not_target": {dr: certificate(T, raw, target, d, dr) for dr in ("left", "right")},
        }
        pv = pinned_value(T, raw, d)
        out[name]["pinned_value_wide_sandwich"] = cgt.show(pv) if pv is not None else None
    out["terminals"] = rows
    if not args.dry_run:
        write_json(path, out)
    brief = {k: v for k, v in out.items() if k not in ("terminals", "special_categories_this_run",
                                                       "non_LR_terminals", "disagree_with_count_model",
                                                       "iterations")}
    print(json.dumps(brief, indent=1, default=str))
    print("non-L/R terminals:", len(out["non_LR_terminals"]),
          "disagreements with count model:", len(out["disagree_with_count_model"]))
    return out


# ===================================================================== v2
# Exhaustive (offline-friendly) resolution of every terminal, and bounds by
# plain monotonicity. Used by `solve_candidate oracle-all`.
#
# Per terminal t, the real-chess results rW (White moves first) and rB (Black
# moves first), White's view, are each +1/0/-1 or None (unresolved). Its
# replacement game is only known to lie in an interval [lo(t), hi(t)]:
#
#   treatment "switch" (draw_as = +1 or -1): a draw counts as a win for that
#     side; then L -> +BIG, R -> -BIG, N -> {+BIG | -BIG}, P -> 0, and an
#     unresolved side may be either result. lo/hi are the least / greatest
#     possible game when one exists (R <= P <= L), else -2BIG / +2BIG: the
#     switch N = {+BIG | -BIG} is confused with both +BIG and -BIG, so a
#     terminal that might be N (or is unknown) gets [-2BIG, +2BIG].
#   treatment "free": only certain L and certain R terminals are fixed (+-BIG);
#     every other terminal (N, P, any draw, any partly or wholly unresolved
#     one) is an arbitrary game in [-2BIG, +2BIG] (which contains +-BIG,
#     {+BIG | -BIG} and 0).
#
# Raising any option never lowers a game (Conway), so with G_lo, G_hi built
# from all lo's / all hi's, G_lo <= G <= G_hi for every admissible choice.
#   * pinned:            G_lo == G_hi  (the value is then that game);
#   * target excluded:   G_lo is not <= target, or target is not <= G_hi.

CLASS_GAME = {"L": G_BIG, "R": G_NBIG, "N": G_SWITCH, "P": cgt.ZERO}
TREATMENTS = {
    # name: (kind, draw_as)
    "switch, draw = Black win": ("switch", -1),
    "switch, draw = White win": ("switch", +1),
    "switch, draw = 0": ("draw0", 0),
    "free (only L/R fixed)": ("free", 0),
}


def pair_game(rw, rb, kind: str, draw_as: int = -1):
    """Replacement game for a terminal whose real results are rw (White moves
    first) and rb (Black moves first), White's view, both known.
      switch: a draw counts as a win for side draw_as; then L -> +BIG,
              R -> -BIG, N -> {+BIG | -BIG}, P -> 0;
      draw0 : L -> +BIG, R -> -BIG, otherwise {BIG*rw | BIG*rb} (a draw is
              worth 0: e.g. draw/Black-win -> {0 | -BIG}, draw/draw -> *)."""
    if kind == "switch":
        f = lambda x: x if x != 0 else draw_as
        return CLASS_GAME[class_of(f(rw), f(rb))]
    if kind == "draw0":
        if rw == rb and rw != 0:
            return G_BIG if rw == 1 else G_NBIG
        return cgt.make([cgt.integer(BIG * rw)], [cgt.integer(BIG * rb)])
    raise ValueError(kind)


def possible_games(rw, rb, kind: str, draw_as: int = -1):
    vals = (1, 0, -1)
    ws = [rw] if rw is not None else vals
    bs = [rb] if rb is not None else vals
    out = []
    for a in ws:
        for b in bs:
            g = pair_game(a, b, kind, draw_as)
            if all(g is not h for h in out):
                out.append(g)
    return out


def _extreme(games, low: bool):
    """A possible game that is <= (low) / >= (high) every possible game, if
    one exists; otherwise -2BIG / +2BIG, which bound every replacement game
    used here. (Careful: the switch {+BIG | -BIG} is confused with BOTH +BIG
    and -BIG, so N is incomparable with L and with R.)"""
    for g in games:
        if all((cgt.le(g, h) if low else cgt.le(h, g)) for h in games):
            return g
    return G_NBIG2 if low else G_BIG2


def interval_of(rw, rb, kind: str, draw_as: int = -1):
    if kind == "free":
        if rw is not None and rb is not None and rw == rb and rw != 0:
            return (G_BIG, G_BIG) if rw == 1 else (G_NBIG, G_NBIG)
        return (G_NBIG2, G_BIG2)
    games = possible_games(rw, rb, kind, draw_as)
    return _extreme(games, True), _extreme(games, False)


def sandwich(T: Terminals, raw: dict, kind: str, draw_as: int = -1, fixed=None):
    """(G_lo, G_hi); `fixed` maps some terminals to a chosen game."""
    fixed = fixed or {}
    iv = {t: interval_of(*raw.get(t, (None, None)), kind, draw_as) for t in T.terms}
    g_lo = T.value(lambda t: fixed[t] if t in fixed else iv[t][0])
    g_hi = T.value(lambda t: fixed[t] if t in fixed else iv[t][1])
    return g_lo, g_hi


def excluded(g_lo, g_hi, target) -> dict:
    return {"by_lower_bound": not cgt.le(g_lo, target), "by_upper_bound": not cgt.le(target, g_hi)}


def ambiguous_partials(T, raw, kind, draw_as):
    """Terminals with at least one known side whose possible games have no
    least or no greatest element (so the sandwich must use +-2BIG)."""
    out = []
    for t in T.terms:
        rw, rb = raw.get(t, (None, None))
        if (rw is None) == (rb is None) or kind == "free":
            continue
        games = possible_games(rw, rb, kind, draw_as)
        lo, hi = _extreme(games, True), _extreme(games, False)
        if lo is G_NBIG2 or hi is G_BIG2:
            out.append(t)
    return out


def enum_certificate(T, raw, target, kind, draw_as, enum_set, max_combos=1 << 14):
    """Exclusion of `target` with the terminals in enum_set ranging over their
    possible games ONE COMBINATION AT A TIME (exact), all other terminals in
    their sandwich. True / False / None (too many combinations)."""
    import itertools
    opts = [possible_games(*raw.get(t, (None, None)), kind, draw_as) for t in enum_set]
    n = 1
    for o in opts:
        n *= len(o)
    if n > max_combos:
        return None, n
    for combo in itertools.product(*opts):
        g_lo, g_hi = sandwich(T, raw, kind, draw_as, fixed=dict(zip(enum_set, combo)))
        ex = excluded(g_lo, g_hi, target)
        if not (ex["by_lower_bound"] or ex["by_upper_bound"]):
            return False, n
    return True, n


def _minimal(games, low=True):
    """Minimal (low) / maximal elements of a finite set of games."""
    out = []
    for g in games:
        dominated = any((h is not g) and (cgt.le(h, g) if low else cgt.le(g, h)) for h in games)
        if not dominated:
            out.append(g)
    return out


def one_sided_certificate(T, raw, target, kind, draw_as, enum_set, test: str, max_combos=1 << 14):
    """test='lower': for every combination of MINIMAL possible games of the
    terminals in enum_set (others at their sandwich low end), G_lo is not <=
    target. Every admissible assignment lies above one such combination, so by
    monotonicity no admissible G is <= target, hence none equals it.
    test='upper' is the mirror image (maximal games, target not <= G_hi)."""
    import itertools
    low = test == "lower"
    opts = [_minimal(possible_games(*raw.get(t, (None, None)), kind, draw_as), low) for t in enum_set]
    n = 1
    for o in opts:
        n *= len(o)
    if n > max_combos:
        return None, n
    for combo in itertools.product(*opts):
        g_lo, g_hi = sandwich(T, raw, kind, draw_as, fixed=dict(zip(enum_set, combo)))
        if low and cgt.le(g_lo, target):
            return False, n
        if not low and cgt.le(target, g_hi):
            return False, n
    return True, n


def describe_bounds(g_lo, g_hi, targets: dict):
    out = {"G_lo": cgt.show(g_lo), "G_hi": cgt.show(g_hi), "pinned": g_lo is g_hi,
           "outcome_G_lo": cgt.outcome(g_lo), "outcome_G_hi": cgt.outcome(g_hi)}
    for name, g in targets.items():
        ex = excluded(g_lo, g_hi, g)
        out[f"excludes {name}"] = ex["by_lower_bound"] or ex["by_upper_bound"]
        out[f"excludes {name} (how)"] = ex
    if g_lo is g_hi:
        out["value"] = cgt.show(g_lo)
        try:
            out["mean"] = str(cgt.mean(g_lo))
            t = cgt.temperature(g_lo)
            out["temperature"] = "number" if t is None else str(t)
        except Exception as e:  # pragma: no cover
            out["thermo_error"] = repr(e)
    return out


def resolve_all(T: Terminals, s: Searcher, ext: int, deepen_fn, log=None):
    """Real-chess results (White's view) of every terminal, both sides to move."""
    raw, how = {}, {}
    for i, t in enumerate(T.order):
        res = []
        for side in "WB":
            pos = T.real_pos(t, side)
            errs = mg.validity_errors(pos)
            if errs:
                res.append(None)
                how[(t, side)] = "illegal: " + "; ".join(errs)
                continue
            if pos.men() <= 7:
                iv = s.search(pos, 0)
                src = "tablebase (<=7 men)"
            else:
                iv = deepen_fn(s, pos, ext)
                src = f"search (8 men, ext<={ext})"
            if iv[0] == iv[1]:
                res.append(iv[0] if pos.stm == mg.WHITE else -iv[0])
                how[(t, side)] = src
            else:
                res.append(None)
                how[(t, side)] = src + " -> unresolved " + str(tuple(iv))
        raw[t] = tuple(res)
        if log and (i + 1) % 100 == 0:
            log(f"[oracle-all] {i + 1}/{len(T.order)} terminals")
    return raw, how


def stage_oracle_all(args, build):
    """Resolve EVERY terminal as far as the oracle allows (use --offline to
    stay inside the cache), then report bounds, pins and exclusions."""
    from .solve_candidate import RESULTS, write_json, tag_of, comp_str, make_order, deepen
    comp, model, oracle, cached, region = build(args)
    T = Terminals(comp)
    s = Searcher(oracle, mode=args.mode, order_hint=make_order(model, cached), region=region,
                 cached=cached, kb=oracle.kb)
    if args.use_l8:
        s.kb_max_men = 8
    t0 = time.time()
    status = "complete"
    path = os.path.join(RESULTS, f"{tag_of(comp)}_oracleall_{args.mode}{args.label}.json")
    if args.resume and os.path.exists(path):
        # re-analyse saved results (no search, no network)
        old = json.load(open(path))
        byname = {str(t): t for t in T.terms}
        raw, how = {}, {}
        for r in old["terminals"]:
            t = byname[r["terminal"]]
            raw[t] = (r["real_W_first"], r["real_B_first"])
            how[(t, "W")], how[(t, "B")] = r["how_W"], r["how_B"]
        status = "re-analysed from " + os.path.basename(path)
    else:
        try:
            raw, how = resolve_all(T, s, args.ext, deepen, log=lambda m: print(m, flush=True))
        except CapReached as e:
            raise SystemExit(f"stopped: {e} (re-run; results so far are cached)")
    passed_rule = "e.p.-aware" if getattr(pawns, "PASSED_RESPECTS_EP", False) else "textbook"
    targets = {"*2": cgt.nimber(2), "0": cgt.ZERO}
    # the model values (cylcgt) of this component, as comparison targets
    mvals = {}
    for rule in ("count", "mover", "opponent"):
        old = pawns.RACE_RULE
        pawns.RACE_RULE = rule
        pawns._value.cache_clear()
        try:
            mvals[rule] = pawns.value(T.board, comp)
        finally:
            pawns.RACE_RULE = old
            pawns._value.cache_clear()
        targets[f"model value under {rule} ({cgt.show(mvals[rule])})"] = mvals[rule]
    rows = []
    for t in T.order:
        rw, rb = raw[t]
        cls = class_of(rw, rb) if rw is not None and rb is not None else None
        if cls == "D":
            cls = "draw(" + ",".join(f"{s_}-first:{ {1: 'W wins', 0: 'draw', -1: 'B wins'}[v]}"
                                     for s_, v in (("W", rw), ("B", rb))) + ")"
        rows.append({"terminal": str(t), "men": T.men(t), "entered_by": sorted(T.movers[t]),
                     "race": pawns.passed(T.board, t, "W") and pawns.passed(T.board, t, "B"),
                     "model_by_rule": {rule: sorted({("L" if C.model_terminal_value(T.board, t, m, rule) > 0
                                                      else "R") for m in T.movers[t]})
                                       for rule in ("count", "mover", "opponent")},
                     "real_W_first": rw, "real_B_first": rb, "real_class": cls,
                     "how_W": how.get((t, "W")), "how_B": how.get((t, "B")),
                     "fen_W": mg.normal_fen(T.real_pos(t, "W")),
                     "fen_B": mg.normal_fen(T.real_pos(t, "B"))})
    full = [r for r in rows if r["real_class"]]
    out = {"component": comp_str(comp), "passed_test": passed_rule, "mode": args.mode,
           "ext": args.ext, "uses_lichess_8man_categories": bool(args.use_l8),
           "offline": bool(args.offline), "status": status,
           "internal_nodes": len(T.internal), "terminals_total": len(T.terms),
           "terminals_by_men": dict(Counter(T.men(t) for t in T.terms)),
           "sides_resolved": sum((r["real_W_first"] is not None) + (r["real_B_first"] is not None)
                                 for r in rows),
           "terminals_resolved_both_sides": len(full),
           "terminals_partial": sum(1 for r in rows if (r["real_W_first"] is None) != (r["real_B_first"] is None)),
           "terminals_unresolved": sum(1 for r in rows if r["real_W_first"] is None and r["real_B_first"] is None),
           "class_counts": dict(Counter(("D" if r["real_class"].startswith("draw") else r["real_class"])
                                        for r in full)),
           "non_LR_terminals": [r for r in full if r["real_class"] not in ("L", "R")],
           "LR_terminals_disagreeing_with_model": {
               rule: [r["terminal"] for r in full if r["real_class"] in ("L", "R")
                      and r["model_by_rule"][rule] != [r["real_class"]]]
               for rule in ("count", "mover", "opponent")},
           "model_values": {rule: cgt.show(g) for rule, g in mvals.items()},
           "new_requests": oracle.new_requests, "kb_hits": s.kb_hits,
           "seconds": round(time.time() - t0, 1)}
    out["bounds"] = {}
    for name, (kind, d) in TREATMENTS.items():
        g_lo, g_hi = sandwich(T, raw, kind, d)
        b = describe_bounds(g_lo, g_hi, targets)
        amb = ambiguous_partials(T, raw, kind, d)
        b["ambiguous_partial_terminals"] = len(amb)
        # exact enumeration over the ambiguous partials, when few enough
        for tname, tg in targets.items():
            if b[f"excludes {tname}"] or not amb:
                continue
            ok, n = enum_certificate(T, raw, tg, kind, d, amb)
            b[f"excludes {tname} (enumerating {len(amb)} ambiguous partials, {n} combinations)"] = ok
        out["bounds"][name] = b
    # indicative only: unresolved sides filled with the cylcgt model's verdict (count rule)
    prior = {}
    for t in T.terms:
        m = next(iter(T.movers[t]))
        prior[t] = C.model_terminal_value(T.board, t, m, "count")
    fill = {t: tuple(v if v is not None else prior[t] for v in raw[t]) for t in T.terms}
    for name, (kind, d) in TREATMENTS.items():
        if kind == "free":
            continue
        g = T.value(lambda t: pair_game(*fill[t], kind, d))
        out["bounds"][name]["indicative_value_unresolved_sides_from_model"] = cgt.show(g)
    out["terminals"] = rows
    if not args.dry_run:
        write_json(path, out)
    brief = {k: v for k, v in out.items() if k not in ("terminals", "non_LR_terminals")}
    brief["non_LR_terminals"] = [(r["terminal"], r["real_class"]) for r in out["non_LR_terminals"]]
    print(json.dumps(brief, indent=1, default=str))
    return out
