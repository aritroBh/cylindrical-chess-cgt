#!/usr/bin/env python3
"""Collect nimber>=3 / near hits from h4 outputs, canonicalise (file mirror, colour reversal, shift to file a), dedupe."""
import re, sys, glob, collections

def parse(pos):
    m = re.match(r'W:\s*(.*?)\s*/\s*B:\s*(.*)$', pos)
    w = [(ord(t[0]) - 97, int(t[1:])) for t in m.group(1).split()]
    b = [(ord(t[0]) - 97, int(t[1:])) for t in m.group(2).split()]
    return w, b

def fmt(w, b):
    nm = lambda s: f"{chr(97 + s[0])}{s[1]}"
    return "W: " + " ".join(map(nm, sorted(w))) + " / B: " + " ".join(map(nm, sorted(b)))

def canon(pos, ring=None):
    w, b = parse(pos)
    cands = []
    for col in (0, 1):
        ww, bb = (w, b) if not col else ([(f, 9 - r) for f, r in b], [(f, 9 - r) for f, r in w])
        allf = [f for f, _ in ww + bb]
        for mir in (0, 1):
            if ring:
                for rot in range(ring):
                    w2 = [(((-f if mir else f) + rot) % ring, r) for f, r in ww]
                    b2 = [(((-f if mir else f) + rot) % ring, r) for f, r in bb]
                    cands.append(fmt(w2, b2))
            else:
                lo, hi = min(allf), max(allf)
                w2 = [((hi - f) if mir else (f - lo), r) for f, r in ww]
                b2 = [((hi - f) if mir else (f - lo), r) for f, r in bb]
                cands.append(fmt(w2, b2))
    return min(cands)

if __name__ == '__main__':
    kind = sys.argv[1]  # 'nim' or 'near'
    thr = int(sys.argv[2])
    ring = int(sys.argv[3]) or None
    files = sys.argv[4:]
    seen = {}
    for f in files:
        for line in open(f):
            parts = line.rstrip('\n').split('\t')
            if kind == 'nim':
                # ext format: tag pos n outcome nim=K m=.. ; scan format: pos width n outcome nim
                if len(parts) >= 5 and parts[4].startswith('nim='):
                    pos, n, k = parts[1], int(parts[2]), int(parts[4][4:])
                elif len(parts) == 5 and parts[0].startswith('W:') and parts[4].lstrip('-').isdigit():
                    pos, n, k = parts[0], int(parts[2]), int(parts[4])
                else:
                    continue
                if k >= thr:
                    c = canon(pos, ring)
                    seen.setdefault(c, (n, k))
            else:
                if parts[0].startswith('NEAR') and int(parts[0][4:]) >= thr:
                    pos = parts[1]
                    c = canon(pos, ring)
                    seen.setdefault(c, (int(parts[2]), parts[0] + ' ' + parts[3]))
    byn = collections.Counter(v[0] for v in seen.values())
    for c, v in sorted(seen.items(), key=lambda kv: (kv[1][0], kv[0])):
        print(f"{c}\t{v[0]}\t{v[1]}")
    print('#', len(seen), 'canonical positions; by pawn count', dict(sorted(byn.items())), file=sys.stderr)
