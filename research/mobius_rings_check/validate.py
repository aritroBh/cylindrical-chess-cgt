"""Compare a deterministic sample of small single-component cylinder games."""
import random
import subprocess
from collections import Counter
from pathlib import Path

from cylcgt import cgt, pawns

board = pawns.Board(3, 8, True, True)
assert pawns.PASSED_RESPECTS_EP and pawns.RACE_RULE == "count"
rng = random.Random(77)
squares = [(f, r) for f in range(3) for r in range(2, 8)]
cases = {}
while len(cases) < 300:
    size = rng.randint(2, 5)
    cells = rng.sample(squares, size)
    cut = rng.randrange(1, size)
    pos = pawns.Pos(frozenset(cells[:cut]), frozenset(cells[cut:]))
    if pos in cases or any(pawns.passed(board, pos, side) for side in "WB"):
        continue
    tokens = []
    for f in range(3):
        token = ""
        for side, army in (("W", pos.white), ("B", pos.black)):
            ranks = sorted(r for file, r in army if file == f)
            if ranks:
                token += side + "".join(map(str, ranks))
        tokens.append(token or "-")
    cases[pos] = " ".join(tokens)

binary = Path(__file__).with_name("check").resolve()
run = subprocess.run([binary, "cylinder", "3", "solve"],
                     input="\n".join(cases.values()) + "\n",
                     text=True, capture_output=True, check=True)
signature_counts = Counter()
for (pos, tokens), actual in zip(cases.items(), run.stdout.splitlines(), strict=True):
    game = pawns.value(board, pos)
    ref = "".join(cgt.outcome(cgt.add(game, cgt.nimber(h))) for h in range(4))
    assert actual == ref, (tokens, actual, ref)
    signature_counts[ref] += 1
print(f"{len(cases)} distinct positions matched at every heap size")
print(dict(sorted(signature_counts.items())))
