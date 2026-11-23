"""difftest.py SEED COUNT -- differential test of mgame.py against research/mobius_rings_n/bin/mob2_32 (C2 of the
earlier report): random strip positions (n = 3..6 files, 2..6 pawns, both colours, either direction, ranks 2..7),
no passed pawn at the root; outcome of G + *h, h = 0..3, by an unreduced search in mgame (own code) and by mob2.
Also, for each such position, the signature of the REDUCED game (rgraph.py) is compared: this tests Lemma 1."""
import sys, random, subprocess, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgame import Board, fmt, code
from rgraph import classify_moves

def unreduced(B, root, H=3):
    memo = {}
    def win(p, side, h):
        k = (p, side, h)
        if k in memo: return memo[k]
        w = False
        for _, ch in B.moves(p, side):
            c = B.classify(ch, side)
            if c > 0 or (c == 0 and not win(ch, 1 - side, h)): w = True; break
        if not w: w = any(not win(p, 1 - side, g) for g in range(h))
        memo[k] = w; return w
    return ''.join('N' if win(root, 0, h) and win(root, 1, h) else 'L' if win(root, 0, h) else
                   'R' if win(root, 1, h) else 'P' for h in range(H + 1))

def reduced_sig(B, root, H=3):
    nodes = {}; order = [root]; seen = {root}
    while order:
        p = order.pop()
        nodes[p] = [classify_moves(B, p, s) for s in (0, 1)]
        for s in (0, 1):
            for ch in nodes[p][s][3]:
                if ch not in seen: seen.add(ch); order.append(ch)
    memo = {}
    def win(p, side, h):
        k = (p, side, h)
        if k in memo: return memo[k]
        T, L, P, K = nodes[p][side]
        w = T > 0 or any(not win(c, 1 - side, h) for c in K) or any(not win(p, 1 - side, g) for g in range(h))
        memo[k] = w; return w
    return ''.join('N' if win(root, 0, h) and win(root, 1, h) else 'L' if win(root, 0, h) else
                   'R' if win(root, 1, h) else 'P' for h in range(H + 1))

def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2]); rnd = random.Random(seed)
    mob2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../mobius_rings_n/bin/mob2_32')
    pos_list = []
    while len(pos_list) < count:
        n = rnd.randint(3, 6); k = rnd.randint(2, 6)
        cells = [[0] * 8 for _ in range(n)]
        for _ in range(k):
            f, r = rnd.randrange(n), rnd.randint(2, 7)
            cells[f][r - 1] = code(rnd.randint(0, 1), rnd.choice((1, 1, -1)))
        pos = (tuple(tuple(x) for x in cells), None); B = Board(n)
        if B.passers(pos, 0) or B.passers(pos, 1): continue
        pos_list.append((B, pos))
    # one mob2 process per width: mob2's memo table is keyed by the cell array only, not by the width, so a batch
    # that mixes widths can reuse an entry of another width (seen once: 'W5 B6 w7 -' after a 3-file position).
    out = [None] * len(pos_list)
    for n in sorted({B.n for B, _ in pos_list}):
        idx = [i for i, (B, _) in enumerate(pos_list) if B.n == n]
        inp = '\n'.join(fmt(pos_list[i][1]) for i in idx) + '\n'
        res = subprocess.run(['nice', '-n', '15', mob2, 'solve'], input=inp, capture_output=True, text=True).stdout.split()
        for i, o in zip(idx, res): out[i] = o
    bad = badred = 0
    for (B, p), o in zip(pos_list, out):
        u = unreduced(B, p); r = reduced_sig(B, p)
        if u != o: bad += 1; print('DIFF mob2', fmt(p), 'mine', u, 'mob2', o)
        if r != u: badred += 1; print('DIFF reduced', fmt(p), 'unreduced', u, 'reduced', r)
    import collections; print('signature histogram', dict(collections.Counter(out)))
    print('positions %d  mgame-unreduced vs mob2 mismatches %d  reduced vs unreduced mismatches %d' % (len(pos_list), bad, badred))

if __name__ == '__main__':
    main()
