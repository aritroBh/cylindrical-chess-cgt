#!/usr/bin/env bash
set -euo pipefail
cd /Users/aritro/Downloads/Research/Chessendgames
export PYTHONPATH=.
nice -n 10 .venv/bin/python -m pytest kings/delegate/out/K5/test_canon.py -q
nice -n 10 .venv/bin/python kings/delegate/out/K5/check_targets.py
