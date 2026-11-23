#!/bin/zsh
# K43: 4-file windows, <= 3+3 pawns, kings anywhere, both orientations; one heavy.sh slot at a time.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K43
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
cd $D
for job in "cyl 6 0" "cyl 7 0" "cyl 8 0" "cyl 9 0" "flat 7 0" "flat 7 1" "flat 8 0" "flat 8 1" "flat 8 2"; do
  set -- ${=job}
  tag=${1}${2}x6_F4_off$3_33
  [[ -f logs/$tag.done ]] && continue
  $H ./bin/plocal43 --kind $1 --W $2 --H 6 --F 4 --off $3 --nw 3 --nb 3 --mode both > logs/$tag.out 2> logs/$tag.err
  echo "rc=$?" > logs/$tag.done
done
echo ALLDONE > logs/main.done
