#!/bin/zsh
# K48 part 2 driver: chain_flat.sh IMPL BATCHSIZE W... ; each batch of BATCHSIZE triples is one heavy.sh job (nice 15, 2-slot lock).
cd "$(dirname $0)/.."
impl=$1; bs=$2; shift 2
for W in "$@"; do
  ts=($(cat in/triples_flat$W.txt)); todo=()
  for t in $ts; do [[ -f logs/flat/${impl}_flat${W}x6_f${t//,/_}.done ]] || todo+=($t); done
  while (( ${#todo} > 0 )); do
    b=(${todo[1,$bs]}); todo=(${todo[$((bs+1)),-1]})
    echo "$$ batch $impl W=$W ${b[*]} $(date +%H:%M:%S)" >> pids.log
    ../../heavy.sh scripts/batch_flat.sh $impl $W $b
    sleep 20
  done
done
echo done > logs/chain_flat_$impl.done
