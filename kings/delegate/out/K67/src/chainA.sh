#!/bin/zsh
# K67 phase A: regression, then p45a (over orientation) on the two new classes.  One run at a time, each through
# src/run.sh (heavy.sh, /usr/bin/time -l, watchdog); the chain stops at logs/STOP (written by any watchdog kill).
cd "$(dirname $0)/.."
step() { [[ -f logs/STOP ]] && { echo "STOP: chain halted before $1"; exit 1; }; [[ -f logs/$1.rc ]] && return; zsh src/run.sh "$@"; echo "$1 $(cat logs/$1.rc) $(grep -E ' real' logs/$1.err) $(grep 'maximum resident' logs/$1.err)"; }
step regress/A87_125 bin/p45a --kind flat --W 8 --H 7 --files 1,2,5 --nw 3 --nb 3 --mode over
step regress/R88_125_22 bin/r48 enum flat:8x8 1,2,5 2 2
step search/A88_f0_1_4 bin/p45a --kind flat --W 8 --H 8 --files 0,1,4 --nw 3 --nb 3 --mode over
step search/A88_f0_3_4 bin/p45a --kind flat --W 8 --H 8 --files 0,3,4 --nw 3 --nb 3 --mode over
echo "chain A done $(date +%H:%M:%S)"
