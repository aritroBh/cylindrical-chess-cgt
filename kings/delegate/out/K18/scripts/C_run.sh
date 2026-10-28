#!/bin/zsh
# chess (not P-model) check: officer cap 1, promotion to Q only, small zero contexts (one White and one Black context pawn)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18
nice -n 15 bin/kp --board cyl:8x6 --ep on --promote Q --cap 1 --threads 2 < logs/C_in.txt > logs/C_out.txt 2> logs/C_err.txt
