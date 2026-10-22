import itertools, sys
sys.path.insert(0, "research/ring_family")
from ringlib import *
# all file contents with <=3 pawns, W ranks in 2..6, B ranks in 3..7
def contents(maxp=3, minp=1):
    out = []
    for nw in range(0, 4):
        for ws in itertools.combinations(range(2, 7), nw):
            for nb in range(0, 4):
                for bs in itertools.combinations(range(3, 8), nb):
                    if minp <= nw + nb <= maxp and not (set(ws) & set(bs)): out.append((ws, bs))
    return out
if __name__ == "__main__":
    C = contents()
    print(len(C))
    tot = 0
    by = {}
    for c in C: by.setdefault(len(c[0]) + len(c[1]), []).append(c)
    print({k: len(v) for k, v in by.items()})
    # 3-file cores with 6 pawns total
    cnt = 0
    for p1 in range(1, 4):
        for p2 in range(1, 4):
            p3 = 6 - p1 - p2
            if 1 <= p3 <= 3:
                cnt += len(by[p1]) * len(by[p2]) * len(by[p3])
    print("3-file cores with 6 pawns:", cnt)
    
