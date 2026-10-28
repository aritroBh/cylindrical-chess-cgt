#!/bin/zsh
# cap1_each.sh INFILE OUTFILE : run kpsolve (chess, cap 1) on each position of INFILE as its own single-thread process,
# nice 15, CPU limit 58 s per process (each run is under one CPU-minute, so it needs no heavy.sh slot); appends
# "<pos> | A B # user-seconds maxRSS-bytes" to OUTFILE.
in=$1; out=$2
while IFS= read -r pos; do
  [[ -z $pos ]] && continue
  tmp=$(mktemp)
  r=$( (ulimit -t 58; echo "$pos" | nice -n 15 /usr/bin/time -l ./kp --board flat:7x6 --cap 1 2> $tmp) )
  u=$(grep -E "user" $tmp | awk '{print $3}'); m=$(grep "maximum resident" $tmp | awk '{print $1}')
  if [[ -z $r ]]; then r="$pos | TIMEOUT"; fi
  echo "$r # user=${u}s rss=${m}" >> $out
  rm -f $tmp
done < $in
