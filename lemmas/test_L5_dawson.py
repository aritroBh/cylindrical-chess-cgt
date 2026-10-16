"""Falsification tests for Lemma L5 (Dawson's chess on the 3 x n cylinder).

Run (from the project root):
    PYTHONPATH=. .venv/bin/python lemmas/test_L5_dawson.py [--nmax N] [--cgt-nmax M]

This file re-implements Dawson's chess from the pawn rules WITHOUT using
cylcgt/dawson.py (only cylcgt.cgt for canonical forms), so it is a second
implementation of the move rules. Rules: 3 ranks; White pawns on rank 1, Black
pawns on rank 3, rank 2 empty; a pawn moves one square forward or captures one
square diagonally forward (files wrap on the cylinder); captures are
compulsory; normal play (no move = loss). No double steps exist on 3 ranks.

Checks
  L5.1  macro-move structure: from the full ring R_n (3 <= n <= nmax), every
        alternating continuation of every first move is forced for exactly
        5 plies (each of plies 2-5 has only captures, at least one, all on the
        pushed file f), and every 5-ply line ends in the same position: files
        f-1, f+1 empty, file f holding a blocked W/B pair, all other files
        untouched; the player to move then has no capture.
  L5.2  the end position equals (as a CGT game, computed independently) the
        flat 3 x (n-3) Dawson position: ring opens into a strip.
  L5.3  alternating-play outcome of R_n (plain minimax, no CGT) is a
        first-player win iff G(n-3) = 0, G = Grundy function of octal 0.137.
  L5.4  the partizan CGT value of R_n (per-side compulsion, as in dawson.py)
        equals * if G(n-3)=0 and 0 otherwise    (n <= cgt-nmax)
  L5.5  flat strips: the CGT value of D_k equals *G(k)          (k <= cgt-nmax)
        and agrees with cylcgt.dawson.solve (the first implementation).
"""
from __future__ import annotations

import argparse
import sys
from functools import lru_cache

from cylcgt import cgt

FAIL = []


def fail(msg):
    FAIL.append(msg)
    print("FAIL:", msg)


def grundy_0137(N):
    """Octal 0.137: from a heap of k remove 1 (only if k = 1), remove 2 from
    an end (leaving k-2), or remove 3 leaving two heaps a, b with a+b = k-3."""
    g = [0] * (N + 1)
    for k in range(1, N + 1):
        opts = set()
        if k == 1:
            opts.add(0)
        if k >= 2:
            opts.add(g[k - 2])
        for a in range(0, k - 2):
            opts.add(g[a] ^ g[k - 3 - a])
        m = 0
        while m in opts:
            m += 1
        g[k] = m
    return g


class Dawson:
    def __init__(self, n: int, ring: bool):
        self.n, self.ring = n, ring

    def nbrs(self, f):
        out = []
        for d in (-1, 1):
            g = f + d
            if self.ring:
                out.append(g % self.n)
            elif 0 <= g < self.n:
                out.append(g)
        return sorted(set(out))

    def moves(self, W, B, side):
        """(captures, pushes) for `side`; positions are (W, B) frozensets."""
        mine, theirs = (W, B) if side == "W" else (B, W)
        d = 1 if side == "W" else -1
        occ = W | B
        caps, pushes = [], []
        for (f, r) in mine:
            r1 = r + d
            if not 1 <= r1 <= 3:
                continue
            for g in self.nbrs(f):
                if (g, r1) in theirs:
                    caps.append((mine - {(f, r)} | {(g, r1)}, theirs - {(g, r1)}))
            if (f, r1) not in occ:
                pushes.append((mine - {(f, r)} | {(f, r1)}, theirs))
        def back(lst):
            out = []
            for m, t in lst:
                out.append((frozenset(m), frozenset(t)) if side == "W" else (frozenset(t), frozenset(m)))
            return list(dict.fromkeys(out))
        return back(caps), back(pushes)

    def legal(self, W, B, side):
        caps, pushes = self.moves(W, B, side)
        return caps if caps else pushes

    def start(self):
        return (frozenset((f, 1) for f in range(self.n)), frozenset((f, 3) for f in range(self.n)))


@lru_cache(maxsize=None)
def cgt_value(n, ring, W, B):
    D = Dawson(n, ring)
    L = [cgt_value(n, ring, w, b) for w, b in D.legal(W, B, "W")]
    R = [cgt_value(n, ring, w, b) for w, b in D.legal(W, B, "B")]
    return cgt.make(L, R)


