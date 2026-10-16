"""T1-refute: independent pixel-level transcription of the 12 paper diagrams.

Stdlib only (zlib PNG decoder written here). Imports nothing from cylcgt/ or verify/diagrams/.
For each diagram:
  1. decode the PNG;
  2. find the board as the bounding box of the blue (dark-square) pixels;
     (a1 and h8 are dark squares, so this box is the whole 8x8 board if a1 is dark);
  3. in every square, count pure-white pixels (piece fill of a white piece) and near-black
     pixels (outline / fill), and measure the bounding box of piece pixels;
  4. classify: empty / white / black, pawn / king (king is wider and taller than a pawn).
Then CLAIMS is read from cylcgt/verify_paper.py with ast (not imported) and compared as sets.

Run: cd /Users/aritro/Downloads/Research/Chessendgames && python3 -I verify/diagrams/T1-refute/pixscan.py
"""
import ast
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PICS = ROOT / "prior_work" / "Pictures"


def read_png(path):
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    i = 8
    idat = b""
    while i < len(data):
        n = struct.unpack(">I", data[i:i + 4])[0]
        typ = data[i + 4:i + 8]
        body = data[i + 8:i + 8 + n]
        if typ == b"IHDR":
            w, h, bd, ct, cm, fm, il = struct.unpack(">IIBBBBB", body)
            assert bd == 8 and il == 0 and ct in (2, 6), (bd, ct, il)
        elif typ == b"IDAT":
            idat += body
        i += 12 + n
    bpp = 4 if ct == 6 else 3
    raw = zlib.decompress(idat)
    stride = w * bpp
    rows = []
    prev = bytearray(stride)
    p = 0
    for y in range(h):
        f = raw[p]
        p += 1
        cur = bytearray(raw[p:p + stride])
        p += stride
        if f == 1:
            for x in range(bpp, stride):
                cur[x] = (cur[x] + cur[x - bpp]) & 255
        elif f == 2:
            for x in range(stride):
                cur[x] = (cur[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                a = cur[x - bpp] if x >= bpp else 0
                cur[x] = (cur[x] + ((a + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                a = cur[x - bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x - bpp] if x >= bpp else 0
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                cur[x] = (cur[x] + pr) & 255
        rows.append(bytes(cur))
        prev = cur
    def px(x, y):
        r = rows[y]
        o = x * bpp
        return r[o], r[o + 1], r[o + 2]
    return w, h, px


def is_blue(c):
    r, g, b = c
    return 90 <= r <= 130 and 115 <= g <= 155 and 165 <= b <= 205 and b - r > 50


def is_light(c):
    r, g, b = c
    return 225 <= r <= 245 and 225 <= g <= 245 and 225 <= b <= 245 and max(c) - min(c) < 6


def is_white(c):
    return min(c) >= 250


def is_black(c):
    return max(c) <= 70


EMPTY_MAX = [0.0]


def scan(path):
    w, h, px = read_png(path)
    # board box from blue pixels (sample every pixel; images are small)
    xs, ys = [], []
    minx = miny = 10 ** 9
    maxx = maxy = -1
    for y in range(h):
        for x in range(w):
            if is_blue(px(x, y)):
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y
    W = maxx - minx + 1
    H = maxy - miny + 1
    sq = W / 8.0
    sqh = H / 8.0
    out = {}
    colour_check = {}
    for fi in range(8):
        for ri in range(8):  # ri=0 top row (rank 8)
            x0 = minx + fi * sq
            y0 = miny + ri * sqh
            # background colour at a corner region of the square (4..10% in)
            bx, by = int(x0 + 0.05 * sq), int(y0 + 0.05 * sqh)
            bg = px(bx, by)
            rank = 8 - ri
            name = "abcdefgh"[fi] + str(rank)
            colour_check[name] = "dark" if is_blue(bg) else ("light" if is_light(bg) else f"?{bg}")
            nw = nb = 0
            pxs = []
            for y in range(int(y0 + 0.04 * sqh), int(y0 + 0.96 * sqh)):
                for x in range(int(x0 + 0.04 * sq), int(x0 + 0.96 * sq)):
                    c = px(x, y)
                    if is_white(c):
                        nw += 1
                        pxs.append((x, y))
                    elif is_black(c):
                        nb += 1
                        pxs.append((x, y))
            area = sq * sqh
            if (nw + nb) / area < 0.03:
                EMPTY_MAX[0] = max(EMPTY_MAX[0], (nw + nb) / area)
                continue
            bxs = [p[0] for p in pxs]
            bys = [p[1] for p in pxs]
            bw = (max(bxs) - min(bxs) + 1) / sq
            bh = (max(bys) - min(bys) + 1) / sqh
            colour = "W" if nw > nb else "B"
            kind = "K" if bw > 0.66 else "P"
            out[name] = (colour, kind, round(nw / area, 3), round(nb / area, 3), round(bw, 2), round(bh, 2))
    return (w, h, minx, miny, maxx, maxy), out, colour_check


DIAGRAMS = [
    ("2.1", "ZeroGame1.png"), ("2.2", "ZeroGame2.png"), ("2.3", "ZeroGame3.png"),
    ("3.1", "OneGame1.png"), ("3.2", "TwoGame1.png"), ("4.1", "StarGame1.png"),
    ("4.2", "UpGame1.png"), ("4.3", "TinyGame1.png"), ("5.1", "TrebuchetPosition1.png"),
    ("7.1", "ChessPuzzle1.png"), ("7.2", "ChessPuzzle2.png"), ("7.3", "ChessPuzzle3.png"),
]


def load_claims():
    src = (ROOT / "cylcgt" / "verify_paper.py").read_text()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "CLAIMS" for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit("CLAIMS not found")


def parse_pos(text):
    wpart, bpart = text.split("/")
    w = set(wpart.split(":")[1].split())
    b = set(bpart.split(":")[1].split())
    return w, b


def main():
    claims = load_claims()
    by_key = {}
    for label, text, val in claims:
        by_key.setdefault(label.split()[0], []).append((label, text, val))
    scanned = {}
    for key, fn in DIAGRAMS:
        box, pieces, cc = scan(PICS / fn)
        # checkerboard sanity: a1 dark, and colour alternates
        bad = [s for s, c in cc.items()
               if c != ("dark" if (("abcdefgh".index(s[0]) + int(s[1])) % 2 == 1) else "light")]
        scanned[key] = pieces
        print(f"    max piece-pixel fraction over empty squares so far: {EMPTY_MAX[0]:.4f}")
        wp = sorted(s for s, v in pieces.items() if v[:2] == ("W", "P"))
        bp = sorted(s for s, v in pieces.items() if v[:2] == ("B", "P"))
        ks = {s: v[0] + v[1] for s, v in pieces.items() if v[1] == "K"}
        print(f"{key} {fn}: img {box[0]}x{box[1]} board x[{box[2]},{box[4]}] y[{box[3]},{box[5]}] "
              f"a1={cc['a1']} checkerboard_mismatches={bad}")
        print(f"    W pawns {wp}  B pawns {bp}  kings {ks}")
        for s, v in sorted(pieces.items()):
            print(f"      {s}: {v}")
        if key not in by_key:
            print(f"    -> no CLAIMS entry for {key}")
            continue
        for label, text, val in by_key[key]:
            cw, cb = parse_pos(text)
            ow, ob = set(wp), set(bp)
            print(f"    CLAIMS '{label}': W {sorted(cw)} B {sorted(cb)}")
            print(f"      only in scan: W {sorted(ow - cw)} B {sorted(ob - cb)};"
                  f" only in CLAIMS: W {sorted(cw - ow)} B {sorted(cb - ob)}")


if __name__ == "__main__":
    main()
