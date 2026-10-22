#!/usr/bin/env python3
"""Independent audit of K5b.  Written from the brief (kings/delegate/briefs/K5b_sumsolver_identities.md) and
sumtest/sumsolver.py only; it does not import or copy kings/delegate/out/K5b/identities.py.

Run from the project root:
    PYTHONPATH=. nice -n 10 .venv/bin/python kings/delegate/out/K5b/audit/audit_k5b.py [outdir]

What it does
  A. Builds every V from its definition with a small string parser on top of Trees.node / Trees.add / Trees.neg
     (so each tree is literally the brief's text, e.g. '{0|{0|-1}}').
  B. Evaluates the sanity facts with its OWN lazy-sum outcome evaluator (components kept separate, negation as a
     sign flag), so Trees.add / Trees.neg are not trusted either.
  C. Recomputes the sanity table with sumsolver, G0 = 'W: a4 / B: a5', all 9 settings x both modes.
  D. Pass 1: 39 claims x both modes.  Compared with claims.tsv.
  E. Cross-checks that the settings are wired the right way round (a claim must FAIL under the wrong setting
     wherever the brief says the value differs).
  F. Pass 2: cylcgt's value at all 81 pairs, converted via .L/.R tuples only.  Compared with cylcgt.tsv.
  G. Diagnostics: tag-vs-structure agreement of cylcgt integers, integer-size distribution, 'off' invariances.
"""
import os
import re
import signal
import sys
import time
from functools import lru_cache

sys.setrecursionlimit(1_000_000)
from sumtest.sumsolver import Geometry, Rules, SumSolver, Trees     # noqa: E402

ROOT = os.getcwd()
K5B = os.path.join(ROOT, "kings/delegate/out/K5b")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(K5B, "audit")
os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(OUT, "audit_out.txt"), "w")


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


# ---------------------------------------------------------------------------------------------------------
# A. Parser for the brief's definitions
# ---------------------------------------------------------------------------------------------------------
DEFS = {
    "star": "{0|0}",
    "star2": "{0,star|0,star}",
    "up": "{0|star}",
    "down": "{star|0}",
    "downstar": "down+star",
    "up2": "{0|downstar}",
    "up2star": "up2+star",
    "up2starlit": "{0,star|down}",
    "h2": "{0|1}",
    "h4": "{0|h2}",
    "h8": "{0|h4}",
    "h16": "{0|h8}",
    "tiny1": "{0|{0|-1}}",
    "sw": "{{3|1}|{-1|-3}}",
}
ZERO = "0"


class Builder:
    TOK = re.compile(r"\s*(\d+|[A-Za-z_][A-Za-z0-9_]*|[{}|,+\-()])")

    def __init__(self, T):
        self.T = T
        self.memo = {}
        self.ints = {}

    def integer(self, n):
        if n not in self.ints:
            T = self.T
            if n == 0:
                self.ints[n] = T.node()
            elif n > 0:
                self.ints[n] = T.node([self.integer(n - 1)], [])
            else:
                self.ints[n] = T.node([], [self.integer(n + 1)])
        return self.ints[n]

    def __call__(self, text):
        if text in self.memo:
            return self.memo[text]
        toks = self.TOK.findall(text)
        assert "".join(toks) == re.sub(r"\s+", "", text), text
        self.toks, self.i = toks, 0
        v = self.expr()
        assert self.i == len(toks), text
        self.memo[text] = v
        return v

    # grammar: expr := ['-'] term (('+'|'-') term)* ; term := INT | NAME | '(' expr ')' | '{' list '|' list '}'
    def peek(self):
        return self.toks[self.i] if self.i < len(self.toks) else None

    def eat(self, t=None):
        x = self.toks[self.i]
        assert t is None or x == t, (t, x)
        self.i += 1
        return x

    def expr(self):
        T = self.T
        neg = False
        if self.peek() == "-":
            self.eat()
            neg = True
        v = self.term()
        if neg:
            v = T.neg(v)
        while self.peek() in ("+", "-"):
            op = self.eat()
            w = self.term()
            v = T.add(v, w if op == "+" else T.neg(w))
        return v

    def term(self):
        t = self.peek()
        if t.isdigit():
            self.eat()
            return self.integer(int(t))
        if t == "(":
            self.eat()
            v = self.expr()
            self.eat(")")
            return v
        if t == "{":
            self.eat()
            left = self.lst()
            self.eat("|")
            right = self.lst()
            self.eat("}")
            return self.T.node(left, right)
        # name
        self.eat()
        saved = (self.toks, self.i)
        v = self(DEFS[t])
        self.toks, self.i = saved
        return v

    def lst(self):
        out = []
        if self.peek() in ("|", "}"):
            return out
        out.append(self.expr())
        while self.peek() == ",":
            self.eat()
            out.append(self.expr())
        return out


