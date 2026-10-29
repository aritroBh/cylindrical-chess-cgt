#!/bin/zsh
# run_screen.sh [first]: Phase 1 screen.  For every configuration in configs.txt run grp --mode test --first N (default 1)
# over the symmetry-class representatives (data/rep_*.txt) through the shared heavy lock; one heavy.sh call per configuration.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29
cd $D
FIRST=${1:-1}
grep -v '^#' scripts/configs.txt | while read name board zs fz dmin rep; do
  [[ -s data/screen_${name}.txt ]] && continue
  /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh /usr/bin/time -l ./bin/grp --board $board --mode test --zs $zs --fz $fz --dmin $dmin --cw 2 --cb 2 --first $FIRST < data/rep_${rep}.txt > data/screen_${name}.tmp 2> logs/screen_${name}.err
  mv data/screen_${name}.tmp data/screen_${name}.txt
  echo "$name done $(date +%H:%M)" >> logs/screen_progress.txt
done
