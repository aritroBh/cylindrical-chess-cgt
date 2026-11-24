#!/bin/bash
# Fast analysis using awk

OUT_DIR="research/star3_hunt"

# Settings: count/epon, count/epoff, count/epon/aware, mover/epon, mover/epoff, mover/epon/aware, opponent/epon, opponent/epoff, opponent/epon/aware
# Columns 4-12 in TSV (1-indexed)

analyze_file() {
    local file=$1
    local name=$(basename "$file" .tsv)
    
    # Skip pilot files
    if [[ "$name" == *"pilot"* ]]; then
        return
    fi
    
    echo "=== $name ==="
    awk -F'\t' '
    NR == 1 { next }
    {
        total++
        for (i = 4; i <= 12; i++) {
            if ($i ~ /^N,[0-9]+$/) {
                split($i, a, ",")
                nimber = a[2]
                if (nimber == 2) star2[i]++
                else if (nimber >= 3) star3plus[i]++
                if (nimber > max_nimber[i]) max_nimber[i] = nimber
            }
        }
    }
    END {
        settings[4]="C/T"; settings[5]="C/off"; settings[6]="C/aware"
        settings[7]="M/T"; settings[8]="M/off"; settings[9]="M/aware"
        settings[10]="O/T"; settings[11]="O/off"; settings[12]="O/aware"
        printf "  Total roots: %d\n", total
        printf "  %-10s %12s %6s %6s %6s\n", "Setting", "Roots", "*2", "*3+", "Max*"
        for (i = 4; i <= 12; i++) {
            roots = star2[i] + star3plus[i]  # This is wrong, need actual roots per setting
            printf "  %-10s %12s %6d %6d %6d\n", settings[i], total, star2[i]+0, star3plus[i]+0, max_nimber[i]+0
        }
    }' "$file"
    echo
}

# Process each scan group
echo "===== Flat width 4, 8 pawns ====="
for f in "$OUT_DIR"/flat_w4p8_*.tsv; do
    analyze_file "$f"
done

echo "===== Flat width 4, 9 pawns ====="
for f in "$OUT_DIR"/flat_w4p9_*.tsv; do
    analyze_file "$f"
done

echo "===== Flat width 5, 9 pawns ====="
for f in "$OUT_DIR"/flat_w5p9_*.tsv; do
    analyze_file "$f"
done

echo "===== Flat width 6, 7 pawns ====="
for f in "$OUT_DIR"/flat_w6p7_*.tsv; do
    analyze_file "$f"
done

echo "===== Flat width 6, 8 pawns ====="
for f in "$OUT_DIR"/flat_w6p8_*.tsv; do
    analyze_file "$f"
done

echo "===== Cylinder C3, 6-8 pawns ====="
for f in "$OUT_DIR"/cylinder_w3p*.tsv; do
    analyze_file "$f"
done

echo "===== Cylinder C4, 6-8 pawns ====="
for f in "$OUT_DIR"/cylinder_w4p*.tsv; do
    analyze_file "$f"
done

echo "===== Cylinder C5, 7-9 pawns ====="
for f in "$OUT_DIR"/cylinder_w5p*.tsv; do
    analyze_file "$f"
done

echo "===== Cylinder C6, 7-8 pawns ====="
for f in "$OUT_DIR"/cylinder_w6p*.tsv; do
    analyze_file "$f"
done