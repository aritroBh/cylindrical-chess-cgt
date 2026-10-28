#!/bin/zsh
# referee: ownchess on the six decisive capture positions, one process per position, each under one CPU-minute (ulimit -t 58), nice 15
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/verify
: > $D/own_capt_single.out
for spec in "1 0" "3 0" "5 0" "4 1" "6 1" "8 1"; do
  set -- ${=spec}
  line=$(sed -n "${1}p" $D/capt8.txt)
  r=$( ( ulimit -t 58; echo "$line" | nice -n 15 $D/work/ownchess 7 6 $2 2>>$D/own_capt_single.err ) )
  echo "bound=$2 $r" >> $D/own_capt_single.out
done
echo done > $D/own_capt_single.done
