#!/bin/zsh
# K26: the 8 roots with full move lists of Z_B, Z_C and their mirrors, kpp (--pmodel) and ref3m, on the boards named below. Output audit/movelists.txt
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
roots() { # wk1 wk2 bk1 bk2 pawns
  for w in $1 $2; do for b in $3 $4; do for s in w b; do echo "K$w k$b $5 $s -"; done; done; done; }
{
for spec in "ZB b2 c3 a4 b5 Pa3 Pb4 pb3 pc4" "ZBm a3 b2 b5 c4 Pb4 Pc3 pa4 pb3" "ZC c2 c3 a4 a5 Pa2 Pc4 pa3 pc5" "ZCm a2 a3 c4 c5 Pa4 Pc2 pa5 pc3"; do
  set -- ${=spec}; g=$1; shift
  for board in flat:7x6 cyl:7x6 cyl:8x6; do
    echo "### $g $board  (kings $1 $2 / $3 $4; pawns $5 $6 $7 $8)"
    roots $1 $2 $3 $4 "$5 $6 $7 $8" > /tmp/k26_roots_$$.txt
    echo "-- kpp --pmodel (White-view value of the position after each move)"
    nice -n 15 $D/bin/kpp --board $board --ep on --promote QRBN --cap 1 --pmodel --moves < /tmp/k26_roots_$$.txt 2>/dev/null
    echo "-- ref3m"
    b=${board/flat:/flat}
    nice -n 15 $D/bin/ref3m --board $b --moves < /tmp/k26_roots_$$.txt 2>/dev/null | grep ' | '
  done
done
} > $D/audit/movelists.txt
rm -f /tmp/k26_roots_$$.txt
