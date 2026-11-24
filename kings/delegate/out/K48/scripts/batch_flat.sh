#!/bin/zsh
# K48 part 2, one heavy.sh job = one batch: run_batch IMPL W t1 t2 ... runs each file triple in turn (skipping those done).
# IMPL A = p45a (K45 implementation A, both orientations), R = r48 (K45 referee's r45 + flat option, under orientation).
cd "$(dirname $0)/.."
impl=$1; W=$2; shift 2
for t in "$@"; do
  tag=${impl}_flat${W}x6_f${t//,/_}
  [[ -f logs/flat/$tag.done ]] && continue
  if [[ $impl == A ]]; then bin/p45a --kind flat --W $W --H 6 --files $t --nw 3 --nb 3 --mode both > logs/flat/$tag.out 2> logs/flat/$tag.err
  else bin/r48 enum pln:${W}x6 $t 3 3 > logs/flat/$tag.out 2> logs/flat/$tag.err; fi
  echo "rc=$? $(date +%H:%M:%S)" > logs/flat/$tag.done
done
