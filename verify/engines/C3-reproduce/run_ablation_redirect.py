#!/usr/bin/env python3
"""Run the worker's engine/ablation/run_ablation.py unchanged, but write results into
verify/engines/C3-reproduce/results/ instead of engine/ablation/results/ (worker files are read-only).
Usage (from project root): .venv/bin/python verify/engines/C3-reproduce/run_ablation_redirect.py <run_ablation args>"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "engine" / "ablation"))
import run_ablation  # noqa: E402
run_ablation.HERE = Path(__file__).resolve().parent   # only used for outdir = HERE / "results"
sys.argv = ["run_ablation.py"] + sys.argv[1:]
run_ablation.main()
