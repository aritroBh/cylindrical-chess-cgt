"""Adversarial check of claim T1 (diagram transcription), independent of the worker's eyes.

Decodes each diagram PNG with the stdlib only (zlib), locates the board from the
blue dark-square pixels, splits it into 8x8 cells, and classifies each cell by
pixel counts:
  - near-black pixels (outline / black piece fill)
  - pure-white pixels (white piece fill; light squares are ~#eee, not #fff)
Piece colour: black piece = many black, few white; white piece = many white.
Piece type: king vs pawn by total glyph-pixel area (king glyph is much larger).
Also reports whether a1 is a dark square (orientation sanity).

Then compares the resulting FEN board part with MINE in verify/diagrams/rerun.py
and with cylcgt.verify_paper.CLAIMS.

Run from project root:
  PYTHONPATH=. .venv/bin/python verify/diagrams/T1-reproduce/pixel_transcribe.py
"""
from __future__ import annotations

import importlib.util
import struct
import sys
import zlib

PIC = "prior_work/Pictures/"
DIAGRAMS = {
    "2.1": "ZeroGame1.png", "2.2": "ZeroGame2.png", "2.3": "ZeroGame3.png",
    "3.1": "OneGame1.png", "3.2": "TwoGame1.png",
    "4.1": "StarGame1.png", "4.2": "UpGame1.png", "4.3": "TinyGame1.png",
    "5.1": "TrebuchetPosition1.png",
    "7.1": "ChessPuzzle1.png", "7.2": "ChessPuzzle2.png", "7.3": "ChessPuzzle3.png",
}


def decode_png(path):
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    pos = 8
    idat = b""
    while pos < len(data):
        ln, typ = struct.unpack(">I4s", data[pos:pos + 8])
        chunk = data[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            w, h, bd, ct, _, _, il = struct.unpack(">IIBBBBB", chunk)
        elif typ == b"IDAT":
            idat += chunk
        pos += 12 + ln
    assert bd == 8 and il == 0 and ct in (2, 6), (bd, ct, il)
    bpp = 4 if ct == 6 else 3
    raw = zlib.decompress(idat)
    stride = w * bpp
    rows = []
    prev = bytearray(stride)
    i = 0
    for _ in range(h):
        ft = raw[i]
        i += 1
        line = bytearray(raw[i:i + stride])
        i += stride
        if ft == 1:
            for x in range(bpp, stride):
                line[x] = (line[x] + line[x - bpp]) & 255
        elif ft == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 255
        elif ft == 3:
            for x in range(stride):
                a = line[x - bpp] if x >= bpp else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 255
        elif ft == 4:
            for x in range(stride):
                a = line[x - bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x - bpp] if x >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        rows.append(line)
        prev = line
    def px(x, y):
        o = x * bpp
        r = rows[y]
        return r[o], r[o + 1], r[o + 2], (r[o + 3] if bpp == 4 else 255)
    return w, h, px


def is_blue(p):
    r, g, b, a = p
    return a > 200 and b > 150 and r < 140 and 100 < g < 160 and b - r > 50


def is_black(p):
    r, g, b, a = p
    return a > 200 and r < 60 and g < 60 and b < 60


def is_white(p):
    r, g, b, a = p
    return a > 200 and r >= 250 and g >= 250 and b >= 250


def transcribe(path):
    w, h, px = decode_png(path)
    xs, ys = [], []
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if is_blue(px(x, y)):
                xs.append(x)
                ys.append(y)
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    cw, ch = (x1 - x0) / 8, (y1 - y0) / 8
    board = {}
    stats = {}
    sq_dark = {}
    for row in range(8):          # row 0 = top = rank 8
        for col in range(8):      # col 0 = left = file a
            cx0 = int(x0 + col * cw + 0.08 * cw)
            cx1 = int(x0 + (col + 1) * cw - 0.08 * cw)
            cy0 = int(y0 + row * ch + 0.04 * ch)
            cy1 = int(y0 + (row + 1) * ch - 0.04 * ch)
            nb = nw = nblue = n = 0
            for y in range(cy0, cy1):
                for x in range(cx0, cx1):
                    p = px(x, y)
                    n += 1
                    nb += is_black(p)
                    nw += is_white(p)
                    nblue += is_blue(p)
            rank = 8 - row
            sq = "abcdefgh"[col] + str(rank)
            sq_dark[sq] = nblue > 0.3 * n
            fb, fw = nb / n, nw / n
            stats[sq] = (round(fb, 3), round(fw, 3))
            if fb < 0.01:
                continue
            colour = "W" if fw > 0.7 * fb else "B"  # black king glyph has small white inner details
            area = fb + fw
            kind = "K" if area > 0.30 else "P"
            board[sq] = kind if colour == "W" else kind.lower()
    return board, stats, sq_dark


def to_fen(board):
    out = []
    for rank in range(8, 0, -1):
        s, e = "", 0
        for f in "abcdefgh":
            c = board.get(f"{f}{rank}")
            if c:
                if e:
                    s += str(e)
                    e = 0
                s += c
            else:
                e += 1
        if e:
            s += str(e)
        out.append(s)
    return "/".join(out)


def main():
    spec = importlib.util.spec_from_file_location("rerun", "verify/diagrams/rerun.py")
    rerun = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rerun)
    MINE = rerun.MINE
    from cylcgt.verify_paper import CLAIMS
    from cylcgt.pawns import Pos
    allok = True
    for key, fn in DIAGRAMS.items():
        board, stats, dark = transcribe(PIC + fn)
        fen = to_fen(board)
        ok = fen == MINE[key]
        allok &= ok
        orient = "a1 dark" if dark["a1"] and not dark["a8"] and dark["h8"] and not dark["h1"] else "ORIENTATION?"
        print(f"{key:4s} {fn:24s} pixel-FEN {fen:40s} worker-MINE {'SAME' if ok else 'DIFFERENT: ' + MINE[key]}  [{orient}]")
        for sq in sorted(board):
            print(f"       {sq}={board[sq]} black-frac {stats[sq][0]} white-frac {stats[sq][1]}")
    print("\nAll pixel transcriptions equal worker's MINE:", allok)
    # Cross-check pixel transcription against CLAIMS (pawns only), full-position entries
    print("\nPixel transcription vs CLAIMS (pawn sets):")
    for label, text, claim in CLAIMS:
        key = label.split()[0]
        board, _, _ = transcribe(PIC + DIAGRAMS[key])
        cp = Pos.parse(text)
        fs = {f for f, _ in cp.white | cp.black}
        def sq2(s):
            return ("abcdefgh".index(s[0]), int(s[1:]))
        W = {sq2(s) for s, c in board.items() if c == "P"}
        B = {sq2(s) for s, c in board.items() if c == "p"}
        Wf = {s for s in W if s[0] in fs}
        Bf = {s for s in B if s[0] in fs}
        full = (W == set(cp.white) and B == set(cp.black))
        onfiles = (Wf == set(cp.white) and Bf == set(cp.black))
        name = lambda S: " ".join(sorted("abcdefgh"[f] + str(r) for f, r in S))
        print(f"  {label:32s} full-board-equal={full}  equal-on-its-files={onfiles}"
              + ("" if full else f"  | diagram-only W[{name(W - set(cp.white))}] B[{name(B - set(cp.black))}]"
                                 f" claims-only W[{name(set(cp.white) - W)}] B[{name(set(cp.black) - B)}]"))


if __name__ == "__main__":
    main()
