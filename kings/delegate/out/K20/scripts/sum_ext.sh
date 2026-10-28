#!/bin/zsh
# usage: sum_ext.sh logs/ext_X.log : totals of the extended-battery and additivity checks
f=$1
grep -h "EXT" $f | sed -E 's/EXT [0-9]+ contexts://' | tr ';' '\n' | sed 's/^ *//' | awk 'NF{a=$0; sub(/ agree.*/,"",a); n=$0; match(n,/agree=[0-9]+/); ag=substr(n,RSTART+6,RLENGTH-6); match(n,/disagree=[0-9]+/); dg=substr(n,RSTART+9,RLENGTH-9); A[a]+=ag; Dg[a]+=dg} END{for(k in A) print "EXT", k, "agree", A[k], "disagree", Dg[k]}' | sort
grep -h PAIRS $f | awk '{c+=$3; m+=$5} END{print "PAIRS checked", c, "mismatches", m}'
