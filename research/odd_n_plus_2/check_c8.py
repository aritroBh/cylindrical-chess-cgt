#!/usr/bin/env python3
"""Preflight the C8 reference hits against the C9 core-plus-wall predicates."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HITS = ROOT / "research/star26_rings/c8/p10_5_5_hits.tsv"


def parse(text, n=8):
    w, b = [0] * n, [0] * n
    sides = re.split(r"\s*/\s*", text)
    assert len(sides) == 2
    for side, target in zip(sides, (w, b)):
        for file_, rank in re.findall(r"([a-i])([1-8])", side):
            target[ord(file_) - ord("a")] |= 1 << int(rank)
    return tuple(zip(w, b))


def no_passer(board):
    n = len(board)
    for f, (wm, bm) in enumerate(board):
        neigh = ((f - 1) % n, f, (f + 1) % n)
        enemy_b = board[neigh[0]][1] | bm | board[neigh[2]][1]
        enemy_w = board[neigh[0]][0] | wm | board[neigh[2]][0]
        for r in range(2, 8):
            if wm & (1 << r) and not enemy_b >> (r + 1):
                return False
            if bm & (1 << r) and not (enemy_w & ((1 << r) - 1)):
                return False
    return True


def descriptors(board, offsets=(2,)):
    n = len(board)
    out = []
    for width in range(4, 8):
        for phase in range(2):
            for white_rank in range(2, 6):
              for offset in offsets:
                if white_rank + offset > 7:
                    continue
                ok = True
                for j, f in enumerate(range(width, n)):
                    w, b = board[f]
                    is_white = (j + phase) % 2 == 0
                    expected = ((1 << white_rank), 0) if is_white else (0, 1 << (white_rank + offset))
                    if (w, b) != expected:
                        ok = False
                        break
                if ok:
                    out.append((width, offset, white_rank, phase))
    return out


def transforms(board):
    n = len(board)
    for reflected in (False, True):
        for rotation in range(n):
            for color_reversed in (False, True):
                row = []
                for j in range(n):
                    src = (rotation - j) % n if reflected else (rotation + j) % n
                    w, b = board[src]
                    if color_reversed:
                        flip = lambda x: sum(1 << (9-r) for r in range(1, 9) if x & (1 << r))
                        w, b = flip(b), flip(w)
                    row.append((w, b))
                yield tuple(row)


def key_order(desc):
    width, offset, rank, phase = desc
    return (width, 0 if offset == 2 else offset, rank, phase)


def canonical(board):
    options = [(t, d) for t in transforms(board) for d in descriptors(t, (1, 2, 3))]
    return min(options, key=lambda x: (key_order(x[1]), x[0]))


def main():
    rows = [line.rstrip("\n").split("\t") for line in HITS.read_text().splitlines()]
    checked, excluded, keys_by_width = [], [], {}
    for i, row in enumerate(rows, 1):
        pos = parse(row[0])
        desc = [(t, d) for t in transforms(pos) for d in descriptors(t)]
        if desc and no_passer(pos):
            checked.append(i)
            t, d = canonical(pos)
            keys_by_width.setdefault(d[0], set()).add((t, d))
        else:
            excluded.append(i)
    assert len(rows) == 20
    assert checked == list(range(1, 21)), (checked, excluded)
    one_file = any(d[0] == 7 and d[2] == 5 for t in transforms(parse(rows[13][0])) for d in descriptors(t))
    assert one_file
    print(f"C8 reference hits: {len(checked)}/{len(rows)} pass the d=2 wall and e.p.-aware no-passer predicates")
    print("#14 fits the literal generalized pattern as a one-file W5 wall; it is excluded only by the older W2/B4 or W3/B5-only classification.")
    expected = keys_by_width.get(4, set())
    if expected:
        proc = subprocess.Popen(
            [str(ROOT / "research/odd_n_plus_2/enumerate"), "8", "4"],
            cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        found = set()
        for line in proc.stdout:
            fields = line.rstrip("\n").split("\t")
            if len(fields) != 6 or fields[0] != "RING":
                raise AssertionError(f"bad enumerator row: {line!r}")
            _, w, d, r, p, pos = fields
            board2 = tuple(parse_engine(pos, 8))
            found.add((board2, (int(w), int(d), int(r), int(p))))
        err = proc.stderr.read()
        rc = proc.wait()
        assert rc == 0, (rc, err)
        assert expected <= found, (len(expected), len(expected & found))
        print(f"C enumerator C8 w=4: emitted all {len(expected)} expected canonical reference hits")


def parse_engine(text, n):
    out = []
    for token in text.split():
        wm = bm = 0
        mode = None
        for ch in token:
            if ch == "W": mode = 0
            elif ch == "B": mode = 1
            elif ch.isdigit():
                if mode == 0: wm |= 1 << int(ch)
                elif mode == 1: bm |= 1 << int(ch)
        out.append((wm, bm))
    assert len(out) == n
    return out


if __name__ == "__main__":
    main()
