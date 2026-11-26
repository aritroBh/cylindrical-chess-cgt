"""Compare finished independent tallies with the designated Lean reference."""
from collections import defaultdict
from pathlib import Path
import re

root = Path('delegate/out/L14_codex')
rows = defaultdict(lambda: [0]*5)
for line in (root/'full.out').read_text().splitlines():
    w,k,*vals = map(int,line.split('gapped')[0].split())
    rows[w,k] = [a+b for a,b in zip(rows[w,k], vals, strict=True)]
expected = {}
for w,k,fields in re.findall(r'\((\d+), (\d+), ⟨([\d, ]+)⟩\)', Path('lean/CylChess/CensusData.lean').read_text()):
    r,p,z,s,other,big,failed = map(int,fields.split(', '))
    assert other == r-z-s-big and failed == 0
    expected[int(w),int(k)] = [r,p,z,s,big]
assert set(rows) == set(expected) == {(w,k) for w in range(1,5) for k in range(2,7)}
for key in sorted(rows):
    assert rows[key] == expected[key], (key, rows[key], expected[key])
    print(*key,*rows[key])
print('total',*(sum(col) for col in zip(*rows.values())))
