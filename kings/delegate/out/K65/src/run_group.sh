#!/bin/zsh
# K65: checks of one exact over group on flat 8x8: Definition 4.8 again (ref3m and kp_p --pmodel through def48.py),
# (B1) at every non-shuttle Black root move (vgsum59 --lowmem under the sum's rule; pr57 (N1), which implies (B1)).
# Every process under the 2.2 GB watchdog; the solvers go through heavy.sh (def48.py calls it itself).
# usage: run_group.sh <tag> "<pieces with the Black king on z0>" <z1>
cd "$(dirname $0)/.."
tag=$1; G=$2; z1=$3; mkdir -p logs/grp
for s in ref3m kpp; do
  python3 src/def48.py $s flat 8 8 b "$G" $z1 ${tag}_$s > logs/grp/${tag}_def48_$s.txt 2>&1 &
  P=$!; echo "$P def48.py $tag $s $(date +%H:%M:%S)" >> pids.log
  zsh src/watch3.sh $P ${tag}_def48_$s & Wd=$!; echo "$Wd watch.sh ${tag}_def48_$s" >> pids.log
  wait $P; wait $Wd
done
zsh src/hrun3.sh grp/${tag}_vgsum bin/vgsum59 --lowmem --board flat:8x8 --root "$G" --shuttle $z1
zsh src/hrun3.sh grp/${tag}_pr57 bin/pr57 --board flat:8x8 --root "$G" --shuttle $z1 --orient over
python3 src/cmp_p1.py logs/grp/${tag}_vgsum.out logs/grp/${tag}_pr57.out $tag > logs/grp/${tag}_cmp.txt 2>&1
