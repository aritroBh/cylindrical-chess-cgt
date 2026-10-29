#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/f3/cf
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
$H perl -e 'alarm 1100; exec @ARGV' ../kpp --board cyl:8x8 --ep on --cap 0 --pmodel < d8x8.in > d8x8.out 2> d8x8.err
echo "done d88 exit=$? $(date +%T)" >> d8x8.progress
