"""K68: compare the chess claims of PROOF.md section 6 with the cached Syzygy answers of K65
(kings/delegate/out/K65/verify/logs/tbcache.tar.xz, unpacked into kings/delegate/out/K68/tb/; offline).

For each of the eight positions (two roots, two q's, each side to move) it prints the tablebase category and the
category of every move (from the point of view of the side that made it), and checks the claims of PROOF.md:
roots and q's with Black to move: lost for Black, every Black move loses; roots with White to move: won, and the
freeze is the only move that does not lose; q's with White to move: lost for White, every White move loses.
It also checks that the legal move lists equal python-chess's.
Usage: chess_check.py TBCACHE_DIR
"""
import glob
import json
import sys

import chess

cache = {}
for f in glob.glob(sys.argv[1] + "/*/*.json"):
    d = json.load(open(f))
    cache[" ".join(d["fen"].split()[:2])] = d

POS = [("root b4", "8/1p6/1Pp5/2P5/1k1K4/8/2P5/8", "c2c4"),
       ("root b5", "8/1p6/1Pp5/1kP5/3K4/8/2P5/8", "c2c3"),
       ("q1 (after c2-c4)", "8/1p6/1Pp5/2P5/1kPK4/8/8/8", None),
       ("q2 (after c2-c3)", "8/1p6/1Pp5/1kP5/3K4/2P5/8/8", None)]
FLIP = {"win": "loss", "loss": "win", "draw": "draw"}
ok = True
for name, fen, freeze in POS:
    for side in "bw":
        key = fen + " " + side
        d = cache.get(key)
        if d is None:
            print("%-18s %s: NOT IN CACHE" % (name, side))
            ok = False
            continue
        cat = d["data"]["category"]
        b = chess.Board(key + " - - 0 1")
        legal = sorted(m.uci() for m in b.legal_moves)
        tbm = sorted(m["uci"] for m in d["data"]["moves"])
        mover = {m["uci"]: FLIP[m["category"]] for m in d["data"]["moves"]}  # result for the side that moved
        line = "%-18s %s to move: %-4s | %s" % (name, "White" if side == "w" else "Black", cat,
                                                  " ".join("%s:%s" % (u, mover[u]) for u in tbm))
        if legal != tbm:
            line += "  MOVE LISTS DIFFER"
            ok = False
        if side == "b":
            want = cat == "loss" and all(v == "loss" for v in mover.values())
        elif freeze:
            want = cat == "win" and mover[freeze] == "win" and all(v == "loss" for u, v in mover.items() if u != freeze)
        else:
            want = cat == "loss" and all(v == "loss" for v in mover.values())
        line += "   claim %s" % ("holds" if want else "FAILS")
        ok &= want
        print(line)
        cats = {m["category"] for m in d["data"]["moves"]} | {cat}
        if cats - {"win", "loss", "draw"}:
            print("   note: categories", cats)
print("ALL CHESS CLAIMS AGREE WITH THE TABLEBASE" if ok else "SOME CHESS CLAIM DISAGREES")
