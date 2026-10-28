"""K17 library: exact checks of the hypotheses (V1a), (V1b), (V2), (V3), (V4) of Theorem 1.14 of LOOPY.md
for K+P positions in the structured class of Definition 2.1 (king group Z on files F_Z, pawn-free buffer,
context pawns on files at distance >= 2 from F_Z), and the D-results of the context.

Models of D used here (all use the 'count' race rule, normal play, Z deleted):
  D_whole  whole-board decisive-event game, global e.p. right that expires after one move
           (lemmas.common.alt_winner; this is the chess pawn game with 'passer = win')
  D_fix    disjunctive sum of the ROOT components with component-local e.p. rights that persist while
           the other component is played (Definition 1.3 reading of G1 + ... + Gk, our own recursion)
  D_S      outcome class of cylcgt.pawns.value (the BIG value, re-splitting)
P models: kp --frozen (V3 by fiat) and kp_p --pmodel (real kings, first promotion wins).

Run with PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames.
"""
from __future__ import annotations
import re, subprocess, sys, os
from functools import lru_cache
sys.setrecursionlimit(1_000_000)
from cylcgt import pawns, cgt
from cylcgt.pawns import Board, Pos, name, sq
from lemmas import common as C

assert pawns.PASSED_RESPECTS_EP is True
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
KP = os.path.join(OUT, "bin", "kp")
KPP = os.path.join(OUT, "bin", "kp_p")
HEAVY = "/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh"

# ---------------------------------------------------------------- boards
def board_of(spec: str):
    kind, dims = spec.split(":")
    w, h = map(int, dims.split("x"))
    return Board(w, h, kind == "cyl", True)

def fdist(b: Board, f, g):
    d = abs(f - g)
    return min(d, b.files - d) if b.wrap else d

# ---------------------------------------------------------------- pawn game helpers (context only)
def side_moves(b, pos, side):
    """children by one move of `side`; a right belonging to the other side expires."""
    src = pos if (pos.ep and pos.ep[2] == side) else Pos(pos.white, pos.black, None)
    return pawns.moves(b, src, side)

def mover_diff(parent: Pos, child: Pos, side):
    pm, cm = (parent.white, child.white) if side == "W" else (parent.black, child.black)
    frm = pm - cm
    to = cm - pm
    assert len(frm) == 1 and len(to) == 1, (parent, child, side)
    return next(iter(frm)), next(iter(to))

def other(s): return "B" if s == "W" else "W"

def decisive(b, child: Pos, mover):
    """None if not decisive, else beneficiary 'W'/'B' under the count race rule."""
    t = C.terminal(b, child)
    if t is None: return None
    if t == 1: return "W"
    if t == -1: return "B"
    return C.race_winner(b, child, mover, "count")

def reach(b, root: Pos, stm):
    """alternating-play closure of the chess-reachable non-terminal (pos,stm); returns dict
    (pos,stm) -> list of (from,to,child,beneficiary_or_None)"""
    out = {}
    stack = [(root, stm)]
    while stack:
        key = stack.pop()
        if key in out: continue
        pos, s = key
        ev = []
        for c in side_moves(b, pos, s):
            fr, to = mover_diff(pos, c, s)
            ben = decisive(b, c, s)
            ev.append((fr, to, c, ben))
            if ben is None and (c, other(s)) not in out:
                stack.append((c, other(s)))
        out[key] = ev
    return out

# ---------------------------------------------------------------- D models
@lru_cache(maxsize=None)
def D_whole_win(b, pos, s):
    return C.alt_winner(b, pos, s, "count", False)

def D_whole(b, pos):
    """(result with White to move, result with Black to move), each from White's view W/L"""
    return ("W" if D_whole_win(b, pos, "W") == "W" else "L",
            "W" if D_whole_win(b, pos, "B") == "W" else "L")

@lru_cache(maxsize=None)
def _dfix(b, comps, s):
    # comps: tuple of component Pos (each with its local e.p. right); returns winner of normal play
    for i, comp in enumerate(comps):
        src = comp if (comp.ep and comp.ep[2] == s) else Pos(comp.white, comp.black, None)
        for c in pawns.moves(b, src, s):
            t = C.terminal(b, c)
            if t is not None:
                res = ("W" if t == 1 else "B") if t != 0 else C.race_winner(b, c, s, "count")
            else:
                nc = comps[:i] + (c,) + comps[i + 1:]
                res = _dfix(b, nc, other(s))
            if res == s: return s
    return other(s)

def D_fix(b, pos):
    comps = tuple(sorted(pawns.components(b, pos), key=lambda p: sorted(p.white | p.black)))
    return ("W" if _dfix(b, comps, "W") == "W" else "L",
            "W" if _dfix(b, comps, "B") == "W" else "L")

def D_S(b, pos):
    o = cgt.outcome(pawns.value(b, pos))   # L,R,N,P
    return {"L": ("W", "W"), "R": ("L", "L"), "N": ("W", "L"), "P": ("L", "W")}[o], o

# ---------------------------------------------------------------- hypotheses on the context
def v4_hss_exact(b, root, stm, rc=None):
    rc = rc or reach(b, root, stm)
    return all(C.pairwise_safe(b, p) for (p, s) in rc)

