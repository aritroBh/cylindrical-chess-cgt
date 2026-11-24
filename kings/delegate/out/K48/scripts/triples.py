# file triples {f1<f2<f3} with f3-f1 <= 5 on a flat board of width W, one per left-right reflection class
import sys
W = int(sys.argv[1]); out = []
for a in range(W):
    for b in range(a + 1, W):
        for c in range(b + 1, min(a + 6, W)):
            t = (a, b, c); m = tuple(sorted(W - 1 - x for x in t))
            if t <= m: out.append(t)
for t in out: print('%d,%d,%d' % t)
