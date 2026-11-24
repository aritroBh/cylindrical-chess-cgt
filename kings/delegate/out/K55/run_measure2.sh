#!/bin/zsh
# K55: memory of one solve with the largest test game (m = 49 of the 275 on cyl:10x6; m = 90 of the new battery on cyl:8x6)
cd "$(dirname $0)"
echo "$$ run_measure2.sh $(date)" >> pids.log
./capped.sh logs/m2_za_G10.out logs/m2_za_G10.err src/za_k55 10 6 roots_G10.txt t_big275.txt N
./capped.sh logs/m2_rz_G10.out logs/m2_rz_G10.err src/rz_k55 10 6 roots_G10.txt t_big275.txt N
./capped.sh logs/m2_za_G8.out logs/m2_za_G8.err src/za_k55 8 6 roots_G8.txt t_big55.txt N
./capped.sh logs/m2_rz_G8.out logs/m2_rz_G8.err src/rz_k55 8 6 roots_G8.txt t_big55.txt N
echo done > logs/measure2.done
