#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/final
for j in "cyl:7x6 alone" "cyl:8x6 alone" "cyl:7x6 ZB_blocked" "cyl:7x6 ZB_onemove" "cyl:7x6 D2m_blocked" "cyl:7x6 ZB_gap" "cyl:7x6 D2m_onemove"; do
  set -- ${=j}; ./run_chess.sh $1 $2 1
done
echo finished > chess/queue1.done
