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

