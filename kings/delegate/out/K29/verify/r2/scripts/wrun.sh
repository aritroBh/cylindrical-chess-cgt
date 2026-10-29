#!/bin/zsh
# wrun.sh FN : solve data/ws_FN.{pos,ppos,ppos1} with kp_p, ref3, kp --frozen, ref3 --frozen (one heavy.sh call; FN like cyl7x6 / flat7x6)
R=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/verify/r2
FN=$1; B=$(cat $R/data/ws_$FN.board); RB=${B/:/}; case $B in flat*) RB=flat${B#flat:};; *) RB=$B;; esac
cd $R/data
nice -n 15 $R/bin/kpp --board $B --pmodel --ep on --promote Q < ws_$FN.pos > ws_$FN.Pkp 2>/dev/null
nice -n 15 $R/bin/ref3 --board $RB < ws_$FN.pos > ws_$FN.Pref 2>/dev/null
nice -n 15 $R/bin/kp --board $B --frozen --ep on --promote Q < ws_$FN.ppos > ws_$FN.Fkp 2>/dev/null
nice -n 15 $R/bin/ref3 --board $RB --frozen < ws_$FN.ppos > ws_$FN.Fref 2>/dev/null
nice -n 15 $R/bin/ref3 --board $RB --frozen < ws_$FN.ppos1 > ws_$FN.Fref1 2>/dev/null
