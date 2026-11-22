#!/bin/sh
# usage: run_scans.sh mob1|mob2 jobsfile      (one worker; jobs lines: n P K)
cd "$(dirname "$0")"
prog=$1; jobs=$2
while read n p k; do
  case "$n" in \#*|"") continue;; esac
  i=0
  while [ $i -lt $k ]; do
    base=results/n${n}_p${p}_c${i}of${k}
    if [ ! -f $base.$prog.done ]; then
      /usr/bin/time -p nice -n 15 ./$prog scan $n $p --chunk $i $k --out $base.$prog.sig > $base.$prog.out 2> logs/scan_$prog.err.tmp
      zstd -q -9 -f --rm $base.$prog.sig
      zstd -t -q $base.$prog.sig.zst && cp logs/scan_$prog.err.tmp $base.$prog.time && touch $base.$prog.done
      echo "$(date +%T) $prog n=$n P=$p chunk $i/$k done" >> logs/progress_$prog.log
    fi
    i=$((i+1))
  done
done < $jobs
