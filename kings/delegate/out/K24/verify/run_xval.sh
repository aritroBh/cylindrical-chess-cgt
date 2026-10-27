#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K24/verify
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
$PY xval.py cyl:5x6 250 101 1 1
$PY xval.py flat:5x6 250 102 1 1
$PY xval.py cyl:6x6 200 103 1 1
$PY xval.py cyl:5x6 80 104 2 1
$PY xval.py flat:5x6 80 105 1 2
