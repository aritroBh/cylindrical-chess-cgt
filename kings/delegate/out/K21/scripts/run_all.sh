#!/bin/zsh
# reproduces every abstract number in REPORT.md (each command < 1 CPU-minute)
cd "$(dirname "$0")"
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
mkdir -p ../logs
for s in 101 102 103; do KRICH=0 $PY run_tests.py bridge 6000 $s 5 > ../logs/bridge_B5_s$s.json; done
for s in 111 112; do KRICH=1 $PY run_tests.py bridge 4000 $s 7 > ../logs/bridge_rich_B7_s$s.json; done
for s in 201 202 203; do KRICH=1 $PY run_tests.py sandwich 5000 $s > ../logs/sandwich_s$s.json; done
for s in 301 302; do KRICH=1 $PY run_tests.py stopper 8000 $s > ../logs/stopper_s$s.json; done
for s in 401 402 403; do KRICH=1 $PY run_tests.py regime 4000 $s 14 > ../logs/regime_B14_s$s.json; done
for s in 501 502; do KRICH=1 $PY run_tests.py subadd 3000 $s 5 > ../logs/subadd_s$s.json; done
for s in 601 602; do KRICH=1 $PY run_tests.py thm34 8000 $s > ../logs/thm34_s$s.json; done
for s in 701; do KRICH=1 $PY run_tests.py over46 8000 $s > ../logs/over46_s$s.json; done
for s in 801; do $PY crosscheck.py 6000 $s 5 > ../logs/crosscheck_s$s.json; done
$PY search_c1.py 1 30000 > ../logs/search_c1_s1.txt
for s in 901 902 903; do KRICH=1 $PY run_tests.py thm111b 6000 $s > ../logs/thm111b_s$s.json; done
$PY crosscheck.py 3000 7 5 > ../logs/crosscheck_s007.json
for s in 1001 1002; do KRICH=1 $PY run_tests.py pure 4000 $s > ../logs/pure_s$s.json; done
for s in 1101 1102 1103; do KRICH=1 $PY run_tests.py onestopper 6000 $s > ../logs/onestopper_s$s.json; done
