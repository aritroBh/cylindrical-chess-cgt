#!/bin/zsh
# K21 chess kpsolve cap-1 attempt. Usage: run_kp_cap1.sh ; limits: 18 min wall via perl alarm.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K21
echo $$ > $D/chess/kp_wrapper.pid
cd $D
/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh perl -e 'alarm 1080; exec @ARGV' bin/kp --board cyl:7x6 --ep on --promote QRBN --cap 1 --threads 2 < chess/positions_C.txt > chess/results_C.txt 2> chess/err_C.txt
echo "exit $?" >> chess/err_C.txt