# ---------------------------------------------------------------------------------------------------------
# B. Own lazy-sum outcome evaluator (components kept apart; sign -1 means "negative of this tree")
# ---------------------------------------------------------------------------------------------------------
class Lazy:
    def __init__(self, T):
        self.T = T
        self.fw = lru_cache(maxsize=None)(self._fw)

    def _fw(self, comps, left):
        T = self.T
        for i, (k, s) in enumerate(comps):
            if s > 0:
                opts = T.L[k] if left else T.R[k]
            else:
                opts = T.R[k] if left else T.L[k]
            rest = comps[:i] + comps[i + 1:]
            for c in opts:
                if not self.fw(tuple(sorted(rest + ((c, s),))), not left):
                    return True
        return False

    def outcome(self, comps):
        comps = tuple(sorted(comps))
        l, r = self.fw(comps, True), self.fw(comps, False)
        return {(True, False): "L", (False, True): "R", (True, True): "N", (False, False): "P"}[(l, r)]


# ---------------------------------------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------------------------------------
EPS = ("off", "textbook", "aware")
RACES = ("count", "mover", "opponent")
SETTINGS = [(e, r) for e in EPS for r in RACES]
MODES = ("whole", "comp")


def rules_for(geo, e, r, off_ep_aware=False):
    if e == "off":
        return Rules(geo, ep=False, ep_aware=off_ep_aware, race_rule=r, race_double=True)
    if e == "textbook":
        return Rules(geo, ep=True, ep_aware=False, race_rule=r, race_double=True)
    return Rules(geo, ep=True, ep_aware=True, race_rule=r, race_double=True)


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout()


def solve_all(geo, rules, T, text, labels, limit=300):
    """labels: name -> node.  Returns {mode: {name: outcome}}.  T must be complete before this call."""
    n0 = len(T)
    W, B = geo.parse(text)
    res = {}
    for mode in MODES:
        s = SumSolver(rules, T, mode=mode, ep_scope="component")
        signal.signal(signal.SIGALRM, _alarm)
        signal.alarm(limit)
        try:
            wl, wr = s.solve(s.start_state(W, B))
            res[mode] = {k: SumSolver.outcome(wl, wr, node) for k, node in labels.items()}
        except Timeout:
            res[mode] = {k: "timeout" for k in labels}
        finally:
            signal.alarm(0)
        assert len(T) == n0, "tree grew after SumSolver construction"
    return res


