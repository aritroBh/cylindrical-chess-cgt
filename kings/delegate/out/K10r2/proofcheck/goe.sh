#!/bin/sh
# goe.sh tag seed N W H maxp
S=/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k10r2
cd /Users/aritro/Downloads/Research/Chessendgames; export PYTHONPATH=.
tag=$1; seed=$2; N=$3; W=$4; H=$5; maxp=$6
nice -n 10 .venv/bin/python $S/e2e.py gen $seed $N $W $H $maxp $S/$tag 2>&1 | cut -c1-200
nice -n 10 $S/kp --board cyl:${W}x${H} --ep on --promote QRBN --cap 1 --frozen --threads 2 < $S/$tag.pos > $S/$tag.res 2>$S/$tag.err
tail -1 $S/$tag.err
.venv/bin/python $S/e2e.py cmp $S/$tag | tail -3
