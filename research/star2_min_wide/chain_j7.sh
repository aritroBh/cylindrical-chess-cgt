#!/bin/bash
# variant-R scanner rows (gapped) vs whole-board cylcgt (hash samples)
cd "$(dirname "$0")"
run() { W=$1; P=$2; NW=$3; M=$4; O=rsample/w${W}p${P}_${NW}_mod${M}.out
  nice -n 15 ./scan_R --flat --width $W --min $P --max $P --nw $NW --nb $((P-NW)) --only-setting 2 2>/dev/null \
   | PYTHONPATH=../.. nice -n 15 ../../.venv/bin/python sample_gapped_R.py $M > $O 2> $O.err; echo "$O: $(head -1 $O)"; }
run 5 6 3 100; run 5 6 2 50; run 6 6 3 200; run 8 6 2 100; run 8 6 3 300; run 5 7 3 5000; run 6 7 2 3000; run 8 7 3 20000
