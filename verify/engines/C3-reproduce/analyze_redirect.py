#!/usr/bin/env python3
"""Run the worker's engine/ablation/analyze.py unchanged, but on verify/engines/C3-reproduce/results/."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "engine" / "ablation"))
import analyze  # noqa: E402
analyze.HERE = Path(__file__).resolve().parent
analyze.main(); analyze.equal_nodes(); analyze.depth1_misses()
