#!/usr/bin/env python3
"""Second, separately written perft for the flat 8x8 board and the 8-file cylinder (stdlib only).

Written after cylperft.c by the same author, but structured differently on purpose:
  * the board is a dict {(file, rank): piece letter} with files and ranks 0..7;
  * "is square X attacked?" is answered *forwards*: every enemy piece's attack set is generated and
    searched for X (cylperft.c looks *backwards* from X along rays);
  * moves are collected in a set of (from, to, promotion), so a square reached by two routes is one move.

Rules as in cylperft.c and engine/FAIRY_CYLINDER.md section 2 (plan B0): every file step wraps modulo 8
on the cylinder; slider rays stop at the first piece and never come back to their own square; castling
is the flat rule with cylinder attacks; e.p. across the seam; legal = the mover's king is not attacked
after the move.

Usage (from the project root):
    .venv/bin/python engine/perft/cylperft.py cyl 4 "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    .venv/bin/python engine/perft/cylperft.py flat 3 "<FEN>" divide
"""
from __future__ import annotations

import sys

KNIGHT = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
KING = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]
ORTHO = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DIAG = [(1, 1), (1, -1), (-1, 1), (-1, -1)]


class Board:
    def __init__(self, wrap: bool):
        self.wrap = wrap

    def go(self, sq, df, dr):
        f, r = sq[0] + df, sq[1] + dr
        if not 0 <= r < 8:
            return None
        if self.wrap:
            f %= 8
        elif not 0 <= f < 8:
            return None
        return (f, r)

    # ---- attack sets, forwards --------------------------------------------------------------
    def attacks_of(self, pos, sq):
        """Squares attacked by the piece on sq (for pawns: capture squares only)."""
        p = pos["board"][sq]
        t = p.upper()
        white = p.isupper()
        out = set()
        if t == "P":
            for df in (-1, 1):
                s = self.go(sq, df, 1 if white else -1)
                if s:
                    out.add(s)
        elif t in "NK":
            for df, dr in (KNIGHT if t == "N" else KING):
                s = self.go(sq, df, dr)
                if s and s != sq:
                    out.add(s)
        else:
            dirs = (ORTHO if t == "R" else DIAG if t == "B" else ORTHO + DIAG)
            for df, dr in dirs:
                for k in range(1, 8):
                    s = self.go(sq, df * k, dr * k)
                    if s is None or s == sq:
                        break
                    out.add(s)
                    if s in pos["board"]:
                        break
        return out

    def attacked(self, pos, target, by_white: bool) -> bool:
        for sq, p in pos["board"].items():
            if p.isupper() == by_white and target in self.attacks_of(pos, sq):
                return True
        return False

    # ---- move generation ----------------------------------------------------------------------
    def pseudo(self, pos):
        b, white = pos["board"], pos["white"]
        mv = set()
        for sq, p in list(b.items()):
            if p.isupper() != white:
                continue
            t = p.upper()
            if t == "P":
                d = 1 if white else -1
                last = 7 if white else 0
                one = self.go(sq, 0, d)
                promos = "QRBN" if white else "qrbn"
                if one and one not in b:
                    if one[1] == last:
                        mv |= {(sq, one, x) for x in promos}
                    else:
                        mv.add((sq, one, None))
                        if sq[1] == (1 if white else 6):
                            two = self.go(sq, 0, 2 * d)
                            if two not in b:
                                mv.add((sq, two, None))
                for s in self.attacks_of(pos, sq):
                    if s in b and b[s].isupper() != white:
                        if s[1] == last:
                            mv |= {(sq, s, x) for x in promos}
                        else:
                            mv.add((sq, s, None))
                    elif s == pos["ep"]:
                        mv.add((sq, s, None))
            else:
                for s in self.attacks_of(pos, sq):
                    if s not in b or b[s].isupper() != white:
                        mv.add((sq, s, None))
        # castling (flat definition)
        r = 0 if white else 7
        k, rk = ("K", "R") if white else ("k", "r")
        if b.get((4, r)) == k:
            enemy = not white
            if (("K" if white else "k") in pos["castle"] and b.get((7, r)) == rk
                    and (5, r) not in b and (6, r) not in b
                    and not any(self.attacked(pos, (f, r), enemy) for f in (4, 5, 6))):
                mv.add(((4, r), (6, r), None))
            if (("Q" if white else "q") in pos["castle"] and b.get((0, r)) == rk
                    and all((f, r) not in b for f in (1, 2, 3))
                    and not any(self.attacked(pos, (f, r), enemy) for f in (4, 3, 2))):
                mv.add(((4, r), (2, r), None))
        return mv

    def make(self, pos, m):
        frm, to, promo = m
        b = dict(pos["board"])
        p = b.pop(frm)
        white = pos["white"]
        ep = None
        if p.upper() == "P":
            if to == pos["ep"] and to not in b:          # en passant: the victim is beside us
                b.pop((to[0], frm[1]))
            if abs(to[1] - frm[1]) == 2:
                ep = (frm[0], (frm[1] + to[1]) // 2)
        if p.upper() == "K" and frm[0] == 4 and to[0] in (2, 6) and frm[1] == to[1]:
            r = frm[1]
            if to[0] == 6:
                b[(5, r)] = b.pop((7, r))
            else:
                b[(3, r)] = b.pop((0, r))
        b[to] = promo if promo else p
        castle = pos["castle"]
        for sq, lost in (((4, 0), "KQ"), ((7, 0), "K"), ((0, 0), "Q"),
                         ((4, 7), "kq"), ((7, 7), "k"), ((0, 7), "q")):
            if frm == sq or to == sq:
                castle = "".join(c for c in castle if c not in lost)
        return {"board": b, "white": not white, "castle": castle, "ep": ep}

    def legal(self, pos):
        out = []
        white = pos["white"]
        for m in self.pseudo(pos):
            q = self.make(pos, m)
            ksq = next(s for s, p in q["board"].items() if p == ("K" if white else "k"))
            if not self.attacked(q, ksq, not white):
                out.append(m)
        return out

    def perft(self, pos, d):
        ms = self.legal(pos)
        if d == 1:
            return len(ms)
        return sum(self.perft(self.make(pos, m), d - 1) for m in ms)


def parse_fen(fen: str):
    parts = fen.split()
    b = {}
    for i, row in enumerate(parts[0].split("/")):
        r, f = 7 - i, 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                b[(f, r)] = ch
                f += 1
    ep = None if parts[3] == "-" else ("abcdefgh".index(parts[3][0]), int(parts[3][1]) - 1)
    return {"board": b, "white": parts[1] == "w", "castle": "" if parts[2] == "-" else parts[2], "ep": ep}


def name(sq):
    return "abcdefgh"[sq[0]] + str(sq[1] + 1)


def main():
    topo, depth, fen = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    B = Board(topo == "cyl")
    pos = parse_fen(fen)
    if len(sys.argv) > 4 and sys.argv[4] == "divide":
        tot = 0
        for m in sorted(B.legal(pos)):
            n = B.perft(B.make(pos, m), depth - 1) if depth > 1 else 1
            print(f"{name(m[0])}{name(m[1])}{(m[2] or '').lower()} {n}")
            tot += n
        print("total", tot)
    else:
        print(B.perft(pos, depth))


if __name__ == "__main__":
    main()
