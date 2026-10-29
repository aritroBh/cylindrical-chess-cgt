#!/bin/zsh
# verify_one.sh KPBOARD REFBOARD ZS "Z tokens" CFILES CW CB TAG [PARKW PARKB]
# For one group Z and every context on CFILES (<= CW white, <= CB black pawns, ranks 2-5, e.p. '-', both sides to move):
#   Phi = P value of Z + H   (kp_p --pmodel and ref3, position by position)
#   Psi = frozen value of H with parked kings (kpsolve --frozen and ref3 --frozen)
# prints counts and the contexts with Phi != Psi.  Writes data/ver_TAG.* ; run it through heavy.sh.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29
cd $D
KB=$1; RB=$2; Z=$4; CF=$5; CW=$6; CB=$7; TAG=$8; PW=${9:-a1}; PB=${10:-a6}
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
$PY scripts/gen_ctx.py "$Z" $CF $CW $CB 2-5 > data/ver_$TAG.pos 2>/dev/null
$PY scripts/gen_ctx.py "K$PW k$PB" $CF $CW $CB 2-5 > data/ver_$TAG.ppos 2>/dev/null
nice -n 15 ./bin/kpp --board $KB --pmodel --ep on --promote Q < data/ver_$TAG.pos > data/ver_$TAG.Pkp 2>/dev/null
nice -n 15 ./bin/ref3 --board $RB < data/ver_$TAG.pos > data/ver_$TAG.Pref 2>/dev/null
nice -n 15 ./bin/kp --board $KB --frozen --ep on --promote Q < data/ver_$TAG.ppos > data/ver_$TAG.Fkp 2>/dev/null
nice -n 15 ./bin/ref3 --board $RB --frozen < data/ver_$TAG.ppos > data/ver_$TAG.Fref 2>/dev/null
$PY scripts/cmp_ver.py $TAG "$Z"
