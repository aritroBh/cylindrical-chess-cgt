#!/bin/zsh
# K56: P values of the sampled nodes by kp_p --pmodel (K44's kp_p10.c), for comparison with pr56.
cd "$(dirname $0)"
while read name board sh rest; do
  awk -F' [|] ' '{print $1}' val/$name.mine > val/$name.in
  ./hrun.sh V_$name src/kp_p10 --board $board --pmodel --cap 1 --threads 1 < val/$name.in
done < groups.txt