# ---------------------------------------------------------------------------------------------------------
# C. Sanity
# ---------------------------------------------------------------------------------------------------------
def sanity():
    say("=" * 100)
    say("C. SANITY  (own parser trees, G0 = 'W: a4 / B: a5', 9 settings x 2 modes) vs lazy evaluator vs sanity.txt")
    geo = Geometry(8, False)
    T = Trees()
    P = Builder(T)
    lazy = Lazy(T)
    # check list: (key, sanity.txt name, expr text, expected, kind)
    checks = []
    vs = [("1", "1"), ("2", "2"), ("3", "3"), ("-1", "-1"), ("-2", "-2"), ("-3", "-3"), ("1/2", "h2"),
          ("1/4", "h4"), ("1/8", "h8"), ("1/16", "h16"), ("*", "star"), ("*2", "star2"), ("up", "up"),
          ("down", "down"), ("down*", "downstar"), ("up2", "up2"), ("up2*", "up2star"),
          ("up2*[literal]", "up2starlit"), ("tiny1", "tiny1"), ("sw", "sw")]
    for nm, ex in vs:
        checks.append((f"V-V {nm}", f"V + (-V) is P, V = {nm}", f"({ex}) - ({ex})", "P"))
    checks += [
        ("1/8+1/8-1/4", "1/8 + 1/8 + (-1/4) is P", "h8+h8-h4", "P"),
        ("up2 L", "up2 is L", "up2", "L"),
        ("up-up2 L", "up - up2 is L", "up-up2", "L"),
        ("tiny L", "tiny(1) is L", "tiny1", "L"),
        ("up2-tiny", "up2 - tiny(1) (no expected answer)", "up2-tiny1", None),
        ("*2+*2", "*2 + *2 is P", "star2+star2", "P"),
        ("sw+sw", "G + G is P, G = {2+-1 | -2+-1}", "sw+sw", "P"),
        ("up2star lit vs sum", "up2*[literal {0,*|down}] - up2*[up2 + *] (P means equal)", "up2starlit-up2star", None),
        ("up2star lit", "up2*[literal] outcome", "up2starlit", None),
        ("up2star sum", "up2*[sum] outcome", "up2star", None),
    ]
    nodes = {k: P(ex) for k, _, ex, _ in checks}
    # extra independent checks of Trees.add / Trees.neg through the lazy evaluator
    extra = []
    for nm in ("star", "down", "up", "h8", "tiny1", "sw", "up2", "downstar"):
        x = P(nm)
        extra.append((f"neg({nm}) + {nm} is P (lazy)", lazy.outcome([(T.neg(x), 1), (x, 1)]), "P"))
    extra.append(("T.add(down,*) - down - * is P (lazy)",
                  lazy.outcome([(P("downstar"), 1), (P("down"), -1), (P("star"), -1)]), "P"))
    extra.append(("T.add(up2,*) - up2 - * is P (lazy)",
                  lazy.outcome([(P("up2star"), 1), (P("up2"), -1), (P("star"), -1)]), "P"))
    extra.append(("literal {0,*|down} - up2 - * is P (lazy)",
                  lazy.outcome([(P("up2starlit"), 1), (P("up2"), -1), (P("star"), -1)]), "P"))
    extra.append(("down* is down + * : lazy [down*, -down, -*] P", lazy.outcome([(P("downstar"), 1), (P("down"), -1), (P("star"), -1)]), "P"))
    # claims about the CGT identities themselves (lazy, independent of sumsolver):  1/8+1/8=1/4 etc.
    extra.append(("1/8+1/8-1/4 is P (lazy, components apart)",
                  lazy.outcome([(P("h8"), 1), (P("h8"), 1), (P("h4"), -1)]), "P"))
    extra.append(("up > up2 > 0: up - up2 is L (lazy)", lazy.outcome([(P("up"), 1), (P("up2"), -1)]), "L"))
    extra.append(("up2 > tiny1 > 0: up2 - tiny1 is L (lazy)", lazy.outcome([(P("up2"), 1), (P("tiny1"), -1)]), "L"))
    extra.append(("sw + sw is P (lazy, components apart)", lazy.outcome([(P("sw"), 1), (P("sw"), 1)]), "P"))
    extra.append(("*2 + *2 is P (lazy, components apart)", lazy.outcome([(P("star2"), 1), (P("star2"), 1)]), "P"))

    # sumsolver on G0 under all settings
    labels = {k: v for k, v in nodes.items()}
    table = {}
    W, B = geo.parse("W: a4 / B: a5")
    for e, r in SETTINGS:
        rules = rules_for(geo, e, r)
        assert not rules.moves(W, B, -1, True) and not rules.moves(W, B, -1, False)
        res = solve_all(geo, rules, T, "W: a4 / B: a5", labels)
        for mode in MODES:
            for k, o in res[mode].items():
                table.setdefault(k, {}).setdefault(mode, set()).add(o)
    # parse sanity.txt
    their = {}
    for line in open(os.path.join(K5B, "sanity.txt")):
        m = re.match(r"^(PASS|FAIL|INFO)\s+(.*?)\s+expected=(\S+)\s+whole=(\S+) comp=(\S+)\s*$", line)
        if m:
            their[m.group(2).strip()] = (m.group(1), m.group(3), m.group(4), m.group(5))
    bad = 0
    for key, nm, ex, exp in checks:
        w = "/".join(sorted(table[key]["whole"]))
        c = "/".join(sorted(table[key]["comp"]))
        lazy_o = lazy.outcome([(nodes[key], 1)])
        ok = (exp is None) or (w == exp and c == exp)
        t = their.get(nm)
        diff = ""
        if t is None:
            diff = "MISSING-IN-sanity.txt"
        elif (t[2], t[3]) != (w, c):
            diff = f"DIFF sanity.txt whole={t[2]} comp={t[3]}"
        if lazy_o not in (w, c) or w != c:
            diff += f" lazy={lazy_o}"
        bad += (not ok) + bool(diff)
        say(f"{'ok ' if ok else 'BAD'} {nm:68s} exp={exp or '-'} whole={w} comp={c} lazy={lazy_o} {diff}")
    for nm, got, exp in extra:
        ok = got == exp
        bad += not ok
        say(f"{'ok ' if ok else 'BAD'} {nm:68s} exp={exp} got={got}")
    say(f"sanity discrepancies (bad flags or differences vs sanity.txt): {bad}")
    n_sanity_lines = len([1 for k in their])
    say(f"sanity.txt check-lines parsed: {n_sanity_lines}; my required/record/info checks: {len(checks)}")
    return bad


