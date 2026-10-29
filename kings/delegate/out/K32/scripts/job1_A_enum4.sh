#!/bin/zsh
# job 1: exhaustive n=4 with implementation A, root-only tally (one line per rooted isomorphism class)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K32
K32_ROOT=1 /private/tmp/claude-501/k32A2 enum 4 > logs/A_enum4_root.txt
