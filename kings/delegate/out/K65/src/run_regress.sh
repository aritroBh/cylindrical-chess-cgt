#!/bin/zsh
# K65 regression: both programs (K65 copies, r48 with the two-file option) must reproduce K59's flat 8x7 counters for
# the class {b,c,f} exactly (785,481,597 placements, 3 exact over groups).  A = p45a over orientation, R = r48 (under).
cd "$(dirname $0)/.."
zsh src/hrunw.sh regress/A87_125 bin/p45a --kind flat --W 8 --H 7 --files 1,2,5 --nw 3 --nb 3 --mode over &
zsh src/hrunw.sh regress/R87_125 bin/r48 enum pln:8x7 1,2,5 3 3 &
wait
