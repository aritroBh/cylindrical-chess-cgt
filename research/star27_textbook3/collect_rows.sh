#!/bin/sh
# T27 step 1b: list the distinct hit positions (hit_positions.txt) and pull their complete 9-column scanner rows
# out of the 4+4 split file (scanner_rows.tsv).  Run after extract_hits.sh, from the project root.
D=research/star27_textbook3
awk -F'\t' 'NR>1 {print $1}' $D/all_hits.tsv | sort -u > $D/hit_positions.txt
for s in 2_6 3_5 4_4 5_3 6_2; do
  awk -F'\t' 'NR==FNR {want[$1]=1; next} ($1 in want)' $D/hit_positions.txt research/star3_hunt/flat_w6p8_$s.tsv
done > $D/scanner_rows.tsv
