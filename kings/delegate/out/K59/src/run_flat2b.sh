#!/bin/zsh
# K59: F2..F5 on flat 9x7 and 8x8 (translates, one rank up), Definition 4.8 with ref3m and kp_p.
cd "$(dirname $0)/.."
python3 src/groupsF.py ref3m > logs/p2d_F2to5_ref3m.txt 2>&1
python3 src/groupsF.py kpp > logs/p2d_F2to5_kpp.txt 2>&1
