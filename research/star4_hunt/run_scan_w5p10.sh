#!/bin/bash
# exhaustive flat width-5, 10-pawn, single-component scan (default setting), chunked, sequential
cd "$(dirname "$0")"
mkdir -p out/w5p10 logs
scan() { # nw nb chunks extra
  local nw=$1 nb=$2 n=$3 extra=$4
  for ((i=0;i<n;i++)); do
    f=out/w5p10/${nw}_${nb}_c${i}of${n}
    [ -f $f.done ] && continue
    nice -n 15 ./h4 --flat --width 5 --single --nw $nw --nb $nb $extra --chunk $i $n --max-entries 33554432 > $f.tsv 2> $f.err && touch $f.done
  done
}
scan 2 8 2 ""
scan 3 7 12 ""
scan 5 5 24 "--colsym"
scan 4 6 32 ""
echo ALLDONE > logs/scan_w5p10.done
