"""Merge the per-budget Lc0 runs into one file in the layout of sf19_nodes.json,
so engine/runs/analyze_sf.py can score it:
    .venv/bin/python engine/runs/analyze_sf.py engine/runs/lc0/lc0_nodes.json
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
merged = {"engine": None, "limits": [], "results": []}
for n in [1000, 10000, 100000, 1000000]:
    path = HERE / f"lc0_nodes_{n}.json"
    if not path.exists():
        continue
    d = json.loads(path.read_text())
    merged["engine"] = merged["engine"] or d.get("engine")
    merged["limits"] += d["limits"]
    merged["results"] += d["results"]
(HERE / "lc0_nodes.json").write_text(json.dumps(merged, indent=1))
print(f"merged {len(merged['results'])} results over {merged['limits']}")
