#!/bin/zsh
# bundle_ex.sh BOARD MAXW MAXB NSHARDS FIRST LAST TAG [chk args...]   -- run inside ONE heavy.sh acquisition
# EXHAUSTIVE sweep of shards FIRST..LAST (beta = White; cylinder: beta's king on file a) with the strategy simulation.
# Every certified instance is simulated (Pi = 'beta pushes p' against all omega lines); positions in which some line fails
# (omega stalemated) are collected and solved once by kp_p.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16
board=$1; mw=$2; mb=$3; ns=$4; first=$5; last=$6; tag=$7; shift 7
mkdir -p $D/work/$tag $D/logs
b=$D/work/$tag/all
: > $b.pos; : > $b.meta; : > $b.tally
for ((i=first; i<=last; i++)); do
  $D/work/chk3 --board $board --mode enum --maxw $mw --maxb $mb --shard $i/$ns --onlystale --out $b.$i "$@" >> $b.tally 2> $b.chk
  cat $b.$i.pos >> $b.pos; cat $b.$i.meta >> $b.meta; rm -f $b.$i.pos $b.$i.meta
done
n=$(wc -l < $b.pos)
if [[ $n -gt 0 ]]; then
  /usr/bin/time -l $D/work/kpp --board $board --pmodel < $b.pos > $b.res 2> $b.err
  rss=$(grep "maximum resident" $b.err | awk '{print $1}')
  s=$(/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python $D/scripts/cmp.py $b.pos $b.meta $b.res $b.viol)
else
  s='{"positions": 0, "violating_positions": 0, "viol_results": {}, "variants[instances,violations]": {"orig": [0, 0], "S0": [0, 0], "S1": [0, 0], "S2": [0, 0], "S1S2": [0, 0], "S3": [0, 0]}, "gap": 0, "S2_but_stalemate": 0}'
  rss=0
fi
tal=$(/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python -c "
import json,sys,collections
t=collections.Counter()
for l in open('$b.tally'):
    for k,v in json.loads(l).items(): t[k]+=v
print(json.dumps(t))")
echo "{\"tag\":\"$tag\",\"board\":\"$board\",\"shard\":\"$first-$last\",\"of\":$ns,\"nshards\":$((last-first+1)),\"tally\":$tal,\"summary\":$s,\"rss\":${rss:-0}}" >> $D/logs/EX_$tag.jsonl
[[ -s $b.viol ]] && cat $b.viol >> $D/logs/viol_EX_$tag.txt
rm -rf $D/work/$tag
