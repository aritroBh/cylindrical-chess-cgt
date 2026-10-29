#!/bin/zsh
# sequential tail of the K15 queue; waits for the earlier K15 jobs (pmodel + chain2) to finish first
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15
while kill -0 42334 2>/dev/null; do sleep 20; done
/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh ./kp --board cyl:8x6 --cap 1 --threads 2 < conf/c86chess.in > conf/c86chess.out 2> conf/c86chess.err
echo "done chess exit=$?" >> runs/census.log
./run_census2.sh 8 6 3 12 12
./run_census2.sh 6 6 3 12 12
