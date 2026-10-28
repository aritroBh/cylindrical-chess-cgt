#!/bin/bash
cd "$(dirname "$0")"
nice -n 15 python3 solve.py cand_pump_even.tsv res_pump_even.tsv
nice -n 15 python3 solve.py cand_pump_k6to12.tsv res_pump_k6to12.tsv
echo ALLDONE > pump.done
