#!/bin/zsh
# exhaustive tiny pawn sets (direct, below one CPU-minute each): small.sh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16
for b in cyl:6x6 cyl:7x6 cyl:8x6 flat:6x6 flat:7x6; do
  for cfg in "1 0" "1 1" "2 0"; do
    set -- ${=cfg}
    t=work/small/$(echo $b|tr ':' '_')_$1$2
    $D/work/chk --board $b --mode enum --maxw $1 --maxb $2 --out $D/$t 2>/dev/null
    n=$(wc -l < $D/$t.pos)
    nice -n 15 $D/work/kpp --board $b --pmodel < $D/$t.pos > $D/$t.res 2>/dev/null
    echo "$b $1+$2 n=$n $(python3 $D/scripts/cmp.py $D/$t.pos $D/$t.meta $D/$t.res $D/$t.viol | cut -c1-330)"
  done
done
