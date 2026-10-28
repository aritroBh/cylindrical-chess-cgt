#!/bin/zsh
# run_rand.sh BOARD MAXW MAXB STYLE NCHUNKS PER_CHUNK SEED0 TAG [chk extra args...]
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16
board=$1; mw=$2; mb=$3; style=$4; nc=$5; per=$6; seed0=$7; tag=$8; shift 8
mkdir -p $D/work/$tag $D/logs
for ((i=0; i<nc; i++)); do
  b=$D/work/$tag/r$i
  $D/work/chk --board $board --mode rand --maxw $mw --maxb $mb --style $style --n $per --seed $((seed0+i)) --out $b "$@" 2> $b.chk
  [[ -s $b.pos ]] || { rm -f $b.*; continue; }
  /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh /usr/bin/time -l $D/work/kpp --board $board --pmodel < $b.pos > $b.res 2> $b.err
  rss=$(grep "maximum resident" $b.err | awk '{print $1}')
  s=$(/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python $D/scripts/cmp.py $b.pos $b.meta $b.res $b.viol)
  echo "{\"tag\":\"$tag\",\"board\":\"$board\",\"seed\":$((seed0+i)),\"summary\":$s,\"rss\":${rss:-0},\"chk\":\"$(tail -1 $b.chk)\"}" >> $D/logs/$tag.jsonl
  [[ -s $b.viol ]] && sed "s/^/seed $((seed0+i)): /" $b.viol >> $D/logs/viol_$tag.txt
  rm -f $b.pos $b.meta $b.res $b.err $b.viol $b.chk
done
echo done >> $D/logs/$tag.done
