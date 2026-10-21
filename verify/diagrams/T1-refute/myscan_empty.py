"""T1-refute: independent pixel transcription of the 12 board diagrams.
Own PNG decoder (png2.py), no project code imported.
Run: cd verify/diagrams/T1-refute && ../../../.venv/bin/python -I myscan.py
"""
import sys, collections
sys.path.insert(0, '.')
from png2 import read_png

PIC = '../../../prior_work/Pictures/'
IMGS = [('2.1', 'ZeroGame1'), ('2.2', 'ZeroGame2'), ('2.3', 'ZeroGame3'), ('3.1', 'OneGame1'),
        ('3.2', 'TwoGame1'), ('4.1', 'StarGame1'), ('4.2', 'UpGame1'), ('4.3', 'TinyGame1'),
        ('5.1', 'TrebuchetPosition1'), ('7.1', 'ChessPuzzle1'), ('7.2', 'ChessPuzzle2'), ('7.3', 'ChessPuzzle3')]
FILES = 'abcdefgh'

def near(c, ref, tol):
    return all(abs(c[i] - ref[i]) <= tol for i in range(3))

def scan(key, stem):
    w, h, px = read_png(PIC + stem + '.png')
    cnt = collections.Counter(px(x, y)[:3] for y in range(0, h, 3) for x in range(0, w, 3))
    L = next(c for c, _ in cnt.most_common() if min(c) > 200 and max(c) < 250 and max(c) - min(c) < 6)
    D = next(c for c, _ in cnt.most_common() if c[2] > c[0] + 40)
    # board bbox: rows/cols containing many L or D pixels
    def isbg(c): return near(c, L, 4) or near(c, D, 4)
    colhits = [sum(isbg(px(x, y)) for y in range(0, h, 2)) for x in range(w)]
    rowhits = [sum(isbg(px(x, y)) for x in range(0, w, 2)) for y in range(h)]
    thr_c = 0.3 * max(colhits); thr_r = 0.3 * max(rowhits)
    xs = [x for x in range(w) if colhits[x] > thr_c]; ys = [y for y in range(h) if rowhits[y] > thr_r]
    x0, x1, y0, y1 = xs[0], xs[-1], ys[0], ys[-1]
    sw = (x1 - x0 + 1) / 8; sh = (y1 - y0 + 1) / 8
    pieces = {}; parity_bad = []; feats = {}; emp = []
    for fi in range(8):
        for ri in range(8):          # ri=0 is top row (rank 8)
            rank = 8 - ri
            ax0 = int(x0 + fi * sw); ax1 = int(x0 + (fi + 1) * sw); ay0 = int(y0 + ri * sh); ay1 = int(y0 + (ri + 1) * sh)
            inset = int(0.06 * sw)
            nL = nD = nW = nB = nO = 0; minx = miny = 10**9; maxx = maxy = -1
            for y in range(ay0 + inset, ay1 - inset):
                for x in range(ax0 + inset, ax1 - inset):
                    c = px(x, y)
                    if near(c, L, 4): nL += 1; continue
                    if near(c, D, 4): nD += 1; continue
                    if min(c[:3]) >= 248: nW += 1
                    elif max(c[:3]) <= 45: nB += 1
                    else: nO += 1
                    minx = min(minx, x); maxx = max(maxx, x); miny = min(miny, y); maxy = max(maxy, y)
            area = (ax1 - ax0 - 2 * inset) * (ay1 - ay0 - 2 * inset)
            dark_expected = (fi + rank) % 2 == 0   # a1 (0,1) -> odd -> ... a1 dark iff (file+rank) even with file a=1
            dark_expected = ((fi + 1) + rank) % 2 == 0
            bgdark = nD > nL
            if bgdark != dark_expected:
                parity_bad.append(f'{FILES[fi]}{rank}')
            piece_frac = (nW + nB + nO) / area
            emp.append(piece_frac) if piece_frac <= 0.03 else None
            if piece_frac > 0.03:
                colour = 'W' if nW > nB else 'B'
                bw = (maxx - minx + 1) / sw; bh = (maxy - miny + 1) / sh
                feats[f'{FILES[fi]}{rank}'] = (colour, round(piece_frac, 3), round(nW / area, 3), round(nB / area, 3), round(bw, 2), round(bh, 2))
    print(key, "empty squares:", len(emp), "max non-bg fraction on an empty square:", round(max(emp), 4)); return (w, h, L, D, (x0, x1, y0, y1), parity_bad, feats)

def main():
    allfeats = {}
    for key, stem in IMGS:
        w, h, L, D, bb, bad, feats = scan(key, stem)
        print(f'{key} {stem}.png {w}x{h} L={L} D={D} board x[{bb[0]},{bb[1]}] y[{bb[2]},{bb[3]}] '
              f'sq={((bb[1]-bb[0]+1)/8):.1f}x{((bb[3]-bb[2]+1)/8):.1f} parity_mismatch={bad}')
        for sq, f in sorted(feats.items()):
            print(f'    {sq}: colour={f[0]} frac={f[1]} white={f[2]} black={f[3]} bbox_w={f[4]} bbox_h={f[5]}')
        allfeats[key] = feats
    return allfeats

if __name__ == '__main__':
    main()
