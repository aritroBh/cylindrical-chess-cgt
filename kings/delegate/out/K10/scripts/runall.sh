#!/bin/bash
cd /Users/aritro/Downloads/Research/Chessendgames
export PYTHONPATH=.
for cfg in "8 6 2" "6 7 3" "6 5 3" "7 6 3"; do
  echo "== $cfg" >> /private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k10/fin/direct.log
  nice -n 10 .venv/bin/python /private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k10/fin/direct.py $cfg 2>&1 | cut -c1-1200 >> /private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k10/fin/direct.log
done
echo DONE >> /private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k10/fin/direct.log
