#!/bin/bash
# run_conn_sample.sh WIDTH P NW MOD : scanner | cmp_cylcgt.py connected MOD  (hash sample crc32(position)%MOD==0 of the connected rows)
cd "$(dirname "$0")"; W=$1; P=$2; NW=$3; MOD=$4; NB=$((P-NW))
O=conn/sample_w${W}p${P}_${NW}_mod${MOD}.out
nice -n 15 ./scan_fixed2 --flat --width $W --min $P --max $P --nw $NW --nb $NB --only-setting 2 --max-entries 67108864 2>/dev/null \
 | PYTHONPATH=../.. nice -n 15 ../../.venv/bin/python cmp_cylcgt.py connected $MOD > $O 2> $O.err
echo "done $O: $(head -1 $O)"
