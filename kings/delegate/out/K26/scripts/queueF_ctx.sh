#!/bin/zsh
# K26 attempt 5: fresh context runs with the build in K26/bin. (1) sampled contexts for the 20 selected groups (ctxtest.py, 4 chunks of 5 groups); (2) exhaustive <= 3-pawn contexts for Z_B and Z_C (ctx_exh.py).
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
echo $$ > $D/logs/f/queue_E.pid
for i in 0 1 2 3; do
  [[ -f $D/logs/f/ctx/ctx_final_$i.json ]] && continue
  echo "start ctx_final_$i $(date +%T)" >> $D/logs/f/queue_E.log
  $H $PY $D/scripts/ctxtest.py $D/logs/f/ctx/g_final_$i.json $D/logs/f/ctx/ctx_final_$i.json --nbase 66 --nflip 6 --ncheck 12 --seed 3 > $D/logs/f/ctx/ctx_final_$i.log 2>&1
  echo "end   ctx_final_$i $(date +%T) rc=$?" >> $D/logs/f/queue_E.log
done
for job in "ZB cyl:8x6 efg 3 12" "ZC cyl:8x6 efg 3 12" "ZB cyl:7x6 ef 3 4" "ZB flat:7x6 efg 3 12"; do
  set -- ${=job}
  g=$1; b=$2; f=$3; m=$4; n=$5
  for ((i=0;i<n;i++)); do
    tag=${g}_${b/:/_}_${f}_m${m}_s${i}of${n}
    [[ -f $D/logs/f/exh/$tag.json ]] && continue
    echo "start $tag $(date +%T)" >> $D/logs/f/queue_E.log
    $H $PY $D/scripts/ctx_exh.py $g $b $f $m $i/$n $D/logs/f/exh/$tag.json > $D/logs/f/exh/$tag.log 2>&1
    echo "end   $tag $(date +%T) rc=$?" >> $D/logs/f/queue_E.log
  done
done
echo "QUEUE E DONE $(date +%T)" >> $D/logs/f/queue_E.log
