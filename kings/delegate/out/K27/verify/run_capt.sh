#!/bin/zsh
# referee: re-run the 8 capture positions with kp (cap 1), one at a time, each under one CPU-minute (ulimit -t 58), nice 15
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/verify
while IFS= read -r line; do
  [[ -z $line ]] && continue
  ( ulimit -t 58; echo "$line" | nice -n 15 $D/work/kp --board flat:7x6 --cap 1 2>>$D/kp_capt.err | grep '|' >> $D/kp_capt.out )
done < $D/capt8.txt
echo done > $D/kp_capt.done
