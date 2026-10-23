#!/bin/bash
# duel boards (one W and one B pawn on every file) in chunks: flat w6, C6
cd "$(dirname "$0")"
while [ ! -f logs/queue9.done ]; do sleep 20; done
mkdir -p out/duel6
for ((i=0;i<8;i++)); do
  [ -f out/duel6/flat_w6_c${i}.done ] || { nice -n 15 ./h4 --flat --width 6 --max-entries 16777216 --duel --chunk $i 8 > out/duel6/flat_w6_c${i}.tsv 2>/dev/null && touch out/duel6/flat_w6_c${i}.done; }
done
for ((i=0;i<16;i++)); do
  [ -f out/duel6/cyl_w6_c${i}.done ] || { nice -n 15 ./h4 --cylinder --width 6 --max-entries 16777216 --duel --chunk $i 16 > out/duel6/cyl_w6_c${i}.tsv 2>/dev/null && touch out/duel6/cyl_w6_c${i}.done; }
done
echo ALLDONE > logs/queue11.done
