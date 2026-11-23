#!/bin/zsh
cd "$(dirname $0)"
/usr/bin/time -l ./rz_k47ref 8 6 roots_gap.txt t0.txt C pv > logs/gap_C.out 2> logs/gap_C.err
