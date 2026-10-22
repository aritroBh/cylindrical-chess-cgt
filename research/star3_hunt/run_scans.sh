#!/bin/bash
# T24: *3 hunt and cylinder minimum for *2
# Run scans with nice -n 10, at most 3 processes at once, each under 40 minutes.
# Split by (nw, nb) as T21's run_all.sh does.

set -u
cd /Users/aritro/Downloads/Research/Chessendgames
BIN=research/star3_hunt/frontier_split
OUT=research/star3_hunt

run_one() {
    local geometry=$1 width=$2 minp=$3 maxp=$4 nw=$5 nb=$6
    local tag="${geometry}_w${width}p${maxp}_${nw}_${nb}"
    echo "[$(date +%H:%M:%S)] start $tag"
    /usr/bin/time -p nice -n 10 "$BIN" --$geometry --width "$width" --min "$minp" --max "$maxp" --nw "$nw" --nb "$nb" \
        > "$OUT/${tag}.tsv" 2> "$OUT/${tag}.log"
    echo "[$(date +%H:%M:%S)] done $tag"
}

wait_for_jobs() {
    for pid in "$@"; do
        wait $pid
    done
}

# ============================================================
# 1. Flat width 4 with 8 pawns
# ============================================================
echo "=== Flat width 4, 8 pawns ==="
run_one flat 4 8 8 1 7 & p1=$!
run_one flat 4 8 8 2 6 & p2=$!
run_one flat 4 8 8 3 5 & p3=$!
wait_for_jobs $p1 $p2 $p3

run_one flat 4 8 8 4 4 & p1=$!
run_one flat 4 8 8 5 3 & p2=$!
run_one flat 4 8 8 6 2 & p3=$!
wait_for_jobs $p1 $p2 $p3

run_one flat 4 8 8 7 1
echo "Flat width 4, 8 pawns complete"

# ============================================================
# 2. Flat width 4 with 9 pawns
# ============================================================
echo "=== Flat width 4, 9 pawns ==="
run_one flat 4 9 9 2 7 & p1=$!
run_one flat 4 9 9 3 6 & p2=$!
run_one flat 4 9 9 4 5 & p3=$!
wait_for_jobs $p1 $p2 $p3

run_one flat 4 9 9 5 4 & p1=$!
run_one flat 4 9 9 6 3 & p2=$!
run_one flat 4 9 9 7 2 & p3=$!
wait_for_jobs $p1 $p2 $p3
echo "Flat width 4, 9 pawns complete"

# ============================================================
# 3. Flat width 5 with 9 pawns (skip 4+5 and 5+4 - over 6 CPU-hours)
# ============================================================
echo "=== Flat width 5, 9 pawns (skipping 4+5, 5+4) ==="
run_one flat 5 9 9 2 7 & p1=$!
run_one flat 5 9 9 3 6 & p2=$!
run_one flat 5 9 9 7 2 & p3=$!
wait_for_jobs $p1 $p2 $p3

run_one flat 5 9 9 6 3
echo "Flat width 5, 9 pawns complete (4+5 and 5+4 skipped)"

# ============================================================
# 4. Flat width 6 with 7 pawns
# ============================================================
echo "=== Flat width 6, 7 pawns ==="
run_one flat 6 7 7 1 6 & p1=$!
run_one flat 6 7 7 2 5 & p2=$!
run_one flat 6 7 7 3 4 & p3=$!
wait_for_jobs $p1 $p2 $p3

run_one flat 6 7 7 4 3 & p1=$!
run_one flat 6 7 7 5 2 & p2=$!
run_one flat 6 7 7 6 1 & p3=$!
wait_for_jobs $p1 $p2 $p3
echo "Flat width 6, 7 pawns complete"

# ============================================================
# 5. Flat width 6 with 8 pawns
# ============================================================
echo "=== Flat width 6, 8 pawns ==="
run_one flat 6 8 8 2 6 & p1=$!
run_one flat 6 8 8 3 5 & p2=$!
run_one flat 6 8 8 4 4 & p3=$!
wait_for_jobs $p1 $p2 $p3

run_one flat 6 8 8 5 3 & p1=$!
run_one flat 6 8 8 6 2 & p2=$!
wait_for_jobs $p1 $p2
echo "Flat width 6, 8 pawns complete"

# ============================================================
# 6. Cylinder C3 with 6-8 pawns (rings)
# ============================================================
echo "=== Cylinder C3, 6-8 pawns ==="
run_one cylinder 3 6 6 3 3
run_one cylinder 3 7 7 3 4
run_one cylinder 3 8 8 4 4
echo "Cylinder C3 complete"

# ============================================================
# 7. Cylinder C4 with 6-8 pawns (rings)
# ============================================================
echo "=== Cylinder C4, 6-8 pawns ==="
run_one cylinder 4 6 6 3 3
run_one cylinder 4 7 7 3 4
run_one cylinder 4 8 8 4 4
echo "Cylinder C4 complete"

# ============================================================
# 8. Cylinder C5 with 7-9 pawns (rings) - skip 4+5 for 9 pawns
# ============================================================
echo "=== Cylinder C5, 7-9 pawns (skipping 4+5 for 9 pawns) ==="
run_one cylinder 5 7 7 3 4
run_one cylinder 5 8 8 4 4
run_one cylinder 5 9 9 3 6
# 4+5 for 9 pawns skipped (over 6 CPU-hours)
echo "Cylinder C5 complete"

# ============================================================
# 9. Cylinder C6 with 7-8 pawns (rings)
# ============================================================
echo "=== Cylinder C6, 7-8 pawns ==="
run_one cylinder 6 7 7 3 4
run_one cylinder 6 8 8 4 4
echo "Cylinder C6 complete"

echo "ALL SCANS COMPLETE"