"""K50 referee: every ChessSums position of the engine test subset (200) through embed_check with --group,
classified here independently (FEN parsed by hand; SHARED = a non-group pawn on a group file, ADJACENT = on a file
next to one, else APART). Run from the project root."""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.getcwd())
from kings.embed_check import Board, Checker  # noqa: E402

D = "engine/runs/chesssums/"
meta = {m["id"]: m for m in json.load(open(D + "meta.json"))}
ids = json.load(open(D + "subset_ids.json"))
tally = Counter()
bad = []
for i in ids:
    m = meta[i]
    fz = m["freeze"]
    gsq = {fz[k] for k in ("wk", "bk", "wp", "bp")}
    gfiles = {s[0] for s in gsq}
    pawns = []
    for r, row in enumerate(m["fen"].split()[0].split("/")):
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                if ch in "Pp":
                    pawns.append("abcdefgh"[f] + str(8 - r))
                f += 1
    cf = {p[0] for p in pawns if p not in gsq}
    if cf & gfiles:
        cls = "SHARED"
    elif any(abs(ord(a) - ord(c)) == 1 for a in cf for c in gfiles):
        cls = "ADJACENT"
    else:
        cls = "APART"
    grp = f"K{fz['wk']},P{fz['wp']},k{fz['bk']},p{fz['bp']}"
    r = Checker(Board(8, 8, False), 8, 300000, False, 20).run(m["fen"], None, grp)
    sep = r["separation"]["verdict"]
    tally[(cls, sep, r["verdict"])] += 1
    if (cls == "APART") != (sep == "PASS"):
        bad.append((i, cls, sep, r["separation"].get("witness")))
    print(json.dumps({"id": i, "class": cls, "sep": sep, "verdict": r["verdict"],
                      "witness": r["separation"].get("witness")}), flush=True)
print("TALLY", {" ".join(k): v for k, v in sorted(tally.items())})
print("MISMATCH (APART must pass, others must fail):", len(bad), bad[:5])
