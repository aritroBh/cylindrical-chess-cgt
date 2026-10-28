#!/bin/bash
# count the C10 root rings with 11 pawns for all ten splits (NW NB), one enum_rings process at a time, nice 15.
# columns: N P NW NB rings wall_s user_s sys_s   (enum_rings --count; no solving)
cd "$(dirname "$0")"
: > count_c10p11.txt
TIMEFORMAT='%R %U %S'
for s in "1 10" "2 9" "3 8" "4 7" "7 4" "8 3" "9 2" "10 1" "5 6" "6 5"; do
  set -- $s
  tfile=$(mktemp)
  r=$( { time nice -n 15 ../enum_rings 10 11 $1 $2 --count 2>/dev/null | tail -1 ; } 2> "$tfile" )
  set -- $s $r $(cat "$tfile")
  rm -f "$tfile"
  echo "10 11 $1 $2 $3 $4 wall_s=$5 user_s=$6 sys_s=$7" >> count_c10p11.txt
done
echo done >> count_c10p11.txt
