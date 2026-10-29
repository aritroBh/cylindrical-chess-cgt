#!/bin/zsh
# K39 (resumed session): the packed binaries kp39p and own39p on the flat 7x6 random set of val.sh (cap 1, refinement),
# compared with the unpacked kp39 / own39 outputs. usage: valp.sh kp|own
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K39
cd $D
echo "$$ valp.sh $1" >> pids.log
if [[ $1 == kp ]]; then
  scripts/hrun.sh valp_kp39p_flat_7x6 1500 in/rand_flat_7x6.in bin/kp39p --board flat:7x6 --ep on --promote QRBN --cap 1 --refine --moves
else
  scripts/hrun.sh valp_own39p_flat_7x6_b0 1500 in/rand_flat_7x6.in bin/own39p 7 6 0 0 1 1
  scripts/hrun.sh valp_own39p_flat_7x6_b1 1500 in/rand_flat_7x6.in bin/own39p 7 6 0 1 1 1
fi