# ---------------------------------------------------------------------------------------------------------
# D / E. Pass 1: claims
# ---------------------------------------------------------------------------------------------------------
TARGETS = {
    1: (8, False, "W: a2 a3 b2 / B: a6 b5 b6"),
    2: (8, False, "W: a2 b2 b3 / B: a5 a6 b6"),
    3: (8, False, "W: a2 b4 c4 / B: a7 b7 d6"),
    4: (8, False, "W: a2 b2 c3 / B: b5 b6 c7"),
    5: (8, False, "W: a2 b2 d4 / B: a7 c6 d7"),
    6: (8, False, "W: a2 b2 b6 / B: a6 b7 c5"),
    7: (8, False, "W: a2 b2 b6 / B: a6 b7 c6"),
    8: (8, False, "W: a2 c2 / B: b7 d7"),
    9: (3, True, "W: a2 a3 b2 / B: b7 c6 c7"),
}


def claim_table():
    """(target, ep, race) -> expression of the claimed V, straight from the brief's table."""
    c = {}
    allset = [(e, r) for e in EPS for r in RACES]
    for t, v in ((1, "h8"), (2, "h8"), (6, "up2star")):
        for s in allset:
            c[(t,) + s] = v
    c[(3, "aware", "count")] = "h8"
    c[(4, "aware", "count")] = "h16"
    c[(5, "aware", "count")] = "up2"
    c[(7, "aware", "count")] = "tiny1"
    for e in ("off", "textbook"):
        for r, v in (("count", "star2"), ("mover", "star2"), ("opponent", "0")):
            c[(8, e, r)] = v
    c[(8, "aware", "count")] = "sw"
    c[(9, "aware", "count")] = "star2"
    return c


