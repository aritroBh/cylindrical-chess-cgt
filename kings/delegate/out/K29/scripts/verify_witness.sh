#!/bin/zsh
# verify_witness.sh NAME BOARD ZS H : re-solve the first failing context of every group of data/screen_NAME.txt with two
# independent implementations (kp_p --pmodel and ref3 for P; kpsolve --frozen and ref3 --frozen for the parked-king value).
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29
cd $D
N=$1; B=$2; ZS=$3; H=$4
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
RB=${B/:/}      # cyl:7x6 -> cyl7x6 ; ref3 wants cyl:7x6 or flat7x6 as in the brief
case $B in flat*) RB=flat${B#flat:};; *) RB=$B;; esac
$PY scripts/witness.py gen $N $ZS $H
nice -n 15 ./bin/kpp --board $B --pmodel --ep on --promote Q < data/wit_$N.pos  > data/wit_$N.Pkp  2>/dev/null
nice -n 15 ./bin/ref3 --board $RB < data/wit_$N.pos > data/wit_$N.Pref 2>/dev/null
nice -n 15 ./bin/kp --board $B --frozen --ep on --promote Q < data/wit_$N.ppos > data/wit_$N.Fkp 2>/dev/null
nice -n 15 ./bin/ref3 --board $RB --frozen < data/wit_$N.ppos > data/wit_$N.Fref 2>/dev/null
$PY scripts/witness.py cmp $N | tee logs/witness_$N.txt
