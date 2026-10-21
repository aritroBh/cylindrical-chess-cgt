"""Exact text key of a canonical cylcgt game, and its inverse (key -> canonical game)."""
from fractions import Fraction
from cylcgt import cgt

_memo = {}
def key(g):
    r = _memo.get(g.id)
    if r is not None: return r
    if g.num is not None:
        x = g.num; r = str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    elif g.nim is not None:
        r = f"*{g.nim}"
    else:
        r = "{" + ",".join(sorted(key(x) for x in g.L)) + "|" + ",".join(sorted(key(x) for x in g.R)) + "}"
    _memo[g.id] = r; return r

_pm = {}
def parse(s):
    if s in _pm: return _pm[s]
    pos = 0
    def p():
        nonlocal pos
        if s[pos] == "{":
            pos += 1; L, R = [], []; cur = L
            while True:
                c = s[pos]
                if c == "|": cur = R; pos += 1; continue
                if c == "}": pos += 1; break
                if c == ",": pos += 1; continue
                cur.append(p())
            return cgt.make(L, R)
        if s[pos] == "*":
            j = pos + 1
            while j < len(s) and s[j].isdigit(): j += 1
            k = int(s[pos+1:j]); pos = j
            return cgt.nimber(k)
        j = pos
        while j < len(s) and (s[j].isdigit() or s[j] in "-/"): j += 1
        t = s[pos:j]; pos = j
        return cgt.number(Fraction(t))
    g = p(); assert pos == len(s)
    _pm[s] = g; return g

def bigfree(k):
    return all(abs(Fraction(t)) < 128 for t in __import__("re").findall(r"-?\d+(?:/\d+)?", k.replace("*", "#")) if not t.startswith("#"))
