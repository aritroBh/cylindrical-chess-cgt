"""negative tests for ringtools.legality: it must reject rings with a passed pawn, an empty file, a repeated square,
rank-out-of-range pawns, wrong pawn count."""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ringtools as rt
hit = "B4 B7 W3 W2B5 B7 W3 W2 B7 W2"
base = rt.parse(hit)
assert rt.legality(base, 9, 10) == []
def mod(i, w=None, b=None):
    r = list(base); W, B = r[i]; r[i] = (tuple(w) if w is not None else W, tuple(b) if b is not None else B); return tuple(r)
cases = {
 "passed black pawn (file 1 B7 -> B3)": mod(1, b=(3,)),
 "passed black pawn (file 6 B7 -> B3)": mod(6, b=(3,)),
 "passed white pawn (file 4 W2B5 -> W6, black above gone)": mod(4, w=(6,), b=()),
 "white pawn on rank 7": mod(3, w=(2, 7)),
 "black pawn on rank 2": mod(0, b=(2,)),
 "two pawns on one square": mod(3, w=(2, 5), b=(5,)),
 "empty file": mod(8, w=(), b=()),
 "11 pawns": mod(0, w=(2,), b=(4,)),
}
for k, r in cases.items():
    e = rt.legality(r, 9, 10)
    print("%-48s -> %s" % (k, "REJECTED: " + e[0] if e else "ACCEPTED (BAD)"))
    assert e
# colour reversal is an involution and preserves legality
for h in ["B4 B7 W3 W2B5 B7 W3 W2 B7 W2", "B4 W2 B6 W2 W3 B6 B7 W3 W6B7"]:
    r = rt.parse(h); assert rt.colour_reverse(rt.colour_reverse(r)) == r and not rt.legality(rt.colour_reverse(r), 9, 10)
print("self-test ok")
