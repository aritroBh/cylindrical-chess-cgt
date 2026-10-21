"""Deterministic printing and safe parsing of short-game values for ChessSums.

`cylcgt.cgt.show` orders options by internal object id, which depends on the
order in which games were created, so it is not stable across runs. This module
prints canonical forms with options sorted by their printed text, and parses
answers (from people or models) back into canonical games so that values can be
compared exactly (two games are equal iff they are the same interned object).

Printed format (unicode, standard CGT notation)
    numbers         0  3  -5/2
    number+ups+star 1/2*  ↑  ⇑*  -1↓  *2 ...   (x + u.↑ + *m, juxtaposed)
    switches        ±1   3/2±1/2               (= {x+y | x-y})
    anything else   {A, B | C}                 (options recursively, sorted)
ASCII variant: ↑ -> ^, ⇑ -> ^^, ↓ -> v, ⇓ -> vv, ± -> +- .

Parser accepts both variants plus explicit sums ("1/2 + *", "{1|-1} + ^"),
'+/-', parentheses, and unary minus. It has hard size limits so a malicious or
degenerate model answer cannot make the reward function run for long.
"""
from __future__ import annotations

import re
from fractions import Fraction

from cylcgt import cgt

_UPSTAR: dict[int, tuple[int, int]] = {}  # game id -> (u, m) for u.↑ + *m
_UPSTAR_GAME: dict[tuple[int, int], cgt.Game] = {}
MAX_UP = 12
MAX_NIM = 15


def ups(u: int) -> cgt.Game:
    g = cgt.ZERO
    step = cgt.UP if u > 0 else cgt.DOWN
    for _ in range(abs(u)):
        g = cgt.add(g, step)
    return g


def upstar(u: int, m: int) -> cgt.Game:
    key = (u, m)
    if key not in _UPSTAR_GAME:
        _UPSTAR_GAME[key] = cgt.add(ups(u), cgt.nimber(m))
    return _UPSTAR_GAME[key]


def _build_upstar_table():
    if _UPSTAR:
        return
    for u in range(-MAX_UP, MAX_UP + 1):
        for m in range(0, MAX_NIM + 1):
            g = upstar(u, m)
            _UPSTAR.setdefault(g.id, (u, m))


def fnum(x: Fraction) -> str:
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def _up_str(u: int) -> str:
    if u == 0:
        return ""
    a = "↑" if u > 0 else "↓"
    if abs(u) == 2:
        return "⇑" if u > 0 else "⇓"
    return a * abs(u)


def decompose(g: cgt.Game):
    """Return (x, u, m) with g = x + u.↑ + *m, or None."""
    _build_upstar_table()
    if g.num is not None:
        return (g.num, 0, 0)
    try:
        ls, rs = cgt.stops(g)
    except AssertionError:  # pragma: no cover
        return None
    if ls != rs:
        return None
    x = Fraction(ls)
    if x.denominator & (x.denominator - 1):
        return None
    h = cgt.add(g, cgt.number(-x)) if x != 0 else g
    um = _UPSTAR.get(h.id)
    if um is None:
        return None
    return (x, um[0], um[1])


def fmt(g: cgt.Game, ascii: bool = False) -> str:
    s = _fmt(g)
    return to_ascii(s) if ascii else s


def to_ascii(s: str) -> str:
    return s.replace("⇑", "^^").replace("⇓", "vv").replace("↑", "^").replace("↓", "v").replace("±", "+-")


_fmt_memo: dict[int, str] = {}


def _fmt(g: cgt.Game) -> str:
    r = _fmt_memo.get(g.id)
    if r is not None:
        return r
    d = decompose(g)
    if d is not None:
        x, u, m = d
        parts = []
        if x != 0 or (u == 0 and m == 0):
            parts.append(fnum(x))
        parts.append(_up_str(u))
        if m:
            parts.append("*" if m == 1 else f"*{m}")
        r = "".join(parts)
    elif (len(g.L) == 1 and len(g.R) == 1 and g.L[0].num is not None
          and g.R[0].num is not None and g.L[0].num > g.R[0].num):
        a, b = g.L[0].num, g.R[0].num
        mid, half = (a + b) / 2, (a - b) / 2
        r = ("" if mid == 0 else fnum(mid)) + "±" + fnum(half)
    else:
        L = sorted(_fmt(x) for x in g.L)
        R = sorted(_fmt(x) for x in g.R)
        r = "{" + ", ".join(L) + " | " + ", ".join(R) + "}"
    _fmt_memo[g.id] = r
    return r


def kind(g: cgt.Game) -> str:
    """Coarse value class used for score breakdowns."""
    d = decompose(g)
    if d is not None:
        x, u, m = d
        if u == 0 and m == 0:
            return "integer" if x.denominator == 1 else "number"
        if u == 0:
            return "number+nimber"
        return "number+ups(+nimber)"
    t = cgt.temperature(g)
    if t is not None and t > 0:
        if (len(g.L) == 1 and len(g.R) == 1 and g.L[0].num is not None and g.R[0].num is not None):
            return "switch"
        return "hot-other"
    return "cold-other"


# ---------------------------------------------------------------------------
# parser
# ---------------------------------------------------------------------------

class ParseError(ValueError):
    pass


MAX_LEN = 2000
MAX_DEPTH = 12
MAX_ABS_NUM = 1024
MAX_DENOM = 1 << 12
MAX_PARSE_NIM = 32
MAX_PARSE_UP = 32
MAX_ATOMS = 500       # total atoms in one answer (gold values use at most 153)
MAX_ARROWS = 128      # total arrows in one answer (gold values use at most 48)

