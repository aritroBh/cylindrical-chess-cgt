#!/bin/zsh
R=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/verify/r2
cd $R/data; B=cyl:7x6
nice -n 15 $R/bin/kpp --board $B --pmodel --ep on --promote Q < c3_pos > c3.Pkp 2>/dev/null
nice -n 15 $R/bin/ref3 --board $B < c3_pos > c3.Pref 2>/dev/null
nice -n 15 $R/bin/kp --board $B --frozen --ep on --promote Q < c3_ppos > c3.Fkp 2>/dev/null
nice -n 15 $R/bin/ref3 --board $B --frozen < c3_ppos > c3.Fref 2>/dev/null
nice -n 15 $R/bin/ref3 --board $B --frozen < c3_ppos1 > c3.Fref1 2>/dev/null
