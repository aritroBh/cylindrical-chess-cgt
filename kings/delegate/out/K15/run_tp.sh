#!/bin/zsh
# usage: run_tp.sh [--flat] W H F wmax bmax  -> tempo-signature census (strict + passer variants) through the shared lock
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15
fl=""; if [[ "$1" == "--flat" ]]; then fl="--flat"; shift; fi
W=$1;H=$2;F=$3;wm=$4;bm=$5; t=tp_${fl#--}${fl:+_}${W}x${H}_f${F}_${wm}${bm}
/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh ./grp_t --tempo $=fl --W $W --H $H --F $F --wmax $wm --bmax $bm --out runs/$t > runs/$t.json 2> runs/$t.err
echo "done $t exit=$?" >> runs/census.log
