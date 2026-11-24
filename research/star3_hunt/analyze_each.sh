#!/bin/bash
# Analyze each TSV file and save summary to a temp file

OUT_DIR="research/star3_hunt"
TMP_DIR="$OUT_DIR/analysis_tmp"
mkdir -p "$TMP_DIR"

analyze_file() {
    local file=$1
    local name=$(basename "$file" .tsv)
    
    # Skip pilot files
    if [[ "$name" == *"pilot"* ]]; then
        return
    fi
    
    local outfile="$TMP_DIR/${name}.summary"
    
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
        print "FILE=" FILENAME
        print "TOTAL=" total
        for (i = 4; i <= 12; i++) {
            print settings[i] "=" star2[i]+0 "," star3plus[i]+0 "," max_nimber[i]+0
        }
    }' "$file" > "$outfile"
    
    echo "Done: $name"
}

export -f analyze_file
export OUT_DIR TMP_DIR

# Process files in parallel (max 4 at a time)
find "$OUT_DIR" -name "*.tsv" ! -name "*pilot*" | xargs -P 4 -I {} bash -c 'analyze_file "$@"' _ {}

echo "All files processed. Aggregating..."

# Aggregate by scan group
aggregate_group() {
    local group_name=$1
    local pattern=$2
    
    echo "=== $group_name ==="
    
    local total_roots=0
    declare -A star2 star3plus max_nimber
    for i in {4..12}; do
        star2[$i]=0
        star3plus[$i]=0
        max_nimber[$i]=0
    done
    
    for f in "$TMP_DIR"/${pattern}*.summary; do
        if [[ ! -f "$f" ]]; then continue; fi
        while IFS='=' read -r key value; do
            if [[ "$key" == "TOTAL" ]]; then
                total_roots=$((total_roots + value))
            elif [[ "$key" =~ ^(C/T|C/off|C/aware|M/T|M/off|M/aware|O/T|O/off|O/aware)$ ]]; then
                IFS=',' read -r s2 s3p mn <<< "$value"
                star2[$key]=$((star2[$key] + s2))
                star3plus[$key]=$((star3plus[$key] + s3p))
                if (( mn > max_nimber[$key] )); then
                    max_nimber[$key]=$mn
                fi
            fi
        done < "$f"
    done
    
    echo "Total roots: $total_roots"
    printf "%-10s %12s %6s %6s %6s\n" "Setting" "Roots" "*2" "*3+" "Max*"
    for key in "C/T" "C/off" "C/aware" "M/T" "M/off" "M/aware" "O/T" "O/off" "O/aware"; do
        printf "%-10s %12s %6d %6d %6d\n" "$key" "$total_roots" "${star2[$key]}" "${star3plus[$key]}" "${max_nimber[$key]}"
    done
    echo
}

# Define groups
aggregate_group "Flat width 4, 8 pawns" "flat_w4p8_"
aggregate_group "Flat width 4, 9 pawns" "flat_w4p9_"
aggregate_group "Flat width 5, 9 pawns" "flat_w5p9_"
aggregate_group "Flat width 6, 7 pawns" "flat_w6p7_"
aggregate_group "Flat width 6, 8 pawns" "flat_w6p8_"
aggregate_group "Cylinder C3, 6-8 pawns" "cylinder_w3p"
aggregate_group "Cylinder C4, 6-8 pawns" "cylinder_w4p"
aggregate_group "Cylinder C5, 7-9 pawns" "cylinder_w5p"
aggregate_group "Cylinder C6, 7-8 pawns" "cylinder_w6p"

# Also print markdown table
echo "## Summary Table"
echo
echo "| Scan | Total Roots | C/T (*2/*3+/max) | C/off (*2/*3+/max) | C/aware (*2/*3+/max) | M/T (*2/*3+/max) | M/off (*2/*3+/max) | M/aware (*2/*3+/max) | O/T (*2/*3+/max) | O/off (*2/*3+/max) | O/aware (*2/*3+/max) |"
echo "|---|---|---|---|---|---|---|---|---|---|---|"

for pattern in "flat_w4p8_" "flat_w4p9_" "flat_w5p9_" "flat_w6p7_" "flat_w6p8_" "cylinder_w3p" "cylinder_w4p" "cylinder_w5p" "cylinder_w6p"; do
    # Compute totals for this pattern
    total_roots=0
    declare -A star2 star3plus max_nimber
    for key in "C/T" "C/off" "C/aware" "M/T" "M/off" "M/aware" "O/T" "O/off" "O/aware"; do
        star2[$key]=0
        star3plus[$key]=0
        max_nimber[$key]=0
    done
    
    for f in "$TMP_DIR"/${pattern}*.summary; do
        if [[ ! -f "$f" ]]; then continue; fi
        while IFS='=' read -r key value; do
            if [[ "$key" == "TOTAL" ]]; then
                total_roots=$((total_roots + value))
            elif [[ "$key" =~ ^(C/T|C/off|C/aware|M/T|M/off|M/aware|O/T|O/off|O/aware)$ ]]; then
                IFS=',' read -r s2 s3p mn <<< "$value"
                star2[$key]=$((star2[$key] + s2))
                star3plus[$key]=$((star3plus[$key] + s3p))
                if (( mn > max_nimber[$key] )); then
                    max_nimber[$key]=$mn
                fi
            fi
        done < "$f"
    done
    
    # Get group name
    case $pattern in
        flat_w4p8_) group="Flat width 4, 8 pawns" ;;
        flat_w4p9_) group="Flat width 4, 9 pawns" ;;
        flat_w5p9_) group="Flat width 5, 9 pawns (4+5,5+4 skipped)" ;;
        flat_w6p7_) group="Flat width 6, 7 pawns" ;;
        flat_w6p8_) group="Flat width 6, 8 pawns" ;;
        cylinder_w3p) group="Cylinder C3, 6-8 pawns" ;;
        cylinder_w4p) group="Cylinder C4, 6-8 pawns" ;;
        cylinder_w5p) group="Cylinder C5, 7-9 pawns (4+5 for 9 skipped)" ;;
        cylinder_w6p) group="Cylinder C6, 7-8 pawns" ;;
    esac
    
    row="| $group | $total_roots |"
    for key in "C/T" "C/off" "C/aware" "M/T" "M/off" "M/aware" "O/T" "O/off" "O/aware"; do
        row+=" ${star2[$key]}/${star3plus[$key]}/${max_nimber[$key]} |"
    done
    echo "$row"
done