#!/bin/bash
# regenerate every table in one file (data file, not a report)
cd "$(dirname "$0")"
{
echo "=== 1. scan (frontier_split1_fixed2, flat, default setting, edge files occupied, mirror-reduced), every width 1..8 and 2..7 pawns"; python3 -I tabulate.py
echo; echo "=== 1b. colour-reversal twin consistency"; python3 -I twin_check.py
echo; echo "=== 2. width 9 (scan_wide, 128-bit masks), 7 pawns: variant S and variant R"; for f in wide/w9p7_*.summary wide/R_w9p7_*.summary; do echo "$f: $(tr '\n' ' ' < $f | cut -c1-120)"; done
echo; echo "=== 3. sum of parts (cylcgt sum model), any width"; cat sums_out.txt
echo; echo "=== 4. gapped rows: scanner vs sum of cylcgt part values"; python3 -I aggregate_gapped.py
echo; echo "=== 5. connected rows: cylcgt vs scanner"; python3 -I aggregate_conn.py
echo; echo "=== 6. e.p. variant S vs R"; cat sr_table.txt
} > FINAL_TABLES.txt 2>&1
echo written FINAL_TABLES.txt
