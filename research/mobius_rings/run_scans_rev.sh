#!/bin/sh
# usage: run_scans_rev.sh prog n P K  -- same as run_scans.sh for one job but chunks K-1, K-2, ...; stops at the first
# chunk that already has an output file (started by the forward driver).
cd "$(dirname "$0")" || exit 1
prog=$1; n=$2; p=$3; k=$4
i=$((k-1))
while [ $i -ge 0 ]; do
  base=results/n${n}_p${p}_c${i}of${k}
  [ -e $base.$prog.out ] && { echo "stop at chunk $i"; exit 0; }
  /usr/bin/time -p nice -n 15 ./$prog scan $n $p --chunk $i $k --out $base.$prog.sig > $base.$prog.out 2> logs/scan_${prog}_rev.err.tmp
  zstd -q -9 -f --rm $base.$prog.sig
  zstd -t -q $base.$prog.sig.zst && cp logs/scan_${prog}_rev.err.tmp $base.$prog.time && touch $base.$prog.done
  echo "$(date +%T) $prog n=$n P=$p chunk $i/$k done (reverse driver)" >> logs/progress_$prog.log
  i=$((i-1))
done