def pass1():
    say("=" * 100)
    say("D. PASS 1: claims, both modes (own script)")
    claims = claim_table()
    say(f"claims: {len(claims)}")
    out = {}
    for (t, e, r), v in sorted(claims.items()):
        files, wrap, text = TARGETS[t]
        geo = Geometry(files, wrap)
        rules = rules_for(geo, e, r)
        T = Trees()
        P = Builder(T)
        labels = {"claim": T.neg(P(v))}
        if v == "up2star":
            labels["lit"] = T.neg(P("up2starlit"))
        if e == "off":     # invariance: ep_aware flag cannot matter when ep=False; check by running True too
            pass
        res = solve_all(geo, rules, T, text, labels)
        out[(t, e, r)] = (v, res)
        if e == "off":
            rules2 = rules_for(geo, e, r, off_ep_aware=True)
            res2 = solve_all(geo, rules2, T, text, labels)
            if res2 != res:
                say(f"!! off: ep_aware True/False differ at T{t} {e}/{r}: {res} vs {res2}")
    # compare with claims.tsv
    theirs = {}
    for line in list(open(os.path.join(K5B, "claims.tsv")))[1:]:
        f = line.rstrip("\n").split("\t")
        theirs[(int(f[0]), f[1])] = f[2:]
    bad = 0
    for (t, e, r), (v, res) in sorted(out.items()):
        w, c = res["whole"]["claim"], res["comp"]["claim"]
        conf = "yes" if (w, c) == ("P", "P") else "no"
        tr = theirs.get((t, f"{e}/{r}"))
        if tr is None or (tr[1], tr[2], tr[3]) != (w, c, conf):
            say(f"DIFF claims.tsv T{t} {e}/{r}: mine whole={w} comp={c} conf={conf}; theirs={tr}")
            bad += 1
        if conf != "yes":
            say(f"NON-P: T{t} {e}/{r} claim {v}: whole={w} comp={c}")
        if v == "up2star":
            lw, lc = res["whole"]["lit"], res["comp"]["lit"]
            if (lw, lc) != ("P", "P"):
                say(f"NON-P literal up2*: T{t} {e}/{r}: {lw} {lc}")
                bad += 1
    say(f"pass 1: {len(out)} claims, mine confirmed in both modes: "
        f"{sum(1 for k, (v, res) in out.items() if (res['whole']['claim'], res['comp']['claim']) == ('P', 'P'))}; "
        f"rows differing from claims.tsv: {bad}; claims.tsv rows: {len(theirs)}")
    return out, bad


def wrong_setting_checks():
    """Settings wiring: wherever the brief says the value differs between settings, the other value must fail."""
    say("=" * 100)
    say("E. WIRING / NEGATIVE CHECKS (expected non-P in the 'must fail' rows)")
    cases = [
        # (target, ep, race, wrong V expression, why)
        (8, "textbook", "count", "sw", "textbook T8 is *2, not {2+-1|-2+-1}"),
        (8, "aware", "count", "star2", "aware T8 is {2+-1|-2+-1}, not *2"),
        (8, "off", "count", "sw", "off T8 is *2"),
        (8, "off", "opponent", "star2", "off/opponent T8 is 0, not *2"),
        (8, "textbook", "opponent", "star2", "textbook/opponent T8 is 0, not *2"),
        (8, "off", "mover", "0", "off/mover T8 is *2, not 0"),
        (9, "off", "count", "star2", "off T9: cylcgt says 0 (claim only for aware)"),
        (9, "aware", "count", "0", "aware T9 is *2, not 0"),
        (1, "aware", "count", "h16", "T1 is 1/8, not 1/16"),
        (1, "aware", "count", "h4", "T1 is 1/8, not 1/4"),
        (1, "aware", "count", "0", "T1 is 1/8, not 0"),
        (4, "aware", "count", "h8", "T4 is 1/16, not 1/8"),
        (4, "aware", "count", "h16+h16-h8+h16", "T4 = 1/16 (sanity of sum form: should be P)"),
        (5, "aware", "count", "up", "T5 is up2, not up"),
        (5, "aware", "count", "up2star", "T5 is up2, not up2*"),
        (6, "aware", "count", "up2", "T6 is up2*, not up2"),
        (6, "aware", "count", "up2-star", "up2 - * as an alternative; up2* != up2 - * ... is the same game (** = 0): expect P"),
        (7, "aware", "count", "up2", "T7 is tiny1, not up2"),
        (7, "aware", "count", "0", "T7 is tiny1, not 0"),
        (3, "aware", "count", "h4", "T3 is 1/8, not 1/4"),
    ]
    bad = 0
    for t, e, r, v, why in cases:
        files, wrap, text = TARGETS[t]
        geo = Geometry(files, wrap)
        rules = rules_for(geo, e, r)
        T = Trees()
        P = Builder(T)
        res = solve_all(geo, rules, T, text, {"x": T.neg(P(v))})
        w, c = res["whole"]["x"], res["comp"]["x"]
        should_be_P = why.endswith("expect P") or "should be P" in why
        flag = "P-expected" if should_be_P else "must-fail"
        ok = (w == c == "P") if should_be_P else (w != "P" and c != "P")
        bad += not ok
        say(f"{'ok ' if ok else 'BAD'} T{t} {e}/{r}  G - ({v}): whole={w} comp={c}  [{flag}] {why}")
    say(f"wiring checks failing: {bad}")
    return bad


