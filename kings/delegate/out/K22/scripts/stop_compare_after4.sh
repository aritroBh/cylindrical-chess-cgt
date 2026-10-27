#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K22
until [ $(grep -c compared $D/logs/compare_log.txt) -ge 4 ]; do sleep 1; done
kids=$(ps -eo pid,ppid | awk '$2==11576{print $1}')
kill 11576
for p in $kids; do echo $p >> $D/logs/my_pids.txt; kill $p; done
echo "stopped run_compare_direct.sh (PID 11576) and its child after 4 chunks" >> $D/logs/compare_log.txt
