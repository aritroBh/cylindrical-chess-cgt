#!/usr/bin/env python3
"""flipcheck.py BOARD POS RES META OUTPREFIX : flip every position (ranks reversed, colours and side to move swapped),
write the flipped positions for chk/kpp.  Second call (with --compare) compares chk's certificates and kpp's results."""
import sys
def flip_line(line, H):
    t = line.split()
    out = []
    for tok in t:
        if tok in ('w', 'b'):
            out.append('b' if tok == 'w' else 'w')
        elif tok == '-':
            out.append(tok)
        elif tok[0].isalpha() and len(tok) >= 3 and tok[0] in 'KkPp':
            out.append((tok[0].swapcase()) + tok[1] + str(H + 1 - int(tok[2:])))
        else:  # ep square
            out.append(tok[0] + str(H + 1 - int(tok[1:])))
    return " ".join(out)
if sys.argv[1] == '--make':
    H = int(sys.argv[2]); src, dst = sys.argv[3:5]
    with open(dst, 'w') as f:
        for l in open(src):
            f.write(flip_line(l.strip(), H) + "\n")
else:  # --compare H origpos origmeta origres flippos flipcert flipres
    H = int(sys.argv[2]); op, om, orr, fp, fc, fr = sys.argv[3:9]
    n = bad = 0
    sw = {'W': 'L', 'D': 'D', 'L': 'W'}
    for a, b, c, d, e, g in zip(open(op), open(om), open(orr), open(fp), open(fc), open(fr)):
        a = a.strip(); d = d.strip()
        assert flip_line(a, H) == d
        A, B = c.split(' | ')[1].split()
        A2, B2 = g.split(' | ')[1].split()
        mo = sorted(t.split(':')[0] + ':' + t.split(':')[1] for t in b.split(' | ')[1].split())
        mf = sorted(t.split(':')[0] + ':' + t.split(':')[1] for t in e.split(' | ')[1].split() if t != '-')
        def fl(tok):
            col, sq = tok.split(':'); return ('B' if col == 'W' else 'W') + ':' + sq[0] + str(H + 1 - int(sq[1:]))
        n += 1
        if sorted(fl(t) for t in mo) != mf or sw[A] != A2 or sw[B] != B2:
            bad += 1
            if bad < 5: print("DIFF", a, c.strip(), g.strip(), mo, mf)
    print("flipcheck positions", n, "mismatches", bad)
