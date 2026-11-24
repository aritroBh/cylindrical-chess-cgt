#!/bin/bash
# Fast extraction using awk

OUT_DIR="research/star3_hunt"

echo "## *3+ Positions Found (for verification)"
echo
echo "| Scan | Split | Position | Setting | Nimber |"
echo "|---|---|---|---|---|"

for f in "$OUT_DIR"/*.tsv; do
    name=$(basename "$f" .tsv)
    if [[ "$name" == *"pilot"* ]]; then continue; fi
    if [[ ! -s "$f" ]]; then continue; fi
    
    awk -F'\t' -v name="$name" '
    NR == 1 { next }
    {
        pos = $1
        for (i = 4; i <= 12; i++) {
            if ($i ~ /^N,[0-9]+$/) {
                split($i, a, ",")
                nimber = a[2]
                if (nimber >= 3) {
                    settings[4]="C/T"; settings[5]="C/off"; settings[6]="C/aware"
                    settings[7]="M/T"; settings[8]="M/off"; settings[9]="M/aware"
                    settings[10]="O/T"; settings[11]="O/off"; settings[12]="O/aware"
                    print "| " name " | " pos " | " settings[i] " | *" nimber " |"
                }
            }
        }
    }' "$f"
done

echo
echo "## *2 Positions on Cylinders (C/aware = count/epon/aware)"
echo
echo "| Scan | Split | Position |"
echo "|---|---|---|"

for f in "$OUT_DIR"/cylinder_w*p*.tsv; do
    name=$(basename "$f" .tsv)
    if [[ "$name" == *"pilot"* ]]; then continue; fi
    if [[ ! -s "$f" ]]; then continue; fi
    
    awk -F'\t' -v name="$name" '
    NR == 1 { next }
    {
        pos = $1
        # C/aware is column 6 (index 3+2=5 in 0-indexed, but awk is 1-indexed so $6)
        if ($6 == "N,2") {
            print "| " name " | " pos " |"
        }
    }' "$f"
done

echo
echo "## *3+ Positions under Opponent Race Rule"
echo
echo "| Scan | Split | Position | Setting | Nimber |"
echo "|---|---|---|---|---|"

for f in "$OUT_DIR"/*.tsv; do
    name=$(basename "$f" .tsv)
    if [[ "$name" == *"pilot"* ]]; then continue; fi
    if [[ ! -s "$f" ]]; then continue; fi
    
    awk -F'\t' -v name="$name" '
    NR == 1 { next }
    {
        pos = $1
        # Opponent settings: columns 10, 11, 12 (O/T, O/off, O/aware)
        if ($10 ~ /^N,[0-9]+$/) {
            split($10, a, ",")
            if (a[2] >= 3) print "| " name " | " pos " | O/T | *" a[2] " |"
        }
        if ($11 ~ /^N,[0-9]+$/) {
            split($11, a, ",")
            if (a[2] >= 3) print "| " name " | " pos " | O/off | *" a[2] " |"
        }
        if ($12 ~ /^N,[0-9]+$/) {
            split($12, a, ",")
            if (a[2] >= 3) print "| " name " | " pos " | O/aware | *" a[2] " |"
        }
    }' "$f"
done