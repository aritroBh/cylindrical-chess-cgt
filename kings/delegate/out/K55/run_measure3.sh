#!/bin/zsh
# K55: rz after the memory changes (bit-set levels instead of a FIFO queue, hash table freed): the two largest cases again
cd "$(dirname $0)"
echo "$$ run_measure3.sh $(date)" >> pids.log
./capped.sh logs/m3_rz_G8.out logs/m3_rz_G8.err src/rz_k55 8 6 roots_G8.txt t_big55.txt N
./capped.sh logs/m3_rz_G10.out logs/m3_rz_G10.err src/rz_k55 10 6 roots_G10.txt t_big275.txt N
echo done > logs/measure3.done
