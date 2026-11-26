#!/bin/zsh
# K65: measure p45a and r48 on small inputs of flat 8x8 (files b, c, f) before any long run; every run under the watchdog.
cd "$(dirname $0)/.."
zsh src/hrunw.sh meas/A88_125_22_over bin/p45a --kind flat --W 8 --H 8 --files 1,2,5 --nw 2 --nb 2 --mode over &
zsh src/hrunw.sh meas/R88_125_22 bin/r48 enum flat:8x8 1,2,5 2 2 &
wait
zsh src/hrunw.sh meas/A88_125_22_both bin/p45a --kind flat --W 8 --H 8 --files 1,2,5 --nw 2 --nb 2 --mode both
