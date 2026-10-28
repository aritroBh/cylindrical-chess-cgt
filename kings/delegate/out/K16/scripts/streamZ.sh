#!/bin/zsh
# after stream X: sharper G_omega (KV=1) exhaustive sweeps, and the control KV=2 (omega king may not move in G_omega)
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16
S=$D/scripts
while kill -0 $(cat $D/logs/pid_streamX) 2>/dev/null; do sleep 30; done
$S/run_ex.sh cyl:6x6 3 3 2 EXKV1_c66_33 --kv 1
$S/run_ex.sh flat:6x6 3 3 8 EXKV1_f66_33 --kv 1
$S/run_ex.sh cyl:7x6 3 3 4 EXKV1_c76_33 --kv 1
$S/run_ex.sh cyl:6x6 3 3 2 EXKV2_c66_33 --kv 2
$S/run_ex.sh flat:6x6 3 3 8 EXKV2_f66_33 --kv 2
