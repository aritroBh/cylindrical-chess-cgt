#!/usr/bin/env python3
"""Headline positions: values under all 15 settings (flat and cylinder of the same
width), an independent check of the claimed value with the A2 worker's C solver
(nimscan --test; widths <= 4), the 8x8 freeze/legality test and FENs.

Usage (from the project root):
  PYTHONPATH=. .venv/bin/python atlas/targets/headline.py
Writes atlas/targets/headline.json and headline.out.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C  # noqa: E402
import freeze  # noqa: E402
from crosscheck import dag_of, col_name, NIMSCAN  # noqa: E402

# (label, position, width, reference setting for the claimed value)
HEADLINE = [
    ("1/8 (6 pawns, smallest)", "W: a2 a3 b2 / B: a6 b5 b6", 2, C.AWARE),
    ("1/8 (6 pawns, mirror, reachable)", "W: a2 b2 b3 / B: a5 a6 b6", 2, C.AWARE),
    ("1/8 (7 pawns)", "W: a2 a3 a4 b2 / B: a5 a7 b7", 2, C.AWARE),
    ("1/8 (7 pawns)", "W: a2 a3 a4 c2 / B: b6 b7 c6", 3, C.AWARE),
    ("1/8 (7 pawns)", "W: a2 a3 b6 c2 / B: b5 b7 c6", 3, C.AWARE),
    ("1/8 (7 pawns)", "W: a2 a3 b6 c2 / B: b5 b7 d7", 4, C.AWARE),
    ("1/8 (7 pawns)", "W: a5 b2 b3 d2 / B: b7 c5 d6", 4, C.AWARE),
    ("1/16 (7 pawns)", "W: a5 b2 b3 d2 / B: b7 c5 d7", 4, C.AWARE),
    ("-1/16 (7 pawns, colour reversal)", "W: a2 b4 c2 / B: a7 c6 c7 d4", 4, C.AWARE),
    ("up2* (6 pawns)", "W: a2 b2 b6 / B: a6 b7 c5", 3, C.AWARE),
    ("up2* (4 pawns, smallest)", "W: a2 b2 / B: a6 c5", 3, C.AWARE),
    ("up2 (6 pawns, aware)", "W: a2 b2 d4 / B: a7 c6 d7", 4, C.AWARE),
    ("*2 (7 pawns, adopted model)", "W: a4 b3 d2 d3 / B: a7 b7 c5", 4, C.AWARE),
    ("*2 (7 pawns, colour reversal)", "W: b4 c2 d2 / B: a6 a7 c6 d5", 4, C.AWARE),
    ("*2 (4 pawns, textbook only)", "W: a2 c2 / B: b7 d7", 4, C.TEXTBOOK),
    ("tiny(1/2) (w5, textbook)", "W: b3 c2 e2 / B: a6 c6 d7", 5, C.TEXTBOOK),
    ("1+tiny(1/2) (w5, aware)", "W: b4 d2 e2 / B: a7 c6 e7", 5, C.AWARE),
    ("tiny(1/2) (w4, 7 pawns, mover)", "W: a3 b2 d2 / B: a6 b5 b6 c7", 4, ("mover", 1, 0)),
    ("tiny(1/2) (w4, e.p. off)", "W: a4 c2 d3 / B: a5 b6 d6 d7", 4, ("count", 0, 0)),
    ("tiny(3/2+-1/2) (robust)", "W: a2 a3 c2 / B: a6 c6 c7", 3, C.AWARE),
    ("-1+tiny(3/2+-1/2) (3 pawns)", "W: a2 / B: a6 a7", 1, C.AWARE),
    ("hottest robust {3*|-4}, t=7/2", "W: a2 b4 c2 / B: a4 b7 c5", 3, C.AWARE),
    ("+-3 robust", "W: a2 b4 / B: a5 b7", 2, C.AWARE),
    ("hottest 3/2+-11/2, t=11/2", "W: a2 a4 b2 / B: a7 b5 c7", 3, C.AWARE),
]


def main():
    extra = []
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as fh:
            for d in json.load(fh):
                ref = tuple(d["ref"]) if "ref" in d else C.AWARE
                extra.append((d["label"], d["position"], d["width"], ref))
    items = HEADLINE + extra
    inp = []
    for _, p, w, _ in items:
        for wrap in (0, 1):
            for (r, ep, aw) in C.SETTINGS:
                inp.append(f"{p}\t{w}\t{wrap}\t{r}\t{ep}\t{aw}")
    out = subprocess.run([os.path.join(HERE, "pcgt"), "--printlimit", "3000"], input="\n".join(inp) + "\n",
                         capture_output=True, text=True, check=True).stdout
    vals, rows = {}, {}
    for line in out.splitlines():
        q = line.split("\t")
        if q[0] == "#V":
            vals[int(q[1])] = (q[4], q[5], q[3])
        else:
            rows[(q[0], int(q[1]), int(q[2]), q[3], int(q[4]), int(q[5]))] = int(q[6])
    res, lines = [], []
    tests = []
    for lab, p, w, ref in items:
        by = {}
        for wrap in (0, 1):
            for s in C.SETTINGS:
                gid = rows[(p, w, wrap) + tuple(s)]
                by[("cyl:" if wrap else "") + C.sname(s)] = vals[gid][0] if vals[gid][0] != "-" else f"(±W game {vals[gid][2]})"
        claimed = by[C.sname(ref)]
        same = [C.sname(s) for s in C.SETTINGS if by[C.sname(s)] == claimed]
        fz = freeze.placements(p, w) if w <= 5 else {"fits": False}
        good = [x for x in fz.get("placements", []) if x["freeze_ok"] and x["legal_necessary_ok"]]
        e = {"label": lab, "position": p, "width": w, "reference_setting": C.sname(ref), "claimed": claimed,
             "same_in_of15": len(same), "settings_equal": same, "values": by,
             "freeze_fits_8x8": fz["fits"], "placements_ok": len(good),
             "fen_example": good[0]["fen_w"] if good else None,
             "fen_example_placement": ({k: good[0][k] for k in ("mirror", "offset", "treb_rank", "orientation", "WK", "BK")}
                                       if good else None)}
        res.append(e)
        if w <= 4:
            key = None
            gid = rows[(p, w, 0) + tuple(ref)]
            key = vals[gid][1]
            if key != "-":
                T = C.parse_key(key)
                dag = dag_of(C.cgt.neg(T))
                if len(dag) <= 256 and all(len(L) <= 16 and len(R) <= 16 for L, R in dag):
                    tests.append((len(res) - 1, p, w, dag))
    path = os.path.join(C.WORK, "headline_nimscan_input.tsv")
    with open(path, "w") as fh:
        for _, p, w, dag in tests:
            fh.write(f"{p}\t{w}\t" + ";".join(",".join(map(str, L)) + "|" + ",".join(map(str, R)) for L, R in dag) + "\n")
    nout = subprocess.run([NIMSCAN, "--test", path], capture_output=True, text=True, check=True).stdout.strip().split("\n")
    header = nout[0].split("\t")[2:]
    for (idx, p, w, dag), line in zip(tests, nout[1:]):
        q = line.split("\t")
        assert q[0] == p
        cvec = dict(zip(header, (x == "EQUAL" for x in q[2:])))
        e = res[idx]
        mine = {col_name(s): e["values"][C.sname(s)] == e["claimed"] for s in C.SETTINGS}
        e["nimscan_equal_in"] = sum(cvec.values())
        e["nimscan_agrees_all15"] = all(cvec[k] == mine[k] for k in mine)
    for e in res:
        lines.append(f"{e['label']}")
        lines.append(f"   {e['position']} (w{e['width']}): {e['claimed']} under {e['reference_setting']}; "
                     f"same under {e['same_in_of15']}/15 settings; nimscan agrees: {e.get('nimscan_agrees_all15', 'n/a')}")
        diff = {k: v for k, v in e["values"].items() if not k.startswith("cyl:") and v != e["claimed"]}
        if diff:
            lines.append("   differs under: " + "; ".join(f"{k}: {v[:50]}" for k, v in diff.items()))
        lines.append(f"   cylinder (count, e.p. on): textbook {e['values']['cyl:count/epon-textbook'][:60]}, aware {e['values']['cyl:count/epon-aware'][:60]}")
        lines.append(f"   8x8 freeze+legality placements: {e['placements_ok']}; FEN {e['fen_example']}")
    with open(os.path.join(HERE, "headline.json"), "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, "headline.out"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
