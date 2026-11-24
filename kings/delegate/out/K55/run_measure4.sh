#!/bin/zsh
# K55: rz after packing value and counter into one byte: the largest cyl:10x6 case, and a regression run against K47's referee output
cd "$(dirname $0)"
echo "$$ run_measure4.sh $(date)" >> pids.log
./capped.sh logs/m4_rz_G10.out logs/m4_rz_G10.err src/rz_k55 10 6 roots_G10.txt t_big275.txt N
./capped.sh logs/m4_rz_reg.out logs/m4_rz_reg.err src/rz_k55 8 6 roots_ref4.txt tests_ref27.txt N
echo done > logs/measure4.done
