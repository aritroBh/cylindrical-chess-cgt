#!/bin/bash
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15
for il in 0 1; do for pa in 0 1; do
 fl=(); [ $il = 1 ] && fl+=(--ignore-leak); [ $pa = 1 ] && fl+=(--allow-passer)
 ./v2/grp15 --W 5 --H 5 --F 3 --wmax 2 --bmax 2 "${fl[@]}" --census --dumproots v2/chk/g_5x5_il${il}_pa${pa}.tsv --out v2/chk/g5 > v2/chk/g5.json 2>/dev/null
 sort v2/chk/g_5x5_il${il}_pa${pa}.tsv > v2/chk/a.s; sort v2/chk/p_5x5_il${il}_pa${pa}.tsv > v2/chk/b.s
 echo "il=$il pa=$pa roots=$(wc -l < v2/chk/a.s) difflines=$(diff v2/chk/a.s v2/chk/b.s | wc -l) classes: $(cut -f2 v2/chk/a.s | sort | uniq -c | tr '\n' ' ')"
done; done
