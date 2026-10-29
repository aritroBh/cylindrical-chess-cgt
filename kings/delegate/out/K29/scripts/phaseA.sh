#!/bin/zsh
# phaseA.sh NAME [CTXHI]: Phase A screen of configuration NAME (a line of scripts/configs.txt): every symmetry-class
# representative (data/rep_*.txt) against the first CTXHI (default 300) contexts in grp2's sorted order, stopping at the first
# failing context of each group.  One heavy.sh call.  Output data/A_NAME.txt (R lines), time/RSS in logs/A_NAME.err.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29
cd $D
NAME=$1; HI=${2:-300}
[[ -s data/A_${NAME}.txt ]] && exit 0
line=$(grep -v '^#' scripts/configs.txt | awk -v n=$NAME '$1==n')
set -- ${=line}
board=$2 zs=$3 fz=$4 dmin=$5 rep=$6
/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh /usr/bin/time -l ./bin/grp2 --board $board --mode test --zs $zs --fz $fz --dmin $dmin --cw 2 --cb 2 --first 1 --ctxlo 0 --ctxhi $HI < data/rep_${rep}.txt > data/A_${NAME}.tmp 2> logs/A_${NAME}.err
mv data/A_${NAME}.tmp data/A_${NAME}.txt
echo "A $NAME done $(date +%H:%M)" >> logs/progress.txt
