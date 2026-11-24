#!/bin/zsh
# K48: the final r48 binary (with the memo front cache) re-checked against ref3m on the random flat 8x6 and 10x6 positions and on the K45 group.
cd "$(dirname $0)/.."
scripts/hrun.sh val2_r48_flat8 2400 in/rnd_flat8.txt bin/r48 val pln:8x6
scripts/hrun.sh val2_r48_flat10 2400 in/rnd_flat10.txt bin/r48 val pln:10x6
scripts/hrun.sh grp2_r48_cyl8 1200 /dev/null bin/r48 group cyl:8x6 over "Pb2 Pb4 Pe2 pa4 pb5 pe5" d4 d5 f5
echo done > logs/val_flat2.done
