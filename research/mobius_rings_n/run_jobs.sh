#!/bin/sh
# usage: run_jobs.sh BIN jobsfile tag   (one worker; jobs lines: n P K [TBITS]). BIN e.g. bin/mob1_12
cd "$(dirname "$0")"
bin=$1; jobs=$2; tag=$3; prog=$(basename $bin | cut -d_ -f1)
echo $$ > logs/worker_$tag.pid
while read n p k tb; do
  case "$n" in \#*|"") continue;; esac
  i=0
  while [ $i -lt $k ]; do
    base=results/n${n}_p${p}_c${i}of${k}
    if [ ! -f $base.$prog.done ]; then
      [ -n "$tb" ] && export TBITS=$tb
      /usr/bin/time -p nice -n 15 ./$bin scan $n $p --chunk $i $k --out $base.$prog.sig > $base.$prog.out 2> logs/tmp_$tag.err
      zstd -q -9 -f --rm $base.$prog.sig
      zstd -t -q $base.$prog.sig.zst && cp logs/tmp_$tag.err $base.$prog.time && touch $base.$prog.done
      echo "$(date +%T) $prog n=$n P=$p chunk $i/$k done" >> logs/progress_$tag.log
    fi
    i=$((i+1))
  done
done < $jobs
rm -f logs/worker_$tag.pid
