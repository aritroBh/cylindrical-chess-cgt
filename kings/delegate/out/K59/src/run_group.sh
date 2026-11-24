#!/bin/zsh
# K59: full check of one over group on a flat board: Definition 4.8 (ref3m, kp_p via def48.py), (B1) (vgsum59 sum rule,
# pr57 pass game), direct sums (vgsum59 beside 63 games, pr57 beside 600 random games).
# usage: run_group.sh <tag> <W> <H> "<pieces with Black king on z0>" <z1>
cd "$(dirname $0)/.."
tag=$1; W=$2; H=$3; G=$4; z1=$5
python3 src/def48.py ref3m flat $W $H b "$G" $z1 ${tag}_ref3m > logs/${tag}_def48_ref3m.txt 2>&1
python3 src/def48.py kpp flat $W $H b "$G" $z1 ${tag}_kpp > logs/${tag}_def48_kpp.txt 2>&1
src/hrun.sh ${tag}_vgsum bin/vgsum59 --lowmem --board flat:${W}x$H --root "$G" --shuttle $z1 --tests in/T_h10.txt
src/hrun.sh ${tag}_pr57 bin/pr57 --board flat:${W}x$H --root "$G" --shuttle $z1 --orient over
src/hrun.sh ${tag}_pr57sum bin/pr57 --board flat:${W}x$H --root "$G" --shuttle $z1 --orient over --sum in/rnd_all.txt
