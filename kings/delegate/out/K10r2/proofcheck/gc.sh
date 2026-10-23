#!/bin/sh
# gc.sh tag W H maxp flo fhi   (env DROP, SLACK pass through)
S=/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k10r2
cd /Users/aritro/Downloads/Research/Chessendgames; export PYTHONPATH=.
tag=$1; W=$2; H=$3; maxp=$4; flo=$5; fhi=$6
nice -n 10 .venv/bin/python $S/cons.py $W $H $maxp $flo $fhi $S/$tag 2>&1 | tail -2
nice -n 10 $S/kp --board cyl:${W}x${H} --ep on --promote QRBN --cap 1 --frozen --threads 2 < $S/$tag.pos > $S/$tag.res 2>$S/$tag.err
tail -1 $S/$tag.err
.venv/bin/python $S/cons_cmp.py $S/$tag | tail -4
