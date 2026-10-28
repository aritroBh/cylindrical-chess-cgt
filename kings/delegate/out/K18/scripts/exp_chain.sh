#!/bin/zsh
# usage: exp_chain.sh OUTDIR BOARD i j ...   : kpp P-model on the context inputs of sorties i j ... (one heavy slot, sequential)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18
D=$1; B=$2; shift 2
for i in "$@"; do
  /usr/bin/time -p nice -n 15 bin/kpp --board $B --ep on --pmodel --promote Q --cap 0 --threads 2 < $D/in_$i.txt > $D/out_$i.txt 2> $D/err_$i.txt
done
