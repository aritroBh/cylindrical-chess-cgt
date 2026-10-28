#!/bin/zsh
# chess (officer cap 1, promotion to Q only) on the failing contexts of ES and on controls
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18
nice -n 15 bin/kp --board cyl:8x6 --ep on --promote Q --cap 1 --threads 2 < logs/C2_in.txt > logs/C2_out.txt 2> logs/C2_err.txt
