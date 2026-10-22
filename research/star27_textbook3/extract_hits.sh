#!/bin/sh
# T27 step 1: stream the five T24 split files (flat, 6 files, 8 pawns) and keep every row whose nimber is >= 3
# in a count or mover column.  TSV columns (1-based): 1 position, 2 width, 3 npawns, then
#   4 C/T  5 C/off  6 C/aware  7 M/T  8 M/off  9 M/aware  10 O/T  11 O/off  12 O/aware   (each "outcome,nimber").
# Output: all_hits.tsv (one row per hit cell) and opponent_hit_counts.txt (the opponent columns are counted only).
# Run from the project root:  sh research/star27_textbook3/extract_hits.sh
D=research/star27_textbook3
S=research/star3_hunt
printf 'position\twidth\tnpawns\tsetting\toutcome\tnimber\tsource_file\n' > $D/all_hits.tsv
: > $D/opponent_hit_counts.txt
for s in 2_6 3_5 4_4 5_3 6_2; do
  awk -F'\t' -v src=research/star3_hunt/flat_w6p8_$s.tsv '
    BEGIN { split("count/epon count/epoff count/epon/aware mover/epon mover/epoff mover/epon/aware opponent/epon opponent/epoff opponent/epon/aware", nm, " ") }
    /^#/ { next }
    { for (i = 4; i <= 12; i++) { n = split($i, a, ","); if (n == 2 && a[2] + 0 >= 3) {
        if (i <= 9) print $1 "\t" $2 "\t" $3 "\t" nm[i-3] "\t" a[1] "\t" a[2] "\t" src;
        else opp[nm[i-3]]++ } } }
    END { for (k in opp) print src "\t" k "\t" opp[k] > "/dev/stderr" }' $S/flat_w6p8_$s.tsv 2>> $D/opponent_hit_counts.txt >> $D/all_hits.tsv
done