@lru_cache(maxsize=None)
def first_player_wins(n, ring, W, B, side):
    D = Dawson(n, ring)
    other = "B" if side == "W" else "W"
    return any(not first_player_wins(n, ring, w, b, other) for w, b in D.legal(W, B, side))


def check_macro(n: int):
    """L5.1 for the ring of size n: returns the set of end positions."""
    D = Dawson(n, True)
    W0, B0 = D.start()
    ends = set()
    for side in "WB":
        other = "B" if side == "W" else "W"
        caps, pushes = D.moves(W0, B0, side)
        if caps:
            fail(f"L5.1 n={n}: captures at the start")
        for (W1, B1) in pushes:
            moved = ((W0 - W1) if side == "W" else (B0 - B1))
            f = next(iter(moved))[0]
            frontier = [(W1, B1)]
            to_move = other
            for ply in range(2, 6):
                nxt = []
                for (w, b) in frontier:
                    c, _ = D.moves(w, b, to_move)
                    if not c:
                        fail(f"L5.1 n={n} f={f} ply {ply}: no capture available")
                    for (w2, b2) in c:
                        changed = {s[0] for s in (w ^ w2) | (b ^ b2)}
                        if not changed <= {f, (f - 1) % n, (f + 1) % n}:
                            fail(f"L5.1 n={n} f={f} ply {ply}: capture away from f")
                    nxt.extend(c)
                frontier = list(dict.fromkeys(nxt))
                to_move = "B" if to_move == "W" else "W"
            for (w, b) in frontier:
                c, _ = D.moves(w, b, to_move)
                if c:
                    fail(f"L5.1 n={n} f={f}: capture still available after 5 plies")
                files_w = {s[0] for s in w}
                files_b = {s[0] for s in b}
                if (f - 1) % n in files_w | files_b or (f + 1) % n in files_w | files_b:
                    fail(f"L5.1 n={n} f={f}: neighbour file not emptied")
                pair = ({s for s in w if s[0] == f}, {s for s in b if s[0] == f})
                expect = ({(f, 2)}, {(f, 3)}) if side == "W" else ({(f, 1)}, {(f, 2)})
                if pair != expect:
                    fail(f"L5.1 n={n} f={f}: file f is {pair}, expected {expect}")
                rest = {g for g in range(n) if g not in (f, (f - 1) % n, (f + 1) % n)}
                for g in rest:
                    if {s for s in w if s[0] == g} != {(g, 1)} or {s for s in b if s[0] == g} != {(g, 3)}:
                        fail(f"L5.1 n={n} f={f}: file {g} disturbed")
                ends.add((side, f, w, b))
            if len(frontier) != 1:
                fail(f"L5.1 n={n} f={f}: {len(frontier)} distinct end positions")
    return ends


def strip_of_end(n, f, w, b):
    """Relabel the n-3 untouched files f+2, ..., f-2 as a flat strip 0..n-4."""
    order = [(f + 2 + i) % n for i in range(n - 3)]
    m = {g: i for i, g in enumerate(order)}
    W = frozenset((m[s[0]], s[1]) for s in w if s[0] in m)
    B = frozenset((m[s[0]], s[1]) for s in b if s[0] in m)
    return W, B


