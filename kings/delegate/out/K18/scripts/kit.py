"""helpers shared by the K18 scripts (imports the independent move generator of lg2.py)."""
import sys
_argv = sys.argv
sys.argv = [sys.argv[0], "--board", "cyl:8x6", "--fz", "0:3"]
import importlib.util, os
_spec = importlib.util.spec_from_file_location("lg2", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lg2.py"))
lg2 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(lg2)
sys.argv = _argv

def setboard(board, fz):
    """re-point lg2's globals at another board"""
    kind, dims = board.split(":")
    lg2.CYL = kind == "cyl"
    lg2.W, lg2.H = map(int, dims.split("x"))
    f0, n = map(int, fz.split(":"))
    lg2.FZFILES = {(f0 + i) % lg2.W for i in range(n)}

def sqn(s): return "abcdefgh"[s[0]] + str(s[1] + 1)
def fmt(state):
    Wp, Bp, wk, bk, stm, ep = state
    return " ".join(["K" + sqn(wk)] + ["P" + sqn(s) for s in sorted(Wp)] + ["k" + sqn(bk)] + ["p" + sqn(s) for s in sorted(Bp)] + [stm, sqn(ep) if ep else "-"])
def mname(state, color, mv):
    ns, kd, frm, to = mv
    Wp, Bp, wk, bk, stm, ep = state
    own = Wp if color == "w" else Bp
    king = frm not in own
    return ("K" if king else "") + sqn(frm) + "-" + sqn(to) + ("=Q" if kd == "promo" else "")
def apply_move(state, name, confine=False):
    color = state[4]
    for mv in lg2.moves(state, color, confine):
        if mname(state, color, mv) == name: return mv[0]
    raise ValueError("no move " + name + " in " + fmt(state))
