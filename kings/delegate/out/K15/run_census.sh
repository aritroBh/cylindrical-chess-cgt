#!/bin/zsh
# usage: run_census.sh W H F wmax bmax [heavy]   -> runs/<tag>.json (4 variants: strict, strict_il, passer, passer_il)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15
W=$1;H=$2;F=$3;wm=$4;bm=$5; t=cen_${W}x${H}_f${F}_${wm}${bm}
if [[ "$6" == heavy ]]; then pre=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh; else pre="nice -n 15"; fi
$=pre ./grp --W $W --H $H --F $F --wmax $wm --bmax $bm --variants --out runs/$t > runs/$t.json 2> runs/$t.err
echo "done $t exit=$?" >> runs/census.log
