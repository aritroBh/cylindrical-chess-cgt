#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/verify
: > $D/children2.out
while [ ! -f $D/own_capt_single.done ]; do sleep 5; done
for n in 1 2; do
  line=$(sed -n "${n}p" $D/children2.txt)
  ( ulimit -t 58; echo "$line" | nice -n 15 $D/work/kp --board flat:7x6 --cap 1 2>>$D/children2.err | grep '|' >> $D/children2.out )
  for b in 0 1; do
    r=$( ( ulimit -t 58; echo "$line" | nice -n 15 $D/work/ownchess 7 6 $b 2>>$D/children2.err ) )
    echo "own bound=$b $r" >> $D/children2.out
  done
done
echo done > $D/children2.done
