#!/usr/bin/env python3
"""K5b: check cylcgt's pawn-endgame values by playing  G - V  with sumtest/sumsolver.py.

    G = V   iff   G + (-V) is a second-player win (outcome P).

No canonical forms are used on the checking side.  Every V is built from its definition with
Trees.node / Trees.add / Trees.neg.  cylcgt is imported only to (a) read the value cylcgt assigns to a
position and (b) convert that value to a Trees node by walking its Left/Right option lists (attributes
.L and .R, nothing else).  cylcgt.cgt.show is used for display only.

Sub-commands (run from the project root with PYTHONPATH=.):
    sanity   -> sanity.txt         (exit 1 if a required check fails)
    run      -> results.jsonl      (one line per target x setting x mode; resumable)
    tables   -> claims.tsv, claims_literal_up2star.tsv, cylcgt.tsv, summary.json
    controls -> controls.tsv       (non-vacuity: G - V' for decoy values V')
    guardtest-> guardtest.txt      (self-test of the SIGALRM memory / wall-clock watchdog)

`run` is resumable: it skips every item already in results.jsonl.  run.sh deletes results.jsonl first, so
run.sh always recomputes from scratch.  The field proc_peak_rss_mb in results.jsonl is the high-water mark
of this process (getrusage ru_maxrss) after the solve, so it never decreases from one record to the next.
"""
import gc
import json
import os
import resource
import signal
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.setrecursionlimit(1_000_000)

from sumtest.sumsolver import Geometry, Rules, SumSolver, Trees      # noqa: E402

RESULTS = os.path.join(HERE, "results.jsonl")
SANITY = os.path.join(HERE, "sanity.txt")

ITEM_TIMEOUT = 300.0        # seconds per target x setting x mode (brief: 5 minutes)
RSS_LIMIT_KB = 2_600_000    # watchdog, below the 3 GB budget
BIG_SKIP = 64               # skip pairs whose V_cyl contains an integer of |n| >= 64

EPMODES = ("off", "textbook", "aware")
RACES = ("count", "mover", "opponent")
SETTINGS = [(e, r) for e in EPMODES for r in RACES]
MODES = ("whole", "comp")


# ---------------------------------------------------------------------------
# Values, from their definitions
# ---------------------------------------------------------------------------

class Vals:
    """Builds every named game inside one Trees object (definitions only)."""

    def __init__(self, T):
        self.T = T
        self._int = {}
        z = self.zero = T.node()
        self.star = T.node([z], [z])
        self.star2 = T.node([z, self.star], [z, self.star])
        self.up = T.node([z], [self.star])
        self.down = T.node([self.star], [z])
        self.downstar = T.add(self.down, self.star)                # explicit sum
        self.up2 = T.node([z], [self.downstar])                    # {0 | down*}
        self.up2star = T.add(self.up2, self.star)                  # explicit sum up2 + *
        self.up2star_lit = T.node([z, self.star], [self.down])     # literal {0,* | down}
        self.half = T.node([z], [self.integer(1)])
        self.quarter = T.node([z], [self.half])
        self.eighth = T.node([z], [self.quarter])
        self.sixteenth = T.node([z], [self.eighth])
        self.tiny1 = T.node([z], [T.node([z], [self.integer(-1)])])        # {0 || 0 | -1}
        self.sw = T.node([T.node([self.integer(3)], [self.integer(1)])],   # {2+-1 | -2+-1}
                         [T.node([self.integer(-1)], [self.integer(-3)])])

    def integer(self, n):
        """n = {n-1 | },  -n = { | -n+1}."""
        if n not in self._int:
            if n == 0:
                self._int[n] = self.T.node()
            elif n > 0:
                self._int[n] = self.T.node([self.integer(n - 1)], [])
            else:
                self._int[n] = self.T.node([], [self.integer(n + 1)])
        return self._int[n]

    def named(self, name):
        return {
            "0": self.zero, "*": self.star, "*2": self.star2, "up": self.up, "down": self.down,
            "down*": self.downstar, "up2": self.up2, "up2*": self.up2star,
            "up2*[literal]": self.up2star_lit, "1/2": self.half, "1/4": self.quarter,
            "1/8": self.eighth, "1/16": self.sixteenth, "tiny1": self.tiny1, "sw": self.sw,
            "1": self.integer(1), "2": self.integer(2), "3": self.integer(3),
            "-1": self.integer(-1), "-2": self.integer(-2), "-3": self.integer(-3),
        }[name]


