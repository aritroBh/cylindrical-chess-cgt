#!/bin/zsh
# wsym_run.sh NAME BOARD ZS FZ RESFILE REPSUFFIX NSAMPLE : verify NSAMPLE random non-representative class members of the failing classes
# (witness mapped by the symmetry) with kp_p/ref3 (P) and kpsolve/ref3 --frozen (parked kings).  One heavy.sh call.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29
cd $D
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
N=$1; B=$2; ZS=$3; FZ=$4; RES=$5; REP=$6; NS=$7
case $B in flat*) RB=flat${B#flat:};; *) RB=$B;; esac
$PY scripts/witsym.py gen ws_$N $B $ZS $FZ data/$RES $NS 20261029 data/classes_$REP.txt
nice -n 15 ./bin/kpp --board $B --pmodel --ep on --promote Q < data/wsym_ws_$N.pos > data/wsym_ws_$N.Pkp 2>/dev/null
nice -n 15 ./bin/ref3 --board $RB < data/wsym_ws_$N.pos > data/wsym_ws_$N.Pref 2>/dev/null
nice -n 15 ./bin/kp --board $B --frozen --ep on --promote Q < data/wsym_ws_$N.ppos > data/wsym_ws_$N.Fkp 2>/dev/null
nice -n 15 ./bin/ref3 --board $RB --frozen < data/wsym_ws_$N.ppos > data/wsym_ws_$N.Fref 2>/dev/null
$PY scripts/witsym.py cmp ws_$N | tee logs/wsym_$N.txt
