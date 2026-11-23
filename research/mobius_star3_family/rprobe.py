import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mobius_rings_proof'))
from mgame import parse_ring
from fgame import FBoard as Board
from rgraph import classify_moves
ring = sys.argv[1]; root = parse_ring(ring); B = Board(len(root[0]))
nodes = {root: 1}; order = [root]; i = 0; t = time.time()
while i < len(order) and time.time() - t < float(sys.argv[2]):
    p = order[i]; i += 1
    for s in (0, 1):
        for ch in classify_moves(B, p, s)[3]:
            if ch not in nodes: nodes[ch] = 1; order.append(ch)
    if i % 500 == 0: print(i, len(order), round(time.time() - t, 1), flush=True)
print('done' if i == len(order) else 'cut', i, len(order), round(time.time() - t, 1))
