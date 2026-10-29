#!/bin/zsh
# usage: cmp.sh W H F wmax bmax n seed   (validates grp --nopass against kp_p --pmodel)
W=$1;H=$2;F=$3;wm=$4;bm=$5;n=$6;seed=$7
t=val_${W}x${H}_F${F}_${wm}${bm}_s${seed}
../grp --W $W --H $H --F $F --wmax $wm --bmax $bm --nopass --dumprand $n $seed > $t.mine 2>/dev/null
sed 's/ | .*//' $t.mine > $t.in
nice -n 15 ./kpp --board cyl:${W}x${H} --ep on --cap 1 --pmodel < $t.in > $t.kpp 2>/dev/null
python3 - $t <<'PY'
import sys
t=sys.argv[1]
a=[l.rstrip('\n') for l in open(t+'.mine')]
b=[l.rstrip('\n') for l in open(t+'.kpp') if not l.startswith('#')]
bad=0
for x,y in zip(a,b):
    v=x.split(' | ')[1]; A,B=y.split(' | ')[1].split()
    if not(A==B==v):
        bad+=1
        if bad<6: print('DIFF',x,'|',y)
from collections import Counter
print(t,'n=',len(a),len(b),'mismatch',bad, Counter(x.split(' | ')[1] for x in a))
PY
