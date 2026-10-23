#!/bin/bash
# source this: scan DIR KIND WIDTH NW NB NCHUNKS [extra flags]
H=${H:-./h4}
scan() {
  local dir=$1 kind=$2 w=$3 nw=$4 nb=$5 n=$6; shift 6
  mkdir -p out/$dir
  for ((i=0;i<n;i++)); do
    local f=out/$dir/${nw}_${nb}_c${i}of${n}
    [ -f $f.done ] && continue
    nice -n 15 $H --$kind --width $w --single --nw $nw --nb $nb "$@" --chunk $i $n --max-entries 33554432 --scan-mex > $f.tsv 2> $f.err && touch $f.done
  done
}
