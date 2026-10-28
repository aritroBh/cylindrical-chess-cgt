#!/bin/zsh
# run_ex.sh BOARD MAXW MAXB NSHARDS TAG [chk args...]
# EXHAUSTIVE sweep (beta = White; cylinder: beta's king on file a) with the strategy simulation: for every certified
# instance the simulation decides whether 'beta pushes p' wins against all omega lines.  Only positions in which omega can
# be stalemated in some line (the only way the strategy can fail) go to kp_p, which then decides the true P value.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
board=$1; mw=$2; mb=$3; ns=$4; tag=$5; shift 5
mkdir -p $D/work/$tag $D/logs
for ((i=0; i<ns; i++)); do
  b=$D/work/$tag/x$i
  $H $D/work/chk3 --board $board --mode enum --maxw $mw --maxb $mb --shard $i/$ns --onlystale --out $b "$@" > $b.tally 2> $b.chk
  n=$(wc -l < $b.pos)
  if [[ $n -gt 0 ]]; then
    $H /usr/bin/time -l $D/work/kpp --board $board --pmodel < $b.pos > $b.res 2> $b.err
    rss=$(grep "maximum resident" $b.err | awk '{print $1}')
    s=$(/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python $D/scripts/cmp.py $b.pos $b.meta $b.res $b.viol)
  else
    s='{"positions": 0, "violating_positions": 0, "viol_results": {}, "variants[instances,violations]": {"orig": [0, 0], "S0": [0, 0], "S1": [0, 0], "S2": [0, 0], "S1S2": [0, 0]}, "gap": 0, "S2_but_stalemate": 0}'
    rss=0
  fi
  echo "{\"tag\":\"$tag\",\"board\":\"$board\",\"shard\":$i,\"of\":$ns,\"tally\":$(cat $b.tally),\"summary\":$s,\"rss\":${rss:-0}}" >> $D/logs/EX_$tag.jsonl
  [[ -s $b.viol ]] && sed "s/^/shard $i: /" $b.viol >> $D/logs/viol_EX_$tag.txt
  # keep the stalemate-instance positions with their kp_p results (small) for later study
  [[ $n -gt 0 ]] && paste -d'#' $b.pos $b.res >> /dev/null
  rm -f $b.pos $b.meta $b.res $b.err $b.viol $b.chk $b.tally
done
echo done >> $D/logs/EX_$tag.done
