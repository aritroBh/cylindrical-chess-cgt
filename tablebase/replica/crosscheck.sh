#!/bin/sh
# Cross-check the replica against ../egt_prototype.c: first the summary numbers
# each program prints, then every position of every table. Run ./run_all.sh first.
# The prototype is not modified; a copy that also writes its arrays is built in a
# temporary directory.
set -e
cd "$(dirname "$0")"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cc -O2 -Wall -Wextra -o replica replica.c
cc -O2 -o "$tmp/egt" ../egt_prototype.c
sed 's|^  solve(&T, 1, argv\[1\]);|& if (getenv("DUMP")) { FILE *f = fopen(getenv("DUMP"), "wb"); fwrite(T.w, 1, T.n, f); fwrite(T.b, 1, T.n, f); fclose(f); }|' \
  ../egt_prototype.c > "$tmp/egt_dump.c"
grep -q 'getenv("DUMP")' "$tmp/egt_dump.c"
cc -O2 -o "$tmp/egt_dump" "$tmp/egt_dump.c"
mkdir -p prototype_results
for topo in plane cyl torus; do
  for men in Q R BB BN NN RB RR QR; do
    "$tmp/egt" "$topo" "$men" > "prototype_results/${topo}_${men}.txt"
  done
done
python3 compare.py
: > position_compare.txt
for topo in plane cyl torus; do
  for men in Q R BB BN NN RB RR QR; do
    ./replica "$topo" "$men" dump "$tmp/rep" 2> /dev/null
    DUMP="$tmp/pro" "$tmp/egt_dump" "$topo" "$men" > /dev/null
    printf "%-6s K%sK  " "$topo" "$men" | tee -a position_compare.txt
    python3 compare_positions.py "$tmp/rep" "$tmp/pro" ${#men} | tee -a position_compare.txt
  done
done
