#!/bin/zsh
# C7 ring scan for the n+3 question (default setting only), fixed scanner with cap replacement (fixed2), one process at a time under nice 15,
# memo table capped at 2^26 entries (3.76 GB). Splits with nw > nb are the colour-reversal images of nw < nb and
# are not run. Order: 10-pawn balanced splits first (existence), then 9 pawns (minimality), then the rest.
cd "${0:A:h}/.."
run_split() {  # P NW NB N
  local P=$1 NW=$2 NB=$3 N=$4 D=c7/p$1_$2_$3
  mkdir -p $D
  for ((i=0; i<N; i++)); do
    [[ -s $D/c${i}of${N}.summary.txt ]] && continue
    nice -n 15 ./frontier_split1_fixed2 --cylinder --width 7 --min $P --max $P --nw $NW --nb $NB --only-setting 2 \
      --chunk $i $N --max-entries 67108864 2> $D/c${i}of${N}.log \
      | awk -v sumfile=$D/c${i}of${N}.summary.txt -f filter.awk > $D/c${i}of${N}.hits.tsv
  done
  python3 -I fixed_rerun/merge_subchunks.py $D > $D/MERGE.txt 2>&1
  echo "[$(date +%H:%M)] done p$P $NW+$NB: $(sed -n 2p $D/MERGE.txt)" >> c7/progress.txt
}
run_split 10 5 5 1024
run_split 10 4 6 1024
run_split 9 4 5 512
run_split 10 3 7 256
run_split 9 3 6 256
run_split 9 2 7 64
run_split 10 2 8 64
run_split 9 1 8 16
run_split 10 1 9 16
echo "[$(date +%H:%M)] ALL DONE" >> c7/progress.txt
