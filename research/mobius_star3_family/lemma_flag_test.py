"""lemma_flag_test.py SEED COUNT -- random sanity test of the insertion step (Lemma 3 of research/mobius_rings_proof)
in the form needed here: positions WITH an e.p. flag whose victim lies outside the ten-file arc c-4..c+5.
Positions: a type-E (W2/B4) or type-O (B7/W5) arc of 10 pattern files somewhere on the chart (touching the seam or
not), other files random; then a random double step of a pawn on a far file is played, so the child has a flag
(kept only if some enemy pawn can take e.p.). Test, for both sides to move: K-children of ins_c(p) = ins_c-images of
the K-children of p, T-move existence equal. Positions with a passed pawn are skipped."""
import sys, random, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mobius_rings_proof'))
from mgame import code
from fgame import FBoard
from rgraph import classify_moves, ins
from lemma_test import wall_cell
def rand_file(rnd):
    row = [0] * 8
    for _ in range(rnd.choice((0, 1, 1, 2))):
        row[rnd.randint(2, 7) - 1] = code(rnd.randint(0, 1), rnd.choice((1, 1, -1)))
    # sometimes a pawn on its home rank, to allow double steps
    if rnd.random() < 0.5:
        if rnd.random() < 0.5: row[1] = code(0, 1)
        else: row[6] = code(1, -1)
    return tuple(row)
def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2]); rnd = random.Random(seed)
    st = dict(pos=0, bad=0, seam_touch=0, tries=0)
    while st['pos'] < count:
        st['tries'] += 1
        n = rnd.randint(12, 15); kind = rnd.choice('EO'); L = 10
        start = rnd.choice([0, n - L, rnd.randint(0, n - L)])
        cells = [rand_file(rnd) for _ in range(n)]; ph = rnd.randint(0, 1)
        arc = set(range(start, start + L))
        for i in range(L): cells[start + i] = wall_cell(kind, (i + ph) % 2)
        p0 = (tuple(cells), None); B = FBoard(n)
        if B.passers(p0, 0) or B.passers(p0, 1): continue
        side = rnd.randint(0, 1)
        ds = [ch for d, ch in B.moves(p0, side) if d[2] == 'd' and d[0] not in arc and ch[1]]
        if not ds: continue
        p = rnd.choice(ds)
        if B.passers(p, 0) or B.passers(p, 1): continue
        c = start + 4; q = ins(p, c); B2 = FBoard(n + 2)
        st['pos'] += 1
        if start == 0 or start + L == n: st['seam_touch'] += 1
        for s in (0, 1):
            T1, _, _, K1 = classify_moves(B, p, s); T2, _, _, K2 = classify_moves(B2, q, s)
            if (T1 > 0) != (T2 > 0) or set(ins(x, c) for x in K1) != set(K2):
                st['bad'] += 1; print('MISMATCH side', s, p, c); break
    print(st)
main()
