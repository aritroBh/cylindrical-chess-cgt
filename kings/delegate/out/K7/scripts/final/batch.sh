#!/bin/sh
cd /private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k7/w
for cfg in "11 6000 7 6 cyl a1 4 ctx" "12 6000 7 6 cyl a2 4 mix" "13 4000 8 6 cyl a3 4 ctx" "14 4000 6 6 flat a4 4 ctx" "15 4000 7 5 cyl a5 3 ctx" "16 4000 7 7 cyl a6 4 ctx" "17 6000 7 6 cyl a7 5 z"; do
  nice -n 10 /Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python ept.py $cfg 2>&1 | tail -20 >> batch.log
done
echo done > batch.done