def v4_strong(b, root):
    return C.hereditarily_safe(b, root)

def tempo_ok(b, root):
    n = len(root.white) + len(root.black)
    return (b.ranks - 2) * n + 1 < pawns.BIG

def usable_ep(b, pos, s):
    """True if side s has an e.p. capture available at pos (the captured pawn disappears)."""
    if not (pos.ep and pos.ep[2] == s): return False
    cap = pos.ep[1]
    theirs = pos.black if s == "W" else pos.white
    for c in pawns.moves(b, pos, s):
        ct = c.black if s == "W" else c.white
        if cap in theirs and cap not in ct:
            return True
    return False

def E_violated(b, root, stm, rc=None):
    """(E) of L1.6: some chess-reachable Y with >= 2 components carries a usable e.p. right"""
    rc = rc or reach(b, root, stm)
    for (p, s) in rc:
        if p.ep and p.ep[2] == s and len(pawns.components(b, p)) >= 2 and usable_ep(b, p, s):
            return (p, s)
    return None

# ---------------------------------------------------------------- Z and kp positions
def sqn(s): return name(s)

def chess_str(pos: Pos, stm, Z):
    """Z = dict(wk='a1', bk='a5', wz=['a3'], bz=['a4'], FZ={0,1})"""
    toks = ["K" + Z["wk"], "k" + Z["bk"]]
    toks += ["P" + x for x in Z.get("wz", [])] + ["p" + x for x in Z.get("bz", [])]
    toks += ["P" + sqn(s) for s in sorted(pos.white)] + ["p" + sqn(s) for s in sorted(pos.black)]
    ep = "-"
    if pos.ep and pos.ep[2] == stm: ep = sqn(pos.ep[0])
    return " ".join(toks) + (" w " if stm == "W" else " b ") + ep

MV = re.compile(r"([KPkp])([a-h]\d)([a-h]\d)(?:=?([QRBN]))?:([WLD])")

def run_kp(binary, board_spec, lines, flags=("--frozen", "--moves"), heavy=False, threads=2):
    cmd = ([HEAVY] if heavy else []) + [binary, "--board", board_spec, *flags, "--threads", str(threads)]
    r = subprocess.run(cmd, input="\n".join(lines) + "\n", capture_output=True, text=True)
    res = {}
    for ln in r.stdout.splitlines():
        if " | " not in ln: continue
        pos, rest = ln.split(" | ", 1)
        parts = rest.split(" | ")
        head = parts[0].split()
        mv = parts[1] if len(parts) > 1 else ""
        res[pos] = (head[0], head[1], [m for m in mv.split()])
    return res, r.stderr

def parse_moves(toks):
    out = []
    for t in toks:
        m = MV.fullmatch(t)
        assert m, t
        out.append((m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)))
    return out

def verify(b, board_spec, root: Pos, stm, Z, kpres, rc=None, model="frozen"):
    """Exact check of V1a (no check, move sets equal, i.e. chess pawn moves = D-options in the whole-board
    game), V1b, V2, V3 at every chess-reachable position. kpres: dict position-string -> (A,B,moves).
    Returns dict of booleans and notes."""
    rc = rc or reach(b, root, stm)
    FZ = Z["FZ"]
    notes = []
    ok = dict(V1a_moves=True, V1b=True, V2=True, V3=True)
    for (p, s), ev in rc.items():
        key = chess_str(p, s, Z)
        if key not in kpres:
            raise KeyError(key)
        A, B_, toks = kpres[key]
        if A == "X":
            notes.append(f"illegal chess position {key}")
            ok["V1a_moves"] = False
            continue
        mv = parse_moves(toks)
        if len(mv) == 0:
            ok["V1b"] = False; notes.append(f"no legal move at {key} ({A})")
        # context pawn moves from kp vs D-options
        ctx_kp = {}
        for (pc, fr, to, pr, val) in mv:
            f_file = sq(fr)[0]
            is_pawn = pc in "Pp"
            if is_pawn and f_file not in FZ:
                ctx_kp[(fr, to)] = val
            else:
                # Z-move (king move or Z-pawn move)
                mover_loses = (val == ("L" if s == "W" else "W"))
                if not mover_loses:
                    ok["V3"] = False; notes.append(f"Z-move {pc}{fr}{to} not punished at {key}: {val}")
        exp = {(sqn(fr), sqn(to)): ben for (fr, to, c, ben) in ev}
        if set(ctx_kp) != set(exp):
            ok["V1a_moves"] = False
            notes.append(f"move sets differ at {key}: kp-only {sorted(set(ctx_kp)-set(exp))} D-only {sorted(set(exp)-set(ctx_kp))}")
        for k_, ben in exp.items():
            if ben is not None and k_ in ctx_kp:
                want = "W" if ben == "W" else "L"
                if ctx_kp[k_] != want:
                    ok["V2"] = False
                    notes.append(f"V2 fails: {k_} at {key}: D says {ben}, kp {ctx_kp[k_]}")
    return ok, notes

def all_queries(b, root, stm, Z, rc=None):
    rc = rc or reach(b, root, stm)
    return [chess_str(p, s, Z) for (p, s) in rc]
