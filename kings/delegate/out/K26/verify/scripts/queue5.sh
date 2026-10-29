#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/verify
echo $$ > logs/queue5.pid
while [[ ! -f logs/queue4.done ]]; do sleep 20; done
for nb in "3 2" "2 3"; do
  for i in 0 1 2 3 4 5 6 7; do
    /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh /bin/zsh -c "cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/verify; python3 scripts/ref_under.py cyl:8x6 ${nb} 3 $i/8 2>/dev/null >> logs/under_cyl8x6_${nb// /}.txt"
  done
done
echo finished > logs/queue5.done
