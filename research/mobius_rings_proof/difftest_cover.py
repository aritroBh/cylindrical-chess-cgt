"""difftest_cover.py SEED COUNT -- coverage of difftest.py's positions (same generator): how many positions have,
in their reachable unreduced tree (moves from non-terminal positions), an e.p. capture, a capture across the seam,
and a move by a pawn whose direction is reversed."""
import sys, random, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgame import Board, code, dirn, col
seed, count = int(sys.argv[1]), int(sys.argv[2]); rnd = random.Random(seed)
tot = ep = seam = rev = 0; k_done = 0
while k_done < count:
    n = rnd.randint(3, 6); k = rnd.randint(2, 6)
    cells = [[0] * 8 for _ in range(n)]
    for _ in range(k):
        f, r = rnd.randrange(n), rnd.randint(2, 7)
        cells[f][r - 1] = code(rnd.randint(0, 1), rnd.choice((1, 1, -1)))
    pos = (tuple(tuple(x) for x in cells), None); B = Board(n)
    if B.passers(pos, 0) or B.passers(pos, 1): continue
    k_done += 1
    seen = {pos}; st = [pos]; f_ep = f_seam = f_rev = False
    while st:
        p = st.pop()
        for side in (0, 1):
            for (f0, r0, kind, f1, r1), ch in B.moves(p, side):
                if kind == 'e': f_ep = True
                if kind in 'xe' and abs(f1 - f0) > 1: f_seam = True
                c = p[0][f0][r0 - 1]
                if dirn(c) != (1 if col(c) == 0 else -1): f_rev = True
                if B.classify(ch, side) == 0 and ch not in seen: seen.add(ch); st.append(ch)
    ep += f_ep; seam += f_seam; rev += f_rev
print('positions %d: with an e.p. capture in the tree %d, with a capture across the seam %d, with a reversed pawn moving %d' % (count, ep, seam, rev))
