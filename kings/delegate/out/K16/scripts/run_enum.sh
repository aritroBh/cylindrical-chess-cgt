#!/bin/zsh
# run_enum.sh BOARD MAXW MAXB NSHARDS FIRST LAST TAG [chk extra args...]
# exhaustive enumeration (beta = White, cylinder: beta's king on file a), shard by shard:
# chk -> kp_p (--pmodel, via the shared heavy lock) -> cmp.py; bulk files are deleted after each shard.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16
board=$1; mw=$2; mb=$3; ns=$4; first=$5; last=$6; tag=$7; shift 7
mkdir -p $D/work/$tag $D/logs
for ((i=first; i<=last; i++)); do
  b=$D/work/$tag/s$i
  $D/work/chk --board $board --mode enum --maxw $mw --maxb $mb --shard $i/$ns --out $b "$@" 2> $b.chk
  [[ -s $b.pos ]] || { rm -f $b.*; continue; }
  /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh /usr/bin/time -l $D/work/kpp --board $board --pmodel < $b.pos > $b.res 2> $b.err
  rss=$(grep "maximum resident" $b.err | awk '{print $1}')
  s=$(/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python $D/scripts/cmp.py $b.pos $b.meta $b.res $b.viol)
  echo "{\"tag\":\"$tag\",\"board\":\"$board\",\"shard\":$i,\"of\":$ns,\"summary\":$s,\"rss\":${rss:-0},\"chk\":\"$(tail -1 $b.chk)\"}" >> $D/logs/$tag.jsonl
  [[ -s $b.viol ]] && sed "s/^/shard $i: /" $b.viol >> $D/logs/viol_$tag.txt
  rm -f $b.pos $b.meta $b.res $b.err $b.viol $b.chk
done
echo done >> $D/logs/$tag.done
