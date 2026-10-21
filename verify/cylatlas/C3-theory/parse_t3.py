"""Extract the 53 W-free cylinder-only rows (value, n, witness) from atlas/cylinder/logs/tables.txt T3."""
import json, re, sys
rows = []
on = False
for line in open("atlas/cylinder/logs/tables.txt"):
    if line.startswith("## T3"):
        on = True; continue
    if on and line.startswith("values on some flat"):
        break
    if on and line.startswith("| ") and not line.startswith("| value"):
        parts = [p.strip() for p in line.strip().strip("|").split(" | ")]
        # value may contain ' | ' itself; last 4 fields are cls, temp, n, witness
        wit = parts[-1]; n = int(parts[-2]); temp = parts[-3]; cls = parts[-4]
        val = " | ".join(parts[:-4])
        rows.append({"value": val, "cls": cls, "temp": temp, "n": n, "pos": wit})
json.dump(rows, open("verify/cylatlas/C3-theory/t3_rows.json", "w"), indent=1, ensure_ascii=False)
from collections import Counter
print(len(rows), Counter(r["n"] for r in rows))
