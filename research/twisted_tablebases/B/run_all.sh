#!/bin/bash
# Reproduce everything in this folder: about 10 minutes, two processes at a time, each under nice -n 15,
# peak memory about 480 MB per process.  Large table dumps go to work/ (about 1.4 GB); delete it afterwards.
cd "$(dirname "$0")" || exit 1
cc -O2 -Wall -o twist twist.c || exit 1
mkdir -p results work/geo

# 1. solve all 11 materials on each board (self-test, geometry report, symmetry test, table dump)
solve() { for g in "$@"; do nice -n 15 ./twist "$g" all -g -s -d work -G "work/geo/$g.txt" > "results/$g.txt"; done; }
solve plane cyl torus &
solve mobius klein rp2 &
wait

# 2. ray-rule sensitivity (naive variants 1 and 2) on the three new boards
variant() { for g in mobius klein rp2; do nice -n 15 ./twist "$g" all -r "$1" > "results/${g}_ray$1.txt"; done; }
variant 1 &
variant 2 &
wait

# 3. independent check (separate geometry code and brute-force rules, Python)
check_geometry() { for g in plane cyl torus mobius klein rp2; do nice -n 15 python3 -I verify.py "$g" geometry "work/geo/$g.txt"; done; }
check_geometry > results/verify_geometry.txt
check_tables() { for g in "$@"; do for m in Q R B N QR RR QQ BB NN BN RB; do nice -n 15 python3 -I verify.py "$g" "$m" work 150000 7; done; done; }
check_tables plane cyl torus > results/verify_150k_a.txt &
check_tables mobius klein rp2 > results/verify_150k_b.txt &
wait
cat results/verify_150k_a.txt results/verify_150k_b.txt > results/verify_150k.txt
rm -f results/verify_150k_a.txt results/verify_150k_b.txt
# optional, about 20 minutes: 600000 samples for each 4-man table on the new boards
#   for g in mobius klein rp2; do for m in QR RR QQ BB NN BN RB; do nice -n 15 python3 -I verify.py $g $m work 600000 11; done; done > results/verify_600k.txt

# 4. tables for the report (stdout)
python3 -I mkreport.py
