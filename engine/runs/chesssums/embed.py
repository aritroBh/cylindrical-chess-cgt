"""Embed 8-file ChessSums instances into legal 8x8 FENs with a king freeze."""
import json, sys, glob, os
from pathlib import Path
from collections import Counter

ROOT = Path(".")
OUT = Path(__file__).resolve().parent
FILES = "abcdefgh"

def occ_set(placement):
    sqs = set(); pieces = {}
    for i, row in enumerate(placement.split("/")):
        r = 8 - i; f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                sqs.add((f, r)); pieces[(f, r)] = ch; f += 1
    return sqs, pieces

def king_in_check(king_sq, enemy_pawns, king_color):
    fx, fy = king_sq
    if king_color == "W":
        return (fx - 1, fy + 1) in enemy_pawns or (fx + 1, fy + 1) in enemy_pawns
    return (fx - 1, fy - 1) in enemy_pawns or (fx + 1, fy - 1) in enemy_pawns

def candidates(sqs, pieces):
    white_pawns = {(f, r) for (f, r), ch in pieces.items() if ch == "P"}
    black_pawns = {(f, r) for (f, r), ch in pieces.items() if ch == "p"}
    res = []
    for orient in ("A", "B"):
        for r in range(2, 7):
            for p in range(1, 7):
                if orient == "A":
                    wp, bp, wk, bk = (p, r), (p, r + 1), (p - 1, r + 1), (p + 1, r)
                else:
                    wp, bp, wk, bk = (p, r), (p, r + 1), (p + 1, r + 1), (p - 1, r)
                if any(s in sqs for s in (wp, bp, wk, bk)):
                    continue
                if king_in_check(wk, black_pawns, "W"):
                    continue
                if king_in_check(bk, white_pawns, "B"):
                    continue
                if max(abs(wk[0] - bk[0]), abs(wk[1] - bk[1])) <= 1:
                    continue
                cost = abs(p - 6) + abs(r - 4) + (0 if orient == "A" else 1)
                res.append((cost, orient, r, p, wk, bk, wp, bp))
    res.sort()
    return res

def make_fen(pieces, freeze):
    grid = dict(pieces); grid.update(freeze)
    rows = []
    for r in range(8, 0, -1):
        s = ""; empty = 0
        for f in range(8):
            ch = grid.get((f, r))
            if ch is None:
                empty += 1
            else:
                if empty:
                    s += str(empty); empty = 0
                s += ch
        if empty:
            s += str(empty)
        rows.append(s)
    return "/".join(rows)

def uci_move(m):
    return m.replace("-", "")

def value_class_4(v):
    if "W" in v:
        vc = "hot-BIG" if ("|" in v or "±" in v) else "decided"
    elif v.lstrip("-").replace("/", "").isdigit():
        vc = "number"
    elif v.startswith("*"):
        vc = "nimber"
    elif any(a in v for a in "↑↓⇑⇓"):
        vc = "infinitesimal"
    elif "±" in v and "|" not in v:
        vc = "switch"
    else:
        vc = "other-tame"
    if vc in ("other-tame", "hot-BIG", "decided", "switch"):
        return "switch"
    return vc

# read all 8-file subsets
all_rows = []
for path in sorted(glob.glob(str(ROOT / "bench/data/*_8file.jsonl"))):
    for line in open(path):
        line=line.strip()
        if line:
            all_rows.append(json.loads(line))

meta = []
epd_lines = []
bad = 0
for row in all_rows:
    sqs, pieces = occ_set(row["placement"])
    cands = candidates(sqs, pieces)
    if not cands:
        bad += 1
        continue
    cost, orient, r, p, wk, bk, wp, bp = cands[0]
    freeze = {wp: "P", bp: "p", wk: "K", bk: "k"}
    fen_board = make_fen(pieces, freeze)
    outcome = row["outcome"]
    if outcome == "R":
        stm = "b"
        sols = [uci_move(m) for m in row["winning_moves"]["B"]]
    else:
        stm = "w"
        sols = [uci_move(m) for m in row["winning_moves"]["W"]]
    fen4 = f"{fen_board} {stm} - -"
    vc4 = value_class_4(row["value"])
    c2_field = " ".join(f'"{m}"' for m in sols) if sols else '""'
    c3 = f'value-class={vc4}; bench-kind={row["kind"]}; k={row["k"]}; outcome={outcome}; split={row["split"]}; id={row["id"]}'
    epd = f'{fen4} id "{row["id"]}"; c2 {c2_field}; c3 "{c3}";'
    epd_lines.append(epd)
    meta.append({
        "id": row["id"],
        "split": row["split"],
        "fen": fen4,
        "stm": stm,
        "k": row["k"],
        "outcome": outcome,
        "value": row["value"],
        "value_class": vc4,
        "bench_kind": row["kind"],
        "solutions_uci": sols,
        "freeze": {"orient": orient, "rank": r, "file": p,
                   "wk": f"{FILES[wk[0]]}{wk[1]}", "bk": f"{FILES[bk[0]]}{bk[1]}",
                   "wp": f"{FILES[wp[0]]}{wp[1]}", "bp": f"{FILES[bp[0]]}{bp[1]}"},
        "original_men": len(row["white"]) + len(row["black"]),
        "total_men": len(row["white"]) + len(row["black"]) + 4,
    })

(OUT / "chesssums.epd").write_text("\n".join(epd_lines) + "\n")
(OUT / "meta.json").write_text(json.dumps(meta, indent=1))
print("embedded", len(meta), "bad", bad)
print("by k", Counter(m["k"] for m in meta))
print("by class", Counter(m["value_class"] for m in meta))
print("by outcome", Counter(m["outcome"] for m in meta))
