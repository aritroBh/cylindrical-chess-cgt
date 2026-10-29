#!/bin/zsh
# usage: run_sweep.sh "<W H F wmax bmax>" ... ; runs grp census (strict) and (ignore-leak) for each config; output in runs/
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15
for cfg in "$@"; do
  set -- ${=cfg}; W=$1; H=$2; F=$3; wm=$4; bm=$5
  t=c${W}x${H}_f${F}_${wm}${bm}
  nice -n 15 ./grp --W $W --H $H --F $F --wmax $wm --bmax $bm --out runs/$t > runs/$t.json 2> runs/$t.err
  nice -n 15 ./grp --W $W --H $H --F $F --wmax $wm --bmax $bm --ignore-leak --out runs/${t}_il > runs/${t}_il.json 2> runs/${t}_il.err
  echo done $t
done
