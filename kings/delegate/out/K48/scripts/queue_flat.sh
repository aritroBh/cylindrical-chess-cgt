#!/bin/zsh
# K48 part 2: Definition 4.8 search on flat Wx6, every file triple within a six-file span (one per reflection class), <= 3 + 3 pawns,
# every king placement.  Usage: queue_flat.sh A|R W...   A = K45's p45a (K43 table solver; both orientations), R = r48 (K45 referee's r45 + flat option;
# under orientation; over = colour mirror, same domain).  Logs: logs/flat/{A,R}_flatWx6_f*.{out,err,done}.
cd "$(dirname $0)/.."
impl=$1; shift
for W in "$@"; do
  for t in $(cat in/triples_flat$W.txt); do
    tag=${impl}_flat${W}x6_f${t//,/_}
    [[ -f logs/flat/$tag.done ]] && continue
    echo "$$ $tag $(date +%H:%M:%S)" >> pids.log
    if [[ $impl == A ]]; then
      ../../heavy.sh bin/p45a --kind flat --W $W --H 6 --files $t --nw 3 --nb 3 --mode both > logs/flat/$tag.out 2> logs/flat/$tag.err
    else
      ../../heavy.sh bin/r48 enum pln:${W}x6 $t 3 3 > logs/flat/$tag.out 2> logs/flat/$tag.err
    fi
    echo "rc=$? $(date +%H:%M:%S)" > logs/flat/$tag.done
    sleep 20   # let other queued heavy.sh jobs take the freed slot
  done
done
echo done > logs/queue_flat_${impl}_$1.done