CLAIM_LABEL = {   # how a claimed value is printed in the tables
    "0": "0", "*2": "*2", "1/8": "1/8", "1/16": "1/16", "up2": "up2", "up2*": "up2*",
    "tiny1": "tiny(1)", "sw": "{2+-1|-2+-1}",
}


# ---------------------------------------------------------------------------
# Targets and claims
# ---------------------------------------------------------------------------

TARGETS = {
    1: ("flat", 8, False, "W: a2 a3 b2 / B: a6 b5 b6"),
    2: ("flat", 8, False, "W: a2 b2 b3 / B: a5 a6 b6"),
    3: ("flat", 8, False, "W: a2 b4 c4 / B: a7 b7 d6"),
    4: ("flat", 8, False, "W: a2 b2 c3 / B: b5 b6 c7"),
    5: ("flat", 8, False, "W: a2 b2 d4 / B: a7 c6 d7"),
    6: ("flat", 8, False, "W: a2 b2 b6 / B: a6 b7 c5"),
    7: ("flat", 8, False, "W: a2 b2 b6 / B: a6 b7 c6"),
    8: ("flat", 8, False, "W: a2 c2 / B: b7 d7"),
    9: ("cyl", 3, True, "W: a2 a3 b2 / B: b7 c6 c7"),
}


def claims():
    """(target, epmode, race) -> claimed value name."""
    c = {}
    for t, v in ((1, "1/8"), (2, "1/8"), (6, "up2*")):
        for s in SETTINGS:
            c[(t,) + s] = v
    c[(3, "aware", "count")] = "1/8"
    c[(4, "aware", "count")] = "1/16"
    c[(5, "aware", "count")] = "up2"
    c[(7, "aware", "count")] = "tiny1"
    for e in ("off", "textbook"):
        c[(8, e, "count")] = "*2"
        c[(8, e, "mover")] = "*2"
        c[(8, e, "opponent")] = "0"
    c[(8, "aware", "count")] = "sw"
    c[(9, "aware", "count")] = "*2"
    return c


CLAIMS = claims()


# ---------------------------------------------------------------------------
# Solver construction
# ---------------------------------------------------------------------------

def make_rules(geo, epmode, race):
    if epmode == "off":
        return Rules(geo, ep=False, ep_aware=True, race_rule=race, race_double=True)
    if epmode == "textbook":
        return Rules(geo, ep=True, ep_aware=False, race_rule=race, race_double=True)
    if epmode == "aware":
        return Rules(geo, ep=True, ep_aware=True, race_rule=race, race_double=True)
    raise ValueError(epmode)


class Abort(Exception):
    pass


def max_rss_kb():
    """High-water RSS of this process in KB (getrusage: bytes on macOS, KB on Linux)."""
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r // 1024 if sys.platform == "darwin" else r


class Guard:
    """SIGALRM watchdog on this process only: wall-clock limit and RSS limit (checked every `interval` s)."""

    def __init__(self, seconds, interval=3.0):
        self.seconds = seconds
        self.interval = interval
        self.t0 = time.time()
        self.reason = None

    def _handler(self, signum, frame):
        if time.time() - self.t0 > self.seconds:
            self.reason = "timeout"
            raise Abort("timeout")
        if max_rss_kb() > RSS_LIMIT_KB:
            self.reason = "memory"
            raise Abort("memory")

    def __enter__(self):
        self._old = signal.signal(signal.SIGALRM, self._handler)
        signal.setitimer(signal.ITIMER_REAL, self.interval, self.interval)
        return self

    def __exit__(self, *a):
        signal.setitimer(signal.ITIMER_REAL, 0, 0)
        signal.signal(signal.SIGALRM, self._old)
        return False


