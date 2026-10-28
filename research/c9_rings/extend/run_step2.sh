#!/bin/bash
cd "$(dirname "$0")"
for t in C11b_p12 C12_p13 C13_p14; do
  nice -n 15 python3 solve.py cand_$t.tsv res_$t.tsv
done
echo ALLDONE > step2.done
