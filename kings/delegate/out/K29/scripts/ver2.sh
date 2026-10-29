#!/bin/zsh
# ver2.sh TAG KPBOARD REFBOARD CTXFILES PW PB "Z tokens" ["Z2 ..."...]   (one heavy.sh call per invocation)
# Verification of survivors over ALL contexts (<= 2 white, <= 2 black pawns on CTXFILES, ranks 2-5, both sides to move, e.p. '-'),
# with kp_p --pmodel (kpp) and ref3 for Phi (P with the group), and kpsolve --frozen (kp) and ref3 --frozen for Psi (kings parked
# on PW, PB).  Psi is computed once per TAG (data/psi_TAG.*), Phi per group (data/ver_TAG_<n>.*).
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29
cd $D
TAG=$1; KB=$2; RB=$3; CF=$4; PW=$5; PB=$6; shift 6
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
if [[ ! -s data/psi_$TAG.ref3 ]]; then
  $PY scripts/gen_ctx.py "K$PW k$PB" $CF 2 2 2-5 > data/psi_$TAG.pos 2>/dev/null
  nice -n 15 ./bin/kp --board $KB --frozen --ep on --promote Q < data/psi_$TAG.pos > data/psi_$TAG.kp 2>/dev/null
  nice -n 15 ./bin/ref3 --board $RB --frozen < data/psi_$TAG.pos > data/psi_$TAG.ref3.tmp 2>/dev/null; mv data/psi_$TAG.ref3.tmp data/psi_$TAG.ref3
fi
n=0
for Z in "$@"; do
  n=$((n+1)); K=${TAG}_$(echo $Z | tr -d ' ')
  [[ -s data/ver_$K.cmp ]] && continue
  $PY scripts/gen_ctx.py "$Z" $CF 2 2 2-5 > data/ver_$K.pos 2>/dev/null
  nice -n 15 ./bin/kpp --board $KB --pmodel --ep on --promote Q < data/ver_$K.pos > data/ver_$K.kpp 2>/dev/null
  nice -n 15 ./bin/ref3 --board $RB < data/ver_$K.pos > data/ver_$K.ref3 2>/dev/null
  $PY scripts/cmp2.py $TAG $K "$Z" > data/ver_$K.cmp
  cat data/ver_$K.cmp
  rm -f data/ver_$K.pos data/ver_$K.kpp data/ver_$K.ref3
done
