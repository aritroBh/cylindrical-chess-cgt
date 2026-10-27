#!/bin/zsh
# run_round.sh R [deadline_seconds]: two rgf workers (nice 15) on cand_rR_a.txt / cand_rR_b.txt, then wait.
R=$1
cd "${0:A:h}"
export TBITS=23 NODELIM=4000000 EARLYSTOP=1 DEADLINE_S=${2:-3000}
nice -n 15 ./rgf solve 7 < cand_r${R}_a.txt > out_r${R}_a.txt 2> err_r${R}_a.txt &
nice -n 15 ./rgf solve 7 < cand_r${R}_b.txt > out_r${R}_b.txt 2> err_r${R}_b.txt &
wait
echo "round $R workers finished $(date +%H:%M:%S)"
