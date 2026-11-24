#!/bin/zsh
cd "$(dirname $0)"
../../../heavy.sh /usr/bin/time -l ./kp_p10 --board cyl:10x6 --pmodel --cap 1 --moves --threads 1 < logs/roots.kin > logs/roots.kpp 2> logs/roots.kpp.err &
P=$!; echo "$P heavy.sh time kp_p10 roots $(date)" >> pids.log; wait $P
