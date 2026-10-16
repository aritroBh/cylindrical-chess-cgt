"""Is a trebuchet a real mutual zugzwang?  Flat 8x8 and the 8-file cylinder.

For a K+P vs K+P trebuchet (pawns blocked on one file), we
  1. list every square each king attacks (marking squares reached across the
     a/h seam on the cylinder);
  2. for each side to move, list its legal moves (the pawn is blocked, so only
     king moves), check whether each move abandons the pawn (the enemy king can
     capture it next move), and look up the resulting K+P vs K ending, with the
     original mover to move, in an exact KPK table (./kpk, see kpk.c);
  3. call the position "lost for the side to move" if every legal move allows a
     capture into a KPK win for the opponent.  This is a sufficient condition
     (the opponent may have other wins too); if it fails we say so.

KPK caveats: queen promotion only (rook under-promotion credited on the flat
board only), and "KQK is a win" is assumed (classical on the flat board; on the
cylinder it rests on the project's single-implementation 4-man prototype).

Run:  cd /Users/aritro/Downloads/Research/Chessendgames/atlas/cylinder && \
      cc -O2 -o kpk kpk.c && ../../.venv/bin/python trebuchet.py
"""
from __future__ import annotations

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = "abcdefgh"
N, RANKS = 8, 8


def sq(s):
    return FILES.index(s[0]), int(s[1:])


def nm(s):
    return f"{FILES[s[0]]}{s[1]}"


def kmoves(s, wrap):
    f, r = s
    out = []
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == dr == 0:
                continue
            g, q = f + df, r + dr
            if wrap:
                g %= N
            if not (0 <= g < N) or not (1 <= q <= RANKS):
                continue
            out.append((g, q))
    return out


def adj(a, b, wrap):
    return a != b and b in kmoves(a, wrap)


def pawn_attacks(p, colour, wrap):
    f, r = p
    q = r + (1 if colour == "W" else -1)
    out = []
    for df in (-1, 1):
        g = f + df
        if wrap:
            g %= N
        if 0 <= g < N and 1 <= q <= RANKS:
            out.append((g, q))
    return out


def seam(a, b):
    return abs(a[0] - b[0]) > 1  # adjacent only through the a/h seam


class KPK:
    """Thin wrapper around the compiled ./kpk (White-pawn tables)."""

    def __init__(self, wrap):
        self.wrap = wrap
        exe = os.path.join(HERE, "kpk")
        if not os.path.exists(exe):
            subprocess.check_call(["cc", "-O2", "-o", exe, os.path.join(HERE, "kpk.c")])
        self.exe = exe

    def query(self, rows):
        """rows: list of (wk, bk, pawn, pawn_colour, stm). Returns 'W','B','D' per row."""
        lines, flips = [], []
        for wk, bk, p, pc, stm in rows:
            if pc == "W":
                lines.append(f"{nm(wk)} {nm(bk)} {nm(p)} {stm}")
                flips.append(False)
            else:  # colour reversal: flip ranks, swap colours
                fl = lambda s: (s[0], RANKS + 1 - s[1])
                lines.append(f"{nm(fl(bk))} {nm(fl(wk))} {nm(fl(p))} {'B' if stm == 'W' else 'W'}")
                flips.append(True)
        out = subprocess.run([self.exe, str(N), "1" if self.wrap else "0", "0" if self.wrap else "1"],
                             input="\n".join(lines) + "\n", capture_output=True, text=True, check=True)
        res = []
        for line, flip in zip(out.stdout.strip().splitlines(), flips):
            v = line.split()[-1]
            if v == "ILLEGAL":
                res.append("?")
            elif v == "D":
                res.append("D")
            else:  # 'W' = pawn side (as White in the table) wins
                res.append("B" if flip else "W")
        return res


