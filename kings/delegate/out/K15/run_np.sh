#!/bin/zsh
# usage: run_np.sh [--flat] W H F wmax bmax  -> real-P (--nopass) census, strict + passer variants, through the shared lock
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15
fl=""; if [[ "$1" == "--flat" ]]; then fl="--flat"; shift; fi
W=$1;H=$2;F=$3;wm=$4;bm=$5; t=np_${fl#--}${fl:+_}${W}x${H}_f${F}_${wm}${bm}
/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh ./grp --nopass $=fl --W $W --H $H --F $F --wmax $wm --bmax $bm --sp-variants --out runs/$t > runs/$t.json 2> runs/$t.err
echo "done $t exit=$?" >> runs/census.log
