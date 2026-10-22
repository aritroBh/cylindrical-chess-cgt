"""Second implementation of the e.p. ablation: cylcgt with a patched moves() that drops chosen e.p. captures."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from cylcgt import pawns, cgt
orig = pawns.moves
ALLOWED = None   # None = all; else set of (side, 'from', 'to') strings
def patched(board, pos, side):
    out = orig(board, pos, side)
    if ALLOWED is None or not (pos.ep and pos.ep[2] == side):
        return out
    keep = []
    for c in out:
        mo, mn = (pos.white, c.white) if side == "W" else (pos.black, c.black)
        to_, tn = (pos.black, c.black) if side == "W" else (pos.white, c.white)
        is_ep = (pos.ep[1] in to_ and pos.ep[1] not in tn and pos.ep[0] in mn and pos.ep[0] not in mo)
        if is_ep:
            frm = next(iter(mo - mn))
            if (side, pawns.name(frm), pawns.name(pos.ep[0])) not in ALLOWED:
                continue
        keep.append(c)
    return keep
pawns.moves = patched
pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True
B = pawns.Board(3, 8, True, True)
P = pawns.Pos.parse("W: a2 a3 b2 / B: b7 c6 c7")
ALL = {("B","a4","b3"),("B","b4","a3"),("B","c4","a3"),("B","c4","b3"),("W","a5","b6"),("W","a5","c6"),("W","b5","c6"),("W","c5","b6")}
def run(label, allowed):
    global ALLOWED
    ALLOWED = allowed; pawns._value.cache_clear()
    g = pawns.value(B, P)
    print(f"{label:45s} -> {cgt.show(g)[:60]}  outcome {cgt.outcome(g)}")
run("all e.p. captures allowed", None)
run("none allowed", set())
run("all but W c5xb6", ALL - {("W","c5","b6")})
run("only W c5xb6", {("W","c5","b6")})
run("all but W a5xb6", ALL - {("W","a5","b6")})
run("all but B b4xa3", ALL - {("B","b4","a3")})
run("all but W b5xc6", ALL - {("W","b5","c6")})
run("only B b4xa3", {("B","b4","a3")})
run("only W b5xc6", {("W","b5","c6")})
run("only B b4xa3 + W b5xc6", {("B","b4","a3"),("W","b5","c6")})