def analyse(title, wrap, wk, bk, wp, bp, verbose=True):
    wk, bk, wp, bp = map(sq, (wk, bk, wp, bp))
    kpk = KPK(wrap)
    out = {"title": title, "wrap": wrap}
    if verbose:
        print(f"\n### {title} ({'8-file cylinder' if wrap else 'flat 8x8'}): "
              f"WK {nm(wk)}, BK {nm(bk)}, W P{nm(wp)}, B P{nm(bp)}")
    for name, k in (("WK", wk), ("BK", bk)):
        att = kmoves(k, wrap)
        s = ", ".join(nm(t) + ("(seam)" if seam(k, t) else "") for t in sorted(att))
        out[name + "_attacks"] = [nm(t) for t in sorted(att)]
        if verbose:
            print(f"  {name} {nm(k)} attacks: {s}")
    wpa, bpa = pawn_attacks(wp, "W", wrap), pawn_attacks(bp, "B", wrap)
    if verbose:
        print(f"  W P{nm(wp)} attacks {', '.join(nm(t) + ('(seam)' if seam(wp, t) else '') for t in wpa)}; "
              f"B P{nm(bp)} attacks {', '.join(nm(t) + ('(seam)' if seam(bp, t) else '') for t in bpa)}")
    verdict = {}
    for mover in ("W", "B"):
        K, EK = (wk, bk) if mover == "W" else (bk, wk)
        P, EP = (wp, bp) if mover == "W" else (bp, wp)
        epa = bpa if mover == "W" else wpa  # squares attacked by the enemy pawn
        rows, labels, notes = [], [], []
        for d in kmoves(K, wrap):
            if d == P or d == EK or adj(d, EK, wrap) or d in epa:
                continue
            if d == EP:
                # capture of the enemy pawn: legal only if it is undefended
                if adj(EP, EK, wrap):
                    continue
                notes.append(f"K{nm(d)} captures the enemy pawn (undefended!)")
                continue
            # can the enemy king now capture our pawn?
            if adj(P, EK, wrap) and not adj(P, d, wrap):
                ek2 = P
                if mover == "W":
                    rows.append((d, ek2, EP, "B", "W"))
                else:
                    rows.append((ek2, d, EP, "W", "B"))
                labels.append(f"K{nm(d)}")
            else:
                notes.append(f"K{nm(d)} keeps the pawn (no immediate capture)")
        res = kpk.query(rows) if rows else []
        opp = "B" if mover == "W" else "W"
        lines = [f"K{lab[1:]} ...Kx{nm(P)} -> {'opponent wins' if r == opp else ('draw' if r == 'D' else r)}"
                 for lab, r in zip(labels, res)]
        all_lose = bool(rows) and not notes and all(r == opp for r in res)
        verdict[mover] = all_lose
        out[mover] = {"moves": lines, "other": notes, "lost_for_mover": all_lose}
        if verbose:
            print(f"  {mover} to move: {len(rows) + len(notes)} legal moves")
            for l in lines:
                print("     " + l)
            for nt in notes:
                print("     " + nt)
            print(f"     => {'LOST for the side to move (every move drops the pawn into a lost KPK)' if all_lose else 'NOT shown lost'}")
    out["mutual_zugzwang"] = verdict["W"] and verdict["B"]
    if verbose:
        print(f"  mutual zugzwang (both sides to move lose): {out['mutual_zugzwang']}")
    return out


def sweep(wrap):
    """All trebuchets W P(x,r), B P(x,r+1), WK (x+s,r+1), BK (x-s,r) on the board."""
    rows = []
    for x in range(N):
        for r in range(2, 7):
            for s in (1, -1):
                fw, fb = x + s, x - s
                if wrap:
                    fw %= N
                    fb %= N
                if not (0 <= fw < N and 0 <= fb < N):
                    continue
                o = analyse("", wrap, nm((fw, r + 1)), nm((fb, r)), nm((x, r)), nm((x, r + 1)), verbose=False)
                rows.append((nm((x, r)), r, s, o["W"]["lost_for_mover"], o["B"]["lost_for_mover"]))
    return rows


if __name__ == "__main__":
    print("## Paper 5.1 trebuchet on the 8-file cylinder")
    analyse("paper 5.1", True, "h5", "b4", "a4", "a5")
    print("\n## Same diagram read on a flat board (no seam)")
    analyse("paper 5.1 on flat board", False, "h5", "b4", "a4", "a5")
    print("\n## Proposed 8x8 embedding trebuchet: W Pg4 / B Pg5, WK f5, BK h4")
    analyse("g-file trebuchet", False, "f5", "h4", "g4", "g5")
    analyse("g-file trebuchet", True, "f5", "h4", "g4", "g5")
    for wrap in (False, True):
        rows = sweep(wrap)
        tot = len(rows)
        both = sum(1 for r in rows if r[3] and r[4])
        print(f"\n## Sweep of all trebuchets on the {'8-file cylinder' if wrap else 'flat 8x8'}: "
              f"{both}/{tot} are mutual zugzwangs by the drop-into-lost-KPK test")
        byr = {}
        for p, r, s, lw, lb in rows:
            byr.setdefault(r, [0, 0, 0, 0])
            byr[r][0] += 1
            byr[r][1] += lw
            byr[r][2] += lb
            byr[r][3] += lw and lb
        for r in sorted(byr):
            t, lw, lb, both = byr[r]
            print(f"   white pawn on rank {r}: {t} placements; WTM lost {lw}, BTM lost {lb}, both {both}")
        if not wrap:
            bad = [f"{p}(s={s:+d}) W{'L' if lw else '?'} B{'L' if lb else '?'}" for p, r, s, lw, lb in rows if not (lw and lb)]
            print("   failures:", ", ".join(bad))
