#!/bin/zsh
# referee enumeration queue 2 (relative paths; run from verify/)
for job in "10 0,1,5" "10 0,2,4" "10 0,2,5" "8 0,1,5" "8 0,2,4" "8 0,2,5" "7 0,1,5" "7 0,2,4" "7 0,2,5"; do
  set -- ${=job}
  ../../../heavy.sh ./r45 enum cyl:$1x6 $2 3 3 > enum_$1_${2//,/}.out 2> enum_$1_${2//,/}.err
done
echo done > queue2.done
