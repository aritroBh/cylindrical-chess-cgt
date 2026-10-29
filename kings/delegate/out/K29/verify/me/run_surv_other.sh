#!/bin/zsh
# referee K29 pass 2: survivor checks on other boards, one heavy.sh call per (board, group)
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/verify
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
cd $D
run() { # tag kb rb files pw pb Z
  $H $PY scripts/surv.py $2 $3 $4 $5 $6 "$7" > logs/me_surv_$1.txt 2>&1
}
run cyl8x6_eg_1 cyl:8x6 cyl:8x6 eg a1 a6 "Kb3 Pa2 Pc2 kb1 pa3 pc3"
run flat7x6_z2_ag_1 flat:7x6 flat7x6 ag c1 c6 "Kd3 Pc2 Pe2 kd1 pc3 pe3"
run cyl8x6_eg_2 cyl:8x6 cyl:8x6 eg a1 a6 "Kb1 Pa2 Pb3 ka3 pb2 pc5"
run flat7x6_z2_ag_2 flat:7x6 flat7x6 ag c1 c6 "Kd1 Pc2 Pd3 kc3 pd2 pe5"
run flat7x6_ef_1 flat:7x6 flat7x6 ef a1 a6 "Kb3 Pa2 Pc2 kb1 pa3 pc3"
echo done > logs/me_surv_other.done
