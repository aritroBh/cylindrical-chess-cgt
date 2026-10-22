"""Diagnose every mismatch between real chess and the frozen-king convention in an
experiment file written by kings/experiment.py.

For each mismatching position and side to move:
  * convention says the mover loses, real chess is better for the mover:
      which moves achieve the real result? If only king moves do, the zugzwang is
      broken by a king leaving the trebuchet ("escape").
  * convention says the mover wins, real chess is worse for the mover:
      for each pawn move the convention counts as winning, find the opponent's best
      reply in real chess. If every refutation is a king move, a king leaves the
      trebuchet to stop the pawns ("king refutes"); whether the move creates a passed
      pawn (convention value +-BIG) is recorded too.

Usage (from the project root):
  python3 kings/analyze.py kings/results/exp_cyl7x6_epon_Q.jsonl
Writes <input>_diagnosis.jsonl and prints a tally.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from cylcgt import cgt, pawns  # noqa: E402

# The sweeps were run with cylcgt's textbook passed test (before the e.p.-aware test became the default
# on 2026-10-16); pin it so reruns reproduce them. kings/conventions.py scores both tests.
if hasattr(pawns, "PASSED_RESPECTS_EP"):
    pawns.PASSED_RESPECTS_EP = False
from kings.experiment import PREDICT, layout  # noqa: E402

FILES = "abcdefgh"


def sq(t):
    return FILES.index(t[0]), int(t[1:])


def kpsolve_moves(lines, summary):
    cmd = [f"{ROOT}/kings/kpsolve", "--board", summary["board"], "--ep", summary["ep"], "--promote",
           summary["promote"], "--cap", str(summary["cap"]), "--threads", os.environ.get("KP_THREADS", "4"), "--moves"]
    out = subprocess.run(cmd, input="\n".join(lines) + "\n", capture_output=True, text=True, check=True)
    res = {}
    for line in out.stdout.splitlines():
        parts = [p.strip() for p in line.split("|")]
        pos, (a, b) = parts[0], parts[1].split()
        mv = {}
        if len(parts) >= 3:
            # with differing bounds the format is "A: ... | B: ..."; keep bound A (cap 2 runs are exact here)
            text = parts[2][3:] if parts[2].startswith("A: ") else parts[2]
            for tok in text.split():
                m, v = tok.rsplit(":", 1)
                mv[m] = v
        res[pos] = (a, b, mv)
    return res


def apply_move(line, move, ep_on):
    """Position string after `move` (format Pd2d3, Kf4e4, Pd5d6=Q)."""
    toks, stm, _ep = line.split()[:-2], line.split()[-2], line.split()[-1]
    piece, promo = move[0], None
    body = move[1:]
    if "=" in body:
        body, promo = body.split("=")
    # split from/to (squares are letter + digit on these boards)
    frm, to = body[:2], body[2:]
    white = stm == "w"
    letter = piece if white else piece.lower()
    new, moved = [], False
    for t in toks:
        if t[1:] == to:
            continue  # captured
        if not moved and t[0] == letter and t[1:] == frm:
            moved = True
            new.append((promo if white else promo.lower()) + to if promo else letter + to)
            continue
        new.append(t)
    if piece == "P" and promo is None and frm[0] == to[0]:
        (f, r1), (_, r2) = sq(frm), sq(to)
        ep = f"{frm[0]}{(r1 + r2) // 2}" if abs(r2 - r1) == 2 and ep_on else "-"
    else:
        ep = "-"
    # an e.p. capture (diagonal pawn move onto an empty square) removes the pawn behind
    return " ".join(new) + (" b " if white else " w ") + ep


def convention_after(row_P, move, stm, pfiles, H, ep):
    """Convention prediction (White's view) after a pawn move in the P files, opponent to move."""
    w = [sq(t) for t in row_P.split("/")[0].split(":")[1].split()]
    b = [sq(t) for t in row_P.split("/")[1].split(":")[1].split()]
    body = move[1:].split("=")[0]
    frm, to = sq(body[:2]), sq(body[2:])
    mine, theirs = (w, b) if stm == "w" else (b, w)
    if frm not in mine or frm[0] not in pfiles:
        return None, None
    mine = [to if s == frm else s for s in mine]
    theirs = [s for s in theirs if s != to]
    w2, b2 = (mine, theirs) if stm == "w" else (theirs, mine)
    off = pfiles[0]
    board = pawns.Board(len(pfiles), H, False, ep)
    pos = pawns.Pos(frozenset((f - off, r) for f, r in w2), frozenset((f - off, r) for f, r in b2))
    try:
        g = pawns.value(board, pos)
    except pawns.RaceError:
        return "race", None
    opp = "btm" if stm == "w" else "wtm"
    o = cgt.outcome(g)
    return PREDICT[o][0 if opp == "wtm" else 1], cgt.show(g)


def main():
    path = sys.argv[1]
    summary = json.load(open(path.replace(".jsonl", "_summary.json")))
    kind, size = summary["board"].split(":")
    W, H = map(int, size.split("x"))
    _, pfiles = layout(kind, W, H)
    ep_on = summary["ep"] == "on"
    rows = [json.loads(l) for l in open(path)]
    cases = []
    for row in rows:
        if row["verdict"] != "MISMATCH":
            continue
        for k, side in ((0, "wtm"), (1, "btm")):
            pv, rv = row["predicted"][k], row["real"][side][0]
            if pv != rv:
                cases.append({"P": row["P"], "value": row["value"], "side": side, "line": row[side],
                              "predicted": pv, "real": rv})
    roots = kpsolve_moves([c["line"] for c in cases], summary) if cases else {}
    children, need = {}, []
    for c in cases:
        stm = c["line"].split()[-2]
        good = "W" if stm == "w" else "L"
        mv = roots[c["line"]][2]
        c["moves"] = mv
        if c["predicted"] != good:  # convention: mover loses
            best = [m for m, v in mv.items() if v == c["real"]]
            kinds = {m[0] for m in best}
            c["best_moves"] = best
            c["diagnosis"] = ("escape: only king moves (leaving the trebuchet) reach the real result"
                              if kinds == {"K"} else "a pawn move the convention counts as losing does better")
        else:  # convention: mover wins
            wins = []
            for m in mv:
                if m[0] != "P":
                    continue
                pred, val = convention_after(c["P"], m, stm, pfiles, H, ep_on)
                if pred == good:
                    wins.append((m, val))
            c["convention_winning_moves"] = [m for m, _ in wins]
            c["creates_passer"] = [m for m, val in wins if val in ("+W", "-W")]
            if not wins:
                c["diagnosis"] = "no pawn move the convention counts as winning (its win is by zugzwang)"
            for m, _ in wins:
                child = apply_move(c["line"], m, ep_on)
                c.setdefault("children", {})[m] = child
                need.append(child)
    if need:
        children = kpsolve_moves(sorted(set(need)), summary)
    tally = Counter()
    for c in cases:
        if "children" in c:
            refs = {}
            for m, child in c["children"].items():
                a, _b, mv = children[child]
                refs[m] = {"real_after": a, "refutations": [r for r, v in mv.items() if v == a]}
            c["refutations"] = refs
            kinds = {r[0] for v in refs.values() for r in v["refutations"]}
            if not refs:
                c["diagnosis"] = "no pawn move the convention counts as winning (win was by zugzwang elsewhere)"
            elif kinds == {"K"}:
                c["diagnosis"] = "king refutes: every refutation of the convention's winning moves is a king move"
            else:
                c["diagnosis"] = "pawn or mixed refutation of the convention's winning moves"
            c.pop("children")
        tally[c["diagnosis"]] += 1
    out_path = path.replace(".jsonl", "_diagnosis.jsonl")
    with open(out_path, "w") as fh:
        for c in cases:
            fh.write(json.dumps(c) + "\n")
    print(json.dumps({"file": path, "mismatching sides": len(cases), "diagnoses": dict(tally)}, indent=1))


if __name__ == "__main__":
    main()
