"""Stdlib-only PNG decoder: sample background colour near the corners of each square
(avoids piece glyphs) to check which squares are dark, and locate the board frame.
Usage: python pngsample.py <png>"""
import sys, zlib, struct

def load(path):
    data = open(path, 'rb').read()
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    i = 8; idat = b''
    while i < len(data):
        n, = struct.unpack('>I', data[i:i+4]); t = data[i+4:i+8]; c = data[i+8:i+8+n]; i += 12 + n
        if t == b'IHDR':
            w, h, bd, ct, _, _, il = struct.unpack('>IIBBBBB', c)
        elif t == b'IDAT':
            idat += c
    assert bd == 8 and il == 0
    bpp = {2: 3, 6: 4}[ct]
    raw = zlib.decompress(idat); stride = w * bpp
    rows = []; prev = bytearray(stride); p = 0
    for y in range(h):
        f = raw[p]; p += 1; cur = bytearray(raw[p:p+stride]); p += stride
        for x in range(stride):
            a = cur[x-bpp] if x >= bpp else 0; b = prev[x]; cc = prev[x-bpp] if x >= bpp else 0
            if f == 1: cur[x] = (cur[x] + a) & 255
            elif f == 2: cur[x] = (cur[x] + b) & 255
            elif f == 3: cur[x] = (cur[x] + (a + b) // 2) & 255
            elif f == 4:
                pa, pb, pc = abs(b - cc), abs(a - cc), abs(a + b - 2*cc)
                pr = a if pa <= pb and pa <= pc else (b if pb <= pc else cc)
                cur[x] = (cur[x] + pr) & 255
        rows.append(cur); prev = cur
    return w, h, bpp, rows

def px(rows, bpp, x, y):
    r = rows[y]; return tuple(r[x*bpp:x*bpp+3])

def isblue(c):
    return c[2] > c[0] + 40

path = sys.argv[1]
w, h, bpp, rows = load(path)
# find board frame: dark-grey border lines. scan middle row/col for blue/grey runs
midy = h // 2
xs = [x for x in range(w) if isblue(px(rows, bpp, x, midy)) or px(rows,bpp,x,midy)[0] > 220]
ys = [y for y in range(h) if isblue(px(rows, bpp, w//2, y)) or px(rows,bpp,w//2,y)[0] > 220]
# board extents: first/last x where colour is square-like on several rows
def extent(vals):
    return min(vals), max(vals)
x0, x1 = extent([x for x in range(w) if sum(isblue(px(rows,bpp,x,y)) for y in range(0,h,7)) > 3])
y0, y1 = extent([y for y in range(h) if sum(isblue(px(rows,bpp,x,y)) for x in range(0,w,7)) > 3])
sq = (x1 - x0 + 1) / 8
print(f"{path.split('/')[-1]}: {w}x{h} board x[{x0},{x1}] y[{y0},{y1}] square~{sq:.1f}px")
grid = []
for r in range(8):  # r=0 is top row (rank 8)
    line = ''
    for f in range(8):
        cx = int(x0 + f*sq + 0.12*sq); cy = int(y0 + r*sq + 0.12*sq)  # near top-left corner of the square
        line += 'D' if isblue(px(rows,bpp,cx,cy)) else 'L'
    grid.append(line)
for r, line in enumerate(grid):
    print(f"  rank {8-r}: {line}")
print("  a1 is", "dark" if grid[7][0]=='D' else "LIGHT", "; h1 is", "dark" if grid[7][7]=='D' else "light")
ok = all(((r+f)%2==0) == (grid[r][f]=='L') for r in range(8) for f in range(8))
print("  standard checkerboard with a8 light/a1 dark:", ok)
