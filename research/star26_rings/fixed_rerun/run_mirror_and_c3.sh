#!/bin/zsh
# Fixed-binary re-runs of the remaining crash artifacts: C3 p10 9+1 (all nine settings; ib/iw overflow in the
# original) and the C6 p9 5+4 mirror split (default setting), one process at a time, table capped at 2^26 entries.
cd "${0:A:h}/.."
nice -n 15 ./frontier_split1_fixed --cylinder --width 3 --min 10 --max 10 --nw 9 --nb 1 \
  2> fixed_rerun/cyl_w3_p10_9_1_fixed.log | awk -v sumfile=fixed_rerun/cyl_w3_p10_9_1_fixed.summary.txt -f filter.awk \
  > fixed_rerun/cyl_w3_p10_9_1_fixed.hits.tsv
D=fixed_rerun/w6_p9_5_4_sub128
for i in {0..127}; do
  [[ -s $D/c${i}of128.summary.txt ]] && continue
  nice -n 15 ./frontier_split1_fixed --cylinder --width 6 --min 9 --max 9 --nw 5 --nb 4 --only-setting 2 \
    --chunk $i 128 --max-entries 67108864 2> $D/c${i}of128.log \
    | awk -v sumfile=$D/c${i}of128.summary.txt -f filter.awk > $D/c${i}of128.hits.tsv
done
python3 -I fixed_rerun/merge_subchunks.py $D > $D/MERGE.txt 2>&1
echo done > $D/ALL_DONE
