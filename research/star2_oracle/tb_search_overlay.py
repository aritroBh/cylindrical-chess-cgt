"""Convert exact side-to-move intervals from resolve_tb.py to a WDL overlay.

Usage:
    PYTHONPATH=. .venv/bin/python research/star2_oracle/tb_search_overlay.py \
        research/star2_oracle/tb_A_8men.json > research/star2_oracle/search_A_8men.overlay.out
"""
import json
import sys

WDL = {1: "W", 0: "D", -1: "L"}


def tokens(fen):
    board, stm, _castle, ep = fen.split()[:4]
    out = []
    for i, row in enumerate(board.split("/")):
        rank, f = 8 - i, 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                out.append(f"{ch}{'abcdefgh'[f]}{rank}")
                f += 1
    return " ".join(out) + f" {stm} {ep}"


d = json.load(open(sys.argv[1]))
print(f"# exact overlay from {sys.argv[1]} (Searcher interval; WDL is side-to-move view)")
for row in d["sides"]:
    interval = row.get("interval")
    if interval is None or interval[0] != interval[1]:
        continue
    result = WDL[interval[0]]
    print(f"# {row['terminal']} men={row['men']} side={row['side']} FEN={row['fen']}")
    print(f"{tokens(row['fen'])} | {result} {result}")
