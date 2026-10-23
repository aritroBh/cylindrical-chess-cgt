"""Independent referee check of Lemma 2(b) for O_n and E_n, n <= 13.

Uses ONLY cylcgt.pawns.Board, Pos.parse, cylcgt.pawns.passed (ep-aware) plus a
hand-written pawn move generator. Does NOT use rg.c or cylcgt game-value code.

For each start position (no e.p. flag), for each side to move, for each wall
pawn of that side whose files j-1..j+3 or j-3..j+1 are pattern files (wall files),
enumerate every legal move of that pawn and check:
  (2a) mover has no passed pawn in the child;
  (L/P) either opponent already has a passed pawn in the child (L), or opponent
        has at least one move (the poisoning reply) after which opponent has a
        passed pawn and mover does not (P); and that reply is a capture.
Report every exception.
"""
import sys, os, importlib.util
sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames")
from cylcgt.pawns import Board, Pos, passed

spec = importlib.util.spec_from_file_location("fam", "/Users/aritro/Downloads/Research/Chessendgames/research/ring_family_proof/fam.py")
fam_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fam_mod)

FILES = "abcdefghijklmnopqrstuvwxyz"

def parse_token(tok):
    w=[]; b=[]; mode=None
    if tok == "-": return w, b
    for ch in tok:
        if ch in "WB": mode = ch
        else:
            if mode == "W": w.append(int(ch))
            else: b.append(int(ch))
    return w, b

def family_tokens(fam, n):
    if fam == "odd":
        assert n % 2 == 1 and n >= 5
        k = (n - 3)//2
        return ["W23B4","B5","W2B5"] + ["W3","B5"]*k
    if fam == "even":
        assert n % 2 == 0 and n >= 6
        m = (n - 6)//2
        return ["B5","W2B5","W35B6","W2"] + ["B4","W2"]*(m+1)
    raise ValueError(fam)

def to_pos_str(tokens):
    ws=[]; bs=[]
    for j, tok in enumerate(tokens):
        w, b = parse_token(tok)
        for r in w: ws.append(f"{FILES[j]}{r}")
        for r in b: bs.append(f"{FILES[j]}{r}")
    return "W: " + " ".join(ws) + " / B: " + " ".join(bs)

def own_moves(board, pos, side):
    mine, theirs = (pos.white, pos.black) if side == "W" else (pos.black, pos.white)
    occ = pos.white | pos.black
    d = 1 if side == "W" else -1
    start_rank = 2 if side == "W" else board.ranks - 1
    ep_target = pos.ep if (pos.ep and pos.ep[2] == side) else None
    out = []
    for (f, r) in mine:
        rest = mine - {(f, r)}
        r1 = r + d
        if 1 <= r1 <= board.ranks:
            if (f, r1) not in occ:
                newpos = _make_pos(side, rest | {(f, r1)}, theirs, None)
                out.append((newpos, f, f"{f}.step"))
                r2 = r + 2*d
                if r == start_rank and 1 <= r2 <= board.ranks and (f, r2) not in occ:
                    ep = None
                    if board.ep:
                        other = "B" if side == "W" else "W"
                        ep = ((f, r1), (f, r2), other)
                    newpos = _make_pos(side, rest | {(f, r2)}, theirs, ep)
                    out.append((newpos, f, f"{f}.double"))
        for df in (-1, 1):
            g = board.nb(f, df)
            if g is None: continue
            r1 = r + d
            if not (1 <= r1 <= board.ranks): continue
            t = (g, r1)
            if t in theirs:
                newpos = _make_pos(side, rest | {t}, theirs - {t}, None)
                out.append((newpos, f, f"{f}.capture"))
            elif ep_target and ep_target[0] == t:
                captured = ep_target[1]
                newpos = _make_pos(side, rest | {t}, theirs - {captured}, None)
                out.append((newpos, f, f"{f}.epcapture"))
    seen=set(); uniq=[]
    for np, f, desc in out:
        key = (frozenset(np.white), frozenset(np.black), np.ep)
        if key in seen: continue
        seen.add(key)
        uniq.append((np, f, desc))
    return uniq

def _make_pos(side, new_mine, new_theirs, ep):
    if side == "W":
        return Pos(frozenset(new_mine), frozenset(new_theirs), ep)
    else:
        return Pos(frozenset(new_theirs), frozenset(new_mine), ep)

def main():
    exceptions = []
    stats = {"moves":0, "L":0, "P":0}
    for fam in ("odd", "even"):
        ns = range(5, 14, 2) if fam == "odd" else range(6, 14, 2)
        for n in ns:
            tokens = family_tokens(fam, n)
            board = Board(n, 8, True, True)
            pos0 = Pos.parse(to_pos_str(tokens))
            wall = fam_mod.wall_files(fam, n)
            for side_to_move in ("W", "B"):
                for j in range(n):
                    if j not in wall: continue
                    w_ranks, b_ranks = parse_token(tokens[j])
                    if side_to_move == "W" and not w_ranks: continue
                    if side_to_move == "B" and not b_ranks: continue
                    if len(w_ranks)+len(b_ranks) != 1:
                        continue
                    cond1 = all(((j + d) % n) in wall for d in range(-1, 4))
                    cond2 = all(((j + d) % n) in wall for d in range(-3, 2))
                    if not (cond1 or cond2):
                        continue
                    moves = own_moves(board, pos0, side_to_move)
                    for (child, f, desc) in moves:
                        if f != j: continue
                        stats["moves"] += 1
                        mover_passed = passed(board, child, side_to_move)
                        opp = "B" if side_to_move == "W" else "W"
                        opp_passed = passed(board, child, opp)
                        if mover_passed:
                            exceptions.append((fam, n, side_to_move, j, desc, "2a_VIOLATION: mover has passed pawn in child"))
                            continue
                        if opp_passed:
                            stats["L"] += 1
                            continue
                        # P case
                        opp_moves = own_moves(board, child, opp)
                        found_any = False
                        found_cap = False
                        for (gchild, gf, gdesc) in opp_moves:
                            if passed(board, gchild, opp) and not passed(board, gchild, side_to_move):
                                found_any = True
                                if "capture" in gdesc:
                                    found_cap = True
                        if not found_any:
                            exceptions.append((fam, n, side_to_move, j, desc, "NOT_P: no opponent move yields opponent passed pawn"))
                        elif not found_cap:
                            exceptions.append((fam, n, side_to_move, j, desc, "NO_CAPTURE: opponent passed pawn only via non-capture"))
                        else:
                            stats["P"] += 1
    outdir = "/Users/aritro/Downloads/Research/Chessendgames/research/ring_family_proof_check"
    with open(os.path.join(outdir, "independent_check.txt"), "w") as fh:
        fh.write(f"Total wall-pawn moves checked: {stats['moves']}\n")
        fh.write(f"L cases: {stats['L']}, P cases: {stats['P']}\n")
        fh.write(f"Total exceptions: {len(exceptions)}\n")
        for e in exceptions:
            fh.write(repr(e) + "\n")
    print("moves:", stats["moves"], "L:", stats["L"], "P:", stats["P"], "exceptions:", len(exceptions))
    for e in exceptions[:50]:
        print(e)

if __name__ == "__main__":
    main()
