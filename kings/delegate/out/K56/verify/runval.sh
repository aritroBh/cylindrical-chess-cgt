#!/bin/zsh
# K56 referee: P values of vg's sampled states by kp_p --pmodel (K44's kp_p10.c), through heavy.sh.
cd "$(dirname $0)"
for g in H10:cyl:10x6 ZO:cyl:8x6; do name=${g%%:*}; board=${g#*:}
  awk -F' [|] ' '{print $1}' logs/$name.sample > logs/$name.kin
  ../../../heavy.sh /usr/bin/time -l ./kp_p10 --board $board --pmodel --cap 1 --threads 1 < logs/$name.kin > logs/$name.kpp 2> logs/$name.kpp.err &
  P=$!; echo "$P heavy.sh time kp_p10 $name $(date)" >> pids.log; wait $P
  paste -d'|' logs/$name.sample logs/$name.kpp | awk -F'|' -v n=$name '{m=$2; gsub(/ /,"",m); split($4,a," "); c[m]++; if (m!=a[1]||a[1]!=a[2]) d++; t++} END{print n": "t" states compared ("c["W"]+0" W, "c["D"]+0" D, "c["L"]+0" L), "d+0" differ"}'
done
