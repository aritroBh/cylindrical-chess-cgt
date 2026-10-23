"""Differential test of the independent C engine rg (move generation, passed test, race rule, class T/L/P/K)
against the project's reference implementation cylcgt.pawns, on random positions of the n-file cylinder.
Run from the project root:  PYTHONPATH=. .venv/bin/python research/ring_family_proof/difftest.py [N_POSITIONS] [SEED]
"""
import sys, random, subprocess, os
from cylcgt import pawns
from cylcgt.pawns import Board, Pos

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fam import parse_classify
pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True
BIG = pawns.BIG

def to_tok(pos, n):
    toks = []
    for f in range(n):
        w = sorted(r for g, r in pos.white if g == f); b = sorted(r for g, r in pos.black if g == f)
        t = ("W" + "".join(map(str, w)) if w else "") + ("B" + "".join(map(str, b)) if b else "")
        toks.append(t or "-")
    s = " ".join(toks)
    if pos.ep:
        (tf, tr), (cf, cr), holder = pos.ep
        s += f" ep{'W' if holder == 'B' else 'B'}={cf}"        # epW=f: the White pawn on file f has just double-stepped
    return s

def norm_ep(board, pos):
    """drop an e.p. field when it has no effect (no enemy pawn beside the landing square): the C engine does so"""
    if pos.ep is None: return pos
    (tf, tr), (cf, cr), holder = pos.ep
    theirs = pos.white if holder == "W" else pos.black
    if any((g, cr) in theirs for g in (board.nb(cf, -1), board.nb(cf, 1))): return pos
    return Pos(pos.white, pos.black, None)

def canon(pos):
    ep = None
    if pos.ep:
        ep = (pos.ep[1], pos.ep[2])
    return (frozenset(pos.white), frozenset(pos.black), ep)

def term(board, pos, side):
    """+1/-1/0: terminal win/loss for `side` (who has just moved to `pos`) / non-terminal, using cylcgt's passed test and race rule"""
    wp, bp = pawns.passed(board, pos, "W"), pawns.passed(board, pos, "B")
    if wp and bp:
        v = pawns._child(board, pos, side)                 # race rule: returns an integer, no recursion
        return 1 if ((v.num > 0) == (side == "W")) else -1
    if not wp and not bp: return 0
    return 1 if (wp == (side == "W")) else -1

def ref_classes(board, pos):
    """{(side, child canon): class} using cylcgt: T/L/P/K"""
    out = {}
    for side in ("W", "B"):
        opp = "B" if side == "W" else "W"
        plain = Pos(pos.white, pos.black, None)
        lpos = plain if (pos.ep and pos.ep[2] != side) else pos
        for ch in pawns.moves(board, lpos, side):
            ch = norm_ep(board, ch)
            t = term(board, ch, side)
            if t != 0:
                code = "T" if t == 1 else "L"
            else:
                code = "K"
                pl = Pos(ch.white, ch.black, None)
                rpos = pl if (ch.ep and ch.ep[2] != opp) else ch
                for c2 in pawns.moves(board, rpos, opp):
                    if term(board, norm_ep(board, c2), opp) == 1:
                        code = "P"; break
            out[(side, canon(ch))] = code
    return out

def rand_pos(n, npawn, rng, want_ep):
    board = Board(n, 8, True, True)
    for _ in range(1000):
        occ = set(); W = set(); B = set()
        for _ in range(npawn):
            f = rng.randrange(n); r = rng.randrange(2, 8)
            if (f, r) in occ: continue
            occ.add((f, r)); (W if rng.random() < 0.5 else B).add((f, r))
        ep = None
        if want_ep:
            cands = []
            for (f, r) in W:
                if r == 4 and (f, 3) not in occ and (f, 2) not in occ: cands.append(((f, 3), (f, 4), "B"))
            for (f, r) in B:
                if r == 5 and (f, 6) not in occ and (f, 7) not in occ: cands.append(((f, 6), (f, 5), "W"))
            if not cands: continue
            ep = rng.choice(cands)
        pos = Pos(frozenset(W), frozenset(B), ep)
        pos = norm_ep(board, pos)
        if pawns.passed(board, pos, "W") or pawns.passed(board, pos, "B"): continue
        return board, pos
    return None

def child_canon(tok, n):
    parts = tok.split(); ep = None
    W = set(); B = set(); f = 0
    for t in parts:
        if t.startswith("ep"):
            holder = "B" if t[2] == "W" else "W"      # epW=f -> a White pawn doubled -> holder B
            cf = int(t.split("=")[1]); ep = cf, holder
            continue
        if t != "-":
            mode = None
            for ch in t:
                if ch in "WB": mode = ch
                else: (W if mode == "W" else B).add((f, int(ch)))
        f += 1
    if ep:
        cf, holder = ep
        r = 4 if holder == "B" else 5
        ep = ((cf, r), holder)
    return (frozenset(W), frozenset(B), ep)

def main():
    npos = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    rng = random.Random(seed)
    cases = []
    while len(cases) < npos:
        n = rng.choice([5, 6, 7, 8, 9, 11, 14])
        npawn = rng.randrange(4, 2 * n + 2)
        r = rand_pos(n, npawn, rng, want_ep=(rng.random() < 0.4))
        if r: cases.append(r)
    mismatches = 0; moves_seen = 0; counts = {"T": 0, "L": 0, "P": 0, "K": 0}
    # group by n because rg's N is set by the position line (the engine re-reads N per line)
    inp = "\n".join(to_tok(p, b.files) for b, p in cases) + "\n"
    out = subprocess.run([os.path.join(HERE, "rg"), "classify"], input=inp, capture_output=True, text=True).stdout
    blocks = parse_classify(out)
    assert len(blocks) == len(cases), (len(blocks), len(cases))
    for (board, pos), blk in zip(cases, blocks):
        ref = ref_classes(board, pos)
        mine = {}
        for side, code, mv, child in blk["mv"]:
            mine[(side, child_canon(child, board.files))] = code
        moves_seen += len(ref)
        for k in ref: counts[ref[k]] += 1
        if ref != mine:
            mismatches += 1
            if mismatches <= 5:
                print("MISMATCH", pos, "only ref:", [(k[0], v) for k, v in ref.items() if mine.get(k) != v][:3],
                      "only mine:", [(k[0], v) for k, v in mine.items() if ref.get(k) != v][:3])
    print(f"differential test: {len(cases)} random positions (n=5..14, with and without e.p.), {moves_seen} moves, class counts {counts}, race-rule invocations (cylcgt) {len(pawns.race_hits)}, mismatches {mismatches}")
    return mismatches

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
