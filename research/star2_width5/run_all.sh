#!/bin/bash
# Run the missing scope: flat width 5, exactly 8 pawns, all nine settings.
# Split by pawn split (nw, nb); two jobs at a time, one CPU core each.
set -u
cd .
OUT=research/star2_width5
BIN=$OUT/frontier_split

run_one () {
    local nw=$1 nb=$2
    echo "[$(date +%H:%M:%S)] start split ${nw}+${nb}"
    /usr/bin/time -p "$BIN" --flat --width 5 --min 8 --max 8 --nw "$nw" --nb "$nb" \
        > "$OUT/split_${nw}_${nb}.tsv" 2> "$OUT/split_${nw}_${nb}.log"
    echo "[$(date +%H:%M:%S)] done split ${nw}+${nb}"
}

# pairs: (1,7)+(2,6), then (3,5)+(4,4), then (5,3)+(6,2), then (7,1)
run_one 1 7 & p1=$!
run_one 2 6 & p2=$!
wait $p1 $p2

run_one 3 5 & p1=$!
run_one 4 4 & p2=$!
wait $p1 $p2

run_one 5 3 & p1=$!
run_one 6 2 & p2=$!
wait $p1 $p2

run_one 7 1
echo "all splits complete"
