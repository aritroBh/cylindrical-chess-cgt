#!/bin/sh
cd /private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k7/w
while [ ! -f batch.done ]; do sleep 20; done
for cfg in "21 8000 7 6 cyl b1 4 ctx" "22 6000 7 6 cyl b2 4 mix" "23 5000 8 6 cyl b3 4 ctx" "24 5000 6 6 flat b4 4 ctx" "25 5000 7 5 cyl b5 3 ctx" "26 5000 7 7 cyl b6 4 ctx"; do
  nice -n 10 /Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python ept2.py $cfg 2>&1 | tail -20 >> batch2.log
done
echo done > batch2.done
