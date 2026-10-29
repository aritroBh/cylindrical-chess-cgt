#!/bin/zsh
# agentB/run_depth3.sh : depth3.py (ref3m-based, independent of grp2) on the Phase A survivors of the four f3 configurations with a >=2-file context class,
# and comparison with the exact depths of agentB/sortie_table.py (L <= 2 iff punished within 2 punisher moves).
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29; cd $D
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
: > agentB/depth3_survivors.txt
for x in "cyl7x6_f3 cyl:7x6 0 3" "flat7x6_f3_z0 flat:7x6 0 3" "flat7x6_f3_z2 flat:7x6 2 3" "flat8x6_f3_z2 flat:8x6 2 3"; do set -- ${=x}
  while read z; do echo "[$1] $z" >> agentB/depth3_survivors.txt; nice -n 15 $PY agentB/depth3.py $2 $3 $4 "$z" 2>&1 | grep -E "True|SUMMARY|APPLY|Error" >> agentB/depth3_survivors.txt; done < agentB/surv_$1.txt
done
