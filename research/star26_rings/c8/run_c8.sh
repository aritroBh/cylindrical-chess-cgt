#!/bin/zsh
# C8 ring scan for the n+3 question (default setting), fixed2 scanner, one process at a time under nice 15,
# memo table capped at 2^26 entries. Splits with nw > nb are colour-reversal images and are not run.
# First ring *2 on C8: <= 8 pawns none (earlier scan), 11 pawns exist (wall family, T41). This checks 9 and 10.
cd "${0:A:h}/.."
run_split() {  # P NW NB N
  local P=$1 NW=$2 NB=$3 N=$4 D=c8/p$1_$2_$3
  mkdir -p $D
  for ((i=0; i<N; i++)); do
    [[ -s $D/c${i}of${N}.summary.txt ]] && continue
    nice -n 15 ./frontier_split1_fixed2 --cylinder --width 8 --min $P --max $P --nw $NW --nb $NB --only-setting 2 \
      --chunk $i $N --max-entries 67108864 2> $D/c${i}of${N}.log \
      | awk -v sumfile=$D/c${i}of${N}.summary.txt -f filter.awk > $D/c${i}of${N}.hits.tsv
  done
  python3 -I fixed_rerun/merge_subchunks.py $D > $D/MERGE.txt 2>&1
  echo "[$(date +%H:%M)] done p$P $NW+$NB: $(sed -n 2p $D/MERGE.txt)" >> c8/progress.txt
}
run_split 9 4 5 4096
run_split 9 3 6 1024
run_split 9 2 7 256
run_split 9 1 8 64
run_split 10 5 5 4096
run_split 10 4 6 4096
run_split 10 3 7 1024
run_split 10 2 8 256
run_split 10 1 9 64
echo "[$(date +%H:%M)] ALL DONE" >> c8/progress.txt
# compress the per-chunk logs once merged (they are only needed for audits)
for d in c8/p*_*; do tar -cf - $d/*.log 2>/dev/null | zstd -q -T2 -3 -o $d/logs.tar.zst && rm -f $d/*.log; done
