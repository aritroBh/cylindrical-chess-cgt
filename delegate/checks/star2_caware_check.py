"""Every T8 hit whose settings include count/e.p.-aware (C/aware), re-evaluated with cylcgt on the board of its
scope (flat for scopes a-c, the 5..8-file cylinder for scope d), and on the flat 8-file board.

    PYTHONPATH=. .venv/bin/python delegate/checks/star2_caware_check.py
"""
import re

from cylcgt import cgt, pawns

pawns.RACE_RULE = "count"
pawns.PASSED_RESPECTS_EP = True
scope = None
for line in open("research/star2_frontier/all_candidates.txt"):
    m = re.match(r"research/star2_frontier/scope_(\w+?)\.tsv", line)
    if m:
        scope = m.group(1)
        continue
    m = re.match(r"\s+(\d+) pawns; settings=(\S+); trébuchet-fit=(\w+); (W: .*)$", line)
    if not m or "C/aware" not in m.group(2).split(","):
        continue
    text = m.group(4)
    pos = pawns.Pos.parse(text)
    width = 1 + max(f for f, _ in pos.white | pos.black)
    boards = {}
    if scope.startswith("d_c"):
        boards[f"C{scope[3:]}"] = pawns.Board(int(scope[3:]), 8, True, True)
    else:
        boards[f"F{width}"] = pawns.Board(width, 8, False, True)
    boards["F8"] = pawns.Board(8, 8, False, True)
    out = []
    for k, b in boards.items():
        pawns._value.cache_clear()
        out.append(f"{k} {cgt.show(pawns.value(b, pos))}")
    print(f"scope {scope:5s} {m.group(1)}p {text:34s} T8 settings {m.group(2):24s} | " + " | ".join(out), flush=True)
