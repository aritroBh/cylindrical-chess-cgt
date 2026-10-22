#!/bin/bash
# (env WHOLE=1: cylcgt in the whole-board model, output conn/whole_*)
# run_conn.sh WIDTH P NW LO HI : scanner (fixed2, default setting) on flat WIDTH/P/NW, piped into cmp_cylcgt.py connected_range LO HI
# (cylcgt value of every connected root with connected-index in [LO,HI) vs the scanner's outcome and nimber).  Output conn/w{W}p{P}_{NW}_{LO}_{HI}.out
cd "$(dirname "$0")"; W=$1; P=$2; NW=$3; LO=$4; HI=$5; NB=$((P-NW))
O=conn/${WHOLE:+whole_}w${W}p${P}_${NW}_${LO}_${HI}.out
nice -n 15 ./scan_fixed2 --flat --width $W --min $P --max $P --nw $NW --nb $NB --only-setting 2 --max-entries 67108864 2>/dev/null \
 | PYTHONPATH=../.. nice -n 15 ../../.venv/bin/python cmp_cylcgt.py connected_range $LO $HI > $O 2> $O.err
echo "done $O: $(head -1 $O)"
