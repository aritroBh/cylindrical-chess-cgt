#!/bin/sh
# Build the replica solver and solve every endgame of the B2 replication on all
# three boards, with the Bellman and symmetry checks. Output goes to results/.
set -e
cd "$(dirname "$0")"
cc -O2 -Wall -Wextra -o replica replica.c
mkdir -p results
for topo in plane cyl torus; do
  for men in Q R BB BN NN RB RR QR; do
    ./replica "$topo" "$men" check > "results/${topo}_${men}.txt" 2>&1
    cat "results/${topo}_${men}.txt"
  done
done
