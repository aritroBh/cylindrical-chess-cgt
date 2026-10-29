#!/bin/zsh
# K39 (resumed session): re-run the part-2 runs that the first session's 1180 s wall limit cut off (c3 own39p, c4 kp39p),
# with a 3300 s wall. usage: rerun.sh A|B   (A: c3 own39p b0, then c4 kp39p A; B: c3 own39p b1, then c4 kp39p B)
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K39
cd $D
echo "$$ rerun.sh $1" >> pids.log
if [[ $1 == A ]]; then
  scripts/hrun.sh c3_own_b0 3300 in/ctx/c3.zh.in bin/own39p 7 6 0 0 1 1
  scripts/hrun.sh c4_kp_A 3300 in/ctx/c4.zh.in bin/kp39p --board flat:7x6 --cap 1 --refine --bound A --moves --threads 2
else
  scripts/hrun.sh c3_own_b1 3300 in/ctx/c3.zh.in bin/own39p 7 6 0 1 1 1
  scripts/hrun.sh c4_kp_B 3300 in/ctx/c4.zh.in bin/kp39p --board flat:7x6 --cap 1 --refine --bound B --moves --threads 2
fi
