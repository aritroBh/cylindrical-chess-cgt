#!/bin/sh
# Verifier driver: all atoms + sums under both passed tests (count rule, e.p. on).
# Run from the project root:  sh verify/cylatlas/C3-reproduce/run_all.sh
V=verify/cylatlas/C3-reproduce
EP=/private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt
for impl in main ep; do
  if [ $impl = main ]; then R=.; else R=$EP; fi
  for t in flat:1:2 flat:1:3 flat:1:4 flat:1:5 flat:2:2 flat:2:3 flat:2:4 flat:3:3 flat:3:4 flat:4:4 ring:3:3 ring:3:4 ring:4:4 sums; do
    echo "$R $t 0 1 $V/out_$impl/$(echo $t | tr : _).jsonl"
  done
  for t in flat:2:5 flat:3:5 flat:4:5 flat:5:5 ring:3:5 ring:4:5 ring:5:5; do
    for s in 0 1 2 3; do
      echo "$R $t $s 4 $V/out_$impl/$(echo $t | tr : _)_s$s.jsonl"
    done
  done
done | xargs -P 12 -L 1 sh -c 'test -f "$5" || .venv/bin/python '$V'/values.py --root "$1" --task "$2" --shard "$3" --nshards "$4" --out "$5"' _
echo ALLDONE
