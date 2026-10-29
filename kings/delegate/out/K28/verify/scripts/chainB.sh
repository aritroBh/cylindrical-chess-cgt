#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K28/verify
H=scripts/hrun.sh
$H rowsF_kq3_cap2 5400 logs/rowsF.in bin/kq3 --cap 2 --bound AB --moves --threads 3
sed -n 2p logs/children5.in > /dev/null
printf 'Kc4 Pa3 Pb4 ka4 pb3 b -\nKc3 Pb4 ka3 pb3 pc4 w -\n' > logs/r34.in
$H r34_kp_cap2 5400 logs/r34.in bin/kp --board flat:7x6 --ep on --promote QRBN --cap 2 --threads 2 --moves
