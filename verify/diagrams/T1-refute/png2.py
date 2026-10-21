"""Minimal stdlib PNG decoder (8-bit RGB/RGBA, non-interlaced) -- written fresh for T1-refute."""
import struct, zlib

def read_png(path):
    data = open(path, 'rb').read()
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    pos = 8; idat = b''; w = h = None
    while pos < len(data):
        ln, = struct.unpack('>I', data[pos:pos+4]); typ = data[pos+4:pos+8]
        body = data[pos+8:pos+8+ln]; pos += 12 + ln
        if typ == b'IHDR':
            w, h, bd, ct, _, _, il = struct.unpack('>IIBBBBB', body)
            assert bd == 8 and il == 0 and ct in (2, 6), (bd, ct, il)
            bpp = 3 if ct == 2 else 4
        elif typ == b'IDAT':
            idat += body
        elif typ == b'IEND':
            break
    raw = zlib.decompress(idat)
    stride = w * bpp
    rows = []; prev = bytearray(stride); i = 0
    for y in range(h):
        f = raw[i]; i += 1
        line = bytearray(raw[i:i+stride]); i += stride
        if f == 1:
            for x in range(bpp, stride): line[x] = (line[x] + line[x-bpp]) & 255
        elif f == 2:
            for x in range(stride): line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                a = line[x-bpp] if x >= bpp else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x-bpp] if x >= bpp else 0
                b = prev[x]; c = prev[x-bpp] if x >= bpp else 0
                p = a + b - c; pa = abs(p-a); pb = abs(p-b); pc = abs(p-c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        else:
            assert f == 0, f
        rows.append(bytes(line)); prev = line
    def px(x, y):
        o = x * bpp; r = rows[y]
        return (r[o], r[o+1], r[o+2], r[o+3] if bpp == 4 else 255)
    return w, h, px
