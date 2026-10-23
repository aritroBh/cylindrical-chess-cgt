# Which moves from reduced-game nodes are captures, how do they classify, and do they split the ring (empty file)?
import sys
from collections import Counter
from eng import *
from red import build
def run(kind, n):
    pos0 = ring(kind, n); ids, order, info = build(pos0)
    cnt = Counter(); split_cnt = Counter(); k_caps = 0
    for (pos, ep) in order:
        for side in 'WB':
            cl = classify_moves(pos, ep, side)
            for k, np_, ne in cl:
                occ0 = sum(1 for w, b in pos if w | b)
                occ1 = sum(1 for w, b in np_ if w | b)
                npaw0 = npawns(pos); npaw1 = npawns(np_)
                is_cap = npaw1 < npaw0
                if is_cap:
                    cnt[k] += 1
                    if occ1 < occ0: split_cnt[k] += 1
                else:
                    if occ1 < occ0: split_cnt['nonCapSplit'] += 1
    print(kind, n, 'nodes', len(order), 'capture moves by class', dict(cnt), 'of which empty a file (ring splits)', dict(split_cnt))
run('O', 17); run('E', 16)
