#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/verify
for i in 0 1 2 3; do
  /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh /Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python scripts/my_t2.py cyl:8x6 2 2 logs/my_cyl8x6_22_s${i}of4.json $i/4 2> logs/my_cyl8x6_22_s${i}of4.err
done
