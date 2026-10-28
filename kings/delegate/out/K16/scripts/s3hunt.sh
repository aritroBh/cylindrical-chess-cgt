#!/bin/zsh
# s3hunt.sh BOARD N SEED STYLE : positions where the frozen-style H3 at omega's king (S3) holds but some omega line stalemates;
# solved with kp_p.  (sim-only generation: ~20 s CPU per 2M samples)
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16
b=$1; n=$2; seed=$3; style=$4
t=$D/work/s3_$(echo $b | tr ':' '_')_$seed
nice -n 15 $D/work/chk3 --board $b --mode rand --n $n --seed $seed --maxw 3 --maxb 3 --style $style --onlystale --out $t > $t.tally 2> $t.chk
python3 - $t <<'PY'
import sys
t=sys.argv[1]
keep=[]
for lm in open(t+'.meta'):
    pos,toks=lm.rstrip('\n').split(' | ')
    ok=False
    for tok in toks.split():
        b,p,fl=tok.split(':'); a=fl.split('.')
        if int(a[0],16)&1 and len(a)>2 and a[2]=='1': ok=True
    if ok: keep.append((pos,lm))
open(t+'.s3.pos','w').write(''.join(p+'\n' for p,_ in keep))
open(t+'.s3.meta','w').write(''.join(l for _,l in keep))
print("S3-with-stalemate-line positions:",len(keep))
PY
if [[ -s $t.s3.pos ]]; then
  nice -n 15 $D/work/kpp --board $b --pmodel < $t.s3.pos > $t.s3.res 2>/dev/null
  python3 $D/scripts/cmp.py $t.s3.pos $t.s3.meta $t.s3.res $t.s3.viol | cut -c1-400
  [[ -s $t.s3.viol ]] && { cp $t.s3.viol $D/logs/s3viol_$(echo $b | tr ':' '_')_$seed.txt; echo "violations saved"; }
fi
rm -f $t.pos $t.meta $t.s3.pos $t.s3.meta $t.s3.res $t.s3.viol $t.tally $t.chk
