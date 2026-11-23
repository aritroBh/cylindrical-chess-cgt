#!/bin/zsh
# referee enumeration queue 1 (relative paths; run from verify/)
for job in "10 0,1,2" "10 0,1,3" "10 0,1,4" "8 0,1,2" "8 0,1,3" "8 0,1,4" "7 0,1,2" "7 0,1,3" "7 0,1,4"; do
  set -- ${=job}
  ../../../heavy.sh ./r45 enum cyl:$1x6 $2 3 3 > enum_$1_${2//,/}.out 2> enum_$1_${2//,/}.err
done
echo done > queue1.done
