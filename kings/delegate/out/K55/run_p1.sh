#!/bin/zsh
# K55 part 1: the other over-type exact groups of K45 against K47's 275 test games, convention N, both solvers
cd "$(dirname $0)"
echo "$$ run_p1.sh $(date)" >> pids.log
./capped.sh logs/p1_za_G8reg.out logs/p1_za_G8reg.err src/za_k55 8 6 ../K47/roots8.txt tests275.txt N   # regression: must equal K47 logs/full_A_N.out
for g in H10:10 G9:9 G10:10; do n=${g%%:*}; w=${g##*:}
  ./capped.sh logs/p1_za_$n.out logs/p1_za_$n.err src/za_k55 $w 6 roots_$n.txt tests275.txt N
  ./capped.sh logs/p1_rz_$n.out logs/p1_rz_$n.err src/rz_k55 $w 6 roots_$n.txt tests275.txt N
done
echo done > logs/p1.done
