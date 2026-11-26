#!/bin/zsh
# K65 referee: compare ax65's (B1) and Aux values with pk_sum's, move by move (same move order: ax65 wrote the inputs).
cd "$(dirname $0)/.."
for g in "$@"; do
  for kind in B1 aux; do
    f=logs/pk/${kind}_$g.out; [[ -f $f ]] || continue
    if [[ $kind == B1 ]]; then a=$(grep '^B1 ' logs/g/$g.out | sed 's/.*beside -1 not a White win.*/N/;s/.*beside -1 WHITE WIN.*/W/' | tr -d '\n')
    else a=$(grep '^AUX ' logs/g/$g.out | sed 's/.*does NOT win.*/N/;s/.*WINS.*/W/' | tr -d '\n'); fi
    p=$(awk '{print ($(NF-2)=="W")?"W":"N"}' $f | tr -d '\n')
    echo "$g $kind ax65=$a pk_sum=$p $([[ $a == $p ]] && echo agree || echo DISAGREE)"
  done
done
