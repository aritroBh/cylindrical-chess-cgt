#!/bin/zsh
# K43 extensions (plocal43p3, packed 2-bit table): wait for run_main.sh, then more pawns / more ranks / diagnostics, most valuable first.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K43
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
cd $D
while [[ ! -f logs/main.done ]]; do sleep 30; done
# kind W H F off nw nb tagsuffix
for job in "cyl 8 6 3 0 4 4" "cyl 8 6 4 0 3 3 diag" "cyl 8 7 3 0 3 3" "cyl 7 6 3 0 4 4" "cyl 8 8 3 0 3 3" "cyl 8 6 4 0 4 2" \
           "flat 7 6 3 0 4 4" "flat 7 6 3 1 4 4" "flat 7 6 4 1 3 3 diag" "cyl 7 7 3 0 3 3" "cyl 6 6 3 0 4 4" "cyl 9 6 3 0 4 4" "flat 7 6 3 2 4 4" \
           "cyl 7 6 4 0 4 2" "flat 7 6 4 0 4 2" "flat 7 6 4 1 4 2" "cyl 8 6 5 0 3 3" "cyl 7 6 5 0 3 3"; do
  set -- ${=job}
  tag=${1}${2}x${3}_F$4_off$5_$6$7${8:+_$8}
  [[ -f logs/$tag.done ]] && continue
  $H ./bin/plocal43p3 --kind $1 --W $2 --H $3 --F $4 --off $5 --nw $6 --nb $7 --mode both > logs/$tag.out 2> logs/$tag.err
  echo "rc=$?" > logs/$tag.done
done
echo ALLDONE > logs/ext.done
