#!/bin/bash
# independent counter vs tw --count on small cases at several R
cd "$(dirname "$0")"
for a in "3 1 5 2 3" "3 0 7 3 3" "3 1 10 2 3" "3 0 10 3 3" "3 1 12 2 3" "4 0 6 3 3" "4 1 9 2 3" "4 0 11 2 3" "4 1 12 2 2" "5 1 6 3 3" "5 0 7 2 4" "5 1 10 2 3" "3 1 8 3 4"; do
  set -- $a
  x=$(nice -n 15 python3 indep_count.py $a | sed 's/.*roots=//'); y=$(./tw --scan $a --count | sed 's/.*roots=//')
  echo "F=$1 wrap=$2 R=$3 split=$4+$5 indep=$x tw=$y $([ "$x" = "$y" ] && echo OK || echo DIFF)"
done
