#!/bin/zsh
# K55: memory and size of one solve (T = 0, convention N) for each group, both solvers, before any batch
cd "$(dirname $0)"
echo "$$ run_measure.sh $(date)" >> pids.log
for g in G8:8 G9:9 G10:10 H10:10; do n=${g%%:*}; w=${g##*:}
  /usr/bin/time -l src/za_k55 $w 6 roots_$n.txt t0.txt N > logs/m_za_$n.out 2> logs/m_za_$n.err
  /usr/bin/time -l src/rz_k55 $w 6 roots_$n.txt t0.txt N > logs/m_rz_$n.out 2> logs/m_rz_$n.err
done
echo done > logs/measure.done
