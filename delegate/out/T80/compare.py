"""Compare saved census rows to published data without loading either solver."""
import csv
import json
import re
import subprocess
from itertools import product
from pathlib import Path

out = Path(__file__).resolve().parent
published = out.parents[2] / "research/tall_boards/results"
expected = {}
with (published / "table.tsv").open() as source:
    for row in csv.DictReader(source, delimiter="\t"):
        geometry, files = row["board"].split()
        rank = int(row["R"])
        if rank not in (5, 6) and (rank, files) != (7, "3"):
            continue
        assert row["exhausted"] == "1"
        board = {"flat": "F", "cyl": "C"}[geometry] + files
        counts = json.loads(row["counts_by_nimber_over_all_levels"])
        assert not json.loads(row["geq4"])
        minima = [row["least_*" + str(k)] for k in (2, 3)]
        expected[rank, board] = [
            int(row["N_roots_complete"]),
            *(counts.get("*" + str(k), 0) for k in range(8)),
            *(0 if v.startswith("none") else int(v) for v in minima),
        ]

old_splits = {}
raw = subprocess.check_output(["zstd", "-dc", published / "raw/F5c_R6_pass1.out.zst"], text=True)
for line in raw.splitlines():
    if line.startswith("#scan "):
        a, b, n = map(int, re.search(r"split=(\d+)\+(\d+).*roots=(\d+)$", line).groups())
        assert (a, b) not in old_splits
        old_splits[a, b] = [n] + [0] * 8
    elif line.startswith("#hist"):
        _, signature, count = line.split()
        if sorted(signature) == sorted("PNNNNNNN"):
            old_splits[a, b][1 + signature.index("P")] = int(count)
    elif line.startswith("#done"):
        assert "complete=1 " in line

new_splits = {}
for line in (out / "splits.txt").read_text().splitlines():
    a, b, *counts = map(int, line.split())
    assert (a, b) not in new_splits
    new_splits[a, b] = counts

# At 20 pawns ranks 2 and 5 are forced. A letter gives the two middle
# colours, BB/BW/WB/WW. Rank reversal plus colour swap exchanges BB and WW.
orbits = set()
for ring in product(range(4), repeat=5):
    swapped = tuple((3, 1, 2, 0)[v] for v in ring)
    orbits.add(min(word[i:] + word[:i]
                   for word in (ring, ring[::-1], swapped, swapped[::-1])
                   for i in range(5)))
assert len(orbits) == sum(v[0] for (a, b), v in new_splits.items() if a + b == 20)

# Verify every legal material bin, and record the source rows outside the class.
impossible = []
for a, b in sorted(old_splits.keys() | new_splits.keys()):
    if b <= 15:  # each colour has 3 eligible ranks x 5 files
        assert new_splits.get((a, b)) == old_splits.get((a, b)), (a, b)
    else:
        assert (a, b) not in new_splits
        impossible.append(old_splits[a, b])
        print(f"Outside the class: {a}+{b}, published roots and *0..*7 =", old_splits[a, b])
extra = list(map(sum, zip(*impossible)))
total = full_matches = 0
for line in (out / "census.txt").read_text().splitlines():
    rank, board, *fields = line.split()
    actual = list(map(int, fields))
    target = expected.pop((int(rank), board))
    if (rank, board) == ("6", "C5"):
        assert actual[:9] == list(map(sum, zip(*new_splits.values())))
        target = [v-e for v, e in zip(target[:9], extra)] + target[9:]
        print("C5 R6 valid roots at 20 pawns:", len(orbits))
    else:
        full_matches += 1
    assert actual == target, (rank, board, actual, target)
    total += actual[0]
assert not expected, expected
print(f"{total:,} independent roots, {full_matches} published boards match as printed.")
