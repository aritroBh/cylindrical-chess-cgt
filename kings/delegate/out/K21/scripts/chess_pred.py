"""K21: chess instances.  Build the D-game of a pawn context on the e,f files of cyl:7x6 (decisive events = a passer, races by
the 'count' rule: cylcgt/lemmas.common), add the White shuttle on_D (Z_onT1 = Ka5 Pb4 Pc5 / kc6 pb5), predict with the abstract solver.
usage: chess_pred.py gen  -> writes ../chess/positions.txt and ../chess/pred.json"""
import sys, json, random, os
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames")
from cylcgt import pawns
from cylcgt.pawns import Board, Pos, sq, name
from lemmas import common as lc
from dsum import *

BOARD = Board(7, 6, True, True)

def ctx_comp(pos):
    """D-game of a pawn context (positions = Pos objects), root = pos"""
    idx = {}
    nodes = []
    def get(p):
        if p not in idx:
            idx[p] = len(nodes); nodes.append(p)
        return idx[p]
    get(pos)
    L = []; R = []
    i = 0
    while i < len(nodes):
        x = nodes[i]
        lpos, rpos = lc.split_ep(x)
        lo, ro = [], []
        for side, src, out in (("W", lpos, lo), ("B", rpos, ro)):
            for c in pawns.moves(BOARD, src, side):
                t = lc.terminal(BOARD, c)
                if t == 1: out.append(PLUS)
                elif t == -1: out.append(MINUS)
                elif t == 0:
                    out.append(PLUS if lc.race_winner(BOARD, c, side, "count") == "W" else MINUS)
                else:
                    out.append(get(c))
        L.append(sorted(set(lo))); R.append(sorted(set(ro)))
        i += 1
    return Comp(L, R, 0)

def pos_from(wlist, blist):
    return Pos(frozenset(sq(s) for s in wlist), frozenset(sq(s) for s in blist))

def predict(pos, group="on"):
    """predicted (White-to-move, Black-to-move) results from White's view, for Z_onT1 (White shuttle) or, with group='off',
    for the colour-reversed group (Black shuttle) with `pos` read as the context of the colour-reversed game"""
    K = ctx_comp(pos)
    S = mk_on() if group == "on" else mk_off()
    r = solve([K, S], [(0, 0)])
    return r[((0, 0), 0)], r[((0, 0), 1)]

def fen_ctx(pos):
    return " ".join(sorted([("P" + name(s)) for s in pos.white] + [("p" + name(s)) for s in pos.black]))

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "chess"); os.makedirs(out, exist_ok=True)
    rng = random.Random(2026)
    cands = {}
    seen = set()
    squares_w = [f + str(r) for f in "ef" for r in (2, 3, 4, 5)]
    squares_b = list(squares_w)
    for _ in range(6000):
        nw, nb = rng.choice([(1, 1), (1, 2), (2, 1), (2, 2), (1, 0), (0, 1), (2, 0), (0, 2), (2, 3), (3, 2)])
        w = rng.sample(squares_w, nw); b = rng.sample([s for s in squares_b if s not in w], nb)
        pos = pos_from(w, b)
        if pos in seen or lc.terminal(BOARD, pos) is not None: continue
        seen.add(pos)
        pr = predict(pos)
        cands.setdefault(pr, []).append(pos)
    sel = []
    for pr, lst in sorted(cands.items()):
        lst.sort(key=lambda p: (len(p.white) + len(p.black), str(p)))
        # 4 smallest of each predicted class, plus 2 mid-size ones
        pick = lst[:4] + lst[len(lst)//2: len(lst)//2 + 2]
        for p in pick:
            sel.append((p, pr))
    # the LOOPY P9 context, as a control
    p9 = pos_from(["e2"], ["f3"]); 
    if all(p9 != p for p, _ in sel): sel.append((p9, predict(p9)))
    print({k: len(v) for k, v in cands.items()}, len(sel))
    rows = []
    for p, pr in sel:
        rows.append({"group": "on", "ctx": fen_ctx(p), "pred": pr, "base": "Ka5 Pb4 Pc5 kc6 pb5"})
    # mirror (Z_offT1, Black shuttle): colour-reversed contexts; prediction by the off_D model (independent code path)
    for p, pr in sel[::3]:
        q = lc.colour_reverse(BOARD, p)
        rows.append({"group": "off", "ctx": fen_ctx(q), "pred": predict(q, "off"), "base": "Kc1 Pb2 ka2 pb3 pc2", "mirror_of": fen_ctx(p)})
    json.dump(rows, open(os.path.join(out, "pred.json"), "w"), indent=1)
    for grp in ("on", "off"):
        with open(os.path.join(out, "positions_%s.txt" % grp), "w") as f:
            for r in rows:
                if r["group"] == grp:
                    base = r["base"] + " " + r["ctx"]
                    f.write(base + " w -\n"); f.write(base + " b -\n")
    with open(os.path.join(out, "positions_all.txt"), "w") as f:
        for grp in ("on", "off"):
            f.write(open(os.path.join(out, "positions_%s.txt" % grp)).read())
    print(len(rows), "rows written")
