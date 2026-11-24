#!/bin/zsh
# K59: measure p45a and r48 on small inputs of flat 8x7 (files a, b, e) before the full searches.
cd "$(dirname $0)/.."
mkdir -p logs/search
src/hrun.sh search/meas_A_11 bin/p45a --kind flat --W 8 --H 7 --files 0,1,4 --nw 1 --nb 1 --mode both
src/hrun.sh search/meas_R_11 bin/r48 enum pln:8x7 0,1,4 1 1
src/hrun.sh search/meas_A_22 bin/p45a --kind flat --W 8 --H 7 --files 0,1,4 --nw 2 --nb 2 --mode both
src/hrun.sh search/meas_R_22 bin/r48 enum pln:8x7 0,1,4 2 2
