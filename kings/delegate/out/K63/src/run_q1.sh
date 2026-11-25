#!/bin/zsh
# K63 question 1: chess (model C) on flat 8x8 at cap 1, roots and q's of a group with every move valued.
# usage: src/run_q1.sh <tag> <input file>   (run from kings/delegate/out/K63)
cd "$(dirname $0)/.."
tag=$1; I=$2; B=flat:8x8
zsh src/hrun.sh ${tag}_kp $I bin/kpsolve --board $B --ep on --promote QRBN --cap 1 --moves
zsh src/hrun.sh ${tag}_kp39r $I bin/kp39 --board $B --ep on --promote QRBN --cap 1 --refine --moves
zsh src/hrun.sh ${tag}_own_A $I bin/own39 8 8 0 0 1 1
zsh src/hrun.sh ${tag}_own_B $I bin/own39 8 8 0 1 1 1
echo done > logs/${tag}_q1.done