# ---------------------------------------------------------------------------------------------------------
# F / G. Pass 2: cylcgt's own values
# ---------------------------------------------------------------------------------------------------------
def longest_left_chain_max(g, memo):
    """Largest |n| such that some reachable node is the integer chain n (structure only)."""
    # integer value of a node if it is a pure integer chain, else None
    def intval(x):
        k = id(x)
        if k in memo:
            return memo[k]
        if not x.L and not x.R:
            v = 0
        elif len(x.L) == 1 and not x.R:
            u = intval(x.L[0])
            v = u + 1 if (u is not None and u >= 0) else None
        elif len(x.R) == 1 and not x.L:
            u = intval(x.R[0])
            v = u - 1 if (u is not None and u <= 0) else None
        else:
            v = None
        memo[k] = v
        return v

    seen, stack, best = set(), [g], 0
    while stack:
        x = stack.pop()
        if id(x) in seen:
            continue
        seen.add(id(x))
        v = intval(x)
        if v is not None:
            best = max(best, abs(v))
        stack.extend(x.L)
        stack.extend(x.R)
    return best, len(seen), seen


def pass2(claims_out):
    from cylcgt import cgt, pawns
    say("=" * 100)
    say("F. PASS 2: cylcgt value at all 81 pairs; convert through .L/.R only; solve G + (-V_cyl)")
    theirs = {}
    for line in list(open(os.path.join(K5B, "cylcgt.tsv")))[1:]:
        f = line.rstrip("\n").split("\t")
        theirs[(int(f[0]), f[1])] = f[2:]
    rows, bad, skipped, tested, confirmed = [], 0, [], 0, 0
    maxints = {}
    tag_mismatch = 0
    off_inv_bad = 0
    t0 = time.time()
    for t in TARGETS:
        files, wrap, text = TARGETS[t]
        geo = Geometry(files, wrap)
        for e, r in SETTINGS:
            pawns.RACE_RULE = r
            vals = []
            for respects in ((True, False) if e == "off" else ((e != "textbook"),)):
                pawns.PASSED_RESPECTS_EP = respects
                pawns._value.cache_clear()
                board = pawns.Board(files, 8, wrap, e != "off")
                try:
                    g = pawns.value(board, pawns.Pos.parse(text))
                    vals.append((g, cgt.show(g), None))
                except Exception as ex:                       # RaceError
                    vals.append((None, None, f"{type(ex).__name__}: {ex}"))
            if e == "off" and vals[0][1] != vals[1][1]:
                off_inv_bad += 1
                say(f"!! off: PASSED_RESPECTS_EP changes cylcgt value at T{t} {e}/{r}: {vals[0][1]} vs {vals[1][1]}")
            g, shown, err = vals[0]
            th = theirs.get((t, f"{e}/{r}"))
            if g is None:
                say(f"T{t} {e}/{r}: cylcgt raised {err}; theirs={th}")
                rows.append((t, e, r, None, "raised", "-", "-"))
                continue
            mx, nn, seen = longest_left_chain_max(g, {})
            maxints[(t, e, r)] = mx
            # diagnostic only: do cylcgt's integer tags agree with structure?  (not used for conversion)
            for x in {id(y): y for y in _all(g)}.values():
                tag = x.num
                if tag is not None and getattr(tag, 'denominator', None) == 1:
                    sv = _struct_int(x)
                    if sv != int(tag):
                        tag_mismatch += 1
            if mx >= 64:
                skipped.append((t, e, r, shown, mx))
                rows.append((t, e, r, shown, "skipped", "-", "-"))
                if th is None or th[3] != "skipped":
                    say(f"DIFF cylcgt.tsv T{t} {e}/{r}: I skip (max int {mx}) but theirs={th}")
                    bad += 1
                continue
            T = Trees()
            memo = {}

            def conv(x):
                k = id(x)
                if k not in memo:
                    memo[k] = T.node([conv(y) for y in x.L], [conv(y) for y in x.R])
                return memo[k]
            node = conv(g)
            rules = rules_for(geo, e, r)
            res = solve_all(geo, rules, T, text, {"cyl": T.neg(node)})
            w, c = res["whole"]["cyl"], res["comp"]["cyl"]
            tested += 1
            conf = "yes" if (w, c) == ("P", "P") else "no"
            confirmed += conf == "yes"
            rows.append((t, e, r, shown, "tested", w, c))
            if th is None or th[0] != shown or (th[1], th[2], th[3]) != (w, c, conf):
                say(f"DIFF cylcgt.tsv T{t} {e}/{r}: mine value={shown} whole={w} comp={c} conf={conf}; theirs={th}")
                bad += 1
            if conf != "yes":
                say(f"NON-P: T{t} {e}/{r} cylcgt={shown} whole={w} comp={c}")
    say(f"pass 2: pairs {len(rows)}; tested {tested}; confirmed (P/P) {confirmed}; skipped {len(skipped)}; "
        f"rows differing from cylcgt.tsv: {bad}; elapsed {time.time() - t0:.1f}s")
    say("skipped pairs: " + "; ".join(f"T{t} {e}/{r} (max int {mx})" for t, e, r, s, mx in skipped))
    say("max |integer| among tested pairs: " + str(max([m for k, m in maxints.items() if m < 64] or [0])))
    mid = sorted(((k, m) for k, m in maxints.items() if 8 < m < 64))
    say(f"tested pairs with an integer in (8,64) (comp-mode BIGC/bank>8 shortcut region): {mid}")
    say(f"cylcgt integer tags disagreeing with structure (diagnostic): {tag_mismatch}")
    say(f"'off' value changes with PASSED_RESPECTS_EP: {off_inv_bad}")
    # which cylcgt printed values occur
    say("distinct printed values at tested pairs: " + ", ".join(sorted({r[3] for r in rows if r[4] == 'tested'})))
    # consistency: wherever a claim exists, is cylcgt's printed value consistent with it (info only)
    return rows, bad, skipped


def _all(g):
    seen, stack, out = set(), [g], []
    while stack:
        x = stack.pop()
        if id(x) in seen:
            continue
        seen.add(id(x))
        out.append(x)
        stack.extend(x.L)
        stack.extend(x.R)
    return out


def _struct_int(x):
    if not x.L and not x.R:
        return 0
    if len(x.L) == 1 and not x.R:
        u = _struct_int(x.L[0])
        return None if u is None or u < 0 else u + 1
    if len(x.R) == 1 and not x.L:
        u = _struct_int(x.R[0])
        return None if u is None or u > 0 else u - 1
    return None


def main():
    b1 = sanity()
    out, b2 = pass1()
    b3 = wrong_setting_checks()
    rows, b4, skipped = pass2(out)
    say("=" * 100)
    say(f"TOTAL FLAGS: sanity={b1} pass1_vs_tsv={b2} wiring={b3} pass2_vs_tsv={b4}")


if __name__ == "__main__":
    main()
