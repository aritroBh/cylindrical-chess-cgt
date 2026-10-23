#!/bin/zsh
# One cylcgt process per ring (fresh memory each time); two queues in parallel, under nice 15.
cd "${0:A:h}/../../.."
q() {
  while IFS= read -r line; do
    printf '%s\n' "$line" > research/star26_rings/c8/one_$1.tsv
    nice -n 15 .venv/bin/python research/star26_rings/c8/cylcgt_p10.py research/star26_rings/c8/one_$1.tsv >> research/star26_rings/c8/cylcgt_p10_5_5.txt 2>> research/star26_rings/c8/cylcgt_p10_5_5.err
  done
  rm -f research/star26_rings/c8/one_$1.tsv
}
awk 'NR%2==1' research/star26_rings/c8/p10_5_5_reps_todo.tsv | q a &
awk 'NR%2==0' research/star26_rings/c8/p10_5_5_reps_todo.tsv | q b &
wait
echo "[$(date +%H:%M)] cylcgt reps done" >> research/star26_rings/c8/progress.txt
