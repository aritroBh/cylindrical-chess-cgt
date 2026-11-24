#!/bin/zsh
# K59 part 2 step 2: exhaustive Definition 4.8 search on flat 8x7 (ranks 2..6, <= 3 + 3 pawns, every king placement) in
# the file classes of the known shape {f, f+1, f+4} up to left-right reflection: 0,1,4  0,3,4  1,2,5  1,4,5.
# usage: run_search.sh A|R    A = p45a (both orientations), R = r48 (under orientation); each run under the RSS watchdog.
cd "$(dirname $0)/.."
impl=$1; mkdir -p logs/search
for t in 0,1,4 0,3,4 1,2,5 1,4,5; do
  tag=${impl}_flat8x7_f${t//,/_}
  [[ -f logs/search/$tag.done ]] && continue
  if [[ $impl == A ]]; then
    ../../heavy.sh /usr/bin/time -l bin/p45a --kind flat --W 8 --H 7 --files $t --nw 3 --nb 3 --mode both > logs/search/$tag.out 2> logs/search/$tag.err &
  else
    ../../heavy.sh /usr/bin/time -l bin/r48 enum pln:8x7 $t 3 3 > logs/search/$tag.out 2> logs/search/$tag.err &
  fi
  P=$!; echo "$P heavy.sh search $tag $(date +%H:%M:%S)" >> pids.log
  src/watch.sh $P $tag &
  Wd=$!; echo "$Wd watch.sh $tag" >> pids.log
  wait $P; rc=$?; wait $Wd
  echo "rc=$rc $(date +%H:%M:%S)" > logs/search/$tag.done
done
