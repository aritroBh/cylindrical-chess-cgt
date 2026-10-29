#!/bin/zsh
# usage: dud_filter.sh W F  : tempo-signature of every real-P structural dud candidate found for cyl:Wx6 with F files
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15
W=$1; F=$2
cat runs/np_${W}x6_f${F}_*_strict_cands.txt runs/np_${W}x6_f${F}_*_passer_cands.txt | awk -F'\t' '$1=="dud"{print $2}' | sort -u > runs/dudcands_${W}x6_f${F}.txt
for s in strict passer; do cat runs/np_${W}x6_f${F}_*_${s}_cands.txt | awk -F'\t' '$1=="dud"{print $2}' | sort -u > runs/dudcands_${W}x6_f${F}_$s.txt; done
list=$(paste -sd';' runs/dudcands_${W}x6_f${F}.txt)
nice -n 15 ./grp_t --tempo --reach --W $W --H 6 --F $F --classify "$list" 2>/dev/null | grep "|" | sed 's/ | sig /\t/; s/  | class /\t/' > runs/dudsig_${W}x6_f${F}.tsv
