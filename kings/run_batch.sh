#!/bin/sh
# A8 experiment batch (run from the project root): every board, e.p. on and off,
# queen promotion with cap 2; an underpromotion check on the smallest boards; the
# 4-man Lichess cross-check at cap 2. Each run writes kings/results/.
set -e
cc -O2 -Wall -Wextra -o kings/kpsolve kings/kpsolve.c
S=kings/results
run() { echo "== $*"; python3 kings/experiment.py "$@" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['board'], d['ep'], d['promote'], 'cap', d['cap'], 'Z ok' if d['trebuchet_is_mutual_zugzwang'] else 'Z NOT ZUGZWANG', d['counts'], d['seconds'], 's')"; }
for ep in on off; do
  run --board cyl:6x6 --promote Q --cap 2 --ep $ep
  run --board flat:5x6 --promote Q --cap 2 --ep $ep
  run --board cyl:7x6 --promote Q --cap 2 --ep $ep
  run --board flat:6x6 --promote Q --cap 2 --ep $ep
done
# underpromotion: does allowing R, B, N change any result on the smallest boards?
run --board cyl:6x6 --promote QRBN --cap 2 --ep on
run --board flat:5x6 --promote QRBN --cap 2 --ep on
# Lichess 4-man check with two promoted pieces allowed
echo "== lichess cap 2"
python3 kings/lichess_check.py --max-men 4 --cap 2 || true
