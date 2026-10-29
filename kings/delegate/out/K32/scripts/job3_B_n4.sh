#!/bin/zsh
# independent evaluation (implementation B) of every rooted stopper class on 4 nodes, per-node comparison with A, tally by tally.py
S=/private/tmp/claude-501/k32work; P=/private/tmp/claude-501
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K32
bad=0
for c in $S/c4_*; do
  nice -n 15 $P/k32B < $c > $c.B
  nice -n 15 $P/k32A2 eval p < $c | grep '^G' > $c.A
  cmp $c.A $c.B || bad=1
done
echo "per-node A vs B comparison over all chunks: bad=$bad"
