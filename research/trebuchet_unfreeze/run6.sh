#!/bin/zsh
# usage: run6.sh tag input_file kpv-args...   (one heavy process; records its PID)
cd /Users/aritro/Downloads/Research/Chessendgames/research/trebuchet_unfreeze
tag=$1; inp=$2; shift 2
echo $$ > logs/run6_$tag.pid
nice -n 15 /usr/bin/time -l src/kpv --board cyl:6x6 "$@" --moves < $inp > logs/s6_$tag.txt 2> logs/s6_$tag.err