def solve_nodes(geo, rules, T, text, mode, labels, seconds=ITEM_TIMEOUT):
    """Outcome of G + node for each (label -> node) with the solver in `mode`.
    T must already contain every node (the solver precomputes masks at construction)."""
    W, B = geo.parse(text)
    hits0 = rules.race_hits
    solver = SumSolver(rules, T, mode=mode, ep_scope="component")
    t0 = time.time()
    status, out = "ok", {}
    guard = Guard(seconds)
    try:
        with guard:
            wl, wr = solver.solve(solver.start_state(W, B))
        out = {lab: SumSolver.outcome(wl, wr, k) for lab, k in labels.items()}
    except Abort:
        status = guard.reason or "abort"
    except RecursionError:
        status = "recursion"
    info = {"status": status, "secs": round(time.time() - t0, 2), "states": solver.nodes,
            "race_hits": rules.race_hits - hits0, "proc_peak_rss_mb": round(max_rss_kb() / 1024, 1),
            "outcomes": out}
    del solver
    gc.collect()
    return info


# ---------------------------------------------------------------------------
# Sanity
# ---------------------------------------------------------------------------

def sanity():
    """Required checks (brief) plus controls.  G0 = 'W: a4 / B: a5' on the flat board has no moves."""
    geo = Geometry(8, False)
    text = "W: a4 / B: a5"
    T = Trees()
    V = Vals(T)
    zero = V.zero
    checks = []     # (group, name, node, expected or None)

    def P(name, node, group="required"):
        checks.append((group, name, node, "P"))

    for name in ("1", "2", "3", "-1", "-2", "-3", "1/2", "1/4", "1/8", "1/16", "*", "*2", "up", "down",
                 "down*", "up2", "up2*", "up2*[literal]", "tiny1", "sw"):
        v = V.named(name)
        P(f"V + (-V) is P, V = {name}", T.add(v, T.neg(v)))
    P("1/8 + 1/8 + (-1/4) is P", T.add(T.add(V.eighth, V.eighth), T.neg(V.quarter)))
    checks.append(("required", "up2 is L", V.up2, "L"))
    checks.append(("required", "up - up2 is L", T.add(V.up, T.neg(V.up2)), "L"))
    checks.append(("required", "tiny(1) is L", V.tiny1, "L"))
    checks.append(("record", "up2 - tiny(1) (no expected answer)", T.add(V.up2, T.neg(V.tiny1)), None))
    P("*2 + *2 is P", T.add(V.star2, V.star2))
    P("G + G is P, G = {2+-1 | -2+-1}", T.add(V.sw, V.sw))
    # controls: distinct games must be told apart (the test is not vacuous)
    P("control: 0 is P", zero, "control")
    P("control: 1/2 + 1/2 - 1 is P", T.add(T.add(V.half, V.half), V.integer(-1)), "control")
    P("control: 1/16 + 1/16 - 1/8 is P", T.add(T.add(V.sixteenth, V.sixteenth), T.neg(V.eighth)), "control")
    checks.append(("control", "control: 1/8 - 1/16 is L", T.add(V.eighth, T.neg(V.sixteenth)), "L"))
    checks.append(("control", "control: 1/16 - 1/8 is R", T.add(V.sixteenth, T.neg(V.eighth)), "R"))
    checks.append(("control", "control: * is N", V.star, "N"))
    checks.append(("control", "control: *2 - * is N", T.add(V.star2, T.neg(V.star)), "N"))
    checks.append(("control", "control: up + * is N", T.add(V.up, V.star), "N"))
    checks.append(("control", "control: up2* - up2 (= *) is N", T.add(V.up2star, T.neg(V.up2)), "N"))
    checks.append(("control", "control: 1/8 - 1/4 is R", T.add(V.eighth, T.neg(V.quarter)), "R"))
    checks.append(("control", "control: 2 - 3 is R", T.add(V.integer(2), T.neg(V.integer(3))), "R"))
    # the two presentations of up2*
    checks.append(("info", "up2*[literal {0,*|down}] - up2*[up2 + *] (P means equal)",
                   T.add(V.up2star_lit, T.neg(V.up2star)), None))
    checks.append(("info", "up2*[literal] outcome", V.up2star_lit, None))
    checks.append(("info", "up2*[sum] outcome", V.up2star, None))

    labels = {f"{i}": c[2] for i, c in enumerate(checks)}
    res = {}
    for setting in SETTINGS:
        rules = make_rules(geo, *setting)
        for mode in MODES:
            res[(setting, mode)] = solve_nodes(geo, rules, T, text, mode, labels, seconds=120)
    ok_all = True
    lines = ["K5b sanity checks: G0 = 'W: a4 / B: a5' (flat 8x8, no moves for either side) plus an explicit tree.",
             f"Trees nodes: {len(T)}.  Each check is run in both modes under all 9 settings "
             f"(G0 has no moves, so the settings cannot matter; any difference would be a solver bug).", ""]
    for group in ("required", "control", "record", "info"):
        lines.append(f"== {group} ==")
        for i, (g, name, node, exp) in enumerate(checks):
            if g != group:
                continue
            outs = {}
            for setting in SETTINGS:
                for mode in MODES:
                    info = res[(setting, mode)]
                    outs[(setting, mode)] = info["outcomes"].get(str(i), "?") if info["status"] == "ok" else info["status"]
            whole = {o for (s, m), o in outs.items() if m == "whole"}
            comp = {o for (s, m), o in outs.items() if m == "comp"}
            allv = whole | comp
            shown = f"whole={'/'.join(sorted(whole))} comp={'/'.join(sorted(comp))}"
            if exp is None:
                verdict = "INFO"
            else:
                good = allv == {exp}
                verdict = "PASS" if good else "FAIL"
                if g in ("required", "control") and not good:
                    ok_all = False
            exps = f"expected={exp}" if exp else "expected=-"
            lines.append(f"{verdict:5s} {name:68s} {exps:12s} {shown}")
        lines.append("")
    lines.append("ALL REQUIRED AND CONTROL CHECKS PASSED" if ok_all else "SANITY FAILED")
    with open(SANITY, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return ok_all


# ---------------------------------------------------------------------------
# cylcgt side: read a value, convert by walking .L / .R only
# ---------------------------------------------------------------------------

def cyl_value(tkey, epmode, race):
    """Return (shown, root) for cylcgt's value of the target position under the setting."""
    from cylcgt import cgt, pawns
    kind, files, wrap, text = TARGETS[tkey]
    pawns.RACE_RULE = race
    pawns.PASSED_RESPECTS_EP = (epmode != "textbook")       # off: irrelevant (no e.p. rights arise)
    board = pawns.Board(files, 8, wrap, epmode != "off")
    pawns._value.cache_clear()
    try:
        root = pawns.value(board, pawns.Pos.parse(text))
        return cgt.show(root), root, None
    except Exception as e:                                   # RaceError etc.
        return None, None, f"{type(e).__name__}: {e}"


def int_chain(g, memo):
    """Structural: n if g is the integer chain {n-1|} / {|n+1} / {|}, else None (no tags used)."""
    k = id(g)
    if k in memo:
        return memo[k]
    L, R = g.L, g.R
    r = None
    if not L and not R:
        r = 0
    elif len(L) == 1 and not R:
        c = int_chain(L[0], memo)
        r = c + 1 if (c is not None and c >= 0) else None
    elif len(R) == 1 and not L:
        c = int_chain(R[0], memo)
        r = c - 1 if (c is not None and c <= 0) else None
    memo[k] = r
    return r


def max_integer(root):
    """Largest |n| over all sub-games that are pure integer chains (structural walk of .L/.R)."""
    memo, seen, best = {}, set(), 0
    stack = [root]
    while stack:
        g = stack.pop()
        if id(g) in seen:
            continue
        seen.add(id(g))
        c = int_chain(g, memo)
        if c is not None:
            best = max(best, abs(c))
            continue            # an integer chain has no other structure below it
        stack.extend(g.L)
        stack.extend(g.R)
    return best, len(seen)


def convert(root, T):
    """cylcgt Game -> Trees node, by walking Left/Right option lists only."""
    memo = {}

    def go(g):
        k = id(g)
        if k not in memo:
            memo[k] = T.node([go(x) for x in g.L], [go(x) for x in g.R])
        return memo[k]
    return go(root)


# ---------------------------------------------------------------------------
# Main run: pass 1 (claims) and pass 2 (cylcgt's value) share one solve per target x setting x mode,
# because the masks are independent per tree node.
# ---------------------------------------------------------------------------

def done_keys():
    done = set()
    if os.path.exists(RESULTS):
        for line in open(RESULTS):
            r = json.loads(line)
            if r["status"] in ("ok", "timeout", "memory", "recursion"):
                done.add((r["target"], r["epmode"], r["race"], r["mode"]))
    return done


def run(deadline_min=None):
    t_start = time.time()
    done = done_keys()
    order = [(t, e, r) for t in TARGETS for (e, r) in SETTINGS]
    order.sort(key=lambda k: (0 if k in CLAIMS else 1, k[0]))       # items carrying a claim first
    for (t, e, r) in order:
        if all((t, e, r, m) in done for m in MODES):
            continue
        if deadline_min and (time.time() - t_start) / 60 > deadline_min:
            print("budget exhausted; stopping", flush=True)
            break
        kind, files, wrap, text = TARGETS[t]
        geo = Geometry(files, wrap)
        rules = make_rules(geo, e, r)
        T = Trees()
        V = Vals(T)
        labels = {}
        claim = CLAIMS.get((t, e, r))
        if claim is not None:
            labels["claim"] = T.neg(V.named(claim))
            if claim == "up2*":
                labels["claim_literal"] = T.neg(V.up2star_lit)
        shown, root, err = cyl_value(t, e, r)
        skip_reason, max_int = None, None
        if root is None:
            skip_reason = f"cylcgt raised {err}"
        else:
            max_int, _ = max_integer(root)
            if max_int >= BIG_SKIP:
                skip_reason = f"V_cyl contains integer of absolute value {max_int} (>= {BIG_SKIP})"
            else:
                labels["cyl"] = T.neg(convert(root, T))
        for mode in MODES:
            if (t, e, r, mode) in done:
                continue
            info = solve_nodes(geo, rules, T, text, mode, labels)
            rec = {"target": t, "epmode": e, "race": r, "mode": mode, "position": text,
                   "claim": claim, "cyl_shown": shown, "cyl_skip": skip_reason, "cyl_max_int": max_int,
                   "tree_nodes": len(T)}
            rec.update(info)
            with open(RESULTS, "a") as f:
                f.write(json.dumps(rec) + "\n")
            print(f"t{t} {e}/{r} {mode}: {info['status']} {info['secs']}s states={info['states']} "
                  f"claim={claim} cyl={shown} {info['outcomes']}", flush=True)
        del T, V
        gc.collect()


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------

def load_results():
    res = {}
    for line in open(RESULTS):
        r = json.loads(line)
        res[(r["target"], r["epmode"], r["race"], r["mode"])] = r      # last record wins
    return res


def cell(rec, label):
    if rec is None:
        return "not-run"
    if rec["status"] != "ok":
        return rec["status"]
    return rec["outcomes"].get(label, "-")


def confirmed(o_whole, o_comp):
    if o_whole == "P" and o_comp == "P":
        return "yes"
    return "no"


def tables():
    res = load_results()
    summary = {"claims_tested": 0, "claims_confirmed": 0, "claim_non_P": [],
               "cyl_tested": 0, "cyl_confirmed": 0, "cyl_skipped": [], "cyl_non_P": [], "cyl_not_run": [],
               "mode_disagreements": [], "claims_not_run": []}
    with open(os.path.join(HERE, "claims.tsv"), "w") as f, \
            open(os.path.join(HERE, "claims_literal_up2star.tsv"), "w") as g:
        hdr = "target\tsetting\tclaim\twhole\tcomp\tconfirmed\tmodes_differ\n"
        f.write(hdr)
        g.write("target\tsetting\tclaim\twhole\tcomp\tconfirmed\tmodes_differ\tsame_as_sum_form\n")
        for (t, e, r), v in sorted(CLAIMS.items()):
            w, c = res.get((t, e, r, "whole")), res.get((t, e, r, "comp"))
            ow, oc = cell(w, "claim"), cell(c, "claim")
            conf = confirmed(ow, oc)
            diff = "yes" if ow != oc else "no"
            f.write(f"{t}\t{e}/{r}\t{CLAIM_LABEL[v]}\t{ow}\t{oc}\t{conf}\t{diff}\n")
            summary["claims_tested"] += 1
            if "not-run" in (ow, oc):
                summary["claims_not_run"].append(f"T{t} {e}/{r}")
            if conf == "yes":
                summary["claims_confirmed"] += 1
            else:
                summary["claim_non_P"].append(f"T{t} {e}/{r} claim {CLAIM_LABEL[v]}: whole={ow} comp={oc}")
            if ow != oc:
                summary["mode_disagreements"].append(f"claim T{t} {e}/{r}: whole={ow} comp={oc}")
            if v == "up2*":
                lw, lc = cell(w, "claim_literal"), cell(c, "claim_literal")
                same = "yes" if (lw, lc) == (ow, oc) else "no"
                g.write(f"{t}\t{e}/{r}\t{{0,*|down}}\t{lw}\t{lc}\t{confirmed(lw, lc)}\t"
                        f"{'yes' if lw != lc else 'no'}\t{same}\n")
    with open(os.path.join(HERE, "cylcgt.tsv"), "w") as f:
        f.write("target\tsetting\tcylcgt_value\twhole\tcomp\tconfirmed\tmodes_differ\tnote\n")
        for t in TARGETS:
            for (e, r) in SETTINGS:
                w, c = res.get((t, e, r, "whole")), res.get((t, e, r, "comp"))
                rec = w or c
                if rec is None:
                    summary["cyl_not_run"].append(f"T{t} {e}/{r}")
                    f.write(f"{t}\t{e}/{r}\t?\tnot-run\tnot-run\tnot-run\t-\tnot run\n")
                    continue
                shown = rec["cyl_shown"] or "(none)"
                if rec["cyl_skip"]:
                    summary["cyl_skipped"].append(f"T{t} {e}/{r}: {rec['cyl_skip']}")
                    f.write(f"{t}\t{e}/{r}\t{shown}\t-\t-\tskipped\t-\t{rec['cyl_skip']}\n")
                    continue
                ow, oc = cell(w, "cyl"), cell(c, "cyl")
                conf = confirmed(ow, oc)
                diff = "yes" if ow != oc else "no"
                note = ""
                if "not-run" in (ow, oc):
                    summary["cyl_not_run"].append(f"T{t} {e}/{r}")
                    note = "not run"
                elif ow in ("timeout", "memory", "recursion") or oc in ("timeout", "memory", "recursion"):
                    note = "solver aborted (limit)"
                summary["cyl_tested"] += 1
                if conf == "yes":
                    summary["cyl_confirmed"] += 1
                else:
                    summary["cyl_non_P"].append(f"T{t} {e}/{r} cylcgt={shown}: whole={ow} comp={oc}")
                if ow != oc:
                    summary["mode_disagreements"].append(f"cylcgt T{t} {e}/{r} ({shown}): whole={ow} comp={oc}")
                f.write(f"{t}\t{e}/{r}\t{shown}\t{ow}\t{oc}\t{conf}\t{diff}\t{note}\n")
    with open(os.path.join(HERE, "summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print(json.dumps(summary, indent=1))


DECOYS = ["0", "*", "*2", "up", "down", "up2", "up2*", "tiny1", "1/16", "1/8", "1/4", "1/2", "1", "2", "sw",
          "-1/16", "-1/8", "-1/2", "-1"]


def controls():
    """Non-vacuity: for every target (aware / count) play G - V' for a list of decoy values V'.  The claimed
    value should be the only P (up to equal games); every other decoy should be L, R or N."""
    rows = ["target\tposition\tmode\tclaimed\tP_decoys\tnon_P_decoys"]
    lines = []
    for t, (kind, files, wrap, text) in TARGETS.items():
        geo = Geometry(files, wrap)
        rules = make_rules(geo, "aware", "count")
        T = Trees()
        V = Vals(T)
        labels = {}
        for d in DECOYS:
            v = T.neg(V.named(d[1:])) if d.startswith("-") else V.named(d)      # decoy value V'
            labels[d] = T.neg(v)                                               # G + (-V')
        for mode in MODES:
            info = solve_nodes(geo, rules, T, text, mode, labels)
            o = info["outcomes"]
            ps = [d for d in DECOYS if o.get(d) == "P"]
            rest = " ".join(f"{d}:{o.get(d)}" for d in DECOYS if o.get(d) != "P")
            claimed = CLAIM_LABEL.get(CLAIMS.get((t, "aware", "count")), "-")
            rows.append(f"{t}\t{text}\t{mode}\t{claimed}\t{','.join(ps) or 'none'}\t{rest}")
    with open(os.path.join(HERE, "controls.tsv"), "w") as f:
        f.write("\n".join(rows) + "\n")
    print("\n".join(rows))


def guardtest():
    """The solves are all far shorter than the watchdog's 3 s tick, so the watchdog never fires in a real run.
    Exercise it here on a busy loop: (a) RSS limit forced below the current RSS, (b) wall-clock limit of 0 s."""
    global RSS_LIMIT_KB
    saved = RSS_LIMIT_KB
    lines = [f"watchdog self-test (tick 0.5 s).  ru_maxrss now = {max_rss_kb()} KB; run-time limit RSS_LIMIT_KB = {saved} KB."]
    ok = True
    for name, seconds, rss_limit, expect in (("memory limit below current RSS", 300.0, 1, "memory"),
                                              ("wall-clock limit 0 s", 0.0, saved, "timeout"),
                                              ("no limit hit (control)", 300.0, saved, None)):
        RSS_LIMIT_KB = rss_limit
        guard = Guard(seconds, interval=0.5)
        t0 = time.time()
        try:
            with guard:
                while time.time() - t0 < 2.0:
                    pass
            got = None
        except Abort:
            got = guard.reason
        RSS_LIMIT_KB = saved
        good = got == expect
        ok &= good
        lines.append(f"{'PASS' if good else 'FAIL'}  {name}: aborted with {got!r} after {time.time() - t0:.1f} s (expected {expect!r})")
    lines.append("WATCHDOG SELF-TEST PASSED" if ok else "WATCHDOG SELF-TEST FAILED")
    with open(os.path.join(HERE, "guardtest.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return ok


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "sanity":
        sys.exit(0 if sanity() else 1)
    elif cmd == "run":
        if not os.path.exists(SANITY) or "ALL REQUIRED AND CONTROL CHECKS PASSED" not in open(SANITY).read():
            sys.exit("sanity.txt missing or failing; run `identities.py sanity` first")
        run(deadline_min=float(sys.argv[2]) if len(sys.argv) > 2 else None)
    elif cmd == "tables":
        tables()
    elif cmd == "controls":
        controls()
    elif cmd == "guardtest":
        sys.exit(0 if guardtest() else 1)
    else:
        sys.exit(__doc__)
