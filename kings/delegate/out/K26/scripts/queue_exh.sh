#!/bin/zsh
# K26 final: exhaustive <= 3-pawn contexts (ctx_exh.py) for Z_C and Z_B, plus the context detail run (ctxtest2.py) for Z_C.  One heavy.sh call per shard.  PID in logs/queue_exh.pid.
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
echo $$ > $D/logs/queue_exh.pid
for job in "ZC cyl:8x6 efg 3 12" "ZB cyl:8x6 efg 3 12" "ZB cyl:7x6 ef 3 4" "ZB flat:7x6 efg 3 12"; do
  set -- ${=job}
  g=$1; b=$2; f=$3; m=$4; n=$5
  for ((i=0;i<n;i++)); do
    tag=${g}_${b/:/_}_${f}_m${m}_s${i}of${n}
    [[ -f $D/logs/exh/$tag.json ]] && continue
    echo "start $tag $(date +%T)" >> $D/logs/exh/queue.log
    $H $PY $D/scripts/ctx_exh.py $g $b $f $m $i/$n $D/logs/exh/$tag.json > $D/logs/exh/$tag.log 2>&1
    echo "end   $tag $(date +%T) rc=$?" >> $D/logs/exh/queue.log
  done
done
# context detail for Z_C (same sample as the earlier ctx_phase2 / ctx_cyl8_ef runs, seed 1)
python3 - <<'PY'
import json
g = json.load(open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/logs/groups_final.json'))
x = [a for a in g if a['id'] == 'dud_cyl8x6_a2c4-a3c5_c2c3']
json.dump(x, open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/logs/exh/g_zc.json', 'w'))
PY
for f in fg ef; do
  [[ -f $D/logs/exh/detail_zc_$f.json ]] && continue
  echo "start detail_zc_$f $(date +%T)" >> $D/logs/exh/queue.log
  $H $PY $D/scripts/ctxtest2.py $D/logs/exh/g_zc.json $D/logs/exh/detail_zc_$f.json --nbase 60 --nflip 6 --ncheck 12 --files $f > $D/logs/exh/detail_zc_$f.log 2>&1
  echo "end   detail_zc_$f $(date +%T) rc=$?" >> $D/logs/exh/queue.log
done
echo "QUEUE DONE $(date +%T)" >> $D/logs/exh/queue.log
