#!/bin/zsh
# usage: run.sh <dir> <board> <promote> <cap> <tag> [--frozen]
d=$1; b=$2; p=$3; c=$4; t=$5; shift 5
K=/Users/aritro/Downloads/Research/Chessendgames/kings/kpsolve
/usr/bin/time -l nice -n 15 $K --board $b --ep on --promote $p --cap $c --threads 2 "$@" < $d/positions.txt > $d/out_$t.txt 2> $d/err_$t.txt
echo "exit $?" >> $d/err_$t.txt
