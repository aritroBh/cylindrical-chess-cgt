"""lemma_test.py SEED COUNT -- random test of Lemmas 2 and 3 ON THE STRIP (own code, sanity only; the lemmas are
proved by hand in PROOF.md).  Random positions: a wall arc of L pattern files (type W2/B4, or its colour reversal
B7/W5) at a random place of the chart (touching the seam at file 0 or the last file, or in the interior), all other
files random (0-2 pawns, either colour, either direction, ranks 2..7, so pawns across the seam interact with the wall
end).  Positions with a passed pawn or a flag are rejected.
Lemma 3: with the arc = c-4..c+5 (L = 10), for each side the K-children of ins_c(p) are the ins_c-images of those of
p and T-moves exist in both or neither.  Lemma 2: every pawn of the arc with pattern neighbour files and a pattern
window has only L or P moves; after any move of a wall pawn with pattern neighbours the mover has no passed pawn.
Control: the same Lemma 3 test with only 4 pattern files around the cut (c-1..c+2) must find mismatches."""
import sys, random, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgame import Board, code
from rgraph import classify_moves, ins

def wall_cell(kind, parity):
    row = [0] * 8
    if kind == 'E':   # W2/B4 wall: B4 on even arc index, W2 on odd
        if parity == 0: row[3] = code(1, -1)
        else: row[1] = code(0, 1)
    else:             # B7/W5 wall (colour reversal)
        if parity == 0: row[6] = code(1, -1)
        else: row[4] = code(0, 1)
    return tuple(row)

def rand_file(rnd):
    row = [0] * 8
    for _ in range(rnd.choice((0, 1, 1, 2))):
        row[rnd.randint(2, 7) - 1] = code(rnd.randint(0, 1), rnd.choice((1, 1, -1)))
    return tuple(row)

def lemma3(B, p, c):
    q = ins(p, c); B2 = Board(B.n + 2)
    for side in (0, 1):
        T1, _, _, K1 = classify_moves(B, p, side); T2, _, _, K2 = classify_moves(B2, q, side)
        if (T1 > 0) != (T2 > 0) or set(ins(x, c) for x in K1) != set(K2): return False
    return True

def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2]); rnd = random.Random(seed)
    stats = dict(pos=0, l3_bad=0, ctrl_pos=0, ctrl_bad=0, l2a=0, l2a_bad=0, l2b=0, l2b_bad=0, seam_touch=0)
    while stats['pos'] < count:
        n = rnd.randint(11, 15); kind = rnd.choice('EO'); L = 10
        start = rnd.choice([0, n - L, rnd.randint(0, n - L)])
        cells = [rand_file(rnd) for _ in range(n)]
        ph = rnd.randint(0, 1)
        for i in range(L): cells[start + i] = wall_cell(kind, (i + ph) % 2)
        p = (tuple(cells), None); B = Board(n)
        if B.passers(p, 0) or B.passers(p, 1): continue
        stats['pos'] += 1; c = start + 4
        if start == 0 or start + L == n: stats['seam_touch'] += 1
        if not lemma3(B, p, c): stats['l3_bad'] += 1; print('L3 MISMATCH', p, c)
        # Lemma 2 on the pawns of the arc
        arc = set(range(start, start + L))
        for side in (0, 1):
            for d, ch in B.moves(p, side):
                j = d[0]
                if not {j - 1, j, j + 1} <= arc: continue
                stats['l2a'] += 1
                if B.passers(ch, side): stats['l2a_bad'] += 1; print('L2a FAIL', p, d)
                if set(range(j - 1, j + 4)) <= arc or set(range(j - 3, j + 2)) <= arc:
                    stats['l2b'] += 1
                    cl = B.classify(ch, side)
                    if cl > 0 or (cl == 0 and not any(B.classify(g, 1 - side) > 0 for _, g in B.moves(ch, 1 - side))):
                        stats['l2b_bad'] += 1; print('L2b FAIL', p, d)
        # control: destroy the pattern outside c-1..c+2
        for _try in range(30):
            cc = list(cells)
            for f in (c - 4, c - 3, c - 2, c + 3, c + 4, c + 5): cc[f] = rand_file(rnd)
            p2 = (tuple(cc), None)
            if not (B.passers(p2, 0) or B.passers(p2, 1)):
                stats['ctrl_pos'] += 1
                if not lemma3(B, p2, c): stats['ctrl_bad'] += 1
                break
    print(stats)

if __name__ == '__main__':
    main()
