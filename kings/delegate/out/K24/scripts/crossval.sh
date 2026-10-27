#!/bin/zsh
# usage: crossval.sh BOARD N SEED  -- compares kp_p --pmodel with mine --model p on random positions
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K24
PY="/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python"
B=$1; N=$2; S=$3; ONE=$4
W=${B#*:}; W=${W%x*}; H=${B#*x}
$PY $D/scripts/gen_random.py $W $H $N $S $ONE > $D/rnd_$S.txt
nice -n 15 $D/kp_p --pmodel --board $B --ep on --cap 1 < $D/rnd_$S.txt 2>/dev/null | sed 's/ | \(.\) \(.\)$/ | \1/' > $D/rnd_$S.kp
nice -n 15 $D/mine --board $B --model p < $D/rnd_$S.txt 2>/dev/null > $D/rnd_$S.mine
nd=$(diff $D/rnd_$S.kp $D/rnd_$S.mine | grep -c '^<')
echo "$B seed $S: $(wc -l < $D/rnd_$S.txt) positions, $nd differ"