_TOKEN = re.compile(r"""
    (?P<ws>\s+)
  | (?P<pm>±|\+/-|\+-)
  | (?P<num>\d+(?:/\d+|\.\d+)?)
  | (?P<star>\*\d*)
  | (?P<up>[\^↑⇑]+)
  | (?P<down>[v↓⇓]+)
  | (?P<op>[{}|,()+\-])
""", re.X)


def _tokens(s: str):
    s = s.replace("−", "-").replace("–", "-")
    pos, out = 0, []
    while pos < len(s):
        m = _TOKEN.match(s, pos)
        if not m:
            raise ParseError(f"unexpected character {s[pos]!r} at {pos}")
        pos = m.end()
        kind_ = m.lastgroup
        if kind_ == "ws":
            continue
        out.append((kind_, m.group()))
    out.append(("end", ""))
    return out


def _add(a: cgt.Game, b: cgt.Game) -> cgt.Game:
    if a.num is not None and b.num is not None and abs(a.num + b.num) > MAX_ABS_NUM:
        raise ParseError("number too large")
    return cgt.add(a, b)


class _P:
    def __init__(self, s: str):
        if len(s) > MAX_LEN:
            raise ParseError("answer too long")
        self.t = _tokens(s)
        self.i = 0
        self.depth = 0
        self.atoms = 0
        self.arrows = 0

    def peek(self):
        return self.t[self.i]

    def take(self, val=None):
        tok = self.t[self.i]
        if val is not None and tok[1] != val:
            raise ParseError(f"expected {val!r}, got {tok[1]!r}")
        self.i += 1
        return tok

    def expr(self) -> cgt.Game:
        g = self.term()
        while self.peek()[1] in ("+", "-") and self.peek()[0] == "op":
            op = self.take()[1]
            h = self.term()
            g = _add(g, h if op == "+" else cgt.neg(h))
        return g

    def _starts_atom(self, tok) -> bool:
        k, v = tok
        return k in ("num", "star", "up", "down", "pm") or v in ("{", "(")

    def term(self) -> cgt.Game:
        """Juxtaposed atoms are summed ("1/2*", "-1↑", "3/2±1/2"); a unary
        minus binds to the next atom only, so "-1↑" is -1 + ↑."""
        g = self.signed_atom()
        while self._starts_atom(self.peek()):
            g = _add(g, self.atom())
        return g

    def signed_atom(self) -> cgt.Game:
        if self.peek() == ("op", "-"):
            self.take()
            return cgt.neg(self.atom())
        return self.atom()

    def atom(self) -> cgt.Game:
        self.atoms += 1
        if self.atoms > MAX_ATOMS:
            raise ParseError("answer has too many terms")
        k, v = self.peek()
        if k == "num":
            self.take()
            if "." in v:
                x = Fraction(v)
            elif "/" in v:
                a, b = v.split("/")
                if int(b) == 0:
                    raise ParseError("division by zero")
                x = Fraction(int(a), int(b))
            else:
                x = Fraction(int(v))
            if abs(x) > MAX_ABS_NUM or x.denominator > MAX_DENOM or x.denominator & (x.denominator - 1):
                raise ParseError(f"number {v} is not a small dyadic rational")
            return cgt.number(x)
        if k == "star":
            self.take()
            n = int(v[1:]) if len(v) > 1 else 1
            if n > MAX_PARSE_NIM:
                raise ParseError("nimber too large")
            return cgt.nimber(n)
        if k in ("up", "down"):
            self.take()
            n = sum(2 if c in "⇑⇓" else 1 for c in v)
            self.arrows += n
            if n > MAX_PARSE_UP or self.arrows > MAX_ARROWS:
                raise ParseError("too many arrows")
            return ups(n if k == "up" else -n)
        if k == "pm":
            self.take()
            g = self.simple()
            return cgt.make([g], [cgt.neg(g)])
        if v == "(":
            self.take()
            self._enter()
            g = self.expr()
            self.take(")")
            self.depth -= 1
            return g
        if v == "{":
            self.take()
            self._enter()
            L = self.optlist("|")
            self.take("|")
            R = self.optlist("}")
            self.take("}")
            self.depth -= 1
            return cgt.make(L, R)
        raise ParseError(f"unexpected token {v!r}")

    def simple(self) -> cgt.Game:
        """Operand of ±: a juxtaposed run of non-± atoms (e.g. ±1, ±1/2, ±{2|1})."""
        g = self.signed_atom()
        while self._starts_atom(self.peek()) and self.peek()[0] != "pm":
            g = _add(g, self.atom())
        return g

    def optlist(self, stop: str):
        out = []
        if self.peek()[1] == stop:
            return out
        out.append(self.expr())
        while self.peek()[1] == ",":
            self.take()
            out.append(self.expr())
        return out

    def _enter(self):
        self.depth += 1
        if self.depth > MAX_DEPTH:
            raise ParseError("nesting too deep")


def parse(s: str) -> cgt.Game:
    """Parse a value expression into a canonical cgt.Game (raises ParseError)."""
    if not isinstance(s, str) or not s.strip():
        raise ParseError("empty answer")
    p = _P(s.strip())
    g = p.expr()
    if p.peek()[0] != "end":
        raise ParseError(f"trailing input at {p.peek()[1]!r}")
    return g


def same_value(answer: str, gold: str) -> bool:
    """True iff `answer` parses to the same game as `gold` (gold must parse)."""
    try:
        a = parse(answer)
    except (ParseError, RecursionError, ValueError, ZeroDivisionError):
        return False
    return a is parse(gold)
