#!/bin/zsh
# usage: xcheck.sh W H F wmax bmax   -> compares grp.c with pycheck.py over the 4 variants
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15
W=$1;H=$2;F=$3;wm=$4;bm=$5
for il in 0 1; do for pa in 0 1; do
  fl=""; [[ $il == 1 ]] && fl="$fl --ignore-leak"; [[ $pa == 1 ]] && fl="$fl --allow-passer"
  tag=${W}${H}_${F}_${wm}${bm}_il${il}_pa${pa}
  ./grp --W $W --H $H --F $F --wmax $wm --bmax $bm ${=fl} --dumproots pyv/c_$tag.tsv --out pyv/x > /dev/null 2>&1
  python3 pycheck.py $W $H $F $wm $bm pyv/p_$tag.tsv $il $pa 2>/dev/null
  python3 - pyv/c_$tag.tsv pyv/p_$tag.tsv $tag <<'PY'
import sys
from collections import Counter
def load(fn):
    d={}
    for l in open(fn):
        pos,c=l.rstrip('\n').split('\t')
        toks=pos.split()
        key=(toks[0],toks[1],tuple(sorted(toks[2:-2])))
        d[key]=c
    return d
a=load(sys.argv[1]); b=load(sys.argv[2])
diff=[k for k in a if a.get(k)!=b.get(k)]
print(sys.argv[3],'roots C',len(a),'roots Py',len(b),'label mismatches',len(diff)+len(set(b)-set(a)), dict(Counter(a.values())))
for k in diff[:5]: print('  DIFF',k,a[k],b.get(k))
PY
done; done
