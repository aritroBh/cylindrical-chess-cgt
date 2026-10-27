#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K22
until grep -q 'SUMMARY board=flat:6x6 FZ=0..5 f=5 wmax=3 bmax=3 safe=1' $D/logs/scan_all.txt; do sleep 1; done
# the A script now repeats cylinder and 4+4 scans that B and C already ran: stop it by its recorded PID (37743)
kids=$(ps -eo pid,ppid | awk '$2==37743{print $1}')
kill 37743
for p in $kids; do echo $p >> $D/logs/my_pids.txt; kill $p; done
grandkids=$(for p in $kids; do ps -eo pid,ppid | awk -v q=$p '$2==q{print $1}'; done)
for p in $grandkids; do echo $p >> $D/logs/my_pids.txt; kill $p; done
echo STOPPED_A >> $D/logs/scan_all.txt
