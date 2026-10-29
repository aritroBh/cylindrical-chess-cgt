#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/f3/cf
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
for g in 1 4 0 5; do
  $H perl -e 'alarm 1100; exec @ARGV' ../kpp --board cyl:8x8 --ep on --cap 0 --pmodel < a8x8s.g$g.in > a8x8s.g$g.out 2> a8x8s.g$g.err
  echo "done g$g exit=$? lines=$(wc -l < a8x8s.g$g.out) $(date +%T)" >> a8x8s.progress
done
cat a8x8s.g1.out a8x8s.g4.out a8x8s.g0.out a8x8s.g5.out > a8x8s.out; PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames /Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python ../conf2.py cmp a8x8s a8x8s.out > a8x8s.cmp.txt
echo finished >> a8x8s.progress
