"""Checks of the locality statements used in the proof (Lemma 1/2):
 (a) whether a pawn is passed depends only on its own file and the two neighbouring files (and on the e.p. flag);
 (b) if a position has no passed pawn, then after any move the passed pawns of the child lie on files within distance 1
     of a file changed by the move, or are the pawn whose e.p. protection lapsed;
 (c) per-pawn passed flags agree with cylcgt's pawns.passed.
Run from the project root: PYTHONPATH=. .venv/bin/python research/ring_family_proof/locality_test.py [N] [seed]"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cylcgt import pawns
from cylcgt.pawns import Board, Pos
from difftest import rand_pos, norm_ep

pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True

def passed_pawns(board, pos):
    """set of (colour, file, rank) of passed pawns, own implementation of the definition"""
    out = set(); n = board.files
    for colour, mine, theirs in (("W", pos.white, pos.black), ("B", pos.black, pos.white)):
        for (f, r) in mine:
            nb = {f, (f - 1) % n, (f + 1) % n}
            if colour == "W": blocked = any(g in nb and s > r for g, s in theirs)
            else: blocked = any(g in nb and s < r for g, s in theirs)
            prot = False
            if pos.ep and pos.ep[1] == (f, r) and pos.ep[2] != colour:
                prot = any((g, r) in theirs for g in ((f - 1) % n, (f + 1) % n))
            if not blocked and not prot: out.add((colour, f, r))
    return out

def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 2)
    bad_a = bad_b = bad_c = 0; checked_a = checked_b = 0
    for _ in range(N):
        n = rng.choice([5, 6, 7, 9, 12])
        r = rand_pos(n, rng.randrange(4, 2 * n + 2), rng, want_ep=(rng.random() < 0.3))
        if not r: continue
        board, pos = r
        # (c) any-passed agrees
        pp = passed_pawns(board, pos)
        if bool(pp) != (pawns.passed(board, pos, "W") or pawns.passed(board, pos, "B")): bad_c += 1
        # (a) locality of the status: replace all files outside j-1..j+1 by random content and compare the status of the pawn on file j
        for colour, f, rk in list(pp)[:2] if pp else []:
            pass
        for (f, rk) in list(pos.white | pos.black)[:3]:
            col = "W" if (f, rk) in pos.white else "B"
            keep = {f, (f - 1) % n, (f + 1) % n}
            W2 = {s for s in pos.white if s[0] in keep}; B2 = {s for s in pos.black if s[0] in keep}
            for g in range(n):
                if g in keep: continue
                for rr in range(2, 8):
                    if rng.random() < 0.15:
                        if rng.random() < 0.5: W2.add((g, rr))
                        else: B2.add((g, rr))
            W2 -= B2
            ep = pos.ep if (pos.ep and pos.ep[1][0] in keep) else None
            pos2 = Pos(frozenset(W2), frozenset(B2), ep)
            checked_a += 1
            if ((col, f, rk) in passed_pawns(board, pos)) != ((col, f, rk) in passed_pawns(board, pos2)): bad_a += 1
        # (b) after any move from a position without passed pawns
        if pp: continue
        for side in ("W", "B"):
            lp = Pos(pos.white, pos.black, None) if (pos.ep and pos.ep[2] != side) else pos
            for ch in pawns.moves(board, lp, side):
                ch = norm_ep(board, ch)
                changed = set()
                for g in range(n):
                    if {s for s in pos.white if s[0] == g} != {s for s in ch.white if s[0] == g}: changed.add(g)
                    if {s for s in pos.black if s[0] == g} != {s for s in ch.black if s[0] == g}: changed.add(g)
                near = {(g + d) % n for g in changed for d in (-1, 0, 1)}
                lapse = pos.ep[1] if pos.ep else None
                checked_b += 1
                for colour, f, rk in passed_pawns(board, ch):
                    if f not in near and (f, rk) != lapse: bad_b += 1
    print(f"locality checks: (a) status depends on 3 files: {checked_a} pawn checks, violations {bad_a}; "
          f"(b) new passed pawns near changed files: {checked_b} moves, violations {bad_b}; (c) any-passed vs cylcgt: violations {bad_c}")
    return bad_a + bad_b + bad_c

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