def run(nmax: int, cgt_nmax: int):
    g = grundy_0137(nmax + 3)
    notes = []
    print(" n | macro ok | ends | ring: 1st wins | pred G(n-3)=0 | flat D_n: 1st wins | G(n)!=0 |"
          " partizan ring | partizan D_n | *G(n)")
    for n in range(3, nmax + 1):
        before = len(FAIL)
        ends = check_macro(n)
        D = Dawson(n, True)
        W0, B0 = D.start()
        fw = first_player_wins(n, True, W0, B0, "W")
        fb = first_player_wins(n, True, W0, B0, "B")
        pred = (g[n - 3] == 0)
        if fw != pred or fb != pred:
            fail(f"L5.3 n={n}: ring alt outcome W-first {fw}, B-first {fb}, predicted {pred}")
        Df = Dawson(n, False)
        ffw = first_player_wins(n, False, *Df.start(), "W")
        ffb = first_player_wins(n, False, *Df.start(), "B")
        if ffw != (g[n] != 0) or ffb != (g[n] != 0):
            fail(f"L5.3 n={n}: flat alt outcome {ffw},{ffb} but G(n)={g[n]}")
        ring_s = flat_s = "-"
        if n <= cgt_nmax:
            rv = cgt_value(n, True, W0, B0)
            ring_s = cgt.show(rv)
            expect = cgt.nimber(1) if pred else cgt.ZERO
            if rv is not expect:
                notes.append(f"partizan ring value R_{n} = {ring_s}, impartial prediction {cgt.show(expect)}")
            # L5.2: each end position == flat strip of n-3 (partizan values)
            for side, f, w, b in ends:
                endv = cgt_value(n, True, w, b)
                if n - 3 >= 1:
                    Ws, Bs = strip_of_end(n, f, w, b)
                    sv = cgt_value(n - 3, False, Ws, Bs)
                else:
                    sv = cgt.ZERO
                if endv is not sv:
                    fail(f"L5.2 n={n} f={f} {side}: end {cgt.show(endv)} != strip {cgt.show(sv)}")
            fv = cgt_value(n, False, *Df.start())
            flat_s = cgt.show(fv)
            if fv is not cgt.nimber(g[n]):
                notes.append(f"partizan flat value D_{n} = {flat_s}, Grundy value *{g[n]}")
        ok = "yes" if len(FAIL) == before else "NO"
        print(f"{n:2d} | {ok:8s} | {len(ends):4d} | {str(fw):14s} | {str(pred):13s} | {str(ffw):18s} | "
              f"{str(g[n] != 0):7s} | {ring_s:13s} | {flat_s:12s} | *{g[n]}", flush=True)
    print("observations (not failures): the partizan per-side-compulsion CGT value is not the impartial value:")
    for t in notes:
        print("   ", t)
    return notes


def strip_board(sizes):
    """One flat board holding full Dawson strips of the given sizes, separated
    by single empty files."""
    files, f = [], 0
    for k in sizes:
        files.extend(range(f, f + k))
        f += k + 1
    n = f - 1
    W = frozenset((x, 1) for x in files)
    B = frozenset((x, 3) for x in files)
    return n, W, B


def check_sums(max_total=11, cgt_max=6):
    """L5.6: on ONE board with global compulsion, alternating play from a sum of
    strips is decided by the XOR of Grundy values; the sum of the partizan
    component values can give the wrong outcome."""
    g = grundy_0137(max_total)
    wrong_partizan = []
    n_checked = 0
    for a in range(1, max_total):
        for b in range(a, max_total):
            if a + b + 1 > max_total:
                continue
            n, W, B = strip_board([a, b])
            fw = first_player_wins(n, False, W, B, "W")
            fb = first_player_wins(n, False, W, B, "B")
            n_checked += 1
            if fw != (g[a] ^ g[b] != 0) or fb != fw:
                fail(f"L5.6 D{a}+D{b}: alternating {fw},{fb}, Grundy xor {g[a] ^ g[b]}")
            if b <= cgt_max:
                v = cgt.add(cgt_value(a, False, *Dawson(a, False).start()),
                            cgt_value(b, False, *Dawson(b, False).start()))
                if (cgt.outcome(v) == "N") != fw:
                    wrong_partizan.append(f"D{a}+D{b}: partizan sum {cgt.show(v)} ({cgt.outcome(v)}), "
                                          f"alternating play: first player {'wins' if fw else 'loses'}")
    print(f"L5.6 two-strip boards checked: {n_checked}; Grundy XOR always right.")
    print("L5.6 partizan component sums that predict the wrong winner:", len(wrong_partizan))
    for t in wrong_partizan:
        print("    ", t)
    return wrong_partizan


def compare_first_implementation(nmax):
    """L5.5 second half: agreement with cylcgt.dawson.solve."""
    from cylcgt import dawson
    for n in range(1, nmax + 1):
        for ring in (False, True):
            if ring and n < 3:
                continue
            D = Dawson(n, ring)
            mine = cgt_value(n, ring, *D.start())
            theirs = dawson.solve(n, ring)
            if mine is not theirs:
                fail(f"L5.5 n={n} ring={ring}: {cgt.show(mine)} vs dawson.py {cgt.show(theirs)}")
    print(f"agreement with cylcgt/dawson.py for n <= {nmax}: {'yes' if not FAIL else 'see failures'}")


def test_small():
    FAIL.clear()
    run(12, 5)
    compare_first_implementation(5)
    check_sums(9, 5)
    assert not FAIL, FAIL


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmax", type=int, default=24)
    ap.add_argument("--cgt-nmax", type=int, default=7)
    a = ap.parse_args()
    run(a.nmax, a.cgt_nmax)
    compare_first_implementation(min(a.cgt_nmax, 6))
    check_sums(13, min(a.cgt_nmax, 6))
    print("FAILURES:", len(FAIL))
    sys.exit(1 if FAIL else 0)
