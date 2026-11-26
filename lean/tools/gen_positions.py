#!/usr/bin/env python3
"""Random legal-looking positions in the `movelist` input format (lean/notes/L1.md section 1).

Usage: .venv/bin/python lean/tools/gen_positions.py SEED N   (prints N lines; same SEED, same output)

Each line: 1 to 6 files (cylinders 3 to 6, the Mobius strip 3 to 6, always 8 ranks), 5 to 8 ranks
(flat and cylinder), 1 to 8 pawns in total on ranks 2 .. ranks-1 (no pawn on its first or last rank),
any of the nine settings, and about a third of the lines with a live e.p. right. Pawns move in their
normal direction, except that on the strip about a quarter of them are marked `*`. Corners excluded
on purpose: one-file cylinders (note D9), two-file strips (D3), strips with other than eight ranks (D12).
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import py_movelist as pm  # noqa: E402


def make(rng):
    topo = rng.choice(["flat", "cyl", "mob"])
    if topo == "flat":
        files, ranks = rng.randint(1, 6), rng.randint(5, 8)
    elif topo == "cyl":
        files, ranks = rng.randint(3, 6), rng.randint(5, 8)
    else:
        files, ranks = rng.randint(3, 6), 8
    want_ep = rng.random() < 0.4
    ep = rng.choice(["textbook", "aware"]) if want_ep else rng.choice(["off", "textbook", "aware"])
    race = rng.choice(["count", "mover", "opponent"])
    geo = pm.Geo(topo, files, ranks, ep != "off")
    squares = [(f, r) for f in range(files) for r in range(2, ranks)]
    rng.shuffle(squares)
    total = min(rng.randint(1, 8), len(squares))
    W, B = [], []      # (file, rank, up)
    ep_sq = None
    reserved = set()
    if want_ep and geo.ep_on and total >= 2:
        # a double-stepped pawn with an enemy capturer beside it (the capturer lands on the skipped square)
        for _ in range(200):
            owner = rng.choice("WB")
            up = owner == "W"
            if topo == "mob" and rng.random() < 0.25:
                up = not up  # a reversed pawn, double-steps from the other home rank
            home = 2 if up else ranks - 1
            step = 1 if up else -1
            f = rng.randrange(files)
            named = (f, home + 2 * step)
            skipped = (f, home + step)
            if not 1 <= named[1] <= ranks:
                continue
            caps = [(g, s, e) for g in range(files) for s in range(1, ranks + 1) for e in (True, False)
                    if (g, s) not in (named, skipped, (f, home))]
            rng.shuffle(caps)
            cap = None
            for g, s, e in caps:
                if topo != "mob" and e != (owner == "B"):
                    continue  # flat/cyl: the capturer is the enemy pawn in its normal direction
                if any(t[:2] == skipped for t in pm.cap_targets(geo, g, s, e)):
                    cap = (g, s, e)
                    break
            if cap is None:
                continue
            pawn = (f, named[1], up)
            if owner == "W":
                W, B = [pawn], [cap]
            else:
                W, B = [cap], [pawn]
            ep_sq = named
            reserved = {named, skipped, (f, home), cap[:2]}
            break
    if ep_sq is None:
        ep = "off" if not geo.ep_on else ep
    free = [sq for sq in squares if sq not in reserved]
    for f, r in free:
        if len(W) + len(B) >= total:
            break
        if (f, r) in {(p[0], p[1]) for p in W + B}:
            continue
        if topo == "mob":
            up = rng.random() >= 0.25
        else:
            up = None
        if rng.random() < 0.5:
            W.append((f, r, True if up is None else up))
        else:
            B.append((f, r, False if up is None else not up))
    if ep_sq is not None and pm.normalise(geo, W, B, ep_sq) is None:
        ep_sq = None
    pawns_w = [pm.FILES[f] + str(r) + ("" if (topo != "mob" or up) else "*") for f, r, up in W]
    pawns_b = [pm.FILES[f] + str(r) + ("" if (topo != "mob" or not up) else "*") for f, r, up in B]
    rng.shuffle(pawns_w)
    rng.shuffle(pawns_b)
    body = "W: " + " ".join(pawns_w) + " / B: " + " ".join(pawns_b)
    if ep_sq is not None:
        body += " / ep " + pm.FILES[ep_sq[0]] + str(ep_sq[1])
    return f"{topo} {files} {ranks} {ep} {race} | {body}"


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: gen_positions.py SEED N")
    seed, n = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    for _ in range(n):
        print(make(rng))


if __name__ == "__main__":
    main()
